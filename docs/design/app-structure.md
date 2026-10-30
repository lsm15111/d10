# 앱 구조 제안 (모듈러 모놀리스)

기준일 2026-10-29 · 상태: 제안 (D1~D8 결정 전 · D9 적용) · 그림: [system-v3.2.svg](../architecture/system-v3.2.svg), AI는 [ai-architecture.md](ai-architecture.md)

## 결론

- **지금 구조를 유지한다:** 기능별 패키지로 나눈 하나의 FastAPI 앱(모듈러 모놀리스)이고, 기능 안은 `router → service → repository`.
- **세 가지를 더한다:**
  1. 기능 사이 층 순서를 정하고 CI에서 검사한다 (import-linter).
  2. 상태 변경을 한 방식으로 통일한다: 허용 전이 → 조건부 UPDATE → 같은 트랜잭션에 이력 행.
  3. `jobs` 표 하나를 작업 원장 겸 outbox로 쓰고 arq로 돌린다.
- `calc`는 순수 함수의 '안쪽 원'이다. 외부 경계(LLM · 공공 API · 파일 저장)만 어댑터 파일로 둔다.
- **하지 않는다:** 마이크로서비스, 전면 클린 아키텍처 · CQRS, 메시지 브로커. GovBiz에서 비용이 가장 컸던 부분이다.

## GovBiz(4th-1Team)에서 배운 것

- **구조:** Kotlin · Spring 코어 + FastAPI AI + Django ops + 수집 서비스 분리, RabbitMQ, k8s · Argo CD, 웹은 클린 아키텍처 + DI.
- **잘 된 것:**
  - 실제 구현이 둘 이상일 때만 interface를 둔 규칙.
  - AI 응답 계약 검사(후보에 없는 id 거부).
  - 실행 행을 outbox로 쓰고 상태 선점으로 중복 실행 막기.
  - 수집이 일부 실패하면 기존 값 유지.
- **비쌌던 것:**
  - 서비스 경계마다 같은 규칙을 다르게 구현해서 계약 버그가 났다(예: 글자 수를 UTF-16과 코드포인트로 따로 셈, `docs/project-review-20260907.md`).
  - 수집 서비스 분리로 projection · 내부 토큰 · 버전 관리가 늘었다.
  - 언어 3개와 저장소 · 큐 · 인프라 종류가 많았다.
  - 회고에 '고도화될수록 팀원들이 따라오기 어려웠다'는 내용이 있다.
- **그래서:**
  - 언어 하나 · 프로세스 하나로 가고, 경계는 패키지로 나눠 도구로 검사한다.
  - outbox · 상태 선점은 RabbitMQ 대신 arq로 가져온다.
  - 팀원 모두가 한 장 그림으로 설명할 수 있는 구조만 쓴다.

## 후보 구조 판정

| 후보 | 판정 | 이유 |
| --- | --- | --- |
| 모듈러 모놀리스 (기능별 패키지) | 채택 | 지금 구조. 경계 검사만 더한다 |
| 계층형 (router · service · repository) | 기능 안에서만 | 최상위를 기술 종류로 나누면 기능 10개에서 섞인다 |
| 수직 슬라이스 | 일부 | service 함수를 유스케이스 이름으로(`submit_estimate`). 폴더는 안 나눈다 |
| 헥사고날 (포트 · 어댑터) | 일부 | `client.py`, `agent/llm.py`, `files/storage.py`만 어댑터. interface는 두 번째 구현이 생길 때 |
| 클린 · 어니언 | calc만 | calc가 안쪽 원. 나머지에 UseCase · DI를 두지 않는다 |
| DDD 전술 패턴 | 일부 | 용어표, `(project, trade)` · `quote + quote_lines`를 한 단위로 잠금. 이벤트 버스는 안 씀 |
| CQRS | 가볍게 | 비교표 · 진행 현황은 읽기 전용 조회 함수로. 읽기 DB · 이벤트 소싱은 보류 |
| 이벤트 기반 · outbox | 일부 | `jobs` 표 + arq. 처리 함수 목록은 worker.py에 보이게 둔다 |
| 마이크로서비스 | 보류 | 자동 배포 · 관측 같은 선행 비용이 크고, 경계를 처음에 맞게 긋기 어렵다 |

## 목표 폴더

