#!/usr/bin/env bash
set -euo pipefail

# Prepare share directory
mkdir -p "${SMB_SHARE_PATH}"
chmod 0775 "${SMB_SHARE_PATH}"

# Ensure UNIX + Samba user exist
if ! id -u "${SMB_USER}" >/dev/null 2>&1; then
  useradd -M -s /bin/bash "${SMB_USER}" || true
fi
echo "${SMB_USER}:${SMB_PASS}" | chpasswd
(echo "${SMB_PASS}"; echo "${SMB_PASS}") | smbpasswd -s -a "${SMB_USER}"
smbpasswd -e "${SMB_USER}"

# Build dynamic share definition
cat >/etc/samba/shares.conf <<EOF
[${SMB_SHARE_NAME}]
   path = ${SMB_SHARE_PATH}
   browseable = ${SMB_BROWSEABLE}
   read only = ${SMB_READ_ONLY}
   guest ok = ${SMB_GUEST_OK}
   valid users = ${SMB_USER}
   force user = ${SMB_USER}
   create mask = 0664
   directory mask = 0775
EOF
grep -q "include = /etc/samba/shares.conf" /etc/samba/smb.conf || echo -e "\ninclude = /etc/samba/shares.conf" >> /etc/samba/smb.conf

# Fix perms
chown -R "${SMB_USER}:${SMB_USER}" "${SMB_SHARE_PATH}"

# Start services in background
rsyslogd
/usr/sbin/sshd
/usr/sbin/smbd --foreground --no-process-group &
# /usr/sbin/nmbd --foreground --no-process-group &   # optional, if you want NetBIOS

# Show IPs on console
ip -4 addr show || true

# Exec user-supplied command or a login shell
if [[ $# -gt 0 ]]; then
  exec "$@"
else
  exec /bin/bash -l
fi