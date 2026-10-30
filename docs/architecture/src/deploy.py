"""믿집 시스템 구성도 (완성 구성 예시): AWS → EC2 → Docker Compose, 관리형 DB · 파일 · 메일, 배포 · 감시, 외부 API.

  python deploy.py ../system-config.svg
근거: docs/design/target-architecture.md
"""

import sys

from svgkit import Svg

W, H = 1640, 870
s = Svg(W, H, "믿집 시스템 구성도",
        "EC2 한 대의 Docker Compose(Caddy · Next.js · FastAPI · Redis · worker), RDS PostgreSQL · S3 · SES, "
        "GitHub Actions → ECR · SSM 배포, CloudWatch 감시, 외부 OpenAI · 공공데이터 API.")


def a(x):
    s.add(x)


def bar_box(x, y, w, h, title, color):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{color}" stroke-width="1.8"/>')
    a(f'<path d="M{x} {y + 6} a6 6 0 0 1 6 -6 h{w - 12} a6 6 0 0 1 6 6 v24 h-{w} z" fill="{color}"/>')
    a(f'<text x="{x + 14}" y="{y + 21}" font-size="14" font-weight="700" fill="#FFFFFF">{title}</text>')


def tile(x, y, w, icon, title, lines, h=96):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="#2F3B45" stroke-width="1.5"/>')
    icon(x + 14, y + 14)
    s.text(x + 52, y + 33, title, "s-title")
    for i, line in enumerate(lines):
        s.text(x + 14, y + 68 + i * 19, line, "b-mute")


# ── 아이콘 (28px 안에 그린다)
def i_lock(x, y):
    a(f'<rect x="{x}" y="{y}" width="28" height="28" rx="7" fill="#1E6B55"/>'
      f'<path d="M{x + 9} {y + 13} v-3 a5 5 0 0 1 10 0 v3" fill="none" stroke="#fff" stroke-width="2"/>'
      f'<rect x="{x + 7}" y="{y + 13}" width="14" height="10" rx="2" fill="#fff"/>')


def i_next(x, y):
    a(f'<circle cx="{x + 14}" cy="{y + 14}" r="14" fill="#111"/>'
      f'<text x="{x + 14}" y="{y + 19.5}" font-size="15" font-weight="800" fill="#fff" text-anchor="middle">N</text>')


def i_bolt(x, y):
    a(f'<circle cx="{x + 14}" cy="{y + 14}" r="14" fill="#05998B"/>'
      f'<path d="M{x + 16} {y + 4} L{x + 8} {y + 16} H{x + 14} L{x + 12} {y + 24} L{x + 20} {y + 12} H{x + 14} Z" fill="#fff"/>')


def i_gear(x, y):
    cx, cy = x + 14, y + 14
    a("".join(f'<rect x="{cx - 2.5}" y="{cy - 14}" width="5" height="7" rx="1" fill="#B5651D" transform="rotate({k * 45} {cx} {cy})"/>' for k in range(8))
      + f'<circle cx="{cx}" cy="{cy}" r="9" fill="#B5651D"/><circle cx="{cx}" cy="{cy}" r="3.5" fill="#fff"/>')


def i_db(x, y, color="#2F5DA8"):
    a(f'<path d="M{x + 3} {y + 6} v16 a11 4.5 0 0 0 22 0 v-16" fill="{color}"/>'
      f'<ellipse cx="{x + 14}" cy="{y + 6}" rx="11" ry="4.5" fill="#8FB0DA" stroke="{color}" stroke-width="1.5"/>'
      f'<path d="M{x + 3} {y + 14} a11 4.5 0 0 0 22 0" fill="none" stroke="#fff" stroke-width="1.2"/>')


def i_redis(x, y):
    a("".join(f'<path d="M{x + 2} {y + 8 + k * 7} L{x + 14} {y + 3 + k * 7} L{x + 26} {y + 8 + k * 7} L{x + 14} {y + 13 + k * 7} Z" fill="#C8372D" stroke="#fff" stroke-width="1"/>' for k in (2, 1, 0)))


def i_bucket(x, y):
    a(f'<path d="M{x + 3} {y + 6} h22 l-3 18 h-16 z" fill="#3F8624"/><ellipse cx="{x + 14}" cy="{y + 6}" rx="11" ry="3.5" fill="#7DBB57"/>')


def i_mail(x, y):
    a(f'<rect x="{x + 1}" y="{y + 5}" width="26" height="18" rx="3" fill="#DD344C"/>'
      f'<path d="M{x + 3} {y + 8} l11 8 l11 -8" fill="none" stroke="#fff" stroke-width="2"/>')


def i_pulse(x, y):
    a(f'<rect x="{x}" y="{y}" width="28" height="28" rx="7" fill="#E7157B"/>'
      f'<path d="M{x + 4} {y + 15} h5 l3 -6 l4 12 l3 -6 h5" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>')


def i_boxes(x, y):
    a(f'<rect x="{x}" y="{y}" width="28" height="28" rx="7" fill="#ED7100"/>'
      + "".join(f'<rect x="{x + 5 + dx}" y="{y + 5 + dy}" width="8" height="8" rx="1.5" fill="#fff"/>' for dx, dy in ((0, 0), (10, 0), (0, 10), (10, 10))))


def i_globe(x, y):
    cx, cy = x + 14, y + 14
    a(f'<circle cx="{cx}" cy="{cy}" r="13" fill="#8C4FFF"/>'
      f'<ellipse cx="{cx}" cy="{cy}" rx="5.5" ry="12" fill="none" stroke="#fff" stroke-width="1.6"/>'
      f'<path d="M{cx - 12} {cy} h24 M{cx - 10} {cy - 6} h20 M{cx - 10} {cy + 6} h20" stroke="#fff" stroke-width="1.4"/>')


