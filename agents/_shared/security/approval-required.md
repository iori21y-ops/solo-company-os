# 승인 필요 위임 (Approval Required)

> 자동화가 **준비까지는 가능**하지만, **실행 전 텔레그램으로 경년님 승인**을 받아야 한다.
> n8n 워크플로우에서는 "승인 대기 노드"를 삽입하거나 텔레그램 Inline Keyboard로 확인.

## 마스터 데이터 변경

- `vehicles` 테이블 신규 차량 `INSERT`
- `vehicle_msrp`, `pricing` 등 가격 마스터 데이터 `INSERT` / `UPDATE`
- 신규 `slug` 활성화 (`is_active` = true)

## 차량 이미지 본 컬럼 업데이트

- `vehicles.image_url` 본 컬럼 업데이트 — 아래 조건 전부 충족 후 실행
  - 텔레그램에 변경 전/후 이미지 미리보기 첨부
  - 경년님 승인 확인 후에만 실행
  - 실행 전 기존값을 `vehicles.image_url_previous` 컬럼에 자동 보관
  - `image_url_previous` 컬럼이 없으면 `ALTER TABLE`로 추가 필요 → 이 컬럼 추가는 별도 승인 작업

## 콘텐츠 발행

- WordPress 게시물 `publish` (임시저장 → 게시 전환 포함)
- `info_articles` `INSERT` 후 `published_at` 세팅 (공개 발행)

## 대량 작업

- 10건 이상의 일괄 `UPDATE`
- 신규 카테고리·태그 생성

## 버전 관리

- `git commit` 실행 (자동화·스크립트 모두 해당)
- `git push` 실행
- `git tag` 생성·삭제
- `main` 브랜치 직접 변경

> 이유: 자동화·AI가 경년님 명령 없이 커밋·푸시하는 것은 위임 원칙 위반.
> 커밋·푸시는 항상 경년님이 내용을 확인한 뒤 직접 실행하거나, 텔레그램 승인 후에만 실행.

## 승인 메시지 형식 (텔레그램)

```
[승인 요청] {작업 설명}
대상: {테이블 or 파일}
건수: {N}건
[✅ 승인] [❌ 거절]
```

이미지 업데이트 시 추가 첨부:
- 이전 이미지 URL
- 새 이미지 URL (또는 미리보기 썸네일)
