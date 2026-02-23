# Suricata IDS Container

## Overview
This container provides Suricata, a high-performance Network IDS, IPS, and Network Security Monitoring engine. Suricata is designed to be fast and efficient while providing comprehensive network security monitoring capabilities.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- Suricata IDS/IPS with updated rules
- Custom detection rules for common attacks
- Logging enabled (rsyslog)
- IPv4 forwarding enabled

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **IDS/IPS**: suricata

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
sysctl -w net.ipv4.ip_forward=1

# Start logging service
rsyslogd

# Start SSH service
service ssh start

# Start Suricata
suricata -i eth0 -c /etc/suricata/suricata.yaml -D
```

### Suricata Management

#### Check Suricata Status
```bash
# Check if Suricata is running
ps aux | grep suricata

# Check Suricata version
suricata --version

# Test Suricata configuration
suricata -T -c /etc/suricata/suricata.yaml -v
```

#### Suricata Configuration
The main Suricata configuration is located at `/etc/suricata/suricata.yaml`. Key configuration sections:

```yaml
# Network variables
vars:
  address-groups:
    HOME_NET: "[192.168.0.0/24, 192.168.1.0/24]"
    EXTERNAL_NET: "!$HOME_NET"

# Output plugins
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      community-id: true

# Rule files
rule-files:
  - local.rules
  - suricata.rules
```

#### Edit Configuration
```bash
# Edit Suricata configuration
vim /etc/suricata/suricata.yaml

# Test configuration
suricata -T -c /etc/suricata/suricata.yaml -v

# Update rules
suricata-update

# Create custom rules
vim /etc/suricata/rules/local.rules
```

### Suricata Commands

#### Basic Suricata Operations
```bash
# Run Suricata in console mode
suricata -i eth0 -c /etc/suricata/suricata.yaml

# Run Suricata in daemon mode
suricata -i eth0 -c /etc/suricata/suricata.yaml -D

# Run Suricata with specific interface
suricata -i eth1 -c /etc/suricata/suricata.yaml

# Run Suricata with custom rules
suricata -i eth0 -c /etc/suricata/suricata.yaml -S custom.rules
```

#### Suricata Modes
```bash
# IDS mode (default)
suricata -i eth0 -c /etc/suricata/suricata.yaml

# IPS mode (requires NFQUEUE)
suricata -i eth0 -c /etc/suricata/suricata.yaml --af-packet=eth0

# Offline mode (analyze pcap files)
suricata -r capture.pcap -c /etc/suricata/suricata.yaml
```

### Custom Rules

#### Basic Rule Syntax
```bash
# Alert on ping
alert icmp any any -> any any (msg:"ICMP Ping Detected"; itype:8; threshold:type limit, track by_src, count 1, seconds 60; classtype:icmp-event; sid:1000002; rev:1;)

# Alert on port scan
alert tcp any any -> any any (msg:"Nmap Scan Detected"; flags:S,12; threshold:type limit, track by_src, count 1, seconds 60; classtype:attempted-recon; sid:1000001; rev:1;)

# Alert on HTTP requests
alert http any any -> any any (msg:"HTTP Request"; http_method; content:"GET"; sid:1000003; rev:1;)
```

#### Create Custom Rules
```bash
# Edit local rules file
vim /etc/suricata/rules/local.rules

# Test rules
suricata -T -c /etc/suricata/suricata.yaml -v

# Reload Suricata with new rules
pkill suricata
suricata -i eth0 -c /etc/suricata/suricata.yaml -D
```

### Monitoring and Analysis

#### View Suricata Logs
```bash
# View fast log (alerts)
tail -f /var/log/suricata/fast.log

# View eve.json (structured logs)
tail -f /var/log/suricata/eve.json

# View system logs
tail -f /var/log/syslog | grep suricata
```

#### Analyze Traffic
```bash
# Monitor network traffic
tcpdump -i any -w capture.pcap

# Analyze with Suricata
suricata -r capture.pcap -c /etc/suricata/suricata.yaml

# View packet details
tcpdump -r capture.pcap -v
```

### Testing Suricata Detection

#### Generate Test Traffic
```bash
# From another container, generate traffic to test Suricata
ping <suricata_ip>
nmap -sS <suricata_ip>
curl http://<suricata_ip>
```

#### Verify Detection
```bash
# Check if alerts were generated
cat /var/log/suricata/fast.log

# Monitor real-time alerts
tail -f /var/log/suricata/fast.log

# View structured logs
tail -f /var/log/suricata/eve.json
```

### Rule Management
```bash
# Update Suricata rules
suricata-update

# List available rule sources
suricata-update list-sources

# Enable/disable rule sources
suricata-update enable-source et/open
suricata-update disable-source et/open

# Check rule updates
suricata-update check-updates
```

### Logging
- System logs: `/var/log/syslog`
- Suricata alerts: `/var/log/suricata/fast.log`
- Suricata structured logs: `/var/log/suricata/eve.json`
- Auth logs: `/var/log/auth.log`

## Suricata Features
- **Multi-threaded**: High-performance packet processing
- **Protocol Support**: HTTP, TLS, DNS, SMB, and more
- **Rule Engine**: Flexible rule language
- **Logging**: Multiple output formats (fast.log, eve.json)
- **IPS Mode**: Inline prevention capabilities
- **Community Rules**: Regular rule updates

## Troubleshooting
- Check Suricata status: `ps aux | grep suricata`
- Test configuration: `suricata -T -c /etc/suricata/suricata.yaml -v`
- Check logs: `tail -f /var/log/suricata/fast.log`
- Verify interface: `ip addr show`
- Monitor traffic: `tcpdump -i any`
- Check rule syntax: `suricata -T -c /etc/suricata/suricata.yaml -v`
- Update rules: `suricata-update`
