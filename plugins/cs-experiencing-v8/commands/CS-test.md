---
description: "14-agent AI Teams web testing - runs the CS-test domain protocol from cs-experiencing-v1"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList, TaskGet, TeamCreate, TeamDelete, SendMessage, ToolSearch
---

# /CS-test [URL]

14개의 전문 Claude AI 에이전트가 팀을 구성하여 웹 앱을 종합 테스트합니다.

## 사용법

```
/CS-test https://example.com
/CS-test https://example.com --skip-build
```

## 실행

이 커맨드는 `CS-test-v1/skills/CS-test/SKILL.md` 프로토콜을 실행합니다.
(CS-test-v1은 cs-experiencing-v1과 같은 레벨의 plugins/ 디렉토리에 위치)

URL을 대상으로 14-agent 팀을 가동하세요:
1. `../CS-test-v1/VERSION` 읽기 → 현재 버전 확인
2. `../CS-test-v1/skills/CS-test/SKILL.md` 프로토콜 실행

## 에이전트 팀 (14개)

| Phase | 에이전트 | 역할 |
|-------|---------|------|
| 0 | **build-validator** | 빌드/보안/의존성 사전 검증 |
| 1 | **page-explorer** | 페이지 구조 탐색 및 page-map 생성 |
| 2 (병렬 11개) | **functional-tester** | 기능/인터랙션 테스트 |
| | **visual-inspector** | UI/접근성/반응형 |
| | **api-interceptor** | 네트워크/API 분석 |
| | **perf-auditor** | Core Web Vitals |
| | **social-share-auditor** | OG/PWA/카카오 공유 |
| | **db-validator** | DB CRUD 검증 |
| | **touch-interaction-validator** | 터치/스와이프 |
| | **image-optimizer** | 이미지 최적화 |
| | **security-auditor** | 보안 헤더/쿠키 |
| | **seo-auditor** | SEO 메타/sitemap |
| | **error-resilience** | 404/콘솔에러/깨진링크 |
| 3 | **test-lead** | 결과 취합 및 REPORT.md 생성 |

## 출력

`tests/results/REPORT.md` — 종합 테스트 리포트
