"""캡처(../shots)로 화면설계서 HTML · PDF와 화면 흐름 그림을 만든다.

  python build.py            → ../화면설계서.html, ../믿집-화면설계서.pdf, ../화면흐름.png
  python build.py --png 1 5  → 확인용으로 그 쪽만 PNG로 (../preview/)
"""

import json
import sys
from html import escape
from pathlib import Path

from playwright.sync_api import sync_playwright

from screens import SCREENS

DOC = Path(__file__).resolve().parents[1]
SHOTS = DOC / "shots"
TEAM = "SKN34-Final-1Team"
WRITER = "이성민"
# 버전 기록 (2쪽): 버전, 날짜, 작성자, 비고
HISTORY = [
    ("v1.0", "2026-10-29", WRITER, "처음 작성 (요구사항 v3.2 기준, 화면 47쪽)"),
]

PW, PH = 1280, 720
BOX_W, BOX_H = 1216 - 300 - 12, 584
E = escape

CSS = """
@page { size: 1280px 720px; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #e9edf2; }
body { font-family: "Pretendard", "Noto Sans KR", "Malgun Gothic", sans-serif; color: #172233; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 1280px; height: 720px; position: relative; overflow: hidden; background: #fff; page-break-after: always; break-after: page; margin: 0 auto 16px; }
@media print { .page { margin: 0; } body { background: #fff; } }
.top { position: absolute; top: 14px; left: 32px; right: 32px; display: flex; justify-content: flex-end; font-size: 11px; color: #56647a; }
.foot { position: absolute; bottom: 12px; right: 32px; font-size: 11px; color: #56647a; font-variant-numeric: tabular-nums; }
.meta { position: absolute; top: 36px; left: 32px; width: 1216px; border-collapse: collapse; font-size: 12.5px; }
.meta th { background: #3a4659; color: #fff; font-weight: 600; width: 96px; height: 27px; border: 1px solid #3a4659; }
.meta td { border: 1px solid #b8c4d3; padding: 0 12px; height: 27px; }
.meta td.v2 { width: 210px; font-variant-numeric: tabular-nums; }
.body { position: absolute; top: 104px; left: 32px; width: 1216px; height: 584px; display: grid; grid-template-columns: 1fr 300px; gap: 12px; }
.shot { background: #f1f4f8; border: 1px solid #b8c4d3; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.frame { position: relative; box-shadow: 0 1px 4px rgba(23,34,51,.18); }
.frame img { display: block; width: 100%; height: 100%; }
.mk { position: absolute; width: 22px; height: 22px; border-radius: 50%; background: #1f5fae; color: #fff; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 2px #fff; z-index: 2; font-variant-numeric: tabular-nums; }
.ol { position: absolute; border: 2px solid rgba(31,95,174,.85); border-radius: 4px; z-index: 1; }
.desc { border: 1px solid #b8c4d3; display: flex; flex-direction: column; min-height: 0; font-size: 12px; }
.desc h3 { margin: 0; background: #3a4659; color: #fff; font-size: 12.5px; font-weight: 600; text-align: center; padding: 5px 0; }
.desc .sid { padding: 5px 10px; border-bottom: 1px solid #b8c4d3; font-variant-numeric: tabular-nums; }
.items { list-style: none; margin: 0; padding: 0; flex: 1; min-height: 0; overflow: hidden; }
.items > li { display: grid; grid-template-columns: 26px 1fr; border-bottom: 1px solid #d8e2ee; }
.items .n { display: flex; align-items: flex-start; justify-content: center; padding-top: 5px; border-right: 1px solid #d8e2ee; font-weight: 700; color: #1f5fae; font-variant-numeric: tabular-nums; }
.items .c { padding: 4px 8px 5px; line-height: 1.38; }
.dense .items .c { padding: 3px 8px 4px; line-height: 1.32; font-size: 11.5px; } .dense .items b { font-size: 12px; } .dense .items .n { padding-top: 4px; }
.items b, .cp b { display: block; font-size: 12.5px; }
.items ul, .cp ul { margin: 2px 0 0; padding-left: 14px; color: #2c3a4f; }
.cp { padding: 6px 10px 8px; line-height: 1.45; }
/* 표지 */
.cover .logo { position: absolute; top: 44px; left: 60px; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; color: #172233; }
.cover .team { position: absolute; top: 210px; left: 160px; font-size: 26px; font-weight: 700; }
.cover .tag { position: absolute; top: 250px; left: 160px; font-size: 16px; font-weight: 600; color: #2c3a4f; }
.cover .tag::before { content: ""; display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: #2d6cb5; margin-right: 8px; vertical-align: -1px; }
.cover h1 { position: absolute; top: 300px; left: 156px; margin: 0; font-size: 56px; font-weight: 500; letter-spacing: -1px; color: #2a3343; }
.cover .band { position: absolute; left: 0; right: 0; bottom: 0; height: 10px; background: linear-gradient(90deg, #2d6cb5, #b9d3f3); }
/* 목록 · 흐름 */
.sheet { position: absolute; top: 40px; left: 32px; right: 32px; bottom: 34px; display: flex; flex-direction: column; gap: 10px; }
.sheet h2 { margin: 0; font-size: 20px; } .sheet .sub { margin: 0; font-size: 12.5px; color: #46546a; }
.list { width: 100%; border-collapse: collapse; font-size: 12px; }
.list th { background: #3a4659; color: #fff; font-weight: 600; padding: 6px 8px; text-align: left; border: 1px solid #3a4659; }
.list td { border: 1px solid #c9d3df; padding: 4px 8px; vertical-align: top; }
.list td.num, .list td.id { font-variant-numeric: tabular-nums; white-space: nowrap; }
.list tr.grp td { background: #eaf2fc; font-weight: 700; }
.legend { display: flex; gap: 18px; flex-wrap: wrap; font-size: 12px; color: #2c3a4f; }
.legend span::before { content: "●"; color: #1f5fae; margin-right: 5px; }
"""


