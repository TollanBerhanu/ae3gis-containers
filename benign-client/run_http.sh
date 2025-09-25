#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <server_ip> [interval_seconds]"
  exit 1
fi

SERVER_IP="$1"
INTERVAL="${2:-2}"

echo "[http] Server=$SERVER_IP Interval=${INTERVAL}s"

while true; do
  curl -fsS -o /dev/null -w "%{http_code} %{time_total}\n" "http://$SERVER_IP/" || true
  sleep "$INTERVAL"
done


