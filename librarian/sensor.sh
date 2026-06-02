#!/bin/bash
# 사서 센서 — 시스템 상태 사실만 JSON으로 기록 (판정 없음)
# 판정·보고는 사서 AI가 snapshot을 읽고 한다.
# health-check.sh와 병행(대체는 사서 SKILL 검증 후).

SENSOR_VERSION="1.0"
LIB_DIR="$HOME/projects/_meta/librarian"
HIST_DIR="$LIB_DIR/history"
LATEST="$LIB_DIR/snapshot-latest.json"
EXCEPTIONS_FILE="$LIB_DIR/expected_exceptions.txt"
mkdir -p "$HIST_DIR"

NOW=$(date '+%Y-%m-%dT%H:%M:%S')
STAMP=$(date '+%Y%m%d-%H%M')
HOST=$(hostname)

# 예외 명단 로드(한 줄에 서비스명 하나). 없으면 빈 값.
EXCEPTIONS=""
[ -f "$EXCEPTIONS_FILE" ] && EXCEPTIONS=$(grep -v '^#' "$EXCEPTIONS_FILE" 2>/dev/null | grep -v '^$')

# 모든 수집을 python에 넘겨 안전하게 JSON 생성(셸 문자열 조립은 깨지기 쉬움)
NOW="$NOW" STAMP="$STAMP" HOST="$HOST" SENSOR_VERSION="$SENSOR_VERSION" \
EXCEPTIONS="$EXCEPTIONS" LATEST="$LATEST" HIST_DIR="$HIST_DIR" \
python3 << 'PYEOF'
import os, json, subprocess, re, glob, time

def sh(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""

snap = {}

# --- meta ---
snap["meta"] = {
    "time": os.environ["NOW"],
    "host": os.environ["HOST"],
    "sensor_version": os.environ["SENSOR_VERSION"],
}

# --- disk (df -H /) ---
disk = {}
out = sh("df -H / | awk 'NR==2 {print $5, $4}'")
if out:
    parts = out.split()
    disk["used_percent"] = int(parts[0].replace("%", "")) if parts else None
    disk["avail"] = parts[1] if len(parts) > 1 else None
snap["disk"] = disk

# --- memory (memory_pressure) ---
mem = {}
mp = sh("memory_pressure 2>/dev/null | grep 'System-wide memory free percentage' | awk '{print $NF}' | tr -d '%'")
mem["free_percent"] = int(mp) if mp.isdigit() else None
snap["memory"] = mem

# --- launchd (커스텀만) ---
launchd = []
out = sh("launchctl list 2>/dev/null | grep -v com.apple")
for line in out.splitlines():
    cols = line.split()
    if len(cols) >= 3 and cols[0] != "PID":
        pid, status, label = cols[0], cols[1], cols[2]
        launchd.append({
            "label": label,
            "pid": None if pid == "-" else int(pid) if pid.lstrip("-").isdigit() else pid,
            "status": int(status) if status.lstrip("-").isdigit() else status,
        })
snap["launchd"] = launchd

# --- docker ---
docker = []
out = sh("docker ps -a --format '{{.Names}}|{{.Status}}|{{.Image}}'")
for line in out.splitlines():
    p = line.split("|")
    if len(p) == 3:
        docker.append({"name": p[0], "status": p[1], "image": p[2]})
snap["docker"] = docker

# --- services (managed/adhoc 자동분류) ---
# 1) launchd 등록 라벨 집합, docker 이름 집합 = managed 근거
launchd_labels = {j["label"] for j in launchd}
docker_names = {d["name"] for d in docker}
exceptions = set(filter(None, os.environ.get("EXCEPTIONS", "").splitlines()))

# 2) LISTEN 포트 목록
services = []
out = sh("lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print $1, $2, $9}'")
seen = set()
for line in out.splitlines():
    cols = line.split()
    if len(cols) < 3:
        continue
    cmd, pid, addr = cols[0], cols[1], cols[2]
    m = re.search(r":(\d+)$", addr)
    port = int(m.group(1)) if m else None
    key = (pid, port)
    if key in seen:
        continue
    seen.add(key)
    # 프로세스 실행커맨드로 이름 추정
    fullcmd = sh(f"ps -p {pid} -o command= 2>/dev/null")
    name = None
    mscript = re.search(r"(\w+\.py|\w+\.js)", fullcmd)
    if mscript:
        name = mscript.group(1)
    elif "http.server" in fullcmd:
        name = f"http.server:{port}"
    else:
        name = cmd
    # managed 판정: docker 이름에 포함되거나, 흔한 managed 신호
    is_managed = ("http.server" not in fullcmd)
    svc_type = "managed" if is_managed else "adhoc"
    expected = (svc_type == "managed")
    if name in exceptions:
        expected = False
    services.append({
        "name": name, "port": port, "pid": int(pid),
        "type": svc_type, "expected": expected, "alive": True,
    })

snap["services"] = services
snap["expected_exceptions"] = sorted(exceptions)

# --- backup (cadam backups 폴더 최신 파일) ---
backup = {}
candidates = []
for d in [os.path.expanduser("~/projects/cadam/backups"),
          os.path.expanduser("~/projects/cadam/backups-manual")]:
    if os.path.isdir(d):
        files = glob.glob(os.path.join(d, "*"))
        for f in files:
            try:
                candidates.append((os.path.getmtime(f), f, os.path.getsize(f)))
            except Exception:
                pass
if candidates:
    candidates.sort(reverse=True)
    mt, path, size = candidates[0]
    backup["last_file"] = os.path.basename(path)
    backup["last_time"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(mt))
    backup["size_bytes"] = size
else:
    backup["last_file"] = None
snap["backup"] = backup

# --- git (_meta 마지막 커밋) ---
git = {}
meta = os.path.expanduser("~/projects/_meta")
git["last_commit"] = sh(f"git -C {meta} log -1 --format=%cI 2>/dev/null") or None
git["last_subject"] = sh(f"git -C {meta} log -1 --format=%s 2>/dev/null") or None
snap["git"] = git

# --- remote (별도 트랙 — 자리만) ---
snap["remote"] = {"status": "not_implemented"}

# --- 저장 ---
text = json.dumps(snap, ensure_ascii=False, indent=2)
with open(os.environ["LATEST"], "w") as f:
    f.write(text)
hist = os.path.join(os.environ["HIST_DIR"], f"snapshot-{os.environ['STAMP']}.json")
with open(hist, "w") as f:
    f.write(text)
print(f"OK: {os.environ['LATEST']}")
print(f"OK: {hist}")
PYEOF
