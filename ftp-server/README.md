# FTP Server Container (vsftpd)

## Overview
This container provides an FTP server using vsftpd on Ubuntu 24.04 with common tools, logging, and SSH access, following the conventions used in this repository.

## Features
- Ubuntu 24.04 LTS base image
- vsftpd FTP server
- Precreated user `ftpuser` with password `ftppass`
- Local root at `/home/ftpuser/ftp`
- SSH access (root:pass)
- Logging enabled (rsyslog)
- Healthcheck on port 21

## Installed Packages
- FTP Server: vsftpd
- SSH: openssh-server
- Logging: rsyslog
- Network Tools: net-tools, iproute2, iputils-ping, tcpdump
- Text Editors: vim, nano
- Utilities: curl, wget, procps

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

### FTP Access
- Server listens on port 21
- Use credentials: `ftpuser` / `ftppass`
- Home directory: `/home/ftpuser/ftp`

### Example (docker run)
```bash
docker build -t ae3gis-ftp ftp-server

docker run --rm -it \
  -p 2121:21 -p 2222:22 \
  --name ae3gis-ftp \
  ae3gis-ftp
```

### Logging
- System logs: `/var/log/syslog`
- vsftpd log: `/var/log/vsftpd.log` (if enabled)
- Auth logs: `/var/log/auth.log`

## Troubleshooting
- Check vsftpd status: `ps aux | grep vsftpd`
- Verify port: `ss -ltnp | grep :21`
- If login fails, ensure user exists and password is correct


