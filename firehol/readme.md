Inside the FireHOL container:
``` bash
# Enable FireHOL
echo "START_FIREHOL=YES" > /etc/default/firehol

# check if it is installed
firehol version

# Try loading FireHol
firehol try

# OR
firehol start

# Check if it's running
firehol status


# Confirm rules are loaded
iptables -L -n -v

# OR
iptables-legacy -L -n -v
```
