#!/usr/bin/env bash
set -euo pipefail

BRIDGE_NAME=${BRIDGE_NAME:-br0}
EXCLUDE_PORTS=${EXCLUDE_PORTS:-}
OF_PROTOCOLS=${OF_PROTOCOLS:-OpenFlow10,OpenFlow13}
CONTROLLER=${CONTROLLER:-}
DATAPATH_TYPE=${DATAPATH_TYPE:-auto}
OVSDB_REMOTE=${OVSDB_REMOTE:-ptcp:6640}

# Package default locations; ovs-vsctl/ovs-appctl look here without extra flags
DB=/etc/openvswitch/conf.db
SCHEMA=/usr/share/openvswitch/vswitch.ovsschema
RUNDIR=/var/run/openvswitch
LOGDIR=/var/log/openvswitch

mkdir -p "$RUNDIR" "$LOGDIR" /etc/openvswitch

# The userspace datapath creates the bridge's own port as a tap device, through
# /dev/net/tun. Docker allows that device (char 10:200) but only adds it when
# asked (--device); without it OVS fails with "failed to create bridge". Make it.
if [ ! -c /dev/net/tun ]; then
  mkdir -p /dev/net
  mknod /dev/net/tun c 10 200 || echo "WARN: cannot create /dev/net/tun; the netdev datapath will fail" >&2
fi

# Create DB if missing; upgrade one written by an older OVS version
if [ ! -f "$DB" ]; then
  ovsdb-tool create "$DB" "$SCHEMA"
elif [ "$(ovsdb-tool needs-conversion "$DB" "$SCHEMA")" = yes ]; then
  ovsdb-tool convert "$DB" "$SCHEMA"
fi

# Start ovsdb-server (UNIX sock, managers stored in the DB, optional remote mgmt port)
remotes=(--remote="punix:$RUNDIR/db.sock" --remote=db:Open_vSwitch,Open_vSwitch,manager_options)
if [ -n "$OVSDB_REMOTE" ]; then
  remotes+=(--remote="$OVSDB_REMOTE")
fi
ovsdb-server "$DB" "${remotes[@]}" \
             --pidfile --detach --log-file="$LOGDIR/ovsdb-server.log"

ovs-vsctl --no-wait init

# The kernel datapath only works if the host already loaded the openvswitch module
# (a container can't load it); otherwise use the userspace datapath
if [ "$DATAPATH_TYPE" = auto ]; then
  if [ -d /sys/module/openvswitch ]; then DATAPATH_TYPE=system; else DATAPATH_TYPE=netdev; fi
fi

# Userspace datapath: read the kernel's offload metadata (vnet header) on attached ports.
# Without it, TCP from neighbours that use checksum offload (the veth default) arrives with
# bad checksums and is dropped, while ping still works. Only read at ovs-vswitchd startup.
if [ "$DATAPATH_TYPE" = netdev ]; then
  ovs-vsctl --no-wait set Open_vSwitch . other_config:userspace-tso-enable=true
fi

# Start switch daemon
ovs-vswitchd --pidfile --detach --log-file="$LOGDIR/ovs-vswitchd.log"

# Create bridge if not exists (the DB survives container restarts), set datapath and protocols
ovs-vsctl --may-exist add-br "$BRIDGE_NAME" \
  -- set bridge "$BRIDGE_NAME" datapath_type="$DATAPATH_TYPE" protocols="$OF_PROTOCOLS"

# Optional controller
if [ -n "$CONTROLLER" ]; then
  ovs-vsctl set-controller "$BRIDGE_NAME" "$CONTROLLER"
fi

# Bring bridge up
ip link set dev "$BRIDGE_NAME" up || true

# Attach every ethN interface (in GNS3 these are the adapters, eth0 included) unless excluded.
# Each interface is handled once per run, so a port downed by hand isn't forced back up.
declare -A seen=()
attach_ports () {
  local path nic
  for path in /sys/class/net/eth*; do
    nic=${path##*/}
    [ -e "$path" ] && [ -z "${seen[$nic]:-}" ] || continue
    seen[$nic]=1
    case " $EXCLUDE_PORTS " in *" $nic "*) continue ;; esac
    if ip link set dev "$nic" up && ovs-vsctl --may-exist add-port "$BRIDGE_NAME" "$nic"; then
      echo "Attached $nic to $BRIDGE_NAME"
    else
      echo "WARN: could not attach $nic to $BRIDGE_NAME" >&2
    fi
  done
}
attach_ports

echo "OVS ready: bridge=$BRIDGE_NAME datapath=$DATAPATH_TYPE ports=$(ovs-vsctl list-ports "$BRIDGE_NAME" | tr '\n' ' ')"
if [ -n "$OVSDB_REMOTE" ]; then
  echo "Mgmt (ovsdb) listening on $OVSDB_REMOTE"
fi

shutdown () {
  echo "Stopping Open vSwitch"
  ovs-appctl -t ovs-vswitchd exit || true
  ovs-appctl -t ovsdb-server exit || true
  exit 0
}
trap shutdown TERM INT

tail -F "$LOGDIR/ovsdb-server.log" "$LOGDIR/ovs-vswitchd.log" &

# Pick up interfaces that appear later; exit if a daemon dies so the failure is visible
while ovs-appctl -t ovsdb-server version >/dev/null 2>&1 &&
      ovs-appctl -t ovs-vswitchd version >/dev/null 2>&1; do
  sleep 5 & wait $!
  attach_ports
done
echo "ERROR: an Open vSwitch daemon exited, see $LOGDIR" >&2
exit 1
