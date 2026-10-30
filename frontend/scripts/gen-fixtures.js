// 믿집 화면용 예시 데이터 생성: mitjip-v6 계산 엔진 + 공공 단가(2026)로 만든다.
const V6 = process.argv[2], OUT = process.argv[3];
require(V6 + "/js/data.js"); require(V6 + "/js/calc.js");
const C = globalThis.CALC, { VENDORS } = globalThis.DATA;
const fs = require("fs");
const r1000 = (x) => Math.round(x / 1000) * 1000;

const home = { sido: "서울", sgg: "마포구", type: "apt", basis: "jeon", areaM2: 84.97, ext: true, rooms: 3, occupied: true, start: "2026-11-16" };
const rooms = C.roomsOf(home).map((r) => r.id);
const T = (d, m) => ({
  dobae: { on: d, scope: "all", rooms, paper: "silk", ceiling: true, old: "unknown" },
  mokgong: { on: m, molding: true, base: true, door: false, doorN: 3, flatten: false, wall: false, wallM: 3 }
});
const trD = T(true, false), trM = T(false, true), trB = T(true, true);
const today = new Date(2026, 9, 29);
const area = C.areaOf(home);
const dq = C.dobaeQty(home, trB.dobae), mq = C.mokQty(home, trB.mokgong);

// 공공 단가 (출처: mitjip-v5/reports/도배 목공 공정별 계산식 표준.md)
const PUB = {
  wallPaste: { v: 5993, src: "표준시장단가 2026 하반기 OB110.20000 도배지바름 벽(콘크리트·모르타르면)" },
  ceilPaste: { v: 8531, src: "표준시장단가 2026 하반기 OB130.10000 도배지바름 천장(석고보드면)" },
  wallRemove: { v: 2702, src: "표준품셈 2026 유지관리 3-2-7 도배 해체(벽) × 시중노임단가 2026.9.1" },
  ceilRemove: { v: 3507, src: "표준품셈 2026 유지관리 3-2-7 도배 해체(천장) × 시중노임단가 2026.9.1" },
  primer: { v: 242, src: "조달청 시설공통자재 2026 상반기 초배지" },
  molding: { v: 8168, src: "표준시장단가 2026 하반기 OG002 천장 몰딩(재료 제외)" },
  base: { v: 3757, src: "표준시장단가 2026 하반기 OA5 걸레받이 MDF(재료 제외)" }
};
const wall = +dq.wall.toFixed(1), ceil = +dq.ceil.toFixed(1);
const primerM2 = +(wall * 1.2 + ceil * 0.8).toFixed(1);
const silkM2 = +((wall + ceil) * 1.2).toFixed(1);
const silkRolls = Math.ceil(silkM2 / 16.5);
const L = (k, trade, name, qty, unit, unitPrice, src, kind) => ({ k, trade, name, qty, unit, unitPrice, amount: unitPrice == null || qty == null ? null : r1000(qty * unitPrice), src, kind });
const stdLines = [
  L("wall_paste", "dobae", "도배지 바름 · 벽", wall, "㎡", PUB.wallPaste.v, PUB.wallPaste.src, "public"),
  L("ceil_paste", "dobae", "도배지 바름 · 천장", ceil, "㎡", PUB.ceilPaste.v, PUB.ceilPaste.src, "public"),
  L("wall_remove", "dobae", "기존 벽지 해체 · 벽", wall, "㎡", PUB.wallRemove.v, PUB.wallRemove.src, "public"),
  L("ceil_remove", "dobae", "기존 벽지 해체 · 천장", ceil, "㎡", PUB.ceilRemove.v, PUB.ceilRemove.src, "public"),
  L("primer", "dobae", "초배지", primerM2, "㎡", PUB.primer.v, PUB.primer.src, "public"),
  L("silk", "dobae", "정배지 (실크)", silkRolls, "롤", null, "공공 가격 없음 · 표준품셈 정배지 1.2㎡/㎡로 수량만 계산", "none"),
  L("molding", "mokgong", "천장 몰딩 설치", mq.molding, "m", PUB.molding.v, PUB.molding.src, "public"),
  L("base", "mokgong", "걸레받이 설치 (MDF)", mq.base, "m", PUB.base.v, PUB.base.src, "public"),
  L("mok_mat", "mokgong", "몰딩 · 걸레받이 자재", null, "", null, "공공 가격 없음 · 업체 견적에서 확인", "none"),
  L("mok_remove", "mokgong", "기존 몰딩 · 걸레받이 철거", null, "", null, "공공 기준 없음 · 업체 견적에서 확인", "none")
];
const sum = (tr) => stdLines.filter((l) => l.trade === tr && l.amount != null).reduce((s, l) => s + l.amount, 0);
const standard = {
  id: "std-p1-1", createdAt: "2026-10-29", basisDate: "2026-10-29",
  sources: ["표준시장단가 2026 하반기 (2026.5.8 공고)", "시중노임단가 2026.9.1 적용 (도배공 229,833원 · 내장공 258,904원 · 보통인부 172,698원)", "조달청 시설공통자재 가격 2026 상반기", "건설공사 표준품셈 2026"],
  qty: { wall, ceil, totalM2: +(wall + ceil).toFixed(1), molding: mq.molding, base: mq.base, basis: "공급 113.3㎡ · 업계 산식 도배평 = 공급평 × 2.5 · 발코니 확장 +8%" },
  lines: stdLines,
  totals: { dobae: sum("dobae"), mokgong: sum("mokgong"), all: sum("dobae") + sum("mokgong") },
  excluded: ["정배지(실크) 자재비", "몰딩 · 걸레받이 자재비", "기존 몰딩 · 걸레받이 철거", "짐 이동 · 보양 · 폐기물", "간접비 · 이윤 · 부가세"],
  notice: "공공데이터로 계산한 참고용 기준 금액이에요. 업체 견적은 자재 등급, 현장 상태, 인건비 관행에 따라 이보다 높거나 낮을 수 있어요."
};

