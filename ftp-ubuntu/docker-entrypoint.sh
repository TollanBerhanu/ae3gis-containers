#!/bin/sh

# Start SSH (daemon mode)
/usr/sbin/sshd

# Start Pure-FTPd in foreground
exec /usr/sbin/pure-ftpd \
  -l unix \
  -E \
  -j \
  -c 50 \
  -C 5 \
  -p ${PASV_MIN:-21000}:${PASV_MAX:-21010} \
  -P ${PASV_ADDRESS:-0.0.0.0} &

if [ "$#" -gt 0 ]; then
  exec "$@"
else
  exec /bin/bash -l
fi