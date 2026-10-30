# 믿집

도배·목공 견적부터 실측, 공정표, 계약까지 잇는 인테리어 플랫폼.
작업 규칙은 [AGENTS.md](AGENTS.md), 스택 결정은 [ADR 0001](docs/adr/0001-stack.md).

| 구성 | 기술 | 로컬 주소 |
| --- | --- | --- |
| web | Next.js 16 (TypeScript) | http://localhost:3000 |
| api | FastAPI (Python 3.12, uv) | http://localhost:8000/docs |
| worker | arq (Redis 작업 큐) | — |
| db | PostgreSQL 17 | localhost:5433 |
| redis | Redis 8 | localhost:6379 |
| caddy | 운영 HTTPS (EC2에서만) | 443 |

## 처음 한 번

1. Docker Desktop을 켠다.
2. 환경변수 파일을 만든다.

   ```bash
   cp .env.example .env
   ```

## 로컬 개발

```bash
docker compose up --build
```

- `compose.override.yaml`이 자동으로 붙어서 코드를 고치면 api·worker·web이 다시 뜬다.
- 첫 화면(http://localhost:3000)에 api·db·redis 연결 상태가 나온다.
- 끄기: `docker compose down` (DB 데이터는 남는다)
- PC에 PostgreSQL이 이미 깔려 있어 5432가 겹치므로 DB는 5433으로 연다. 다른 포트가 겹치면 `.env`의 `*_HOST_PORT`를 바꾼다.

자주 쓰는 명령:

```bash
docker compose logs -f api
```

```bash
docker compose exec api alembic revision --autogenerate -m "설명"
```

```bash
docker compose run --rm migrate
```

```bash
docker compose exec db psql -U mitjip -d mitjip
```

## 화면

요구사항 정의서 v3.2(2026.10.29) 기준 화면이 `frontend/`에 있다. 흐름 설계는 [docs/design/quote-flow-v3.2.md](docs/design/quote-flow-v3.2.md), 구조도는 [docs/architecture](docs/architecture/README.md).

- **API에 붙은 것:** 로그인 · 회원가입(고객 · 업체) · 로그아웃 · 탈퇴, 내 정보 · 설정, 견적 받기 → 사진 · 도면 올리기 → 프로젝트 만들기, 내 프로젝트, 프로젝트 진행 현황(기본정보 · 사진), 업체 홈(승인 상태), 관리자 업체 가입 승인 · 반려.
- **예시 데이터:** 예시 프로젝트(`/projects/p1`)의 예상 공정표 · 표준견적서 · 업체 · 가견적 · 실측 · 확정 공정표, 관리자 회원 목록.
- **디자인 예시:** `/samples/design` (제안, [visual-design.md](docs/design/visual-design.md)). 실제 프로젝트에서 이 단계를 열면 '아직 연결 전'으로 보인다.

```bash
docker compose up -d db redis api
```

```bash
cd frontend && pnpm dev
```

- `pnpm dev`는 `/api/*`를 `API_INTERNAL_URL`(기본 http://localhost:8000)로 넘긴다. 회원은 가입 화면에서 만들고, 관리자는 아래 'API' 절의 명령어로 만든다.
- API를 바꿨으면 타입을 다시 만든다 (API가 떠 있어야 한다). 생성된 `frontend/lib/backend/schema.d.ts`는 손으로 고치지 않는다.

  ```bash
  cd frontend && pnpm gen:api
  ```
- 예시 데이터: `frontend/lib/mock/fixtures.json` — `node frontend/scripts/gen-fixtures.js <mitjip-v6 경로> <출력 경로>`로 v6 계산 엔진과 2026 공공 단가에서 다시 만든다. 금액 · 수량 · 날짜는 이 파일에서만 나온다.

| 경로 | 요구사항 |
| --- | --- |
| `/login`, `/signup` | FFW-01·02, 권한별 이동 FBF-02 |
| `/signup/vendor`, `/vendor` | FFV-01 업체 가입(기본 정보 + 사업자등록증), 업체 홈(승인 대기 · 승인 · 반려 사유) |
| 헤더 '견적 받기' 창, `/start` | FFW-03 기본정보, FFW-04 공간·공정 · 도배 유형 (질문 하나씩, 같은 흐름) → `POST /files`, `POST /projects` |
| `/projects/{id}` | FFW-18 진행 현황 (실제 프로젝트: API) |
| `/projects/p1` | FFW-18~21 진행 현황 (예시) |
| `/projects/p1/plan` | FAG-01 예상 공정표 (그림 저장) |
| `/projects/p1/standard` | FFW-05 표준견적서, FBF-04 출처·적용 시점 |
| `/projects/p1/vendors`, `/vendors/[id]` | FFW-06~09 업체 목록·추천·검색·상세, FFW-10 담기 |
| `/projects/p1/request` | FFW-10 가견적 요청 |
| `/projects/p1/quotes` | FFW-11 가견적 비교, FFW-12 실측 업체 선택·요청, FBF-05 상태 |
| `/projects/p1/measure` | FFW-13 실측 견적, FFW-14 다시 고르기, FFW-15 확정 |
| `/projects/p1/schedule` | FFW-16 확정 공정표 (FAG-03) |
| `/projects/p1/history` | FFW-22 이력 |
| `/my` | FFW-18 마이페이지 · 내 프로젝트: 공정별 상태 한 줄 + 할 일 버튼 하나 |
| `/account`, `/account/withdraw` | FFW-17 마이페이지 · 내 정보 · 설정, 회원 탈퇴 |
| `/admin/members` | FAD-01 (예시 데이터) |
| `/admin/vendors`, `/admin/vendors/[id]` | FAD-02·03 업체 가입 신청 · 사업자등록증 · 승인 · 반려 (API) |

업체가 쓰는 화면(FFV-01~08)은 [흐름 설계](docs/design/quote-flow-v3.2.md) 5장 순서로 만든다.

## API (FastAPI)

`http://localhost:8000/docs`에서 전체를 볼 수 있다. 오류는 모두 `{"error": {"code", "message", "fields"?}}` 모양이다.

| 묶음 | 경로 | 요구사항 |
| --- | --- | --- |
| 회원 | `POST /auth/signup` · `POST /auth/login` · `POST /auth/logout` · `GET/PATCH /me` · `POST /me/withdraw` | FFW-01·02·17, FBF-02 |
| 업체 가입 · 승인 | `POST /auth/vendor-signup`(name · email · password + license_file) · `GET /admin/vendors?status=` · `GET /admin/vendors/{id}` · `POST /admin/vendors/{id}/approve` · `.../reject` | FFV-01, FBF-01, FAD-02·03 |
| 파일 | `POST /files`(kind = photo · plan · license · portfolio) · `GET /files/{id}` | FFW-03 사진 · 도면 |
| 프로젝트 | `POST /projects` · `GET /projects` · `GET /projects/{id}` · `GET /regions` | FFW-03·04·18 |

- 로그인은 서버 세션이다. 쿠키(`mj_sid`, 운영은 `__Host-mj_sid`)에는 무작위 토큰만, DB에는 그 해시만 둔다. 비밀번호는 argon2id 해시로 저장하고, 같은 이메일로 15분에 10번 틀리면 막는다.
- 상태를 바꾸는 요청은 `ALLOWED_ORIGINS`에 없는 사이트에서 오면 거절한다.
- 파일 형식은 이름이 아니라 파일 앞부분으로 확인한다. 사진 10MB, 도면 20MB까지. 남의 파일은 404로 답한다. 사진은 저장 전에 위치(GPS) · EXIF를 지우고, HEIC는 JPEG로 바꾼다.
- 본문은 경로별로 막는다(JSON 1MB · 파일 21MB). 처리하지 못한 오류도 같은 오류 모양으로 답하고(DB 연결 문제는 503), 로그에는 SQL 값 · 오류 메시지를 넣지 않는다.
- 요청 제한(Redis): 로그인 같은 이메일 · IP 15분 10번 · IP 15분 50번, 가입 IP 1시간 10번, 파일 1시간 120개, 프로젝트 1시간 30개. 넘으면 429와 Retry-After.
- 관리자 계정은 가입 화면이 없다. 이렇게 만든다:

  ```bash
  docker compose exec api python -m app.auth.cli create-admin --email admin@example.com --name 관리자
  ```

## 테스트·검사

백엔드 테스트는 실제 PostgreSQL · Redis를 쓴다. 먼저 띄운다 (테스트는 `mitjip_test` DB를 따로 만들어 쓰고 개발 DB는 건드리지 않는다):

```bash
docker compose up -d db redis
```

```bash
cd backend && uv run pytest && uv run ruff check . && uv run ruff format --check .
```

```bash
cd frontend && pnpm typecheck && pnpm lint
```

PR마다 같은 검사를 CI(`.github/workflows/ci.yml`)가 돌린다: backend ruff · pytest, frontend API 타입 비교 · typecheck · lint · build. 저장소에 올린 뒤 main 보호 규칙에서 필수로 건다.

## EC2 운영

`.env`에 `DOMAIN`과 긴 `POSTGRES_PASSWORD`를 넣고, 도메인의 A 레코드를 EC2의 고정 IP로 맞춘 뒤:

```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d --build
```

- 밖으로 열리는 포트는 80·443뿐이다. Caddy가 인증서를 자동으로 받고 `/api/*`를 FastAPI로, 나머지를 Next.js로 보낸다.
- 운영에서는 API 문서(`/api/docs`)가 닫힌다.
- DB 백업과 이미지 빌드 위치(EC2에서 빌드 vs CI에서 빌드 후 내려받기)는 아직 정하지 않았다.
