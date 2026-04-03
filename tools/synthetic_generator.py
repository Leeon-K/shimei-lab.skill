#!/usr/bin/env python3
import argparse
import json
import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_FORBIDDEN = [
    "好羡慕你",
    "你说什么都对",
    "我好崇拜你",
]

SCENARIO_BANK = {
    "experiment_blocker": {
        "progress": [
            "baseline 已经跑通，新的模型在 train 上有提升",
            "做完两组对照实验，指标波动很大",
            "先复现了论文设定，目前能稳定出结果",
        ],
        "blockers": [
            "验证集指标没有提升",
            "loss 曲线后期震荡比较明显",
            "当前 ablation 结果解释不够清晰",
        ],
        "worries": [
            "怕这个方向最后没有增益",
            "担心是评估流程哪里出了问题",
            "怕改动太多导致结论不可靠",
        ],
        "next_actions": [
            "固定学习率，只调整 weight decay 跑一组单变量对照",
            "补一张 train/val 指标对照表并标记每次改动",
            "先检查数据切分和评估脚本版本是否一致",
        ],
        "questions": [
            "你更想先验证正则化还是模型复杂度？",
            "你现在最需要先排除数据问题还是超参问题？",
            "这一轮你打算先保留哪个关键变量不动？",
        ],
    },
    "writing_blocker": {
        "progress": [
            "论文方法部分写完了第一稿",
            "相关工作和实验设置基本整理完",
            "把主要图表和结果段落都补齐了",
        ],
        "blockers": [
            "贡献点写得不够聚焦",
            "结果讨论段落有点空",
            "摘要里信息太多但重点不突出",
        ],
        "worries": [
            "怕审稿人看不出核心创新",
            "担心结构不够流畅",
            "怕 rebuttal 时证据链不够硬",
        ],
        "next_actions": [
            "把贡献点压缩成三条，每条都对齐证据",
            "给每个主要结论补一条对照或消融证据",
            "先重写摘要第一句，明确问题和贡献",
        ],
        "questions": [
            "你觉得最需要先强化动机还是证据？",
            "你希望先改摘要还是先改实验分析段？",
            "当前最可能被审稿人追问的是哪一块？",
        ],
    },
    "pre_meeting": {
        "progress": [
            "本周主要实验都跑完了",
            "组会 PPT 已经有初版",
            "关键图表已经整理成稿",
        ],
        "blockers": [
            "讲故事线还有点散",
            "失败实验还没解释到位",
            "下一步计划写得偏泛",
        ],
        "worries": [
            "怕组会上被追问细节",
            "担心报告缺少清晰结论",
            "怕时间控制不好",
        ],
        "next_actions": [
            "把每页都改成问题-证据-结论三行结构",
            "为失败实验补一页原因和修正计划",
            "做一次 5 分钟口述演练并删掉冗余页",
        ],
        "questions": [
            "你这次组会最想让大家记住哪一个结论？",
            "你想先补失败原因，还是先收敛下一步计划？",
            "哪一页最容易被问穿，我们先加证据？",
        ],
    },
}


@dataclass
class Config:
    persona_name: str
    encouragement_mode: str
    sessions: int
    turns_min: int
    turns_max: int
    seed: int
    scenarios: list[str]


def load_config(path: Path) -> Config:
    data = json.loads(path.read_text(encoding="utf-8"))
    persona = data.get("persona", {})
    generation = data.get("generation", {})
    scenario_cfg = data.get("scenarios", {})

    turns = generation.get("turns_per_session", [6, 12])
    if not isinstance(turns, list) or len(turns) != 2:
        raise ValueError("generation.turns_per_session must be [min, max]")

    selected = scenario_cfg.get("types", list(SCENARIO_BANK.keys()))
    selected = [s for s in selected if s in SCENARIO_BANK]
    if not selected:
        raise ValueError("No valid scenarios selected")

    return Config(
        persona_name=persona.get("name", "shimei"),
        encouragement_mode=persona.get("praise_style", "specific_not_flattery"),
        sessions=int(generation.get("sessions", 20)),
        turns_min=max(2, int(turns[0])),
        turns_max=max(2, int(turns[1])),
        seed=int(generation.get("seed", 42)),
        scenarios=selected,
    )


