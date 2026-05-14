#!/usr/bin/env python3
"""
CSnCompany: extract_summary.py
프로젝트 디렉토리를 스캔하여 파일 구조 + import 관계 + 함수 목록을 JSON으로 출력.
LLM이 파일 본문 전체를 읽는 대신 이 JSON을 INPUT으로 사용하면 토큰 대폭 절감.

Usage: python3 extract_summary.py <project_root> [--depth 3] [--ext ts,tsx,py,rs]
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

SKIP_DIRS = {'.git', 'node_modules', '.next', 'dist', 'build', 'target',
             '__pycache__', '.bkit', '.omc', '.playwright-mcp', '.next-build',
             'cargo-targets', '.cargo'}

# 언어별 import 패턴
IMPORT_PATTERNS = {
    '.ts': re.compile(r"""(?:import|from)\s+['"]([^'"]+)['"]|require\(['"]([^'"]+)['"]\)"""),
    '.tsx': re.compile(r"""(?:import|from)\s+['"]([^'"]+)['"]"""),
    '.js': re.compile(r"""(?:import|from)\s+['"]([^'"]+)['"]|require\(['"]([^'"]+)['"]\)"""),
    '.jsx': re.compile(r"""(?:import|from)\s+['"]([^'"]+)['"]"""),
    '.py': re.compile(r"""(?:^from\s+(\S+)\s+import|^import\s+(\S+))""", re.MULTILINE),
    '.rs': re.compile(r"""use\s+([\w:]+)"""),
}

# 함수/클래스 추출 패턴
FUNC_PATTERNS = {
    '.ts': re.compile(r"""(?:export\s+)?(?:async\s+)?function\s+(\w+)|(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s*)?\("""),
    '.tsx': re.compile(r"""(?:export\s+(?:default\s+)?)?(?:function|const)\s+(\w+)"""),
    '.py': re.compile(r"""^(?:async\s+)?def\s+(\w+)\s*\(""", re.MULTILINE),
    '.rs': re.compile(r"""(?:pub\s+)?(?:async\s+)?fn\s+(\w+)\s*[(<]"""),
}

# TS interface / Rust struct 추출 (ts_rust_diff.py와 연계)
STRUCT_PATTERNS = {
    '.ts': re.compile(r"""(?:export\s+)?interface\s+(\w+)\s*\{([^}]*)\}""", re.DOTALL),
    '.tsx': re.compile(r"""(?:export\s+)?(?:interface|type)\s+(\w+)\s*[={]\s*\{([^}]*)\}""", re.DOTALL),
    '.rs': re.compile(r"""(?:pub\s+)?struct\s+(\w+)\s*\{([^}]*)\}""", re.DOTALL),
}


def scan_file(path: Path) -> dict:
    ext = path.suffix.lower()
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return {}

    result = {
        'path': str(path),
        'ext': ext,
        'lines': text.count('\n'),
        'size_bytes': path.stat().st_size,
    }

    # imports
    pat = IMPORT_PATTERNS.get(ext)
    if pat:
        matches = pat.findall(text)
        imports = [m[0] or m[1] for m in matches if m[0] or (len(m) > 1 and m[1])]
        result['imports'] = list(dict.fromkeys(imports))[:20]  # dedupe, cap 20

    # functions
    fpat = FUNC_PATTERNS.get(ext)
    if fpat:
        fnames = [m[0] or (m[1] if len(m) > 1 else '') for m in fpat.findall(text)]
        result['functions'] = [f for f in fnames if f][:30]

    # structs/interfaces (짧게)
    spat = STRUCT_PATTERNS.get(ext)
    if spat:
        structs = {}
        for name, body in spat.findall(text):
            fields = re.findall(r'(\w+)\s*[?:]', body)
            structs[name] = fields[:15]
        if structs:
            result['structs'] = structs

    return result


def scan_dir(root: Path, depth: int, exts: set) -> list:
    results = []
    try:
        for entry in sorted(root.iterdir()):
            if entry.name.startswith('.') and entry.name in SKIP_DIRS:
                continue
            if entry.is_dir() and entry.name not in SKIP_DIRS:
                if depth > 0:
                    results.extend(scan_dir(entry, depth - 1, exts))
            elif entry.is_file() and entry.suffix.lower() in exts:
                info = scan_file(entry)
                if info:
                    results.append(info)
    except PermissionError:
        pass
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', help='Project root directory')
    parser.add_argument('--depth', type=int, default=4)
    parser.add_argument('--ext', default='ts,tsx,py,rs,js,jsx')
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(json.dumps({'error': f'Path not found: {root}'}))
        sys.exit(1)

    exts = {f'.{e.strip()}' for e in args.ext.split(',')}
    files = scan_dir(root, args.depth, exts)

    # 통계
    total_lines = sum(f.get('lines', 0) for f in files)
    by_ext = {}
    for f in files:
        by_ext[f['ext']] = by_ext.get(f['ext'], 0) + 1

    output = {
        'root': str(root),
        'total_files': len(files),
        'total_lines': total_lines,
        'by_ext': by_ext,
        'files': files,
    }
    print(json.dumps(output, ensure_ascii=False, indent=None))


if __name__ == '__main__':
    main()
