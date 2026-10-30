# 아키텍처 조사 (구조 · 작업 큐 · 로드밸런싱)

기준일 2026-10-29 · 상태: 조사 · 앞선 제안: [app-structure.md](app-structure.md), [ai-architecture.md](ai-architecture.md), [ADR 0001](../adr/0001-stack.md) · 그림: [system-v3.2.svg](../architecture/system-v3.2.svg)

## 결론

- **구조는 바꾸지 않는다.** FastAPI 앱 하나를 기능별 패키지로 나눈 모듈러 모놀리스가 이 팀 · 이 단계에 맞다. 2023~2026 자료도 같은 쪽이다.
  - Kraken은 파이썬 모놀리스 하나를 import-linter로 층을 나눠 쓰고, 2026년 글에서도 모놀리스 하나로 배포한다.
  - GitHub는 엔지니어 1,000명 이상이 Rails 모놀리스 하나에서 일한다.
  - Fowler · Newman · ThoughtWorks 모두 '처음부터 마이크로서비스'를 말린다.
- **더 나은 '구조'는 찾지 못했다. 고칠 것은 운영 세부다.** 세 가지를 권한다.
  1. **작업 큐:** arq는 2025-10-18부터 유지보수 전용이다. `jobs` 표를 원장 겸 outbox로 쓰는 설계는 맞다(Brandur의 'job drain'과 같은 모양). 다만 arq 동작과 부딪히는 구멍이 셋 있다. 이것을 고치고, arq는 `queue.py` · `worker.py` 두 파일 안에 가둬서 나중에 SAQ로 바꾸기 쉽게 둔다.
  2. **경계 검사:** import-linter(D8)에 ruff `TID251`을 더한다. `arq` · Redis 연결 · LLM SDK · S3 SDK를 정해진 파일에서만 import하게 막는다. ruff는 이미 쓰므로 새 의존성이 없다.
  3. **한 대 다지기:** Caddy 재시도 · keepalive · 본문 한도, 우아한 종료, uvicorn 프로세스 2개, argon2 해시를 이벤트 루프 밖으로, DB 백업.
- **로드밸런싱 판정:** 지금 로드밸런서 + 서버 여러 대는 필요 없다. 수백 명 규모에서 위험은 트래픽보다 아래 셋이다.
  - 서버 한 대를 잃으면 DB · 파일도 같이 잃는다(백업 미정).
  - 배포 · 재시작 때 요청이 끊긴다(Caddy 재시도 꺼짐).
  - 업로드 크기 · 응답 시간에 한도가 없다.
  - 이 셋은 설정과 백업으로 막는다. 두 번째 서버는 파일(S3)과 DB(RDS)를 서버 밖으로 옮긴 뒤에야 의미가 있다.
- **가정:** 실제 트래픽 숫자는 없다. 가입 수백 명, 동시에 쓰는 사람 수십 명 이하, 가장 무거운 요청은 사진 · 도면 업로드(최대 20MB)로 본다. 숫자가 필요하면 부하 시험으로 잰다(AR12).

## 지금 구조 판정

| 항목 | 판정 | 근거 |
| --- | --- | --- |
| 모듈러 모놀리스 (FastAPI 하나 · 기능 패키지) | 맞다 | Fowler MonolithFirst: 처음에는 서비스 경계를 맞게 긋기 어렵다. Newman: 마이크로서비스는 기본값이 아니다. GovBiz 회고와도 맞다 |
| 기능 안 `router → service → repository` | 맞다 · 얇게 | Cosmic Python 2장: 단순 CRUD에는 repository가 필요 없다. AGENTS.md 7장 '필요한 것만'과 같다 |
| `calc` 순수 함수 코어 | 맞다 | 헥사고날의 '안쪽'. DB 없이 테스트한다(Cockburn) |
| `jobs` 표 = 원장 + outbox, 실행은 arq | 모양은 맞다 · 세부 3곳 고침 | 같은 트랜잭션에 행을 쓰고 commit 뒤 큐로 보낸다. Brandur 'Transactionally Staged Job Drains'와 같다. 구멍은 '작업 큐' 장 |
| Next 읽기는 Server Component → API, 쓰기는 브라우저 → `/api` (D9) | 맞다 | Next 데이터 보안 문서가 '다른 언어를 쓰는 백엔드 팀'이면 HTTP API 방식을 든다. Server Action은 본문 1MB, 한 번에 하나씩 실행된다 |
| 서버 세션 (PostgreSQL) | 맞다 | 서버가 여러 대가 돼도 sticky session이 필요 없다 |
| Redis = 큐 · 로그인 제한 (원본 아님) | 맞다 | Redis가 죽어도 로그인은 된다(제한만 풀림). 작업은 `jobs` 표가 원장이라 다시 넣을 수 있다 |
| EC2 한 대 · Compose · Caddy | MVP에 맞다 · 빈 곳 있음 | 빈 곳: 백업, 재시도, keepalive, 본문 한도, 우아한 종료, 이미지 빌드 위치 |
| 파일을 로컬 볼륨(`files-data`)에 | 한 대에서만 맞다 | 두 번째 서버 전에 S3로 옮긴다. `files/storage.py` 경계가 이미 있다 |

- **app-structure.md 출처 하나를 고쳐 읽는다:** Netflix Dispatch 저장소는 2025-09-03에 보관(archived)됐다. 폴더 모양 참고로만 쓴다.

## 다른 구조 비교

