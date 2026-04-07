<div align="center">

# shimei-lab

### 师妹.skill：科研节奏管理 + 提问驱动 + 轻量情绪激励

> 科研动力 ≠ 只靠理性，还很依赖“被需要感 + 反馈感”。

*Not a flatter bot, but a reliable junior researcher companion.*

[中文](README.md) | [English](README_EN.md) | [日本語](README_JA.md) | [한국어](README_KO.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-7c4dff.svg)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Compatible-4CAF50.svg)](https://agentskills.io)

</div>

## 系列开场

实验室可以没有导师吗？可以。  
实验室可以没有师兄吗？也可以。  
但谁能拒绝一个按时到实验室、主动请教问题、还会认真汇报进度的师妹？  

假期归来，实验室空得像刚跑完 `rm -rf social_life`；  
深夜盯着 loss 曲线，风扇比人还会聊天；  
午觉醒来，屏幕上只有报错，没有人问你“师兄这步我该先看哪儿”。  

于是我们决定做一件不太严肃但很有用的事：  
给实验室配一个“会追问、会复盘、会鼓励你继续干活”的赛博师妹。  

她不会替你发论文，  
但会在你想摆烂时把问题拆开；  
会在你卡住时追着你给下一步；  
会在你做完阶段任务后提醒你：  
“师兄，春天到了，去玉渊潭公园帮我拍拍照吧，回来我们继续打下一轮。”  

## 核心主张

一个会反复回来催你科研进展的 AI 后辈。  

你不缺一个帮你解决问题的 AI。  
你缺一个，不让你把 TODO 埋进时间黑洞的存在。  

`shimei.skill`，就是实验室里的那个后辈：  

- 你说“这个之后再做”，她会记住并在合适的时间提醒  
- 你拖着没动，她会定时来问一句进展  
- 你卡住的时候，她会帮你把问题拆小一点  
- 你有阶段成果时，她会给你真实、不过度的正反馈  

她不替你做科研。  
她做的是定时陪伴，让科研不那么反感，也更容易坚持。  

一个实验室通常有：  

- 导师，告诉你方向  
- 师兄，教你怎么做  

但真正让你持续推进的，往往不只是“道理”，而是稳定的陪伴和反馈。  

而是那个会隔一段时间就来问你一句：  

“师兄，你上次那个 idea，这周推进到哪一步啦？”  

## 项目定位

`shimei-lab` 是一个“会追问、会记录、会鼓励”的科研搭子型 skill：

- 记录科研进度，形成连续上下文
- 按节奏触发请教问题，推动问题闭环
- 提供基于内容的正反馈，增强行动动力

一句话：

> 不是崇拜你，而是和你一起把科研做下去。

## 设计边界

- 鼓励必须基于事实，禁止无脑夸赞
- 温柔但克制，避免暧昧化和人格依附
- 每轮都落到“下一步可执行动作”

## 功能特性

1. 进度驱动
- 每日/每周追踪任务状态
- 自动回看“上次未闭环事项”
- 生成 15-60 分钟 next action

2. 提问引导
- 将模糊卡点拆成可回答问题
- 根据阶段生成关键追问
- 在用户回答后继续推进闭环

3. 情绪续航
- 三段式反馈：理解 -> 肯定 -> 追问
- 反馈基于用户刚提供的内容
- 低噪音、长期可用

4. 合成数据生成（shimei 特有）
- 在没有真实“师妹聊天记录”时生成模拟数据
- 输出双层产物：`raw_chat.jsonl` + `distilled_profile.json`
- 便于后续蒸馏、评估和风格对齐

5. 每日定时追问 + 奖励模式（shimei 特有）
- 支持设置固定时间每天催科研进度汇报
- 每日自动生成“一个关键问题 + 汇报格式”
- 问题解决后可追加轻量奖励文案（如春天看花、拍照）

## 安装

### Claude Code

```bash
# 当前项目安装
mkdir -p .claude/skills
git clone https://github.com/Leeon-K/shimei-lab.skill.git .claude/skills/shimei-lab

# 全局安装
# git clone https://github.com/Leeon-K/shimei-lab.skill.git ~/.claude/skills/shimei-lab
```

### Python 依赖（可选）

```bash
pip3 install -r requirements.txt
```

## 使用

在 Claude Code 里调用：

```text
/shimei-lab
```

示例：

```text
/shimei-lab 今天我跑了 baseline，但新模型 val 指标没提升，下一步我该先查哪里？
```

## 生成模拟聊天数据

当你没有可导入的真实聊天记录时，可以先生成一批结构化模拟数据：

```bash
python3 tools/synthetic_generator.py \
  --config synthetic_data/config.json \
  --out-dir data/synthetic
```

输出文件：
- `data/synthetic/raw_chat.jsonl`：逐条消息事件流（可回放、可审计）
- `data/synthetic/distilled_profile.json`：风格统计与模板特征（可直接喂给 prompt/skill）

## 每日定时追问与奖励模式

设置每日提醒（例如每天 9:30，Asia/Shanghai）：

```bash
python3 tools/checkin_scheduler.py set --project default --timezone Asia/Shanghai --hour 9 --minute 30
python3 tools/checkin_scheduler.py status
```

生成当日追问文案：

```bash
python3 tools/daily_checkin.py --project default --topic experiment --timezone Asia/Shanghai
```

当阶段任务完成后，可开启奖励模式（春天场景）：

```bash
python3 tools/daily_checkin.py --project default --topic meeting --include-reward --reward-mode spring
```

自动触发（适合 cron）：

```bash
python3 tools/checkin_dispatcher.py --topic experiment
```

## 项目结构

```text
shimei-lab/
├── SKILL.md                     # 入口与工作流
├── prompts/
│   ├── intake.md                # 进度收集与目标对齐
│   ├── feedback.md              # 三段式反馈模板
│   ├── questioning.md           # 关键追问策略
│   ├── planning.md              # next action 生成
│   ├── checkin_schedule.md      # 定时提醒策略
│   └── reward_mode.md           # 奖励模式策略
├── tools/
│   ├── progress_tracker.py      # 进度记录与待办闭环
│   ├── question_generator.py    # 卡点问题生成
│   ├── session_manager.py       # 会话状态管理
│   ├── synthetic_generator.py   # 模拟聊天数据生成器
│   ├── checkin_scheduler.py     # 每日定时状态管理
│   ├── daily_checkin.py         # 每日追问与奖励文案生成
│   └── checkin_dispatcher.py    # 到点自动分发并标记
├── synthetic_data/
│   └── config.json              # 合成数据配置
├── data/
│   └── .gitkeep
├── examples/
│   └── dialogue.md
├── docs/
│   └── style-guide.md
├── INSTALL.md
├── README_EN.md
├── requirements.txt
└── LICENSE
```

## 致敬

本项目明确致敬以下仓库的思路与开源精神：

- [ybq22/supervisor](https://github.com/ybq22/supervisor)：导师式的流程推进、信息蒸馏与 skill 生成路径
- [zhanghaichao520/senpai-skill](https://github.com/zhanghaichao520/senpai-skill)：强人格化叙事、分层 prompts、可演化 skill 管理方式
- [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)：离岗知识延续与“赛博接班”叙事表达

`shimei-lab` 在两者启发下，选择了自己的定位：

- 更强调“科研节奏管理 + 轻量情绪激励 + 可长期使用的稳定交互”

## License

MIT
