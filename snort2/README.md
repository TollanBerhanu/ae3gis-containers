# Snort 2 IDS Container

## Overview
This container provides Snort 2, a popular open-source Network Intrusion Detection System (NIDS). Snort 2 can perform real-time traffic analysis and packet logging on IP networks.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- Snort 2 IDS with default rules
- Logging enabled (rsyslog)
- Pre-configured for network monitoring

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **IDS**: snort, snort-rules-default

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

# Start Snort manually
snort -i eth0 -A console -c /etc/snort/snort.conf
```

### Snort Management

#### Check Snort Status
```bash
# Check if Snort is running
ps aux | grep snort

# Check Snort version
snort -V

# Test Snort configuration
snort -T -c /etc/snort/snort.conf
```

#### Snort Configuration
The main Snort configuration is located at `/etc/snort/snort.conf`. Key configuration sections:

```bash
# Network variables
var HOME_NET 192.168.1.0/24
var EXTERNAL_NET any

# Output plugins
output alert_fast: /var/log/snort/alert
output log_tcpdump: /var/log/snort/snort.log

# Include rule files
include $RULE_PATH/local.rules
include $RULE_PATH/snort.rules
```

#### Edit Configuration
```bash
# Edit Snort configuration
vim /etc/snort/snort.conf

# Test configuration
snort -T -c /etc/snort/snort.conf

# Create custom rules
vim /etc/snort/rules/local.rules
```

### Snort Commands

#### Basic Snort Operations
```bash
# Run Snort in console mode
snort -i eth0 -A console -c /etc/snort/snort.conf

# Run Snort in daemon mode
snort -i eth0 -D -c /etc/snort/snort.conf

# Run Snort with specific interface
snort -i eth1 -A console -c /etc/snort/snort.conf

# Run Snort with custom rules
snort -i eth0 -A console -c /etc/snort/snort.conf -R /path/to/custom.rules
```

#### Snort Modes
```bash
# Sniffer mode (packet capture)
snort -i eth0 -v

# Packet logger mode
snort -i eth0 -l /var/log/snort

# NIDS mode (default)
snort -i eth0 -c /etc/snort/snort.conf
```

### Custom Rules

#### Basic Rule Syntax
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
vim /etc/snort/rules/local.rules

# Test rules
snort -T -c /etc/snort/snort.conf

# Reload Snort with new rules
pkill snort
snort -i eth0 -D -c /etc/snort/snort.conf
```

### Monitoring and Analysis

#### View Snort Logs
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

# Analyze with Snort
snort -r capture.pcap -c /etc/snort/snort.conf

# View packet details
tcpdump -r capture.pcap -v
```

### Testing Snort Detection

#### Generate Test Traffic
```bash
# From another container, generate traffic to test Snort
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
- Snort alerts: `/var/log/snort/alert`
- Snort logs: `/var/log/snort/snort.log`
- Auth logs: `/var/log/auth.log`

## Snort Rule Categories
- **Exploit**: Exploit attempts
- **Trojan**: Trojan horse activity
- **Virus**: Virus activity
- **Policy**: Policy violations
- **Info**: Information gathering
- **Recon**: Reconnaissance activity

## Troubleshooting
- Check Snort status: `ps aux | grep snort`
- Test configuration: `snort -T -c /etc/snort/snort.conf`
- Check logs: `tail -f /var/log/snort/alert`
- Verify interface: `ip addr show`
- Monitor traffic: `tcpdump -i any`
- Check rule syntax: `snort -T -c /etc/snort/snort.conf`
