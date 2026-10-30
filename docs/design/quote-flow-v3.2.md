# 견적 흐름 설계 (요구사항 v3.2 기준)

기준일 2026-10-29 · 상태: 결정 (10장 모두 권장안, 6번은 ADR 0002)

## 0. 요약

- 요구사항 v3.0 → v3.2의 핵심 변화는 **업체가 직접 쓰는 화면이 생긴 것**이다. 업체가 회원가입하고 관리자 승인을 받은 뒤, 가견적서와 실측 견적서를 직접 써서 내고, 확정되면 공사기간을 등록한다. '자동 등록'(FBF-04, FBF-06)은 '업체가 제출하면 바로 등록'(FFV-03, FFV-05)으로 바뀌었다.
- 지금 화면은 끝난 예시 프로젝트 하나(p1)를 보여 줄 뿐이고, 버튼을 눌러도 다음 단계로 넘어가지 않는다. 백엔드는 상태 확인(health)만 있고 DB 테이블은 없다. **프로젝트 등록은 실제로 저장되지 않는다.**
- 제안: ① 목데이터로 고객 · 업체 · 관리자 화면을 하나의 가상 상태에 묶어 전체 흐름을 먼저 돌려 본다(1단계). ② 같은 함수 모양 그대로 백엔드를 기능 단위로 붙인다(2단계).

## 1. 요구사항 v3.0 → v3.2 바뀐 것

### 새로 생김

| 기능 ID | 이름 | 내용 |
| --- | --- | --- |
| FFV-01 | 업체 회원가입 | 이메일, 비밀번호, 상호명, 대표자명, 사업자등록번호, 연락처, 사업장 주소, 업체 사이트 URL, 사업자등록증 첨부. 포트폴리오는 선택. 가입 후 관리자 승인 |
| FBF-01 | 업체 가입 승인 상태 관리 | 승인대기 · 승인 · 반려. 승인 업체만 업체 기능 사용 |
| FFV-02 | 견적 요청 조회 | 업체가 받은 가견적 요청과 고객의 기본정보 · 사진 · 도면 · 공정을 본다 |
| FFV-03 | 가견적서 제출 | 업체가 가견적 금액과 내용을 써서 낸다. 제출 즉시 고객 프로젝트에 등록 |
| FFV-04 | 실측 요청 확인 | 업체가 받은 실측 요청을 본다. 현장 실측은 업체가 직접 |
| FFV-05 | 실측 견적서 제출 | 실측 후 확정된 견적을 써서 낸다. 제출 즉시 등록 |
| FFV-08 | 업체 정보 관리 (VMY01) | 연락처, 사업장 주소, 사이트 URL, 포트폴리오 수정. 사업자 핵심정보 변경은 관리자 재확인 |
| FAD-02 | 업체 가입 승인 | 관리자가 신청 정보와 사업자등록증을 보고 승인 · 반려 |

### 내용이 바뀜

| 기능 ID | 바뀐 점 |
| --- | --- |
| FFW-01 로그인 | 일반 회원 · 관리자 → 일반 회원 · **업체 회원** · 관리자 |
| FBF-02 권한별 화면 분기 (구 FBF-01) | 승인된 업체는 업체 화면으로 |
| FFW-06 업체 목록, FAG-02 추천 | **승인된 업체만** 목록과 추천에 나온다 |
| FFW-19 · FFW-20 (구 20 · 21) | '자동 등록된' → '업체가 제출한' 가견적서 · 실측 견적서 |
| FAD-01 회원관리 | 일반 회원 + **업체 회원** |
| FAD-03 업체관리 | 승인대기 · 승인 · 반려 목록, 상세에 대표자명 · 사업장 주소 · 사이트 URL · 사업자등록증 |
| FAD-04 업체 정보 수정 | 기본정보 + **승인 상태** 수정 |

### 빠짐

