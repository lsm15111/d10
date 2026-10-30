"use client";
// 시공 전 · 완공 비교. 손가락 · 마우스로 끌거나, 키보드 화살표로 움직이거나, 아래 버튼으로 한 번에 바꾼다.
// 범위 입력(input type=range)을 그림 전체에 겹쳐서 화면 읽기 프로그램도 값을 읽는다.
// 실제 화면에서는 업체가 '전후 짝'으로 묶은 같은 자리 사진 두 장이 들어간다(docs/design/vendor-portfolio.md 4장).
import { useState } from "react";
import { WallScene } from "./art";
import s from "./samples.module.css";

const c = (n: string) => s[`mj-sd-${n}`];

export function BeforeAfter() {
  const [pos, setPos] = useState(50);
  const text = pos <= 0 ? "완공만 보여요" : pos >= 100 ? "시공 전만 보여요" : `왼쪽 ${pos}%는 시공 전, 나머지는 완공`;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10, minWidth: 0 }}>
      <div className={c("ba")} style={{ "--pos": `${pos}%` } as React.CSSProperties}>
        <div className={c("ba-layer")}><WallScene variant="after" id="sd-after" /></div>
        <div className={`${c("ba-layer")} ${c("ba-before")}`}><WallScene variant="before" id="sd-before" /></div>
        <span className={c("ba-line")} aria-hidden="true" />
        <span className={c("ba-knob")} aria-hidden="true">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 6-6 6 6 6M15 6l6 6-6 6" /></svg>
        </span>
        <span className={`${c("ba-tag")} ${s.l}`}>시공 전 · 그림</span>
        <span className={`${c("ba-tag")} ${s.r}`}>완공 · 그림</span>
        <input type="range" min={0} max={100} step={5} value={pos} onChange={(e) => setPos(Number(e.target.value))} aria-label="시공 전과 완공 비교 위치" aria-valuetext={text} />
      </div>
      <div className={c("ba-ctl")} role="group" aria-label="비교 바로 보기">
        <button type="button" className="mj-btn mj-btn-sec mj-btn-sm" aria-pressed={pos === 100} onClick={() => setPos(100)}>시공 전</button>
        <button type="button" className="mj-btn mj-btn-sec mj-btn-sm" aria-pressed={pos === 50} onClick={() => setPos(50)}>반씩</button>
        <button type="button" className="mj-btn mj-btn-sec mj-btn-sm" aria-pressed={pos === 0} onClick={() => setPos(0)}>완공</button>
        <span className="mj-tiny">그림이에요. 실제로는 업체가 같은 자리에서 찍은 사진 두 장이 들어가요.</span>
      </div>
    </div>
  );
}
