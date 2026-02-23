# AE3GIS Containers

A collection of ready-to-use Docker images for building network security labs inside [GNS3](https://www.gns3.com/). Build an image, import it into GNS3, wire it up, and start learning.

## Overview

Every image in this repository is purpose-built for network security education, testing, and simulation. The containers span several categories — clients, firewalls, web servers, intrusion detection systems, SCADA/ICS components, and more — so you can assemble realistic lab topologies without leaving GNS3.

Most images share a **common baseline**:

| Item | Default |
|---|---|
| Base OS | Ubuntu 24.04 LTS (exceptions noted per container) |
| SSH credentials | `root` / `pass` |
| System logging | rsyslog → `/var/log/syslog` |
| Common tools | `net-tools`, `iproute2`, `iputils-ping`, `tcpdump`, `curl`, `wget`, `vim`, `nano`, `procps` |

> Individual containers install additional packages on top of this baseline. See each container's own README for the full list.

## Prerequisites

| Tool | Minimum Version | Notes |
|---|---|---|
| [Docker](https://docs.docker.com/get-docker/) | 20.10+ | Used to build the images |
| [GNS3](https://www.gns3.com/software/download) | 2.2+ | Network simulation environment |
| GNS3 VM **or** a local GNS3 server | — | Required for running Docker containers inside GNS3 |

Make sure the GNS3 server (or GNS3 VM) has Docker available. If you are running GNS3 on Windows or macOS, the GNS3 VM is the easiest way to get Docker support.

## Quick Start

### 1. Build a container image

```bash
# From the repository root
docker build -t ae3gis-benign-client ./benign-client/
docker build -t ae3gis-suricata     ./suricata/
docker build -t ae3gis-nftables     ./nftables/
```

You can name the images however you like; the `ae3gis-` prefix is just a convention used here.

### 2. (Optional) Test locally with Docker

```bash
# Run the benign client interactively
docker run --rm -it ae3gis-benign-client

# Run the Apache web server and map port 80
docker run --rm -it -p 8080:80 ae3gis-apache
```

### 3. Import into GNS3

> The steps below use the GNS3 GUI. You only need to do this once per image.

1. Open GNS3 and go to **Edit → Preferences** (Windows/Linux) or **GNS3 → Preferences** (macOS).
2. In the left sidebar, expand **Docker** and select **Docker containers**.
3. Click **New** to start the Docker container template wizard.
4. Choose **Existing image** and pick the image you just built (e.g. `ae3gis-benign-client`).
5. Give the template a friendly name (e.g. *Benign Client*).
6. Set the number of **network adapters** the appliance needs (1 is fine for most hosts; firewalls and IDS containers typically need 2+).
7. Optionally set a **start command** if the container requires one (most images already define a `CMD` in their Dockerfile).
8. Click **Finish**. The new appliance now appears in the GNS3 toolbar under **All devices → End devices** (or whichever category you chose).

Drag the appliance onto the canvas, connect it to a switch or other nodes, and **Start** it. Right-click → **Console** opens a shell, or you can SSH in from another node:

```bash
ssh root@<container_ip>
# Password: pass
```

### 4. Build a topology

Wire together any combination of the containers in this repo. For example:

```
Benign Client ──┐
                ├── Switch ── nftables Firewall ── Suricata IDS ── Apache Server
Malicious Client┘
```

Each container's README describes its specific services, ports, and configuration files.

## Repository Layout

Containers are grouped by role. Refer to the README inside each folder for full details.

| Category | Containers | Description |
|---|---|---|
| **Clients** | `benign-client`, `malicious-client` | Normal and offensive network endpoints |
| **Firewalls** | `firehol`, `iptables`, `nftables` | Packet filtering and NAT |
| **Web Servers** | `apache-server`, `nginx-server` | HTTP servers with default pages |
| **Network Services** | `ftp-server`, `isc-dhcp-server`, `smb` | FTP, DHCP, and a deliberately vulnerable Samba server |
| **Intrusion Detection** | `snort2`, `snort3`, `suricata`, `zeek` | Network IDS/IPS and security monitoring |
| **Endpoint Security** | `wazuh/wazuh-agent`, `wazuh/wazuh-manager` | Host-based intrusion detection and SIEM |
| **SCADA / ICS** | `openplc`, `scadabr` | Industrial control system components (experimental) |

## Standardized Configuration

Almost every container follows the same conventions so that your lab experience is consistent:

- **SSH** is enabled with `root:pass` and `PermitRootLogin yes`.
- **rsyslog** writes to `/var/log/syslog`.
- **Common networking tools** (`ping`, `ip`, `tcpdump`, `curl`, etc.) are pre-installed.
- **IPv4 forwarding** is enabled on containers that act as routers or firewalls.

> ⚠️ These defaults are intentionally insecure for lab convenience. **Never** reuse them outside of an isolated lab environment.

## Security Considerations

- Several containers ship with **intentionally vulnerable** software (e.g. the Samba container runs a version affected by EternalBlue).
- The `malicious-client` image includes penetration testing tools (`nmap`, `hydra`, `john`, etc.).
- **Use these images only in isolated, controlled environments** — never on production networks.
- Always comply with applicable laws and your organization's acceptable-use policies.

## Contributing

Contributions are welcome — bug fixes, new containers, documentation improvements, and more. Please open an issue or a pull request.

## License

This project is licensed under the [MIT License](./LICENSE).