```
backend/app/
├─ main.py · worker.py   조립만 (router · 미들웨어 등록 / arq 작업 · cron 등록)
├─ config.py · db.py · queue.py
├─ shared/     clock · errors · ids · regions (둘 이상이 실제로 쓰는 것만)
├─ calc/       순수 함수: 금액 · 수량 · 표준견적서 · 견적 합계(포함 상태 6종) · 공정표 · 추천 점수
├─ agent/      설명 · 초안만: llm.py(SDK 한 곳, LLM_LIVE=false면 스텁) · 예상 공정표 · 추천 · 확정 공정표 · prompts/
├─ auth/       회원 · 세션 · deps                         (구현됨)
├─ files/      파일 정보 + storage.py(디스크 → S3 경계)   (구현됨)
├─ vendor/     가입 · 승인 · 목록 · 상세 · 프로필         (가입 · 승인 구현됨)
├─ project/    프로젝트 · 공간 · 공정, 공정 단계, 이력     (만들기 · 보기 구현됨)
├─ refprice/   기준 단가 · 공휴일 + 수집 작업
├─ jobs/       작업 원장 = outbox
├─ quote/      표준견적서 스냅숏 · 추천 결과 · 가견적 요청 · 견적서 · 비교
├─ visit/      실측 요청 · 실측 견적 · 확정 / 다시 고르기
└─ schedule/   예상 공정표 · 공사기간 · 확정 공정표
```

## 의존 규칙

```
조립   main.py | worker.py
흐름   schedule → visit → quote          (화살표 방향으로만 부른다)
대상   project | vendor                  (서로 모른다)
기반   files | refprice | jobs  → auth
도구   agent → calc
공통   shared · config · db · queue
```

- **층 순서:** 위 줄은 아래 줄을 부를 수 있고, 반대는 안 된다. `|`로 묶인 것끼리는 서로 import하지 않는다.
- **다른 기능 부르기:** 그 기능 service의 공개 함수로만 부른다. 다른 기능의 models는 읽기 조인에만 쓰고, 쓰기는 그 표 주인 service만 한다. router끼리 import하지 않는다.
- **아래 층이 위 층에 일을 시킬 때:** 같은 트랜잭션에 `jobs` 행을 남기고 worker가 위 층 service를 부른다. 예: 프로젝트를 만들면 `jobs(project_created)` → 표준견적서 · 추천 · 예상 공정표.
- **agent:** DB에 쓰지 않는다. 결과의 주인 service가 계산 엔진으로 검산한 뒤 저장한다.
- **예외 하나:** `/me`가 업체 승인 상태를 읽으려고 `auth.service → vendor.repository`를 늦게 import한다. 예외로 적어 두거나 옮긴다(D7).

## 상태 바꾸기

- **한 트랜잭션 안의 순서:**
  1. 공정 행(`project_trades`)을 잠그고 지금 단계를 확인한다.
  2. 자기 표를 바꾼다(조건부 UPDATE, 1행이 아니면 409).
  3. 공정 단계를 옮긴다.
  4. `events` 행을 남긴다.
  5. 필요하면 `jobs` 행을 남긴다.
  6. commit한다.
- **DB가 지키는 것:**
  - 가견적 요청은 UNIQUE(project, trade, vendor).
  - 진행 중인 실측은 공정마다 1곳(부분 UNIQUE).
  - 확정은 공정마다 1곳(부분 UNIQUE).
- **jobs 처리:**
  1. commit 뒤에 `_job_id = jobs.id`로 넣는다.
  2. 1분마다 cron이 오래 머문 작업을 다시 넣는다.
  3. `queued → running`을 차지한 쪽만 실행한다.
  4. 두 번 돌아도 한 번만 반영되게 만든다(arq는 같은 작업을 두 번 부를 수 있다).
  5. 실행 기록(입력 스냅숏 · 모델 · 프롬프트 버전 · 비용 · 시간)도 이 행에 둔다.

## 테스트 층

| 층 | 대상 | 지금 |
| --- | --- | --- |
| 단위 | calc (v6 테스트 87개 이식, 불변식) · agent (스텁, 스키마, 숫자 다르면 버림) | 없음 |
| 통합 | API → service → 실제 PostgreSQL: 상태 전이 · 권한 · 개인정보 · 동시 요청 409 | 있음 (28개) |
| 통합 | jobs · worker: 두 번 실행해도 결과 1개, 다시 넣기 | 없음 |
| 스키마 | migration up → down → up, `alembic check` | up/down 있음 |
| 경계 | `lint-imports`, OpenAPI → TS 타입 비교 | 시험만 (CI 없음) |
| E2E | 가견적 → 실측 → 확정 (Playwright) | 나중 |

## 검증 방법 (CI)

