#!/usr/bin/env bash
# Source before running the farm against OpenRouter (run in a REAL terminal).
# Requires OPENROUTER_API_KEY in your environment (same var Codex uses).
: "${OPENROUTER_API_KEY:?set OPENROUTER_API_KEY first (export OPENROUTER_API_KEY=sk-or-...)}"
export DEEPSEEK_API_KEY="$OPENROUTER_API_KEY"          # gateway reads DEEPSEEK_API_KEY
export DEEPSEEK_BASE_URL="https://openrouter.ai/api/v1"
export DEEPSEEK_FLASH_MODEL="deepseek/deepseek-v4.1-flash"   # $0.04/$0.144 per 1M
export DEEPSEEK_THINK_MODEL="deepseek/deepseek-v4.1-flash"
export DEEPSEEK_PRO_MODEL="deepseek/deepseek-v4-pro"        # $0.209/$0.418 per 1M
export DEEPSEEK_REASONING_EFFORT="low"                 # off|low|medium|high
export SLOPI_PROVIDER="deepseek"                       # real provider via OpenRouter
echo "[env] OpenRouter wired: flash=$DEEPSEEK_FLASH_MODEL pro=$DEEPSEEK_PRO_MODEL effort=$DEEPSEEK_REASONING_EFFORT"