| v3.0 기능 | 이유 |
| --- | --- |
| FBF-04 가견적서 자동 등록, FBF-06 실측 견적서 자동 등록 | 업체가 직접 제출(FFV-03, FFV-05)로 바뀜 |
| FFW-13 실측 요청 | FFW-12 실측 업체 선택에 합쳐짐 |
| FAD-03 관리자 업체 등록 | 업체가 스스로 가입하고 관리자는 승인만 |

### 번호만 바뀜

FBF-01→02, FBF-02→03, FBF-03→04, FBF-07→06 · FFW-14→13, 15→14, 16→15, 17→16, 18→17, 19→18, 20→19, 21→20, 22→21, 23→22 · FFV-01→06, FFV-02→07. README의 경로 · 요구사항 표를 이 번호로 고쳐야 한다.

## 2. 지금 화면 · 규칙과 어긋나는 곳

1. **관리자 업체 등록 화면**(`/admin/vendors/new`, 등록 폼)은 v3.2에 없다. 가입 승인 화면으로 바꾼다.
2. **업체 상세(FFW-09)는 소개 · 가능 공정 · 시공 지역을 보여 줘야 하는데**, 업체가 이걸 입력하는 곳(FFV-01 가입, FFV-08 정보 관리)에 해당 항목이 없다. 요구사항 틈 → 정할 것 3.
3. **AGENTS.md 1장 용어표**: 가견적 = "업체 단가표 × 표준 수량으로 믿집이 계산한 견적". v3.2는 업체가 직접 써서 낸다. 정의를 바꿔야 한다.
4. **AGENTS.md 1 · 4장 에이전트 범위**: 업체 추천 · 가견적서 · 공정표. v3.2의 AI 기능은 FAG-01 예상 공정표 · FAG-02 추천 · FAG-03 확정 공정표다. 가견적서 에이전트는 요구사항에 없다. 바꾸려면 ADR로 정한다.
5. 진행 현황의 표 안 링크(가견적 · 실측 견적 칸)는 읽기 불편하다 → 5장의 '진행 현황' 방향으로 바꾼다.

## 3. 전체 흐름

| # | 누가 | 하는 일 | 요구사항 | 화면 | 남는 기록 |
| --- | --- | --- | --- | --- | --- |
| 0 | 업체 · 관리자 | 업체 가입 → 승인 | FFV-01, FBF-01, FAD-02 | 업체 가입, 관리자 가입 승인 | 업체 상태 승인 |
| 1 | 고객 | 기본정보 · 공간 · 공정 입력, 프로젝트 만들기 | FFW-03, FFW-04 | 견적 받기 창 | 프로젝트 |
| 2 | 에이전트 | 예상 공정표 | FAG-01 | 1 예상 공정표 | 예상 공정표 |
| 3 | 시스템 | 표준견적서 | FBF-03, FBF-04, FFW-05 | 2 표준견적서, 3 업체 고르기 위 요약 | 표준견적서(단가 버전 고정) |
| 4 | 에이전트 | 승인 업체 중 추천 3곳 | FAG-02, FFW-07 | 3 업체 고르기 | 추천 결과 |
| 5 | 고객 | 공정별 여러 업체 담기 → 같은 조건으로 가견적 요청 | FFW-06, 08, 09, 10 | 3 업체 고르기 → 요청 확인 | 가견적 요청(요청함) |
| 6 | 업체 | 요청 확인 → 가견적서 작성 · 제출 | FFV-02, FFV-03, FBF-05 | 업체: 견적 요청함 → 가견적서 쓰기 | 가견적서, 요청 상태 제출됨 |
| 7 | 고객 | 표준견적서와 나란히 비교 → 공정별 1곳 실측 요청 (희망일 · 동 · 호수 · 동의) | FFW-11, FFW-12 | 4 가견적 비교 | 실측 요청 |
| 8 | 업체 | 실측 요청 확인 → 현장 실측 → 실측 견적서 제출 | FFV-04, FFV-05 | 업체: 실측 요청 → 실측 견적서 쓰기 | 실측 견적서 |
| 9 | 고객 | 실측 견적 확인 → **확정** 또는 **다시 고르기** | FFW-13, FFW-15, FFW-14 | 5 실측 견적 | 확정 / 다시 고르기 기록 |
| 9′ | 고객 | (다시 고르기) 가견적 받은 다른 업체에 실측 요청, 또는 새 업체에 가견적 요청 → 7 · 5로 | FFW-14 | 4 가견적 비교, 3 업체 고르기 | 이전 업체는 '넘김' |
| 10 | 확정 업체 | 공사 시작일 · 종료 예정일 등록 · 수정 | FFV-06, FFV-07 | 업체: 공사기간 | 공사기간 |
| 11 | 시스템 · 에이전트 | 공정별 공사기간으로 전체 일정 → 확정 공정표 | FBF-06, FAG-03 | 6 확정 공정표 | 확정 공정표 |
| 12 | 고객 | 진행 · 이력 확인 | FFW-16, FFW-18~22 | 진행 현황, 이력, 내 프로젝트 | — |