- **CI를 만들어 두었다 (2026-10-29, `.github/workflows/ci.yml`):** mitjip 폴더가 아직 git 저장소가 아니라서 한 번도 돌지 않았다. 저장소에 올리고 main 보호 규칙에서 필수로 걸어야 효과가 있다.
- **CI에 넣은 것과 이유 (꼭 필요한 것만):**
  - backend `ruff` · `pytest`: 테스트가 실제 PostgreSQL을 써서 로컬에서 빼먹기 쉽다. migration up → down → up도 여기서 돈다.
  - API 타입 비교: 화면이 API를 바로 부르므로, API를 바꾸고 타입을 안 만들면 화면 typecheck는 통과해도 실행 중에 깨진다.
  - frontend `typecheck` · `lint` · `build`: build만 잡는 오류가 있다(예: page 파일에 다른 export를 두면 build만 실패).
- **아직 넣지 않은 것:** `lint-imports`(D8 결정 뒤, 아래 시험 설정 그대로), `alembic check`(테스트가 migration으로 표를 만들어서 빠진 migration은 대부분 테스트에서 잡힌다), 이미지 빌드(배포 때).
- **import-linter 시험 (2026-10-29, v2.15, 프로젝트에 추가하지 않고 `uv run --with`로):**
  - 계약 3개를 걸었다: 기능 사이 층 순서, 기능 안 `router → deps → service → repository → models · schemas`, router끼리 서로 모름.
  - 결과: 함수 안의 늦은 import `auth.service → vendor.repository`(D7 예외)를 찾았다. 예외로 적으면 3개 모두 통과한다. 3초 안쪽.
  - 탈퇴(`account`) · 요청 제한(`shared.ratelimit`)을 더한 뒤 다시 돌렸더니 `shared`가 Redis 연결(`queue`)을 쓴다는 것이 드러나서 층을 `shared → db | queue → config`로 바로잡았다. 44개 파일 · 115개 의존 모두 통과.
- **이 방법이 맞는 이유:** 파이썬 import만 보는 정적 검사라 빠르고, 규칙이 설정 파일 한 장에 보이며, 아직 없는 기능은 괄호로 '있으면 검사'로 둘 수 있다. Tach(v0.35)도 있지만 공개 interface 강제 같은 기능이 지금 필요 없고 설정이 더 크다.
- **못 잡는 것:**
  - 문자열로 부르는 코드(`getattr`, 작업 이름 문자열)
  - 같은 층 안의 잘못된 호출 순서
  - DB를 통한 결합(다른 기능 표에 쓰기)
  - 그래서 '다른 기능 표에 쓰지 않기'는 PR 리뷰와 통합 테스트로 지킨다.
- **시험에 쓴 설정** (D8로 넣기로 하면 `backend/.importlinter`에 둔다):

```ini
[importlinter]
root_package = app
include_external_packages = False

[importlinter:contract:features]
name = 기능 사이 층 순서 (위 → 아래만)
type = layers
layers =
    app.main | app.worker
    (app.schedule)
    (app.visit)
    (app.quote)
    app.account | app.project | app.vendor
    app.files | (app.refprice) | (app.jobs)
    app.auth
    (app.agent)
    (app.calc)
    app.shared
    app.db | app.queue
    app.config
ignore_imports =
    # D7 예외: /me가 업체 승인 상태를 읽는다
    app.auth.service -> app.vendor.repository

[importlinter:contract:inside]
name = 기능 안: router → deps → service → repository → models · schemas
type = layers
containers =
    app.auth
    app.files
    app.project
    app.vendor
    app.account
layers =
    router
    (cli)
    (deps)
    service
    (storage)
    (repository)
    (models) | (schemas)

[importlinter:contract:routers]
name = router끼리는 서로 모른다
type = independence
modules =
    app.auth.router
    app.account.router
    app.files.router
    app.project.router
    app.vendor.router
```

- **CI에 넣을 것 (PR마다):**
  1. `ruff check` · `ruff format --check`
  2. `pytest` (PostgreSQL · Redis 서비스 컨테이너)
  3. `lint-imports`
  4. `alembic upgrade head` 뒤 `alembic check` (모델 ↔ DB 차이 0)
  5. OpenAPI 타입: `pnpm gen:api` 뒤 `git diff --exit-code` (API를 바꾸고 타입을 안 만들면 실패)
  6. `pnpm typecheck` · `pnpm lint` · `pnpm build`
  7. `docker compose config --quiet`, 이미지 빌드

## 프런트

