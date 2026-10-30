// 마이페이지 두 쪽(내 프로젝트 · 내 정보 · 설정) 위에 같은 작은 이동 메뉴를 둔다. 업체는 업체 홈 · 내 정보 · 설정.
import Link from "next/link";
import type { Role } from "@/lib/types";

export function MyPageNav({ role, current }: { role: Role; current: "/my" | "/vendor" | "/account" }) {
  const items = role === "vendor"
    ? [{ href: "/vendor", label: "업체 홈" }, { href: "/account", label: "내 정보 · 설정" }]
    : [{ href: "/my", label: "내 프로젝트" }, { href: "/account", label: "내 정보 · 설정" }];
  return (
    <nav aria-label={role === "vendor" ? "업체 메뉴" : "마이페이지"} className="mj-mynav">
      {items.map((it) => <Link key={it.href} href={it.href} aria-current={current === it.href ? "page" : undefined}>{it.label}</Link>)}
    </nav>
  );
}
