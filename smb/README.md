# Samba Server Container

## Overview
This container provides a vulnerable Samba 4.5.9 server for security testing and educational purposes. It includes the EternalBlue vulnerability (CVE-2017-0144) for penetration testing scenarios.

## Features
- Ubuntu 16.04 base image (for compatibility with vulnerable Samba)
- SSH access (root:pass)
- Vulnerable Samba 4.5.9 server
- SMB/CIFS file sharing
- Logging enabled (rsyslog)

## Installed Packages
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps
- **Build Tools**: build-essential, python, ca-certificates, git
- **Samba**: Compiled from source (vulnerable version 4.5.9)

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

# Start Samba server
/usr/local/samba/sbin/smbd -F --no-process-group
```

### Samba Management

#### Check Samba Status
```bash
# Check if Samba is running
ps aux | grep smbd

# Check Samba version
/usr/local/samba/sbin/smbd --version

# Test Samba configuration
/usr/local/samba/bin/testparm
```

#### Samba Configuration
The Samba configuration is located at `/usr/local/samba/etc/smb.conf`. Example configuration:

```ini
[global]
    workgroup = WORKGROUP
    server string = Samba Server
    security = user
    map to guest = Bad User
    guest account = nobody

[shared]
    comment = Shared Folder
    path = /tmp
    browseable = yes
    writable = yes
    guest ok = yes
    public = yes
```

#### Edit Configuration
```bash
# Edit Samba configuration
vim /usr/local/samba/etc/smb.conf

# Test configuration
/usr/local/samba/bin/testparm

# Restart Samba
pkill smbd
/usr/local/samba/sbin/smbd -F --no-process-group
```

### Samba Commands
```bash
# Start Samba in foreground
/usr/local/samba/sbin/smbd -F --no-process-group

# Start Samba in background
/usr/local/samba/sbin/smbd -D

# Start with specific config
/usr/local/samba/sbin/smbd -F -s /usr/local/samba/etc/smb.conf

# List shares
/usr/local/samba/bin/smbclient -L localhost
```

### Testing Samba Functionality

#### From Samba Server
```bash
# Monitor SMB traffic
tcpdump -i any port 139 or port 445

# Check Samba logs
tail -f /var/log/syslog | grep smbd

# List active connections
/usr/local/samba/bin/smbstatus
```

#### From Client
```bash
# Connect to Samba share
smbclient //<samba_ip>/shared

# Mount Samba share
mount -t cifs //<samba_ip>/shared /mnt -o username=guest

# List shares
smbclient -L <samba_ip>
```

### Security Testing

#### Vulnerability Scanning
```bash
# Scan for SMB vulnerabilities
nmap --script smb-vuln-* <samba_ip>

# Check for EternalBlue
nmap --script smb-vuln-ms17-010 <samba_ip>

# SMB enumeration
nmap --script smb-enum-shares <samba_ip>
```

#### Exploitation (Educational Only)
```bash
# Using Metasploit (if available)
msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <samba_ip>
exploit
```

### Logging
- System logs: `/var/log/syslog`
- Samba logs: `/var/log/syslog` (filter for smbd)
- Auth logs: `/var/log/auth.log`

## Security Considerations
⚠️ **WARNING**: This container contains a vulnerable Samba version with known security issues:
- **CVE-2017-0144**: EternalBlue vulnerability
- **CVE-2017-0143**: EternalRomance vulnerability
- **CVE-2017-0145**: EternalChampion vulnerability

**Use only in:**
- Controlled lab environments
- Authorized security testing
- Educational purposes
- Isolated networks

## Configuration
- SSH is configured to allow root login with password authentication
- Samba is compiled from source with vulnerable version 4.5.9
- Default shares are configured for testing
- Logging is enabled for audit trails

## Troubleshooting
- Check Samba status: `ps aux | grep smbd`
- Test configuration: `/usr/local/samba/bin/testparm`
- Check logs: `tail -f /var/log/syslog | grep smbd`
- Monitor traffic: `tcpdump -i any port 139 or port 445`
- Verify shares: `/usr/local/samba/bin/smbclient -L localhost`
