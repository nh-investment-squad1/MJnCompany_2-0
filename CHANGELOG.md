# Changelog

## [session] 2026-05-02

### Fixed
- `~/.claude/hooks/notification-hook.sh`, `stop-hook.sh`: `.env` 없는 프로젝트에서 `exit 1` → `exit 0` 변경
  - 원인: 훅 비정상 종료가 Claude Code 입력창을 회색으로 블로킹
  - 영향: CS볼트V5 등 `.env` 없는 작업 폴더에서 입력 불가 현상 해소

## [cs-end-v1] 1.1.0 — 2026-05-01

### Added
- Phase 6: Context Compact suggestion — after Phase 5 push report, generates a
  1-2 line session summary and presents a ready-to-run `/compact [summary]` command.
  Skip with `--no-compact` or `--learning-only`.
- `--no-compact` flag added to usage examples.

### Changed
- Frontmatter description updated to include "context compact 제안".
- plugin.json description updated.
