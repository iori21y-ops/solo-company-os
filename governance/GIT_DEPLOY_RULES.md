# git·배포 규칙 (GIT_DEPLOY_RULES)

> 무엇을 정하는 파일: 커밋 메시지, 저장소(리포) 목록, 커밋에 넣을 파일 고르기, push와 배포.
> 마지막 갱신: 2026-11-13 (폴더 이동 후 리포 표 다시 확인) · **이 파일이 원본 — 다른 문서는 여기를 가리킨다.** 지도: [RULES_MAP.md](RULES_MAP.md)
> 배포 상세(Vercel 설정·환경변수·도메인)는 `~/projects/cadam/docs/deploy.md`.

## 1. 커밋 (사장님 결정 1, 2026-11-11)
- 커밋 메시지·코드 주석 = **영어**. (문서 본문은 한국어)
- **파일을 고치기 전에** 그 저장소에서 먼저 커밋: `checkpoint: <작업 설명>`
- Linear 이슈 번호를 넣는다: 진행 중 `Refs REN-N`, 끝났으면 `Fixes REN-N` (push 때 이슈 자동 연결·완료).
- 위키(second-brain) 커밋 메시지: `ingest: …` / `query: …` / `lint: …`. iCloud 볼트 자체는 git이 아니다 — 미러 `~/second-brain-git`이 밤마다 볼트를 복사(rsync)한 뒤 커밋·push한다.
- 커밋은 승인 없이 하고 보고한다 ([SAFETY_RULES.md](SAFETY_RULES.md) §1).
- `node_modules`, `.next`, `__pycache__`, `.env` 류는 커밋하지 않는다.

## 2. 저장소(리포) — 커밋·push 전 `pwd` + `git remote -v` 확인 필수
2026-11-13 `git remote` 확인. 리모트는 모두 `github.com/iori21y-ops/…`.

| 폴더 | 리모트 | 무엇 |
|---|---|---|
| `~/projects/cadam` | `cadam-doc` | 렌테일러 사업 리포: 운영 문서 `docs/`(노션 동기화) + 코드 `collect/`·`core/`·`process/`·`check/`·`facts/`·`ops/`·`services/` 등(2026-11-13 옛 리포 `cadam-n8n`·`cadam-auto`를 이력째 합침, 옛 리포는 보관만) — **코드가 들어 있으므로 push는 따로 승인** |
| `~/projects/web-engine/cadam-web` | `cadam` | 렌테일러 사이트 — **push = 배포** |
| `~/projects/web-engine/cadam-erp` | `cadam-erp` | ERP·모니터 (반영은 `scripts/deploy.sh`, 재시작이라 승인) |
| `~/projects/content-engine` | `blog-engine` (리포 이름은 옛 이름 그대로) | 콘텐츠 엔진(글·영상) |
| `~/projects/content-engine/publishers/naver` | `cadam-naver` | 네이버 발행 서버 (엔진 안의 따로 리포) |
| `~/projects/content-engine/video` | `my-shorts` | 수동 쇼츠 작업 공간 (엔진 안의 따로 리포) |
| `~/projects/_shared` | `solo-shared` | 공용 라이브러리 `solo_common` |
| `~/projects/_meta` | `solo-company-os` | 공통 규칙·인계·점검 스크립트 |
| `~/projects/football-blog` | `football-blog` | 해외파 |
| `~/projects/import-lease` | `import-lease` | 임포리스 |
| `~/second-brain-git` | `second-brain` | 위키 미러 |

- 폴더 안의 따로 리포(`content-engine/publishers/naver`, `content-engine/video`, `cadam/services/gpu-agent`)는 바깥 리포의 `git status`로 안 보인다 → 그 폴더로 들어가서 커밋.
- `~/projects/web-engine` 자체는 리포가 아니다(묶음 폴더).

## 3. 커밋에 넣을 파일 고르기
- 다른 세션의 미커밋 변경이 섞여 있을 수 있다 → **내가 바꾼 파일만** 넣는다.
- 새 파일: `git add <내 파일 경로들>` → `git commit -- <같은 경로들>`. 이미 추적 중인 파일만이면 `git commit -- <경로>`.
- `git add .`·`git add -A`·`git commit -a`는 남의 변경이 없을 때만.

## 4. push (사장님 결정 3)
- push는 **승인 후**. 승인 대상은 커밋이 아니라 push다.
- **"마무리해줘" = 문서·규칙 리포(_meta·_shared 등) push 승인** (결정 10). 코드·사이트 리포(cadam-doc — 2026-11-13부터 코드 포함, cadam-web·cadam-erp·content-engine·football-blog·import-lease 등)는 따로 승인. ERP 이슈 등록(`commitAndPush`)은 cadam-doc을 그대로 push하므로 아직 push 안 한 코드 커밋도 함께 올라간다 — 코드 커밋은 바로 push 승인을 받을 것.
- push 전 `git log --oneline -5`로 올라갈 커밋 확인. 남의 커밋이 섞였으면 보고.
- push 후 `git log --oneline origin/main -3`으로 원격 반영 확인.
- 강제 push·`reset --hard` 금지. merge·rebase도 승인 후.

## 5. 배포 (사장님 결정 2, 2026-11-11)
| 리포 | push하면 | 규칙 |
|---|---|---|
| cadam-web | **즉시 프로덕션 배포** (rentailor.co.kr, Vercel Git 연동) | 사장님 승인 → **로컬 빌드 확인 필수**(`npm run build`) → Claude가 push → `npx vercel ls`로 새 배포 시각 확인 |
| cadam-doc | GitHub Actions가 바뀐 `docs/*.md`를 노션에 복사 | 승인 후 push("마무리해줘"면 승인된 것) → 노션 반영 확인 ([DOCS_RULES.md](DOCS_RULES.md) §2) |
| 그 밖 | 원격 저장만 (Linear 이슈 연결) | 승인 후 push |

- 자동 배포 켜짐/꺼짐은 바뀐 적이 있다 → 배포 여부가 중요하면 문서 말고 `npx vercel ls`로 실측.
- 빌드 실패 시 Vercel은 이전 배포를 그대로 둔다.
