// 화면이 데이터를 받는 유일한 곳 (서버 쪽). AGENTS.md 2장: Next는 API만 부른다.
// - 실제 API: 내 프로젝트 목록 · 프로젝트 보기 (FastAPI, lib/backend/server.ts)
// - 예시 데이터: 예시 프로젝트(p1)의 예상 공정표 · 표준견적서 · 업체 · 견적 · 실측 · 공정표, 관리자 회원 목록.
//   계산 엔진 · 업체 · 견적 API가 생기면 하나씩 실제 호출로 바꾼다.
import { serverGet, type Schemas } from "./backend/server";
import { COMPLEXES, FX, HISTORY, MEMBERS, PROJECTS, QUOTE_REQUESTS, RECOMMEND, VENDORS, VISITS } from "./mock/data";
import type { Trade, Vendor } from "./types";
import type { TradeLine } from "./trade-status";
import { md } from "./format";

export type ApiProject = Schemas["ProjectOut"];
export type ApiProjectItem = Schemas["ProjectListItem"];

/** 예시 프로젝트 id. 이 id만 예시 데이터로 보여 준다. */
export const isDemoProject = (id: string) => PROJECTS.some((p) => p.id === id);
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export async function listMyProjects() { return (await serverGet<ApiProjectItem[]>("/projects")) ?? []; }
/** 내 프로젝트(또는 관리자). 없거나 남의 것이면 null */
export async function getMyProject(id: string) { return UUID.test(id) ? serverGet<ApiProject>(`/projects/${id}`) : null; }

export async function searchComplexes(q: string) {
  const s = q.trim();
  if (!s) return [];
  return COMPLEXES.filter((c) => c.name.includes(s) || c.road.includes(s) || c.dong.includes(s));
}

export async function listDemoProjects() { return PROJECTS; }
export async function getProject(id: string) { return PROJECTS.find((p) => p.id === id) ?? null; }

export async function getExpectedSchedule(_projectId: string) { return FX.expected; }
export async function getStandardQuote(_projectId: string) { return { ...FX.standard, createdAt: "2026-10-20" }; }

export async function getRecommendations(_projectId: string, trade: Trade) { return RECOMMEND[trade]; }

export type VendorQuery = { trade: Trade; region?: string; q?: string; sort?: "reviews" | "rating" | "cases" };
export async function listVendors({ trade, region, q, sort = "reviews" }: VendorQuery) {
  let list = VENDORS.filter((v) => v.trades.includes(trade) && v.status === "active");
  if (region) list = list.filter((v) => v.areas.includes(region));
  if (q?.trim()) list = list.filter((v) => v.name.includes(q.trim()));
  const key: Record<string, (v: Vendor) => number> = { reviews: (v) => v.reviews, rating: (v) => v.rating, cases: (v) => v.portfolio.length };
  return [...list].sort((a, b) => key[sort](b) - key[sort](a));
}
export async function getVendor(id: string) { return VENDORS.find((v) => v.id === id) ?? null; }
export async function listAllVendors() { return VENDORS; }

export async function getQuoteRequests(projectId: string) { return QUOTE_REQUESTS[projectId] ?? []; }
export async function getVendorQuotes(_projectId: string, trade: Trade) { return FX.quotes[trade]; }
export async function getCompare(_projectId: string, trade: Trade) { return FX.compare[trade]; }

export async function getVisits(projectId: string) { return VISITS[projectId] ?? []; }
export async function getFinalQuote(_projectId: string, trade: Trade) { return FX.finals[trade]; }
export async function getConfirmedSchedule(_projectId: string) { return FX.confirmed; }

export async function getHistory(projectId: string) { return HISTORY[projectId] ?? []; }
export async function listMembers() { return MEMBERS; }

export async function vendorName(id: string) { return VENDORS.find((v) => v.id === id)?.name ?? id; }
export const ALL_REGIONS = Array.from(new Set(VENDORS.flatMap((v) => v.areas))).sort((a, b) => a.localeCompare(b, "ko"));

// ── 내 프로젝트 카드의 공정별 상태 (lib/trade-status.ts)

/** 실제 프로젝트: 견적 · 실측 API가 아직 없어서 모든 공정이 '업체 고르기' 단계다. */
export function realTradeLines(trades: string[]): TradeLine[] {
  return trades.filter((t): t is Trade => t === "dobae" || t === "mokgong").map((trade) => ({ trade, stage: "choosing", text: "업체를 골라 가견적을 요청해요" }));
}

/** 예시 프로젝트: 예시 데이터의 요청 · 실측 · 확정 기록으로 단계를 정한다. */
export async function demoTradeLines(id: string): Promise<TradeLine[]> {
  const p = await getProject(id);
  if (!p) return [];
  const reqs = QUOTE_REQUESTS[id] ?? [];
  const visits = VISITS[id] ?? [];
  return (["dobae", "mokgong"] as Trade[]).filter((t) => p.trades[t]).map((t): TradeLine => {
    const conf = FX.confirmed[t];
    if (conf) return { trade: t, stage: "scheduled", text: `${md(conf.start)} ~ ${md(conf.end)} 공사` };
    if (FX.finals[t]) return { trade: t, stage: "final_arrived", text: `${VENDORS.find((v) => v.id === FX.finals[t].vendorId)?.name ?? ""} 실측 견적이 왔어요` };
    if (visits.some((v) => v.trade === t)) return { trade: t, stage: "visit_wait", text: "실측 견적을 기다려요" };
    const r = reqs.filter((x) => x.trade === t);
    const got = r.filter((x) => x.status !== "requested").length;
    if (got) return { trade: t, stage: "comparing", text: `${r.length}곳 중 ${got}곳 도착` };
    if (r.length) return { trade: t, stage: "estimate_wait", text: `${r.length}곳에 요청했어요` };
    return { trade: t, stage: "choosing", text: "업체를 골라 가견적을 요청해요" };
  });
}

/** 예시 프로젝트의 공사가 끝나는 날 (확정 공정표 마지막 날). 없으면 null */
export async function demoProjectEnd(_id: string): Promise<string | null> {
  const ends = (["dobae", "mokgong"] as Trade[]).map((t) => FX.confirmed[t]?.end).filter((e): e is string => !!e);
  return ends.length ? ends.sort().at(-1)! : null;
}

// ── 관리자: 업체 가입 신청 (FAD-02 · 03, API)
export type VendorApplication = Schemas["VendorAdminOut"];
export type VendorStatus = "pending" | "approved" | "rejected";
export async function listVendorApplications(status?: VendorStatus) {
  return (await serverGet<VendorApplication[]>(`/admin/vendors${status ? `?status=${status}` : ""}`)) ?? [];
}
export async function getVendorApplication(id: string) {
  return /^[0-9a-f-]{36}$/i.test(id) ? serverGet<VendorApplication>(`/admin/vendors/${id}`) : null;
}
