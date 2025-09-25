#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <target_ip_or_cidr> [interval_seconds]"
  exit 1
fi

TARGET="$1"
INTERVAL="${2:-2}"

echo "[nmap] Target=$TARGET Interval=${INTERVAL}s"

while true; do
  nmap -Pn -sT --top-ports 10 "$TARGET" || true
  sleep "$INTERVAL"
done


