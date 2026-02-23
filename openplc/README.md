# OpenPLC Container

## Overview

This container provides [OpenPLC](https://openplcproject.com/), an open-source Programmable Logic Controller (PLC) that runs on Linux. It is useful for SCADA/ICS security research, education, and testing within GNS3 network topologies.

> **Status:** Experimental — the image builds OpenPLC from its upstream installer and exposes its web interface and Modbus port.

## Features

- Ubuntu 24.04 LTS base image
- OpenPLC v3 runtime (installed from source)
- SSH access (`root:pass`)
- Modbus TCP server on port 502
- Web-based PLC editor on port 8080
- Common networking tools pre-installed

## Installed Packages

- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, git, netcat-openbsd, telnet
- **PLC Runtime**: OpenPLC v3 (cloned and installed at `/opt/OpenPLC_v3`)

## Usage in GNS3

### Building the Image

```bash
docker build -t ae3gis-openplc ./openplc/
```

> **Note:** The build clones the OpenPLC repository and runs its installer, so it takes considerably longer than most other images in this repo.

### Starting the Container

1. Import the image into GNS3 (see the [central README](../README.md) for the step-by-step guide).
2. Connect to at least one network interface.
3. Start the container.

### Accessing the Container

```bash
# SSH access
ssh root@<container_ip>
# Password: pass

# Or use the GNS3 console
```

### Web Interface

Once the container is running, open a browser and navigate to:

```
http://<container_ip>:8080
```

The default OpenPLC credentials are set during the first-run setup inside the web UI.

### Modbus TCP

OpenPLC exposes a Modbus TCP server on **port 502**. You can interact with it from any Modbus client (e.g. `mbpoll`, ScadaBR, or a custom Python script using `pymodbus`).

```bash
# Quick test from another container (if mbpoll is available)
mbpoll -a 1 -t 0 -r 1 -c 5 <container_ip>
```

## Ports

| Port | Protocol | Service |
|------|----------|---------|
| 22   | TCP      | SSH     |
| 502  | TCP      | Modbus TCP |
| 8080 | TCP      | OpenPLC web interface |

## Logging

- System logs: `/var/log/syslog`
- OpenPLC logs: visible in the web interface and in the terminal output
- Auth logs: `/var/log/auth.log`

## Troubleshooting

- **Build fails:** Ensure you have a working internet connection — the Dockerfile clones an external Git repository and runs an installer that downloads dependencies.
- **Web interface not reachable:** Verify the container is running and port 8080 is accessible: `ss -ltnp | grep 8080`.
- **Modbus not responding:** Check that the OpenPLC runtime has been started from the web interface (it does not auto-start a PLC program).
- **SSH doesn't work:** Confirm sshd is running: `ps aux | grep sshd`.
