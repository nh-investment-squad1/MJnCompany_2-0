---
name: mj-experiencing
user-invocable: true
description: |
  경험 지식 저장소 오케스트레이터.
  도메인별 누적 학습 조회, 실행, 버전 관리.
  Use when invoked via /mj-experiencing, or when user says "경험", "학습 실행", "버전업".
version: 4.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
  - AskUserQuestion
---

# Experiencing - 경험 지식 저장소

## 도메인 위치

4개 도메인은 mj-experiencing-v4과 같은 레벨의 plugins/ 디렉토리에 위치합니다:

```
plugins/
├── mj-experiencing-v4/      ← 이 플러그인 (오케스트레이터, v4)
├── MJ-test-v13/             ← 14-agent 웹 테스트 도메인
├── MJ-plan-v11/             ← TDD+CleanArch 4-agent 플랜 도메인
├── MJ-codebase-review-v13/  ← 5-agent 코드 리뷰 도메인
└── mj-design-v8/            ← 5-agent 디자인 리뷰 도메인
```

마켓플레이스 절대 경로: `~/.claude/plugins/marketplaces/MJnCompany_2-0/plugins/`

## 사용법

```
/mj-experiencing                                          # 도메인 목록 + 버전 현황 표시
/mj-experiencing test [URL]                               # MJ-test 실행 (14-agent 웹 테스트)
/mj-experiencing plan [task]                              # MJ-plan 실행
/mj-experiencing review [path] [--focus aspect]           # MJ-codebase-review 실행 (5-관점 코드 리뷰)
/mj-experiencing design [path] [--focus aspect] [--fix]  # CS-design 실행 (5-관점 디자인 리뷰)
/mj-experiencing update                                   # 4개 스킬 모두 버전업 (version-up all 단축키)
/mj-experiencing version-up [domain]                      # 도메인 버전 증가 (test/plan/review/design)
/mj-experiencing version-up all                           # 4개 도메인 한번에 버전 증가
/mj-experiencing status                                   # 모든 도메인 VERSION 파일 읽기
/mj-experiencing btw [idea]                               # [v4 신규] 세션 중 개선 아이디어 즉시 캡처
/mj-experiencing checkpoint                               # [v4 신규] WIP 체크포인트 커밋 생성
/mj-experiencing pipeline [project]                       # 전체 파이프라인 실행 (review→design→test)
```

---

## 실행 프로토콜

### `/experiencing` (인수 없음)

도메인 목록과 현재 버전을 표시:

```bash
BASE="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/plugins"
for domain in MJ-test MJ-plan MJ-codebase-review; do
  VERSION=$(cat "$BASE/${domain}-v"*/VERSION 2>/dev/null || echo "?")
  echo "📦 $domain | 현재 콘텐츠 버전: $VERSION"
done
```

### `/mj-experiencing test [URL]`

1. 최신 MJ-test 도메인 경로 찾기:
   ```bash
   BASE="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/plugins"
   LATEST_TEST=$(ls -d "$BASE/MJ-test-v"* 2>/dev/null | sort -V | tail -1)
   ```
2. `$LATEST_TEST/VERSION` 읽기 → 현재 버전 확인
3. `$LATEST_TEST/skills/MJ-test/SKILL.md` 프로토콜 실행
4. URL을 대상으로 14-agent 팀 가동

### `/mj-experiencing plan [task]`

1. 최신 MJ-plan 도메인 경로 찾기:
   ```bash
   BASE="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/plugins"
   LATEST_PLAN=$(ls -d "$BASE/MJ-plan-v"* 2>/dev/null | sort -V | tail -1)
   ```
2. `$LATEST_PLAN/VERSION` 읽기 → 현재 버전 확인
3. `$LATEST_PLAN/skills/MJ-plan/SKILL.md` 프로토콜 실행

### `/mj-experiencing review [path] [--focus aspect]`

1. 최신 MJ-codebase-review 도메인 경로 찾기:
   ```bash
   BASE="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/plugins"
   LATEST_REVIEW=$(ls -d "$BASE/MJ-codebase-review-v"* 2>/dev/null | sort -V | tail -1)
   ```
2. `$LATEST_REVIEW/VERSION` 읽기 → 현재 버전 확인
3. `$LATEST_REVIEW/skills/MJ-codebase-review/SKILL.md` 프로토콜 실행
3. 인수 파싱:
   - `[path]` 없음 → 현재 작업 디렉토리 전체 분석
   - `[path]` 있음 → 해당 경로만 분석
   - `--focus [aspect]` 있음 → 해당 관점만 집중 분석 (architecture/quality/security/performance/maintainability)