도배와 목공은 따로 움직인다. 한 공정은 확정됐는데 다른 공정은 아직 비교 중일 수 있다.

## 4. 상태

### 공정별 상태 (한 프로젝트의 한 공정)

```
고르는 중 ─요청─▶ 가견적 기다림 ─업체 제출─▶ 비교 중 ─실측 요청─▶ 실측 기다림 ─업체 제출─▶ 실측 견적 도착
                                                    ▲                                          │
                                                    └────────── 다시 고르기 (업체 넘김) ◀───────┤
                                                                                               ▼
                                                                    확정 ─업체 공사기간 등록─▶ 일정 등록됨
```

- 가견적 요청: `요청함 → 제출됨` (업체별). 같은 공정에 여러 업체.
- 실측: 공정마다 한 번에 1곳. `요청함 → 실측 견적 도착`. 업체 확인(FFV-04)은 상태를 바꾸지 않고 '확인함' 표시만 둔다.
- 다시 고르기: 그 업체를 '넘김'으로 남기고 실측 받을 업체 후보에서 뺀다. 가견적서는 이력에 남는다.
- 확정 · 다시 고르기 · 실측 요청은 고객이 누를 때만, 가견적서 · 실측 견적서 · 공사기간은 업체가 누를 때만 바뀐다 (AGENTS.md 3장).

### 프로젝트 단계 (진행 현황 · 상단 표시)

공정들 중 가장 덜 간 단계를 프로젝트 단계로 쓴다. 이동 메뉴 1~6의 '끝남' 표시도 이것으로 정한다.

| 프로젝트 단계 | 조건 | 끝난 메뉴 |
| --- | --- | --- |
| 예상 공정표 | 요청 없음 | 1 · 2 |
| 가견적 요청 | 요청했고 제출 기다림 | 1 · 2 · 3 |
| 가견적 비교 | 제출된 가견적 있음 | 1 · 2 · 3 |
| 실측 | 실측 요청 / 실측 견적 도착 | 1~4 |
| 업체 확정 | 모든 공정 확정, 공사기간 기다림 | 1~5 |
| 공사 일정 확정 | 모든 공정 공사기간 등록 | 1~6 |

## 5. 화면

### 고객 (있는 화면 고치기)

| 화면 | 바꿀 것 |
| --- | --- |
| 견적 받기 창 | '프로젝트 만들기' → 프로젝트 생성 후 `1 예상 공정표`로 |
| 진행 현황 | 표 안 링크를 없애고, 공정별 **할 일 목록** 형태로: 가견적 요청 / 가견적 도착 / 실측 / 실측 견적 · 확정 / 공사기간 줄마다 상태 표(끝남 · 진행 중 · 아직), 공정마다 **다음 할 일 버튼 하나**만 둔다 (GOV.UK '여러 할 일' 패턴) |
| 3 업체 고르기 | 위쪽에 표준견적서 요약(공정별 기준 금액 · 자세히 보기). 승인 업체만 |
| 4 가견적 비교 | 요청만 하고 도착 전 · 일부 도착 상태 화면. 실측 후보에서 '넘긴' 업체 제외 |
| 5 실측 견적 | 확정 / 다시 고르기가 실제로 상태를 바꿈. 다시 고르기 → 4 가견적 비교로 |
| 6 확정 공정표 | 공사기간 등록 전에는 '확정 업체가 공사기간을 등록하면 만들어져요' |
| 내 정보 | `/account`로 분리함 (FFW-17) |

