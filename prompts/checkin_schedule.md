# Check-in Schedule Prompt

Goal: send one daily research check-in message at a fixed local time.

Message should include:
- brief recall of last progress
- one key question for today
- required reply format: 今日进度 / 当前卡点 / 下一步

If user solved last blocker, append optional reward suggestion.

Automation hint:
- Use `tools/checkin_scheduler.py status` to check due state.
- Use `tools/checkin_dispatcher.py` for one-shot dispatch + mark sent.
