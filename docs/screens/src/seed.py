"""화면설계서 캡처용 시험 데이터 (로컬 개발 서버 전용).

계정 비밀번호는 실행할 때 새로 만들어 MJ_SCREENS_STATE 파일(저장소 밖)에만 둔다.
cleanup은 이 파일에 적힌 시험 계정만 지운다.
"""

import io
import json
import os
import secrets
import subprocess
from datetime import date, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WEB = os.environ.get("MJ_WEB", "http://localhost:3100")
API = f"{WEB}/api"
ROOT = Path(__file__).resolve().parents[3]  # mitjip/
STATE = Path(os.environ["MJ_SCREENS_STATE"])
FONT = "C:/Windows/Fonts/malgun.ttf"

ACCOUNTS = {
    "customer": {"name": "김민지", "email": "screens-customer@example.com"},
    "pending": {"name": "이서준", "email": "screens-vendor-pending@example.com"},
    "rejected": {"name": "박지호", "email": "screens-vendor-rejected@example.com"},
    "approved": {"name": "최유나", "email": "screens-vendor-approved@example.com"},
    "admin": {"name": "관리자", "email": "screens-admin@example.com"},
}
REJECT_REASON = "사업자등록증 글자가 흐려서 사업자등록번호를 확인할 수 없어요. 선명한 사진이나 PDF로 다시 올려 주세요."


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def room_photo(seed: int) -> bytes:
    """벽 · 바닥 · 창이 있는 방 그림 (시험용 사진)."""
    w, h = 1200, 900
    img = Image.new("RGB", (w, h), (236, 230, 219))
    d = ImageDraw.Draw(img)
    wall = [(236, 230, 219), (226, 232, 228), (240, 235, 226)][seed % 3]
    d.rectangle([0, 0, w, h], fill=wall)
    d.polygon([(0, 640), (w, 640), (w, h), (0, h)], fill=(168, 128, 92))
    for x in range(-200, w, 120):
        d.line([(x, h), (x + 160, 640)], fill=(150, 112, 80), width=3)
    d.rectangle([0, 630, w, 646], fill=(250, 250, 248))  # 걸레받이
    d.rectangle([0, 0, w, 18], fill=(250, 250, 248))  # 몰딩
    d.rectangle([380 + seed * 60, 150, 820 + seed * 60, 470], fill=(206, 224, 236), outline=(250, 250, 248), width=14)
    d.line([(600 + seed * 60, 150), (600 + seed * 60, 470)], fill=(250, 250, 248), width=10)
    d.rectangle([60, 250, 230, 640], fill=(214, 196, 170), outline=(250, 250, 248), width=8)
    d.ellipse([200, 440, 214, 454], fill=(120, 100, 80))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return buf.getvalue()


def license_png(company: str) -> bytes:
    """시험용 사업자등록증 그림. 실제 서류가 아님을 크게 적는다."""
    w, h = 900, 1270
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    big, mid, small = (ImageFont.truetype(FONT, s) for s in (52, 30, 24))
    d.rectangle([30, 30, w - 30, h - 30], outline=(60, 60, 60), width=4)
    d.text((w / 2, 130), "사업자등록증", font=big, fill=(20, 20, 20), anchor="mm")
    d.text((w / 2, 200), "(시험용 · 실제 서류가 아니에요)", font=mid, fill=(178, 59, 46), anchor="mm")
    rows = [("상호", company), ("대표자", "시험 대표"), ("등록번호", "000-00-00000"), ("개업연월일", "2019년 3월 4일"), ("사업장 소재지", "서울특별시 (시험용 주소)"), ("업태 · 종목", "건설업 · 실내건축")]
    for i, (k, v) in enumerate(rows):
        y = 320 + i * 90
        d.text((90, y), k, font=mid, fill=(60, 60, 60))
        d.text((330, y), v, font=mid, fill=(20, 20, 20))
        d.line([(90, y + 56), (w - 90, y + 56)], fill=(210, 210, 210), width=2)
    d.text((w / 2, h - 140), "믿집 화면설계서 캡처용 파일", font=small, fill=(120, 120, 120), anchor="mm")
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def _ok(r, what):
    if not r.ok:
        raise SystemExit(f"{what}: {r.status} {r.text()[:300]}")
    return r


def new_ctx(pw):
    return pw.request.new_context(base_url=WEB, extra_http_headers={"Origin": WEB})


def login(pw, role: str, st: dict):
    ctx = new_ctx(pw)
    acc = ACCOUNTS[role]
    _ok(ctx.post("/api/auth/login", data={"email": acc["email"], "password": st["pw"][role]}), f"로그인 {role}")
    return ctx


