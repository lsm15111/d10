"""작은 SVG 도구: 상자 · 글 · 배지 · 화살표. 믿집 구조도 두 장이 같이 쓴다."""

from html import escape

STYLE = """
.t-title { font-size: 26px; font-weight: 700; fill: #1B2127; }
.t-sub { font-size: 15px; fill: #5A6772; }
.g-label { font-size: 15px; font-weight: 700; fill: #33414D; }
.b-title { font-size: 16px; font-weight: 700; fill: #1B2127; }
.s-title { font-size: 14px; font-weight: 700; fill: #1B2127; }
.b-text { font-size: 14px; fill: #2B353E; }
.b-small { font-size: 13px; fill: #2B353E; }
.b-mute { font-size: 12.5px; fill: #5A6772; }
.a-label { font-size: 12.5px; fill: #4A5762; }
.bd-t { font-size: 12px; font-weight: 700; }
.grp { fill: #F4F5F3; stroke: #C9D0D6; stroke-width: 1.2; }
.box { fill: #FFFFFF; stroke: #2F3B45; stroke-width: 1.5; }
.box-core { fill: #EEF6F2; stroke: #1E6B55; stroke-width: 1.8; }
.box-data { fill: #EEF2F8; stroke: #33507A; stroke-width: 1.8; }
.box-ai { fill: #FFF6EC; stroke: #B5651D; stroke-width: 1.8; }
.box-sub { fill: #FFFFFF; stroke: #9AABC0; stroke-width: 1.1; }
.box-ext { fill: #FFFFFF; stroke: #6B5E45; stroke-width: 1.5; }
.box-off { fill: #FFFFFF; stroke: #B23B2E; stroke-width: 1.5; stroke-dasharray: 7 5; }
.box-dash { fill: #FFFFFF; stroke: #5A6772; stroke-width: 1.4; stroke-dasharray: 7 5; }
.ar { stroke: #2F3B45; stroke-width: 1.6; fill: none; marker-end: url(#ah); }
.ar-q { stroke: #B5651D; stroke-width: 1.6; fill: none; marker-end: url(#ahq); }
.ar-d { stroke: #5A6772; stroke-width: 1.4; fill: none; stroke-dasharray: 6 4; marker-end: url(#ah); }
"""

BADGES = {
    # 구조도 1: 지금 상태
    "now": ("동작", "#1E6B55", "#1E6B55", "#FFFFFF"),
    "next": ("다음", "#2F5DA8", "#2F5DA8", "#FFFFFF"),
    "later": ("나중", "#FFFFFF", "#8A96A0", "#5A6772"),
    "none": ("없음", "#B23B2E", "#B23B2E", "#FFFFFF"),
    "try": ("시험 통과", "#FFFFFF", "#1E6B55", "#1E6B55"),
    "ready": ("만들어 둠", "#FFFFFF", "#2F5DA8", "#2F5DA8"),
    # 구조도 2: 첨부안 대비
    "keep": ("유지", "#1E6B55", "#1E6B55", "#FFFFFF"),
    "chg": ("바꿈", "#B5651D", "#B5651D", "#FFFFFF"),
    "add": ("더함", "#2F5DA8", "#2F5DA8", "#FFFFFF"),
    "drop": ("뺌", "#FFFFFF", "#B23B2E", "#B23B2E"),
}


def text_w(s: str, size: float) -> float:
    w = 0.0
    for ch in s:
        if "가" <= ch <= "힣" or ch in "→←·①②③④⑤":
            w += size * 1.0
        elif ch == " ":
            w += size * 0.3
        else:
            w += size * 0.56
    return w


class Svg:
    def __init__(self, w: int, h: int, title: str, desc: str):
        self.w, self.h = w, h
        self.parts: list[str] = []
        self.title, self.desc = title, desc

    def add(self, s: str):
        self.parts.append(s)

    def rect(self, x, y, w, h, cls="box", rx=10):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>')

    def text(self, x, y, s, cls="b-text", anchor=None):
        a = f' text-anchor="{anchor}"' if anchor else ""
        self.add(f'<text x="{x}" y="{y}" class="{cls}"{a}>{escape(s)}</text>')

    def badge(self, right_x, y, kind):
        """y는 글의 기준선. 오른쪽 끝을 right_x에 맞춘다."""
        label, fill, stroke, tf = BADGES[kind]
        bw = text_w(label, 12) + 18
        x = right_x - bw
        self.add(
            f'<rect x="{x:.1f}" y="{y - 15}" width="{bw:.1f}" height="21" rx="10.5" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
            f'<text x="{x + bw / 2:.1f}" y="{y}" class="bd-t" text-anchor="middle" fill="{tf}">{label}</text>'
        )
        return bw

    def line(self, x, y, s, right_x, kind=None, cls="b-text"):
        self.text(x, y, s, cls)
        if kind:
            self.badge(right_x, y, kind)

    def card(self, x, y, w, h, title, rows, cls="box", kind=None, title_cls="b-title", gap=22):
        """rows: (글, 배지 또는 None, 글 class) 목록"""
        self.rect(x, y, w, h, cls)
        self.text(x + 16, y + 28, title, title_cls)
        if kind:
            self.badge(x + w - 14, y + 27, kind)
        yy = y + 28 + gap + 4
        for r in rows:
            s, k, c = (r + (None, None))[:3] if isinstance(r, tuple) else (r, None, None)
            self.line(x + 16, yy, s, x + w - 14, k, c or "b-text")
            yy += gap

    def arrow(self, pts, cls="ar", label=None, lx=None, ly=None, anchor="start"):
        d = "M " + " L ".join(f"{px} {py}" for px, py in pts)
        self.add(f'<path d="{d}" class="{cls}"/>')
        if label:
            self.text(lx, ly, label, "a-label", anchor)

    def render(self) -> str:
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
            "font-family=\"'Noto Sans KR', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif\" style=\"background:#FAFAF8\">\n"
            f"<title>{escape(self.title)}</title>\n<desc>{escape(self.desc)}</desc>\n<style>{STYLE}</style>\n"
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#2F3B45"/></marker>'
            '<marker id="ahq" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#B5651D"/></marker></defs>\n'
            f'<rect width="{self.w}" height="{self.h}" fill="#FAFAF8"/>\n'
        )
        return head + "\n".join(self.parts) + "\n</svg>\n"