| 후보 | 언제 이기나 | 우리 판정 |
| --- | --- | --- |
| 마이크로서비스 | 따로 배포하는 팀이 여럿, 부분마다 확장 요구가 다름, 자동 배포 · 관측 · 빠른 서버 준비가 이미 있음(Fowler 선행 조건) | 아니다. GovBiz에서 비용이 가장 컸다. Prime Video 모니터링 팀 · Istio도 합쳐서 비용을 줄였다 |
| 헥사고날 전면 (모든 의존에 port) | 같은 업무를 UI · CLI · 배치 · 테스트가 모두 부르고, 외부 연동이 많고 자주 바뀜 | 경계만. LLM(`agent/llm.py`), 파일 저장(`files/storage.py`), 공공 API(`client.py`). DB에는 port를 두지 않는다 |
| 클린 · 어니언 전면 (UseCase · DI 컨테이너) | 업무 규칙이 CRUD보다 훨씬 크고, 큰 팀이 오래 유지 | `calc`만 |
| 수직 슬라이스 (요청마다 폴더) | 기능 하나에 요청이 많고 요청끼리 거의 안 겹침 | 이름만. service 함수를 유스케이스 이름으로(이미 채택) |
| DDD-lite · Cosmic Python (Unit of Work · message bus) | 도메인 이벤트가 많고 집합체 규칙이 복잡 | Unit of Work 생각만: 맨 바깥 service가 한 번 commit(app-structure 규칙 3). message bus는 안 쓴다 |
| CQRS | 읽기와 쓰기의 모양 · 부하가 크게 다름 | 읽기 전용 조회 함수만. 읽기 DB · 이벤트 소싱 없음. Fowler도 '위험한 복잡도'라고 한다 |
| 이벤트 기반 (RabbitMQ · Kafka 브로커) | 여러 서비스 · 팀이 같은 사건에 따로 반응 | 아니다. `jobs` 표로 충분하다 |
| BFF (Next가 화면별 API를 따로 만듦) | 앱 · 웹처럼 화면 종류마다 API 모양이 크게 다르고 프런트 팀이 따로 | 지금처럼 얇게. Server Component 읽기가 이미 작은 BFF다. 업무 로직은 넣지 않는다 |
| Server Action으로 쓰기 | Next가 데이터 주인이거나, JS 없이 도는 폼이 중요 | 아니다(D9 유지). 본문 1MB, 한 번에 하나씩 실행, 공개 POST 주소라 매번 권한 검사, 여러 대면 암호 키를 맞춰야 한다 |
| Next가 DB를 직접 (Data Access Layer) | 백엔드도 TypeScript이고 팀이 하나 | 아니다. 계산 엔진 · 에이전트가 Python이다(AGENTS.md 2장) |
| tRPC | 프런트와 백엔드가 모두 TypeScript | 해당 없음. OpenAPI → TS 타입(`schema.d.ts`)이 같은 일을 한다 |
| 서버리스 (Lambda + Lambda Web Adapter) | 트래픽이 거의 0이거나 크게 튀고, 운영할 사람이 없음 | 아니다. LLM 작업이 길고, DB 연결 풀 · Redis가 있고, 2025-08-01부터 cold start(INIT) 시간도 요금에 든다 |
| 모듈 도구 (Spring Modulith · Packwerk) | 자바 · 루비 | 해당 없음. 파이썬에서는 import-linter가 같은 자리다 |

## 작업 큐

### arq 지금 상태

- **버전:** 0.28.0 (2026-04-16). 우리 lock도 0.28.0이다. 2025년 뒤 릴리스는 파이썬 버전 지원 같은 관리 작업뿐이다.
- **유지보수 전용:** 2025-10-18 samuelcolvin이 이슈 #510을 열고 고정했다. 심각한 보안 문제만 고치고 새 수정은 기대하지 말라고 했다. 저장소는 보관하지 않는다.
- **redis-py 상한:** arq가 `redis<6`으로 묶는다. 우리 lock은 redis 5.3.1이다. Redis 8 서버와는 상관없고, 파이썬 클라이언트만 6으로 못 올린다.
- **우리가 기대는 동작 (arq 문서 v0.28):**
  - 적어도 한 번 실행한다. 같은 작업이 두 번 돌 수 있다.
  - 같은 `_job_id`는 앞 작업이 끝나고 **결과가 지워질 때까지** 다시 넣을 수 없다. 넣으면 `None`이 돌아온다. 결과 보관(`keep_result`) 기본값은 3600초다.
  - 종료 신호(SIGTERM)를 받으면 돌던 작업을 **바로 취소**하고 큐에 남긴다. `job_completion_wait`(기본 0초)만큼 기다릴 수 있다.
  - 기본값: `job_timeout` 300초, `max_tries` 5, `health_check_interval` 3600초.
  - cron은 기본 `unique=True`라 worker가 여럿이어도 한 번만 돈다.

### 우리 설계와 arq가 부딪히는 곳

| 구멍 | 왜 생기나 | 고칠 것 |
| --- | --- | --- |
| 다시 넣기가 1시간 막힘 | 1분 cron이 `_job_id = jobs.id`로 다시 넣어도, 앞 실행 결과가 1시간 남아 있으면 조용히 `None` | 작업 함수에 `keep_result=0`(결과는 `jobs` 표에 둔다) 또는 `_job_id = f"{jobs.id}:{attempt}"` |
| `running`에 갇힘 | `queued → running`을 차지한 뒤 worker가 죽으면 행이 `running`으로 남는다. arq가 다시 돌려도 조건부 UPDATE가 실패해서 건너뛴다 | `lease_until` 열을 두고, cron이 `running AND lease_until < now()`도 `queued`로 되돌린다. `CancelledError`를 받으면 바로 `queued`로 되돌린다 |
| 배포 때 유료 호출이 버려짐 | `docker compose up`이 worker를 멈추면 arq가 하던 LLM 호출을 바로 취소하고 처음부터 다시 돈다 | `job_completion_wait = 60`, compose `stop_grace_period: 90s`. LLM 호출 timeout은 `job_timeout`보다 짧게 |

- **판정:** 세 곳을 고치면 지금 설계(commit 뒤 바로 넣기 + 1분 cron 다시 넣기 + 상태 선점 + 두 번 돌아도 한 번 반영)로 충분하다. 1분 cron은 outbox의 'polling publisher' 자리다. commit과 enqueue 사이에 프로세스가 죽어도 1분 안에 다시 넣는다.

### 다른 도구

