---
name: cs-design-sample1
user-invocable: true
description: |
  Crextio-inspired 디자인 가이드 스킬 (warm cream #F5F3EE + amber/slate 액센트).
  ICE 스코어링 페이지와 문제정의 관리 페이지에 적용된 디자인 시스템을 공식화한 레퍼런스.

  Use when user types:
  - "/cs-design-sample1"
  - "디자인 가이드 보여줘"
  - "크렉시오 스타일 적용"
  - "--audit [file]" to check a file
  - "--apply [file]" to apply the design
version: 1.0.0
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - Write
---

# cs-design-sample1 — Crextio-Inspired Design Guide

이 세션에서 확립된 디자인 언어를 캡처한 재사용 가능한 레퍼런스 스킬.

**참조 파일**: `knowledge/design-guide.md` (이 스킬과 같은 플러그인 내)

---

## Usage

```bash
/cs-design-sample1                        # 디자인 가이드 전체 출력
/cs-design-sample1 --audit [file]         # 파일이 가이드를 따르는지 검사
/cs-design-sample1 --apply [file]         # 파일에 디자인 가이드 적용
```

---

## Protocol

### Mode 1: 가이드 출력 (args 없음)

1. `knowledge/design-guide.md`를 Read
2. 전체 디자인 가이드를 사용자에게 출력
3. 주요 섹션: 색상 시스템, 컴포넌트 패턴, 타이포그래피, 간격, 안티패턴

### Mode 2: `--audit [file]`

**목적**: 지정된 파일이 이 디자인 가이드를 따르는지 검사하고 위반 사항 리포트

**실행 절차**:

1. `knowledge/design-guide.md`를 Read (가이드 로드)
2. 지정된 `[file]`을 Read
3. 다음 항목을 체크:

   **배경/레이아웃 체크**
   - [ ] `bg-[#F5F3EE]` 또는 `bg-[#f5f3ee]` 페이지 배경 사용 여부
   - [ ] `rounded-2xl` (not `rounded-xl`) 카드 사용 여부
   - [ ] `shadow-sm` or `shadow-md` (not `border border-gray-200`) 카드 스타일 여부
   - [ ] `space-y-5` 페이지 간격 여부

   **색상 체크**
   - [ ] Primary 버튼이 `bg-slate-900` (not `bg-blue-600`) 여부
   - [ ] 필터 "전체" 버튼이 `bg-slate-900` (not `bg-gray-800`) 여부
   - [ ] 테이블 헤더가 `bg-slate-900` (not `bg-gray-50`) 여부
   - [ ] 액센트 색이 amber-4xx 계열 여부 (not orange, not blue)
   - [ ] Secondary 버튼이 `bg-stone-100` (not `bg-gray-100`) 여부

   **안티패턴 체크**
   - [ ] `bg-gradient-to-br` 배경 사용 없는지
   - [ ] `border border-gray-200` 카드 테두리 없는지
   - [ ] `bg-blue-600` primary 버튼 없는지

4. 결과 리포트 출력:
   ```
   ✅ 통과: [항목 목록]
   ⚠️ 위반: [항목 + 위치 + 수정 제안]
   📊 준수율: X/Y 항목 (XX%)
   ```

### Mode 3: `--apply [file]`

**목적**: 지정된 파일에 이 디자인 가이드를 자동 적용

**실행 절차**:

1. `knowledge/design-guide.md`를 Read (가이드 로드)
2. 지정된 `[file]`을 Read
3. `--audit` 방식으로 위반 항목 파악
4. 위반 항목별 수정 계획 수립:
   - `bg-gradient-to-br from-slate-50...` → `bg-[#F5F3EE]`
   - `border border-gray-200` 카드 → `shadow-sm` 제거
   - `rounded-xl` → `rounded-2xl`
   - `bg-blue-600` primary button → `bg-slate-900`
   - `bg-gray-800` filter active → `bg-slate-900`
   - `bg-gray-50 border-b` table header → `bg-slate-900`
   - `bg-gray-100` secondary button → `bg-stone-100`
   - `space-y-6` page gap → `space-y-5`
5. 수정 사항을 Edit 도구로 적용 (각 변경마다 정확한 old/new string 사용)
6. 적용 완료 요약 출력:
   ```
   ✅ 적용 완료: X개 항목 수정
   📝 변경 내역: [목록]
   ```

---

## 디자인 언어 요약

| 요소 | 값 |
|------|-----|
| 배경 | `#F5F3EE` warm cream |
| Primary accent | `amber-400` (#FBBF24) |
| Dark accent | `slate-900` (#0F172A) |
| Neutral | `stone-*` |
| 카드 스타일 | `bg-white rounded-2xl shadow-sm` |
| 테이블 헤더 | `bg-slate-900 text-slate-400` |
| Primary 버튼 | `bg-slate-900 text-white` |
| KPI 카드 | white / slate-900 / amber-400 3종 |

---

## 참조 디자인

- Crextio HR Management Dashboard (Dribbble #25121521)
- 적용 프로젝트: dash1 (`app/ice/page.tsx`, `app/problems/page.tsx`)
