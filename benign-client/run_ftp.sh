#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <server_ip> <username> [password] [interval_seconds]"
  exit 1
fi

SERVER_IP="$1"
USERNAME="$2"
PASSWORD="${3:-ftppass}"
INTERVAL="${4:-2}"

echo "[ftp] Server=$SERVER_IP User=$USERNAME Interval=${INTERVAL}s"

while true; do
  # List root dir and attempt upload of a small file
  TMPFILE="/tmp/ftp_test_$$.txt"
  date > "$TMPFILE"
  # Using curl for FTP to avoid interactive ftp client
  curl -sS --ftp-method nocwd -u "$USERNAME:$PASSWORD" "ftp://$SERVER_IP/" -l >/dev/null || true
  curl -sS -T "$TMPFILE" -u "$USERNAME:$PASSWORD" "ftp://$SERVER_IP/upload/ftp_test.txt" >/dev/null || true
  rm -f "$TMPFILE"
  sleep "$INTERVAL"
done


