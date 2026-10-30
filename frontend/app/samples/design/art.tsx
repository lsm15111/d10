// 사진 자리를 채우는 그림. 실제 사진이 아니라는 표시를 늘 함께 붙인다.
// 색은 토큰만 쓴다(얼룩 = warn 계열, 이음매 = line 계열).

/** 벽 한 면: 천장 몰딩 · 벽지 이음매 · 문선 · 콘센트 · 걸레받이. before는 얼룩 · 들뜸 · 벌어진 이음매. */
export function WallScene({ variant, id }: { variant: "before" | "after"; id: string }) {
  const before = variant === "before";
  const seams = [70, 128, 186, 244, 302, 360];
  return (
    <svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true" style={{ display: "block", width: "100%", height: "100%" }}>
      <defs>
        <linearGradient id={`${id}-sheen`} x1="0" y1="0" x2="1" y2="0.4">
          <stop offset="0" stopColor="var(--bg)" stopOpacity="0.9" />
          <stop offset="0.5" stopColor="var(--bg)" stopOpacity="0" />
          <stop offset="1" stopColor="var(--bg)" stopOpacity="0.55" />
        </linearGradient>
        <pattern id={`${id}-floor`} width="60" height="28" patternUnits="userSpaceOnUse">
          <path d="M0 27.5h60M30 0v28" stroke="var(--line-strong)" strokeWidth="1" opacity="0.35" />
        </pattern>
      </defs>
      {/* 천장 */}
      <rect width="400" height="40" fill={before ? "var(--surface-2)" : "var(--bg)"} />
      {/* 벽 */}
      <rect y="40" width="400" height="224" fill={before ? "var(--surface-2)" : "var(--surface)"} />
      {!before ? <rect y="40" width="400" height="224" fill={`url(#${id}-sheen)`} /> : null}
      {/* 벽지 이음매: 시공 전은 벌어져 보이고, 완공은 거의 안 보인다 */}
      {seams.map((x) => (
        <path key={x} d={`M${x} 48v214`} stroke={before ? "var(--line-strong)" : "var(--line)"} strokeWidth={before ? 1.6 : 0.8} strokeDasharray={before ? "10 6" : undefined} opacity={before ? 0.7 : 0.6} />
      ))}
      {before ? (
        <>
          {/* 얼룩 */}
          <ellipse cx="160" cy="104" rx="30" ry="20" fill="var(--warn-weak)" stroke="var(--warn)" strokeOpacity="0.35" />
          <ellipse cx="152" cy="110" rx="12" ry="8" fill="var(--warn)" opacity="0.12" />
          <ellipse cx="104" cy="222" rx="20" ry="13" fill="var(--warn-weak)" stroke="var(--warn)" strokeOpacity="0.3" />
          {/* 들뜬 모서리 */}
          <path d="M128 48h22l-22 30z" fill="var(--bg)" stroke="var(--line-strong)" strokeWidth="1.2" />
          <path d="M128 78l22-30" stroke="var(--ink-mute)" strokeWidth="0.8" opacity="0.5" />
        </>
      ) : null}
      {/* 천장 몰딩 */}
      <rect y="40" width="400" height={before ? 6 : 9} fill="var(--bg)" stroke="var(--line-strong)" strokeWidth="1" />
      {/* 문선 · 문 */}
      <rect x="22" y="78" width="40" height="186" fill="none" stroke={before ? "var(--line-strong)" : "var(--ink-sub)"} strokeWidth={before ? 4 : 5} />
      <rect x="26" y="82" width="32" height="182" fill={before ? "var(--surface)" : "var(--bg)"} />
      <circle cx="52" cy="176" r="2.6" fill="var(--ink-sub)" />
      {/* 콘센트 */}
      <rect x="286" y="206" width="20" height="26" rx="3" fill="var(--bg)" stroke="var(--line-strong)" strokeWidth="1.2" />
      <path d="M293 216v6M299 216v6" stroke="var(--ink-sub)" strokeWidth="1.4" strokeLinecap="round" />
      {/* 걸레받이 · 바닥 */}
      <rect y="258" width="400" height={before ? 6 : 8} fill="var(--bg)" stroke="var(--line-strong)" strokeWidth="1" />
      <rect y="266" width="400" height="34" fill="var(--surface-2)" />
      <rect y="266" width="400" height="34" fill={`url(#${id}-floor)`} />
    </svg>
  );
}

/** 도배 유형 견본 그림. 실크 = 은은한 광택 · 맞댐 이음, 합지 = 무광 종이 결 · 겹침 이음 (components/start/PaperSwatch.tsx와 같은 표현) */
export function PaperArt({ kind, id }: { kind: "silk" | "hapji"; id: string }) {
  if (kind === "silk") {
    return (
      <svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true" style={{ display: "block", width: "100%", height: "100%" }}>
        <defs>
          <linearGradient id={`${id}-sheen`} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="var(--bg)" stopOpacity="0.95" />
            <stop offset="0.45" stopColor="var(--bg)" stopOpacity="0.1" />
            <stop offset="0.72" stopColor="var(--bg)" stopOpacity="0.7" />
            <stop offset="1" stopColor="var(--bg)" stopOpacity="0" />
          </linearGradient>
          <pattern id={`${id}-weave`} width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <path d="M0 0v5" stroke="var(--line)" strokeWidth="1" opacity="0.8" />
          </pattern>
        </defs>
        <rect width="320" height="180" fill="var(--surface-2)" />
        <rect width="320" height="180" fill={`url(#${id}-weave)`} />
        <rect width="320" height="180" fill={`url(#${id}-sheen)`} />
        <path d="M160 0v180" stroke="var(--line)" strokeWidth="0.8" opacity="0.7" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true" style={{ display: "block", width: "100%", height: "100%" }}>
      <defs>
        <pattern id={`${id}-fiber`} width="10" height="10" patternUnits="userSpaceOnUse">
          <circle cx="2" cy="2.5" r="0.8" fill="var(--line-strong)" opacity="0.35" />
          <circle cx="7" cy="6.5" r="0.7" fill="var(--line-strong)" opacity="0.3" />
          <path d="M3.5 9l3.2-1" stroke="var(--line-strong)" strokeWidth="0.6" opacity="0.3" />
        </pattern>
      </defs>
      <rect width="320" height="180" fill="var(--surface)" />
      <rect width="320" height="180" fill={`url(#${id}-fiber)`} />
      <rect x="156" width="8" height="180" fill="var(--line)" opacity="0.85" />
      <path d="M164 0v180" stroke="var(--line-strong)" strokeWidth="1" opacity="0.55" />
    </svg>
  );
}
