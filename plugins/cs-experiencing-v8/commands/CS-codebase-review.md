---
description: "5-agent parallel codebase review - Architecture, Quality, Security, Performance, Maintainability"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, TeamCreate, TeamDelete, SendMessage
---

# /CS-codebase-review [path] [--focus aspect]

전체 코드베이스를 5가지 관점에서 병렬 분석하여 종합 리뷰 리포트를 생성합니다.

## 사용법

```
/CS-codebase-review                          # 전체 코드베이스 분석
/CS-codebase-review src/                     # 특정 경로만 분석
/CS-codebase-review --focus security         # 보안 관점만 분석
/CS-codebase-review --focus architecture     # 아키텍처 관점만 분석
```

## 실행

이 커맨드는 `CS-codebase-review-v1/skills/CS-codebase-review/SKILL.md` 프로토콜을 실행합니다.
(CS-codebase-review-v1은 cs-experiencing-v1과 같은 레벨의 plugins/ 디렉토리에 위치)

1. `../CS-codebase-review-v1/VERSION` 읽기 → 현재 버전 확인
2. `../CS-codebase-review-v1/skills/CS-codebase-review/SKILL.md` 프로토콜 실행

## 에이전트 팀 (5개 병렬)

| 에이전트 | 분석 관점 |
|---------|---------|
| **architecture** | 디렉토리 구조, 디자인 패턴, 의존성, 레이어 분리 |
| **quality** | 코드 품질, 복잡도, 중복, 명명 규칙 |
| **security** | OWASP Top 10, 인증/인가, 민감정보 노출 |
| **performance** | 병목 지점, 쿼리 최적화, 캐싱 전략 |
| **maintainability** | 테스트 커버리지, 문서화, 기술 부채 |

## 출력

`codebase-review-report.md` — 종합 코드 리뷰 리포트