def seed(pw) -> dict:
    st = load()
    st.setdefault("pw", {})
    # 고객
    if "customer" not in st["pw"]:
        st["pw"]["customer"] = secrets.token_urlsafe(14)
        ctx = new_ctx(pw)
        _ok(ctx.post("/api/auth/signup", data={**ACCOUNTS["customer"], "password": st["pw"]["customer"]}), "고객 가입")
        save(st)
    # 업체 3곳
    for role, company in (("pending", "한결인테리어"), ("rejected", "바른도배"), ("approved", "온집목공")):
        if role in st["pw"]:
            continue
        st["pw"][role] = secrets.token_urlsafe(14)
        ctx = new_ctx(pw)
        _ok(ctx.post("/api/auth/vendor-signup", multipart={
            "name": ACCOUNTS[role]["name"], "email": ACCOUNTS[role]["email"], "password": st["pw"][role],
            "license_file": {"name": "사업자등록증.png", "mimeType": "image/png", "buffer": license_png(company)},
        }), f"업체 가입 {role}")
        save(st)
    # 관리자 (가입 화면이 없어서 CLI로)
    if "admin" not in st["pw"]:
        st["pw"]["admin"] = secrets.token_urlsafe(14)
        env = {**os.environ, "MJ_ADMIN_PASSWORD": st["pw"]["admin"]}
        subprocess.run(["docker", "compose", "exec", "-T", "-e", "MJ_ADMIN_PASSWORD", "api", "python", "-m", "app.auth.cli",
                        "create-admin", "--email", ACCOUNTS["admin"]["email"], "--name", ACCOUNTS["admin"]["name"]],
                       cwd=ROOT, env=env, check=True, capture_output=True)
        save(st)
    # 관리자: 승인 · 반려
    admin = login(pw, "admin", st)
    apps = _ok(admin.get("/api/admin/vendors"), "업체 목록").json()
    by_email = {a["email"]: a for a in apps}
    st["vendor_ids"] = {r: by_email[ACCOUNTS[r]["email"]]["user_id"] for r in ("pending", "rejected", "approved")}
    if by_email[ACCOUNTS["approved"]["email"]]["status"] == "pending":
        _ok(admin.post(f"/api/admin/vendors/{st['vendor_ids']['approved']}/approve"), "승인")
    if by_email[ACCOUNTS["rejected"]["email"]]["status"] == "pending":
        _ok(admin.post(f"/api/admin/vendors/{st['vendor_ids']['rejected']}/reject", data={"reason": REJECT_REASON}), "반려")
    # 고객 프로젝트 하나 (사진 2장)
    if "project_id" not in st:
        cust = login(pw, "customer", st)
        fids = []
        for i in range(2):
            r = _ok(cust.post("/api/files", multipart={"kind": "photo", "file": {"name": f"room-{i + 1}.jpg", "mimeType": "image/jpeg", "buffer": room_photo(i)}}), "사진")
            fids.append(r.json()["id"])
        start = date.today() + timedelta(days=24)
        body = {
            "sido": "seoul", "sgg": "마포구", "house_type": "apt", "built_year": 2009,
            "size": {"band": "30"}, "balcony_ext": True,
            "when": {"kind": "date", "start": start.isoformat(), "end": (start + timedelta(days=5)).isoformat()},
            "occupied": True, "budget": "500-700",
            "spaces": [{"key": "sp-a", "name": "거실"}, {"key": "sp-b", "name": "방 1"}, {"key": "sp-c", "name": "방 2"}, {"key": "sp-d", "name": "주방"}],
            "trades": {"dobae": {"spaces": ["sp-a", "sp-b", "sp-c"], "grade": "basic"},
                       "mokgong": {"spaces": ["sp-a", "sp-d"], "items": ["molding", "base"]}},
            "photos": [{"space": "sp-a", "file_id": fids[0]}, {"space": "sp-b", "file_id": fids[1]}],
            "plans": [],
        }
        st["project_id"] = _ok(cust.post("/api/projects", data=body), "프로젝트").json()["id"]
        save(st)
    save(st)
    return st


def cleanup(pw) -> None:
    """시험 계정만 지운다: 고객 · 업체는 탈퇴 API(파일까지 지움), 관리자는 탈퇴가 막혀 있어 SQL로."""
    st = load()
    for role in ("customer", "pending", "rejected", "approved"):
        if role not in st.get("pw", {}):
            continue
        ctx = new_ctx(pw)
        r = ctx.post("/api/auth/login", data={"email": ACCOUNTS[role]["email"], "password": st["pw"][role]})
        if r.ok:
            _ok(ctx.post("/api/me/withdraw", data={"password": st["pw"][role]}), f"탈퇴 {role}")
    email = ACCOUNTS["admin"]["email"]
    subprocess.run(["docker", "compose", "exec", "-T", "db", "sh", "-c",
                    f"psql -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\" -qc \"delete from users where email = '{email}'\""],
                   cwd=ROOT, check=True, capture_output=True)
    STATE.unlink(missing_ok=True)
