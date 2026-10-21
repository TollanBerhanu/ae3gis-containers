#!/bin/bash
set -e

# Start syslog-ng in the background so logging works even before shell access
syslog-ng -F &

# If we're not attached to a TTY (e.g., running as a background container), don't block startup
if [ ! -t 0 ]; then
  exec "$@"
fi

TRIES=0
MAX_TRIES=3

while true; do
  echo -n "Login: "
  read -r U

  echo -n "Password: "
  stty -echo
  read -r P
  stty echo
  echo

  if [ "$U" = "$CONTAINER_USER" ] && [ "$P" = "$CONTAINER_PASS" ]; then
    echo "Access granted."
    break
  fi

  TRIES=$((TRIES+1))
  echo "Access denied."
  if [ "$TRIES" -ge "$MAX_TRIES" ]; then
    echo "Too many failed attempts. Exiting."
    exit 1
  fi
done

exec "$@"
