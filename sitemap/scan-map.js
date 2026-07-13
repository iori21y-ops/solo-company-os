#!/usr/bin/env node
// scan-map.js — rentailor 사이트맵 골격(라우트) 자동 추출.
// cadam-web / cadam-erp 의 App Router 파일을 스캔해 id 목록을 만들고,
// baseline 대비 added/removed diff 를 산출한다. 외부 패키지 없이 fs/path 만 사용.
//
// id 규칙:
//   prefix — web:(웹 페이지) / erp:(erp 페이지) / web-api: / erp-api:
//   라우트 그룹 (redesign),(shell) 등 괄호 세그먼트는 URL 에서 제거
//   동적 세그먼트 [slug],[id],[token] 원형 유지
//   /page.tsx · /route.ts 제거, 루트는 '/'
//   리라이트(FLIP)는 해석하지 않음 — 파일 경로 그대로(-preview 이름 유지)

const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process'); // Node 내장 — 외부 패키지 아님

const HOME = process.env.HOME;
const OUT_DIR = path.join(HOME, 'projects/_meta/sitemap');

// --dry-run: 실발송·baseline 쓰기 없이 상태만 산출(검증용). 라우트 파일도 손대지 않음.
const DRY_RUN = process.argv.includes('--dry-run');

// 인프라 노드 레이어 산출 파일 (route diff 의 scan-baseline.json 과 완전 분리)
const MAP_PATH = path.join(OUT_DIR, 'rentailor-map.json');
const INFRA_LATEST = path.join(OUT_DIR, 'scan-infra-latest.json');
const INFRA_BASELINE = path.join(OUT_DIR, 'scan-infra-baseline.json');

const TARGETS = [
  { root: path.join(HOME, 'projects/cadam/cadam-web/src/app'), pagePrefix: 'web',  apiPrefix: 'web-api' },
  { root: path.join(HOME, 'projects/cadam/cadam-erp/src/app'), pagePrefix: 'erp',  apiPrefix: 'erp-api' },
];

// 알림 대상 Discord 채널 (사이트맵 변화 알림). 봇 토큰은 브로커와 동일한 DISCORD_BOT_TOKEN 재사용.
const DISCORD_CHANNEL_ID = '1525715228405403738';

const IGNORE_DIRS = new Set(['node_modules', '.next']);
const PAGE_FILES = new Set(['page.tsx', 'page.ts', 'page.jsx']);
const API_FILES = new Set(['route.ts']);

// 디렉토리 재귀 순회 → 파일 절대경로 목록
function walk(dir) {
  const out = [];
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of entries) {
    if (e.isDirectory()) {
      if (IGNORE_DIRS.has(e.name)) continue;
      out.push(...walk(path.join(dir, e.name)));
    } else if (e.isFile()) {
      out.push(path.join(dir, e.name));
    }
  }
  return out;
}

// src/app 상대경로 → URL 경로(괄호 그룹 제거, 파일명 제거)
function toUrlPath(relFromApp) {
  const segs = relFromApp.split('/');
  segs.pop(); // page.tsx / route.ts 제거
  const kept = segs.filter((s) => s && !/^\(.*\)$/.test(s)); // 괄호 라우트 그룹 제거
  return '/' + kept.join('/'); // 루트면 '/' + '' = '/'
}

function scan() {
  const routes = [];
  const counts = { web: 0, erp: 0, web_api: 0, erp_api: 0, total: 0 };

  for (const t of TARGETS) {
    for (const file of walk(t.root)) {
      const base = path.basename(file);
      const isPage = PAGE_FILES.has(base);
      const isApi = API_FILES.has(base);
      if (!isPage && !isApi) continue;

      const rel = path.relative(t.root, file);
      const urlPath = toUrlPath(rel);
      const prefix = isApi ? t.apiPrefix : t.pagePrefix;
      routes.push(`${prefix}:${urlPath}`);

      if (isApi) counts[t.apiPrefix === 'web-api' ? 'web_api' : 'erp_api']++;
      else counts[t.pagePrefix]++;
    }
  }

  routes.sort();
  counts.total = routes.length;
  return { routes, counts };
}

function readJson(p) {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    return null;
  }
}

