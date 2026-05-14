---
description: "CS 세션 종료 자동화 - 4-Agent 병렬 분석 → 학습 저장 → 플러그인 버전업 → GitHub push → context compact 제안 (/mj-end)"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, Agent, AskUserQuestion
---

# /mj-end — CS Session Closing

세션을 안전하게 종료하면서 학습을 영속화하고 변경된 플러그인을 자동으로 버전업·푸시합니다.

## ⚠️ Author-Only Command

`/mj-end` is designed for the **plugin author** (`nh-investment-squad1`). It commits and pushes changes back to the marketplace repository.

If you are not the author, Phase 4 (git push) is automatically skipped — your local learnings are still saved.

## 실행 순서

0. **Phase 0 — 플래그 파싱 + Origin 확인** (자동)
   ```bash
   PREPASS_RUNNER="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0/shared/run_prepass.sh"
   PREFLIGHT=$(bash "$PREPASS_RUNNER" end-preflight "$@" 2>/dev/null)
   _f() { printf '%s' "$PREFLIGHT" | python3 -c "import sys,json;print(json.load(sys.stdin)$1)" 2>/dev/null; }

   EXPLICIT_PROJECT=$(_f "['flags']['explicit_project']")
   AUTO_NO_PUSH=$(_f "['flags']['auto_no_push']")
   PROJECT_DIR=$(_f "['paths']['project']")
   PROJECT_NAME=$(_f "['paths']['project_name']")
   MARKETPLACE_DIR=$(_f "['paths']['marketplace']")
   ```
   `origin`이 `nh-investment-squad1`가 아니면 `AUTO_NO_PUSH=true`로 자동 설정됩니다 (Python이 판정).

1. **Phase 1 — 4-Agent 병렬 분석**
   - `doc-updater` — 문서 업데이트 필요 항목 추출
   - `learning-extractor` — TIL/패턴/결정 사항 추출
   - `version-scout` — 변경된 플러그인 자동 탐지
   - `followup-suggester` — 다음 세션 follow-up 제안
2. **Phase 2 — 학습 영속화** (mj-experiencing 노하우 섹션 + CHANGELOG 갱신)
3. **Phase 3 — 변경 플러그인 버전업** (VERSION 파일 + plugin.json bump)
4. **Phase 4 — Git commit + push** (atomic commit, marketplace.json 동기화)
5. **Phase 5 — Push 완료 리포트** (두 레포 상태 명확 구분 출력)
6. **Phase 6 — 세션 컨텍스트 압축** (기본 활성화, `--no-compact`로 생략 가능)

## 실행 방식

```bash
VERSIONS=$(bash "$PREPASS_RUNNER" plugin-versions 2>/dev/null)
_v() { printf '%s' "$VERSIONS" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
LATEST_EXP=$(_v "mj-experiencing")
SKILL="$LATEST_EXP/skills/experiencing/SKILL.md"
```

`$SKILL`의 프로토콜에 따라 4-Agent를 단일 메시지에 병렬 스폰하여 실행합니다.

## Phase 5 — Push 완료 리포트

모든 phase가 끝난 뒤 두 레포의 push 상태를 **반드시 구분하여** 출력합니다.

### 탐지 로직

```bash
# Phase 0 PREFLIGHT에서 이미 확보된 값 사용
MARKETPLACE_DIR="$HOME/.claude/plugins/marketplaces/MJnCompany_2-0"
MARKETPLACE_NAME="MJnCompany_2-0"
# PROJECT_DIR, PROJECT_NAME은 Phase 0 PREFLIGHT에서 설정됨

# push 완료 후 최신 git 상태 조회 (Python — Phase 4 이후 호출)
check_push_status() {
  bash "$PREPASS_RUNNER" git-status "$1" 2>/dev/null
  # Returns JSON: {"state":"pushed","ahead":"0","behind":"0","branch":"main","remote":"owner/repo"}
}
_ps() { printf '%s' "$1" | python3 -c "import sys,json;print(json.load(sys.stdin).get('$2',''))" 2>/dev/null; }
```

### 출력 포맷

Phase 4 완료 직후, 다음 형식으로 출력합니다:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Push 완료 리포트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 [마켓플레이스]  MJnCompany_2-0
   ✅ PUSHED     branch: main → nh-investment-squad1/MJnCompany_2-0
   (또는)
   ⏭️  SKIPPED   --no-push 모드 / author 아님

 [프로젝트]      <project-name>
   ✅ PUSHED     branch: main → <owner>/<repo>
   (또는)
   ⚠️  UNPUSHED  <N>개 커밋이 아직 remote에 없음
                 → git -C <path> push origin <branch>
   (또는)
   ─  해당없음   세션 중 별도 프로젝트 레포 없음

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 판정 기준

| 상태 | 조건 |
|------|------|
| `✅ PUSHED` | `ahead == 0` (local이 remote와 동일하거나 push 직후) |
| `⚠️ UNPUSHED` | `ahead > 0` (local에 push 안 된 커밋 존재) |
| `⏭️ SKIPPED` | `--no-push` 플래그 또는 `AUTO_NO_PUSH=true` |
| `─ 해당없음` | 프로젝트 레포 탐지 불가 또는 마켓플레이스와 동일 |

## Phase 6 — 세션 컨텍스트 압축

Phase 5 완료 후, Phase 1의 `learning-extractor`·`followup-suggester` 결과를 바탕으로
현재 세션의 핵심을 1-2줄로 압축하여 `/compact` 인자로 제공합니다.

### 생성 내용

- 이번 세션에서 한 것 (작업 요약)
- 핵심 결정/학습 (3줄 이내)
- 다음 세션 시작 시 알아야 할 것

### 출력 포맷

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 세션 종결 완료 — 아래 명령으로 context를 정리하세요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/compact [생성된 세션 요약 1-2줄]

 또는 완전 초기화: /clear
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

`--no-compact` 플래그가 있거나 `--learning-only` 모드이면 이 Phase를 스킵합니다.

## 사용 예

```
/mj-end                                        # 표준 종료 (분석 → 버전업 → push → compact 제안)
/mj-end --project /path/to/repo               # 프로젝트 레포 명시 (Phase 5 push 상태 포함)
/mj-end --no-push                             # push 생략 (로컬만)
/mj-end --no-compact                          # Phase 6 생략 (compact 제안 없이 종료)
/mj-end --learning-only                       # 학습 추출/저장만 (버전업/push/compact 생략)
/mj-end --project ~/Documents/GitHub/myproduct_v4/easyconversion_web1  # easyconversion_web1 포함
```
