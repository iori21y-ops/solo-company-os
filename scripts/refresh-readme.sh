#!/usr/bin/env bash
# 루트 README.md의 AUTO-GENERATED active_areas 섹션 자동 갱신
# handoff/ 하위 디렉토리에서 handoff-latest.md 보유 영역을 스캔해 표 생성

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
README="$BASE_DIR/README.md"
HANDOFF_DIR="$BASE_DIR/handoff"
RAW_BASE="https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main"

# Python3으로 스캔 + README 갱신
python3 - "$README" "$HANDOFF_DIR" "$RAW_BASE" << 'PYEOF'
import re, os, sys

readme_path = sys.argv[1]
handoff_dir = sys.argv[2]
raw_base    = sys.argv[3]

# handoff-latest.md 보유 디렉토리 스캔
rows = []
for root, dirs, files in os.walk(handoff_dir):
    # .git 등 숨김 폴더 건너뜀
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    if 'handoff-latest.md' in files:
        area     = os.path.relpath(root, handoff_dir)
        category = area.split('/')[0]
        url      = f"{raw_base}/handoff/{area}/handoff-latest.md"
        rows.append((area, category, url))

rows.sort()
table_rows = "\n".join(
    f"| `{area}` | {cat} | [handoff-latest.md]({url}) |"
    for area, cat, url in rows
)

new_section = (
    "<!-- AUTO-GENERATED:START active_areas -->\n"
    "## 🚀 활성 핸드오프 영역\n\n"
    "> 자동 생성 — `scripts/refresh-readme.sh` 실행 시 갱신됩니다.\n\n"
    "| 영역 | 카테고리 | 핸드오프 |\n"
    "| ---- | -------- | -------- |\n"
    f"{table_rows}\n\n"
    "<!-- AUTO-GENERATED:END active_areas -->"
)

with open(readme_path) as f:
    content = f.read()

if "AUTO-GENERATED:START active_areas" in content:
    updated = re.sub(
        r'<!-- AUTO-GENERATED:START active_areas -->.*?<!-- AUTO-GENERATED:END active_areas -->',
        new_section,
        content,
        flags=re.DOTALL
    )
    action = "갱신"
else:
    updated = content.rstrip() + "\n\n" + new_section + "\n"
    action = "추가"

with open(readme_path, 'w') as f:
    f.write(updated)

print(f"✅ README.md 활성 영역 섹션 {action} 완료 ({len(rows)}개 영역 반영)")
PYEOF