def choose_line(rng: random.Random, seq: list[str]) -> str:
    return seq[rng.randrange(len(seq))]


def user_message(rng: random.Random, scenario: dict[str, list[str]]) -> str:
    return (
        f"今天进度：{choose_line(rng, scenario['progress'])}。"
        f"\n当前卡点：{choose_line(rng, scenario['blockers'])}。"
        f"\n我担心：{choose_line(rng, scenario['worries'])}。"
    )


def assistant_message(
    rng: random.Random,
    persona_name: str,
    scenario: dict[str, list[str]],
) -> str:
    progress = choose_line(rng, scenario["progress"])
    blocker = choose_line(rng, scenario["blockers"])
    next_action = choose_line(rng, scenario["next_actions"])
    question = choose_line(rng, scenario["questions"])

    return (
        f"进度理解：你已经完成了“{progress}”，当前主要阻塞在“{blocker}”。\n"
        f"具体肯定：你先把现象和担忧分开描述，这个拆解非常有效。\n"
        f"关键追问：{question}\n"
        f"下一步行动：先用 30 分钟做这一步：{next_action}。"
    )


def generate_dataset(cfg: Config) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rng = random.Random(cfg.seed)
    now = datetime.now(timezone.utc)
    rows: list[dict[str, Any]] = []
    used_scenarios: list[str] = []

    for s_idx in range(1, cfg.sessions + 1):
        scenario_name = cfg.scenarios[(s_idx - 1) % len(cfg.scenarios)]
        used_scenarios.append(scenario_name)
        scenario = SCENARIO_BANK[scenario_name]

        turns = rng.randint(cfg.turns_min, cfg.turns_max)
        if turns % 2 == 1:
            turns += 1

        ts = now + timedelta(minutes=s_idx)
        session_id = f"s{s_idx:03d}"

        for turn in range(1, turns + 1):
            role = "user" if turn % 2 == 1 else "assistant"
            if role == "user":
                text = user_message(rng, scenario)
                tags = ["progress_update", scenario_name]
                quality = None
            else:
                text = assistant_message(rng, cfg.persona_name, scenario)
                tags = ["understand", "affirm", "question", "next_action", scenario_name]
                quality = {
                    "grounded": True,
                    "no_flattery": not any(bad in text for bad in DEFAULT_FORBIDDEN),
                    "contains_action": "下一步行动" in text,
                }

            row = {
                "session_id": session_id,
                "turn": turn,
                "role": role,
                "text": text,
                "tags": tags,
                "ts": (ts + timedelta(seconds=turn * 45)).isoformat(),
            }
            if quality is not None:
                row["quality"] = quality
            rows.append(row)

    assistant_rows = [r for r in rows if r["role"] == "assistant"]
    user_rows = [r for r in rows if r["role"] == "user"]
    avg_len = sum(len(r["text"]) for r in assistant_rows) / max(1, len(assistant_rows))
    question_density = sum("?" in r["text"] or "？" in r["text"] for r in assistant_rows) / max(1, len(assistant_rows))

    profile = {
        "meta": {
            "version": "0.1",
            "source": "synthetic",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "sessions": cfg.sessions,
            "messages": len(rows),
        },
        "style_features": {
            "avg_msg_len": round(avg_len, 1),
            "question_density": round(question_density, 3),
            "encouragement_mode": cfg.encouragement_mode,
        },
        "dialogue_patterns": {
            "feedback_template": ["进度理解", "具体肯定", "关键追问", "下一步行动"],
            "forbidden_phrases": DEFAULT_FORBIDDEN,
            "assistant_message_count": len(assistant_rows),
            "user_message_count": len(user_rows),
        },
        "scenario_coverage": sorted(set(used_scenarios)),
    }
    return rows, profile


def write_outputs(rows: list[dict[str, Any]], profile: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "raw_chat.jsonl"
    profile_path = out_dir / "distilled_profile.json"

    with raw_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {raw_path}")
    print(f"wrote {profile_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic shimei chat dataset")
    parser.add_argument("--config", default="synthetic_data/config.json", help="Path to config json")
    parser.add_argument("--out-dir", default="data/synthetic", help="Output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(Path(args.config))
    rows, profile = generate_dataset(cfg)
    write_outputs(rows, profile, Path(args.out_dir))


if __name__ == "__main__":
    main()
