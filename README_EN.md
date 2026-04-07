<div align="center">

# shimei-lab

### shimei.skill: Research Rhythm + Question-Driven Coaching + Gentle Motivation

> Research momentum is not only rational. It also depends on being needed and getting feedback.

*Not a flatter bot, but a reliable junior researcher companion.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-7c4dff.svg)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Compatible-4CAF50.svg)](https://agentskills.io)

</div>

## Core Idea

An AI junior who keeps coming back to ask about your research progress.

You do not lack AI tools that can answer questions.
You lack one that does not let your TODOs disappear silently.

`shimei.skill` is that lab junior:

- She remembers your "I'll do it later" items.
- She checks in on schedule if progress stalls.
- She helps break blockers into smaller, executable steps.
- She gives grounded positive feedback when you hit milestones.

She does not do research for you.
She helps make research less draining and easier to sustain.

## Positioning

`shimei-lab` is a companion skill that asks, tracks, and encourages:

- Track research progress with continuity.
- Trigger periodic question-based follow-ups.
- Drive closure with concrete next actions.

One line summary:

> Not idolizing you. Growing with you and keeping research moving.

## Design Boundaries

- Encouragement must be fact-based.
- Tone should be warm but restrained.
- Every round ends with one actionable next step.

## Features

1. Progress Loop
- Daily/weekly status tracking
- Review unresolved items automatically
- Generate a 15-60 minute next action

2. Question Guidance
- Convert vague blockers into answerable questions
- Ask one high-leverage question per round
- Continue follow-up after user replies

3. Emotional Sustainment
- 3-step feedback: understand -> affirm -> ask
- Positive feedback grounded in user facts
- Low-noise style for long-term usage

4. Synthetic Data Generation (shimei-specific)
- Generate data when no real chat history exists
- Output `raw_chat.jsonl` + `distilled_profile.json`
- Useful for distillation, evaluation, and prompt alignment

5. Daily Scheduled Check-ins + Reward Mode (shimei-specific)
- Fixed-time daily research check-ins
- Auto-generate one key question + reply format
- Optional lightweight reward line after milestones

## Installation

### Claude Code

```bash
# Install in current project
mkdir -p .claude/skills
git clone https://github.com/Leeon-K/shimei-lab.skill.git .claude/skills/shimei-lab

# Global install
# git clone https://github.com/Leeon-K/shimei-lab.skill.git ~/.claude/skills/shimei-lab
```

### OpenClaw

```bash
git clone https://github.com/Leeon-K/shimei-lab.skill.git ~/.openclaw/workspace/skills/shimei-lab
```

### Optional Python dependency

```bash
pip3 install -r requirements.txt
```

## Usage

Invoke in Claude Code:

```text
/shimei-lab
```

Example:

```text
/shimei-lab I finished baseline, but the new model did not improve val score. What should I check first?
```

## Generate Synthetic Chat Data

```bash
python3 tools/synthetic_generator.py \
  --config synthetic_data/config.json \
  --out-dir data/synthetic
```

Outputs:
- `data/synthetic/raw_chat.jsonl`
- `data/synthetic/distilled_profile.json`

## Daily Check-in and Reward Mode

Set daily check-in (example: 09:30 Asia/Shanghai):

```bash
python3 tools/checkin_scheduler.py set --project default --timezone Asia/Shanghai --hour 9 --minute 30
python3 tools/checkin_scheduler.py status
```

Generate today's check-in message:

```bash
python3 tools/daily_checkin.py --project default --topic experiment --timezone Asia/Shanghai
```

Enable reward mode after milestone completion:

```bash
python3 tools/daily_checkin.py --project default --topic meeting --include-reward --reward-mode spring
```

Auto-dispatch (good for cron):

```bash
python3 tools/checkin_dispatcher.py --topic experiment
```

## Project Structure

```text
shimei-lab/
├── SKILL.md
├── prompts/
├── tools/
├── synthetic_data/
├── data/
├── examples/
├── docs/
├── INSTALL.md
├── README.md
├── README_EN.md
├── README_JA.md
├── README_KO.md
├── requirements.txt
└── LICENSE
```

## Tribute

This project respectfully draws inspiration from:

- [ybq22/supervisor](https://github.com/ybq22/supervisor)
- [zhanghaichao520/senpai-skill](https://github.com/zhanghaichao520/senpai-skill)
- [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)

## License

MIT
