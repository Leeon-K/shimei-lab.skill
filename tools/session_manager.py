#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSION_FILE = ROOT / "data" / "session_state.json"


def read_state() -> None:
    if not SESSION_FILE.exists():
        print("{}")
        return
    print(SESSION_FILE.read_text(encoding="utf-8"))


def write_state(payload: str) -> None:
    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    obj = json.loads(payload)
    SESSION_FILE.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    print("updated")


def main() -> None:
    parser = argparse.ArgumentParser(description="shimei-lab session manager")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("get")
    p_set = sub.add_parser("set")
    p_set.add_argument("--json", required=True)
    args = parser.parse_args()

    if args.cmd == "get":
        read_state()
    else:
        write_state(args.json)


if __name__ == "__main__":
    main()
