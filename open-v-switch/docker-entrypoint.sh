#!/usr/bin/env bash
set -euo pipefail

DB_DIR=${DB_DIR:-/var/lib/openvswitch}
RUNDIR=${RUNDIR:-/var/run/openvswitch}

mkdir -p "$DB_DIR" "$RUNDIR" /etc/openvswitch

# create DB if missing
if [ ! -f /etc/openvswitch/conf.db ]; then
  ovsdb-tool create /etc/openvswitch/conf.db /usr/share/openvswitch/vswitch.ovsschema
fi

# start ovsdb-server
ovsdb-server --remote=punix:/var/run/openvswitch/db.sock \
             --remote=ptcp:6640 \
             --pidfile --detach \
             --log-file

# init default config if empty
ovs-vsctl --no-wait init

# start datapath daemon
ovs-vswitchd --pidfile --detach --log-file

echo "Open vSwitch is up. UNIX DB socket: /var/run/openvswitch/db.sock (ptcp:6640 enabled)"
# Keep the container alive (helpful for logs)
tail -f /var/log/openvswitch/ovs-vswitchd.log /var/log/openvswitch/ovsdb-server.log

