nftables terminal:
```
# Check that it's working
nft --version

# Check loaded ruleset (initially empty)
nft list ruleset

# Flush and update ruleset using nftables.conf file
nft -f /etc/nftables.conf 

# Check loaded ruleset (should contain the input, forward and/or output rulesets)
# Input/Output is for incoming/outgoing traffic to/from the firewall
# Forward is for traffic that passes through
nft list ruleset
```

Benign / Malicious client:
```
# Ping / Nmap before ruleset is loaded (works)
# Ping / Nmap after ruleset is loaded (unable to reach host)
```