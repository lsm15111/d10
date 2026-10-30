"""화면설계서용 캡처: 로컬 개발 서버(웹 3100 · API)를 띄운 뒤 실행한다.

  MJ_SCREENS_STATE=<저장소 밖 파일> python capture.py [seed | shots [SC-..] | cleanup]

shots: 화면마다 캡처(../shots/SC-xx-xxx.jpg)와 번호 표시 위치(../shots/meta.json)를 만든다.
"""

import io
import json
import sys
import tempfile
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

import seed
from screens import SCREENS

OUT = Path(__file__).resolve().parents[1] / "shots"
W, SCALE = 1440, 1.5
X0, X1 = 104, 1336  # 내용 폭(1200px) 바깥의 빈 여백은 잘라 낸다
BOX_JS = "e => { const r = e.getBoundingClientRect(); return [r.x + scrollX, r.y + scrollY, r.width, r.height]; }"
HIDE = "nextjs-portal { display: none !important; } * { caret-color: transparent !important; }"


def temp_files() -> dict:
    d = Path(tempfile.mkdtemp(prefix="mj-screens-"))
    files = {}
    for i in (1, 2):
        p = d / f"거실-{i}.jpg"
        p.write_bytes(seed.room_photo(i - 1))
        files[f"room{i}"] = str(p)
    p = d / "도면.jpg"
    p.write_bytes(seed.room_photo(2))
    files["plan"] = str(p)
    return files


def shots(pw, only: set[str]) -> None:
    st = seed.seed(pw)
    files = temp_files()
    browser = pw.chromium.launch(channel="chrome")
    roles = {s.role for s in SCREENS if s.role}
    cookies = {r: seed.login(pw, r, st).storage_state()["cookies"] for r in roles}
    OUT.mkdir(exist_ok=True)
    meta_path = OUT / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    problems = []
    for s in SCREENS:
        if only and s.id not in only and s.key not in only:
            continue
        vh = s.vh if s.dialog else 900
        ctx = browser.new_context(viewport={"width": W, "height": vh}, device_scale_factor=SCALE, locale="ko-KR", timezone_id="Asia/Seoul")
        if s.role:
            ctx.add_cookies(cookies[s.role])
        page = ctx.new_page()
        url = s.url.format(pid=st["project_id"], vid=st["vendor_ids"]["pending"])
        page.goto(seed.WEB + url, wait_until="networkidle")
        page.add_style_tag(content=HIDE)
        page.evaluate("document.fonts.ready")
        if s.expand:  # 창 안쪽 스크롤을 펼쳐 전체 내용을 한 번에 찍는다 (이 문서에서만)
            page.add_style_tag(content=".mj-dialog { height: auto !important; } .mj-dialog .mj-wiz-body { overflow: visible !important; }")
        if s.prep:
            s.prep(page, st, files)
            page.wait_for_load_state("networkidle")
            page.add_style_tag(content=HIDE)
        page.wait_for_timeout(250)
        clip = None
        if s.dialog:
            clip = page.locator("dialog.mj-dialog[open]").evaluate(BOX_JS)

        # 캡처 범위
        if s.dialog:
            top, h = 0, vh
        elif isinstance(s.top, str):
            try:
                top = max(0, int(page.locator(s.top).first.evaluate(BOX_JS)[1]) - 40)
            except Exception as e:  # noqa: BLE001
                problems.append(f"{s.key} top: {s.top} ({type(e).__name__})")
                top = 0
            h = s.h
        else:
            top, h = s.top, s.h
        full_h = page.evaluate("document.documentElement.scrollHeight")
        if not s.dialog:
            top = max(0, min(top, full_h - h))
            h = min(h, full_h - top)

        marks = []
        for n, m in enumerate(s.marks, 1):
            try:
                x, y, w, hh = page.locator(m.sel).first.evaluate(BOX_JS, timeout=3000)
            except Exception as e:  # noqa: BLE001
                problems.append(f"{s.key} #{n} {m.title}: {m.sel} ({type(e).__name__})")
                continue
            if clip:  # 창 밖으로 그리지 않게 창 안으로 자른다
                cx, cy, cw, ch = clip
                x1, y1 = min(x + w, cx + cw), min(y + hh, cy + ch)
                x, y = max(x, cx), max(y, cy)
                w, hh = x1 - x, y1 - y
                if w <= 0 or hh <= 0:
                    problems.append(f"{s.key} #{n} {m.title}: 창 안에서 보이지 않음")
                    continue
            if y + hh < top or y > top + h:
                problems.append(f"{s.key} #{n} {m.title}: 캡처 범위 밖 (y={y:.0f}, top={top}, h={h})")
            marks.append({"n": n, "title": m.title, "desc": list(m.desc), "box": [x - X0, y - top, w, hh]})

        png = page.screenshot(full_page=not s.dialog)
        img = Image.open(io.BytesIO(png)).convert("RGB")
        img = img.crop((int(X0 * SCALE), int(top * SCALE), int(X1 * SCALE), int((top + h) * SCALE)))
        img.save(OUT / f"{s.key}.jpg", "JPEG", quality=84, optimize=True)
        meta[s.key] = {"w": X1 - X0, "h": h, "marks": marks}
        ctx.close()
        print(f"{s.key} {s.name}: {len(marks)}/{len(s.marks)}")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    browser.close()
    print("\n".join(["--- 문제"] + problems) if problems else "--- 문제 없음")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "shots"
    with sync_playwright() as pw:
        if cmd == "seed":
            seed.seed(pw)
            print("seed ok")
        elif cmd == "cleanup":
            seed.cleanup(pw)
            print("cleanup ok")
        else:
            shots(pw, set(sys.argv[2:]))