def shot_page(s, m: dict, no: int) -> str:
    sc = min(BOX_W / m["w"], BOX_H / m["h"])
    fw, fh = m["w"] * sc, m["h"] * sc
    marks = []
    for k in m["marks"]:
        x, y, w, h = (v * sc for v in k["box"])
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(fw, x + w), min(fh, y + h)
        if x1 > x0 and y1 > y0:
            marks.append(f'<div class="ol" style="left:{x0 - 3:.1f}px;top:{y0 - 3:.1f}px;width:{x1 - x0 + 6:.1f}px;height:{y1 - y0 + 6:.1f}px"></div>')
        cx = min(max(0, x0 - 19), fw - 22)
        cy = min(max(0, y0 - 17), fh - 22)
        marks.append(f'<div class="mk" style="left:{cx:.1f}px;top:{cy:.1f}px">{k["n"]}</div>')
    items = "".join(
        f'<li><span class="n">{k["n"]}</span><div class="c"><b>{E(k["title"])}</b>'
        + ("<ul>" + "".join(f"<li>{E(d)}</li>" for d in k["desc"]) + "</ul>" if k["desc"] else "")
        + "</div></li>"
        for k in m["marks"]
    )
    cp = ""
    if s.check:
        t, lines = s.check
        cp = f'<h3>Check Point</h3><div class="cp"><b>{E(t)}</b><ul>{"".join(f"<li>{E(x)}</li>" for x in lines)}</ul></div>'
    return f"""
<section class="page">
  {top()}
  <table class="meta">
    <tr><th>화면명</th><td>{E(s.name)}</td><th>요구사항 ID</th><td class="v2">{E(s.req)}</td></tr>
    <tr><th>화면 경로</th><td>{E(s.path)} <span style="color:#56647a">· {E(url_of(s))}</span></td><th>화면 ID</th><td class="v2">{s.id}</td></tr>
  </table>
  <div class="body">
    <div class="shot"><div class="frame" style="width:{fw:.1f}px;height:{fh:.1f}px"><img src="shots/{s.key}.jpg" alt="{E(s.name)} 화면">{"".join(marks)}</div></div>
    <div class="desc{" dense" if len(m["marks"]) > 4 else ""}"><h3>Description</h3><div class="sid">{s.id}{f" · {s.part}" if s.part > 1 else ""}</div><ol class="items">{items}</ol>{cp}</div>
  </div>
  {foot(no)}
</section>"""


def url_of(s) -> str:
    """견적 받기 창은 열려도 주소가 바뀌지 않는다. 같은 질문을 한 화면으로 보여 주는 주소가 /start다."""
    return "/start" if s.dialog else s.url.replace("{pid}", "[id]").replace("{vid}", "[id]")


def top() -> str:
    return f'<div class="top"><span>{TEAM}</span></div>'


