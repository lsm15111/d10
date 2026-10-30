// 디자인 예시 (/samples/design). docs/design/visual-design.md의 적용안을 우리 내용으로 먼저 그려 본 화면이다.
// 실제 화면 · 공용 파일은 바꾸지 않는다. 단지 · 업체 · 사례는 예시이고, 금액은 예시 프로젝트(p1) 표준견적서 값을 형식만 바꿔 보인다.
import Link from "next/link";
import { SiteHeader } from "@/components/site/SiteHeader";
import { getStandardQuote } from "@/lib/api";
import { md, won } from "@/lib/format";
import { BrandMark, Check, FEATURE_ICONS, FeatureIcon, Person, type IconName } from "./marks";
import { ProgressDemo } from "./ProgressDemo";
import { GradeCards } from "./GradeCards";
import { BeforeAfter } from "./BeforeAfter";
import s from "./samples.module.css";

export const metadata = { title: "디자인 예시", robots: { index: false } };

const c = (n: string) => s[`mj-sd-${n}`];

const SECTIONS = [
  { id: "chrome", no: "01", title: "헤더 · 파비콘 · 아이콘 · 바닥글" },
  { id: "home", no: "02", title: "홈 첫 화면" },
  { id: "quote", no: "03", title: "견적 받기 창" },
  { id: "case", no: "04", title: "업체 시공 사례" },
  { id: "project", no: "05", title: "내 프로젝트 · 진행 현황" },
];

function Head({ id, no, title, where, from, why }: { id: string; no: string; title: string; where: React.ReactNode; from: string; why: string }) {
  return (
    <div className={c("sec-head")}>
      <span className={c("no")}>{no}</span>
      <h2 id={id} className="mj-h2">{title}</h2>
      <dl className={c("meta")}>
        <dt>넣을 곳</dt><dd>{where}</dd>
        <dt>가져온 곳</dt><dd>{from}</dd>
        <dt>왜</dt><dd>{why}</dd>
      </dl>
    </div>
  );
}

function Frame({ tag, white, children }: { tag: string; white?: boolean; children: React.ReactNode }) {
  return (
    <div className={`${c("frame")} ${white ? c("frame-white") : ""}`}>
      <span className={c("frame-tag")}>{tag}</span>
      {children}
    </div>
  );
}

const TRACK: { icon: IconName; label: string }[] = [
  { icon: "plan", label: "예상 공정표" },
  { icon: "standard", label: "표준견적서" },
  { icon: "vendors", label: "업체 고르기" },
  { icon: "quotes", label: "가견적 비교" },
  { icon: "measure", label: "실측 견적" },
  { icon: "schedule", label: "확정 공정표" },
];
const NOW = 3; // 가견적 비교 차례

