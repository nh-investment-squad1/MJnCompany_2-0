---
description: "5-agent parallel design review - visual hierarchy, interaction quality, design system consistency, responsive/accessibility, anti-pattern detection"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, TeamCreate, TeamDelete, SendMessage
---

# /mj-design [path] [--focus aspect] [--fix]

CS-design 도메인의 5-agent 병렬 디자인 리뷰를 실행합니다.

## 사용법

```
/mj-design                              # 현재 디렉토리 전체 분석
/mj-design src/                         # 특정 경로 분석
/mj-design --focus visual               # 시각 계층만 분석
/mj-design --focus interaction          # 인터랙션 품질만 분석
/mj-design --focus consistency          # 디자인 시스템 일관성만 분석
/mj-design --focus responsive           # 반응형/접근성만 분석
/mj-design --focus antipatterns         # 안티패턴 탐지만 실행
/mj-design --fix                        # 발견된 안티패턴 자동 수정
```

## 실행

`../mj-design-v1/skills/mj-design/SKILL.md` 프로토콜을 따라 design-lead 에이전트를 스폰합니다.
