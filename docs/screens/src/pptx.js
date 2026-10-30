// 화면설계서 PPT: build.py가 만든 ../shots/deck.json으로 PDF와 같은 쪽을 PowerPoint 도형 · 표로 만든다.
//   python build.py   (deck.json · 캡처 준비)
//   node pptx.js      (pptxgenjs 필요: npm install pptxgenjs, 또는 NODE_PATH로 설치 위치를 알려 준다)
// 좌표는 PDF와 같은 1280×720px 기준이고, 96px = 1인치로 바꾼다.
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const DOC = path.resolve(__dirname, "..");
const data = JSON.parse(fs.readFileSync(path.join(DOC, "shots", "deck.json"), "utf8"));
const OUT = path.join(DOC, "믿집-화면설계서.pptx");
const APPLY_THEME = process.env.MJ_APPLY_THEME; // pptx 스킬의 scripts/apply_theme.js 경로 (없으면 테마 색 적용을 건너뜀)

const THEME = {
  name: "Mitjip",
  headFontFace: "Malgun Gothic",
  bodyFontFace: "Malgun Gothic",
  colors: {
    dk1: "172233", lt1: "FFFFFF", dk2: "3A4659", lt2: "F1F4F8",
    accent1: "1F5FAE", accent2: "2D6CB5", accent3: "B9D3F3", accent4: "56647A", accent5: "D8E2EE", accent6: "B8C4D3",
    hlink: "2D6CB5", folHlink: "235A9C",
  },
};

const px = (v) => v / 96; // px → inch
const pt = (v) => Math.round(v * 0.75 * 10) / 10; // CSS px 글자 크기 → pt
const BOX = { x: 32, y: 104, w: 1216 - 300 - 12, h: 584 };
const PANEL = { x: 32 + BOX.w + 12, y: 104, w: 300, h: 584 };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 × 7.5 in = 1280 × 720 px
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "믿집 화면설계서";
pres.author = data.history[0][2];
pres.company = data.team;
// 색은 고정 색값으로 넣는다. 테마 색 번호(schemeClr)로 넣으면 구글 슬라이드 · 한쇼 · Keynote에서 열거나
// 다른 템플릿에 붙여 넣을 때 그 프로그램의 기본 색으로 바뀐다. 테마에도 같은 색을 넣어 PowerPoint 색 고르기 칸과 맞춘다.
const K = { text1: "172233", text2: "3A4659", bg1: "FFFFFF", bg2: "F1F4F8", accent1: "1F5FAE", accent2: "2D6CB5", accent4: "56647A", accent5: "D8E2EE", accent6: "B8C4D3" };

// ── 레이아웃
const teamText = () => ({ text: { text: data.team, options: { x: px(640), y: px(10), w: px(608), h: px(20), fontSize: pt(11), color: K.accent4, align: "right", margin: 0 } } });
const pageNo = { x: px(1168), y: px(696), w: px(80), h: px(18), fontSize: pt(11), color: "56647A", align: "right" };

