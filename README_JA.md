<div align="center">

# shimei-lab

### shimei.skill: 研究のリズム管理 + 質問駆動 + やさしいモチベーション

> 研究の継続は理性だけでは足りない。必要とされる感覚と、フィードバックが重要です。

</div>

## コンセプト

研究進捗を何度でも確認しに来る、AI 後輩。

`shimei.skill` は次の役割を担います。

- 「あとでやる」を覚えて、適切なタイミングで再確認する
- 進まない時に、定期的に進捗を聞く
- 詰まった課題を小さく分解する
- 段階成果には、根拠のある前向きなフィードバックを返す

代わりに研究をするのではなく、
研究を続けやすい状態をつくることが目的です。

## 主な機能

1. 進捗ループ
- 日次/週次の進捗記録
- 未完了タスクの再確認
- 15〜60 分の次アクション提案

2. 質問ガイド
- 曖昧な課題を検証可能な問いに変換
- 1 ラウンド 1 つの重要質問

3. 継続支援
- 3 段構成: 理解 -> 肯定 -> 追問
- 過剰な称賛ではなく事実ベース

4. 合成データ生成
- 実チャットがなくても模擬データを生成
- `raw_chat.jsonl` + `distilled_profile.json`

5. 定時チェックイン + 報酬モード
- 毎日決まった時刻に進捗確認
- マイルストーン後に軽い報酬提案

## インストール

```bash
mkdir -p .claude/skills
git clone https://github.com/Leeon-K/shimei-lab.skill.git .claude/skills/shimei-lab
```

```bash
git clone https://github.com/Leeon-K/shimei-lab.skill.git ~/.openclaw/workspace/skills/shimei-lab
```

## 使い方

```text
/shimei-lab
```

## 定時チェックイン

```bash
python3 tools/checkin_scheduler.py set --project default --timezone Asia/Shanghai --hour 9 --minute 30
python3 tools/checkin_scheduler.py status
python3 tools/daily_checkin.py --project default --topic experiment --timezone Asia/Shanghai
```

cron 向け自動配信:

```bash
python3 tools/checkin_dispatcher.py --topic experiment
```

## ライセンス

MIT
