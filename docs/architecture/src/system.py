import sys

from svgkit import Svg

s = Svg(1800, 1250, "믿집 시스템 구조 (요구사항 v3.2)",
        "FastAPI 한 앱(기능별 패키지) + Next.js 화면 + PostgreSQL 17 + Redis + arq worker. 배지는 2026-10-29 지금 상태: 동작 · 다음 · 나중 · 만들어 둠.")

s.text(24, 42, "믿집 시스템 구조 (요구사항 v3.2)", "t-title")
s.text(24, 70, "2026-10-29 · FastAPI 한 앱(기능별 패키지) + Next.js + PostgreSQL 17 · Redis · arq · 서비스 분리 · k8s · 메시지 브로커 없음 · 배지 = 지금 상태", "t-sub")

# ── 사용자
s.rect(16, 96, 208, 560, "grp")
s.text(30, 122, "사용자 (브라우저)", "g-label")
s.card(28, 138, 184, 150, "고객", [("견적 받기 · 프로젝트", None, "b-small"), ("마이페이지 · 탈퇴", None, "b-small"), ("비교 · 실측 · 확정은 예시", None, "b-mute")], kind="now", gap=24)
s.card(28, 302, 184, 160, "업체", [("가입 · 사업자등록증", None, "b-small"), ("업체 홈 · 승인 상태", None, "b-small"), ("가견적서 · 실측 견적서", None, "b-mute"), ("화면은 다음", None, "b-mute")], kind="now", gap=24)
s.card(28, 476, 184, 160, "관리자", [("업체 가입 승인 · 반려", None, "b-small"), ("사업자등록증 보기", None, "b-small"), ("계정은 명령어로 만듦", None, "b-mute"), ("회원 목록은 예시", None, "b-mute")], kind="now", gap=24)

# 범례
s.rect(16, 672, 208, 282, "grp")
s.text(30, 698, "범례", "g-label")
ly = 730
for k, t in [("now", "만들고 확인함"), ("next", "다음에 만들 것"), ("later", "운영 · 나중"), ("ready", "만들어 둠")]:
    s.badge(98, ly, k)
    s.text(108, ly, t, "b-small")
    ly += 32
s.arrow([(30, ly - 6), (76, ly - 6)], "ar")
s.text(92, ly, "요청 · 바로 응답", "b-small")
s.arrow([(30, ly + 26), (76, ly + 26)], "ar-q")
s.text(92, ly + 32, "작업 큐 (나중에 처리)", "b-small")

# ── EC2 / 개발 PC
s.rect(240, 96, 1180, 1000, "grp")
s.text(256, 122, "EC2 한 대 · Docker Compose (개발은 내 PC의 Docker + pnpm dev)", "g-label")

s.card(256, 140, 250, 176, "Caddy (운영만)", [("HTTPS · 본문 25MB까지", None, "b-small"), ("/api/* → api (헬스체크)", None, "b-small"), ("나머지 → web", None, "b-small"), ("타임아웃 · 연결 유지 60초", None, "b-mute")], kind="later", gap=25)

s.rect(526, 140, 520, 176, "box")
s.text(542, 168, "web · Next.js 16 (화면만, 계산 안 함)", "b-title")
rows = [("읽기: Server Component → API (쿠키 넘김)", "now"), ("쓰기: 브라우저 → 같은 주소 /api (D9)", "now"),
        ("API 타입: OpenAPI → lib/backend/schema.d.ts", "now"), ("업체 가입 · 업체 홈 · 관리자 승인 화면", "now"),
        ("가견적서 · 실측 견적서 · 공사기간 화면", "next")]
y = 198
for t, k in rows:
    s.line(542, y, t, 1032, k, "b-small")
    y += 24

s.card(1066, 140, 334, 176, "Redis 8", [("요청 제한: 로그인 · 가입 · 업로드", "now", "b-small"), ("작업 큐 (arq)", "next", "b-small"), ("짧은 캐시", "later", "b-small"), ("원본이 아님 · 없으면 제한만 풀림", None, "b-mute")], gap=25)

s.arrow([(224, 228), (254, 228)], "ar")
s.arrow([(506, 228), (524, 228)], "ar")