| 도구 | 최신 (날짜) | 언제 이기나 | 판정 |
| --- | --- | --- | --- |
| arq | 0.28.0 (2026-04-16), 유지보수 전용 | 지금 돌고 있고 Redis가 이미 있음 | 당분간 유지. `<0.29`로 묶고 위 세 곳을 고친다 |
| SAQ | 0.26.5 (2026-10-29) | arq와 비슷한 API로 계속 관리되는 도구가 필요할 때. Redis · Postgres 둘 다 되고 heartbeat · 멈춘 작업 정리가 들어 있다 | **바꾼다면 1순위.** 기본값 `timeout=10`초 · `retries=1`은 LLM 작업에 맞게 바꿔야 한다 |
| pgqueuer | 1.6.0 (2026-10-11) | 작업 경로에서 Redis를 빼고 업무 행과 큐 행을 같은 트랜잭션에 넣고 싶을 때(asyncpg, `SKIP LOCKED` + LISTEN/NOTIFY, cron) | 2순위. SQLAlchemy 세션과 같은 연결로 넣는 방법은 확인 필요 |
| procrastinate | 3.10.0 (2026-09-23) | psycopg3 · Django를 쓰는 팀 | 아니다. asyncpg 옆에 드라이버가 하나 더 생긴다 |
| Taskiq | 0.13.0 (2026-09-26) | FastAPI식 의존성 주입, NATS · Kafka 같은 여러 브로커 | 보류. PyPI 표시가 아직 Alpha, Postgres 브로커는 외부 패키지 |
| Celery · Dramatiq | Celery 5.6.3 (2026-03-26), Dramatiq 2.2.1 (2026-09-02) | 동기 코드가 많고 큰 생태계가 필요 | 아니다. 우리 코드는 async이고 Celery는 async 지원이 약하다 |
| PGMQ | 파이썬 클라이언트 1.1.4 (2026-09-20) | SQS 같은 메시지 큐를 Postgres 안에 | 아니다. worker를 다시 만들어야 한다 |
| DBOS · Hatchet · Temporal | DBOS 3.4.0, Hatchet SDK 1.43.2 (2026-10-28) | 여러 단계로 길게 도는 에이전트 흐름을 끊겨도 이어서 돌려야 할 때 | 지금은 과하다. 에이전트 흐름이 여러 단계가 되면 DBOS(Postgres만 씀)를 본다 |

### 권장

1. arq를 유지하고 `arq>=0.28,<0.29`로 묶는다.
2. arq를 import하는 곳은 `app/queue.py`(넣기)와 `app/worker.py`(등록)뿐으로 둔다. 기능 코드는 `queue.enqueue(job_id)` 같은 우리 함수만 부른다. ruff로 검사한다(다음 장).
3. 위 세 구멍을 `jobs` 기능을 만들 때 같이 고친다.
4. **바꿀 조건:** arq 보안 문제가 고쳐지지 않음, redis-py 6이 필요함, 새 파이썬에서 깨짐. 이때 SAQ로 옮긴다. 2번을 지키면 두 파일만 바뀐다.

## 경계 검사 도구

| 도구 | 상태 (날짜) | 판정 |
| --- | --- | --- |
| import-linter | 2.15 (2026-09-04), grimp 3.18 기반. 계약: layers(`containers`), independence, forbidden, protected, acyclic siblings | **채택(D8).** app-structure.md의 계약 3개 그대로 |
| ruff `TID251` (banned-api) | ruff에 들어 있음. 정해진 이름을 프로젝트 전체에서 막고, 파일별로 풀 수 있다 | **더한다.** 외부 경계 import 위치를 고정한다. `importlib`로 피할 수 있어서 '실수 막기'용이다 |
| Tach | 0.35.3 (2026-10-06). gauge-sh에서 tach-org로 옮겼고, 옮기기 전 한동안 관리가 끊겼다 | 보류. 공개 interface 강제가 필요할 때 다시 본다 |
| PyTestArch | 5.1.0 (2026-10-24) | 필요 없음. 규칙을 테스트 코드로 쓰는 방식이다 |
| pytest-archon | 0.0.7 (2025-09-19), 활동 적음 | 아니다 |
| deply | 1.3.0 (2026-10-23) | 필요 없음 |

- **Shopify Packwerk 회고(2024)에서 배울 것:** 위반이 0개여도 실행하면 깨질 수 있었다. 그래서 '그 패키지를 혼자 띄우고 테스트할 수 있나'로 경계를 쟀다. 우리도 규칙 수를 늘리기보다 기능별 통합 테스트로 확인한다.
- **Kraken에서 배울 것:** 말로만 정한 층 규칙은 계속 깨졌다. CI에 일찍 넣을수록 쉽다. 예외 목록(`ignore_imports`)은 갚아 갈 빚 목록으로 쓴다.
- **ruff 설정 예 (적용 안 함):** 하위 모듈까지 막히는지는 확인 필요라서 쓰는 이름을 모두 적는다.

```toml
[tool.ruff.lint]
extend-select = ["TID251"]

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"arq".msg = "arq는 app/queue.py · app/worker.py에서만 쓴다"
"arq.connections".msg = "arq는 app/queue.py · app/worker.py에서만 쓴다"
"redis.asyncio".msg = "Redis 연결은 app/queue.py에서만 만든다 (redis.exceptions는 괜찮다)"
# LLM SDK(AI3로 정한 것)는 app/agent/llm.py에서만, boto3는 app/files/storage.py에서만

[tool.ruff.lint.per-file-ignores]
"app/queue.py" = ["TID251"]
"app/worker.py" = ["TID251"]
```

## 로드밸런싱 · 확장

### 판정

- **지금은 '로드밸런싱'보다 '한 대 다지기'가 맞다.** Caddy는 이미 리버스 프록시이고, 필요하면 같은 서버의 컨테이너 여러 개에 나눠 보낼 수도 있다. 지금은 위쪽(upstream)이 하나씩이라 나눌 것이 없다.
- **헬스체크의 쓸모가 다르다.** 위쪽이 하나면 Caddy 능동 헬스체크는 '실패한 서버를 빼는' 일을 못 한다(뺄 곳이 없다). 대신 재시작 동안 기다려 주는 `lb_try_duration`이 효과가 크다.
- **LB 헬스체크에는 `/health/live`를 쓴다.** `/health/ready`는 Redis까지 본다. LB가 ready를 보면 Redis만 죽어도 API 전체가 빠진다. 로그인 제한을 Redis 없이 돌게 만든 설계와 어긋난다. ready는 감시 · 알림에 쓴다.

