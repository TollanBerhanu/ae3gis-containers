#!/usr/bin/env bash
set -euo pipefail

# Start rsyslog and SSH
rsyslogd
/usr/sbin/sshd

# Start postfix in the background
postfix start

# Optional: show IPs when you open console
ip -4 addr show || true

# If a command is passed, run it; otherwise drop into a login shell
if [[ $# -gt 0 ]]; then
  exec "$@"
else
  exec /bin/bash -l
fi