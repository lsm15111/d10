# 완성 구성 검증 (시스템 구성도)

기준일 2026-10-29 · 상태: 제안 (T1 · T3 결정: [ADR 0003](../adr/0003-openai-rds.md)) · 그림: [system-config.svg](../architecture/system-config.svg) · 앞선 조사: [architecture-research.md](architecture-research.md)

## 결론

- **완성 구성:**
  - EC2 한 대 (Docker Compose: Caddy · Next.js · FastAPI · worker · Redis)
  - 관리형 서비스: RDS PostgreSQL(pgvector) · S3 · SES
  - 배포: GitHub Actions → ECR → SSM
  - 감시: CloudWatch
  - 밖: OpenAI API, 공공데이터 API
- **이 구성이 맞다.**
  - 앞선 조사의 '1단계: 상태를 서버 밖으로'를 끝낸 모양이다. 서버를 잃어도 DB · 파일이 남고, 배포에 SSH가 필요 없다.
  - 로드밸런서, 서버 두 대, ElastiCache는 넣지 않는다. 서버 두 대가 필요해지는 조건(AR13)이 오기 전에는 비용만 는다.
- **새로 확인한 사실:**
  - RDS PostgreSQL 17.11은 pgvector 0.8.2를 지원한다. RAG 2단계도 같은 DB에서 한다.
  - t4g.small은 2026-12-31까지 월 750시간 무료다.
  - SES는 서울 리전에서 쓸 수 있다. 처음에는 샌드박스(하루 200통, 확인된 주소에만)라서 운영 전에 해제를 요청해야 한다.

## 부품별 판정

| 부품 | 완성 구성 | 왜 | 다른 후보 |
| --- | --- | --- | --- |
| 서버 | EC2 t4g.small 1대 + Docker Compose | 가입 수백 명 · 동시 사용 수십 명 규모. 팀이 운영할 것이 가장 적다 | ECS Express Mode · ALB 2대: 무중단 배포나 장애 시간 요구가 생길 때(AR13). App Runner: 2026-04-30부터 새 고객을 받지 않는다 |
| 입구 | Caddy | HTTPS 인증서를 자동으로 받고 갱신한다. 설정은 이미 검증했다 | Nginx + certbot: 같은 일에 설정이 더 많다. ALB + ACM: 서버 두 대일 때 |
| 화면 | Next.js (standalone) | 로그인 쿠키로 서버에서 화면을 그려서 Node 서버가 필요하다 | S3 + CloudFront 정적 배포: 서버 렌더링을 못 한다 |
| API | FastAPI 하나 (모듈러 모놀리스) | 계산 엔진 · 에이전트 · 업무 규칙이 한 코드에 있다 | 예시 그림처럼 RAG용 FastAPI를 따로: 서비스 사이 호출 · 배포 · 인증 비용이 생긴다. 에이전트는 worker 안의 함수로 충분하다 |
| 느린 일 | worker (API와 같은 이미지, arq) | LLM · 기준 단가 수집 · 메일을 요청 밖에서 돌린다 | Celery: async 지원이 약하다. 바꿔야 하면 SAQ(AR2) |
| 큐 · 요청 제한 | Redis 컨테이너 | 지워져도 되는 값만 둔다. 작업 원장은 `jobs` 표다 | ElastiCache: 서버 두 대가 같은 카운터를 써야 할 때. 최소 월 약 $6(서버리스) ~ $9(가장 작은 노드) |
| DB | RDS PostgreSQL 17 | 자동 백업 · 시점 복구. pgvector 0.8.2라 벡터 검색도 같은 DB | EC2 컨테이너 + 매일 `pg_dump` → S3: 가장 싸지만 백업 · 복구를 직접 한다. 별도 벡터 DB(ChromaDB 등): 백업 · 권한 · 트랜잭션이 둘로 나뉜다 |
| 파일 | S3 비공개 버킷 | 서버를 잃어도 남는다. 올리기는 API를 거쳐 형식 검사 · 위치 정보 제거 뒤 S3에, 내려받기는 권한 확인 뒤 짧은 presigned URL | 서버 볼륨: 서버 한 대에 묶인다 |
| 메일 | SES (서울) | 가견적서 도착 · 실측 확인 같은 알림. worker가 보낸다 | 샌드박스 해제 전에는 확인된 주소에만 간다. 도메인 인증(DKIM)이 먼저다 |
| LLM | OpenAI API (ADR 0003) | 설명 · 추천 이유 · 임베딩. 숫자는 계산 엔진이 만든다 | Runpod · 자체 모델(예시 그림의 BGE-m3 · reranker): GPU 비용이 들고, 문서 수십 건 규모에 과하다 |
| 공공데이터 | 건축HUB · 조달청 가격정보 · 공휴일 | worker가 모아서 적용일 · 버전과 함께 저장한다 | — |
| 배포 | GitHub Actions → ECR → SSM Run Command | 키를 저장하지 않는다(OIDC). SSH 포트를 닫는다. 서버에서 빌드하지 않는다 | SSH 배포: 키 관리와 22번 포트가 생긴다. GHCR: 쓸 수 있지만 서버에 토큰이 필요하다. ECR은 서버 역할(IAM)로 받는다 |
| 비밀값 | SSM Parameter Store | `.env`를 서버에 손으로 두지 않는다 | — |
| 감시 | CloudWatch (로그 · 지표 · 알람) | 컨테이너 로그, CPU · 디스크, `/health/ready` 실패 알람 | Sentry: 오류 추적이 더 필요해지면 더한다 |
| 도메인 | 그림에서 뺌 (2026-10-30, 도메인 없이 시작) | HTTPS는 탄력적 IP + Let's Encrypt IP 인증서(6일짜리, 2026-01 정식) 또는 sslip.io 같은 무료 주소로 받는다. 도메인을 사면 그때 더한다 | `.kr`은 Route 53에서 살 수 없다 |