4. 5개 에이전트(Architecture/Quality/Security/Performance/Maintainability)를 병렬 실행
5. 결과 종합 → 등급(A/B/C/D) + 우선순위별 권장 조치사항 리포트 출력

### `/mj-experiencing update`

`version-up all`의 단축 명령어. 3개 도메인(MJ-test, MJ-plan, MJ-codebase-review)을 순차적으로 버전업합니다.

아래 `version-up all` 프로토콜과 동일하게 실행.

---

### `/mj-experiencing design [path] [--focus aspect] [--fix]`

1. 최신 CS-design 도메인 경로 찾기:
   ```bash
   BASE="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/plugins"
   LATEST_DESIGN=$(ls -d "$BASE/mj-design-v"* 2>/dev/null | sort -V | tail -1)
   ```
2. `$LATEST_DESIGN/VERSION` 읽기 → 현재 버전 확인
3. `$LATEST_DESIGN/skills/mj-design/SKILL.md` 프로토콜 실행
4. 인수 파싱:
   - `[path]` 없음 → 현재 작업 디렉토리
   - `--focus [aspect]` 있음 → 해당 관점만 집중 분석 (visual/interaction/consistency/responsive/antipatterns)
   - `--fix` 있음 → 발견된 안티패턴 자동 수정 활성화
5. design-lead 에이전트를 스폰하여 5개 에이전트(visual-hierarchy/interaction-quality/design-system-consistency/responsive-accessibility/anti-pattern-detector) 병렬 실행
6. 결과 종합 → 관점별 점수(0-10) + 등급(A~F) + 우선순위별 수정사항 DESIGN-REVIEW.md 출력

---

### `/mj-experiencing version-up [domain|all]`

**정책: 직전 버전 + 현재 버전 2개만 유지. 더 오래된 버전은 자동 삭제.**

**`all` 키워드**: `test` → `plan` → `review` → `design` 4개 도메인 순차 처리.

**각 도메인마다 아래 순서로 실행:**

---

#### STEP 1: 학습 캡처 (AI 자동 추출 우선)

**AI가 먼저 세션 컨텍스트를 분석해서 핵심 노하우를 추출한다. 발견 시 제안 → 사용자 확인. 없으면 직접 질문.**

**1-A. AI 자동 분석**

현재 세션 대화에서 해당 도메인과 관련된 다음 항목을 탐색:
- 예상과 달랐던 동작 (버그, 엣지케이스, 특이 동작)
- 문제 해결 과정에서 발견한 패턴 또는 원인
- 반복 적용 가능한 팁, 설정, 명령어
- 공식 문서/가정과 실제 동작의 차이

**1-B. 발견사항이 있으면 → 제안 후 확인 (AskUserQuestion 1회)**

```
💡 CS-[DOMAIN] — AI가 분석한 이번 세션 핵심 학습:

"[AI가 추출한 학습 제목]: [구체적 발견 내용 1-2줄]"

이대로 저장할까요?
```
옵션:
- "저장" → 그대로 SKILL.md에 추가
- "직접 수정" → Other 선택 후 수정 내용 입력
- "스킵" → 학습 없이 버전만 증가

**1-C. 발견사항이 없으면 → 자동 스킵 (질문 없음)**

AskUserQuestion 호출하지 않음. 그냥 "📝 학습 스킵 (이번 세션 발견사항 없음)" 출력 후 STEP 3으로 진행.

#### STEP 2: 학습 내용 SKILL.md에 추가 (입력이 있을 경우)

1. 최신 도메인 디렉토리의 SKILL.md 읽기
2. 마지막 노하우 번호 파악 (예: `### 15.` → 다음은 `### 16.`)
3. 오늘 날짜 확인: `date +%Y-%m-%d`
4. Edit 도구로 SKILL.md 노하우 섹션 끝에 추가:

```markdown
### [N]. [학습 제목] ([YYYY-MM-DD])

- **상황**: [어떤 작업 중에 발견했는지]
- **발견**: [구체적으로 무엇을 배웠는지]
- **교훈**: [다음에 어떻게 적용할지]
```

#### STEP 3: 버전 디렉토리 생성