### 상황별

| 상황 | 지금 어떻게 되나 | 고치는 법 | 언제 |
| --- | --- | --- | --- |
| 배포 · 재시작 (api · web을 다시 만듦) | 그동안 Caddy가 바로 502를 준다(`lb_try_duration` 기본 0) | `lb_try_duration 10s`: 연결 실패는 다시 시도하고, GET은 응답 실패도 다시 시도한다 | 지금 |
| 쉬던 연결을 다시 쓰다 끊김 | Caddy는 위쪽 연결을 2분 열어 두고, uvicorn은 5초 뒤 닫는다. 드물게 POST가 502(Caddy 문서 경고) | Caddy `keepalive 4s`(위쪽보다 짧게). Node 기본 5초는 확인 필요. 웹은 standalone의 `KEEP_ALIVE_TIMEOUT`으로도 늘릴 수 있다 | 지금 |
| 큰 · 느린 업로드 | Caddy 본문 한도 없음(기본값 문서에 없음, 확인 필요). Starlette는 파일을 임시 디스크에 다 받은 뒤 앱이 크기를 본다 | `/api`에 `request_body max_size 25MB`. Starlette 1.6부터 `max_body_size`가 있다(FastAPI에서 쓰는 방법은 확인 필요) | 지금 |
| 응답이 안 옴 | Caddy 응답 헤더 timeout 없음 | `response_header_timeout 60s` (LLM은 worker라 API는 빨라야 한다) | 지금 |
| 로그인이 몰림 | argon2(64MiB · t=3 · p=4)가 async 함수 안에서 돌아, 그동안 이 프로세스의 모든 요청이 멈춘다 | 스레드로 넘기고 동시 개수를 2로 제한한다(64MiB × 개수) | 지금 |
| CPU 하나가 꽉 참 | uvicorn 프로세스 1개 = 코어 1개 | `--workers 2` (2 vCPU). 사진 처리 한도(`images._SLOTS = 2`)는 프로세스마다라 같이 2배가 된다 → 메모리 표 | 지금 |
| api가 죽음 | 운영은 `restart: unless-stopped`로 다시 뜬다. `--workers`를 쓰면 uvicorn이 죽은 자식 프로세스도 다시 띄운다 | 그대로 | — |
| api가 멈춤 (떠 있지만 응답 없음) | healthcheck가 unhealthy로 표시만 한다. Docker는 unhealthy를 재시작하지 않는다 | 바깥 업타임 감시 + 알림. 자동 재시작 도구는 필요해지면 정한다 | 다음 |
| worker가 죽음 · 멈춤 | healthcheck 없음 | `arq --check` healthcheck + `health_check_interval = 60` | jobs 만들 때 |
| 배포 중 LLM 작업 | 바로 취소되고 처음부터 다시 돈다 | `job_completion_wait = 60`, `stop_grace_period: 90s` | jobs 만들 때 |
| LLM 공급자가 느림 · 실패 | 아직 없음 | 호출 timeout < `job_timeout`(300초). 다시 하기는 `jobs` 표의 시도 수로. 실패하면 "설명을 만들지 못했어요" | jobs 만들 때 |
| Redis가 죽음 | 로그인 제한이 풀린다(의도). 큐가 멈춘다. `/health/ready`가 503 | `jobs` 표가 원장이라 Redis가 돌아오면 1분 cron이 다시 넣는다. LB는 `/health/live` | 지금 (규칙) |
| DB 연결이 모자람 | 프로세스마다 기본 5 + 10. api 15 + worker 15(worker가 DB를 쓰기 시작하면) = 30 | pool 크기를 적어 두고 아래 표로 센다 | 다음 |
| migration이 틀림 | `migrate`가 실패하면 api가 안 뜬다 | CI에서 up → down → up과 `alembic check`. 지우는 변경은 두 번에 나눈다(더하기 → 옮기기 → 지우기) | CI 만들 때 |
| 디스크가 참 | DB · 파일 · Redis · 이미지가 한 디스크 | 디스크 사용률 알림, 오래된 이미지 정리 | 다음 |
| EC2 · 디스크를 잃음 | DB · 파일 · 세션을 모두 잃는다. 백업 미정(README) | 매일 EBS 스냅숏(DLM) + 매일 `pg_dump` → S3. 복구를 한 번 해 본다 | **실제 사용자 받기 전** |
| AZ · 리전 장애 | 대응 없음 | MVP에서는 받아들이고 적어 둔다. 필요해지면 RDS Multi-AZ | 바꿀 조건 |
| EC2에서 이미지 빌드 | 2GiB에서 `next build`가 메모리 부족일 수 있다(확인 필요). 빌드하는 동안 서비스도 느려진다 | CI에서 빌드 → 레지스트리 → EC2는 받기만. t4g(ARM)이면 arm64 이미지로 빌드 | 다음 |
| 사용자가 계속 늘어남 | 서버 한 대 | 아래 '단계'의 바꿀 조건 | 바꿀 조건 |

### 프로세스 · 연결 · 메모리

- **uvicorn 프로세스 방식:**
  - uvicorn 0.30(2024-05)부터 `--workers`가 자식 프로세스를 감시하고 죽으면 다시 띄운다.
  - `uvicorn.workers`(Gunicorn용)는 사라질 예정이고 `uvicorn-worker` 패키지로 옮겼다. 우리는 Gunicorn을 쓰지 않는다.
  - FastAPI 문서: 오케스트레이터(k8s · ECS)를 쓰면 컨테이너마다 프로세스 1개, 'Compose로 서버 한 대'면 컨테이너 안에 여러 worker가 맞다. 우리는 뒤쪽이다.
  - 종료 timeout(`--timeout-graceful-shutdown`) 기본값이 없어서, Docker가 10초 뒤 강제로 끈다. 20초로 정하고 `stop_grace_period`를 30초로 둔다.
