#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'portadas.json'

PATTERN = re.compile(
    r'^(?:PORTADA-(\d+)|[A-Z][1-9]?-PORTADA-(\d+))$',
    re.IGNORECASE,
)

def parse_name(name: str):
    base = Path(name).stem
    match = PATTERN.match(base)
    if not match:
        return None

    order = int(match.group(1) or match.group(2))
    priority = 1 if match.group(2) is not None else 0

    return {'order': order, 'priority': priority}

files = []
for p in sorted(ROOT.iterdir()):
    if not p.is_file() or p.suffix.lower() != '.png':
        continue
    base = p.name
    parsed = parse_name(base)
    if parsed is None:
        continue
    files.append((parsed['order'], parsed['priority'], base))

files.sort(key=lambda item: (item[0], item[1], item[2]))
out = [name for _, _, name in files]
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=2))