// YYYYMMDD (로컬)
function yyyymmdd() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}`;
}

// diff 목록 → Discord content 문자열 (상위 15개 + "외 N개")
function buildMessage(added, removed) {
  const MAX = 15;
  const block = (title, arr, sign) => {
    if (arr.length === 0) return '';
    const head = arr.slice(0, MAX).map((r) => `${sign} ${r}`).join('\n');
    const rest = arr.length > MAX ? `\n…외 ${arr.length - MAX}개` : '';
    return `\n\n**${title}**\n${head}${rest}`;
  };
  return `🗺 **사이트맵 변화 감지**\n신규 ${added.length}개 / 삭제 ${removed.length}개`
    + block('신규', added, '+')
    + block('삭제', removed, '-');
}

// Discord 봇 REST 전송 (브로커/health-check와 동일: Bot 토큰 + /channels/{id}/messages).
// 실패해도 throw 하지 않음(호출부에서 exit 0 유지). 성공(HTTP 200) 여부를 resolve.
function sendDiscord(token, content) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ content: content.slice(0, 1900) }); // Discord 2000자 한도 여유
    const opts = {
      method: 'POST',
      hostname: 'discord.com',
      path: `/api/v10/channels/${DISCORD_CHANNEL_ID}/messages`,
      headers: {
        'Authorization': `Bot ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
      timeout: 8000,
    };
    const req = https.request(opts, (res) => {
      let resp = '';
      res.on('data', (c) => { resp += c; });
      res.on('end', () => {
        const ok = res.statusCode === 200;
        if (ok) console.log(`Discord OK (HTTP 200, channel ${DISCORD_CHANNEL_ID})`);
        else console.warn(`WARN: Discord 전송 실패 (HTTP ${res.statusCode}) ${resp.slice(0, 200)}`);
        resolve(ok);
      });
    });
    req.on('error', (e) => {
      console.warn(`WARN: Discord 전송 오류 — ${e.message}`);
      resolve(false);
    });
    req.on('timeout', () => {
      console.warn('WARN: Discord 전송 타임아웃');
      req.destroy();
      resolve(false);
    });
    req.write(body);
    req.end();
  });
}

// ── 라우트 스캔(기존 로직) — 자체 return 으로 흐름 종료 후 main 이 이어서 인프라 스캔 실행 ──
async function runRouteScan() {
  const { routes, counts } = scan();
  const latest = {
    generated_at: new Date().toISOString(),
    counts,
    routes,
  };

  const latestPath = path.join(OUT_DIR, 'scan-latest.json');
  const baselinePath = path.join(OUT_DIR, 'scan-baseline.json');

  // dry-run: 라우트 파일 일절 쓰지 않고 알림도 안 함(검증 시 route baseline/latest 훼손 방지)
  if (DRY_RUN) {
    const baseline = readJson(baselinePath) || { routes: [] };
    const baseSet = new Set(baseline.routes || []);
    const nowSet = new Set(routes);
    const added = routes.filter((r) => !baseSet.has(r));
    const removed = (baseline.routes || []).filter((r) => !nowSet.has(r));
    console.log(`ROUTE_DRY_RUN  total=${counts.total} added=${added.length} removed=${removed.length} (쓰기/알림 생략)`);
    return;
  }

  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + '\n');

  const baseline = readJson(baselinePath);
  if (!baseline) {
    fs.writeFileSync(baselinePath, JSON.stringify(latest, null, 2) + '\n');
    console.log('BASELINE_CREATED');
    console.log(`web=${counts.web} erp=${counts.erp} web_api=${counts.web_api} erp_api=${counts.erp_api} total=${counts.total}`);
    return;
  }

  const baseSet = new Set(baseline.routes || []);
  const nowSet = new Set(routes);
  const added = routes.filter((r) => !baseSet.has(r));
  const removed = (baseline.routes || []).filter((r) => !nowSet.has(r));

  if (added.length === 0 && removed.length === 0) {
    console.log('NO_CHANGE');
    return;
  }

  const diff = {
    generated_at: latest.generated_at,
    baseline_at: baseline.generated_at || null,
    added,
    removed,
  };
  // diff 는 날짜 붙여 보존 (같은 날 재실행 시 덮어쓰기)
  const diffPath = path.join(OUT_DIR, `scan-diff-${yyyymmdd()}.json`);
  fs.writeFileSync(diffPath, JSON.stringify(diff, null, 2) + '\n');

  console.log(`CHANGED  added=${added.length} removed=${removed.length}`);
  for (const r of added) console.log(`  + ${r}`);
  for (const r of removed) console.log(`  - ${r}`);

  // Discord 알림 (diff 있을 때만)
  const token = process.env.DISCORD_BOT_TOKEN;
  if (!token || token.trim() === '') {
    console.warn('WARN: DISCORD_BOT_TOKEN 미설정 — 알림 생략(스캔은 정상)');
  } else {
    await sendDiscord(token, buildMessage(added, removed));
  }

  // baseline 을 latest 로 갱신 — 같은 변화를 매일 반복 알림하지 않기 위함
  fs.writeFileSync(baselinePath, JSON.stringify(latest, null, 2) + '\n');
}