- **DB 연결 수:** PostgreSQL `max_connections`는 보통 100이고 관리자용 3개를 남긴다. migrate · psql · 백업 몫도 남긴다.

| 구성 | 프로세스 | 프로세스마다 (pool + overflow) | 최대 연결 |
| --- | --- | --- | --- |
| 지금: api 1 + worker 1 | 2 | 5 + 10 | 30 |
| 권장: api `--workers 2` + worker 1 | 3 | 5 + 10 | 45 |
| 서버 두 대, 각각 위와 같음 | 6 | 5 + 10 | 90 (한도에 가까움) |
| 서버 두 대 + pool 5 + 5 | 6 | 5 + 5 | 60 |

- **메모리 (추정):** 사진 한 장 처리가 수백 MB를 쓸 수 있다(images.py 주석). `--workers 2`면 동시에 4장이다. 2GiB 서버에서는 `_SLOTS`를 1로 줄이거나 4GiB로 올린다. argon2도 동시에 64MiB × 개수다.

### 제안 설정 (적용 안 함)

- **Caddyfile:**

```caddyfile
{
	servers {
		timeouts {
			read_header 10s
		}
	}
}

{$DOMAIN} {
	encode zstd gzip

	handle_path /api/* {
		# 도면 20MB + 여유. 넘으면 413
		request_body {
			max_size 25MB
		}
		reverse_proxy api:8000 {
			# api가 다시 뜨는 동안 10초까지 기다렸다 넘긴다 (연결 실패 · GET만 다시 시도)
			lb_try_duration 10s
			transport http {
				# uvicorn(5초)보다 먼저 쉬는 연결을 닫는다
				keepalive 4s
				response_header_timeout 60s
			}
		}
	}

	handle {
		reverse_proxy web:3000 {
			lb_try_duration 10s
			transport http {
				keepalive 4s
			}
		}
	}
}
```

- **API 실행 (`backend/Dockerfile` prod CMD):** `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2 --proxy-headers --forwarded-allow-ips "*" --timeout-graceful-shutdown 20`
- **compose:** api `stop_grace_period: 30s`, worker `stop_grace_period: 90s` + `healthcheck: ["CMD", "arq", "--check", "app.worker.WorkerSettings"]`, web에도 healthcheck.
- **worker:** `job_completion_wait = 60`, `health_check_interval = 60`, `keep_result = 0`, `max_tries`는 `jobs` 표의 시도 수와 맞춘다.
- **DB 엔진:** `pool_size=5, max_overflow=5, pool_timeout=10`을 적어 둔다.
- **argon2:** `anyio.to_thread.run_sync(..., limiter=CapacityLimiter(2))`. anyio는 Starlette가 이미 쓴다.

### 단계 (지금 · 다음 단계 · 바꿀 조건)

| 단계 | 할 일 | 비용 | 넘어갈 조건 |
| --- | --- | --- | --- |
| 0. 지금: 한 대 다지기 | 위 제안 설정, argon2 스레드, 백업(DLM + `pg_dump` → S3), CI에서 이미지 빌드 | 거의 0 (스냅숏 · S3 몇 달러) | — |
| 1. 다음: 상태를 서버 밖으로 | 파일 → S3(`files/storage.py`만 바꿈). DB → RDS 또는 지금 백업 유지. 업타임 감시 · 오류 알림 | RDS 소형 월 $12~18 (제3자 자료, 확인 필요) | 실제 고객 · 업체를 받기 시작할 때 |
| 2. 바꿀 조건이 오면: 두 대 이상 | ALB(+ACM 인증서) 뒤에 같은 이미지 2대, 또는 ECS Express Mode. Redis → ElastiCache(Valkey). migrate는 배포 단계 하나로. Next `deploymentId` | ALB 최소 월 약 $22 + 서버 1대 | 아래 중 하나: 배포 중 끊김을 받아들일 수 없다 / CPU가 팀이 정한 값(예: 70%)을 오래 넘는다 / 서버 한 대 장애 시간을 받아들일 수 없다 |
| 3. 연결 · 데이터 | PgBouncer 또는 RDS Proxy. 시점 복구(PITR: RDS 또는 WAL-G) | — | DB 연결이 한도의 70%를 넘는다 / 하루치 데이터 손실도 안 된다 |

- 한 서버 안에서 무중단 배포만 원하면 2단계 전에 docker-rollout(v0.14, 2026-07)을 볼 수 있다. 서비스를 2배로 띄우고 healthcheck가 통과하면 옛 것을 지운다. Caddy와 같이 쓰는 예는 문서에 없어서 확인 필요다.

### 호스팅 선택지

가격은 us-east-1 기준이다. 서울 리전은 다르다(확인 필요).

| 선택지 | 비용 (확인된 것) | 맞는 때 | 판정 |
| --- | --- | --- | --- |
| EC2 한 대 + Compose + Caddy (지금) | t4g.small(2 vCPU · 2GiB)은 2026-12-31까지 월 750시간 무료. 공인 IPv4는 시간당 $0.005(월 약 $3.65). 무료가 끝난 뒤 요금은 확인 필요 | 시연 · MVP | 유지 |
| Lightsail | 2GB $12/월, 4GB $24/월(IPv4 포함), LB $18/월, DB 1GB $15/월 | 월 요금이 고정이면 좋을 때 | 비슷하다. 옮길 이유가 약하다 |
| ECS Express Mode (Fargate + ALB) | 추가 요금 없음, Fargate · ALB 값만. ALB는 시간당 $0.0225 + LCU | 컨테이너 여러 개를 관리형으로 쓰고 자동 확장 · 배포가 필요할 때 | 바꿀 조건이 오면 1순위 |
| App Runner | 2026-04-30부터 새 고객을 받지 않는다 | — | 못 쓴다 |
| Elastic Beanstalk | 추가 요금 없음 | Beanstalk 경험이 있을 때 | 필요 없음 |
| Fly.io · Render · Railway | Fly 1GB 머신 $6.70, Postgres $38부터. Render 무료 Postgres는 30일 뒤 만료. Railway Hobby $5 | AWS 밖이어도 될 때 | AWS로 정했으면 보류 |
| Kamal 2 (배포 도구) | 무료 | 서버 여러 대에 같은 방식으로 무중단 배포 | 두 대 이상이 되면 후보. Compose + Caddy를 바꿔야 해서 지금은 아니다 |

