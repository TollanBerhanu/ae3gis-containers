# MariaDB (Historian / Pivot) Container

## Overview
Ubuntu 24.04 running **MariaDB**, with the OT client libraries pre-installed. In the ICS lab this node plays the **historian** and the dual-homed **pivot** between the IT and OT segments, but the image is named for what it actually is (a MariaDB server). Its lab role is carried in the AE3GIS metadata (`io.ae3gis.type=database-server`).

## Features
- Ubuntu 24.04 LTS base image
- MariaDB server (port 3306)
- OT client libraries in a venv at `/opt/venv`: `pymodbus` (Modbus, Scenario A) and `c104` (IEC-104, Scenario B)
- Recon tools for the OT side: `nmap`, `netcat-openbsd`
- SSH access (`root:pass`)
- IP forwarding is **not** enabled — this is a pivot, not a router

## Installed Packages
- **Database**: mariadb-server
- **OT clients (venv)**: pymodbus, c104
- **Recon**: nmap, netcat-openbsd
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Python**: python3, python3-venv

## Usage

```bash
# OT client libraries
/opt/venv/bin/python -c "import pymodbus, c104; print('OT clients OK')"

# MariaDB (local root socket auth by default)
mysql -e "SELECT VERSION();"
```

The OT client libs let this node poll the field devices (OpenPLC over Modbus, or the IEC-104 RTU) as part of the scenarios. Forwarding is deliberately left off; enable it at the topology layer only if a scenario needs this node to route.

> Credentials and SSH settings are intentionally weak for an isolated lab. Never reuse outside one.