## 예시 그림(다른 팀)과 다른 곳

| 예시 | 믿집 | 이유 |
| --- | --- | --- |
| Nginx + React | Caddy + Next.js | 인증서 자동, 서버 렌더링 |
| FastAPI 백엔드 + FastAPI RAG | FastAPI 하나 + worker | 서비스를 나누는 비용이 크다. RAG는 `agent` 안의 함수 |
| ChromaDB | RDS PostgreSQL의 pgvector | DB 하나로 백업 · 권한 · 트랜잭션 |
| Script | worker 작업 | 수집 · 정리도 같은 작업 원장(`jobs`)으로 |
| Runpod (BGE-m3 · reranker) | LLM 공급자의 임베딩 | GPU 서버를 두지 않는다 |
| RDS MySQL | RDS PostgreSQL | pgvector · 기존 코드 |
| ElastiCache | Redis 컨테이너 | 지워져도 되는 값만 두고 서버가 한 대 |
| S3 | S3 | 같다 |

## 서버 메모리 (t4g.small 2GiB, 추정)

- Caddy 약 30MB, Next.js 약 200MB, FastAPI 프로세스 2개 약 400MB, worker 약 150MB, Redis 약 20MB → 합계 약 0.8GB
- 사진 한 장을 처리할 때 수백 MB를 더 쓴다. 동시 처리는 1장으로 막아 두었다(`files/images.py`).
- DB가 RDS로 나가서 2GiB로 된다. 시연 전 부하 시험(AR12)으로 확인한다.

## 비용 (대략, 확인 필요)

| 항목 | 값 |
| --- | --- |
| EC2 t4g.small | 2026-12-31까지 무료 체험. 공인 IPv4 월 약 $3.65 |
| RDS db.t4g.micro (서울) | 시간당 약 $0.025, 월 약 $18 (제3자 가격표) |
| S3 · SES · ECR · CloudWatch | 이 규모에서 월 몇 달러 |
| 프리 티어 | 2025-07-15 뒤에 만든 계정은 크레딧 방식($100 + 과제로 최대 $200, 6개월). 그 전 계정은 12개월 무료가 남아 있을 수 있다 |

## 정할 것

| | 질문 | 권장 |
| --- | --- | --- |
| T1 | DB를 RDS로 할지 | **결정: RDS** (2026-10-29, ADR 0003) |
| T2 | 저장소를 공개할지 | 공개면 GitHub의 무료 ARM 러너로 arm64 이미지를 빌드한다. 비공개면 에뮬레이션 빌드(느림) 또는 x86 서버 |
| T3 | LLM 공급자 · 모델 | **결정: OpenAI** (2026-10-29, ADR 0003). 작업별 모델은 정하는 날 모델 목록으로 확인 |
| T4 | 도메인 | 팀이 가진 도메인이 없으면 Route 53에서 산다 |

## 출처

- [RDS PostgreSQL 확장 버전 (17.11 · pgvector 0.8.2)](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html)
- [EC2 T4g (t4g.small 무료 체험 2026-12-31까지)](https://aws.amazon.com/ec2/instance-types/t4/)
- [SES 리전 · 할당량 (서울, 샌드박스 하루 200통)](https://docs.aws.amazon.com/general/latest/gr/ses.html), [SES 프로덕션 액세스 요청](https://docs.aws.amazon.com/ko_kr/ses/latest/DeveloperGuide/request-production-access.html)
- 프리 티어 변경: [Neowin](https://www.neowin.net/news/aws-free-tier-overhauled-new-users-get-200-in-credits-but-theres-a-catch/), [InfraTally](https://infratally.com/articles/aws-free-tier-2026/) (제3자 자료)
- ElastiCache 요금: [Upstash 정리](https://upstash.com/blog/aws-elasticache-pricing-explained-2026-full-cost-breakdown) (제3자 자료)
- RDS 서울 요금: [Spare Cores](https://sparecores.com/database/aws/db.t4g.micro), [Bytebase](https://www.bytebase.com/dbcost/rds/instance/db.t4g.micro/) (제3자 자료)
- ARM 러너: [GitHub 블로그](https://github.blog/news-insights/product-news/arm64-on-github-actions-powering-faster-more-efficient-build-systems/) (비공개 저장소 조건은 확인 필요)
- GitHub Actions → AWS 키 없이 배포(OIDC · SSM): [Zenn 예시](https://zenn.dev/rescuenow/articles/9facd2d4be02a1)
- 앞선 조사의 출처(App Runner · ECS Express Mode · arq · Caddy · uvicorn): [architecture-research.md](architecture-research.md)
