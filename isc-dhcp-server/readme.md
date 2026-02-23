# ISC DHCP Server Container

## Overview
This container provides an ISC DHCP server for dynamic IP address assignment in network environments. It's ideal for testing DHCP functionality and network configuration scenarios.

## Features
- Ubuntu 24.04 LTS base image
- SSH access (root:pass)
- ISC DHCP server
- Logging enabled (rsyslog)
- Customizable DHCP configuration

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **DHCP Server**: isc-dhcp-server

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

# Start DHCP server manually
/usr/local/bin/start.sh
```

### DHCP Server Management

#### Check DHCP Server Status
```bash
# Check if DHCP server is running
ps aux | grep dhcpd

# Check DHCP server version
dhcpd --version

# Test configuration
dhcpd -t -cf /etc/dhcp/dhcpd.conf
```

#### DHCP Configuration
The DHCP configuration is located at `/etc/dhcp/dhcpd.conf`. Example configuration:

```bash
# Global settings
default-lease-time 600;
max-lease-time 7200;
authoritative;

# Subnet configuration
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    option domain-name "example.com";
}

# Static IP assignment
host server1 {
    hardware ethernet 00:11:22:33:44:55;
    fixed-address 192.168.1.10;
}
```

#### Edit Configuration
```bash
# Edit DHCP configuration
vim /etc/dhcp/dhcpd.conf

# Test configuration
dhcpd -t -cf /etc/dhcp/dhcpd.conf

# Restart DHCP server
systemctl restart isc-dhcp-server
# OR
pkill dhcpd && /usr/sbin/dhcpd -f -d
```

#### DHCP Server Commands
```bash
# Start DHCP server in foreground
/usr/sbin/dhcpd -f -d

# Start DHCP server in background
/usr/sbin/dhcpd

# Start with specific interface
/usr/sbin/dhcpd -f -d eth0

# Start with specific config file
/usr/sbin/dhcpd -f -d -cf /etc/dhcp/dhcpd.conf
```

### Testing DHCP Functionality

#### From DHCP Server
```bash
# Monitor DHCP traffic
tcpdump -i any port 67 or port 68

# Check DHCP leases
cat /var/lib/dhcp/dhcpd.leases

# View DHCP logs
tail -f /var/log/syslog | grep dhcpd
```

#### From Client (VPCS or other container)
```bash
# Request DHCP lease
ip dhcp

# Check assigned IP
ip addr show

# Check routing table
ip route show

# Test connectivity
ping 192.168.1.1
```

### DHCP Lease Management
```bash
# View active leases
cat /var/lib/dhcp/dhcpd.leases

# Clear all leases
rm /var/lib/dhcp/dhcpd.leases
touch /var/lib/dhcp/dhcpd.leases

# Restart DHCP server to reload leases
systemctl restart isc-dhcp-server
```

### Logging
- System logs: `/var/log/syslog`
- DHCP logs: `/var/log/syslog` (filter for dhcpd)
- Auth logs: `/var/log/auth.log`

## DHCP Configuration Options
- **default-lease-time**: Default lease duration in seconds
- **max-lease-time**: Maximum lease duration in seconds
- **authoritative**: Server is authoritative for the subnet
- **range**: IP address range for dynamic assignment
- **option routers**: Default gateway
- **option domain-name-servers**: DNS servers
- **option domain-name**: Domain name

## Troubleshooting
- Check DHCP server status: `ps aux | grep dhcpd`
- Test configuration: `dhcpd -t -cf /etc/dhcp/dhcpd.conf`
- Check logs: `tail -f /var/log/syslog | grep dhcpd`
- Monitor traffic: `tcpdump -i any port 67 or port 68`
- Verify interface: `ip addr show`
- Check leases: `cat /var/lib/dhcp/dhcpd.leases`