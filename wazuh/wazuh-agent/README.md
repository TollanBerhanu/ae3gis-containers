# Wazuh Agent Container

## Overview
This container provides a Wazuh agent for endpoint security monitoring. The Wazuh agent collects security events, system information, and performs real-time monitoring of the host system.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- Wazuh agent for endpoint monitoring
- Logging enabled (rsyslog)
- IPv4 forwarding enabled

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **Security**: wazuh-agent

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

# Start Wazuh agent
service wazuh-agent start
```

### Wazuh Agent Management

#### Check Wazuh Agent Status
```bash
# Check if Wazuh agent is running
ps aux | grep wazuh

# Check Wazuh agent version
/var/ossec/bin/wazuh-control info

# Check agent status
/var/ossec/bin/agent_control -l
```

#### Wazuh Agent Configuration
The Wazuh agent configuration is located at `/var/ossec/etc/ossec.conf`. Key configuration sections:

```xml
<ossec_config>
    <client>
        <server-ip>192.168.1.100</server-ip>
        <config-profile>ubuntu</config-profile>
        <notify_time>10</notify_time>
        <time-reconnect>60</time-reconnect>
        <auto_restart>yes</auto_restart>
    </client>
    
    <client_buffer>
        <disabled>no</disabled>
        <queue_size>5000</queue_size>
        <events_per_second>500</events_per_second>
    </client_buffer>
</ossec_config>
```

#### Edit Configuration
```bash
# Edit Wazuh agent configuration
vim /var/ossec/etc/ossec.conf

# Test configuration
/var/ossec/bin/wazuh-control info

# Restart Wazuh agent
service wazuh-agent restart
```

### Wazuh Agent Commands

#### Basic Operations
```bash
# Start Wazuh agent
service wazuh-agent start

# Stop Wazuh agent
service wazuh-agent stop

# Restart Wazuh agent
service wazuh-agent restart

# Check status
service wazuh-agent status
```

#### Agent Control
```bash
# List agents
/var/ossec/bin/agent_control -l

# Get agent info
/var/ossec/bin/agent_control -i <agent_id>

# Restart agent
/var/ossec/bin/agent_control -r <agent_id>

# Remove agent
/var/ossec/bin/agent_control -r <agent_id>
```

### Monitoring and Analysis

#### View Wazuh Logs
```bash
# View Wazuh agent logs
tail -f /var/ossec/logs/ossec.log

# View alerts
tail -f /var/ossec/logs/alerts/alerts.log

# View system logs
tail -f /var/log/syslog | grep wazuh
```

#### Check Agent Communication
```bash
# Check agent registration
/var/ossec/bin/agent_control -l

# Check communication with manager
/var/ossec/bin/wazuh-control info

# View network connections
netstat -tulpn | grep wazuh
```

### Testing Wazuh Agent

#### Generate Test Events
```bash
# Generate failed login attempts
for i in {1..5}; do ssh root@localhost; done

# Generate file system events
touch /tmp/test_file
rm /tmp/test_file

# Generate process events
ps aux | head -10
```

#### Verify Event Collection
```bash
# Check if events are being collected
tail -f /var/ossec/logs/ossec.log

# Check alerts
tail -f /var/ossec/logs/alerts/alerts.log

# Check agent status
/var/ossec/bin/agent_control -l
```

### Logging
- System logs: `/var/log/syslog`
- Wazuh agent logs: `/var/ossec/logs/ossec.log`
- Wazuh alerts: `/var/ossec/logs/alerts/alerts.log`
- Auth logs: `/var/log/auth.log`

## Wazuh Agent Features
- **Log Collection**: Collects system and application logs
- **File Integrity**: Monitors file system changes
- **Rootkit Detection**: Scans for rootkits and malware
- **Vulnerability Assessment**: Checks for known vulnerabilities
- **Compliance**: PCI DSS, GDPR, HIPAA compliance checks
- **Real-time Monitoring**: Continuous system monitoring

## Troubleshooting
- Check Wazuh agent status: `service wazuh-agent status`
- Check agent info: `/var/ossec/bin/wazuh-control info`
- Check logs: `tail -f /var/ossec/logs/ossec.log`
- Verify network connectivity: `ping <wazuh_manager_ip>`
- Check agent registration: `/var/ossec/bin/agent_control -l`
- Restart agent: `service wazuh-agent restart`
