# Apache Server Container

## Overview
This container provides an Apache HTTP Server on Ubuntu 24.04 with common tools, logging, and SSH access, aligned with conventions used in this repository.

## Features
- Ubuntu 24.04 LTS base image
- Apache2 with `mod_rewrite` enabled and `.htaccess` allowed
- SSH access (root:pass)
- Logging enabled (rsyslog)
- Default index page at `/var/www/html/index.html`
- Healthcheck on `http://127.0.0.1:80/`

## Installed Packages
- **Web Server**: apache2
- **SSH**: openssh-server
- **Logging**: rsyslog
- **Network Tools**: net-tools, iproute2, iputils-ping, tcpdump
- **Text Editors**: vim, nano
- **Utilities**: curl, wget, procps

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

# Start Apache in foreground
apache2ctl -D FOREGROUND
```

### Web Access
- Default site: http://<container_ip>/
- Document root: /var/www/html

### Mount Your Site (docker run)
```bash
docker run --rm -it \
  -p 8080:80 -p 2222:22 \
  -v $(pwd)/site:/var/www/html:ro \
  --name ae3gis-apache \
  ae3gis-apache
```

### Logging
- System logs: `/var/log/syslog`
- Apache logs: `/var/log/apache2/access.log`, `/var/log/apache2/error.log`
- Auth logs: `/var/log/auth.log`

## Configuration
- `ServerName localhost` configured via `a2enconf servername`
- `mod_rewrite` enabled via `a2enmod rewrite`
- `.htaccess` allowed by setting `AllowOverride All` in `apache2.conf`

## Troubleshooting
- Check Apache status: `ps aux | grep apache2`
- Tail Apache logs: `tail -f /var/log/apache2/error.log`
- Healthcheck locally: `curl -v http://127.0.0.1:80/`
- If SSH fails, ensure service is running: `ps aux | grep sshd`