const vinfo = (v) => ({ id: v.id, name: v.name, trades: v.trades, years: v.years, since: v.since, areas: v.areas, crew: v.crew, rating: v.rating, reviews: v.reviews, jobs: v.jobs, license: v.license, bond: v.bond, response: v.response, as: v.as, notes: v.notes, weekend: v.weekend, visitFee: v.visitFee });
const vendors = VENDORS.map(vinfo);
const mapLines = (lines) => lines.map((l) => ({ k: l.k, name: l.label || l.name, qty: l.qty, unit: l.unit, amount: l.amount, state: l.state, note: l.note || "" }));
const est = (v, tr) => { const e = C.estimate(v, home, tr, {}); return { total: e.total, vat: e.vat, direct: e.direct, margin: e.margin, marginRate: e.marginRate, lo: e.lo, hi: e.hi, lines: mapLines(e.lines) }; };
const fin = (v, tr) => { const q = C.finalQuote(v, home, tr); const e = C.estimate(v, home, tr, {}); return { total: q.total, vat: q.vat, direct: q.direct, margin: q.margin, estimateTotal: e.total, deltaTotal: q.total - e.total, findings: q.findings.map((f) => f.t), lines: mapLines(q.lines), diff: C.diffQuotes(e, q).map((d) => ({ name: d.label, from: d.from ? d.from.qty : null, to: d.to ? d.to.qty : null, delta: d.delta })) }; };
const rec = (tr) => C.recommend(home, tr, today).rows.map((r) => ({ vendorId: r.v.id, rank: r.rank, score: r.score, total: r.est.total, pros: r.pros, cons: r.cons }));
const recommend = { dobae: rec(trD).slice(0, 3), mokgong: rec(trM).slice(0, 3) };
const byId = (id) => VENDORS.find((v) => v.id === id);
const quotes = {
  dobae: recommend.dobae.map((r) => ({ vendorId: r.vendorId, ...est(byId(r.vendorId), trD) })),
  mokgong: recommend.mokgong.map((r) => ({ vendorId: r.vendorId, ...est(byId(r.vendorId), trM) }))
};
// 가견적 비교표: 표준견적과 업체 가견적을 같은 줄로 묶는다 (금액 합산은 여기서만)
const amt = (q, ...ks) => q.lines.filter((l) => ks.includes(l.k)).reduce((s, l) => s + (l.amount || 0), 0);
const stOf = (q, k) => (q.lines.find((l) => l.k === k) || {}).state;
const stdAmt = (...ks) => stdLines.filter((l) => ks.includes(l.k)).reduce((s, l) => s + (l.amount || 0), 0);
const cell = (amount, text) => ({ amount, text: text || "" });
const stateCell = (q, k, inText) => {
  const s = stOf(q, k), a = amt(q, k);
  if (s === "in") return cell(a, "포함");
  if (s === "sep") return cell(a, "별도");
  if (s === "opt") return cell(a, "선택");
  if (s === "bundle") return cell(null, inText || "다른 항목에 포함");
  if (s === "cond") return cell(null, "실측 후 결정");
  if (s === "no") return cell(null, "안 함");
  return cell(null, "적지 않음");
};
const cmpRows = {
  dobae: [
    { key: "paper", label: "벽지 (실크)", std: cell(null, "공공 가격 없음"), v: (q) => cell(amt(q, "rollWall", "rollCeil"), "포함") },
    { key: "sub", label: "부자재 · 초배지", std: cell(stdAmt("primer"), "조달청 초배지"), v: (q) => stateCell(q, "sub") },
    { key: "labor", label: "도배 인건비", std: cell(stdAmt("wall_paste", "ceil_paste"), "표준시장단가"), v: (q) => stateCell(q, "labor") },
    { key: "demo", label: "기존 벽지 철거", std: cell(stdAmt("wall_remove", "ceil_remove"), "표준품셈"), v: (q) => stateCell(q, "demo", "인건비에 포함") },
    { key: "primer", label: "천장 초배", std: cell(null, "초배지에 포함"), v: (q) => stateCell(q, "primer", "기본 포함") },
    { key: "putty", label: "퍼티 · 바탕 보수", std: cell(null, "공공 기준 없음"), v: (q) => stateCell(q, "putty") },
    { key: "move", label: "짐 이동 · 보양", std: cell(null, "제외"), v: (q) => stateCell(q, "move") },
    { key: "waste", label: "폐기물 · 운반", std: cell(null, "제외"), v: (q) => stateCell(q, "waste") },
    { key: "margin", label: "이윤 · 관리비", std: cell(null, "제외"), v: (q) => cell(q.margin, `${Math.round(q.marginRate * 100)}%`) }
  ],
  mokgong: [
    { key: "molding", label: "천장 몰딩", std: cell(stdAmt("molding"), "시공만 · 자재 제외"), v: (q) => cell(amt(q, "molding"), "자재 · 시공 · 철거") },
    { key: "base", label: "걸레받이", std: cell(stdAmt("base"), "시공만 · 자재 제외"), v: (q) => cell(amt(q, "base"), "자재 · 시공 · 철거") },
    { key: "protect", label: "보양 · 자재 운반", std: cell(null, "제외"), v: (q) => stateCell(q, "mprotect") },
    { key: "margin", label: "이윤 · 관리비", std: cell(null, "제외"), v: (q) => cell(q.margin, `${Math.round(q.marginRate * 100)}%`) }
  ]
};
const compare = {};
for (const t of ["dobae", "mokgong"]) {
  compare[t] = {
    rows: cmpRows[t].map((r) => ({ key: r.key, label: r.label, std: r.std, vendors: Object.fromEntries(quotes[t].map((q) => [q.vendorId, r.v(q)])) })),
    total: { label: "합계 · 부가세 별도", std: cell(standard.totals[t], "공공 기준 · 일부 제외"), vendors: Object.fromEntries(quotes[t].map((q) => [q.vendorId, cell(q.total, "")])) }
  };
}
const pick = { dobae: recommend.dobae[0].vendorId, mokgong: recommend.mokgong[0].vendorId };
const finals = { dobae: { vendorId: pick.dobae, ...fin(byId(pick.dobae), trD) }, mokgong: { vendorId: pick.mokgong, ...fin(byId(pick.mokgong), trM) } };

