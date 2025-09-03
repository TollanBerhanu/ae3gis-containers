Connect DHCP server and multiple VPCS workstations via a Switch

on DHCP server
```bash
# start dhcp server
/usr/local/bin/start.sh
```

on VPCS workstation
```bash
# look for dhcp server and request IP
ip dhcp
```

For testing, ping one VPCS from another using the IPs obtained from the DHCP server