### 두 번째 서버를 붙이면 깨지는 것

| 것 | 지금 | 두 대가 되려면 |
| --- | --- | --- |
| 올린 파일 | 서버 디스크(`files-data`) | S3. 올리기는 지금처럼 API를 거친다(형식 검사 · EXIF 제거 유지). 내려받기는 권한 확인 뒤 짧은 presigned URL |
| DB · Redis | 앱과 같은 서버의 컨테이너 | RDS · ElastiCache처럼 서버 밖으로 |
| 로그인 세션 | PostgreSQL | 그대로 된다 |
| migration | `compose up`마다 `migrate`가 돈다 | 두 서버가 동시에 돌리면 겹친다. 배포 단계에서 한 번만 돌린다 |
| arq cron | `unique=True` | 그대로 된다. 작업은 두 번 돌아도 한 번 반영되게 만든다 |
| HTTPS 인증서 | Caddy 볼륨 | ALB + ACM으로 옮기거나, Caddy들이 같은 저장소를 쓰게 한다 |
| Next.js | 한 대 | 같은 이미지 하나를 모든 대에 쓴다. `deploymentId`(버전이 섞일 때 새로고침). 캐시는 대마다 따로인데 우리는 쿠키를 읽는 동적 화면이라 영향이 작다. Server Action 키는 Server Action을 안 써서 영향 없음 |
| 로드밸런서 헬스체크 | — | `/health/live` |

## 위험한 곳

| # | 곳 | 문제 | 고칠 것 | 급함 |
| --- | --- | --- | --- | --- |
| 1 | `README.md` 'EC2 운영', `compose.yaml` `db-data` | DB 백업이 없다. DB가 앱과 같은 디스크에 있다 | DLM 매일 스냅숏 + 매일 `pg_dump` → S3, 복구 연습 1회 | 실제 사용자 전 |
| 2 | `infra/caddy/Caddyfile` | 재시도 꺼짐(배포 때 502), keepalive 2분 vs uvicorn 5초, 본문 한도 · 응답 timeout 없음 | 위 제안 Caddyfile | 지금 |
| 3 | `backend/app/auth/service.py` 38 · 93 · 103행 | argon2 `hash` · `verify`가 async 함수 안에서 이벤트 루프를 막는다 | 스레드로 넘기고 동시 2개 제한 | 지금 |
| 4 | `backend/Dockerfile` 27행 | uvicorn 1 프로세스, 종료 timeout 없음 | `--workers 2 --timeout-graceful-shutdown 20` | 지금 |
| 5 | `compose.yaml` api · worker · web | worker · web healthcheck 없음, `stop_grace_period` 기본 10초 | 제안 compose 값 | 지금 |
| 6 | `backend/pyproject.toml` 13행 `arq>=0.28` | 유지보수 전용인데 상한이 없다 | `arq>=0.28,<0.29` | 지금 (한 줄) |
| 7 | `backend/app/worker.py` (jobs 설계) | 결과 보관 1시간 동안 다시 넣기 막힘, `running` 갇힘, 종료 때 바로 취소 | `keep_result=0`, `lease_until`, `job_completion_wait` | jobs 만들 때 |
| 8 | `backend/app/main.py` 62~77행 `/health/ready` | Redis까지 봐서, LB가 이것을 보면 Redis 장애가 전체 장애가 된다 | LB는 `/health/live`, ready는 감시용 | 두 대 때 |
| 9 | `backend/app/files/storage.py`, `files/router.py` 42~50행 | 로컬 디스크 + `FileResponse`라 서버 한 대에 묶인다. `save()`는 async 흐름에서 동기 쓰기(20MB까지) | S3로 바꿀 때 같이 고친다 | 다음 |
| 10 | `backend/app/files/images.py` 22행 `_SLOTS = 2` | 프로세스마다 2장이라 `--workers 2`면 4장 | 2GiB 서버면 1로 | `--workers`와 같이 |
| 11 | `backend/app/db.py` 20~24행 | pool 크기가 기본값에 숨어 있다 | 값을 적고 위 표로 센다 | 다음 |
| 12 | `frontend/next.config.ts` 11행 `proxyClientMaxBodySize` | 이 값은 `proxy.ts`(Next 16에서 middleware 새 이름)가 있을 때만 쓰인다. 지금은 효과가 없다. 나중에 `proxy.ts`를 만들면 한도를 넘는 본문이 **오류 없이 잘린다** | 주석을 고치거나 지운다. `proxy.ts`를 만들면 `/api`는 matcher에서 뺀다 | 낮음 |
| 13 | `compose.yaml` 46~56행 `migrate` | `up`마다 돈다. 두 대면 동시에 돈다 | 배포 단계 하나로 | 두 대 때 |
| 14 | `README.md` 142행 이미지 빌드 위치 미정 | EC2에서 빌드하면 메모리 부족 · 서비스 느려짐 | CI 빌드 → 레지스트리 | 다음 |
| 15 | `compose.prod.yaml` 5행 `caddy:2.10-alpine` | 지금은 2.11.x | 올릴 때 Caddyfile 다시 확인 | 낮음 |
| 16 | `backend/Dockerfile` 27행 `--forwarded-allow-ips "*"` | 8000번을 밖에 열면 아무나 IP를 속일 수 있다. 운영은 안 열려 있고 Caddy가 받은 값을 버린다 | 그대로 두되 8000번을 밖에 열지 않는 규칙을 적는다 | 낮음 |

## 정할 것

