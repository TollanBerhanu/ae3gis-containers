#!/bin/sh

# Start SSH (daemon mode)
/usr/sbin/sshd


# Squid cache dir init (first-run safe)
if [ ! -f /var/spool/squid/00 ]; then
  squid -Nz
fi

# Start Squid in foreground (so container lifecycle follows Squid)
exec squid -NYCd 1