def foot(no: int) -> str:
    return f'<div class="foot">{no}</div>'


def cover() -> str:
    return f"""
<section class="page cover">
  <div class="logo">믿집</div>
  <div class="team">{TEAM}</div>
  <div class="tag">믿집: 아파트 도배 · 목공 견적을 공공 기준과 비교하며 업체를 고르는 서비스</div>
  <h1>믿집 화면설계서</h1>
  <div class="band"></div>
</section>"""


def index_pages(first_page: dict, start_no: int) -> list[str]:
    rows, last = [], None
    for s in SCREENS:
        if s.part != 1:
            continue
        if s.group != last:
            rows.append(f'<tr class="grp"><td colspan="6">{E(s.group)}</td></tr>')
            last = s.group
        url = url_of(s)
        name = s.name.split(' · ')[0] if sum(x.id == s.id for x in SCREENS) > 1 else s.name
        rows.append(f'<tr><td class="id">{s.id}</td><td>{E(name)}</td><td class="id">{E(url)}</td><td>{E(s.req)}</td><td>{E(s.path)}</td><td class="num">{first_page[s.id]}</td></tr>')
    per = 20
    chunks = [rows[i:i + per] for i in range(0, len(rows), per)]
    pages = []
    for i, ch in enumerate(chunks):
        head = "화면 목록" + (f" ({i + 1}/{len(chunks)})" if len(chunks) > 1 else "")
        pages.append(f"""
<section class="page">
  {top()}
  <div class="sheet"><h2>{head}</h2>
    <table class="list"><tr><th style="width:96px">화면 ID</th><th style="width:190px">화면명</th><th style="width:190px">URL</th><th style="width:170px">요구사항 ID</th><th>화면 경로</th><th style="width:40px">쪽</th></tr>{"".join(ch)}</table>
  </div>
  {foot(start_no + i)}
</section>""")
    return pages


