#!/usr/bin/python3

import argparse
import json
import re
import sys

def parse_mimikatz(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    # Extract Object Security ID (SID)
    sid_match = re.search(r'Object Security ID\s*:\s*(S-1-5-21-\d+(?:-\d+)*)', content)
    
    #Extract aes256_hmac key
    aes_match = re.search(r'aes256_hmac\s*\(\d+\)\s*:\s*([a-fA-F0-9]{64})', content)

    full_sid = sid_match.group(1) if sid_match else None
    
    # Get the Domain SID by stripping off the trailing RID from object SID
    domain_sid = '-'.join(full_sid.split('-')[:-1]) if full_sid else None
    aes256_key = aes_match.group(1) if aes_match else None

    # Construct the data dictionary
    data = {
        "sid": domain_sid,
        "aesKey": aes256_key
    }

    return data

def main():
    parser = argparse.ArgumentParser(description="Parse Mimikatz output and generate a JSON representation of credentials.")
    parser.add_argument("file", help="Path to the Mimikatz text output file")
    parser.add_argument("-o", "--output", help="Optional path to save the output JSON file", default=None)
    
    args = parser.parse_args()

    result = parse_mimikatz(args.file)

    json_output = json.dumps(result, indent=4)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as out_f:
            out_f.write(json_output)
        print(f"[+] JSON successfully written to {args.output}")
    else:
        print(json_output)

if __name__ == '__main__':
    main()