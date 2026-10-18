"""Model gateway: the single door between the swarm and the LLM backends.

Responsibilities (blueprint §2, §6.4):
  * route logical tier ('flash' | 'pro') to a concrete provider,
  * account cost per call using cache-hit-aware pricing,
  * retry transient errors and fall back mock<->real when needed,
  * expose a spend hook so the global cost governor can enforce the kill-switch,
  * keep a per-trajectory ledger for cost-per-flag metrics.

Escalation is *not* a hardware switch: it is simply calling `.chat(..., tier="pro")`
with the same message list. The cascade logic that decides *when* to escalate
lives in the agent/orchestrator, not here.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from ..config import MODEL_IDS, PRICING, SETTINGS, Settings
from .providers import DeepSeekProvider, MockProvider
from .types import GatewayResponse, Usage


def price_call(tier: str, usage: Usage) -> float:
    """Cost in USD for one call, honouring the cache-hit discount."""
    p = PRICING[tier]
    return (
        usage.cache_miss_tokens / 1_000_000 * p.input_miss
        + usage.cache_hit_tokens / 1_000_000 * p.input_hit
        + usage.completion_tokens / 1_000_000 * p.output
    )


@dataclass
class Ledger:
    """Running cost/usage accumulator (per trajectory or global)."""
    calls: int = 0
    cost_usd: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_hit_tokens: int = 0
    escalations: int = 0
    by_tier: Dict[str, int] = field(default_factory=lambda: {"flash": 0, "pro": 0})

    def add(self, resp: GatewayResponse) -> None:
        self.calls += 1
        self.cost_usd += resp.cost_usd
        self.prompt_tokens += resp.usage.prompt_tokens
        self.completion_tokens += resp.usage.completion_tokens
        self.cache_hit_tokens += resp.usage.cache_hit_tokens
        self.by_tier[resp.model_tier] = self.by_tier.get(resp.model_tier, 0) + 1
        if resp.model_tier == "pro":
            self.escalations += 1


class GatewayError(RuntimeError):
    pass


class ModelGateway:
    def __init__(self, settings: Settings = SETTINGS,
                 on_spend: Optional[Callable[[float, str], None]] = None):
        self.settings = settings
        self.on_spend = on_spend            # governor hook: (usd, tier) -> None
        self.global_ledger = Ledger()
        self.balance_guard = None           # optional observability.governor.BalanceGuard
        self._provider_name = settings.resolved_provider()
        self._provider = self._build_provider(self._provider_name)
        # Keep a mock ready for fallback if the real provider dies mid-run.
        self._fallback = (
            MockProvider(MODEL_IDS["mock"])
            if self._provider_name != "mock" else None
        )

    @property
    def provider_name(self) -> str:
        return self._provider_name

    def _build_provider(self, name: str):
        if name == "deepseek":
            if not self.settings.deepseek_api_key:
                raise GatewayError("DEEPSEEK_API_KEY not set but provider=deepseek")
            return DeepSeekProvider(
                api_key=self.settings.deepseek_api_key,
                base_url=self.settings.deepseek_base_url,
                model_ids=MODEL_IDS["deepseek"],
                timeout=self.settings.request_timeout,
            )
        return MockProvider(MODEL_IDS["mock"])

    def chat(self, *, messages: List[Dict[str, Any]], tier: str = "flash",
             tools: Optional[List[Dict[str, Any]]] = None,
             temperature: float = 0.2, max_tokens: int = 2048,
             ledger: Optional[Ledger] = None) -> GatewayResponse:
        """One completion. Retries transient failures, falls back to mock."""
        if self.balance_guard is not None:
            self.balance_guard.check()      # raises KillSwitch at the real-balance floor
        last_err: Optional[Exception] = None
        for attempt in range(self.settings.max_retries):
            try:
                resp = self._provider.complete(
                    messages=messages, tier=tier, tools=tools,
                    temperature=temperature, max_tokens=max_tokens,
                )
                if not getattr(resp, "cost_from_provider", False):
                    resp.cost_usd = price_call(tier, resp.usage)
                self._book(resp, ledger)
                return resp
            except Exception as e:  # noqa: BLE001 - provider-agnostic retry
                last_err = e
                time.sleep(min(2 ** attempt, 8))
        # Retries exhausted: fall back to mock so the trajectory can still close
        # cleanly rather than crashing the whole workflow (durability principle).
        if self._fallback is not None:
            resp = self._fallback.complete(
                messages=messages, tier=tier, tools=tools,
                temperature=temperature, max_tokens=max_tokens,
            )
            resp.cost_usd = price_call(tier, resp.usage)
            resp.provider = "mock(fallback)"
            self._book(resp, ledger)
            return resp
        raise GatewayError(f"gateway failed after retries: {last_err}")

    def _book(self, resp: GatewayResponse, ledger: Optional[Ledger]) -> None:
        self.global_ledger.add(resp)
        if ledger is not None:
            ledger.add(resp)
        if self.on_spend is not None:
            self.on_spend(resp.cost_usd, resp.model_tier)
