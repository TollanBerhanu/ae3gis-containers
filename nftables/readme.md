# nftables Firewall Container

## Overview
This container provides a Linux-based firewall using nftables, the modern replacement for iptables. nftables offers improved performance, better syntax, and more features than traditional iptables.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- nftables firewall management
- IPv4 forwarding enabled
- Logging enabled (rsyslog)

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **Firewall**: nftables

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

# Load nftables rules
nft -f /etc/nftables.conf

# Start SSH service
/usr/sbin/sshd -D
```

### nftables Management

#### Check nftables Status
```bash
# Check nftables version
nft --version

# List current ruleset
nft list ruleset

# List specific table
nft list table inet filter

# List specific chain
nft list chain inet filter input
```

#### Basic Firewall Rules
```bash
# Create a table
nft create table inet filter

# Create chains
nft create chain inet filter input { type filter hook input priority 0 \; }
nft create chain inet filter forward { type filter hook forward priority 0 \; }
nft create chain inet filter output { type filter hook output priority 0 \; }

# Set default policies
nft add rule inet filter input policy drop
nft add rule inet filter forward policy drop
nft add rule inet filter output policy accept

# Allow loopback
nft add rule inet filter input iif lo accept
nft add rule inet filter output oif lo accept

# Allow established connections
nft add rule inet filter input ct state established,related accept

# Allow SSH
nft add rule inet filter input tcp dport 22 accept

# Allow ping
nft add rule inet filter input icmp type echo-request accept
```

#### Advanced Rules
```bash
# Allow specific network
nft add rule inet filter input ip saddr 192.168.1.0/24 accept

# Block specific IP
nft add rule inet filter input ip saddr 192.168.1.100 drop

# Allow port range
nft add rule inet filter input tcp dport 8000-9000 accept

# Log dropped packets
nft add rule inet filter input log prefix "DROPPED: " drop
```

#### NAT Rules
```bash
# Create NAT table
nft create table inet nat

# Create NAT chains
nft create chain inet nat prerouting { type nat hook prerouting priority 0 \; }
nft create chain inet nat postrouting { type nat hook postrouting priority 100 \; }

# SNAT (Source NAT)
nft add rule inet nat postrouting oifname eth0 masquerade

# DNAT (Destination NAT)
nft add rule inet nat prerouting tcp dport 80 dnat to 192.168.1.10:80
```

#### Save and Load Rules
```bash
# Save current ruleset
nft list ruleset > /etc/nftables.conf

# Load rules from file
nft -f /etc/nftables.conf

# Flush all rules
nft flush ruleset
```

### Configuration File
The nftables configuration is located at `/etc/nftables.conf`. Example configuration:

```bash
#!/usr/sbin/nft -f

# Flush existing rules
flush ruleset

# Create table
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        
        # Allow loopback
        iif lo accept
        
        # Allow established connections
        ct state established,related accept
        
        # Allow SSH
        tcp dport 22 accept
        
        # Allow ping
        icmp type echo-request accept
        
        # Log and drop everything else
        log prefix "DROPPED: " drop
    }
    
    chain forward {
        type filter hook forward priority 0; policy drop;
    }
    
    chain output {
        type filter hook output priority 0; policy accept;
    }
}
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
- nftables logs: `/var/log/kern.log`
- Auth logs: `/var/log/auth.log`

## nftables vs iptables
- **Better performance**: nftables is faster than iptables
- **Simpler syntax**: More readable and maintainable rules
- **Unified interface**: Single tool for all packet filtering
- **Better debugging**: More detailed error messages
- **Atomic updates**: Rules are applied atomically

## Troubleshooting
- Check nftables status: `nft list ruleset`
- Verify IP forwarding: `cat /proc/sys/net/ipv4/ip_forward`
- Check logs: `tail -f /var/log/syslog`
- Test connectivity: `ping` and `nmap`
- View connection tracking: `cat /proc/net/nf_conntrack`
- Validate configuration: `nft -c -f /etc/nftables.conf`