### 업체 (새로)

| 경로 | 요구사항 | 내용 |
| --- | --- | --- |
| `/signup/vendor` | FFV-01 | 기본 회원정보(담당자 이름 · 이메일 · 비밀번호) + 사업자등록증만 (2026-10-29 PO 결정). 업체 정보는 승인 뒤 `/vendor/profile`에서 |
| `/vendor/pending` | FBF-01 | 승인대기 · 반려 안내 (반려 사유) |
| `/vendor` | FFV-02, FFV-04, FFV-06 | 할 일 모음: 새 가견적 요청 · 실측 요청 · 공사기간 등록할 프로젝트 |
| `/vendor/requests/[id]` | FFV-02, FFV-03 | 고객 조건 · 사진 · 도면(동 · 호수 없음) + 가견적서 쓰기 |
| `/vendor/visits/[id]` | FFV-04, FFV-05 | 실측 요청(희망일 · 시간대) 확인 → 확인을 누른 뒤에 동 · 호수가 보임 + 실측 견적서 쓰기 |
| `/vendor/projects/[id]/period` | FFV-06, FFV-07 | 공사 시작일 · 종료 예정일 등록 · 수정 |
| `/vendor/profile` | FFV-08 | 업체 정보 관리 |

가견적서 · 실측 견적서 양식: **표준 행 양식**을 권장한다. 공정별 표준 행(인건비, 철거, 초배, 몰딩 …)마다 금액과 포함 상태(포함 · 묶음 포함 · 따로 계산 · 선택 · 실측 후 · 안 함)를 고르고, 없는 항목은 줄을 더한다. 이렇게 해야 FFW-11 비교표가 같은 줄끼리 맞고, AGENTS.md 3장의 '표준 행 키 + 포함 상태 6종' 저장 규칙도 지킨다. 합계는 화면이 아니라 서버(계산 엔진)가 만든다.

### 관리자

| 경로 | 요구사항 | 바꿀 것 |
| --- | --- | --- |
| `/admin/members` | FAD-01 | 일반 회원 · 업체 회원 탭 |
| `/admin/vendors` | FAD-03 | 승인대기 · 승인 · 반려 탭 |
| `/admin/vendors/[id]` | FAD-02, FAD-04 | 신청 정보 · 사업자등록증 보기, 승인 · 반려(사유), 기본정보 · 승인 상태 수정 |
| `/admin/vendors/new` | (삭제) | v3.2에 없음 |

로그인은 하나(FFW-01). 업체 계정이 승인 상태면 `/vendor`, 승인대기 · 반려면 `/vendor/pending`으로 보낸다(FBF-02).

## 6. 데이터 (PostgreSQL)

