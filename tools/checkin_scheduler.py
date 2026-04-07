#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "data" / "checkin_schedule.json"


@dataclass
class Schedule:
    project: str
    timezone: str
    hour: int
    minute: int
    last_sent_at: Optional[str]


def _read() -> Optional[Schedule]:
    if not STATE_FILE.exists():
        return None
    obj = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return Schedule(
        project=obj.get("project", "default"),
        timezone=obj.get("timezone", "Asia/Shanghai"),
        hour=int(obj.get("hour", 10)),
        minute=int(obj.get("minute", 0)),
        last_sent_at=obj.get("last_sent_at"),
    )


def _write(s: Schedule) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(
            {
                "project": s.project,
                "timezone": s.timezone,
                "hour": s.hour,
                "minute": s.minute,
                "last_sent_at": s.last_sent_at,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def _next_run(now: datetime, s: Schedule) -> datetime:
    local_now = now.astimezone(ZoneInfo(s.timezone))
    target = local_now.replace(hour=s.hour, minute=s.minute, second=0, microsecond=0)
    if local_now >= target:
        target = target + timedelta(days=1)
    return target.astimezone(ZoneInfo("UTC"))


def cmd_set(args: argparse.Namespace) -> None:
    s = Schedule(
        project=args.project,
        timezone=args.timezone,
        hour=args.hour,
        minute=args.minute,
        last_sent_at=None,
    )
    _write(s)
    print("schedule_saved")


def cmd_status(args: argparse.Namespace) -> None:
    s = _read()
    if not s:
        print(json.dumps({"exists": False}, ensure_ascii=False, indent=2))
        return
    now = datetime.now(ZoneInfo("UTC"))
    next_run = _next_run(now, s)

    due = False
    if s.last_sent_at:
        last = datetime.fromisoformat(s.last_sent_at)
        local_last = last.astimezone(ZoneInfo(s.timezone)).date()
        local_now = now.astimezone(ZoneInfo(s.timezone)).date()
        due = local_last != local_now and now >= next_run - timedelta(days=1)
    else:
        local_now = now.astimezone(ZoneInfo(s.timezone))
        due = local_now.hour > s.hour or (local_now.hour == s.hour and local_now.minute >= s.minute)

    print(
        json.dumps(
            {
                "exists": True,
                "project": s.project,
                "timezone": s.timezone,
                "daily_time": f"{s.hour:02d}:{s.minute:02d}",
                "last_sent_at": s.last_sent_at,
                "next_run_utc": next_run.isoformat(),
                "due_now": due,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_mark(args: argparse.Namespace) -> None:
    s = _read()
    if not s:
        raise SystemExit("schedule not set")
    now = datetime.now(ZoneInfo("UTC")).isoformat()
    s.last_sent_at = now
    _write(s)
    print("marked_sent")


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily check-in scheduler")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_set = sub.add_parser("set")
    p_set.add_argument("--project", default="default")
    p_set.add_argument("--timezone", default="Asia/Shanghai")
    p_set.add_argument("--hour", type=int, default=10)
    p_set.add_argument("--minute", type=int, default=0)
    p_set.set_defaults(func=cmd_set)

    p_status = sub.add_parser("status")
    p_status.set_defaults(func=cmd_status)

    p_mark = sub.add_parser("mark-sent")
    p_mark.set_defaults(func=cmd_mark)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
