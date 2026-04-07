<div align="center">

# shimei-lab

### shimei.skill: 연구 리듬 관리 + 질문 기반 진행 + 부드러운 동기 부여

> 연구를 계속하게 만드는 힘은 이성만이 아닙니다. 필요하다는 감각과 피드백이 중요합니다.

</div>

## 핵심 아이디어

연구 진행 상황을 주기적으로 다시 물어보는 AI 후배.

`shimei.skill`은 다음을 돕습니다.

- "나중에 할게"를 기억하고 적절한 시점에 다시 확인
- 진행이 멈추면 정해진 시간에 체크인
- 막힌 문제를 더 작은 실행 단위로 분해
- 단계 성과가 나오면 과하지 않은, 근거 있는 긍정 피드백 제공

연구를 대신 해주는 도구가 아니라,
연구를 계속하기 쉬운 상태를 만드는 동반자입니다.

## 주요 기능

1. 진행 루프
- 일/주 단위 진행 기록
- 미해결 항목 자동 재확인
- 15~60분 단위 다음 액션 제안

2. 질문 가이드
- 모호한 막힘을 검증 가능한 질문으로 변환
- 라운드당 핵심 질문 1개

3. 지속 지원
- 3단계 피드백: 이해 -> 칭찬 -> 질문
- 과장된 칭찬이 아닌 사실 기반 피드백

4. 합성 데이터 생성
- 실제 채팅 로그가 없어도 모의 데이터 생성
- `raw_chat.jsonl` + `distilled_profile.json`

5. 매일 정시 체크인 + 보상 모드
- 매일 고정 시간에 연구 진행 확인
- 단계 완료 후 가벼운 보상 문구 추가 가능

## 설치

```bash
mkdir -p .claude/skills
git clone https://github.com/Leeon-K/shimei-lab.skill.git .claude/skills/shimei-lab
```

## 사용

```text
/shimei-lab
```

## 정시 체크인

```bash
python3 tools/checkin_scheduler.py set --project default --timezone Asia/Shanghai --hour 9 --minute 30
python3 tools/checkin_scheduler.py status
python3 tools/daily_checkin.py --project default --topic experiment --timezone Asia/Shanghai
```

cron 자동 발송:

```bash
python3 tools/checkin_dispatcher.py --topic experiment
```

## 라이선스

MIT
