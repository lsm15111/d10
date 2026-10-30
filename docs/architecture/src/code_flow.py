import sys

from svgkit import Svg

W, H = 1800, 960
s = Svg(W, H, "믿집 코드 흐름",
        "요청 하나가 어떤 파일을 차례로 지나가는지: 층 8개와 대표 흐름 4개(화면 읽기, 프로젝트 만들기, 업체 가입 · 승인, 오류).")

s.text(24, 42, "믿집 코드 흐름 (요청 하나가 지나가는 파일)", "t-title")
s.text(24, 70, "2026-10-29 · 위: 층과 대표 파일 · 아래: 자주 쓰는 흐름 4개 · 화살표 방향으로만 부른다 (AGENTS.md 2장)", "t-sub")

# ── 층 8개
layers = [
    ("1 화면", "box", ["components/*.tsx", "Wizard · LoginForm 등", "'use client'는 입력 · 클릭만"]),
    ("2 Next 서버", "box", ["app/**/page.tsx", "lib/api.ts → server.ts", "lib/session.ts (GET /me)"]),
    ("3 넘기기", "box", ["개발: next.config.ts", "운영: Caddy /api/*", "쓰기: lib/backend/client.ts"]),
    ("4 API 입구", "box-core", ["main.py", "CatchAll → BodyLimit", "→ Origin 확인 · errors.py"]),
    ("5 router", "box-core", ["router.py: HTTP 모양", "deps.py: 쿠키 → 회원", "ratelimit.py: 횟수 제한"]),
    ("6 service", "box-core", ["service.py: 업무 흐름", "검사 · 상태 변경 · commit", "다른 기능은 service로만"]),
    ("7 저장 경계", "box-data", ["repository.py: SQL", "files/storage.py: 디스크", "files/images.py: 사진 정리"]),
    ("8 저장소", "box-data", ["PostgreSQL (원본)", "files-data 볼륨 (파일)", "Redis (횟수 · 큐)"]),
]
bw, gap, top = 206, 15, 96
for i, (title, cls, lines) in enumerate(layers):
    x = 24 + i * (bw + gap)
    s.rect(x, top, bw, 150, cls)
    s.text(x + 14, top + 28, title, "b-title")
    for j, line in enumerate(lines):
        s.text(x + 14, top + 58 + j * 26, line, "b-mute" if j else "b-small")
    if i < len(layers) - 1:
        s.arrow([(x + bw, top + 75), (x + bw + gap - 1, top + 75)], "ar")

s.text(24, 284, "calc(계산 엔진)는 service가 부르는 순수 함수, agent는 worker가 부른다 — 둘 다 DB에 쓰지 않는다. 다른 기능 router끼리는 import하지 않는다.", "b-small")

# ── 흐름 4개
flows = [
    ("화면 읽기", "내 프로젝트 /my", [
        ("app/my/page.tsx", "Server Component"),
        ("lib/session.ts", "GET /me로 로그인 확인"),
        ("lib/api.ts → server.ts", "GET /projects|브라우저 쿠키를 넘김"),
        ("project/router.py", "require_role(customer)"),
        ("project/service.py", "list_mine"),
        ("project/repository.py", "내 프로젝트 SELECT"),
        ("ProjectListItem JSON", "OpenAPI 타입 그대로"),
        ("ProjectCard.tsx", "공정별 상태 한 줄|버튼 하나"),
    ]),
    ("화면 쓰기", "프로젝트 만들기", [
        ("Wizard.tsx finish()", "GET /me: 로그인 · 역할"),
        ("client.ts call()", "POST /files|사진마다 한 번"),
        ("files/service.upload_by", "횟수 제한 · 권한|DB 연결 먼저 돌려줌"),
        ("files/images.py", "GPS · EXIF 지움|작업 스레드 · 1장씩"),
        ("storage.save → File 행", "DB가 실패하면|디스크 파일도 지움"),
        ("POST /projects", "project/service.create|지역 · 날짜 검사"),
        ("files.service.owned", "내 파일 · 안 쓴 파일"),
        ("commit", "겹치면 409|성공 → /projects/{id}"),
    ]),
    ("업체 가입 · 승인", "FFV-01 · FAD-02", [
        ("VendorSignupForm.tsx", "이름 · 이메일 · 비밀번호|사업자등록증"),
        ("vendor/router.py", "multipart|→ VendorSignupIn"),
        ("vendor/service.signup", "가입 횟수 제한 (IP)"),
        ("files.prepare(license)", "DB 쓰기 전에|형식 · 크기 검사"),
        ("auth.create_user", "Vendor 행 (pending)|세션 · commit"),
        ("/vendor 업체 홈", "승인 대기 표시"),
        ("관리자 VendorReview", "POST …/approve|또는 reject(사유)"),
        ("repository.set_status", "조건부 UPDATE|아니면 409"),
    ]),
    ("오류", "모든 흐름", [
        ("어느 층이든 AppError", "status · code · message"),
        ("app_error_handler", '{"error": {code, message}}'),
        ("검사 실패 (Pydantic)", "422 · fields: 칸별 문장"),
        ("FastAPI 404 · 405 · 413", "http_error_handler|같은 모양"),
        ("예상 못 한 오류", "CatchAll: 500|DB 연결 문제면 503"),
        ("로그", "오류 종류 · 위치만|SQL 값 숨김"),
        ("client.ts ApiError", "message를|그대로 보여 줌"),
        ("화면", "칸 옆 · 위 요약에|초점 옮김"),
    ]),
]
row_h, y0 = 150, 314
sw, sg, sx = 182, 12, 196
for r, (name, sub, steps) in enumerate(flows):
    y = y0 + r * row_h
    s.rect(16, y, W - 32, row_h - 14, "grp")
    s.text(30, y + 30, name, "g-label")
    s.text(30, y + 54, sub, "b-mute")
    for i, (t, d) in enumerate(steps):
        x = sx + i * (sw + sg)
        s.rect(x, y + 14, sw, row_h - 42, "box-sub", rx=8)
        s.text(x + 10, y + 40, t, "s-title")
        for j, part in enumerate(d.split("|")):
            s.text(x + 10, y + 64 + j * 20, part, "b-mute")
        if i < len(steps) - 1:
            s.arrow([(x + sw, y + 14 + (row_h - 42) / 2), (x + sw + sg - 1, y + 14 + (row_h - 42) / 2)], "ar")

open(sys.argv[1], "w", encoding="utf-8").write(s.render())
print("ok")
