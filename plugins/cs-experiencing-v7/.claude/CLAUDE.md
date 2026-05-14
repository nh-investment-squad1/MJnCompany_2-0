# cs-experiencing-v4 - 경험 지식 저장소

이 플러그인은 누적된 학습 경험을 도메인별로 관리합니다.

## 도메인 구성

| 도메인 | 현재 버전 | 내용 |
|--------|-----------|------|
| **CS-test** | v14 | 웹 테스트 (14-agent playwright 팀) |
| **CS-plan** | v12 | TDD+CleanArch 플랜 (4-agent: domain-analyst, arch-designer, tdd-strategist, checklist-builder) |
| **CS-codebase-review** | v14 | 5-관점 병렬 코드 리뷰 (Architecture/Quality/Security/Performance/Maintainability) |
| **cs-design** | v9 | 5-관점 병렬 디자인 리뷰 (visual-hierarchy/interaction-quality/design-system-consistency/responsive-accessibility/anti-pattern-detector) |
| **cs-clarify** | v1 | [신규] 요구사항 명료화 (4-agent: clarify-lead, requirements-interviewer, scope-validator, assumption-mapper) |
| **cs-ship** | v1 | [신규] PR 전 검증 게이트 (4-agent: ship-lead, pre-pr-validator, coverage-auditor, commit-crafter) |
| **cs-ceo** | v1 | CS 시리즈 CEO 오케스트레이터 — 공수 추정 후 도메인 자율 배분 + cs-smart-run 자율 선택 |

## 사용법

```
/cs-experiencing                                          # 도메인 목록 및 버전 확인
/cs-experiencing test [URL]                               # CS-test 실행 (14개 에이전트로 웹 테스트)
/cs-experiencing plan [task]                              # CS-plan 실행
/cs-experiencing review [path] [--focus aspect]           # CS-codebase-review 실행 (5-관점 코드 리뷰)
/cs-experiencing design [path] [--focus aspect] [--fix]  # cs-design 실행 (5-관점 디자인 리뷰)
/cs-experiencing version-up test                          # CS-test 버전 업그레이드
/cs-experiencing version-up plan                          # CS-plan 버전 업그레이드
/cs-experiencing version-up review                        # CS-codebase-review 버전 업그레이드
/cs-experiencing version-up design                        # cs-design 버전 업그레이드
/cs-experiencing version-up all                           # 6개 도메인 한번에 버전업
/cs-clarify "[요청]"                                      # [신규] 요구사항 명료화 (플랜 전)
/cs-ship                                                  # [신규] PR 전 최종 검증 게이트
/cs-experiencing btw "[아이디어]"                         # [v4] 세션 중 개선 아이디어 캡처
/cs-experiencing checkpoint                               # [v4] WIP 체크포인트 커밋
```

## 버전 관리

각 도메인의 VERSION 파일이 현재 콘텐츠 버전을 나타냅니다.
새 학습이 추가되면 `/cs-experiencing version-up [domain]` 으로 버전 증가.

## 도메인 파일 구조

6개 도메인은 cs-experiencing-v4과 같은 레벨의 plugins/ 디렉토리에 위치합니다:

```
plugins/
├── cs-experiencing-v4/    ← 이 플러그인 (오케스트레이터)
├── CS-test-v4/
│   ├── VERSION            # 현재: 4
│   ├── agents/            # 14개 테스트 에이전트
│   ├── skills/CS-test/SKILL.md
│   └── commands/CS-test.md
├── CS-plan-v4/
│   ├── VERSION            # 현재: 4
│   ├── agents/            # 4개: domain-analyst, arch-designer, tdd-strategist, checklist-builder
│   ├── commands/CS-plan.md
│   ├── knowledge/README.md
│   └── skills/CS-plan/SKILL.md
├── CS-codebase-review-v4/
│   ├── VERSION            # 현재: 4
│   ├── skills/CS-codebase-review/SKILL.md
│   └── commands/CS-codebase-review.md
└── cs-design-v1/          ← 신규
    ├── VERSION            # 현재: 1
    ├── agents/design-lead.md
    ├── commands/cs-design.md
    ├── references/        # typography, color-contrast, spacing-layout, interaction-states, anti-patterns
    └── skills/cs-design/SKILL.md
```
