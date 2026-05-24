# 자동 허용 위임 (Auto-Allowed)

> 경년님 승인 없이 **무인 자동 실행이 허가된** 작업 목록.
> 이 목록에 없는 작업은 `approval-required.md` 또는 `delegation-blacklist.md`를 먼저 확인.

## 데이터 수집

- 읽기 전용 크롤링 (rate limit 준수: 요청 간 2초 이상 간격)
- 공공 API 조회 (KOSIS, 공공데이터포털 등)
- 제조사 사이트 이미지 URL 수집 (다운로드·저장 포함)

## 결과 저장

- 로컬 파일로만 저장하는 분류·라벨링 작업 (CSV, JSON, HTML 리포트)
- 로그 파일 생성·추가 (append)
- Supabase `SELECT` 조회 (읽기 전용)
- 처리 결과를 Supabase Storage의 `staging/` 또는 `tmp/` 경로에만 업로드.
  사용자 노출 버킷인 `car-360`, `vehicles` 등 public 경로는 제외 (`approval-required.md` 참조)

## 알림

- 텔레그램 운영 알림 발송 (결과 리포트, 오류 통보)

## 이미지 처리

- 배경 제거, WebP 변환, 리사이즈 (로컬 파일 대상)