const stdVendor = { ...byId("v3"), crew: { dobae: 2, mokgong: 1 }, weekend: "sat" };
const stdQuote = C.estimate(stdVendor, home, trB, {});
const expected = C.schedule(stdVendor, home, trB, stdQuote, "2026-11-16");
const fm = C.finalQuote(byId(pick.mokgong), home, trM), fd = C.finalQuote(byId(pick.dobae), home, trD);
const sm = C.schedule(byId(pick.mokgong), home, trM, fm, "2026-11-16");
const nextDay = (iso) => { const [y, m, d] = iso.split("-").map(Number); const t = new Date(y, m - 1, d + 1); return `${t.getFullYear()}-${String(t.getMonth() + 1).padStart(2, "0")}-${String(t.getDate()).padStart(2, "0")}`; };
const sd = C.schedule(byId(pick.dobae), home, trD, fd, nextDay(sm.end));
// 반나절 칸(s, e)을 날짜 + 오전/오후로 바꿔 둔다 (화면에서 날짜 계산을 하지 않게)
const dated = (sch) => sch.tasks.map((t) => ({ ...t, from: { date: sch.days[Math.floor(t.s / 2)], half: t.s % 2 ? "pm" : "am" }, to: { date: sch.days[Math.floor((t.e - 1) / 2)], half: (t.e - 1) % 2 ? "pm" : "am" } }));
expected.tasks = dated(expected);
sm.tasks = dated(sm); sd.tasks = dated(sd);
const confirmed = { mokgong: { vendorId: pick.mokgong, start: sm.start, end: sm.end, days: sm.days, tasks: sm.tasks }, dobae: { vendorId: pick.dobae, start: sd.start, end: sd.end, days: sd.days, tasks: sd.tasks } };

