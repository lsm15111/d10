// 공정별 진행 상태 → 내 프로젝트 카드 한 줄 (docs/design/mypage-vendor-info.md 5.3, quote-flow-v3.2.md 4장).
// 상태는 데이터를 주는 쪽(lib/api.ts)이 정하고, 여기서는 화면 말과 갈 곳만 붙인다.
import type { Trade } from "./types";

export type TradeStage = "choosing" | "estimate_wait" | "comparing" | "visit_wait" | "final_arrived" | "confirmed" | "scheduled";
export type Turn = "me" | "vendor" | "done";

export interface TradeLine {
  trade: Trade;
  stage: TradeStage;
  text: string; // 예: "3곳 중 2곳 도착"
}

export const TURN_LABEL: Record<Turn, string> = { me: "내 차례", vendor: "업체 차례", done: "일정 확정" };

const STAGE: Record<TradeStage, { turn: Turn; seg: string; action?: string }> = {
  choosing: { turn: "me", seg: "vendors", action: "업체 고르기" },
  estimate_wait: { turn: "vendor", seg: "quotes" },
  comparing: { turn: "me", seg: "quotes", action: "가견적 비교하기" },
  visit_wait: { turn: "vendor", seg: "measure" },
  final_arrived: { turn: "me", seg: "measure", action: "실측 견적 확인하기" },
  confirmed: { turn: "vendor", seg: "measure" },
  scheduled: { turn: "done", seg: "schedule" },
};

export const turnOf = (l: TradeLine) => STAGE[l.stage].turn;
export const hrefOf = (projectId: string, l: TradeLine) => `/projects/${projectId}/${STAGE[l.stage].seg}?trade=${l.trade}`;

/** 카드의 주 버튼 하나: 가장 먼저 할 내 일. 모두 끝났으면 확정 공정표, 업체 차례뿐이면 없음. */
export function mainAction(projectId: string, lines: TradeLine[]): { label: string; href: string } | null {
  const mine = lines.find((l) => turnOf(l) === "me");
  if (mine) return { label: `${tradeName(mine.trade)} ${STAGE[mine.stage].action}`, href: hrefOf(projectId, mine) };
  if (lines.length && lines.every((l) => l.stage === "scheduled")) return { label: "확정 공정표 보기", href: `/projects/${projectId}/schedule` };
  return null;
}

const tradeName = (t: Trade) => (t === "dobae" ? "도배" : "목공");
