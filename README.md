# wonka
Golden Ticket attack automation for red vs blue competitions
## Prerequisites
### DNS
For the attack to work Kerberos needs to be able to resolve the FQDN (can add to /etc/hosts if need to)

## Setup
These setup instructions assume you are using Kali Linux. If using a different operating system the instructions may slightly differ

### Install packages
```
sudo apt install ansible python3-impacket python3-winrm python3-requests-kerberos krb5-user
```