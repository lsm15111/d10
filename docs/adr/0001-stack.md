# 0001. 기본 스택: Next.js + FastAPI + PostgreSQL + Redis, Docker로 EC2 한 대

- 상태: 제안 (2026-10-29)
- 결정할 사람: 팀 전체

## 맥락

1차 범위는 도배·목공 견적, 실측, 공정표, 계약이다. 에이전트 3개(업체 추천, 가견적 설명, 공정표)가 들어가고, 금액·날짜는 계산 엔진이 만든다. 팀은 React와 Python(FastAPI)을 써 봤다. 시연까지 기간이 짧아 운영할 서비스 수를 줄여야 한다.

## 결정

| 영역 | 선택 | 이유 |
| --- | --- | --- |
| 웹 | Next.js 16 (App Router, TypeScript) | React 경험을 그대로 쓰고, 공개 페이지(업체 소개·가격 안내)를 서버에서 그릴 수 있다 |
| API | FastAPI 한 앱 (기능별 패키지) | 업무 API와 에이전트가 같은 언어(Python)라 LLM SDK·데이터 처리와 붙이기 쉽다 |
| DB | PostgreSQL 17 | 금액·날짜 제약(CHECK, FK), 견적 스냅숏용 JSONB, 나중에 검색(pg_trgm)·벡터(pgvector)를 DB 하나로 |
| 큐·캐시 | Redis 8 + arq | LLM 호출·기준 단가 수집·알림을 요청 밖에서 돌린다 |
| 배포 | Docker Compose, EC2 한 대, Caddy(HTTPS) | 서비스 6개를 파일 하나로 띄우고, 인증서를 자동으로 받는다 |

## 다른 안

- Kotlin·Spring core + FastAPI agent (GovBiz 방식): 경계는 분명하지만 언어 둘, 서비스 둘을 운영해야 한다.
- MySQL: 팀이 써 봤지만 JSONB·CHECK·범위 타입이 약하다.
- Vite SPA: 더 가볍지만 공개 페이지 SEO와 서버 렌더링을 따로 만들어야 한다.
- Kubernetes: 시연 단계에는 과하다.

## 결과

- Next 서버는 화면만 맡고 업무 로직·DB·LLM을 부르지 않는다(AGENTS.md 2장).
- 계산 엔진은 `backend/app/calc`에 Python 순수 함수로 만든다. 시안(mitjip-v6/js/calc.js)의 산식과 테스트 87개를 옮긴다.
- EC2 한 대에 DB까지 두므로 매일 백업이 필요하다. 운영 전환 때 RDS로 옮길지 다시 정한다.
- LLM 공급자는 별도 ADR로 정한다.
