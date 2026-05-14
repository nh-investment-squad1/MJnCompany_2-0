# CS Plugins 상황별 메뉴얼

복붙해서 바로 사용하세요.

---

## 워크플로우 한눈에 보기

```
[요청이 모호] → /cs-clarify → [요청이 명확] → /CS-plan → [구현] → /cs-ship → PR
[코드 리뷰]  → /CS-codebase-review
[디자인 리뷰] → /cs-design
[웹 테스트]  → /CS-test
```

---

## 상황 1 — 새 기능을 만들어야 한다 (요청이 명확한 경우)

```
/CS-plan "로그인 기능 추가 — JWT 토큰, 이메일+비밀번호"
```

완료 후 구현 → PR 전:
```
/cs-ship
```

---

## 상황 2 — 요청이 모호하거나 범위가 클 때

```
/cs-clarify "사용자 관리 시스템 만들기"
```

결과로 `CLARIFY.md` 생성됨 → 그 다음:
```
/CS-plan "사용자 관리 시스템 — CLARIFY.md 참고"
```

---

## 상황 3 — 구현 완료, PR 만들기 전 최종 점검

```
/cs-ship
```

자동으로:
- PLAN.md vs 실제 구현 비교
- 테스트 커버리지 확인
- 커밋 메시지 자동 생성

결과: `SHIP-REPORT.md` + 판정 (PASS / BLOCKED / WARNINGS)

---

## 상황 4 — 코드 품질이 걱정될 때

```
/CS-codebase-review
```

특정 파일/폴더만:
```
/CS-codebase-review src/auth
```

특정 관점만:
```
/CS-codebase-review --focus security
/CS-codebase-review --focus architecture
/CS-codebase-review --focus performance
```

---

## 상황 5 — UI가 이상한 것 같을 때

```
/cs-design
```

빠른 확인 (수정된 파일만):
```
/cs-design --quick
```

문제 자동 수정까지:
```
/cs-design --fix
```

---

## 상황 6 — 웹사이트/앱 전체 테스트

```
/CS-test https://your-site.com
```

---

## 상황 7 — 작업 중 개선 아이디어가 떠올랐을 때

나중에 잊어버리기 전에 바로 캡처:
```
/cs-experiencing btw "로그인 실패 시 에러 메시지가 너무 모호함"
```

---

## 상황 8 — 잠깐 자리 비워야 할 때 (진행 상황 저장)

```
/cs-experiencing checkpoint
```

---

## 상황 9 — 현재 버전 상태 확인

```
/cs-experiencing status
```

---

## 상황 10 — 학습 내용 버전업 (오늘 배운 것 저장)

도메인별:
```
/cs-experiencing version-up test
/cs-experiencing version-up plan
/cs-experiencing version-up review
/cs-experiencing version-up design
```

한 번에 전부:
```
/cs-experiencing version-up all
```

---

## 도메인별 포커스 옵션 모아보기

### /CS-codebase-review --focus
| 옵션 | 내용 |
|------|------|
| `architecture` | 구조, 레이어, 의존성 |
| `quality` | 코드 품질, 중복, 복잡도 |
| `security` | 보안 취약점, OWASP |
| `performance` | 성능 병목 |
| `maintainability` | 유지보수성, 가독성 |

### /cs-design --focus
| 옵션 | 내용 |
|------|------|
| `visual` | 시각적 계층, 타이포그래피 |
| `interaction` | 인터랙션 품질 |
| `consistency` | 디자인 시스템 일관성 |
| `responsive` | 반응형, 접근성 |
| `antipatterns` | 안티패턴 탐지 |

---

## 전체 사이클 (한 기능을 처음부터 끝까지)

```bash
# 1. 요청 명료화 (모호한 경우)
/cs-clarify "기능 설명"

# 2. 코딩 플랜 생성
/CS-plan "기능 설명"

# 3. 구현 (Claude가 PLAN.md 따라 구현)

# 4. PR 전 최종 검증
/cs-ship

# 5. PASS이면 커밋 + PR 생성
# commit 메시지는 cs-ship이 자동 제안
```

---

## Pull Request란?

내 브랜치의 코드를 메인 브랜치에 **병합해달라는 요청**.  
팀원들이 리뷰 → 승인 → 병합 순서로 진행됩니다.

```
내 브랜치 (feature/login)
    ↓ /cs-ship 통과
    ↓ git commit -m "feat(auth): add JWT login"
    ↓ git push
    ↓ gh pr create
메인 브랜치 (main) ← 팀원 리뷰 후 merge
```
