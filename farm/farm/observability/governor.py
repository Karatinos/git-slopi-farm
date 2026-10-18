"""Cost governor + kill-switch.

The blueprint is emphatic: a budget governor is mandatory from phase 0, because
a looping swarm can silently burn money. This is the single authority that
tracks global spend and trips a hard stop.

Usage:
    gov = CostGovernor(global_cap_usd=5.0)
    gateway = ModelGateway(on_spend=gov.record)
    ...
    gov.check()          # raises KillSwitch if over budget
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Dict


class KillSwitch(RuntimeError):
    """Raised when the farm exceeds its hard global budget."""


@dataclass
class CostGovernor:
    global_cap_usd: float
    spent_usd: float = 0.0
    spent_by_tier: Dict[str, float] = field(default_factory=dict)
    tripped: bool = False
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record(self, usd: float, tier: str) -> None:
        with self._lock:
            self.spent_usd += usd
            self.spent_by_tier[tier] = self.spent_by_tier.get(tier, 0.0) + usd
            if self.spent_usd >= self.global_cap_usd:
                self.tripped = True

    def remaining(self) -> float:
        return max(0.0, self.global_cap_usd - self.spent_usd)

    def check(self) -> None:
        """Call before starting new work; raises when the budget is spent."""
        if self.tripped:
            raise KillSwitch(
                f"global budget exhausted: spent ${self.spent_usd:.4f} "
                f">= cap ${self.global_cap_usd:.2f}"
            )

    def would_exceed(self, projected_usd: float) -> bool:
        return (self.spent_usd + projected_usd) > self.global_cap_usd

    def snapshot(self) -> dict:
        return {
            "cap_usd": self.global_cap_usd,
            "spent_usd": round(self.spent_usd, 6),
            "remaining_usd": round(self.remaining(), 6),
            "by_tier": {k: round(v, 6) for k, v in self.spent_by_tier.items()},
            "tripped": self.tripped,
        }


class BalanceGuard:
    """Hard stop on the provider's REAL account balance.

    The price table can drift from actual billing (a run estimated at ~$2.2 was
    billed ~$4), so an estimate-based cap is not enough. This guard reads the
    live balance from the provider every few calls and trips once it falls to
    the floor, regardless of what the local ledger believes.
    """

    def __init__(self, fetch_balance, floor_usd: float, every_calls: int = 4,
                 estimate_fn=None, estimate_ceiling: float = None):
        self._fetch = fetch_balance
        self.floor = floor_usd
        self.every = every_calls
        # real-time estimate stop (the balance API lags minutes; the local
        # estimate is instantaneous, just under-counting — corrected by caller)
        self._estimate = estimate_fn
        self.estimate_ceiling = estimate_ceiling
        self._calls = 0
        self.last_balance = None
        self.tripped = False
        self._lock = threading.Lock()

    def check(self, force: bool = False) -> None:
        with self._lock:
            if self.tripped:
                raise KillSwitch("budget guard already tripped")
            if self._estimate is not None and self.estimate_ceiling is not None:
                est = self._estimate()
                if est >= self.estimate_ceiling:
                    self.tripped = True
                    raise KillSwitch(f"estimated spend ${est:.3f} >= ceiling "
                                     f"${self.estimate_ceiling:.3f}")
            self._calls += 1
            if not force and self._calls % self.every:
                return
        try:
            bal = float(self._fetch())
        except Exception:  # noqa: BLE001 - a failed read must not stop work
            return
        with self._lock:
            self.last_balance = bal
            if bal <= self.floor:
                self.tripped = True
                raise KillSwitch(f"balance floor reached: {bal} <= {self.floor}")


def deepseek_balance_fetcher(api_key: str, base_url: str):
    import httpx
    root = base_url.rstrip("/").removesuffix("/v1")

    def fetch() -> float:
        r = httpx.get(root + "/user/balance",
                      headers={"Authorization": f"Bearer {api_key}"}, timeout=20)
        info = r.json()["balance_infos"]
        return sum(float(x["total_balance"]) for x in info if x.get("currency") == "USD")
    return fetch
