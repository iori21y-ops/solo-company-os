# 위임 작업 정의 템플릿

새로운 작업을 로컬 AI·n8n에 위임할 때 이 템플릿을 복사해서 작성한다.

---

## 작업명

{작업명}

## 목적

{이 작업이 왜 필요한지}

## 위험도 분류

아래 3단계로 분류한다. 판단이 애매하면 더 높은 단계로 분류.

| 단계 | 기준 문서 | 이 작업의 해당 여부 |
|------|-----------|-------------------|
| 🔴 위임 금지 | [security/delegation-blacklist.md](security/delegation-blacklist.md) | [ ] 해당 없음 확인 |
| 🟡 승인 필요 | [security/approval-required.md](security/approval-required.md) | [ ] 해당 없음 / [ ] 해당 → 승인 노드 삽입 |
| 🟢 자동 허용 | [security/auto-allowed.md](security/auto-allowed.md) | [ ] 해당 확인 |

> 분류 결과: 🔴 / 🟡 / 🟢 (하나만 선택)

## 입력

- 입력 데이터:
- 입력 경로/형식:

## 출력

- 출력 결과:
- 저장 위치:

## 실행 조건

- 트리거: (수동 / 스케줄 / 이벤트)
- 실행 주기:

## 승인 필요 시 텔레그램 메시지 형식

```
[승인 요청] {작업명}
대상: {대상}
건수: {N}건
[✅ 승인] [❌ 거절]
```

## 롤백 방법

{문제 발생 시 되돌리는 방법}

## 관련 문서

- [README.md](README.md)
- [../security.md](../security.md)
