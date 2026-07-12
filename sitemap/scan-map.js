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

const HOME = process.env.HOME;
const OUT_DIR = path.join(HOME, 'projects/_meta/sitemap');

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

async function main() {
  const { routes, counts } = scan();
  const latest = {
    generated_at: new Date().toISOString(),
    counts,
    routes,
  };

  const latestPath = path.join(OUT_DIR, 'scan-latest.json');
  const baselinePath = path.join(OUT_DIR, 'scan-baseline.json');

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

main();
