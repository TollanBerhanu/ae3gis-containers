#!/bin/bash
set -e

echo "[+] Starting rsyslogd..."
rsyslogd &

# optional: wait a sec to ensure it bound the ports
sleep 1
echo "[+] rsyslog started (PID: $(pidof rsyslogd))"

# drop into an interactive shell
exec /bin/bash