- `app/(site)`, `app/(customer)`, `app/vendor`, `app/admin`으로 나누되 URL은 그대로 둔다.
- `components/<영역>/` 끼리는 import하지 않는다. 조합은 app 화면에서 한다.
- `lib/api/`: OpenAPI에서 만든 타입, `server.ts`(server-only, 쿠키 전달), `client.ts`(/api). 파일은 백엔드 기능과 1:1로 둔다.
- 읽기는 Server Component, 쓰기는 클라이언트에서 `/api`로. Server Action은 쓰지 않는다(한 가지 방식만).
- **D9를 적용했다 (2026-10-29):** `lib/backend/server.ts`(읽기, 쿠키 넘김), `lib/backend/client.ts`(쓰기, `/api`), `lib/backend/schema.d.ts`(OpenAPI에서 생성, `pnpm gen:api`).
- **D9가 맞는 이유:**
  - 세션 쿠키를 API 한 곳이 심고 지운다. Server Action을 쓰면 Next가 쿠키를 다시 옮겨 심어야 한다.
  - 사진 · 도면이 Next 서버를 한 번 더 거치지 않는다. Server Action 본문은 기본 1MB이고, 도면은 20MB다.
  - 오류 모양이 API 하나다. 같은 주소라 CORS 설정이 필요 없다.
- **D9의 대가:**
  - 쓰기 화면은 자바스크립트가 있어야 돈다. 질문 흐름은 원래 그렇다.
  - 개발 중에는 Next가 `/api`를 넘기므로 본문 한도(`proxyClientMaxBodySize`, 기본 10MB)를 25MB로 올렸다. 운영은 Caddy가 바로 넘긴다.

## AGENTS.md에 넣을 규칙 (제안)

1. **층 순서:** 위 그림을 넣고 순환 import를 금지한다. CI에서 `lint-imports`로 검사하고, 예외는 설정 파일에 이유와 함께 적는다.
2. **다른 기능 부르기:** service 공개 함수로만. 다른 기능 models는 읽기 조인만 하고, router끼리 import하지 않는다.
3. **commit:** 요청 하나 · 작업 하나당 맨 바깥 service에서 한 번. 다른 기능이 부르는 함수는 flush만 하고 그렇게 적는다.
4. **상태 변경:** 허용 전이 → 조건부 UPDATE → 같은 트랜잭션에 `events`. 불변식은 부분 UNIQUE · CHECK로도 지킨다.
5. **후속 작업:** `jobs` 행 + commit 뒤 enqueue, 두 번 돌아도 한 번만 반영.
6. **프런트:** 읽기 `lib/api/server.ts`, 쓰기 `/api`, 기능 폴더끼리 import 금지.

## 정할 것

| | 질문 | 권장 |
| --- | --- | --- |
| D1 | 추천 결과 · 표준견적서는 어느 기능이 가지나 | `quote` (업체 고르기 → 가견적이 한 흐름) |
| D2 | 프로젝트를 만든 뒤 계산은 누가 부르나 | `jobs` + worker |
| D3 | 작업 원장 | `jobs` 표 하나 (agent_run · 알림 · 수집을 따로 두지 않음) |
| D4 | 기능 안 `jobs.py`(worker 작업 함수) 허용 | 허용 |
| D5 | 확정 · 다시 고르기는 어느 기능이 가지나 | `visit` |
| D6 | 공정 단계 저장 | `project_trades.stage` + 행 잠금 |
| D7 | `/me`의 역방향 import | 예외로 적어 둠 |
| D8 | 새 의존성 | import-linter(개발용). openapi-typescript는 AGENTS.md 7장대로 넣었고(개발용), openapi-fetch는 필요 없음(40줄 `client.ts`로 충분) |
| D9 | 프런트 쓰기 경로 | 클라이언트에서 `/api` 직접 — 적용함 |

## 출처

- FastAPI 관례: [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices), [Netflix Dispatch](https://github.com/Netflix/dispatch/tree/main/src/dispatch/incident), [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)
- 모놀리스 · 마이크로서비스: [MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html), [MicroservicePrerequisites](https://martinfowler.com/bliki/MicroservicePrerequisites.html), [Shopify 모놀리스 분해](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity)
- 구조 패턴: [Vertical Slice](https://www.jimmybogard.com/vertical-slice-architecture/), [Hexagonal](https://alistair.cockburn.us/hexagonal-architecture/), [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), [DDD Aggregate](https://martinfowler.com/bliki/DDD_Aggregate.html)
- CQRS · outbox: [CQRS](https://martinfowler.com/bliki/CQRS.html), [Event-driven](https://martinfowler.com/articles/201701-event-driven.html), [Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html), [arq](https://arq-docs.helpmanual.io/)
- 검사 도구: [import-linter 2.15 (PyPI)](https://pypi.org/project/import-linter/), [Tach](https://github.com/tach-org/tach)
- 도구 · 프런트: [import-linter](https://import-linter.readthedocs.io/en/v2.0/contract_types.html), [Next.js 프로젝트 구조](https://nextjs.org/docs/app/getting-started/project-structure), [Next.js 데이터 보안](https://nextjs.org/docs/app/guides/data-security), [bulletproof-react](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md)
