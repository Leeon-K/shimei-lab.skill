#!/usr/bin/env python3
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

import checkin_scheduler
import daily_checkin


def main() -> None:
    parser = argparse.ArgumentParser(description="Dispatch daily check-in if due")
    parser.add_argument("--topic", choices=sorted(daily_checkin.QUESTIONS), default="experiment")
    parser.add_argument("--include-reward", action="store_true")
    parser.add_argument("--reward-mode", choices=sorted(daily_checkin.REWARDS), default="default")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    schedule = checkin_scheduler._read()
    if not schedule:
        raise SystemExit("schedule not set")

    now_utc = datetime.now(ZoneInfo("UTC"))
    if not checkin_scheduler._is_due_now(now_utc, schedule):
        print("not_due")
        return

    message = daily_checkin.compose(
        project=schedule.project,
        topic=args.topic,
        reward_mode=args.reward_mode,
        include_reward=args.include_reward,
        seed=args.seed,
        timezone_name=schedule.timezone,
    )
    print(message)

    schedule.last_sent_at = now_utc.isoformat()
    checkin_scheduler._write(schedule)


if __name__ == "__main__":
    main()
