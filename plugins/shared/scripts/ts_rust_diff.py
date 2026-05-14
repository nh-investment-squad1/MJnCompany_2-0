#!/usr/bin/env python3
"""
CSnCompany: ts_rust_diff.py — 노하우 #16 자동화
TypeScript interface 필드 ↔ Rust struct 필드를 비교하여 불일치를 JSON으로 출력.
serde 역직렬화 시 silently drop되는 필드를 LLM 추론 없이 결정론적으로 탐지.

Usage: python3 ts_rust_diff.py <project_root>
"""

import sys
import os
import re
import json
from pathlib import Path

SKIP_DIRS = {'.git', 'node_modules', '.next', 'dist', 'build', 'target',
             '__pycache__', 'cargo-targets'}

# TS interface/type 파싱
TS_INTERFACE = re.compile(
    r'(?:export\s+)?(?:interface|type)\s+(\w+)\s*(?:extends\s+\w+\s*)?\{([^}]+)\}',
    re.DOTALL
)
TS_FIELD = re.compile(r'^\s*(?:readonly\s+)?(\w+)\s*\??:', re.MULTILINE)

# Rust struct 파싱
RS_STRUCT = re.compile(
    r'(?:#\[derive[^\]]*\])?\s*(?:pub\s+)?struct\s+(\w+)\s*\{([^}]+)\}',
    re.DOTALL
)
RS_FIELD = re.compile(r'^\s*(?:pub\s+)?(\w+)\s*:', re.MULTILINE)


def extract_ts_interfaces(root: Path) -> dict:
    interfaces = {}
    for path in root.rglob('*.ts'):
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
            for name, body in TS_INTERFACE.findall(text):
                fields = TS_FIELD.findall(body)
                # 주석 제거
                fields = [f for f in fields if not f.startswith('//')]
                if fields:
                    interfaces[name] = {
                        'fields': fields,
                        'file': str(path.relative_to(root))
                    }
        except Exception:
            continue
    return interfaces


def extract_rs_structs(root: Path) -> dict:
    structs = {}
    for path in root.rglob('*.rs'):
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
            for name, body in RS_STRUCT.findall(text):
                fields = RS_FIELD.findall(body)
                if fields:
                    structs[name] = {
                        'fields': fields,
                        'file': str(path.relative_to(root))
                    }
        except Exception:
            continue
    return structs


def compare(ts_interfaces: dict, rs_structs: dict) -> list:
    mismatches = []
    for name in ts_interfaces:
        if name not in rs_structs:
            continue
        ts_fields = set(ts_interfaces[name]['fields'])
        rs_fields = set(rs_structs[name]['fields'])

        only_in_ts = ts_fields - rs_fields
        only_in_rs = rs_fields - ts_fields

        if only_in_ts or only_in_rs:
            mismatches.append({
                'name': name,
                'ts_file': ts_interfaces[name]['file'],
                'rs_file': rs_structs[name]['file'],
                'only_in_ts': sorted(only_in_ts),   # RS에 없음 → serde drop 위험
                'only_in_rs': sorted(only_in_rs),   # TS에 없음
                'severity': 'HIGH' if only_in_ts else 'LOW',
                'risk': f"Rust struct '{name}'에 {sorted(only_in_ts)} 필드 없음 — JSON 역직렬화 시 silently drop" if only_in_ts else None
            })
    return mismatches


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Usage: ts_rust_diff.py <project_root>'}))
        sys.exit(1)

    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.exists():
        print(json.dumps({'error': f'Path not found: {root}'}))
        sys.exit(1)

    ts_interfaces = extract_ts_interfaces(root)
    rs_structs = extract_rs_structs(root)
    mismatches = compare(ts_interfaces, rs_structs)

    output = {
        'ts_interfaces_found': len(ts_interfaces),
        'rs_structs_found': len(rs_structs),
        'matched_pairs': sum(1 for n in ts_interfaces if n in rs_structs),
        'mismatches': mismatches,
        'high_risk_count': sum(1 for m in mismatches if m['severity'] == 'HIGH'),
    }
    print(json.dumps(output, ensure_ascii=False, indent=None))


if __name__ == '__main__':
    main()
