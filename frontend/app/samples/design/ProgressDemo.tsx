"use client";
// 견적 받기 창 머리 예시: 질문 9~11개를 묶음 4개로 나눠 보인다.
// 지금 창(components/start/Wizard.tsx)은 '1 / 9'와 막대 하나라서, 도배 · 목공을 고르면 전체 수가 바뀌고 어디쯤인지 감이 안 온다.
// 묶음 이름은 그대로 두고 묶음 안 칸만 채우면 질문 수가 바뀌어도 막대가 뒤로 가지 않는다.
import { useEffect, useRef, useState } from "react";
import s from "./samples.module.css";

const c = (n: string) => s[`mj-sd-${n}`];
const GROUPS = ["집 정보", "일정 · 예산", "공정", "사진 · 확인"];
// 질문 제목은 지금 Wizard와 같다. 도배만 고른 경우(10개)
const STEPS: { g: number; t: string; opt?: boolean }[] = [
  { g: 0, t: "공사할 집은 어디인가요?" },
  { g: 0, t: "어떤 집인가요?" },
  { g: 0, t: "집은 몇 평인가요?" },
  { g: 1, t: "언제쯤 공사하고 싶으세요?" },
  { g: 1, t: "공사할 때 집은 어떤가요?" },
  { g: 1, t: "생각하는 예산이 있나요?", opt: true },
  { g: 2, t: "어떤 공사가 필요한가요?" },
  { g: 2, t: "도배할 공간과 유형을 골라 주세요" },
  { g: 3, t: "공간별 사진과 도면이 있나요?", opt: true },
  { g: 3, t: "이대로 프로젝트를 만들까요?" },
];

export function ProgressDemo() {
  const [i, setI] = useState(4);
  const h = useRef<HTMLHeadingElement>(null);
  const moved = useRef(false);
  useEffect(() => { if (moved.current) h.current?.focus(); }, [i]);

  const cur = STEPS[i];
  const fill = (g: number) => {
    if (g < cur.g) return 100;
    if (g > cur.g) return 0;
    const inG = STEPS.filter((x) => x.g === g);
    const at = STEPS.slice(0, i + 1).filter((x) => x.g === g).length;
    return Math.round((at / inG.length) * 100);
  };
  const go = (d: number) => { moved.current = true; setI((x) => Math.min(STEPS.length - 1, Math.max(0, x + d))); };

  return (
    <div className={c("dlg")}>
      <div className={c("dlg-head")}>
        <div className={c("dlg-top")}>
          <span><b>{GROUPS[cur.g]}</b><span className="mj-sub"> · 묶음 {cur.g + 1} / {GROUPS.length}</span></span>
          <span className="mj-num mj-sub" aria-live="polite">질문 {i + 1} / {STEPS.length}</span>
        </div>
        <ol className={c("seg")} aria-label="질문 묶음">
          {GROUPS.map((g, k) => (
            <li key={g} className={k === cur.g ? s.cur : k < cur.g ? s.done : undefined} aria-current={k === cur.g ? "step" : undefined}>
              <span className={c("seg-bar")} aria-hidden="true"><span style={{ width: `${fill(k)}%` }} /></span>
              <span>{g}{k < cur.g ? <span className="mj-sr"> · 끝남</span> : null}</span>
            </li>
          ))}
        </ol>
      </div>
      <div className={c("dlg-body")}>
        <h4 ref={h} tabIndex={-1}>{cur.t}{cur.opt ? <span className="mj-opt"> (선택)</span> : null}</h4>
        <p className="mj-small">질문 내용은 지금 창과 같아요. 이 예시는 위쪽 진행 표시만 바꿨어요.</p>
      </div>
      <div className={c("dlg-foot")}>
        <button type="button" className="mj-btn mj-btn-sec" onClick={() => go(-1)} disabled={i === 0}>이전</button>
        <button type="button" className="mj-btn mj-btn-pri" onClick={() => go(1)} disabled={i === STEPS.length - 1}>다음</button>
      </div>
    </div>
  );
}
