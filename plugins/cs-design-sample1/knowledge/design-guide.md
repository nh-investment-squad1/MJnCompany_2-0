# cs-design-sample1 Design Guide

Crextio HR Dashboard에서 영감을 받은 내부 대시보드 디자인 시스템.
Tailwind CSS + Next.js 기반 데이터 집약적 내부 도구(Internal Tool)에 최적화.

---

## 1. 색상 시스템 (Color System)

### 배경 (Background)
```css
/* globals.css body */
background: #F5F3EE;  /* warm cream */
```
```tsx
// Tailwind
<div className="bg-[#F5F3EE]">
```

### 주요 액센트 (Primary Accent) — Yellow/Amber
| 용도 | 클래스 |
|------|--------|
| 강조 배지, KPI 카드, FOCUS 뱃지 | `bg-amber-400` |
| 액센트 카드 위 텍스트 | `text-amber-900` |
| 필터 활성 상태 | `bg-amber-400 text-amber-900 border-amber-400` |
| 필터 아이템 idle | `bg-amber-50 border-amber-200 text-amber-700` |
| 폼 카드 좌측 보더 | `border-l-4 border-amber-400` |
| 진행 바 fill | `bg-amber-400` |
| 세그먼트 FOCUS 카드 테두리 | `border-amber-300 bg-amber-50/60 ring-1 ring-amber-200` |

### 보조 액센트 (Secondary Accent) — Dark Slate
| 용도 | 클래스 |
|------|--------|
| 테이블 헤더 배경 | `bg-slate-900` |
| KPI 다크 카드 배경 | `bg-slate-900` |
| Primary 버튼 | `bg-slate-900 hover:bg-slate-800` |
| 그룹 헤더 (KR, 섹션 타이틀) | `bg-slate-900 text-white` |
| 필터 "전체" 버튼 활성 | `bg-slate-900 text-white border-slate-900` |
| 2위 순위 뱃지 | `bg-slate-800 text-white` |
| 테이블 헤더 텍스트 | `text-slate-400` |
| 활성 스코어러 컬럼 헤더 | `text-amber-400` (슬레이트 배경 위) |

### 중립 (Neutral) — Stone palette
| 용도 | 클래스 |
|------|--------|
| 레이블, 서브텍스트 | `text-stone-400` |
| 섹션 구분선 | `bg-stone-100`, `border-stone-100` |
| 섹션 토글 배경 | `bg-stone-50 hover:bg-stone-100` |
| 스코어러 선택 트랙 | `bg-stone-100 rounded-full p-1` |
| Secondary 버튼 | `bg-stone-100 text-stone-600 hover:bg-stone-200` |
| 링크 버튼 | `bg-white shadow-sm border border-stone-200 text-stone-600` |
| 셀렉트 박스 보더 | `border-stone-200` |
| 3위 순위 뱃지 | `bg-stone-200 text-stone-600` |
| "노션필요" 등 비활성 뱃지 | `bg-stone-100 text-stone-400` |

### 기능성 색상 (유지)
| 용도 | 클래스 |
|------|--------|
| 에러 배너 | `bg-red-50 border border-red-200 text-red-700` |
| ICE 연동 뱃지 | `bg-green-100 text-green-600` |
| 하이라이트 행 | `bg-green-50 ring-2 ring-inset ring-green-300` |
| 스테이터스 배지 | 각 상태별 시맨틱 색상 유지 |

---

## 2. 컴포넌트 패턴 (Component Patterns)

### 페이지 레이아웃
```tsx
<div className="min-h-screen bg-[#F5F3EE] p-6">
  <div className="max-w-7xl mx-auto space-y-5">
    {/* header */}
    {/* KPI cards */}
    {/* content */}
  </div>
</div>
```

### 페이지 헤더
```tsx
<div className="flex items-start justify-between">
  <div>
    <h1 className="text-2xl font-bold text-slate-900 tracking-tight">페이지 제목</h1>
    <p className="text-sm text-stone-400 mt-0.5">부제목 설명</p>
  </div>
  <div className="flex items-center gap-2">
    {/* FontSizeControl */}
    <Link className="px-3 py-1.5 text-xs bg-white shadow-sm border border-stone-200 text-stone-600 rounded-lg hover:bg-stone-50 transition-colors">
      다른 탭 →
    </Link>
  </div>
</div>
```