// ────────────────────────────────────────────────────────────────
// 인프라 노드 레이어 스캔 (2026-07-13 추가)
// rentailor-map.json 의 infra_ops_nodes 를 읽어 '기계적으로 확인 가능한 상태'만 점검.
// 산출: scan-infra-latest.json. 변화 시에만(토큰 있고 dry-run 아닐 때) #시스템알림 통보.
// ────────────────────────────────────────────────────────────────

// child_process 안전 실행 — 비정상 종료(grep/pgrep no-match 등)여도 stdout 반환, 없으면 ''
function sh(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf8', timeout: 8000, stdio: ['ignore', 'pipe', 'ignore'] });
  } catch (e) {
    return e && e.stdout ? String(e.stdout) : '';
  }
}

// `launchctl list` 1회 → Map(label → {pid, exit})
function loadLaunchctl() {
  const out = sh('launchctl list');
  const m = new Map();
  for (const line of out.split('\n')) {
    const parts = line.split('\t');
    if (parts.length < 3) continue;
    const label = parts[2].trim();
    if (label === 'Label') continue;
    m.set(label, { pid: parts[0].trim(), exit: parts[1].trim() });
  }
  return m;
}

// `docker ps` 1회 → {set:Set(names), ok:bool}. docker 미설치/미기동이면 ok=false
function loadDocker() {
  try {
    const out = execSync("docker ps --format '{{.Names}}'", { encoding: 'utf8', timeout: 8000, stdio: ['ignore', 'pipe', 'ignore'] });
    return { set: new Set(out.split('\n').map((s) => s.trim()).filter(Boolean)), ok: true };
  } catch {
    return { set: new Set(), ok: false };
  }
}

function portListening(port) {
  const out = sh(`lsof -nP -iTCP:${port} -sTCP:LISTEN`);
  return /LISTEN/.test(out);
}

function pgrepCount(pattern) {
  const out = sh(`pgrep -f ${JSON.stringify(pattern)}`);
  return out.trim().split('\n').filter(Boolean).length;
}

// 노드 1개 상태 판정. status 는 변화감지의 기준(거친 상태값).
function checkInfraNode(node, lc, docker, dockerOk) {
  const c = node.check || { method: 'none' };
  const r = {
    id: node.id, name: node.name, nodeType: node.nodeType,
    category: node.category, method: c.method, judge: c.judge || 'strict',
  };
  if (c.method === 'launchctl') {
    const e = lc.get(c.target);
    if (!e) { r.status = 'MISSING'; r.detail = 'launchctl 미적재'; }
    else {
      r.pid = e.pid; r.lastExit = e.exit;
      if (c.kind === 'resident') r.status = (e.pid && e.pid !== '-') ? 'up' : 'DOWN';
      else r.status = 'loaded'; // scheduled: tick 사이 PID '-' 는 정상
    }
  } else if (c.method === 'docker') {
    if (!dockerOk) { r.status = 'UNKNOWN'; r.detail = 'docker 조회 불가'; }
    else r.status = docker.has(c.target) ? 'up' : 'down';
  } else if (c.method === 'pgrep') {
    const n = pgrepCount(c.target); r.procCount = n; r.status = n > 0 ? 'alive' : 'ABSENT';
  } else if (c.method === 'port') {
    r.status = portListening(c.target) ? 'listen' : 'CLOSED';
  } else {
    r.status = 'n/a'; r.detail = c.reason || '기계적 확인 불가(종속/외부)';
  }
  // 보조 프로브(있으면): 포트 리슨 / pgrep 교차확인
  if (c.port) r.portProbe = { port: c.port, listen: portListening(c.port) };
  if (c.pgrep) r.pgrepProbe = { pattern: c.pgrep, count: pgrepCount(c.pgrep) };
  return r;
}