| | 질문 | 권장 |
| --- | --- | --- |
| AR1 | 구조 | 모듈러 모놀리스 유지. ADR 0001에 이 문서를 근거로 단다 |
| AR2 | 작업 큐 도구 | arq 유지 + `<0.29`. 바꿀 조건이 오면 SAQ |
| AR3 | arq를 쓰는 곳 | `app/queue.py` · `app/worker.py`만. ruff `TID251`로 검사 |
| AR4 | `jobs` 표에 더할 열 | `attempt`, `lease_until`. 결과 보관 `keep_result=0` |
| AR5 | 경계 검사 | import-linter(D8) + ruff `TID251`(arq · Redis 연결 · LLM SDK · boto3). Tach는 안 씀 |
| AR6 | uvicorn 프로세스 수 | `--workers 2`(2 vCPU), Gunicorn 안 씀. 2GiB면 사진 동시 처리를 1로 |
| AR7 | Caddy 설정 | 제안 Caddyfile(재시도 10초, keepalive 4초, `/api` 25MB, 응답 60초) |
| AR8 | LB · 감시 헬스체크 주소 | LB는 `/health/live`, 감시 · 알림은 `/health/ready` |
| AR9 | 백업 · 데이터 손실 허용 | DLM 매일 스냅숏 7일 + 매일 `pg_dump` → S3 14일. 하루치 손실(RPO 24시간)을 팀이 받아들이는지 정한다 |
| AR10 | 이미지 빌드 위치 (README 미정 항목) | GitHub Actions에서 빌드 → GHCR 또는 ECR → EC2는 받기만. ARM 서버면 arm64로 |
| AR11 | 서버 크기 | 시연까지 t4g.small. 무료가 2026-12-31에 끝나므로 그 전에 서울 리전 요금을 보고 다시 정한다 |
| AR12 | 부하 시험 | 시연 전 한 번: 로그인 · 사진 올리기 · 진행 현황 보기. 결과로 AR6 · AR11을 다시 본다 |
| AR13 | 두 번째 서버로 갈 조건 | 팀이 숫자로 정한다(예: CPU 70% 지속, 무중단 배포 요구). 순서는 S3 → RDS → ALB 2대 또는 ECS Express Mode |

## 출처