### KPI 카드 4종 세트
```tsx
<div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
  {/* White card */}
  <div className="bg-white rounded-2xl shadow-sm p-4">
    <p className="text-xs text-stone-400 font-medium mb-1">라벨</p>
    <p className="text-3xl font-bold text-slate-900 tabular-nums">{value}</p>
    <p className="text-xs text-stone-400 mt-1">보조 설명</p>
  </div>

  {/* White card with progress bar */}
  <div className="bg-white rounded-2xl shadow-sm p-4">
    <p className="text-xs text-stone-400 font-medium mb-1">진행률</p>
    <p className="text-3xl font-bold text-slate-900 tabular-nums">{count}</p>
    <div className="mt-2 h-1.5 rounded-full bg-stone-100 overflow-hidden">
      <div className="h-full rounded-full bg-amber-400 transition-all" style={{ width: `${pct}%` }} />
    </div>
  </div>

  {/* Dark card */}
  <div className="bg-slate-900 rounded-2xl shadow-sm p-4">
    <p className="text-xs text-slate-400 font-medium mb-1">라벨</p>
    <p className="text-3xl font-bold text-white tabular-nums">{value}</p>
    <p className="text-xs text-slate-400 mt-1 truncate">부제</p>
  </div>

  {/* Amber accent card */}
  <div className="bg-amber-400 rounded-2xl shadow-sm p-4">
    <p className="text-xs text-amber-900/70 font-medium mb-1">라벨</p>
    <p className="text-3xl font-bold text-amber-900 tabular-nums">{value}</p>
    <p className="text-xs text-amber-900/70 mt-1">보조 설명</p>
  </div>
</div>
```

### 일반 카드
```tsx
<div className="bg-white rounded-2xl shadow-sm p-4">
  {/* 내용 */}
</div>
```

### 폼 카드 (amber 좌측 보더)
```tsx
<div className="bg-white rounded-2xl shadow-md p-4 space-y-3 border-l-4 border-amber-400">
  {/* 폼 필드 */}
</div>
```

### 데이터 테이블
```tsx
<div className="bg-white rounded-2xl shadow-md overflow-hidden">
  <div className="overflow-x-auto">
    <table className="w-full text-sm">
      <thead>
        <tr className="bg-slate-900">
          <th className="px-4 py-3.5 text-left text-xs font-semibold text-slate-400">컬럼</th>
          {/* 활성 스코어러 컬럼: text-amber-400 */}
        </tr>
      </thead>
      <tbody className="divide-y divide-stone-100">
        <tr className="hover:bg-stone-50/60 transition-colors">
          {/* 활성 컬럼 셀: bg-amber-50/50 */}
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

### 순위 뱃지
```tsx
{/* 1위 */}
<span className="inline-flex items-center justify-center w-7 h-7 rounded-lg bg-amber-400 text-amber-900 font-bold text-xs shadow-sm">1</span>
{/* 2위 */}
<span className="inline-flex items-center justify-center w-7 h-7 rounded-lg bg-slate-800 text-white font-bold text-xs">2</span>
{/* 3위 */}
<span className="inline-flex items-center justify-center w-7 h-7 rounded-lg bg-stone-200 text-stone-600 font-bold text-xs">3</span>
{/* 4위+ */}
<span className="text-stone-400 text-xs font-medium tabular-nums">{rank}</span>
```

### 최고 점수 셀 뱃지
```tsx
<span className="inline-block px-2.5 py-1 rounded-lg bg-amber-400 text-amber-900 font-bold text-sm tabular-nums shadow-sm">{score}</span>
```

### 버튼
```tsx
{/* Primary */}
<button className="px-4 py-2 text-sm bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors font-medium disabled:opacity-50">
  저장
</button>

{/* Secondary */}
<button className="px-4 py-2 text-sm bg-stone-100 text-stone-600 rounded-lg hover:bg-stone-200 transition-colors">
  취소
</button>

{/* Small primary */}
<button className="px-3 py-1.5 text-xs bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors font-medium">
  + 추가
</button>

{/* Link-style (탭 이동) */}
<Link className="px-3 py-1.5 text-xs bg-white shadow-sm border border-stone-200 text-stone-600 rounded-lg hover:bg-stone-50 transition-colors">
  다른 탭 →