```bash
BASE_PATH="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/plugins"
ALL_DIRS=($(ls -d "$BASE_PATH/CS-${DOMAIN}-v"* 2>/dev/null | sort -V))
LATEST_DIR="${ALL_DIRS[-1]}"
CURRENT_VERSION=$(cat "$LATEST_DIR/VERSION" 2>/dev/null || echo "1")
NEXT_VERSION=$((CURRENT_VERSION + 1))
NEW_DIR="$BASE_PATH/CS-${DOMAIN}-v${NEXT_VERSION}"

cp -r "$LATEST_DIR" "$NEW_DIR"
echo "$NEXT_VERSION" > "$NEW_DIR/VERSION"
```

#### STEP 4: marketplace.json 업데이트

파일: `~/.claude/plugins/marketplaces/MJnCompany_2-0/.claude-plugin/marketplace.json`

Edit 도구로:
- `"./plugins/CS-[DOMAIN]-v[CURRENT]"` → `"./plugins/CS-[DOMAIN]-v[NEXT]"`

#### STEP 5: 오래된 버전 정리

```bash
TOTAL=${#ALL_DIRS[@]}
DELETE_COUNT=$((TOTAL - 1))
if [ $DELETE_COUNT -gt 0 ]; then
  for dir in "${ALL_DIRS[@]:0:$DELETE_COUNT}"; do
    echo "🗑️ 삭제: $(basename $dir)"
    rm -rf "$dir"
  done
fi
```

#### STEP 6: 완료 안내

```
✅ CS-[DOMAIN] 버전업 완료
📦 현재 버전: CS-[DOMAIN]-v[NEXT] (VERSION=[NEXT])
📦 보관 버전: CS-[DOMAIN]-v[CURRENT] (직전)
🗑️ 삭제됨: [삭제된 버전들]
📝 학습 추가: "[제목]" (노하우 #[N])   ← 입력 있을 경우
📝 학습 스킵                           ← 입력 없을 경우
```

---

**`version-up all` 실행 순서**: `test → plan → review → design → ceo` (5개 순차)

**`version-up ceo` 프로토콜** (6-step):

CEO 버전업은 다른 4개 도메인과 동일한 구조이나 학습 캡처 내용이 다르다.

**STEP 1: 학습 분석 (CEO 특화)**

이번 세션에서 CEO가 내린 배분 결정을 회고한다:
- smart-run을 선택한/안 한 결정이 올바랐는가?
- 어떤 요청 패턴에서 공수 추정이 틀렸는가?
- 새로 발견한 효과적인 도메인 조합은?
- 어떤 상황에서 모드 C(smart-run)가 효과적이었는가?

발견사항이 있으면 AskUserQuestion으로 1회 확인. 없으면 자동 스킵.

**STEP 2: 학습 추가** (입력 있을 경우)

**⚠️ 두 파일 동시 업데이트 필수** — 에이전트(ceo.md)와 스킬(SKILL.md)이 항상 동기화되어야 한다.

1. `$LATEST_CEO/agents/ceo.md`의 `## CEO 노하우` 섹션 끝에 추가
2. `$LATEST_CEO/skills/mj-ceo/SKILL.md`의 `## CEO 노하우` 섹션 끝에 추가

두 파일 모두 동일한 내용을 추가한다:

```markdown
### [N]. [학습 제목] ([YYYY-MM-DD])
- **상황**: [어떤 요청이었는가]
- **판단**: [CEO가 내린 결정]
- **결과**: [효과적이었는가]
- **교훈**: [다음에 유사 상황에서 어떻게 판단할 것인가]
```

**STEP 3: 버전 디렉토리 생성**

```bash
BASE_PATH="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/plugins"
ALL_DIRS=($(ls -d "$BASE_PATH/mj-ceo-v"* 2>/dev/null | sort -V))
LATEST_DIR="${ALL_DIRS[-1]}"
CURRENT_VERSION=$(cat "$LATEST_DIR/VERSION" 2>/dev/null || echo "1")
NEXT_VERSION=$((CURRENT_VERSION + 1))
NEW_DIR="$BASE_PATH/mj-ceo-v${NEXT_VERSION}"

cp -r "$LATEST_DIR" "$NEW_DIR"
echo "$NEXT_VERSION" > "$NEW_DIR/VERSION"
```

**STEP 4: marketplace.json 업데이트**

Edit 도구로: `"./plugins/mj-ceo-v[CURRENT]"` → `"./plugins/mj-ceo-v[NEXT]"`

**STEP 5: 오래된 버전 정리** (2개 유지)

