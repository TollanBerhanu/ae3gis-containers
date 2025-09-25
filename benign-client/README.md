# Benign Client Container

## Overview
This container provides a standard Ubuntu client with basic networking tools for testing and simulation purposes. It's designed to represent a normal, non-malicious client in network security testing scenarios.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- Basic networking utilities
- DNS tools
- Network scanning tools (nmap, netcat)
- Logging enabled (rsyslog)
 - Traffic scripts for ping, nmap, HTTP, and FTP (2s interval by default)

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **DNS**: dnsutils
- **Security Tools**: nmap, netcat-openbsd

## Usage in GNS3

### Starting the Container
1. Import the container into GNS3
2. Connect to network interfaces as needed
3. Start the container

### Accessing the Container
```bash
# SSH access
ssh root@<container_ip>
# Password: pass

# Or use GNS3 console
```

### Manual Service Startup (if needed)
```bash
# Start logging service
rsyslogd

# Start SSH service
/usr/sbin/sshd -D
```

### Testing Network Connectivity
```bash
# Test basic connectivity
ping <target_ip>

# DNS resolution
nslookup <domain>
dig <domain>

# Network scanning
nmap -sn <network_range>
nmap -p 22,80,443 <target_ip>

# Port connectivity
nc -zv <target_ip> <port>
```

### Traffic Generation Scripts
All scripts accept target parameters and run continuously with a default 2-second interval. You can override the interval by passing a second argument where applicable.

```bash
# Ping continuously
./run_ping.sh <target_ip> [interval_seconds]

# Nmap lightweight scans repeatedly
./run_nmap.sh <target_ip_or_cidr> [interval_seconds]

# HTTP GET to root path repeatedly
./run_http.sh <server_ip> [interval_seconds]

# FTP list and upload test file repeatedly
./run_ftp.sh <server_ip> <username> [password] [interval_seconds]
```

### Logging
- System logs: `/var/log/syslog`
- Auth logs: `/var/log/auth.log`
- Custom logs: `/var/log/`

## Configuration
- SSH is configured to allow root login with password authentication
- All basic networking tools are pre-installed and ready to use
- Logging is enabled for troubleshooting and monitoring

## Troubleshooting
- If SSH doesn't work, check if the service is running: `ps aux | grep sshd`
- For network issues, verify interface configuration: `ip addr show`
- Check logs for errors: `tail -f /var/log/syslog`
