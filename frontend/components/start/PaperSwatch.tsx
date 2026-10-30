// 벽지 종류 견본. 실제 사진이 있으면 사진을, 없으면 그림을 보인다.
// 실제 사진: 사용 허락을 받은 사진(직접 찍은 샘플북 사진 등)을 public/images/wallpaper/에 넣고 PHOTOS에 경로를 적는다.
// 그림: 실크는 은은한 광택과 맞댐 이음새(거의 안 보임), 합지는 무광 종이 결과 겹침 이음새(살짝 보임).
const PHOTOS: Partial<Record<"silk" | "hapji", string>> = {};

export function PaperSwatch({ kind }: { kind: "silk" | "hapji" }) {
  const id = `sw-${kind}`;
  const src = PHOTOS[kind];
  if (src) return <img className="mj-swatch" src={src} alt="" />;
  if (kind === "silk") {
    return (
      <svg className="mj-swatch" viewBox="0 0 64 64" aria-hidden="true">
        <defs>
          <linearGradient id={`${id}-sheen`} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="var(--bg)" stopOpacity="0.95" />
            <stop offset="0.45" stopColor="var(--bg)" stopOpacity="0.1" />
            <stop offset="0.7" stopColor="var(--bg)" stopOpacity="0.65" />
            <stop offset="1" stopColor="var(--bg)" stopOpacity="0" />
          </linearGradient>
          <pattern id={`${id}-weave`} width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <path d="M0 0v4" stroke="var(--line)" strokeWidth="1" opacity="0.7" />
          </pattern>
        </defs>
        <rect width="64" height="64" rx="8" fill="var(--surface-2)" />
        <rect width="64" height="64" rx="8" fill={`url(#${id}-weave)`} />
        <rect width="64" height="64" rx="8" fill={`url(#${id}-sheen)`} />
        <path d="M33 0v64" stroke="var(--line)" strokeWidth="0.6" opacity="0.6" />
      </svg>
    );
  }
  return (
    <svg className="mj-swatch" viewBox="0 0 64 64" aria-hidden="true">
      <defs>
        <pattern id={`${id}-fiber`} width="8" height="8" patternUnits="userSpaceOnUse">
          <circle cx="1.5" cy="2" r="0.7" fill="var(--line-strong)" opacity="0.35" />
          <circle cx="5.5" cy="5" r="0.6" fill="var(--line-strong)" opacity="0.3" />
          <path d="M3 7.2l2.6-.8" stroke="var(--line-strong)" strokeWidth="0.5" opacity="0.3" />
        </pattern>
      </defs>
      <rect width="64" height="64" rx="8" fill="var(--surface)" />
      <rect width="64" height="64" rx="8" fill={`url(#${id}-fiber)`} />
      <rect x="31" y="0" width="4" height="64" fill="var(--line)" opacity="0.8" />
      <path d="M35 0v64" stroke="var(--line-strong)" strokeWidth="0.8" opacity="0.55" />
    </svg>
  );
}
