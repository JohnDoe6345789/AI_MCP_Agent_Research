#!/usr/bin/env python3
"""Simple tool to write a .env file.
Usage:
  python make_env.py --out .env KEY=VALUE FOO=BAR
"""

import argparse
from pathlib import Path

def parse_kv(pairs):
    result = []
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid pair: {pair}")
        k, v = pair.split("=", 1)
        result.append((k, v))
    return result

def main():
    parser = argparse.ArgumentParser(description="Create .env file from key=value pairs.")
    parser.add_argument("--out", default=".env", help="Output env file path.")
    parser.add_argument("pairs", nargs="+", help="KEY=VALUE entries.")
    args = parser.parse_args()

    kvs = parse_kv(args.pairs)
    out = Path(args.out)

    lines = [f"{k}={v}" for k, v in kvs]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