```bash
TOTAL=${#ALL_DIRS[@]}
DELETE_COUNT=$((TOTAL - 1))
if [ $DELETE_COUNT -gt 0 ]; then
  for dir in "${ALL_DIRS[@]:0:$DELETE_COUNT}"; do
    rm -rf "$dir"
  done
fi
```

**STEP 6: 완료 안내**

```
✅ mj-ceo 버전업 완료
📦 현재 버전: mj-ceo-v[NEXT] (VERSION=[NEXT])
📦 보관 버전: mj-ceo-v[CURRENT] (직전)
📝 학습 추가: "[제목]" (노하우 #[N])  또는  📝 학습 스킵
```

---

**`all` 완료 후 종합 안내:**
```
✅ 전체 버전업 완료
📦 MJ-test: v[N] → v[N+1]  (학습 추가/스킵)
📦 MJ-plan: v[N] → v[N+1]  (학습 추가/스킵)
📦 MJ-codebase-review: v[N] → v[N+1]  (학습 추가/스킵)
📦 mj-design: v[N] → v[N+1]  (학습 추가/스킵)
📦 mj-ceo: v[N] → v[N+1]  (학습 추가/스킵)
```

### `/mj-experiencing pipeline [project]`

전체 파이프라인을 순서대로 실행합니다. experiencing-lead 에이전트가 오케스트레이션을 담당합니다.

1. **Preflight** (preflight-checker 에이전트 호출): 성공 기준 정의 + 범위 확인
2. **Checkpoint**: 파이프라인 시퀀스 확인 (AskUserQuestion)
3. **실행 순서**: `review → design → test` (순차, 각 단계 후 체크포인트)
4. **Evaluator-Optimizer**: 각 단계 등급 < B이면 "수정 후 재실행" 제안
5. **최종 요약**: 3개 도메인 결과 + 우선순위 액션 3개

```
경험 lead 에이전트 스폰:
BASE="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/plugins"
LEAD_DIR=$(ls -d "$BASE/mj-experiencing-v"* 2>/dev/null | sort -V | tail -1)
```

에이전트 파일: `$LEAD_DIR/agents/experiencing-lead.md`

---

### `/mj-experiencing btw [idea]` ← v4 신규 (bkit btw 패턴)

세션 중 발견한 개선 아이디어를 즉시 캡처합니다.

```bash
BTW_FILE="$(dirname $(ls -d "$HOME/.claude/plugins/marketplaces/MJnCompany_2-0" 2>/dev/null || echo "/tmp"))/.experiencing-btw.json"
# {id, idea, date, status: "pending"} 형태로 JSON 배열에 추가
```

저장 후: `💡 BTW #[N] 캡처됨: "[아이디어]"` 출력. version-up 시 pending 항목 자동 제안.

---

### `/mj-experiencing checkpoint` ← v4 신규 (gstack 패턴)

현재 작업 상태를 WIP 커밋으로 보존합니다.

```bash
DATE=$(date +%Y-%m-%d-%H%M)
git -C "$HOME/.claude/plugins/marketplaces/MJnCompany_2-0" add -A
git -C "$HOME/.claude/plugins/marketplaces/MJnCompany_2-0" commit -m "wip: mj-experiencing checkpoint $DATE"
```

완료 후: `✅ 체크포인트 저장됨 (${DATE})` 출력.

---

### `/mj-experiencing status`

모든 도메인의 VERSION 파일 표시:

```bash
BASE="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/plugins"
for PATTERN in "MJ-test-v" "MJ-plan-v" "MJ-codebase-review-v" "mj-design-v"; do
  LATEST=$(ls -d "$BASE/${PATTERN}"* 2>/dev/null | sort -V | tail -1)
  if [ -n "$LATEST" ]; then
    VER=$(cat "$LATEST/VERSION" 2>/dev/null || echo "?")
    DOMAIN=$(basename "$LATEST")
    echo "📋 $DOMAIN: v$VER"
  fi
done
```

---

## 버전 철학

- **도메인 디렉토리명** (`MJ-test-v2`): 스키마/구조 버전 — 큰 구조 변경 시에만 변경
- **VERSION 파일**: 콘텐츠 버전 — 새 학습이 추가될 때마다 증가
- **plugin.json version**: 전체 플러그인 버전 — semver (major.minor.patch)

---

## experiencing 노하우

### 1. version-up은 학습 캡처 + 디렉토리 복사 두 단계여야 한다 (2026-04-11)