</Link>
```

### 스코어러 선택 네비게이션 (Pill-nav)
```tsx
<div className="inline-flex gap-1 bg-stone-100 rounded-full p-1 flex-wrap">
  {items.map((s) => (
    <button
      key={s}
      onClick={() => setActive(s)}
      className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
        active === s ? "bg-white shadow-sm text-slate-900" : "text-stone-500 hover:text-slate-700"
      }`}
    >
      {s}
    </button>
  ))}
</div>
```

### 필터 (문제영역/세그먼트)
```tsx
{/* "전체" 버튼 */}
<button className={`text-xs px-3 py-1 rounded-full border transition-colors ${
  isAll ? "bg-slate-900 text-white border-slate-900" : "bg-white text-stone-500 border-stone-300 hover:border-stone-400"
}`}>
  전체
</button>

{/* 필터 아이템 */}
<button className={`text-xs px-3 py-1 rounded-full border transition-colors ${
  active ? "bg-amber-400 text-amber-900 border-amber-400 font-semibold" : "bg-amber-50 border-amber-200 text-amber-700 hover:border-amber-400"
}`}>
  {active && <span className="mr-1">✓</span>}{label}
</button>
```

### 그룹 헤더 (KR, 섹션 타이틀)
```tsx
<div className="bg-white rounded-2xl shadow-md overflow-hidden">
  <div className="bg-slate-900 px-5 py-3">
    <h3 className="text-sm font-bold text-white">그룹 제목</h3>
  </div>
  {/* 내용 */}
</div>
```

### 섹션 토글 (접기/펼치기)
```tsx
<button className="w-full flex items-center gap-2 px-5 py-2.5 bg-stone-50 hover:bg-stone-100 transition-colors text-left">
  <span className="text-xs text-stone-400">{collapsed ? "▶" : "▼"}</span>
  <span className="text-xs font-semibold text-stone-600">섹션 이름</span>
  <span className="text-xs text-stone-400 ml-2">({count}개)</span>
</button>
```

### FOCUS 뱃지 (집중 세그먼트 표시)
```tsx
<span className="text-[9px] bg-amber-400 text-amber-900 px-1.5 py-0.5 rounded-full font-bold">FOCUS</span>
```

### 진행 바 (집중도, 달성률)
```tsx
<div className="w-full h-1.5 bg-stone-200 rounded-full overflow-hidden">
  <div className="h-full rounded-full bg-amber-400" style={{ width: `${pct}%` }} />
</div>
```

---

## 3. 타이포그래피 (Typography)

| 역할 | 클래스 |
|------|--------|
| 페이지 제목 | `text-2xl font-bold text-slate-900 tracking-tight` |
| 페이지 부제목 | `text-sm text-stone-400` |
| 섹션 헤딩 | `text-sm font-semibold text-slate-700` |
| 카드 레이블 | `text-xs text-stone-400 font-medium` |
| 필터 레이블 | `text-xs font-semibold text-stone-400 whitespace-nowrap` |
| 테이블 헤더 | `text-xs font-semibold text-slate-400` |
| KPI 숫자 (white card) | `text-3xl font-bold text-slate-900 tabular-nums` |
| KPI 숫자 (dark card) | `text-3xl font-bold text-white tabular-nums` |
| KPI 숫자 (amber card) | `text-3xl font-bold text-amber-900 tabular-nums` |
| 바디 텍스트 | `text-sm text-slate-900` |
| Muted 텍스트 | `text-xs text-stone-400` |
| 숫자 (테이블 내) | `font-bold text-sm text-slate-700 tabular-nums` |

---

## 4. 간격 / 레이아웃 (Spacing & Layout)

| 항목 | 값 |
|------|-----|
| 페이지 패딩 | `p-6` |
| 최대 너비 | `max-w-7xl mx-auto` |
| 컨텐츠 수직 간격 | `space-y-5` |
| KPI 카드 그리드 | `grid grid-cols-2 sm:grid-cols-4 gap-3` |
| 카드 내부 패딩 | `p-4` |
| 테이블 셀 패딩 | `px-4 py-3` (일반) / `px-4 py-3.5` (헤더) |
| 버튼 간격 | `gap-2` |

---

## 5. 적용하지 말아야 할 것 (Anti-patterns)

- ❌ `border border-gray-200` 카드 테두리 → `shadow-sm` 사용
- ❌ `bg-gradient-to-br from-slate-50 ...` 배경 → `bg-[#F5F3EE]` 단색 사용
- ❌ `rounded-xl` 카드 → `rounded-2xl` 사용
- ❌ Primary 버튼에 `bg-blue-600` → `bg-slate-900` 사용
- ❌ 필터 active에 `bg-gray-800` → `bg-slate-900` 사용
- ❌ 테이블 헤더 `bg-gray-50 border-b` → `bg-slate-900` 사용
- ❌ 액센트 컬러에 `bg-orange-*` / `bg-blue-*` 혼재 → amber/slate 통일
- ❌ `space-y-6` 페이지 간격 → `space-y-5` 사용

---

## 6. 실제 적용 사례

### 적용된 페이지
- `/Users/gwanli/.../dash1/app/ice/page.tsx` — ICE 스코어링
- `/Users/gwanli/.../dash1/app/problems/page.tsx` — 문제정의 관리
- `/Users/gwanli/.../dash1/app/globals.css` — 전역 배경색

### 참고 디자인
- Crextio HR Management Dashboard (Dribbble shot #25121521)
- 핵심 요소: 따뜻한 크림 배경, 황금 amber 액센트, 차콜 다크 패널, 화이트 카드 + 소프트 섀도
