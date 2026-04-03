<div align="center">

# shimei-lab

### 师妹.skill：科研节奏管理 + 提问驱动 + 轻量情绪激励

> 科研动力 ≠ 只靠理性，还很依赖“被需要感 + 反馈感”。

*Not a flatter bot, but a reliable junior researcher companion.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-7c4dff.svg)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Compatible-4CAF50.svg)](https://agentskills.io)

</div>

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

## 安装

### Claude Code

```bash
# 当前项目安装
mkdir -p .claude/skills
git clone https://github.com/your-org/shimei-lab.git .claude/skills/shimei-lab

# 全局安装
# git clone https://github.com/your-org/shimei-lab.git ~/.claude/skills/shimei-lab
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

## 项目结构

```text
shimei-lab/
├── SKILL.md                     # 入口与工作流
├── prompts/
│   ├── intake.md                # 进度收集与目标对齐
│   ├── feedback.md              # 三段式反馈模板
│   ├── questioning.md           # 关键追问策略
│   └── planning.md              # next action 生成
├── tools/
│   ├── progress_tracker.py      # 进度记录与待办闭环
│   ├── question_generator.py    # 卡点问题生成
│   ├── session_manager.py       # 会话状态管理
│   └── synthetic_generator.py   # 模拟聊天数据生成器
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

`shimei-lab` 在两者启发下，选择了自己的定位：

- 更强调“科研节奏管理 + 轻量情绪激励 + 可长期使用的稳定交互”

## License

MIT
