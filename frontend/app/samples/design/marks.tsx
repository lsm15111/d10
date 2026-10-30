// 디자인 예시용 표시 · 기능 아이콘. 색은 currentColor와 토큰만 쓴다.
// BrandMark는 app/icon.svg(파비콘)와 같은 모양이다.

export function BrandMark({ size = 28, title }: { size?: number; title?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" role={title ? "img" : undefined} aria-hidden={title ? undefined : true} aria-label={title}>
      <rect width="32" height="32" rx="8" fill="var(--accent)" />
      <path d="M6.5 14.5 16 7l9.5 7.5" fill="none" stroke="var(--bg)" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
      <rect x="10" y="14.5" width="12" height="10.5" rx="1.5" fill="none" stroke="var(--bg)" strokeWidth="2.6" />
    </svg>
  );
}

export type IconName = "hub" | "plan" | "standard" | "vendors" | "quotes" | "measure" | "schedule" | "history";

/** 화면 이름 ↔ 아이콘. 프로젝트 이동(ProjectNav) 순서와 같다. */
export const FEATURE_ICONS: { name: IconName; label: string; where: string }[] = [
  { name: "hub", label: "진행 현황", where: "/projects/[id]" },
  { name: "plan", label: "예상 공정표", where: "/plan" },
  { name: "standard", label: "표준견적서", where: "/standard" },
  { name: "vendors", label: "업체 고르기", where: "/vendors" },
  { name: "quotes", label: "가견적 비교", where: "/quotes" },
  { name: "measure", label: "실측 견적", where: "/measure" },
  { name: "schedule", label: "확정 공정표", where: "/schedule" },
  { name: "history", label: "이력", where: "/history" },
];

// 24px 격자, 선 1.8px, 둥근 끝. AccountMenu의 사람 아이콘과 같은 굵기다.
const PATHS: Record<IconName, React.ReactNode> = {
  hub: <path d="M4 11.2 12 4.8l8 6.4V19a1 1 0 0 1-1 1h-4.5v-5h-5v5H5a1 1 0 0 1-1-1z" />,
  plan: <><path d="M4 6.5h8" /><path d="M8 12h10" /><path d="M13 17.5h7" /><path d="M4 4v16" /></>,
  standard: <><rect x="5" y="3.5" width="14" height="17" rx="2" /><path d="M8.5 8.5h7M8.5 12h7M8.5 15.5h4" /></>,
  vendors: <><circle cx="10.5" cy="10.5" r="5.5" /><path d="m15 15 4.5 4.5" /></>,
  quotes: <><rect x="3.5" y="5" width="7.5" height="14" rx="1.5" /><rect x="13" y="5" width="7.5" height="14" rx="1.5" /><path d="M6 9h2.5M15.5 9h2.5M6 12.5h2.5M15.5 12.5h2.5" /></>,
  measure: <><rect x="2.5" y="8.5" width="19" height="7" rx="1.5" /><path d="M6.5 8.5v3M10 8.5v2M13.5 8.5v3M17 8.5v2" /></>,
  schedule: <><rect x="4" y="5.5" width="16" height="14.5" rx="2" /><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4" /><path d="m9 15 2 2 4-4" /></>,
  history: <><circle cx="12" cy="12" r="8" /><path d="M12 8v4l2.6 2.6" /></>,
};

export function FeatureIcon({ name, size = 24 }: { name: IconName; size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {PATHS[name]}
    </svg>
  );
}

/** 계정 아이콘 (components/site/AccountMenu.tsx와 같은 모양) */
export function Person({ size = 22 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" aria-hidden="true">
      <circle cx="12" cy="8.5" r="3.8" /><path d="M4.5 20c1.4-3.6 4.2-5.4 7.5-5.4s6.1 1.8 7.5 5.4" />
    </svg>
  );
}

export function Check({ size = 16 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m3.5 8.5 3 3 6-6.5" />
    </svg>
  );
}