pres.defineSlideMaster({
  title: "COVER",
  background: { color: K.bg1 },
  objects: [
    { text: { text: "믿집", options: { x: px(60), y: px(36), w: px(200), h: px(40), fontSize: pt(26), bold: true, color: K.text1, margin: 0 } } },
    { rect: { x: 0, y: px(710), w: px(1280), h: px(10), fill: { color: K.accent2 } } },
    { placeholder: { options: { name: "team", type: "body", x: px(160), y: px(206), w: px(900), h: px(36), fontSize: pt(26), bold: true, color: K.text1, align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "tag", type: "body", x: px(182), y: px(250), w: px(900), h: px(24), fontSize: pt(16), bold: true, color: K.text2, align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: px(156), y: px(290), w: px(1000), h: px(90), fontSize: pt(56), color: K.text1, align: "left", valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "SHEET",
  background: { color: K.bg1 },
  objects: [teamText(), { placeholder: { options: { name: "title", type: "title", x: px(32), y: px(34), w: px(900), h: px(34), fontSize: pt(20), bold: true, color: K.text1, align: "left", margin: 0 }, text: "" } }],
  slideNumber: pageNo,
});
pres.defineSlideMaster({
  title: "SCREEN",
  background: { color: K.bg1 },
  objects: [
    teamText(),
    // 화면명은 위 표의 '화면명' 칸 자리에 슬라이드 제목으로 넣는다
    { placeholder: { options: { name: "title", type: "title", x: px(128 + 12), y: px(36), w: px(814 - 24), h: px(27), fontSize: pt(12.5), color: K.text1, align: "left", valign: "middle", margin: 0 }, text: "" } },
  ],
  slideNumber: pageNo,
});

// ── 공통 조각
const headCell = (text, extra = {}) => ({ text, options: { fill: { color: K.text2 }, color: K.bg1, bold: true, align: "center", valign: "middle", ...extra } });
const border = { type: "solid", pt: 0.75, color: K.accent6 };

function listTable(slide, header, widths, rows, y) {
  const total = widths.reduce((a, b) => a + b, 0);
  slide.addTable([header.map((h) => headCell(h, { align: "left" })), ...rows], {
    x: px(32), y: px(y), w: px(total), colW: widths.map(px), rowH: px(24),
    fontSize: pt(12), color: K.text1, valign: "middle", border, margin: [0.03, px(8), 0.03, px(8)], // [위, 오른쪽, 아래, 왼쪽] 인치
  });
}

// ── 1쪽 표지
pres.addSection({ title: "표지" });
{
  const s = pres.addSlide({ masterName: "COVER", sectionTitle: "표지" });
  s.addText(data.team, { placeholder: "team" });
  s.addText("믿집: 아파트 도배 · 목공 견적을 공공 기준과 비교하며 업체를 고르는 서비스", { placeholder: "tag" });
  s.addText("믿집 화면설계서", { placeholder: "title" });
  s.addShape(pres.shapes.OVAL, { x: px(160), y: px(255), w: px(14), h: px(14), fill: { color: K.accent2 }, line: { color: K.accent2, width: 0 }, objectName: "tag-dot" });
}

// ── 2쪽 버전 기록
pres.addSection({ title: "버전 기록" });
{
  const s = pres.addSlide({ masterName: "SHEET", sectionTitle: "버전 기록" });
  s.addText("버전 기록", { placeholder: "title" });
  const rows = data.history.map(([v, d, w, c]) => [v, d, w, c].map((t) => ({ text: t })));
  listTable(s, ["버전", "날짜", "작성자", "비고"], [90, 120, 200, 806], rows, 80);
}

// ── 화면 목록
pres.addSection({ title: "화면 목록" });
data.index.forEach((page) => {
  const s = pres.addSlide({ masterName: "SHEET", sectionTitle: "화면 목록" });
  s.addText(page.title, { placeholder: "title" });
  const rows = page.rows.map((r) =>
    r.group
      ? [{ text: r.group, options: { colspan: 6, bold: true, fill: { color: K.bg2 } } }]
      : [r.id, r.name, r.url, r.req, r.path, String(r.page)].map((t) => ({ text: t })),
  );
  listTable(s, ["화면 ID", "화면명", "URL", "요구사항 ID", "화면 경로", "쪽"], [96, 190, 190, 170, 530, 40], rows, 80);
});

// ── 화면 쪽
function screenSlide(sc) {
  const s = pres.addSlide({ masterName: "SCREEN", sectionTitle: sc.group });
  s.addText(sc.name, { placeholder: "title" });

  // 위 표: 화면명(제목 자리) · 요구사항 ID / 화면 경로 · 화면 ID
  const val = (text) => ({ text, options: { align: "left" } });
  s.addTable(
    [
      [headCell("화면명"), val(""), headCell("요구사항 ID"), val(sc.req)],
      [headCell("화면 경로"), { text: [{ text: `${sc.path} ` }, { text: `· ${sc.url}`, options: { color: K.accent4 } }] }, headCell("화면 ID"), val(sc.id)],
    ],
    { x: px(32), y: px(36), w: px(1216), colW: [96, 814, 96, 210].map(px), rowH: px(27), fontSize: pt(12.5), color: K.text1, valign: "middle", border, margin: [0.02, px(12), 0.02, px(12)] },
  );

  // 왼쪽: 캡처 + 번호
  s.addShape(pres.shapes.RECTANGLE, { x: px(BOX.x), y: px(BOX.y), w: px(BOX.w), h: px(BOX.h), fill: { color: K.bg2 }, line: { color: K.accent6, width: 0.75 }, objectName: "shot-box" });
  const sc_ = Math.min(BOX.w / sc.w, BOX.h / sc.h);
  const fw = sc.w * sc_, fh = sc.h * sc_;
  const fx = BOX.x + (BOX.w - fw) / 2, fy = BOX.y + (BOX.h - fh) / 2;
  s.addImage({ path: sc.img, x: px(fx), y: px(fy), w: px(fw), h: px(fh), altText: `${sc.name} 화면`, objectName: "shot" });
  sc.marks.forEach((m) => {
    const [x, y, w, h] = m.box.map((v) => v * sc_);
    const x0 = Math.max(0, x), y0 = Math.max(0, y), x1 = Math.min(fw, x + w), y1 = Math.min(fh, y + h);
    if (x1 > x0 && y1 > y0) {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: px(fx + x0 - 3), y: px(fy + y0 - 3), w: px(x1 - x0 + 6), h: px(y1 - y0 + 6), rectRadius: 0.04,
        fill: { color: K.bg1, transparency: 100 }, line: { color: K.accent1, width: 1.5 }, objectName: `mark-box-${m.n}`,
      });
    }
    const cx = Math.min(Math.max(0, x0 - 19), fw - 22), cy = Math.min(Math.max(0, y0 - 17), fh - 22);
    s.addText(String(m.n), {
      shape: pres.shapes.OVAL, x: px(fx + cx), y: px(fy + cy), w: px(22), h: px(22), fill: { color: K.accent1 }, line: { color: K.bg1, width: 1.5 },
      fontSize: pt(12), bold: true, color: K.bg1, align: "center", valign: "middle", margin: 0, objectName: `mark-${m.n}`,
    });
  });

  // 오른쪽: Description · Check Point
  const dense = sc.marks.length > 4;
  const tSize = pt(dense ? 12 : 12.5), dSize = pt(dense ? 11.5 : 12);
  s.addShape(pres.shapes.RECTANGLE, { x: px(PANEL.x), y: px(PANEL.y), w: px(PANEL.w), h: px(PANEL.h), fill: { color: K.bg1 }, line: { color: K.accent6, width: 0.75 }, objectName: "desc-panel" });
  s.addText("Description", { x: px(PANEL.x), y: px(PANEL.y), w: px(PANEL.w), h: px(26), fill: { color: K.text2 }, color: K.bg1, bold: true, fontSize: pt(12.5), align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "desc-head" });
  s.addText(sc.part > 1 ? `${sc.id} · ${sc.part}` : sc.id, { x: px(PANEL.x + 10), y: px(PANEL.y + 26), w: px(PANEL.w - 20), h: px(26), fontSize: pt(12), color: K.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "desc-id" });
  s.addShape(pres.shapes.LINE, { x: px(PANEL.x), y: px(PANEL.y + 52), w: px(PANEL.w), h: 0, line: { color: K.accent6, width: 0.75 } });

  const itemRows = sc.marks.map((m) => [
    { text: String(m.n), options: { color: K.accent1, bold: true, align: "center", valign: "top", fontSize: tSize } },
    {
      text: [
        { text: m.title, options: { bold: true, fontSize: tSize, breakLine: m.desc.length > 0 } },
        ...m.desc.map((d, i) => ({ text: d, options: { bullet: { indent: 10 }, fontSize: dSize, color: K.text2, breakLine: i < m.desc.length - 1 } })),
      ],
      options: { valign: "top" },
    },
  ]);
  if (itemRows.length) {
    s.addTable(itemRows, {
      x: px(PANEL.x), y: px(PANEL.y + 52), w: px(PANEL.w), colW: [26, 274].map(px), color: K.text1,
      border: [{ type: "none" }, { type: "none" }, { type: "solid", pt: 0.5, color: K.accent5 }, { type: "none" }], margin: [0.03, 0.06, 0.04, 0.06],
    });
  }

  if (sc.check) {
    const [title, lines] = sc.check;
    // 글 줄 수를 어림해 Check Point를 칸 아래쪽에 붙인다 (한 줄에 한글 약 24자)
    const lineCount = 1 + lines.reduce((n, l) => n + Math.ceil(l.length / 24), 0);
    const h = 26 + 12 + lineCount * 17;
    const top = PANEL.y + PANEL.h - h;
    s.addText("Check Point", { x: px(PANEL.x), y: px(top), w: px(PANEL.w), h: px(26), fill: { color: K.text2 }, color: K.bg1, bold: true, fontSize: pt(12.5), align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "cp-head" });
    s.addText(
      [
        { text: title, options: { bold: true, fontSize: pt(12.5), breakLine: true } },
        ...lines.map((l, i) => ({ text: l, options: { bullet: { indent: 10 }, fontSize: pt(12), color: K.text2, breakLine: i < lines.length - 1 } })),
      ],
      { x: px(PANEL.x + 8), y: px(top + 30), w: px(PANEL.w - 16), h: px(h - 34), valign: "top", color: K.text1, margin: 0, isTextBox: true, objectName: "cp-body" },
    );
  }
}

let lastGroup = null;
data.screens.forEach((sc) => {
  if (sc.group !== lastGroup) {
    pres.addSection({ title: sc.group });
    lastGroup = sc.group;
  }
  screenSlide(sc);
});

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (APPLY_THEME) {
    const { applyTheme } = require(APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log(`${path.basename(OUT)} ok`);
})();