- **모놀리스 · 마이크로서비스:**
  - [Shopify, Deconstructing the Monolith](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity) (2019-02-21)
  - [Shopify, Under Deconstruction](https://shopify.engineering/shopify-monolith) (2020-09-16)
  - [A Packwerk Retrospective](https://railsatscale.com/2024-01-26-a-packwerk-retrospective/) (2024-01-26)
  - [GitHub, Building GitHub with Ruby and Rails](https://github.blog/engineering/architecture-optimization/building-github-with-ruby-and-rails/) (2023-04-06)
  - [DHH, The Majestic Monolith](https://signalvnoise.com/svn3/the-majestic-monolith/) (2016-02-29), [The Majestic Monolith can become The Citadel](https://signalvnoise.com/svn3/the-majestic-monolith-can-become-the-citadel/) (2020-04-08)
  - [Fowler, MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html) (2015), [MicroservicePrerequisites](https://martinfowler.com/bliki/MicroservicePrerequisites.html) (2014)
  - [Sam Newman 인터뷰 (InfoQ)](https://www.infoq.com/news/2020/05/monolith-decomposition-newman/) (2020-05-13)
  - [ThoughtWorks Radar, Microservice envy](https://www.thoughtworks.com/radar/techniques/microservice-envy) (Hold), [Spring Modulith](https://www.thoughtworks.com/radar/languages-and-frameworks/spring-modulith) (Assess)
  - [Spring Modulith 2.1.1 · 2.2 M1](https://spring.io/blog/2026/08/26/spring-modulith-2-2-m1-2-1-1-2-0-8-and-1-4-13-released/) (2026-08-26)
  - [Kraken, How we organise our very large Python monolith](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/) (2023-07-11), [Kraken, How we ship (2026)](https://engineering.kraken.tech/news/2026/03/09/how-we-ship-2026.html) (2026-03-09)
  - [Prime Video 모놀리스 전환 (InfoQ)](https://www.infoq.com/news/2023/05/prime-ec2-ecs-saves-costs/) (2023-05-03)
  - [Istio, istiod](https://istio.io/latest/blog/2020/istiod/) (2020-03-19)
  - [Netflix Dispatch](https://github.com/Netflix/dispatch) (2025-09-03 보관됨), [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices), [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
  - 'CNCF 2025 조사에서 42%가 모놀리스로 돌아왔다'는 숫자는 블로그끼리만 서로 인용하고 [CNCF 2024 조사](https://www.cncf.io/reports/cncf-annual-survey-2024/)에는 없다. 쓰지 않는다.
- **다른 구조:**
  - [Cockburn, Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/), [Bogard, Vertical Slice](https://www.jimmybogard.com/vertical-slice-architecture/) (2018-04-19), [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
  - [Cosmic Python 2장 Repository](https://www.cosmicpython.com/book/chapter_02_repository.html), [Cosmic Python 맺음말](https://www.cosmicpython.com/book/epilogue_1_how_to_get_there_from_here.html)
  - [Fowler, CQRS](https://martinfowler.com/bliki/CQRS.html), [Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html), [Sam Newman, BFF](https://samnewman.io/patterns/architectural/bff/) (2015-11-18)
  - [tRPC](https://trpc.io/docs), [AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [Lambda INIT 과금](https://aws.amazon.com/blogs/compute/aws-lambda-standardizes-billing-for-init-phase/) (2025-04-29 발표, 2025-08-01 시행)
- **Next.js:**
  - [Data Security](https://nextjs.org/docs/app/guides/data-security) (2026-10-06 갱신), [Backend for Frontend](https://nextjs.org/docs/app/guides/backend-for-frontend), [Mutating Data](https://nextjs.org/docs/app/getting-started/mutating-data)
  - [serverActions.bodySizeLimit (기본 1MB)](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverActions), [proxy (middleware 새 이름)](https://nextjs.org/docs/app/api-reference/file-conventions/proxy), [proxyClientMaxBodySize](https://nextjs.org/docs/app/api-reference/config/next-config-js/proxyClientMaxBodySize)
  - [Self-Hosting](https://nextjs.org/docs/app/guides/self-hosting) (2026-10-15 갱신: 여러 대 · `deploymentId` · 캐시 · SIGTERM), [output standalone](https://nextjs.org/docs/app/api-reference/config/next-config-js/output), [standalone KEEP_ALIVE_TIMEOUT (#46052)](https://github.com/vercel/next.js/pull/46052)
- **작업 큐:**
  - [arq PyPI 기록](https://pypi.org/project/arq/#history), [arq 이슈 #510 유지보수 전용](https://github.com/python-arq/arq/issues/510) (2025-10-18), [arq 이슈 #437](https://github.com/python-arq/arq/issues/437), [arq 문서 v0.28](https://arq-docs.helpmanual.io/)
  - [SAQ](https://github.com/tobymao/saq), [pgqueuer](https://github.com/janbjorge/pgqueuer), [procrastinate 연결](https://procrastinate.readthedocs.io/en/stable/howto/basics/connector.html), [Taskiq](https://pypi.org/project/taskiq/#history), [Dramatiq 변경 기록](https://dramatiq.io/changelog.html), [Celery](https://pypi.org/project/celery/#history), [PGMQ](https://github.com/pgmq/pgmq)
  - [Brandur, Transactionally Staged Job Drains](https://brandur.org/job-drain) (2017-09-20), [Brandur, Postgres Job Queues & Failure By MVCC](https://brandur.org/postgres-queues) (2015-05-18), [River, Transactional enqueueing](https://riverqueue.com/docs/transactional-enqueueing)
- **경계 검사:**
  - [import-linter PyPI](https://pypi.org/project/import-linter/), [import-linter 문서](https://import-linter.readthedocs.io/en/stable/), [grimp](https://pypi.org/project/grimp/)
  - [Tach (tach-org)](https://github.com/tach-org/tach), [dtach (관리 공백 기록)](https://github.com/DetachHead/dtach), [PyTestArch](https://pypi.org/project/PyTestArch/), [pytest-archon](https://pypi.org/project/pytest-archon/), [deply](https://pypi.org/project/deply/)
  - [ruff 설정 (flake8-tidy-imports banned-api)](https://docs.astral.sh/ruff/settings/)
- **서버 · 프록시:**
  - [Uvicorn Deployment](https://uvicorn.dev/deployment/), [Uvicorn Settings](https://uvicorn.dev/settings/), [Uvicorn Server Behavior](https://uvicorn.dev/server-behavior/), [Uvicorn 릴리스 기록](https://uvicorn.dev/release-notes/)
  - [FastAPI Server Workers](https://fastapi.tiangolo.com/deployment/server-workers/), [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
  - [Caddy reverse_proxy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy), [Caddy 전역 옵션 (timeouts)](https://caddyserver.com/docs/caddyfile/options), [Caddy request_body](https://caddyserver.com/docs/caddyfile/directives/request_body), [Caddy Automatic HTTPS (클러스터)](https://caddyserver.com/docs/automatic-https)
  - [Starlette Requests (파일은 임시 저장소로)](https://starlette.dev/requests/), [Starlette 릴리스 기록 (1.6.0 max_body_size)](https://starlette.dev/release-notes/)
  - [ALB 502 원인 (keep-alive)](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html)
  - [Compose services (stop_grace_period · restart)](https://docs.docker.com/reference/compose-file/services/), [Docker가 unhealthy를 재시작하지 않음 (포럼)](https://forums.docker.com/t/unhealthy-container-does-not-restart/105822)
  - [SQLAlchemy 연결 풀](https://docs.sqlalchemy.org/en/20/core/pooling.html), [SQLAlchemy asyncpg · PgBouncer](https://docs.sqlalchemy.org/en/21/dialects/postgresql.html), [PostgreSQL 17 연결 설정](https://www.postgresql.org/docs/17/runtime-config-connection.html)
  - [argon2-cffi API (기본값 RFC 9106 저메모리)](https://argon2-cffi.readthedocs.io/en/latest/api.html)
  - [docker-rollout](https://github.com/wowu/docker-rollout), [Kamal proxy](https://kamal-deploy.org/docs/configuration/proxy/)
- **AWS · 호스팅:**
  - [App Runner (2026-04-30부터 새 고객 안 받음)](https://aws.amazon.com/apprunner/), [App Runner 변경 · ECS Express Mode 안내](https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html), [ECS Express Mode 발표](https://aws.amazon.com/about-aws/whats-new/2025/11/announcing-amazon-ecs-express-mode/) (2025-11)
  - [EC2 T4g (무료 체험)](https://aws.amazon.com/ec2/instance-types/t4/), [공인 IPv4 요금](https://aws.amazon.com/vpc/pricing/), [Lightsail 요금](https://aws.amazon.com/lightsail/pricing/), [ELB 요금](https://aws.amazon.com/elasticloadbalancing/pricing/), [Fargate 요금](https://aws.amazon.com/fargate/pricing/), [ElastiCache 요금](https://aws.amazon.com/elasticache/pricing/), [AWS 프리 티어](https://aws.amazon.com/free/)
  - [Fly.io 요금](https://docs.fly.io/about/pricing), [Render 무료 플랜](https://render.com/docs/free), [Railway 요금](https://railway.com/pricing)
- **백업:**
  - [PostgreSQL 17 파일 시스템 백업 (스냅숏)](https://www.postgresql.org/docs/17/backup-file.html), [EBS Data Lifecycle Manager](https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html), [EBS 요금](https://aws.amazon.com/ebs/pricing/)
- **우리 코드:** AGENTS.md 2 · 3 · 7 · 10장, [app-structure.md](app-structure.md), [ai-architecture.md](ai-architecture.md), `compose*.yaml`, `infra/caddy/Caddyfile`, `backend/Dockerfile`, `backend/app/{main,db,queue,worker}.py`, `backend/app/auth/service.py`, `backend/app/files/{storage,images,router}.py`, `frontend/next.config.ts`, `frontend/lib/backend/{server,client}.ts`
