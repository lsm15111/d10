# 0003. LLM은 OpenAI, DB는 RDS PostgreSQL로 한다

- 상태: 결정 (2026-10-29)
- 결정한 사람: PO
- 바꾸는 것: [ai-architecture.md](../design/ai-architecture.md) AI3, [target-architecture.md](../design/target-architecture.md) T1 · T3

## 맥락

AGENTS.md 4장은 LLM 공급자를 ADR로 하나만 정하라고 한다. 완성 구성 검증(target-architecture.md)에서 DB를 RDS로 할지, EC2 안의 PostgreSQL 컨테이너 + 백업으로 할지가 열려 있었다.

## 결정

- **LLM 공급자는 OpenAI 하나다.** 설명 · 추천 이유 · 임베딩을 OpenAI API로 받는다. SDK 호출은 `app/agent/llm.py` 한 곳에서만 한다.
- **작업별 모델 이름은 정하는 날 OpenAI 모델 목록으로 다시 확인해서** 이 ADR 아래에 적는다. 모델을 바꾸는 PR에는 eval 결과를 붙인다(AGENTS.md 4장).
- **운영 DB는 RDS PostgreSQL 17**(서울 리전)이다. 자동 백업을 켜고, 벡터 검색은 RDS의 pgvector로 한다. 로컬 개발과 CI는 지금처럼 PostgreSQL 컨테이너를 쓴다.

## 다른 안

- 다른 LLM 공급자 또는 여러 공급자: 프롬프트 · eval · 비용 관리가 공급자마다 따로 생긴다.
- EC2 안의 PostgreSQL 컨테이너 + 매일 `pg_dump` → S3: 가장 싸지만 백업 · 복구를 팀이 직접 하고, 서버를 잃으면 마지막 백업 뒤 데이터를 잃는다.

## 결과

- 시스템 구성도에 OpenAI API · RDS PostgreSQL을 적는다.
- 비용: RDS 가장 작은 크기(db.t4g.micro, 서울)는 월 약 $18(제3자 가격표, 확인 필요). OpenAI 호출은 사용량만큼 나온다. 하루 예산 · 호출 timeout은 jobs를 만들 때 정한다.
- 운영 연결 문자열 · OpenAI 키는 SSM Parameter Store에 둔다. `.env`는 커밋하지 않는다.
