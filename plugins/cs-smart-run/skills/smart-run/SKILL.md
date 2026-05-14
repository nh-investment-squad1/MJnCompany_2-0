---
name: cs-smart-run
user-invocable: true
description: |
  Two-phase orchestrator: Plan with Opus → Execute with Sonnet.
  Opus analyzes the task and produces a structured plan; Sonnet agents
  execute each step in parallel where possible.
  Use when asked to "smart run", "/smart-run", "플랜실행", or when the user
  wants Opus-quality planning with Sonnet-speed execution across multiple skills.
version: 1.0.0
allowed-tools:
  - Agent
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Smart Run — Plan with Opus, Execute with Sonnet

## How this skill works

When invoked, you orchestrate **two distinct phases**:

1. **PLAN phase** — spawn a single Opus agent to think deeply and produce a structured plan
2. **EXEC phase** — spawn one or more Sonnet agents to implement the plan

---

## cmux 환경 지원

cmux 터미널(`$CMUX_SOCKET_PATH` 설정됨)에서 실행 시 진행 상황을 사이드바에 표시한다:

```bash
# Phase 시작 시 호출
[ -n "$CMUX_SOCKET_PATH" ] && cmux set-status "smart-run" "running" --icon "gear"
[ -n "$CMUX_SOCKET_PATH" ] && cmux set-progress 0.0 --label "Smart Run 시작..."
```

각 Phase 전환 시:
- Phase 1 시작: `cmux set-progress 0.2 --label "PLAN: Opus 분석 중..."`
- Phase 2 시작: `cmux set-progress 0.5 --label "EXEC: Sonnet 실행 중..."`
- Phase 3 완료: `cmux set-progress 1.0 --label "완료"` + `cmux notify --title "Smart Run 완료" --body "[태스크 요약]"`

---

## Phase 1: PLAN (Opus)

Spawn ONE agent with `model: "opus"` to analyze the task and return a structured plan.

Prompt the Opus agent with:
```
You are a senior architect. The user wants: <task>

Produce a PLAN with these sections:
## Goal
One-sentence summary.

## Steps
Numbered list. Each step must specify:
- What to do
- Which skill or tool to use (if applicable)
- Input/output dependencies with other steps
- Whether it can run in PARALLEL with other steps (mark with [PARALLEL])

## Risks
Key risks or blockers to watch for.

## Definition of Done
How to verify the work is complete.

Be thorough but concise. This plan will be handed directly to execution agents.
```

Wait for the Opus agent to return the plan before proceeding.

---

## Phase 2: EXEC (Sonnet)

Read the plan from Phase 1. For each step:

- **Independent steps** (marked `[PARALLEL]`): spawn Sonnet agents **simultaneously** in a single message
- **Sequential steps**: spawn Sonnet agents one at a time, passing the previous result as context

Spawn each execution agent with `model: "sonnet"`.

Prompt each Sonnet execution agent with:
```
You are an expert implementer. Execute this specific step from a larger plan:

## Your Step
<step description>

## Full Plan Context
<full plan from Opus>

## Prior Step Results (if any)
<results>

Execute completely. Return: what you did, files changed, and any output the next step needs.
```

---

## Phase 3: REPORT

After all execution agents complete, summarize:
- What was planned (Opus)
- What was executed (Sonnet agents)
- Any steps that failed or need follow-up

---

## Invocation

When the user runs `/smart-run <task>` or `/플랜실행 <task>`:

1. Confirm you understood the task (one line)
2. Announce: "**[PLAN]** Thinking with Opus..."
3. Run Phase 1 (Opus agent)
4. Show the plan to the user, ask for approval or proceed automatically at L2+
5. Announce: "**[EXEC]** Executing with Sonnet..."
6. Run Phase 2 (Sonnet agents)
7. Report results
