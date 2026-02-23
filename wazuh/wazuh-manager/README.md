# Wazuh Manager Container

## Overview
This container provides a Wazuh manager for centralized security monitoring and management. The Wazuh manager collects data from agents, performs analysis, and provides a web interface for security monitoring.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- Wazuh manager for centralized monitoring
- Logging enabled (rsyslog)
- IPv4 forwarding enabled
- Web interface access

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **Security**: wazuh-manager

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

# Start Wazuh manager
service wazuh-manager start
```

### Wazuh Manager Management

#### Check Wazuh Manager Status
```bash
# Check if Wazuh manager is running
ps aux | grep wazuh

# Check Wazuh manager version
/var/ossec/bin/wazuh-control info

# Check manager status
service wazuh-manager status
```

#### Wazuh Manager Configuration
The Wazuh manager configuration is located at `/var/ossec/etc/ossec.conf`. Key configuration sections:

```xml
<ossec_config>
    <global>
        <jsonout_output>yes</jsonout_output>
        <alerts_log>yes</alerts_log>
        <logall>no</logall>
        <logall_json>no</logall_json>
        <email_notification>no</email_notification>
    </global>
    
    <alerts>
        <log_alert_level>3</log_alert_level>
        <email_alert_level>12</email_alert_level>
    </alerts>
    
    <remote>
        <connection>secure</connection>
        <port>1514</port>
        <protocol>tcp</protocol>
    </remote>
</ossec_config>
```

#### Edit Configuration
```bash
# Edit Wazuh manager configuration
vim /var/ossec/etc/ossec.conf

# Test configuration
/var/ossec/bin/wazuh-control info

# Restart Wazuh manager
service wazuh-manager restart
```

### Wazuh Manager Commands

#### Basic Operations
```bash
# Start Wazuh manager
service wazuh-manager start

# Stop Wazuh manager
service wazuh-manager stop

# Restart Wazuh manager
service wazuh-manager restart

# Check status
service wazuh-manager status
```

#### Agent Management
```bash
# List all agents
/var/ossec/bin/agent_control -l

# Get agent info
/var/ossec/bin/agent_control -i <agent_id>

# Restart agent
/var/ossec/bin/agent_control -r <agent_id>

# Remove agent
/var/ossec/bin/agent_control -r <agent_id>

# Add agent
/var/ossec/bin/agent_control -a <agent_ip>
```

### Monitoring and Analysis

#### View Wazuh Logs
```bash
# View Wazuh manager logs
tail -f /var/ossec/logs/ossec.log

# View alerts
tail -f /var/ossec/logs/alerts/alerts.log

# View system logs
tail -f /var/log/syslog | grep wazuh
```

#### Check Manager Status
```bash
# Check manager info
/var/ossec/bin/wazuh-control info

# Check agent connections
/var/ossec/bin/agent_control -l

# Check network connections
netstat -tulpn | grep wazuh
```

### Web Interface

#### Access Web Interface
```bash
# Check if web interface is running
ps aux | grep wazuh

# Access web interface
# URL: http://<manager_ip>:443
# Default credentials: admin/wazuh
```

#### Web Interface Features
- **Dashboard**: Real-time security overview
- **Agents**: Agent management and monitoring
- **Rules**: Rule management and customization
- **Logs**: Log analysis and search
- **Reports**: Security reports and compliance
- **Settings**: System configuration

### Testing Wazuh Manager

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

#### Verify Event Processing
```bash
# Check if events are being processed
tail -f /var/ossec/logs/ossec.log

# Check alerts
tail -f /var/ossec/logs/alerts/alerts.log

# Check agent status
/var/ossec/bin/agent_control -l
```

### Logging
- System logs: `/var/log/syslog`
- Wazuh manager logs: `/var/ossec/logs/ossec.log`
- Wazuh alerts: `/var/ossec/logs/alerts/alerts.log`
- Auth logs: `/var/log/auth.log`

## Wazuh Manager Features
- **Centralized Management**: Manage multiple agents from one interface
- **Real-time Monitoring**: Continuous security monitoring
- **Log Analysis**: Advanced log analysis and correlation
- **Rule Engine**: Customizable detection rules
- **Compliance**: PCI DSS, GDPR, HIPAA compliance monitoring
- **Web Interface**: User-friendly web dashboard
- **API**: RESTful API for integration

## Ports
- **22**: SSH access
- **1514**: Agent communication (TCP)
- **1515**: Agent communication (UDP)
- **443**: Web interface (HTTPS)
- **55000**: Wazuh API

## Troubleshooting
- Check Wazuh manager status: `service wazuh-manager status`
- Check manager info: `/var/ossec/bin/wazuh-control info`
- Check logs: `tail -f /var/ossec/logs/ossec.log`
- Verify network connectivity: `ping <agent_ip>`
- Check agent connections: `/var/ossec/bin/agent_control -l`
- Restart manager: `service wazuh-manager restart`
- Check web interface: `curl -k https://localhost:443`
