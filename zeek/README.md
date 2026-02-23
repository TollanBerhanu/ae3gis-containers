# Zeek Network Security Monitor Container

## Overview
This container provides Zeek (formerly Bro), a powerful network security monitoring platform. Zeek provides comprehensive network analysis capabilities, including protocol analysis, traffic monitoring, and security event detection.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- Zeek 6.0 network security monitor
- ZeekControl for management
- Logging enabled (rsyslog)
- IPv4 forwarding enabled

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **Security**: zeek-6.0, zeek-6.0-core, zeekctl-6.0

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
service ssh start

# Start Zeek
zeekctl start
```

### Zeek Management

#### Check Zeek Status
```bash
# Check if Zeek is running
ps aux | grep zeek

# Check Zeek version
zeek --version

# Check ZeekControl status
zeekctl status
```

#### Zeek Configuration
The main Zeek configuration is located at `/opt/zeek/etc/node.cfg`. Key configuration sections:

```bash
# Node configuration
[zeek]
type=standalone
host=localhost
interface=eth0

# Logging configuration
[logger]
type=logger
host=localhost

[manager]
type=manager
host=localhost

[proxy]
type=proxy
host=localhost
```

#### Edit Configuration
```bash
# Edit Zeek configuration
vim /opt/zeek/etc/node.cfg

# Edit ZeekControl configuration
vim /opt/zeek/etc/zeekctl.cfg

# Test configuration
zeekctl check

# Deploy configuration
zeekctl deploy
```

### Zeek Commands

#### Basic Zeek Operations
```bash
# Start Zeek
zeekctl start

# Stop Zeek
zeekctl stop

# Restart Zeek
zeekctl restart

# Check status
zeekctl status

# Deploy configuration
zeekctl deploy
```

#### Zeek Analysis
```bash
# Run Zeek on live traffic
zeek -i eth0

# Run Zeek on pcap file
zeek -r capture.pcap

# Run Zeek with specific scripts
zeek -i eth0 scripts/policy/misc/scan.zeek

# Run Zeek in daemon mode
zeek -i eth0 -d
```

### Zeek Scripts

#### Basic Scripts
```bash
# List available scripts
zeek -N

# Run specific script
zeek -i eth0 scripts/policy/misc/scan.zeek

# Run multiple scripts
zeek -i eth0 scripts/policy/misc/scan.zeek scripts/policy/protocols/conn/known-services.zeek
```

#### Custom Scripts
```bash
# Create custom script
vim /opt/zeek/share/zeek/site/local.zeek

# Example custom script
event connection_established(c: connection)
{
    print fmt("New connection: %s -> %s", c$id$orig_h, c$id$resp_h);
}
```

### Monitoring and Analysis

#### View Zeek Logs
```bash
# View Zeek logs
tail -f /opt/zeek/logs/current/conn.log

# View specific log types
tail -f /opt/zeek/logs/current/http.log
tail -f /opt/zeek/logs/current/dns.log
tail -f /opt/zeek/logs/current/ssl.log

# View system logs
tail -f /var/log/syslog | grep zeek
```

#### Analyze Traffic
```bash
# Monitor network traffic
tcpdump -i any -w capture.pcap

# Analyze with Zeek
zeek -r capture.pcap

# View analysis results
ls /opt/zeek/logs/current/
```

### Testing Zeek

#### Generate Test Traffic
```bash
# From another container, generate traffic to test Zeek
ping <zeek_ip>
nmap -sS <zeek_ip>
curl http://<zeek_ip>
```

#### Verify Analysis
```bash
# Check if logs are being generated
ls -la /opt/zeek/logs/current/

# View connection logs
tail -f /opt/zeek/logs/current/conn.log

# View HTTP logs
tail -f /opt/zeek/logs/current/http.log
```

### Logging
- System logs: `/var/log/syslog`
- Zeek logs: `/opt/zeek/logs/current/`
- Auth logs: `/var/log/auth.log`

## Zeek Log Types
- **conn.log**: Connection information
- **http.log**: HTTP protocol analysis
- **dns.log**: DNS protocol analysis
- **ssl.log**: SSL/TLS protocol analysis
- **files.log**: File transfer analysis
- **notice.log**: Security notices and alerts

## Zeek Features
- **Protocol Analysis**: Deep packet inspection
- **Traffic Monitoring**: Comprehensive network monitoring
- **Security Detection**: Built-in security event detection
- **Custom Scripts**: Extensible with Zeek scripting language
- **Log Analysis**: Structured log output for analysis
- **Real-time Processing**: Live network analysis

## Troubleshooting
- Check Zeek status: `zeekctl status`
- Check Zeek info: `zeek --version`
- Check logs: `tail -f /opt/zeek/logs/current/conn.log`
- Verify interface: `ip addr show`
- Monitor traffic: `tcpdump -i any`
- Check configuration: `zeekctl check`
- Restart Zeek: `zeekctl restart`
