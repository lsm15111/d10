import Link from "next/link";
import { SiteHeader } from "@/components/site/SiteHeader";
import { MyPageNav } from "@/components/my/MyPageNav";
import { ProfileForm } from "@/components/my/ProfileForm";
import { requireRole } from "@/lib/session";

export const metadata = { title: "내 정보 · 설정" };

// 마이페이지 · 내 정보 · 설정 (FFW-17). 헤더 계정 메뉴에서 들어온다. 고객과 업체가 함께 쓴다.
// 비밀번호 바꾸기 · 알림 · 동의 내역은 API가 생기면 이 쪽에 묶음으로 더한다 (docs/design/mypage-vendor-info.md 5.4).
export default async function AccountPage() {
  const s = await requireRole(["customer", "vendor"], "/account");
  return (
    <>
      <SiteHeader />
      <main id="main" className="mj-wrap mj-main" style={{ maxWidth: 760 }}>
        <MyPageNav role={s.role} current="/account" />
        <h1 className="mj-h1">내 정보 · 설정</h1>
        <section aria-labelledby="acc-h" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <h2 id="acc-h" className="mj-h2">회원 정보</h2>
          <ProfileForm name={s.name} email={s.email} labelledBy="acc-h" />
        </section>
        <section aria-labelledby="out-h" className="mj-panel" style={{ maxWidth: 520 }}>
          <h2 id="out-h" className="mj-h3">회원 탈퇴</h2>
          <p className="mj-small">탈퇴하면 회원 정보와 {s.role === "vendor" ? "사업자등록증 · 업체 정보" : "프로젝트 · 사진 · 도면"}를 바로 지워요.</p>
          <Link href="/account/withdraw" className="mj-btn mj-btn-sec" style={{ alignSelf: "flex-start" }}>탈퇴하기</Link>
        </section>
      </main>
    </>
  );
}