function buildInfraMessage(changed, newNodes) {
  const lines = changed.map((c) => `• ${c.name}: ${c.from} → ${c.to}`);
  const head = `🖥 **인프라 노드 상태 변화**\n변경 ${changed.length}건`
    + (newNodes.length ? ` / 신규 ${newNodes.length}건` : '');
  return head + (lines.length ? '\n\n' + lines.slice(0, 15).join('\n') : '');
}

async function scanInfra() {
  let map;
  try {
    map = JSON.parse(fs.readFileSync(MAP_PATH, 'utf8'));
  } catch (e) {
    console.warn('WARN: 인프라 스캔 생략 — 지도 파싱 실패: ' + e.message);
    return; // 라우트 스캔에 영향 주지 않음
  }
  const nodes = Array.isArray(map.infra_ops_nodes) ? map.infra_ops_nodes : [];
  if (nodes.length === 0) {
    console.warn('WARN: infra_ops_nodes 없음 — 인프라 스캔 생략');
    return;
  }

  const lc = loadLaunchctl();
  const { set: docker, ok: dockerOk } = loadDocker();
  const results = nodes.map((n) => checkInfraNode(n, lc, docker, dockerOk));

  // 요약 집계
  const byStatus = {};
  for (const r of results) byStatus[r.status] = (byStatus[r.status] || 0) + 1;
  const problems = results.filter((r) => ['MISSING', 'DOWN', 'down', 'ABSENT', 'CLOSED'].includes(r.status) && r.judge !== 'info');

  const out = {
    generated_at: new Date().toISOString(),
    dry_run: DRY_RUN,
    docker_available: dockerOk,
    summary: { total: results.length, by_status: byStatus, problems_strict: problems.length },
    nodes: results,
  };

  console.log(`INFRA  total=${results.length} ` + Object.entries(byStatus).map(([k, v]) => `${k}=${v}`).join(' '));
  if (problems.length) {
    console.log(`INFRA_PROBLEMS(strict)=${problems.length}`);
    for (const p of problems) console.log(`  ! ${p.id} ${p.status}`);
  }

  if (DRY_RUN) {
    fs.writeFileSync(INFRA_LATEST, JSON.stringify(out, null, 2) + '\n');
    console.log('INFRA_DRY_RUN — scan-infra-latest.json 만 기록(baseline/Discord 생략)');
    return;
  }

  fs.writeFileSync(INFRA_LATEST, JSON.stringify(out, null, 2) + '\n');

  const base = readJson(INFRA_BASELINE);
  if (!base) {
    fs.writeFileSync(INFRA_BASELINE, JSON.stringify(out, null, 2) + '\n');
    console.log('INFRA_BASELINE_CREATED');
    return;
  }

  // 변화 감지: 노드별 거친 status 비교(lastExit/PID 변동은 노이즈라 제외)
  const baseMap = new Map((base.nodes || []).map((n) => [n.id, n.status]));
  const changed = results
    .filter((r) => baseMap.has(r.id) && baseMap.get(r.id) !== r.status)
    .map((r) => ({ id: r.id, name: r.name, from: baseMap.get(r.id), to: r.status, judge: r.judge }));
  const newNodes = results.filter((r) => !baseMap.has(r.id));

  if (changed.length === 0 && newNodes.length === 0) {
    console.log('INFRA_NO_CHANGE');
  } else {
    console.log(`INFRA_CHANGED  changed=${changed.length} new=${newNodes.length}`);
    for (const c of changed) console.log(`  ~ ${c.id}: ${c.from} -> ${c.to}`);
    // judge:info(시각 의존 n8n·gpu-agent 등)는 알림 제외 — 보고만
    const alertable = changed.filter((c) => c.judge !== 'info');
    const token = process.env.DISCORD_BOT_TOKEN;
    if (alertable.length === 0) {
      console.log('INFRA: 변화는 있으나 전부 info 등급 — 알림 생략');
    } else if (!token || token.trim() === '') {
      console.warn('WARN: DISCORD_BOT_TOKEN 미설정 — 인프라 알림 생략(스캔은 정상)');
    } else {
      await sendDiscord(token, buildInfraMessage(alertable, newNodes));
    }
  }

  // 인프라 baseline 갱신(같은 변화 반복 알림 방지)
  fs.writeFileSync(INFRA_BASELINE, JSON.stringify(out, null, 2) + '\n');
}

async function main() {
  await runRouteScan(); // 라우트 diff (기존)
  await scanInfra();    // 인프라 노드 상태 (신규) — 라우트 무변화여도 항상 실행
}

main();