| 테이블 | 주요 열 |
| --- | --- |
| `users` | id, email(UNIQUE), password_hash, name, role(customer · vendor · admin), status(active · suspended), created_at |
| `vendors` | user_id(FK), biz_name, owner_name, biz_no, phone, address, site_url, license_file_id, status(pending · approved · rejected), reject_reason, reviewed_by, reviewed_at, trades[], areas[], intro |
| `vendor_portfolio` | vendor_id, title, caption, file_id |
| `projects` | id, owner_id, sido, sgg, house_type, size_band, area_basis, area_m2(numeric(7,1)), built_year, balcony_ext, start_kind, start_date, end_date, occupied, budget_band, created_at |
| `project_spaces` | project_id, name, sort |
| `project_trades` | project_id, trade, space_ids[], items[] |
| `files` | id, owner_id, kind(photo · plan · license · portfolio), storage_key, filename, size, content_type, space_id? |
| `expected_schedules` · `standard_quotes` · `recommendations` | project_id, trade, 결과(JSONB), 산식 · 단가 버전, agent_run_id |
| `quote_requests` | project_id, trade, vendor_id, status(requested · submitted), requested_at, submitted_at · UNIQUE(project, trade, vendor) |
| `quotes` · `quote_lines` | kind(estimate · final), vendor_id, project_id, trade, total, vat, submitted_at / row_key, state(6종), qty, unit, amount(bigint), note |
| `visits` | project_id, trade, vendor_id, status(requested · quoted), wish_date, wish_slot, dong · ho(암호화), consent_at, seen_at |
| `selections` | project_id, trade, vendor_id, decision(confirmed · passed), decided_at |
| `work_periods` | project_id, trade, vendor_id, start_date, end_date, updated_at |
| `ref_prices` | source, item, value, valid_from, collected_at, version (FDT-01) |
| `events` | project_id, actor, kind, payload, at (이력 FFW-22) |
| `agent_runs` | 입력 스냅숏, 출력, 모델, 프롬프트 버전, 비용, 시간 (AGENTS.md 4장) |

## 7. API (FastAPI)

| 묶음 | 경로 |
| --- | --- |
| 인증 | `POST /auth/signup` · `POST /auth/vendor-signup`(파일 포함) · `POST /auth/login` · `POST /auth/logout` · `GET /me` · `PATCH /me` |
| 고객 프로젝트 | `POST /projects` · `GET /projects` · `GET /projects/{id}` · `POST /projects/{id}/files` · `GET /projects/{id}/expected-schedule` · `GET /projects/{id}/standard-quote` · `GET /projects/{id}/recommendations?trade=` |
| 업체 찾기 | `GET /vendors?trade=&region=&q=` (승인만) · `GET /vendors/{id}` |
| 가견적 | `POST /projects/{id}/quote-requests` {trade, vendor_ids} · `GET /projects/{id}/quotes?trade=&kind=estimate` · `GET /projects/{id}/compare?trade=` |
| 실측 · 확정 | `POST /projects/{id}/visits` · `GET /projects/{id}/quotes?kind=final` · `POST /projects/{id}/trades/{trade}/confirm` · `POST /projects/{id}/trades/{trade}/reselect` |
| 일정 · 이력 | `GET /projects/{id}/schedule` · `GET /projects/{id}/history` |
| 업체 | `GET /vendor/inbox` · `GET /vendor/requests/{id}` · `POST /vendor/requests/{id}/quote` · `GET /vendor/visits/{id}` · `POST /vendor/visits/{id}/seen` · `POST /vendor/visits/{id}/quote` · `PUT /vendor/projects/{id}/trades/{trade}/period` · `GET/PATCH /vendor/profile` |
| 관리자 | `GET /admin/members?role=` · `PATCH /admin/members/{id}` · `GET /admin/vendors?status=` · `POST /admin/vendors/{id}/approve` · `POST /admin/vendors/{id}/reject` · `PATCH /admin/vendors/{id}` |

호출 흐름 예: `web → POST /api/projects → project.service → calc · (큐 → worker → agent) → PostgreSQL`.

## 8. 지금 상태와 '실제로 등록'에 필요한 작업

### 지금

- 견적 받기 답은 브라우저(localStorage)에만 있다. '프로젝트 만들기'는 예시 프로젝트 p1로 이동할 뿐 저장하지 않는다.
- 로그인은 데모 쿠키다. 비밀번호 확인 · 회원 저장이 없다.
- 백엔드는 `/health/live`, `/health/ready`뿐이고, Alembic 기준 버전(0001)은 비어 있다.
- 금액 · 일정은 `frontend/lib/mock/fixtures.json`(v6 계산 엔진 + 2026 공공 단가로 미리 만든 값)에서 온다.

### 실제로 등록되게 하려면 (순서대로)