- **상황**: 초기 version-up이 디렉토리 복사 + VERSION 번호 증가만 수행
- **발견**: 단순 cp는 파일 내용이 동일하므로 "경험 저장소"가 아니라 "버전 스냅샷"에 불과함. 새 VERSION 디렉토리에 이번 세션에서 배운 내용이 없으면 버전 증가의 의미가 없다.
- **교훈**: version-up 실행 시 반드시 AskUserQuestion으로 학습 내용을 받아 SKILL.md 노하우 섹션에 추가한 뒤 cp 실행. 학습 없이 버전만 올리는 것은 의미 없음.

### 2. `all` 키워드로 3개 도메인 한번에 버전업 (2026-04-11)

- **상황**: 도메인별로 version-up을 3번 따로 실행해야 했음
- **발견**: `test` → `plan` → `review` 순서로 순차 처리하면 한 번의 명령으로 모두 처리 가능
- **교훈**: `/mj-experiencing version-up all` 지원으로 워크플로우 간소화. 각 도메인마다 학습 캡처 인터랙션이 뜨므로 3번의 입력 기회가 생김.

### 3. AI 자동 학습 추출 — 수동 입력보다 먼저 시도 (2026-04-14)

- **상황**: version-up 시 항상 수동으로 학습 내용을 입력해야 했음. 세션이 길면 무엇을 배웠는지 직접 요약하기 번거로움.
- **발견**: AI가 세션 컨텍스트를 먼저 분석하면 핵심 발견사항(버그 원인, 해결 패턴, 예상 외 동작 등)을 자동 추출 가능. 사용자는 제안을 확인만 하면 됨.
- **교훈**: STEP 1을 "AI 분석 → 제안 → 확인" 순서로 바꾸면 마찰 최소화. 발견사항이 없을 때만 기존 수동 입력 fallback.

### 4. 외부 소스 학습 통합 — bkit·Karpathy·gstack 패턴 (2026-04-20)

- **상황**: bkit-claude-code, Karpathy-skills, gstack 3개 외부 레포 분석 후 mj-experiencing 및 4개 도메인에 적용 가능한 패턴을 발견함
- **발견**: bkit → Evaluator-Optimizer 루프(등급 미달 자동 재실행), Checkpoint 패턴(단계 간 사용자 확인 게이트). Karpathy → Think-Before-Coding(모호성 선제 해소), Goal-Driven Execution(성공 기준 명시). gstack → 선형 파이프라인(review→design→test), CSS/JSX 리스크 버짓 분리, 크로스 모델 듀얼 리뷰.
- **교훈**: 외부 패턴 학습은 각 도메인 SKILL.md 노하우에 직접 추가. 오케스트레이터(experiencing)에는 파이프라인 커맨드 + experiencing-lead/preflight-checker 신규 에이전트로 반영. 학습 후 즉시 version-up 실행.

### 5. bkit btw 패턴 — 세션 중 아이디어 즉시 캡처 (2026-04-20)

- **상황**: version-up 시 "이번 세션에서 뭘 개선해야 할지" 기억이 흐릿함. 작업 중 발견한 개선점이 세션 끝에 사라짐.
- **발견**: bkit의 btw(By-The-Way) 패턴: 작업 중 즉시 캡처 → JSON 파일에 pending 상태로 저장 → version-up 시 pending 항목을 먼저 보여주고 반영 여부 결정.
- **교훈**: `/mj-experiencing btw [idea]` 명령 추가. 세션 중 발견사항을 즉시 캡처하면 version-up의 AI 분석 단계를 보완할 수 있음.

### 6. gstack Iron Law — version-up 루프 실패 상한 (2026-04-20)

- **상황**: version-up all 실행 중 특정 도메인에서 오류가 생기면 전체가 중단되거나 무한 재시도 가능성 있음.
- **발견**: gstack Iron Law: "동일 문제에 3회 실패 시 강제 중단 + STUCK 리포트." version-up에도 동일 원칙 적용 — 도메인 처리 실패 2회 시 해당 도메인 스킵 + 경고 출력 후 다음 도메인으로.
- **교훈**: `version-up all` 프로토콜에 도메인별 retry 상한(2회) 추가. 실패 도메인은 스킵하고 `⚠️ [DOMAIN] 스킵됨 — 수동 확인 필요` 출력 후 계속 진행.

### 7. osascript 디버깅 — 레이어 격리로 root cause 빠르게 찾기 (2026-04-25)

