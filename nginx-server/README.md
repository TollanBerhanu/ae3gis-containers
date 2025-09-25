# Nginx Server Container

## Overview
This container provides an Nginx HTTP Server on Ubuntu 24.04 with common tools, logging, and SSH access, following the same conventions as `apache-server` in this repository.

## Features
- Ubuntu 24.04 LTS base image
- Nginx web server
- SSH access (root:pass)
- Logging enabled (rsyslog)
- Default index page at `/var/www/html/index.html`
- Healthcheck on `http://127.0.0.1:80/`

## Installed Packages
- Web Server: nginx
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

### Manual Service Startup (if needed)
```bash
# Start logging service
rsyslogd

# Start SSH service
/usr/sbin/sshd -D

# Start Nginx in foreground
nginx -g 'daemon off;'
```

### Web Access
- Default site: http://<container_ip>/
- Document root: /var/www/html

### Mount Your Site (docker run)
```bash
docker build -t ae3gis-nginx nginx-server

docker run --rm -it \
  -p 8080:80 -p 2222:22 \
  -v $(pwd)/site:/var/www/html:ro \
  --name ae3gis-nginx \
  ae3gis-nginx
```

### Logging
- System logs: `/var/log/syslog`
- Nginx access log: `/var/log/nginx/access.log`
- Nginx error log: `/var/log/nginx/error.log`
- Auth logs: `/var/log/auth.log`

## Troubleshooting
- Check Nginx status: `ps aux | grep nginx`
- Tail Nginx logs: `tail -f /var/log/nginx/error.log`
- Healthcheck locally: `curl -v http://127.0.0.1:80/`
- If SSH fails, ensure service is running: `ps aux | grep sshd`


