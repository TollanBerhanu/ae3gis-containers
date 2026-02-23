# FireHOL Firewall Container

## Overview
This container provides a FireHOL-based firewall solution. FireHOL is a language to express firewalling policies that is easy to read and understand, making it ideal for complex firewall configurations.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- FireHOL firewall management
- IPv4 forwarding enabled
- Logging enabled (rsyslog)

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **Firewall**: firehol

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
# Apply sysctl settings
sysctl -p

# Start logging service
rsyslogd

# Start FireHOL
firehol start

# Start SSH service
/usr/sbin/sshd -D
```

### FireHOL Management

#### Check FireHOL Status
```bash
# Check if FireHOL is running
firehol status

# Check FireHOL version
firehol version

# Test configuration without applying
firehol try
```

#### FireHOL Configuration
```bash
# Edit FireHOL configuration
vim /etc/firehol.conf

# Reload configuration
firehol restart

# Stop FireHOL
firehol stop

# Start FireHOL
firehol start
```

#### Viewing Firewall Rules
```bash
# View iptables rules
iptables -L -n -v

# View with line numbers
iptables -L -n -v --line-numbers

# View specific chain
iptables -L INPUT -n -v
iptables -L FORWARD -n -v
iptables -L OUTPUT -n -v
```

#### Testing Firewall Rules
```bash
# Test from another container
ping <firewall_ip>
nmap -p 22 <firewall_ip>

# Check if traffic is being blocked
tcpdump -i any host <target_ip>
```

### Configuration File
The FireHOL configuration is located at `/etc/firehol.conf`. The default configuration shipped with this container:

```bash
version 6

# Accept any traffic to/from the container (for testing)
interface any world
    policy drop

    # Accept SSH
    server ssh accept
    client all accept

    # Accept PING (ICMP echo-request)
    server ping accept
    client ping accept

    # Log and drop everything else
    protection strong
    server all log "FIREHOL_DROP " drop
```

### Logging
- System logs: `/var/log/syslog`
- FireHOL logs: `/var/log/firehol.log`
- Auth logs: `/var/log/auth.log`

## FireHOL Language Basics
FireHOL uses a simple language to define firewall rules:

```bash
# Allow all traffic from trusted network
client all accept src 192.168.1.0/24

# Block specific IP
client all deny src 192.168.1.100

# Allow specific service
server http accept

# Allow port range
server "1000:2000" accept
```

## Troubleshooting
- Check FireHOL status: `firehol status`
- Test configuration: `firehol try`
- View iptables rules: `iptables -L -n -v`
- Check logs: `tail -f /var/log/syslog`
- Verify IP forwarding: `cat /proc/sys/net/ipv4/ip_forward`