def i_spark(x, y):
    cx, cy = x + 14, y + 14
    a(f'<circle cx="{cx}" cy="{cy}" r="14" fill="#6B4FBB"/>'
      f'<path d="M{cx} {cy - 9} Q{cx + 1.5} {cy - 1.5} {cx + 9} {cy} Q{cx + 1.5} {cy + 1.5} {cx} {cy + 9} Q{cx - 1.5} {cy + 1.5} {cx - 9} {cy} Q{cx - 1.5} {cy - 1.5} {cx} {cy - 9} Z" fill="#fff"/>')


def i_gov(x, y):
    a(f'<path d="M{x + 2} {y + 10} L{x + 14} {y + 3} L{x + 26} {y + 10} Z" fill="#46546A"/>'
      + "".join(f'<rect x="{x + 4 + k * 6}" y="{y + 12}" width="3" height="10" fill="#46546A"/>' for k in range(4))
      + f'<rect x="{x + 2}" y="{y + 23}" width="24" height="3" fill="#46546A"/>')


def i_ci(x, y):
    a(f'<circle cx="{x + 14}" cy="{y + 14}" r="14" fill="#24292F"/>'
      f'<path d="M{x + 8} {y + 14.5} l4 4 l8 -9" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')


def i_user(cx, cy):
    a(f'<circle cx="{cx}" cy="{cy}" r="34" fill="#FFFFFF" stroke="#2D6CB5" stroke-width="2.5"/>'
      f'<circle cx="{cx}" cy="{cy - 9}" r="10" fill="none" stroke="#2D6CB5" stroke-width="2.5"/>'
      f'<path d="M{cx - 19} {cy + 21} a19 16 0 0 1 38 0" fill="none" stroke="#2D6CB5" stroke-width="2.5"/>')


def label(x, y, t, anchor="start", color="#4A5762"):
    an = f' text-anchor="{anchor}"' if anchor != "start" else ""
    a(f'<text x="{x}" y="{y}" font-size="12.5" fill="{color}"{an}>{t}</text>')


def line(pts, both=False, color="#2F3B45"):
    d = "M " + " L ".join(f"{px} {py}" for px, py in pts)
    st = ' marker-start="url(#ah)"' if both else ""
    a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6"{st} marker-end="url(#ah)"/>')


# ── 제목
s.text(32, 44, "믿집 시스템 구성도", "t-title")

# ── 사용자
i_user(90, 350)
s.text(90, 410, "사용자", "s-title", anchor="middle")
s.text(90, 430, "고객 · 업체 · 관리자", "b-mute", anchor="middle")

# ── AWS > EC2 > Docker
bar_box(170, 100, 1080, 740, "AWS · 서울 리전", "#232F3E")
bar_box(200, 150, 1000, 330, "EC2 · t4g.small", "#C7511F")
bar_box(228, 196, 944, 264, "Docker Compose", "#1D63ED")

R = 300
tile(240, R, 150, i_lock, "Caddy", ["HTTPS · 프록시"])
tile(430, R, 140, i_next, "Next.js", ["화면"])
tile(610, R, 160, i_bolt, "FastAPI", ["API · 계산 엔진"])
tile(810, R, 140, i_redis, "Redis", ["큐 · 요청 제한"])
tile(990, R, 170, i_gear, "worker", ["에이전트 · 수집 · 메일"])

line([(126, 350), (237, 350)], both=True, color="#2D6CB5")
line([(390, 340), (427, 340)])
label(409, 332, "/", "middle")
line([(315, R), (315, 256), (690, 256), (690, R - 3)])
label(502, 250, "/api", "middle")
line([(570, 368), (607, 368)])
label(589, 360, "읽기", "middle")
line([(770, 340), (807, 340)])
label(789, 332, "큐", "middle")
line([(950, 340), (987, 340)])
label(969, 332, "작업", "middle")

# ── 관리형 서비스 (EC2 밖)
M = 540
tile(420, M, 180, i_bucket, "S3", ["사진 · 도면"])
tile(640, M, 250, i_db, "RDS PostgreSQL", ["데이터 · pgvector"])
tile(1016, M, 150, i_mail, "SES", ["메일 알림"])

line([(700, R + 96), (700, M - 3)])
label(708, 510, "SQL", "start")
line([(1010, R + 96), (1010, 432), (840, 432), (840, M - 3)])
label(925, 426, "저장", "middle")
line([(630, R + 96), (630, 432), (510, 432), (510, M - 3)])
label(570, 426, "파일", "middle")
line([(1120, R + 96), (1120, M - 3)])
label(1128, 510, "메일", "start")

# ── 배포 · 감시
O = 690
tile(420, O, 300, i_pulse, "CloudWatch", ["로그 · 지표 · 알람"])
tile(760, O, 406, i_boxes, "ECR · SSM", ["이미지 · 배포 명령 · 비밀값"])
line([(620, 480), (620, O - 3)])
label(628, 668, "로그", "start")
line([(950, O), (950, 483)])
label(958, 668, "배포", "start")

# ── 밖
EX = 1290
tile(EX, 150, 320, i_ci, "GitHub Actions", ["CI · 이미지 빌드 · 배포"])
tile(EX, 290, 320, i_spark, "OpenAI API", ["설명 · 추천 · 임베딩"])
tile(EX, 430, 320, i_gov, "공공데이터 API", ["건축HUB · 조달청 · 공휴일"])
line([(1160, 330), (EX - 3, 330)])
line([(1160, 375), (1236, 375), (1236, 475), (EX - 3, 475)])
line([(EX + 320, 195), (1626, 195), (1626, 738), (1169, 738)])

open(sys.argv[1], "w", encoding="utf-8").write(s.render())
print("ok")
