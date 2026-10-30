// 내 프로젝트 카드: 공정마다 상태 한 줄(내 차례 · 업체 차례 · 끝남) + 지금 할 일 버튼 하나.
// 강조색은 '내 차례'에만 쓴다. 상태 문구는 그 공정 화면으로 가는 링크다.
import Link from "next/link";
import { TRADE_LABEL } from "@/lib/types";
import { TURN_LABEL, hrefOf, mainAction, turnOf, type TradeLine } from "@/lib/trade-status";
import { md } from "@/lib/format";

export function ProjectCard({ id, title, sub, created, lines, demo }: { id: string; title: string; sub?: string; created: string; lines: TradeLine[]; demo?: boolean }) {
  const act = mainAction(id, lines);
  return (
    <article className="mj-panel mj-pcard" aria-labelledby={`pc-${id}`}>
      <div className="mj-pcard-head">
        <h3 id={`pc-${id}`} className="mj-h3"><Link href={`/projects/${id}`} style={{ color: "var(--ink)" }}>{title}</Link></h3>
        {demo ? <span className="mj-badge">예시</span> : null}
        <span className="mj-small">{sub ? `${sub} · ` : ""}만든 날 {md(created)}</span>
      </div>
      <ul className="mj-pcard-lines">
        {lines.map((l) => {
          const turn = turnOf(l);
          return (
            <li key={l.trade}>
              <b>{TRADE_LABEL[l.trade]}</b>
              <span className={`mj-turn mj-turn-${turn}`}>{TURN_LABEL[turn]}</span>
              <Link href={hrefOf(id, l)}>{l.text}</Link>
            </li>
          );
        })}
      </ul>
      <div className="mj-btn-row">
        {act ? <Link href={act.href} className="mj-btn mj-btn-pri mj-btn-sm">{act.label}</Link> : <span className="mj-small">업체가 할 차례예요.</span>}
        <Link href={`/projects/${id}`} className="mj-btn mj-btn-ghost mj-btn-sm">프로젝트 보기</Link>
      </div>
    </article>
  );
}
