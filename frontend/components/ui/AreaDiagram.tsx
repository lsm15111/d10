// 공급(점선) 안에 전용(실선)을 겹쳐 그린다. 크기는 넓이 비율(√)로 맞춘다. 표시용 도식이고 계산에는 쓰지 않는다.
export function AreaDiagram({ supply, jeon, max = 140, maxSupply }: { supply: number; jeon: number; max?: number; maxSupply?: number }) {
  const ref = maxSupply ?? supply;
  const ws = max * Math.sqrt(supply / ref);
  const wj = ws * Math.sqrt(jeon / supply);
  const h = (w: number) => w * 0.82;
  return (
    <svg width={max + 12} height={h(max) + 12} viewBox={`0 0 ${max + 12} ${h(max) + 12}`} role="img" aria-label={`공급 ${supply}제곱미터 안에 전용 ${jeon}제곱미터`}>
      <rect x="6" y="6" width={ws} height={h(ws)} fill="var(--accent-weak)" stroke="var(--accent)" strokeWidth="1.5" strokeDasharray="5 4" rx="2" />
      <rect x="6" y="6" width={wj} height={h(wj)} fill="#fff" stroke="var(--ink)" strokeWidth="2" rx="2" />
    </svg>
  );
}

export function AreaLegend({ supply, jeon }: { supply: number; jeon: number }) {
  return (
    <div className="mj-legend">
      <span><i style={{ border: "2px solid var(--ink)", background: "#fff" }} />전용 <b className="mj-num">{jeon}㎡</b></span>
      <span><i style={{ border: "1.5px dashed var(--accent)", background: "var(--accent-weak)" }} />공급 <b className="mj-num">{supply}㎡</b></span>
    </div>
  );
}
