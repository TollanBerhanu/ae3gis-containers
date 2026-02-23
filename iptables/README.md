# iptables Firewall Container

## Overview
This container provides a Linux-based firewall using iptables. iptables is the traditional Linux firewall tool that provides powerful packet filtering and NAT capabilities.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- iptables firewall management
- iptables-persistent for rule persistence
- IPv4 forwarding enabled
- Logging enabled (rsyslog)

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **Firewall**: iptables, iptables-persistent

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

# Start SSH service
/usr/sbin/sshd -D
```

### iptables Management

#### View Current Rules
```bash
# List all rules
iptables -L -n -v

# List with line numbers
iptables -L -n -v --line-numbers

# List specific table
iptables -t filter -L -n -v
iptables -t nat -L -n -v
iptables -t mangle -L -n -v
```

#### Basic Firewall Rules
```bash
# Set default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow ping
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
```

#### Advanced Rules
```bash
# Allow specific network
iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT

# Block specific IP
iptables -A INPUT -s 192.168.1.100 -j DROP

# Allow port range
iptables -A INPUT -p tcp --dport 8000:9000 -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "DROPPED: "
iptables -A INPUT -j DROP
```

#### NAT Rules
```bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# SNAT (Source NAT)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT (Destination NAT)
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:80
```

#### Save and Restore Rules
```bash
# Save current rules
iptables-save > /etc/iptables/rules.v4

# Restore rules
iptables-restore < /etc/iptables/rules.v4

# Use iptables-persistent
netfilter-persistent save
netfilter-persistent reload
```

### Testing Firewall Rules
```bash
# Test from another container
ping <firewall_ip>
nmap -p 22,80,443 <firewall_ip>

# Monitor traffic
tcpdump -i any host <target_ip>

# Check connection tracking
cat /proc/net/nf_conntrack
```

### Logging
- System logs: `/var/log/syslog`
- iptables logs: `/var/log/kern.log`
- Auth logs: `/var/log/auth.log`

## Common iptables Tables
- **filter**: Default table for packet filtering
- **nat**: Network Address Translation
- **mangle**: Packet modification
- **raw**: Connection tracking bypass

## Common iptables Chains
- **INPUT**: Incoming packets to local processes
- **FORWARD**: Packets routed through the system
- **OUTPUT**: Outgoing packets from local processes
- **PREROUTING**: Packets before routing decision
- **POSTROUTING**: Packets after routing decision

## Troubleshooting
- Check if iptables is running: `iptables -L`
- Verify IP forwarding: `cat /proc/sys/net/ipv4/ip_forward`
- Check logs: `tail -f /var/log/syslog`
- Test connectivity: `ping` and `nmap`
- View connection tracking: `cat /proc/net/nf_conntrack`