const out = { generatedAt: "2026-10-29", note: "예시 데이터. mitjip-v6 계산 엔진과 2026 공공 단가로 만든 값이고, 업체·단지·회원은 모두 가상이에요.",
  area: { supply: +area.supply.toFixed(1), jeon: area.jeon, supplyPy: +area.supplyPy.toFixed(1), dobaePy: +area.dobaePy.toFixed(1) },
  spaces: C.roomsOf(home).map((r) => ({ id: r.id, name: r.name })),
  standard, vendors, recommend, quotes, compare, finals,
  expected: { start: expected.start, end: expected.end, days: expected.days, tasks: expected.tasks, todos: expected.todos, weekendNote: expected.weekendNote },
  confirmed };
fs.writeFileSync(OUT, JSON.stringify(out, null, 2));
console.log("std", JSON.stringify(standard.totals));
console.log("rec", JSON.stringify(recommend.dobae.map((r) => r.vendorId + ":" + r.total)), JSON.stringify(recommend.mokgong.map((r) => r.vendorId + ":" + r.total)));
console.log("finals", finals.dobae.vendorId, finals.dobae.total, finals.mokgong.vendorId, finals.mokgong.total);
console.log("expected", expected.start, expected.end, expected.tasks.map((t) => t.label + "[" + t.s + "-" + t.e + "]").join(" | "));
console.log("confirmed", JSON.stringify({ m: [sm.start, sm.end], d: [sd.start, sd.end] }));
