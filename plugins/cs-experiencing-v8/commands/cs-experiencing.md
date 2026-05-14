---
description: "경험 지식 저장소 - 도메인별 학습 조회/실행/버전업 (/cs-experiencing [test|plan|review|update|version-up|status])"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion
---

# /cs-experiencing [subcommand] [args]

누적된 경험 지식을 도메인별로 관리하고 실행합니다.

## 서브커맨드

| 커맨드 | 설명 |
|--------|------|
| `/cs-experiencing` | 도메인 목록 + 버전 현황 |
| `/cs-experiencing test [URL]` | CS-test 실행 (14-agent 웹 테스트) |
| `/cs-experiencing plan [task]` | CS-plan 실행 |
| `/cs-experiencing review [path] [--focus aspect]` | CS-codebase-review 실행 (5-관점 코드 리뷰) |
| `/cs-experiencing update` | **4개 스킬 모두 버전업** (= version-up all) |
| `/cs-experiencing version-up test` | CS-test 버전 증가 → 새 버전 디렉토리 생성 |
| `/cs-experiencing version-up plan` | CS-plan 버전 증가 |
| `/cs-experiencing version-up review` | CS-codebase-review 버전 증가 |
| `/cs-experiencing version-up design` | cs-design 버전 증가 |
| `/cs-experiencing version-up all` | 4개 도메인 한번에 버전 증가 |
| `/cs-experiencing status` | 모든 도메인 버전 현황 |
| `/cs-experiencing btw [idea]` | **[v4 신규]** 세션 중 개선 아이디어 즉시 캡처 |
| `/cs-experiencing checkpoint` | **[v4 신규]** WIP 체크포인트 커밋 생성 |

## 도메인 현황

| 도메인 | 버전 | 내용 |
|--------|------|------|
| CS-test | v3 | playwright 14-agent 웹 테스트 팀 |
| CS-plan | v3 | TDD+CleanArch 4-agent 플랜 |
| CS-codebase-review | v3 | 5-관점 병렬 코드 리뷰 (Architecture/Quality/Security/Performance/Maintainability) |

## 실행 흐름

`skills/experiencing/SKILL.md` 참고
