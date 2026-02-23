# Snort 3 IDS Container

## Overview
This container provides Snort 3, the next-generation Network Intrusion Detection System (NIDS). Snort 3 offers improved performance, better Lua scripting support, and enhanced detection capabilities compared to Snort 2.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- Snort 3 IDS (compiled from source)
- Logging enabled (rsyslog)
- Pre-configured for network monitoring

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **Build Tools**: build-essential, autotools-dev, libpcap-dev, cmake, git
- **IDS**: Snort 3 (compiled from source)

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

# Start Snort 3 manually
snort -c /usr/local/etc/snort/snort.lua -i eth0
```

### Snort 3 Management

#### Check Snort 3 Status
```bash
# Check if Snort 3 is running
ps aux | grep snort

# Check Snort 3 version
snort --version

# Test Snort 3 configuration
snort -T -c /usr/local/etc/snort/snort.lua
```

#### Snort 3 Configuration
Snort 3 uses Lua configuration files. The main configuration is located at `/usr/local/etc/snort/snort.lua`. Key configuration sections:

```lua
-- Network variables
HOME_NET = '192.168.1.0/24'
EXTERNAL_NET = 'any'

-- Output plugins
alert_fast = {
    file = true,
    packet = false,
    limit = 0
}

-- Include rule files
include('snort_defaults.lua')
include('local.rules')
```

#### Edit Configuration
```bash
# Edit Snort 3 configuration
vim /usr/local/etc/snort/snort.lua

# Test configuration
snort -T -c /usr/local/etc/snort/snort.lua

# Create custom rules
vim /usr/local/etc/snort/rules/local.rules
```

### Snort 3 Commands

#### Basic Snort 3 Operations
```bash
# Run Snort 3 in console mode
snort -c /usr/local/etc/snort/snort.lua -i eth0

# Run Snort 3 in daemon mode
snort -c /usr/local/etc/snort/snort.lua -i eth0 -D

# Run Snort 3 with specific interface
snort -c /usr/local/etc/snort/snort.lua -i eth1

# Run Snort 3 with custom rules
snort -c /usr/local/etc/snort/snort.lua -i eth0 -R /path/to/custom.rules
```

#### Snort 3 Modes
```bash
# Sniffer mode (packet capture)
snort -i eth0 -v

# Packet logger mode
snort -i eth0 -l /var/log/snort

# NIDS mode (default)
snort -c /usr/local/etc/snort/snort.lua -i eth0
```

### Custom Rules

#### Basic Rule Syntax (Snort 3)
```bash
# Alert on ping
alert icmp any any -> any any (msg:"ICMP Ping Detected"; itype:8; sid:1000001; rev:1;)

# Alert on port scan
alert tcp any any -> any any (msg:"Port Scan Detected"; flags:S,12; threshold:type limit, track by_src, count 1, seconds 60; sid:1000002; rev:1;)

# Alert on HTTP requests
alert tcp any any -> any 80 (msg:"HTTP Request"; content:"GET"; http_method; sid:1000003; rev:1;)
```

#### Create Custom Rules
```bash
# Edit local rules file
vim /usr/local/etc/snort/rules/local.rules

# Test rules
snort -T -c /usr/local/etc/snort/snort.lua

# Reload Snort 3 with new rules
pkill snort
snort -c /usr/local/etc/snort/snort.lua -i eth0 -D
```

### Monitoring and Analysis

#### View Snort 3 Logs
```bash
# View alerts
tail -f /var/log/snort/alert

# View packet logs
tail -f /var/log/snort/snort.log

# View system logs
tail -f /var/log/syslog | grep snort
```

#### Analyze Traffic
```bash
# Monitor network traffic
tcpdump -i any -w capture.pcap

# Analyze with Snort 3
snort -r capture.pcap -c /usr/local/etc/snort/snort.lua

# View packet details
tcpdump -r capture.pcap -v
```

### Testing Snort 3 Detection

#### Generate Test Traffic
```bash
# From another container, generate traffic to test Snort 3
ping <snort_ip>
nmap -sS <snort_ip>
curl http://<snort_ip>
```

#### Verify Detection
```bash
# Check if alerts were generated
cat /var/log/snort/alert

# Monitor real-time alerts
tail -f /var/log/snort/alert
```

### Logging
- System logs: `/var/log/syslog`
- Snort 3 alerts: `/var/log/snort/alert`
- Snort 3 logs: `/var/log/snort/snort.log`
- Auth logs: `/var/log/auth.log`

## Snort 3 vs Snort 2
- **Better Performance**: Improved packet processing
- **Lua Configuration**: More flexible configuration language
- **Enhanced Detection**: Better pattern matching and protocol analysis
- **Plugin System**: Improved plugin architecture
- **Memory Management**: Better memory usage and management

## Troubleshooting
- Check Snort 3 status: `ps aux | grep snort`
- Test configuration: `snort -T -c /usr/local/etc/snort/snort.lua`
- Check logs: `tail -f /var/log/snort/alert`
- Verify interface: `ip addr show`
- Monitor traffic: `tcpdump -i any`
- Check rule syntax: `snort -T -c /usr/local/etc/snort/snort.lua`
- Verify library path: `ldconfig -p | grep snort`
