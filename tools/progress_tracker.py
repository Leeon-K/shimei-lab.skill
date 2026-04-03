#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "progress_log.jsonl"


def log_entry(project: str, done: str, blocker: str, nxt: str) -> None:
    DATA.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "project": project,
        "done": done,
        "blocker": blocker,
        "next": nxt,
    }
    with DATA.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("logged")


def tail(n: int) -> None:
    if not DATA.exists():
        print("[]")
        return
    lines = DATA.read_text(encoding="utf-8").splitlines()[-n:]
    rows = [json.loads(x) for x in lines if x.strip()]
    print(json.dumps(rows, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="shimei-lab progress tracker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_log = sub.add_parser("log")
    p_log.add_argument("--project", default="default")
    p_log.add_argument("--done", required=True)
    p_log.add_argument("--blocker", required=True)
    p_log.add_argument("--next", required=True)

    p_tail = sub.add_parser("tail")
    p_tail.add_argument("-n", type=int, default=5)

    args = parser.parse_args()
    if args.cmd == "log":
        log_entry(args.project, args.done, args.blocker, args.next)
    else:
        tail(args.n)


if __name__ == "__main__":
    main()
