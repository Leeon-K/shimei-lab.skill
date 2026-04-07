#!/usr/bin/env python3
import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
PROGRESS_LOG = ROOT / "data" / "progress_log.jsonl"

QUESTIONS = {
    "experiment": [
        "今天你最想先验证哪个单变量？",
        "你这轮最关键的评估指标是哪一个？",
        "当前现象对应的第一假设是什么？",
    ],
    "writing": [
        "你今天想先补哪一段证据链？",
        "摘要里最想先强化哪句贡献？",
        "哪个结论最需要补对照实验？",
    ],
    "meeting": [
        "组会里你最想让大家记住的一个结论是什么？",
        "哪一页最容易被追问，我们要先补证据吗？",
        "下一步计划里最可执行的一步是什么？",
    ],
}

REWARDS = {
    "spring": [
        "如果今天这轮推进完成，我们就给自己一个春天奖励：去玉渊潭看花。",
        "这块收住以后，给自己安排一个轻松奖励：春天出门走走拍几张花。",
        "这一段搞定后就兑现奖励，去看花放松一下再继续冲下一段。",
    ],
    "photo": [
        "你愿意的话，解决完这轮我们安排一次轻松拍照，顺便记录春天。",
        "等这块收尾了，出去拍一组春景照当里程碑纪念吧。",
    ],
    "default": [
        "这一轮做完就给自己一个小奖励，保持科研节奏更稳。",
        "把阶段任务收尾后休息一下，再继续下一轮会更有效率。",
    ],
}


def _load_latest(project: str) -> dict:
    if not PROGRESS_LOG.exists():
        return {}
    rows = []
    for line in PROGRESS_LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        if obj.get("project") == project:
            rows.append(obj)
    return rows[-1] if rows else {}


def _pick(topic: str, seed: Optional[int]) -> str:
    bank = QUESTIONS.get(topic, QUESTIONS["experiment"])
    rng = random.Random(seed)
    return bank[rng.randrange(len(bank))]


def _pick_reward(mode: str, seed: Optional[int]) -> str:
    bank = REWARDS.get(mode, REWARDS["default"])
    rng = random.Random((seed or 0) + 101)
    return bank[rng.randrange(len(bank))]


def compose(
    project: str,
    topic: str,
    reward_mode: str,
    include_reward: bool,
    seed: Optional[int],
) -> str:
    latest = _load_latest(project)
    done = latest.get("done", "（还没收到你今天的进度）")
    blocker = latest.get("blocker", "（还没收到你当前卡点）")
    nxt = latest.get("next", "（还没收到你计划的下一步）")
    q = _pick(topic, seed)

    parts = [
        "今日科研打卡时间到啦，我们来做一次简短同步。",
        f"- 我记录到你上次完成了：{done}",
        f"- 当前卡点是：{blocker}",
        f"- 上次下一步计划：{nxt}",
        f"- 今天我最想请教你的一个问题：{q}",
        "请你按这个格式回我：今日进度 / 当前卡点 / 下一步。",
    ]

    if include_reward:
        parts.append(f"奖励模式：{_pick_reward(reward_mode, seed)}")

    parts.append(f"发送时间（UTC）：{datetime.now(timezone.utc).isoformat()}")
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compose daily check-in message")
    parser.add_argument("--project", default="default")
    parser.add_argument("--topic", choices=sorted(QUESTIONS), default="experiment")
    parser.add_argument("--include-reward", action="store_true")
    parser.add_argument("--reward-mode", choices=sorted(REWARDS), default="default")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    print(
        compose(
            project=args.project,
            topic=args.topic,
            reward_mode=args.reward_mode,
            include_reward=args.include_reward,
            seed=args.seed,
        )
    )


if __name__ == "__main__":
    main()
