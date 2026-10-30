"use client";
// 도배 유형(저가형 · 기본형)을 견본 카드로 고르는 예시.
// 어떤 벽지 · 단가가 들어가는지는 아직 정하지 않았다(AGENTS.md 1장). 카드 안 값은 모양을 보이려는 예시다.
import { useState } from "react";
import { DOBAE_GRADES, type DobaeGrade } from "@/lib/labels";
import { PaperArt } from "./art";
import { Check } from "./marks";
import s from "./samples.module.css";

const c = (n: string) => s[`mj-sd-${n}`];
const SAMPLE: Record<DobaeGrade, { art: "hapji" | "silk"; line: string; spec: [string, string][] }> = {
  economy: { art: "hapji", line: "종이 질감이고, 이음매가 살짝 보여요.", spec: [["벽지", "합지 (예시)"], ["이음", "겹쳐 붙임"], ["물걸레", "어려워요"], ["표준견적서", "정한 뒤 보여요"]] },
  basic: { art: "silk", line: "은은한 광택이 있고, 이음매가 거의 안 보여요.", spec: [["벽지", "실크 (예시)"], ["이음", "맞대어 붙임"], ["물걸레", "돼요"], ["표준견적서", "정한 뒤 보여요"]] },
};

export function GradeCards() {
  const [g, setG] = useState<DobaeGrade>("basic");
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14, minWidth: 0 }}>
      <fieldset className={c("grades")}>
        <legend className="mj-label" style={{ marginBottom: 10 }}>도배 유형</legend>
        {DOBAE_GRADES.map((x) => {
          const d = SAMPLE[x.key];
          return (
            // 카드 전체를 덮는 라디오. 이름은 제목만, 설명은 한 줄만 읽히게 한다(카드 글 전체가 이름이 되지 않게).
            <div key={x.key} className={c("grade")}>
              <input type="radio" name="sd-grade" checked={g === x.key} onChange={() => setG(x.key)} aria-labelledby={`sd-gt-${x.key}`} aria-describedby={`sd-gd-${x.key}`} />
              <div className={c("grade-art")}>
                <PaperArt kind={d.art} id={`sd-art-${x.key}`} />
                <span className={c("art-tag")}>그림 · 실제 견본 사진 필요</span>
                <span className={c("grade-check")} aria-hidden="true"><Check /></span>
              </div>
              <div className={c("grade-body")}>
                <div className={c("grade-t")}><b id={`sd-gt-${x.key}`}>{x.label}</b><span className="mj-badge mj-b-opt">예시 구성</span></div>
                <p className="mj-small" id={`sd-gd-${x.key}`}>{d.line}</p>
                <dl className={c("spec")}>
                  {d.spec.map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}
                </dl>
              </div>
            </div>
          );
        })}
      </fieldset>
      <details className={c("more")}>
        <summary>실크와 합지는 무엇이 다른가요?</summary>
        <div>
          <dl className="mj-kv">
            <dt>실크</dt><dd>종이 위에 비닐(PVC)을 입혀서 닦을 수 있어요. 이음매를 맞대어 붙여서 잘 안 보여요. 값이 더 나가요.</dd>
            <dt>합지</dt><dd>종이를 두 겹 붙인 벽지예요. 이음매를 조금 겹쳐 붙여서 가까이 보면 보여요. 값이 덜 나가요.</dd>
          </dl>
          <p className="mj-tiny" style={{ marginTop: 10 }}>어떤 유형에 어떤 벽지가 들어가는지는 믿집이 정한 뒤 여기에 적어요.</p>
        </div>
      </details>
    </div>
  );
}