def flow_svg() -> str:
    """사용자별 화면 흐름: 고객 · 업체 · 관리자."""
    bw, bh = 196, 58
    xs = [130 + i * 222 for i in range(5)]
    parts = []

    def box(x, y, t, sid, cls="b", w=bw):
        dash = ' stroke-dasharray="6 4"' if cls == "plan" else ""
        fill = {"b": "#ffffff", "core": "#eaf2fc", "plan": "#ffffff", "adm": "#f4f6f9"}[cls]
        stroke = {"b": "#7489a6", "core": "#2d6cb5", "plan": "#7489a6", "adm": "#7489a6"}[cls]
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{bh}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{dash}/>')
        parts.append(f'<text x="{x + 12}" y="{y + 24}" font-size="14" font-weight="700" fill="#172233">{E(t)}</text>')
        parts.append(f'<text x="{x + 12}" y="{y + 44}" font-size="11.5" fill="#46546a">{E(sid)}</text>')

    def arrow(pts, dash=False, color="#46546a"):
        d = "M " + " L ".join(f"{a} {b}" for a, b in pts)
        da = ' stroke-dasharray="6 4"' if dash else ""
        parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6"{da} marker-end="url(#ah)"/>')

    def lane(y, h, label):
        parts.append(f'<rect x="0" y="{y}" width="1216" height="{h}" rx="10" fill="#f7f9fc" stroke="#d8e2ee"/>')
        parts.append(f'<text x="22" y="{y + 30}" font-size="15" font-weight="800" fill="#172233">{E(label)}</text>')

    lane(0, 222, "고객")
    lane(236, 112, "업체")
    lane(362, 112, "관리자")
    r1, r2 = 22, 132
    row1 = [("홈 · 자주 묻는 질문", "SC-01-001 · 005"), ("견적 받기 질문 12개", "SC-02-001 ~ 012"), ("로그인 · 회원가입", "SC-01-002 · 003"), ("진행 현황 · 내 프로젝트", "SC-03-001 ~ 003"), ("1 예상 공정표", "SC-03-004 · FAG-01")]
    row2 = [("2 표준견적서", "SC-03-005"), ("3 업체 고르기 · 상세", "SC-03-006 · 007 · FAG-02"), ("가견적 요청", "SC-03-008"), ("4 가견적 비교 · 실측 요청", "SC-03-009"), ("5 실측 견적 → 6 확정 공정표", "SC-03-010 · 011")]
    for i, (t, sid) in enumerate(row1):
        box(xs[i], r1, t, sid, "core" if i == 4 else "b")  # 에이전트: 예상 공정표
        if i:
            arrow([(xs[i - 1] + bw, r1 + bh / 2), (xs[i] - 3, r1 + bh / 2)])
    for i, (t, sid) in enumerate(row2):
        box(xs[i], r2, t, sid, "core" if i == 1 else "b")  # 에이전트: 업체 추천
        if i:
            arrow([(xs[i - 1] + bw, r2 + bh / 2), (xs[i] - 3, r2 + bh / 2)])
    arrow([(xs[4] + bw / 2, r1 + bh), (xs[4] + bw / 2, r1 + bh + 26), (xs[0] + bw / 2, r1 + bh + 26), (xs[0] + bw / 2, r2 - 3)])
    parts.append(f'<text x="{xs[1] + 8}" y="{r1 + bh + 20}" font-size="11.5" fill="#46546a">프로젝트를 만들면 1 → 6단계 순서 · 이력(SC-03-012)은 언제든</text>')

    vy = 236 + 36
    vx = [130 + i * 182 for i in range(6)]
    vb = [("업체 회원가입", "SC-04-001", "b"), ("업체 홈 · 승인 대기", "SC-04-002", "b"), ("업체 홈 · 승인", "SC-04-002 · 3", "b"),
          ("견적 요청함 · 가견적서", "FFV-02 · 03 (다음)", "plan"), ("실측 · 실측 견적서", "FFV-04 · 05 (다음)", "plan"), ("공사기간 · 업체 정보", "FFV-06 ~ 08 (다음)", "plan")]
    for i, (t, sid, c) in enumerate(vb):
        box(vx[i], vy, t, sid, c, w=164)
        if i and i != 2:
            arrow([(vx[i - 1] + 164, vy + bh / 2), (vx[i] - 3, vy + bh / 2)], dash=c == "plan")
    ay = 362 + 36
    ab = [("업체관리 목록", "SC-05-002"), ("업체 신청 상세", "SC-05-003"), ("승인 · 반려(사유)", "SC-05-003 · 2"), ("회원관리", "SC-05-001 (예시)")]
    ax = [vx[0], vx[1] + 40, vx[2] + 40, vx[4] + 20]
    for i, (t, sid) in enumerate(ab):
        box(ax[i], ay, t, sid, "adm", w=164)
    arrow([(ax[0] + 164, ay + bh / 2), (ax[1] - 3, ay + bh / 2)])
    arrow([(ax[1] + 164, ay + bh / 2), (ax[2] - 3, ay + bh / 2)])
    arrow([(vx[0] + 82, vy + bh), (vx[0] + 82, ay - 3)])  # 가입 → 관리자 목록
    parts.append(f'<text x="{vx[0] + 90}" y="{vy + bh + 22}" font-size="11.5" fill="#46546a">가입 신청</text>')
    arrow([(ax[2] + 82, ay), (ax[2] + 82, vy + bh + 3)])  # 승인 → 업체 홈
    parts.append(f'<text x="{ax[2] + 90}" y="{vy + bh + 22}" font-size="11.5" fill="#46546a">승인하면 업체 홈이 바뀜</text>')
    # 고객 ↔ 업체 (다음 단계)
    arrow([(xs[2] + bw / 2, r2 + bh), (xs[2] + bw / 2, 222 + 7), (vx[3] + 60, 222 + 7), (vx[3] + 60, vy - 3)], dash=True, color="#2d6cb5")
    parts.append(f'<text x="{xs[2] + bw / 2 + 8}" y="{222 - 2}" font-size="11.5" fill="#2d6cb5">가견적 요청 → 업체에게</text>')
    arrow([(vx[3] + 120, vy), (vx[3] + 120, 222 + 16), (xs[3] + bw / 2 + 30, 222 + 16), (xs[3] + bw / 2 + 30, r2 + bh + 3)], dash=True, color="#2d6cb5")

    svg = (f'<svg width="1216" height="476" viewBox="0 0 1216 476" font-family="Pretendard, Noto Sans KR, Malgun Gothic, sans-serif">'
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="context-stroke"/></marker></defs>'
           + "".join(parts) + "</svg>")
    return svg


def version_page(no: int) -> str:
    rows = "".join(f'<tr><td class="id">{E(v)}</td><td class="id">{E(d)}</td><td>{E(w)}</td><td>{E(c)}</td></tr>' for v, d, w, c in HISTORY)
    return f"""
<section class="page">
  {top()}
  <div class="sheet"><h2>버전 기록</h2>
    <table class="list"><tr><th style="width:90px">버전</th><th style="width:120px">날짜</th><th style="width:200px">작성자</th><th>비고</th></tr>{rows}</table>
  </div>
  {foot(no)}
</section>"""


def flow_image(pw) -> Path:
    """화면 흐름을 화면설계서와 따로 그림 한 장으로 만든다."""
    html = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS} body {{ background: #fff; }}'
            '.flow { width: 1280px; padding: 28px 32px 24px; display: flex; flex-direction: column; gap: 12px; }</style></head><body>'
            '<div class="flow sheet" style="position: static"><h2>믿집 화면 흐름</h2>'
            f'{flow_svg()}</div></body></html>')
    src = DOC / "preview-flow.html"
    src.write_text(html, encoding="utf-8")
    out = DOC / "화면흐름.png"
    page = pw.chromium.launch(channel="chrome").new_page(viewport={"width": PW, "height": 600}, device_scale_factor=2)
    page.goto(src.as_uri(), wait_until="networkidle")
    page.locator(".flow").screenshot(path=str(out))
    page.context.browser.close()
    src.unlink()
    return out


def export_deck(meta: dict, first: dict, index_start: int) -> None:
    """PPT(pptx.js)가 쓰는 데이터. PDF와 같은 원본에서 뽑는다."""
    rows, last = [], None
    for s in SCREENS:
        if s.part != 1:
            continue
        if s.group != last:
            rows.append({"group": s.group})
            last = s.group
        name = s.name.split(" · ")[0] if sum(x.id == s.id for x in SCREENS) > 1 else s.name
        rows.append({"id": s.id, "name": name, "url": url_of(s), "req": s.req, "path": s.path, "page": first[s.id]})
    per = 20
    chunks = [rows[i:i + per] for i in range(0, len(rows), per)]
    screens = [{"id": s.id, "part": s.part, "key": s.key, "group": s.group, "name": s.name, "path": s.path, "url": url_of(s), "req": s.req,
                "img": str((SHOTS / f"{s.key}.jpg").resolve()), "w": meta[s.key]["w"], "h": meta[s.key]["h"], "marks": meta[s.key]["marks"],
                "check": list(s.check) if s.check else None} for s in SCREENS]
    data = {"team": TEAM, "history": HISTORY, "index": [{"title": "화면 목록" + (f" ({i + 1}/{len(chunks)})" if len(chunks) > 1 else ""), "rows": ch} for i, ch in enumerate(chunks)],
            "index_start": index_start, "screens": screens}
    (SHOTS / "deck.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def build() -> Path:
    meta = json.loads((SHOTS / "meta.json").read_text(encoding="utf-8"))
    n_index = -(-sum(1 + (1 if i == 0 or SCREENS[i - 1].group != s.group else 0) for i, s in enumerate(SCREENS) if s.part == 1) // 20)
    no = 1 + 1 + n_index + 1  # 표지 · 버전 기록 · 목록 다음
    first, body = {}, []
    for s in SCREENS:
        first.setdefault(s.id, no)
        body.append(shot_page(s, meta[s.key], no))
        no += 1
    pages = [cover(), version_page(2), *index_pages(first, 3), *body]
    export_deck(meta, first, 3)
    html = f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>믿집 화면설계서</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    out = DOC / "화면설계서.html"
    out.write_text(html, encoding="utf-8")
    return out


if __name__ == "__main__":
    html = build()
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": PW, "height": PH})
        page.goto(html.as_uri(), wait_until="networkidle")
        if "--png" in sys.argv:
            prev = DOC / "preview"
            prev.mkdir(exist_ok=True)
            for n in map(int, sys.argv[sys.argv.index("--png") + 1:]):
                page.locator("section.page").nth(n - 1).screenshot(path=str(prev / f"p{n:02d}.png"))
            print("preview ok")
        else:
            page.emulate_media(media="print")
            pdf = DOC / "믿집-화면설계서.pdf"
            page.pdf(path=str(pdf), width=f"{PW}px", height=f"{PH}px", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            print(f"{pdf.name}: {pdf.stat().st_size / 1e6:.1f}MB, {page.locator('section.page').count()}쪽")
        b.close()
        if "--png" not in sys.argv:
            print(f"{flow_image(pw).name} ok")
