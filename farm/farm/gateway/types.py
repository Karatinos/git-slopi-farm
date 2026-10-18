"""Shared types for the model gateway (OpenAI-compatible shapes)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class Usage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_hit_tokens: int = 0        # subset of prompt_tokens billed at hit rate
    cache_miss_tokens: int = 0       # subset of prompt_tokens billed at miss rate

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass
class GatewayResponse:
    text: str                                    # assistant free text (may be "")
    tool_calls: List[ToolCall] = field(default_factory=list)
    model_tier: str = "flash"                    # 'flash' | 'pro'
    provider: str = "mock"
    usage: Usage = field(default_factory=Usage)
    cost_usd: float = 0.0
    finish_reason: str = "stop"
    raw: Optional[Any] = None

    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)
