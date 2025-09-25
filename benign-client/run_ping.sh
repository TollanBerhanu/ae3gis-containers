#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <target_ip> [interval_seconds]"
  exit 1
fi

TARGET_IP="$1"
INTERVAL="${2:-2}"

echo "[ping] Target=$TARGET_IP Interval=${INTERVAL}s"

while true; do
  ping -c 1 -W 1 "$TARGET_IP" || true
  sleep "$INTERVAL"
done