- **상황**: `GET /api/pick-folder`가 즉시 `{"error":"cancelled"}` 반환 — 브라우저에서 폴더 선택 다이얼로그가 열리지 않음.
- **발견**: 문제 레이어를 3단계로 격리해서 빠르게 원인 특정: ① `curl` → API 응답 ② `osascript -e '...'` 직접 실행 → OS/스크립트 문법 ③ `bun -e "Bun.spawn..."` → 런타임. 직접 실행이 성공하면 서버 코드(문법 오류 또는 stale 프로세스) 안에 원인이 있음. 실제 원인: `choose folder with prompt "..." invisibles shown true` — `invisibles shown true`는 `choose folder`에 없는 파라미터로 error -2741 발생 → `on error` → 빈 반환. 추가 원인: `bun --watch`가 Claude Code Edit 도구의 파일 변경을 감지 못해 old 코드가 계속 실행됨.
- **교훈**: ① `choose folder`에 `invisibles shown true` 사용 금지 — 올바른 문법: `choose folder with prompt "..."` 만. ② API 서버 코드 수정 후 curl 테스트 전 반드시 프로세스 재시작 확인 — `bun --watch` 미감지 가능. ③ osascript는 temp 파일(`Bun.write + osascript path`) 방식이 stdin Blob보다 안정적.

### 9. ClipboardItem text/html+text/plain 이중 포맷으로 Slack 하이퍼링크 복사 (2026-04-28)

- **상황**: "Slack 공유용 복사" 버튼 구현 시 URL이 그대로 노출되지 않고 "백로그 바로가기" 같은 라벨 텍스트가 클릭 가능한 링크로 표시되길 원했음.
- **발견**: Slack mrkdwn `<url|label>` 포맷은 Slack Web API 전송 전용 — 클립보드 붙여넣기에서는 리터럴 문자열로 표시됨. 정답은 `navigator.clipboard.write()`에 `ClipboardItem({ "text/html": Blob([html]), "text/plain": Blob([plain]) })`를 동시에 담는 것. Slack 리치텍스트 에디터는 `text/html`을 우선 소비하여 `<a href="url">label</a>`를 클릭 가능한 하이퍼링크로 렌더링. HTML 미지원 앱은 `text/plain` fallback 사용.
- **교훈**: Slack 공유용 클립보드 복사는 mrkdwn이 아닌 HTML ClipboardItem을 기본으로 설계. `try/catch`로 감싸고 실패 시 `writeText()` fallback 필수 (Firefox 등 미지원 브라우저 대응). `navigator.clipboard.write()`는 HTTPS 또는 localhost + 사용자 제스처(클릭) 핸들러 내에서만 동작.

### 10. `/compact`는 스킬에서 직접 호출 불가 — 생성된 요약을 제안하는 패턴으로 우회 (2026-05-01)

- **상황**: mj-end가 세션 종결 자동화를 담당하지만 `/compact`(context 압축)는 별도로 실행해야 했음. 사용자가 "원커맨드 종결"을 원했으나 mj-end가 compact를 수행하지 않았음.
- **발견**: `/compact`는 Claude Code 내장 명령으로, 스킬/커맨드에서 프로그래밍적으로 호출이 불가능함. allowed-tools에도 invoke-command 같은 도구가 없음.
- **교훈**: 자동 호출이 불가능한 명령이 필요한 경우, 해당 명령의 인자를 AI가 생성하여 사용자가 복사-실행할 수 있도록 제안하는 패턴이 최선. mj-end Phase 6: Phase 1 분석 결과로 세션 요약 1-2줄 생성 → `/compact [요약]` 형식으로 출력 → 사용자가 그대로 실행. `--no-compact` 플래그로 생략 가능.

### 8. Tauri webview에서 `window.open()` silent 실패 — 외부 URL은 항상 API.openInChrome (2026-04-26)

- **상황**: deployUrl/githubUrl 카드 버튼에 `window.open(url, '_blank')`를 사용했더니 Tauri 앱에서 아무 반응 없음. 에러도 없고 브라우저도 안 열림.
- **발견**: Tauri webview는 외부 URL 네비게이션을 sandbox로 차단. DOM API(`window.open`)는 silent 실패. Rust 커맨드 `open_in_chrome`을 통해야 동작. 실패가 조용해서 개발 중 발견이 어려움.
- **교훈**: Tauri 앱에서 외부 URL 여는 버튼은 무조건 `API.openInChrome(url).catch(()=>{})`. `window.open` 사용 금지. 새 UI 요소 추가 체크리스트: 기능 코드 → `data-help-key` → `guideContent.ts` 항목 — 세 가지를 같은 커밋에 포함.
