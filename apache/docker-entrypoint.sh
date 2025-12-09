#!/usr/bin/env bash
set -euo pipefail

# Stop children gracefully on container stop
trap 'kill 0 || true' TERM INT

# Start syslog + sshd
rsyslogd
/usr/sbin/sshd

# Start Apache in the background (keep logs visible)
# -D FOREGROUND prevents apache from daemonizing; the trailing '&' backgrounds it here.
apache2ctl start

# Optional: show IPs on login
ip -4 addr show || true

# If a command was provided, run it; otherwise drop into shell for console use
if [[ $# -gt 0 ]]; then
  exec "$@"
else
  exec /bin/bash -l
fi