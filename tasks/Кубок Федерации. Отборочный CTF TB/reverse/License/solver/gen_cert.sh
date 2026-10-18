#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"
HOST="${1:?Usage: sh gen_cert.sh <activation-domain>}"
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365 \
  -subj "/CN=$HOST"