# api
s.rect(256, 352, 780, 344, "box-core")
s.text(272, 380, "api · FastAPI (유일한 공개 API, /api/*) · 프로세스 2개", "b-title")
s.rect(272, 394, 748, 112, "box-sub")
s.text(286, 418, "입구 공통 처리 (모든 요청: CatchAll → BodyLimit → Origin → router)", "s-title")
gate = [("세션 쿠키 · CSRF(Origin) · 남의 것은 404", "now"), ("본문 한도: JSON 1MB · 파일 21MB", "now"),
        ("오류 모양 하나 · DB 장애는 503", "now"), ("비밀번호 해시는 작업 스레드에서", "now")]
for i, (t, k) in enumerate(gate):
    cx = 286 if i % 2 == 0 else 656
    cy = 446 + (i // 2) * 28
    s.line(cx, cy, t, cx + 352, k, "b-small")

s.text(272, 532, "기능 패키지 (router → service → repository)", "s-title")
chips = [("auth", "회원 · 세션", "now"), ("account", "탈퇴", "now"), ("files", "사진 GPS 지움", "now"),
         ("project", "견적 요청", "now"), ("vendor", "가입 · 승인", "now"), ("quote", "견적서", "next"),
         ("visit", "실측 · 확정", "next"), ("schedule", "공정표", "next"), ("refprice", "기준 단가", "next"),
         ("jobs", "작업 원장", "next"), ("agent", "에이전트 3개", "next")]
for i, (name, sub, k) in enumerate(chips):
    cx = 272 + (i % 6) * 125
    cy = 546 + (i // 6) * 58
    s.rect(cx, cy, 119, 50, "box-sub", rx=8)
    s.text(cx + 9, cy + 21, name, "s-title")
    s.badge(cx + 112, cy + 41, k)
    s.text(cx + 9, cy + 41, sub, "b-mute")
s.line(272, 682, "calc: 금액 · 수량 · 기간 · 날짜 · 추천 점수 순수 함수 (v6 엔진 이식)", 1020, "next", "b-small")

# worker
s.rect(1066, 352, 334, 344, "box-ai")
s.text(1082, 380, "worker · arq (<0.29로 묶음)", "b-title")
wrows = [("jobs 행 처리 · 두 번 돌아도 한 번", "next"), ("에이전트 3개 → AI 구조도", "next"), ("기준 단가 수집 (반기 · 연)", "next"),
         ("RAG 문서 넣기", "later"), ("주인 없는 파일 정리", "next")]
y = 414
for t, k in wrows:
    s.line(1082, y, t, 1388, k, "b-small")
    y += 30
s.text(1082, y + 6, "LLM 호출은 여기서만", "b-mute")
s.text(1082, y + 26, "결과 저장 · 상태 변경은 각 기능 service", "b-mute")
s.text(1082, y + 46, "확정 · 서명은 사람이 누를 때만", "b-mute")

s.arrow([(786, 316), (786, 350)], "ar", "/api 넘김 · 쿠키 그대로", 796, 338)
s.arrow([(1036, 600), (1064, 600)], "ar-q")
s.text(1040, 590, "큐", "a-label")
s.arrow([(1233, 316), (1233, 350)], "ar-q")

# PostgreSQL
s.rect(256, 728, 1144, 250, "box-data")
s.text(272, 756, "PostgreSQL 17 · 원본 데이터 · Alembic migration 0001 → 0006 · 연결은 프로세스마다 10개까지", "b-title")
tables = [("계정 · 세션", "users · user_sessions", "now"), ("업체", "vendors (승인 상태 · 등록증)|trades · areas · portfolio (FFV-08 뒤)", "now"),
          ("파일", "files (종류 · 크기 · sha256)|사진은 위치 정보를 지우고 저장", "now"), ("프로젝트", "projects · spaces · files|trades (도배 유형 · 목공 항목)", "now"),
          ("견적", "standard_quotes · quote_requests|quotes · quote_lines (포함 상태 6종)", "next"), ("실측 · 일정", "visits · schedules · events", "next"),
          ("기준 단가", "ref_prices · holidays (적용일별로 쌓음)", "next"), ("AI · 작업", "jobs (작업 원장 · 실행 기록)|rag_documents (나중 pgvector)", "next")]
for i, (t, sub, k) in enumerate(tables):
    cx = 272 + (i % 4) * 280
    cy = 774 + (i // 4) * 96
    s.rect(cx, cy, 268, 84, "box-sub", rx=8)
    s.text(cx + 12, cy + 26, t, "s-title")
    s.badge(cx + 258, cy + 26, k)
    for j, part in enumerate(sub.split("|")):
        s.text(cx + 12, cy + 52 + j * 19, part, "b-mute")
s.arrow([(646, 696), (646, 726)], "ar", "한 트랜잭션: 상태 + events + jobs", 656, 716)
s.arrow([(1233, 696), (1233, 726)], "ar", "결과 저장은 service", 1243, 716)

s.card(256, 996, 360, 84, "migrate (한 번 돌고 끝)", [("api보다 먼저 alembic upgrade head", None, "b-small")], kind="now")
s.card(632, 996, 380, 84, "files-data 볼륨", [("사진 · 도면 · 사업자등록증 (S3는 운영 때)", None, "b-small")], kind="now")
s.card(1028, 996, 372, 84, "백업 · 관측", [("pg_dump → S3 · 오류 알림", None, "b-small")], kind="later")

# ── 외부
s.rect(1436, 96, 348, 1000, "grp")
s.text(1452, 122, "외부 서비스", "g-label")
s.card(1450, 140, 320, 170, "LLM 공급자 (ADR로 하나)", [("app/agent/llm.py 한 곳에서만", None, "b-small"), ("CI는 스텁 (LLM_LIVE=false)", None, "b-small"), ("유료 eval은 PO 승인", None, "b-small"), ("공급자 · 모델 아직 안 정함", None, "b-mute")], kind="next", gap=25)
s.card(1450, 324, 320, 120, "임베딩 모델", [("RAG 문서가 늘면 (AI1)", None, "b-small"), ("LLM과 같은 ADR에서 정함", None, "b-mute")], kind="later", gap=25)
s.card(1450, 458, 320, 170, "공공 기준 데이터", [("표준시장단가 · 시중노임단가", None, "b-small"), ("조달청 가격정보 API", None, "b-small"), ("공휴일 (연 1회)", None, "b-small"), ("일부라도 실패하면 기존 값 유지", None, "b-mute")], kind="next", gap=25)
s.card(1450, 642, 320, 120, "건축HUB (호별 면적)", [("동 · 호수 → 공급 · 전용면적", None, "b-small"), ("실측 요청 때 쓸지 정할 것", None, "b-mute")], kind="later", gap=25)
s.card(1450, 776, 320, 120, "안심번호 · 알림", [("실측 확정 뒤 연락", None, "b-small"), ("실제 번호는 암호화 저장", None, "b-mute")], kind="later", gap=25)
s.arrow([(1400, 420), (1448, 420)], "ar", None)
s.arrow([(1400, 520), (1448, 520)], "ar", None)
s.text(1404, 410, "LLM", "a-label")
s.text(1404, 510, "수집", "a-label")

# ── CI
s.rect(16, 1112, 1768, 122, "grp")
s.text(30, 1138, "CI (GitHub Actions, .github/workflows/ci.yml) · 저장소에 올리면 PR마다 돈다 · main 보호 규칙에서 필수로 건다", "g-label")
s.badge(1770, 1137, "ready")
ci = [("ruff", "lint · format 검사"), ("pytest", "실제 PostgreSQL · Redis"), ("API 타입 비교", "명세 → schema.d.ts diff 0"),
      ("typecheck · lint", "프런트"), ("build", "Next 빌드"), ("lint-imports", "D8 뒤에 더함 · 나중"), ("이미지 빌드", "배포 때 · 나중")]
for i, (t, sub) in enumerate(ci):
    cx = 30 + i * 250
    s.rect(cx, 1152, 236, 66, "box" if i < 5 else "box-dash", rx=8)
    s.text(cx + 12, 1178, t, "s-title")
    s.text(cx + 12, 1202, sub, "b-mute")
    if i < len(ci) - 1:
        s.arrow([(cx + 236, 1185), (cx + 248, 1185)], "ar")

open(sys.argv[1], "w", encoding="utf-8").write(s.render())
print("ok")