export default async function DesignSamples() {
  const std = await getStandardQuote("p1");
  const shortSrc = std.sources.map((x) => x.split(" (")[0]);

  return (
    <>
      <SiteHeader />
      <main id="main" className={`mj-wrap ${c("root")}`}>
        <header className={c("intro")}>
          <p className="mj-eyebrow">디자인 예시 · 제안</p>
          <h1 className="mj-h1">믿집 화면에 더할 디자인 요소</h1>
          <p className="mj-sub">레퍼런스 사이트에서 가져온 방법을 우리 화면 내용으로 먼저 그려 봤어요. 실제 화면은 바꾸지 않았어요. 단지 · 업체 · 시공 사례는 모두 예시이고, 사진 자리는 그림으로 채웠어요.</p>
          <nav aria-label="예시 목록">
            <ol className={c("toc")}>
              {SECTIONS.map((x) => <li key={x.id}><a href={`#${x.id}`}><b>{x.no}</b>{x.title}</a></li>)}
            </ol>
          </nav>
        </header>

        {/* 01 */}
        <section id="chrome" className={c("sec")} aria-labelledby="chrome-h">
          <Head id="chrome-h" no="01" title="헤더 · 파비콘 · 아이콘 · 바닥글" where={<><code>components/site/SiteHeader.tsx</code> · <code>app/icon.svg</code>(새로 둠) · 바닥글은 새 파일</>}
            from="3.3디자인스페이스의 로고 자리, INSHOW의 메뉴 두 개짜리 헤더, R-O · NYC Renovation의 바닥글"
            why="지금은 글자 '믿집'만 있고 파비콘이 없어 탭에서 다른 사이트와 구분이 안 돼요. 바닥글이 없어서 사업자 정보 · 약관 · '거래 당사자가 아니에요' 고지를 둘 곳이 없어요." />

          <Frame tag="예시 · 헤더 (로그인한 고객)" white>
            <div className={c("hdr")} aria-hidden="true">
              <span className={c("brand")}><BrandMark size={30} /><b>믿집</b><small>도배 · 목공 견적 비교</small></span>
              <span className={c("hdr-nav")}><span className={s.on}>내 프로젝트</span></span>
              <span className={c("hdr-r")}><span className={c("fake-btn")}>견적 받기</span><span className={c("fake-avatar")}><Person /></span></span>
            </div>
            <p className="mj-small" style={{ marginTop: 12 }}>표시 + 글자 + 한 줄 설명. 폰 너비에서는 한 줄 설명을 숨겨요. 메뉴 수는 지금처럼 하나로 둬요.</p>
          </Frame>

          <div className={c("pair")}>
            <Frame tag="예시 · 브라우저 탭과 파비콘">
              <div aria-hidden="true">
                <div className={c("tabs")}>
                  <span className={`${c("tab")} ${s.on}`}><BrandMark size={16} /><span>가견적 비교 · 믿집</span></span>
                  <span className={c("tab")}><BrandMark size={16} /><span>표준견적서 · 믿집</span></span>
                  <span className={c("tab")}><BrandMark size={16} /><span>결도배 · 믿집</span></span>
                </div>
                <div className={c("tabs-bar")} />
              </div>
              <p className="mj-small" style={{ marginTop: 12 }}>파비콘은 한 가지로 두고, 쪽마다 다른 것은 제목 글자로 알려요. 제목은 <b>화면 이름 · 믿집</b> 순서예요.</p>
              <div className={c("sizes")} style={{ marginTop: 14 }}>
                {[16, 32, 48, 64].map((n) => <figure key={n}><BrandMark size={n} /><figcaption className="mj-num">{n}px</figcaption></figure>)}
              </div>
            </Frame>

            <Frame tag="예시 · 기능 아이콘 (선 1.8px, 24px 격자)">
              <ul className={c("icons")}>
                {FEATURE_ICONS.map((x) => (
                  <li key={x.name}><i><FeatureIcon name={x.name} /></i><span>{x.label}<small>{x.where}</small></span></li>
                ))}
              </ul>
              <p className="mj-small" style={{ marginTop: 12 }}>프로젝트 단계 이동과 진행 현황 줄 앞에만 써요. 버튼마다 붙이지 않아요.</p>
            </Frame>
          </div>

          <Frame tag="예시 · 바닥글 (링크는 눌러지지 않아요)" white>
            <footer className={c("foot")} aria-label="바닥글 예시">
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                <span className={c("brand")} style={{ minHeight: 0 }}><BrandMark size={24} /><b style={{ fontSize: "var(--fs-lg)" }}>믿집</b></span>
                <p>공공 기준으로 계산한 표준견적서를 보여 드리고, 견적은 업체가 직접 써서 내요.</p>
              </div>
              <div>
                <h3>서비스</h3>
                <ul><li><span>견적 받기</span></li><li><span>내 프로젝트</span></li><li><span>기준 단가 출처</span></li></ul>
              </div>
              <div>
                <h3>약관 · 정책</h3>
                <ul><li><span>이용약관</span></li><li><span><b>개인정보 처리방침</b></span></li><li><span>문의하기</span></li></ul>
              </div>
              <div>
                <h3>사업자 정보</h3>
                <p>상호 · 대표 · 사업자등록번호 · 주소 · 연락처는 정해지면 넣어요.</p>
              </div>
              <p className={c("foot-note")}>믿집은 거래 당사자가 아니에요. 계약과 대금은 업체와 직접 해요. 표준견적서는 참고 금액이고 업체 견적이 아니에요.</p>
            </footer>
          </Frame>
        </section>

        {/* 02 */}
        <section id="home" className={c("sec")} aria-labelledby="home-h">
          <Head id="home-h" no="02" title="홈 첫 화면" where={<code>app/page.tsx</code>}
            from="Loam House의 번호 붙은 묶음과 크게 쓴 '숫자 + 단위', NYC Renovation · RS.D의 단계 띠, 3.3디자인스페이스의 큰 제목"
            why="지금 홈은 제목 · 한 줄 · 버튼 두 개뿐이라 무엇을 받는지 안 보여요. 사진 대신 우리 결과물(표준견적서)을 첫 화면 그림으로 쓰면 지어낸 사진 없이도 뜻이 바로 전해져요." />
          <Frame tag="예시 · 홈 첫 화면 (버튼은 눌러지지 않아요)" white>
            <div className={c("hero")}>
              <div className={c("hero-copy")}>
                <p className="mj-eyebrow">아파트 도배 · 목공</p>
                <h3>공공 기준과 비교하면서<br />우리 집 업체를 골라요</h3>
                <p className={c("hero-lead")}>표준견적서로 기준 금액을 먼저 보고, 여러 업체의 가견적을 같은 양식으로 받아 줄마다 비교해요.</p>
                <div className="mj-btn-row" aria-hidden="true">
                  <span className="mj-btn mj-btn-pri">견적 받기 시작</span>
                  <span className="mj-btn mj-btn-sec">예시 프로젝트 보기</span>
                </div>
              </div>
              <figure className={c("ledger")} style={{ margin: 0 }} aria-label="표준견적서 미리보기 예시">
                <div className={c("ledger-h")}><b>표준견적서</b><span className="mj-small">늘봄마을 2단지 34평형 · 예시</span></div>
                <dl>
                  <div><dt>도배<small className="mj-num"><span className={c("nb")}>벽 {std.qty.wall}㎡</span> · <span className={c("nb")}>천장 {std.qty.ceil}㎡</span></small></dt><dd>{won(std.totals.dobae)}</dd></div>
                  <div><dt>목공<small className="mj-num"><span className={c("nb")}>천장 몰딩 {std.qty.molding}m</span> · <span className={c("nb")}>걸레받이 {std.qty.base}m</span></small></dt><dd>{won(std.totals.mokgong)}</dd></div>
                  <div className={s.total}><dt>합계<small>VAT 별도</small></dt><dd>{won(std.totals.all)}</dd></div>
                </dl>
                <figcaption className={c("ledger-f")}>공공 기준 {std.sources.length}가지로 믿집이 계산한 참고 금액이에요. 업체 견적이 아니에요. {std.excluded[0]} 등 {std.excluded.length}가지는 빠져 있어요.</figcaption>
              </figure>
            </div>
            <ol className={c("how")} style={{ marginTop: 32 }}>
              <li><b>01</b><h4>집 정보 고르기</h4><p>지역 · 평수 · 공정만 골라요. 질문은 9~11개예요.</p></li>
              <li><b>02</b><h4>기준부터 보기</h4><p>표준견적서와 예상 공정표가 바로 나와요.</p></li>
              <li><b>03</b><h4>가견적 비교하기</h4><p>고른 업체가 같은 양식으로 써서 내요.</p></li>
              <li><b>04</b><h4>실측하고 확정하기</h4><p>업체 한 곳이 재고 실측 견적을 내요.</p></li>
            </ol>
            <p className={c("src")}><b>기준 출처</b>{shortSrc.map((x) => <span key={x} className="mj-chip">{x}</span>)}</p>
          </Frame>
        </section>

        {/* 03 */}
        <section id="quote" className={c("sec")} aria-labelledby="quote-h">
          <Head id="quote-h" no="03" title="견적 받기 창" where={<><code>components/start/Wizard.tsx</code> 머리 · 첫 질문 위 · 도배 유형 질문</>}
            from="INSHOW 상담 신청 전 안내(걸리는 시간 · 비용 · 준비물), Loam House 3단계 문의와 '연락처 걱정 없음' 문구, Storey 번호 붙은 질문, 3.3디자인스페이스의 '알아보기' 펼침과 견본 고르기"
            why="'1 / 9' 막대는 도배 · 목공을 고르면 전체 수가 바뀌어요. 묶음 이름이 보이면 남은 일이 짐작돼요. 저가형 · 기본형은 글자만 있어서 차이를 알 수 없어요." />
          <Frame tag="예시 · 진행 표시를 묶음 4개로 (이전 · 다음을 눌러 보세요)">
            <div className={c("qwrap")}>
              <div className={c("before")}>
                <b>시작 전에 알아 두세요</b>
                <ul>
                  <li><i><FeatureIcon name="history" size={20} /></i><div><b>질문 9~11개</b><span>답은 저절로 저장돼요. 닫았다가 이어서 쓸 수 있어요.</span></div></li>
                  <li><i><FeatureIcon name="measure" size={20} /></i><div><b>평형과 사진이 있으면 좋아요</b><span>도면 · 사진이 없어도 견적을 받을 수 있어요.</span></div></li>
                  <li><i><FeatureIcon name="vendors" size={20} /></i><div><b>업체에는 구까지만 보여요</b><span>동 · 호수와 연락처는 실측을 확정하고 동의한 뒤 그 업체에만 보여요.</span></div></li>
                </ul>
              </div>
              <ProgressDemo />
            </div>
          </Frame>
          <h3 className={c("sub")}>도배 유형을 견본 카드로</h3>
          <Frame tag="예시 · 도배 유형 고르기 (등급 구성은 아직 정하지 않았어요)" white>
            <GradeCards />
          </Frame>
        </section>

        {/* 04 */}
        <section id="case" className={c("sec")} aria-labelledby="case-h">
          <Head id="case-h" no="04" title="업체 시공 사례" where={<><code>app/vendors/[id]/page.tsx</code> 포트폴리오 칸 · 사례 상세</>}
            from="INSHOW 사례 상세(왼쪽 고정 사양표 + 오른쪽 사진), 3.3디자인스페이스 사례(완공일 · 공사기간 · 공사 범위 한 줄), 시공 전후 비교 슬라이더"
            why="지금은 회색 '사진' 칸뿐이에요. 고객은 사진보다 '무엇을 어떻게 했는지'로 업체를 판단해요(vendor-portfolio.md). 같은 자리 전후 비교가 가장 강한 근거예요." />
          <Frame tag="예시 · 시공 사례 상세 (그림 · 실제 사진 필요)" white>
            <div className={c("case")}>
              <aside className={c("case-aside")} aria-label="사례 정보">
                <div className="mj-chips"><span className="mj-badge mj-b-ok"><Check size={14} />믿집에서 진행한 공사</span><span className="mj-badge">예시</span></div>
                <h3>마포구 30평대 실크 도배 · 천장 몰딩</h3>
                <p className="mj-small">결도배 (예시) · 도배</p>
                <dl className={c("facts")}>
                  <div><dt>끝난 달</dt><dd>2026.10</dd></div>
                  <div><dt>걸린 기간</dt><dd>2일</dd></div>
                  <div><dt>공간</dt><dd>4곳</dd></div>
                </dl>
                <dl className="mj-kv">
                  <dt>벽지 종류</dt><dd>실크</dd>
                  <dt>천장</dt><dd>포함</dd>
                  <dt>기존 벽지</dt><dd>철거함</dd>
                  <dt>초배</dt><dd>전체</dd>
                  <dt>끝선 마감</dt><dd>몰딩 위</dd>
                  <dt>자재</dt><dd>업체가 적은 브랜드 · 품번<br /><span className="mj-tiny">믿집이 확인하지 않은 정보예요</span></dd>
                </dl>
                <div className="mj-chips" aria-label="공간">{["거실", "안방", "작은방", "주방"].map((x) => <span key={x} className="mj-chip">{x}</span>)}</div>
              </aside>
              <div className={c("case-main")}>
                <BeforeAfter />
                <p className="mj-label" style={{ marginTop: 8 }}>도배 사례에 꼭 넣을 사진</p>
                <ul className={c("shots")}>
                  <li><span className={c("shot")}>사진 자리</span><span>완공 전경<br /><small>문틀에서 가슴 높이</small></span></li>
                  <li><span className={c("shot")}>사진 자리</span><span>이음매 근접<br /><small>빛이 옆에서 들 때</small></span></li>
                  <li><span className={c("shot")}>사진 자리</span><span>천장 경계선<br /><small>몰딩 끝선</small></span></li>
                </ul>
              </div>
            </div>
          </Frame>
        </section>

        {/* 05 */}
        <section id="project" className={c("sec")} aria-labelledby="project-h">
          <Head id="project-h" no="05" title="내 프로젝트 · 진행 현황" where={<><code>app/my/page.tsx</code> 프로젝트 카드 · <code>app/projects/[id]/page.tsx</code> 맨 위</>}
            from="Woonpact의 01~05 일정 띠와 '지금 단계' 표시, GOV.UK 할 일 목록(mypage-vendor-info.md 5.3)"
            why="지금 카드는 지역 · 평수 · 만든 날뿐이라 누구 차례인지 안 보여요. 단계 띠 + 공정별 차례 + 버튼 하나로 '지금 내가 할 일'을 먼저 보여요." />
          <Frame tag="예시 · 프로젝트 카드 (버튼은 눌러지지 않아요)">
            <article className={c("pcard")} aria-label="늘봄마을 2단지 34평형 예시 프로젝트">
              <div className={c("pcard-h")}>
                <h3>늘봄마을 2단지 34평형 <span className="mj-badge">예시</span></h3>
                <span className="mj-small mj-num">마포구 · 만든 날 {md("2026-10-20")}</span>
              </div>
              <ol className={c("track")} aria-label="프로젝트 단계">
                {TRACK.map((t, k) => (
                  <li key={t.label} className={k < NOW ? s.done : k === NOW ? s.cur : undefined} aria-current={k === NOW ? "step" : undefined}>
                    <span className={c("dot")}>{k < NOW ? <Check /> : <FeatureIcon name={t.icon} size={18} />}</span>
                    <span className={c("track-label")}>{t.label}{k < NOW ? <span className="mj-sr"> · 끝남</span> : null}</span>
                    {k === NOW ? <span className={c("now")}>지금</span> : null}
                  </li>
                ))}
              </ol>
              <ul className={c("rows")} aria-label="공정별 차례">
                <li><b>도배</b><span className={c("turn-me")}>내 차례</span><span>가견적 3곳 중 2곳 도착<span className={c("new")}>새로 왔어요</span></span></li>
                <li><b>목공</b><span className={c("turn-them")}>업체 차례</span><span className="mj-num">나무결목공 (예시) 실측 {md("2026-11-02")} 오전 · 실측 견적을 기다려요</span></li>
              </ul>
              <div className="mj-btn-row" aria-hidden="true">
                <span className="mj-btn mj-btn-pri">도배 가견적 비교하기</span>
                <span className="mj-btn mj-btn-ghost">프로젝트 보기</span>
              </div>
            </article>
          </Frame>

          <h3 className={c("sub")}>프로젝트가 없을 때</h3>
          <Frame tag="예시 · 빈 상태" white>
            <div className={c("empty")}>
              <svg className={c("empty-art")} viewBox="0 0 200 140" aria-hidden="true">
                <path d="M30 70 100 18l70 52" fill="none" stroke="currentColor" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
                <rect x="48" y="66" width="104" height="62" rx="6" fill="none" stroke="currentColor" strokeWidth="6" />
                <path d="M70 88h60M70 106h36" stroke="var(--accent)" strokeWidth="5" strokeLinecap="round" />
              </svg>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                <b style={{ fontSize: "var(--fs-lg)" }}>아직 만든 프로젝트가 없어요</b>
                <p className="mj-sub">집 정보를 고르면 표준견적서와 예상 공정표가 바로 나와요.</p>
                <ol><li>집 정보 · 공정 고르기</li><li>표준견적서로 기준 보기</li><li>업체 골라 가견적 받기</li></ol>
                <div className="mj-btn-row" aria-hidden="true"><span className="mj-btn mj-btn-pri">견적 받기 시작</span></div>
              </div>
            </div>
          </Frame>
        </section>

        <p className={`mj-small ${c("end")}`}>설명과 정할 것은 <code>docs/design/visual-design.md</code>에 있어요. <Link href="/">홈으로</Link></p>
      </main>
    </>
  );
}
