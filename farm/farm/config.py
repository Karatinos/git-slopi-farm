"""Central configuration for slopi-farm.

All tunable knobs live here so the rest of the code reads them from one place.
Values that carry money/rate-limit risk (budgets, escalation share, concurrency)
are surfaced explicitly because the blueprint makes the *cost governor* a
first-class, mandatory component from phase 0.

Env overrides (see .env.example):
    DEEPSEEK_API_KEY      - real DeepSeek key; if absent the gateway falls back
                            to the deterministic Mock provider so the whole
                            pipeline still runs end-to-end for free.
    DEEPSEEK_BASE_URL     - OpenAI-compatible endpoint (default DeepSeek).
    SLOPI_PROVIDER        - force 'deepseek' | 'mock' | 'auto' (default auto).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Optional

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:  # dotenv is optional
    pass


# --------------------------------------------------------------------------- #
# Paths                                                                        #
# --------------------------------------------------------------------------- #
# farm/farm/config.py -> farm/ is two parents up from this file's dir.
PKG_DIR = Path(__file__).resolve().parent          # .../farm/farm
FARM_ROOT = PKG_DIR.parent                          # .../farm
PROJECT_ROOT = FARM_ROOT.parent                     # .../slopi-popi
DATA_DIR = FARM_ROOT / "data"
RUN_DIR = FARM_ROOT / ".work"                       # ephemeral run artifacts (gitignored)
TRACE_DIR = DATA_DIR / "traces"
DB_PATH = DATA_DIR / "farm.db"
TASKS_DIR = PROJECT_ROOT / "tasks"
# Ground-truth writeups mirror (quarantined: gold flags + solution-bank seed,
# NEVER shown to an agent). Optional — ingest tolerates its absence.
WRITEUPS_DIR = PROJECT_ROOT / "tasks-with-writeups"
PROGRESS_DIR = PROJECT_ROOT / "progress"

for _d in (DATA_DIR, RUN_DIR, TRACE_DIR, PROGRESS_DIR):
    _d.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
# Model pricing (per 1M tokens, USD).  From CTF-ферма-DeepSeek-V4-API.pdf p.4  #
# Pro price is a documented range; we keep a conservative point and flag it.   #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class ModelPricing:
    input_miss: float   # cache-miss input, $/1M
    input_hit: float    # cache-hit input, $/1M
    output: float       # output, $/1M


PRICING: Dict[str, ModelPricing] = {
    # DeepSeek V4-Flash (~284B) — the swarm workhorse.
    # OpenRouter deepseek/deepseek-v4.1-flash (verified /models 2026-10-18).
    "flash": ModelPricing(input_miss=0.04, input_hit=0.004, output=0.144),
    # Same Flash model with reasoning on (reasoning tokens bill as output).
    "think": ModelPricing(input_miss=0.04, input_hit=0.004, output=0.144),
    # OpenRouter deepseek/deepseek-v4-pro — rare escalation.
    "pro": ModelPricing(input_miss=0.209, input_hit=0.02, output=0.418),
}

# Logical tier -> concrete API model id. Overridable via env so the exact
# DeepSeek-V4 model names can be set at runtime without code changes.
# NB (verified against /models + the `model` field of responses, 2026-09-23):
# the API serves only `deepseek-flash` and `deepseek-v4-pro`. The legacy aliases
# both resolve to Flash — `deepseek-chat` = Flash without thinking and
# `deepseek-reasoner` = Flash WITH thinking — so the old "pro" default silently
# never reached V4-Pro. Pro must be addressed by its explicit id.
MODEL_IDS = {
    "deepseek": {
        "flash": os.environ.get("DEEPSEEK_FLASH_MODEL", "deepseek/deepseek-v4.1-flash"),
        # Flash with reasoning: same OpenRouter slug; reasoning controlled via
        # the `reasoning` request param, not a different model id.
        "think": os.environ.get("DEEPSEEK_THINK_MODEL", "deepseek/deepseek-v4.1-flash"),
        "pro": os.environ.get("DEEPSEEK_PRO_MODEL", "deepseek/deepseek-v4-pro"),
    },
    # Mock provider ignores ids but keeps the mapping shape.
    "mock": {"flash": "mock-flash", "think": "mock-think", "pro": "mock-pro"},
    # ScriptedSolver (no-LLM tooling baseline) — ids unused.
    "scripted": {"flash": "scripted", "think": "scripted", "pro": "scripted"},
}


# --------------------------------------------------------------------------- #
# Budgets — the "governor".  Triple budget per trajectory + global ceiling.    #
# --------------------------------------------------------------------------- #
@dataclass
class Budgets:
    # Per-trajectory triple budget (blueprint §7 "тройной бюджет").
    max_steps: int = 24              # ReAct steps before stop/escalate
    max_tokens: int = 220_000        # in+out tokens per trajectory
    max_seconds: float = 240.0       # wall-clock per trajectory
    max_usd: float = 0.0             # per-trajectory USD hard stop (0 = off)
    # Per-CALL output cap. Must be generous: V4.1-Flash reasons by default and
    # reasoning tokens eat this budget — too small (e.g. 1024) returns EMPTY
    # content with no tool call. 6144 covers low-effort reasoning + a tool call.
    max_tokens_per_call: int = 6144
    # Stall detection: no new fact / repeated action for this many steps -> stop.
    stall_steps: int = 5
    # Global daily ceiling for the whole farm (hard kill-switch), USD.
    global_usd_cap: float = 5.0
    # Per-task ceiling, USD (admission control uses this).
    per_task_usd_cap: float = 1.20


# --------------------------------------------------------------------------- #
# Cascade / escalation policy (blueprint §4).                                  #
# --------------------------------------------------------------------------- #
@dataclass
class CascadePolicy:
    enabled: bool = True                   # master switch for Flash->Pro cascade
    default_model: str = "flash"
    escalation_model: str = "pro"
    target_escalation_rate: float = 0.15   # ~15% of tasks touch Pro
    # Categories that start hot on Pro for part of the ensemble.
    hard_categories: tuple = ("pwn",)


# --------------------------------------------------------------------------- #
# Swarm / ensemble (blueprint §7 "разнообразие важнее количества").           #
# --------------------------------------------------------------------------- #
@dataclass
class SwarmConfig:
    ensemble_size: int = 4                 # diverse attempts per task
    max_concurrent_sandboxes: int = 4      # cap concurrency / backpressure
    max_concurrent_tasks: int = 3
    # Temperature diversity across ensemble members.
    temperatures: tuple = (0.0, 0.4, 0.7, 1.0)
    # Adaptive effort (run 3): allocate the step budget by recon signal instead
    # of spending it uniformly — conclude fast on tasks with no exploitable lead.
    adaptive_effort: bool = False
    low_signal_steps: int = 5       # step cap when recon found no real signal


# --------------------------------------------------------------------------- #
# Sandbox                                                                      #
# --------------------------------------------------------------------------- #
@dataclass
class SandboxConfig:
    backend: str = "auto"                  # 'docker' | 'local' | 'auto'
    image: str = "slopi-farm-sandbox:latest"
    cpu_limit: str = "2"                   # docker --cpus
    mem_limit: str = "2g"                  # docker --memory
    pids_limit: int = 256
    tool_timeout: float = 60.0             # per-tool wall clock
    network: str = "none"                  # egress deny by default (allowlist per task)


@dataclass
class Settings:
    provider: str = os.environ.get("SLOPI_PROVIDER", "auto")  # auto|deepseek|mock
    deepseek_api_key: Optional[str] = os.environ.get("DEEPSEEK_API_KEY")
    deepseek_base_url: str = os.environ.get(
        "DEEPSEEK_BASE_URL", "https://openrouter.ai/api/v1"
    )
    # Reasoning effort for the OpenRouter `reasoning` param (off|low|medium|high).
    reasoning_effort: str = os.environ.get("DEEPSEEK_REASONING_EFFORT", "low")
    request_timeout: float = 120.0
    max_retries: int = 3
    # ACI feature toggles (improvements enabled from run 2 onward).
    enable_recon: bool = False      # auto file/exif/OCR/QR digest before solving
    budgets: Budgets = field(default_factory=Budgets)
    cascade: CascadePolicy = field(default_factory=CascadePolicy)
    swarm: SwarmConfig = field(default_factory=SwarmConfig)
    sandbox: SandboxConfig = field(default_factory=SandboxConfig)
    # Flag regexes tried by the verifier (first match wins). CTF-specific.
    flag_patterns: tuple = (
        r"[A-Za-z0-9_]{2,32}\{[^}\n]{1,200}\}",   # generic name{...}
        r"flag\{[^}\n]{1,200}\}",
    )

    def resolved_provider(self) -> str:
        if self.provider != "auto":
            return self.provider
        return "deepseek" if self.deepseek_api_key else "mock"

    def as_dict(self) -> dict:
        d = asdict(self)
        if d.get("deepseek_api_key"):
            d["deepseek_api_key"] = "***set***"
        return d


SETTINGS = Settings()