1. **인증 · 역할**: users · vendors 테이블, 비밀번호 해시(argon2), httpOnly 세션 쿠키, 역할 · 업체 승인 상태로 접근 막기. 업체 가입 · 관리자 승인.
2. **파일 저장소**: 사진 · 도면 · 사업자등록증을 둘 곳(로컬 볼륨 → 운영은 S3 같은 객체 저장소), 형식 · 용량 제한, 업체에게 보여 줄 권한 규칙.
3. **프로젝트 생성 API**: Pydantic 검사, 공간 · 공정 · 파일 저장. 동 · 호수는 실측 요청 때만 받고 암호화([privacy-rules.md](privacy-rules.md)).
4. **계산 엔진 이식**: mitjip-v6 `calc.js`의 수량 · 표준견적 · 공정표를 `backend/app/calc`(Python)로 옮기고 테스트. 기준 단가(`ref_prices`)는 v5 보고서 값으로 시드(출처 · 적용일 포함).
5. **워커 작업**: 프로젝트를 만들면 예상 공정표 · 표준견적서 · 추천을 만든다. LLM은 설명만, CI는 스텁(`LLM_LIVE=false`).
6. **가견적 · 실측 · 확정 · 공사기간 API**와 업체 화면.
7. **프런트 연결**: `lib/api.ts` 안을 `API_INTERNAL_URL` 호출로 바꾸고, 브라우저 쪽 변경은 `/api`로. OpenAPI로 타입 생성(`openapi-typescript`).
8. **테스트 · CI**: 계산 엔진, 상태 변경, 권한(업체가 남의 요청 주소를 못 봄), 개인정보 가림 (AGENTS.md 10장).

## 9. 진행 제안

**1단계 · 목데이터로 전체 흐름 (프런트만)**

- `lib/mock/flow.ts`에 '가상 서버' 상태를 두고, 쿠키에 저장해 서버 화면도 같은 상태를 읽는다. 고객 · 업체 · 관리자 화면이 모두 이 상태를 읽고 쓴다.
- 데모 계정: 고객 1, 업체 3(승인 2 · 승인대기 1), 관리자 1. 한 브라우저에서 계정만 바꿔 처음부터 끝까지 돌려 볼 수 있다.
- `lib/api.ts` 함수 이름과 인자를 7장 API와 맞춰 두어, 2단계에서 안쪽만 바꾼다.
- 금액은 목데이터에서: 업체 가견적서 양식은 그 업체 단가로 미리 채워 두고(v6 계산 결과), 업체가 고칠 수 있게 한다. 합계는 목 API가 계산한다(나중에 서버 계산 엔진).
- 한계: 저장은 그 브라우저에만, 데모 프로젝트는 1개, 숫자는 예시 집(34평형) 기준.

**2단계 · 백엔드를 기능 단위로** — 8장 1 → 7 순서. 한 단위마다 API + 테이블 + 화면 연결 + 테스트를 함께 끝낸다.

## 10. 결정 (2026-10-29, 모두 권장안)

1. 진행 방식: 1단계(목데이터 흐름) 먼저 → 2단계 (권장) / 바로 백엔드부터.
2. 가견적서 · 실측 견적서 양식: 표준 행 양식 (권장) / 총액 + 파일 첨부만.
3. 업체의 가능 공정 · 시공 지역 · 소개를 어디서 받을지: **바뀜 (2026-10-29 PO)** — 가입은 사업자등록증만, 업체 정보는 승인 뒤 업체 정보 관리(FFV-08)에서. 요구사항 FFV-01 항목을 고쳐야 한다.
4. 실측 일정: 고객 희망일 · 시간대를 보내고 업체는 '확인'만 (권장, FFV-04 그대로) / 업체가 날짜를 다시 제안.
5. 다시 고르기: 이미 가견적 받은 다른 업체에 바로 실측 요청 + 새 업체에 가견적 요청 둘 다 허용 (권장, FFW-14) / 업체 고르기부터 다시.
6. AGENTS.md 1 · 4장(가견적 정의, 에이전트 범위)을 v3.2에 맞게 고치고 ADR 0002로 남길지.
7. 1단계 데모 프로젝트를 1개로 둘지 (권장, 쿠키 크기) / 여러 개.
