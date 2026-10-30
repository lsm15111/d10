"""화면설계서 쪽 목록: 화면마다 캡처할 상태, 번호 표시할 요소, 설명, Check Point.

M(선택자, 제목, 설명...) — 선택자는 Playwright 문법. 번호는 목록 순서대로 붙는다.
top: 캡처를 시작할 y(숫자) 또는 그 요소의 위쪽(선택자). h: 캡처 높이.
dialog=True: 견적 받기 창처럼 화면 위에 뜬 창이라 보이는 화면 그대로 찍는다.
part: 긴 화면 · 같은 화면의 다른 상태를 같은 화면 ID로 여러 쪽에 싣는다.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Callable


@dataclass
class M:
    sel: str
    title: str
    desc: tuple[str, ...]

    def __init__(self, sel: str, title: str, *desc: str):
        self.sel, self.title, self.desc = sel, title, desc


@dataclass
class S:
    id: str
    name: str
    path: str
    req: str
    url: str
    marks: list[M]
    check: tuple[str, list[str]] | None = None
    role: str | None = None
    prep: Callable | None = None
    top: int | str = 0
    h: int = 900
    dialog: bool = False
    vh: int = 900
    expand: bool = False
    group: str = ""
    part: int = 1

    @property
    def key(self) -> str:
        return self.id if self.part == 1 else f"{self.id}_{self.part}"


def sec(title: str) -> str:
    """제목(h1~h3 · legend · caption)이 들어 있는 가장 가까운 덩어리(section · fieldset · panel)."""
    return (f"xpath=//*[self::h1 or self::h2 or self::h3 or self::legend][contains(normalize-space(.), '{title}')]"
            "/ancestor::*[self::section or self::fieldset or contains(concat(' ', @class, ' '), ' mj-panel ')][1]")


def panel(eyebrow: str) -> str:
    """작은 머리말(mj-eyebrow)로 시작하는 패널."""
    return f"section.mj-panel:has(.mj-eyebrow:has-text('{eyebrow}'))"


def field_of(label: str) -> str:
    return f".mj-field:has(label:has-text('{label}'))"


def btn(name: str) -> str:
    return f"role=button[name='{name}'] >> nth=0"


def link(name: str) -> str:
    return f"role=link[name='{name}'] >> nth=0"


def h1(text: str) -> str:
    return f"main h1:has-text('{text}')"


DLG = "dialog.mj-dialog[open]"
TABPANEL = "main [role=tabpanel]"

# ── 견적 받기 창: 임시 저장(localStorage)에 답을 넣고 창을 열면 그 질문부터 보인다
_start = date.today() + timedelta(days=24)
SPACES = [{"id": "sp-a", "name": "거실", "custom": True}, {"id": "sp-b", "name": "방 1", "custom": True},
          {"id": "sp-c", "name": "방 2", "custom": True}, {"id": "sp-d", "name": "주방", "custom": True}]
BASE = {
    "sido": "seoul", "sgg": "마포구", "house": "apt", "builtYear": "2009", "size": "30", "manualM2": "", "balconyExt": True,
    "when": "date", "whenDate": _start.isoformat(), "whenEnd": (_start + timedelta(days=5)).isoformat(), "occupied": "yes",
    "budget": "500만~700만 원", "trades": {"dobae": True, "mokgong": True},
    "dobae": {"spaces": ["sp-a", "sp-b", "sp-c"], "grade": "basic"},
    "mokgong": {"spaces": ["sp-a", "sp-d"], "items": ["천장 몰딩", "걸레받이"]}, "spaces": SPACES,
}


def blur(page):
    page.mouse.move(0, 0)
    page.evaluate("() => document.activeElement && document.activeElement.blur()")


def wizard(step: str, **over) -> Callable:
    def prep(page, st, files):
        a = {**BASE, **over}
        page.evaluate("d => localStorage.setItem('mj_start_draft_v3', JSON.stringify(d))", {"a": a, "step": step})
        page.click("header >> role=button[name='견적 받기']")
        page.wait_for_selector(f"{DLG} .mj-wiz-body h1")
        if step == "photos":
            page.set_input_files(f"{DLG} input#ph-sp-a", [files["room1"], files["room2"]])
            page.wait_for_timeout(400)
        if step == "plan":
            page.set_input_files(f"{DLG} input#plan", [files["plan"]])
            page.wait_for_timeout(400)
        blur(page)
    return prep


def open_menu(page, st, files):
    page.click(".mj-acct-btn")
    page.wait_for_selector(".mj-acct-menu:not([hidden])")


def signup_errors(page, st, files):
    page.click(btn("가입하기"))
    page.wait_for_timeout(300)
    blur(page)


def basket_one(page, st, files):
    page.goto(page.url.replace("/request", "/vendors"), wait_until="networkidle")
    page.locator("li.mj-vendor:has-text('마루와벽') >> role=button[name*='요청함에 담기']").first.click()
    page.wait_for_timeout(200)
    page.goto(page.url.replace("/vendors", "/request"), wait_until="networkidle")


def measure_before(page, st, files):
    page.click(btn("데모 · 확정 전 화면 보기"))
    page.wait_for_timeout(300)
    blur(page)


def reject_open(page, st, files):
    page.click(f"{sec('처리')} >> role=button[name*='반려'] >> nth=0")
    page.fill(f"{sec('처리')} >> input.mj-input", "사업자등록증 글자가 흐려서 사업자등록번호를 확인할 수 없어요.")
    blur(page)


PNAV = M(".mj-pnav", "프로젝트 단계 메뉴", "진행 현황 · 1~6단계 · 이력으로 이동", "지금 볼 수 있는 단계만 눌린다 (아직 연결 전이면 흐리게)")

SCREENS: list[S] = [
    # ───────────── 공통
    S("SC-01-001", "홈", "메인", "FFW-03", "/", group="공통", h=520, marks=[
        M(".mj-nav", "주 메뉴", "고객: 내 프로젝트 · 자주 묻는 질문", "업체: 업체 홈 · 관리자: 회원관리 · 업체관리"),
        M(link("로그인 · 회원가입"), "로그인 · 회원가입", "로그인 화면으로 이동 (로그인하면 계정 아이콘으로 바뀜)"),
        M("header >> role=button[name='견적 받기']", "견적 받기", "어느 화면에서든 견적 받기 질문 창을 엶", "업체 · 관리자에게는 보이지 않음"),
        M(btn("견적 받기 시작"), "견적 받기 시작", "견적 받기 질문 창을 엶 (로그인 없이 시작, 만들 때 로그인)"),
        M(link("내 프로젝트 보기"), "내 프로젝트 보기", "마이페이지 내 프로젝트로 이동 (로그인 안 했으면 로그인 뒤 돌아옴)"),
    ], check=("이어서 쓰기", ["쓰던 견적 요청서가 있으면 아래에 '이어서 쓰기' 카드가 나옴"])),

    S("SC-01-002", "로그인", "메인 > 로그인", "FFW-01, FBF-02", "/login", group="공통", marks=[
        M(field_of("이메일"), "이메일", "가입한 이메일 (대소문자 구분 없음)"),
        M(field_of("비밀번호"), "비밀번호", "같은 이메일 · IP로 15분에 10번 틀리면 잠시 막음"),
        M("main >> role=button[name='로그인']", "로그인", "권한에 맞는 화면으로 이동", "고객: 원래 보던 화면 · 업체: 업체 홈 · 관리자: 회원관리"),
        M("main >> role=link[name='회원가입']", "회원가입", "고객 회원가입으로 이동"),
    ], check=("로그인은 하나", ["고객 · 업체 · 관리자가 같은 화면에서 로그인", "틀리면 한 문장만 보여 주고 가입 여부는 알리지 않음"])),

    S("SC-01-003", "회원가입", "메인 > 로그인 > 회원가입", "FFW-02", "/signup", group="공통", h=1060, marks=[
        M(field_of("이름"), "이름", "견적 요청에 쓰는 이름"),
        M(field_of("이메일"), "이메일", "로그인 아이디. 이미 있으면 가입 안 됨"),
        M(field_of("비밀번호") + " >> nth=0", "비밀번호", "칸 아래 안내: 영문, 숫자, 8자 이상"),
        M(field_of("비밀번호 확인"), "비밀번호 확인", "위와 같아야 함"),
        M(sec("약관 동의"), "약관 동의", "이용약관 · 개인정보 수집 · 이용 (둘 다 필수)"),
        M(btn("가입하기"), "가입하기", "가입하고 바로 로그인한 상태로 원래 화면으로 이동"),
        M(link("업체로 가입하기"), "업체로 가입하기", "업체 회원가입으로 이동"),
    ], check=("고객 회원가입", ["가입은 견적 요청 · 진행 상황을 저장할 때만 필요"])),

    S("SC-01-003", "회원가입 · 입력 오류", "메인 > 회원가입 > 빈 칸으로 가입하기", "FFW-02", "/signup", group="공통", part=2, prep=signup_errors, h=1060, marks=[
        M(field_of("이름"), "칸 아래 오류", "칸마다 무엇을 고칠지 바로 아래에 보여 줌", "첫 번째로 고칠 칸으로 초점을 옮김"),
    ], check=("입력 오류 표시", ["색만으로 알리지 않고 문장으로 알림", "서버 검사 결과(이미 쓰는 이메일 등)도 같은 자리에 보여 줌"])),

    S("SC-01-004", "계정 메뉴", "메인(로그인 o) > 계정 아이콘", "FFW-17", "/my", role="customer", group="공통", prep=open_menu, h=620, marks=[
        M(".mj-acct-btn", "계정 아이콘", "누르면 계정 메뉴가 열림 (Esc · 바깥을 누르면 닫힘)"),
        M(".mj-acct-menu ul", "마이페이지", "내 프로젝트 · 내 정보 · 설정으로 이동"),
        M(".mj-acct-menu >> role=button[name='로그아웃']", "로그아웃", "서버 세션을 지우고 홈으로 이동"),
    ], check=("역할별 메뉴", ["고객: 마이페이지", "업체: 업체 홈 · 내 정보 · 설정", "관리자: 관리자 화면"])),

    S("SC-01-005", "자주 묻는 질문", "메인 > 자주 묻는 질문", "—", "/faq", group="공통", h=900, marks=[
        M("main details >> nth=0 >> summary", "질문", "누르면 답이 펼쳐지고 다시 누르면 접힘"),
        M("main details >> nth=0 >> table", "평수별 비용 표", "평수 · 총비용 · 평당 가격 · 예상 기간 (올수리 기준)"),
        M("main details >> nth=0 >> p.mj-small >> nth=0", "기준", "2025~2026년 수도권 · 반셀프 기준 · 턴키는 30~50% 더"),
        M("main details >> nth=1 >> summary", "반셀프와 턴키", "두 방식의 차이와 비용 차이"),
    ], check=("들어오는 곳", ["헤더 메뉴 '자주 묻는 질문'"])),

    # ───────────── 견적 받기
    S("SC-02-001", "견적 받기 · 지역", "메인 > 견적 받기 > 1 지역", "FFW-03", "/", group="견적 받기", dialog=True,
      prep=wizard("region"), expand=True, vh=1060, marks=[
        M(f"{DLG} .mj-wiz-x", "닫기", "창을 닫음. 답은 브라우저에 저장돼 다시 열면 이어서 씀"),
        M(f"{DLG} fieldset fieldset >> nth=0", "시 · 도", "2026.7 행정구역 개편 반영 (전남광주통합특별시 등)"),
        M(f"{DLG} fieldset fieldset >> nth=1", "시 · 군 · 구", "시 · 도를 고르면 나옴"),
        M(f"{DLG} .mj-wiz-foot >> role=button[name='다음']", "다음", "고르기만 해서는 넘어가지 않고 '다음'을 눌러야 넘어감", "빠진 답은 문장으로 알리고 그 칸으로 초점을 옮김"),
    ], check=("한 화면에 질문 하나", ["헤더 '견적 받기'와 홈 '견적 받기 시작'이 같은 창을 엶", "로그인 없이 끝까지 답할 수 있음", "창은 주소가 바뀌지 않음 · 같은 질문을 /start에서 한 화면으로도 엶", "창 높이는 화면에 맞추고 안쪽이 스크롤됨 (이 쪽은 펼쳐서 찍음)"])),

    S("SC-02-002", "견적 받기 · 집 종류", "메인 > 견적 받기 > 2 집 종류", "FFW-03", "/", group="견적 받기", dialog=True,
      prep=wizard("house"), marks=[
        M(f"{DLG} .mj-choices", "집 종류", "1차 범위는 아파트만. 나머지는 '준비 중이에요'로 막아 둠"),
        M(f"{DLG} {field_of('준공 연도')}", "준공 연도 (선택)", "4자리 숫자 · 1960년 ~ 올해"),
    ], check=("집 종류", ["준공 연도는 공정표 · 견적 참고용"])),

    S("SC-02-003", "견적 받기 · 평수", "메인 > 견적 받기 > 3 평수 > 정확히 적을게요", "FFW-03", "/", group="견적 받기", dialog=True,
      prep=wizard("size", size="manual", manualBasis="supply", manualM2="113.3"), marks=[
        M(f"{DLG} .mj-pick", "평형대", "10평대 ~ 50평 이상 중 대략 고르기"),
        M(f"{DLG} .mj-panel", "정확한 면적", "공급면적(평형) · 전용면적(실평수)을 고르고 ㎡로 적음", "소수점 한 자리까지"),
        M(f"{DLG} label.mj-choice:has-text('발코니')", "발코니 확장", "도배 면적 계산에 더함"),
    ], check=("면적 기준을 함께 저장", ["면적은 ㎡와 기준(공급 · 전용)을 같이 저장하고 평은 보여 줄 때만 계산"])),

    S("SC-02-004", "견적 받기 · 공사 시기", "메인 > 견적 받기 > 4 시기 > 날짜가 정해졌어요", "FFW-03", "/", group="견적 받기", dialog=True,
      prep=wizard("when"), expand=True, vh=1060, marks=[
        M(f"{DLG} label.mj-choice >> nth=0", "시기 고르기", "날짜 확정 · 이사 날만 · 1~2달 안 · 아직 몰라요"),
        M(f"{DLG} .mj-cal", "달력", "시작하는 날과 끝나는 날을 차례로 누름", "오늘 이전 · 2년 넘는 날은 막음"),
    ], check=("공사 시기", ["'이사하는 날만'은 날짜 하나", "'1~2달 안' · '아직 몰라요'는 날짜 없이 넘어감"])),

    S("SC-02-005", "견적 받기 · 집 상태", "메인 > 견적 받기 > 5 집 상태", "FFW-03", "/", group="견적 받기", dialog=True,
      prep=wizard("living"), marks=[
        M(f"{DLG} .mj-choices", "집 상태", "살면서 공사 · 빈집"),
        M(f"{DLG} .mj-wiz-foot >> role=button[name='이전']", "이전", "앞 질문으로. 답은 그대로 남음"),
    ], check=("집 상태", ["살면서 공사하면 예상 공정표의 작업 기간이 늘어남 (짐 있는 집 × 1.25)"])),

    S("SC-02-006", "견적 받기 · 예산", "메인 > 견적 받기 > 6 예산 (선택)", "FFW-03", "/", group="견적 받기", dialog=True,
      prep=wizard("budget"), marks=[
        M(f"{DLG} .mj-choices", "예산 구간", "300만 원 이하 ~ 1,000만 원 넘게 · 아직 정하지 않았어요"),
        M(f"{DLG} .mj-wiz-foot >> role=button[name='건너뛰기']", "건너뛰기", "선택 질문이라 답하지 않고 넘어갈 수 있음"),
    ], check=("예산은 안내에만", ["업체를 거르는 데 쓰지 않고 표준견적서와 비교해 안내하는 데만 씀"])),

    S("SC-02-007", "견적 받기 · 공정", "메인 > 견적 받기 > 7 공정", "FFW-04", "/", group="견적 받기", dialog=True,
      prep=wizard("trades"), marks=[
        M(f"{DLG} label.mj-choice:has-text('도배')", "도배", "벽지 · 천장지"),
        M(f"{DLG} label.mj-choice:has-text('목공')", "목공", "몰딩 · 걸레받이 · 문 · 천장"),
    ], check=("1차 범위는 도배 · 목공", ["고른 공정에 따라 다음 질문(도배 · 목공 상세)이 생김"])),

    S("SC-02-008", "견적 받기 · 도배", "메인 > 견적 받기 > 8 도배 공간 · 유형", "FFW-04", "/", group="견적 받기", dialog=True,
      prep=wizard("dobae"), marks=[
        M(f"{DLG} .mj-btn-row >> nth=0", "빠른 추가", "방 · 주방 · 거실 · 현관을 바로 넣음 (같은 이름은 번호를 붙임)"),
        M(f"{DLG} .mj-space-add", "공간 직접 적기", "예: 복도 · 20자까지"),
        M(f"{DLG} [role=group]", "도배할 공간", "넣은 공간 중 도배할 곳을 고름 · X로 공간 빼기"),
        M(f"{DLG} fieldset:has(> legend:has-text('도배 유형'))", "도배 유형", "저가형 · 기본형 중 하나 (필수)"),
    ], check=("공간은 공정끼리 같이 씀", ["도배에서 넣은 공간을 목공에서도 고를 수 있음"])),

    S("SC-02-009", "견적 받기 · 목공", "메인 > 견적 받기 > 9 목공 공간 · 항목", "FFW-04", "/", group="견적 받기", dialog=True,
      prep=wizard("mokgong"), expand=True, vh=1060, marks=[
        M(f"{DLG} [role=group]", "목공할 공간", "도배에서 넣은 공간이 그대로 보임"),
        M(f"{DLG} fieldset:has(> legend:has-text('목공 항목'))", "목공 항목", "천장 몰딩 · 걸레받이 · 방문 교체 · 천장 평탄화 (하나 이상)"),
    ], check=("목공 항목", ["항목마다 무엇인지 한 줄 설명을 붙임"])),

    S("SC-02-010", "견적 받기 · 공간별 사진", "메인 > 견적 받기 > 10 공간별 사진 (선택)", "FFW-03", "/", group="견적 받기", dialog=True,
      prep=wizard("photos"), expand=True, vh=1060, marks=[
        M(f"{DLG} .mj-pick", "공간 고르기", "고른 공정에 들어간 공간만 · 공간마다 올린 장수"),
        M(f"{DLG} .mj-drop >> nth=0", "공간 사진", "여러 장 · 공간마다 10장 · 한 장 10MB까지", "JPG · PNG · WEBP · HEIC"),
        M(f"{DLG} .mj-wiz-foot >> role=button[name='건너뛰기']", "건너뛰기", "사진 없이 다음 질문(도면)으로"),
    ], check=("사진은 저장 전에 정리", ["올릴 때 위치(GPS) · EXIF를 지우고 HEIC는 JPEG로 바꿈", "파일 형식은 이름이 아니라 파일 앞부분으로 확인", "이 쪽은 창 안쪽 스크롤을 펼쳐서 찍음"])),

    S("SC-02-011", "견적 받기 · 도면", "메인 > 견적 받기 > 11 도면 (선택)", "FFW-03", "/", group="견적 받기", dialog=True,
      prep=wizard("plan"), expand=True, vh=1060, marks=[
        M(f"{DLG} .mj-drop", "아파트 도면", "사진이나 PDF · 5개 · 하나 20MB까지"),
        M(f"{DLG} .mj-wiz-foot >> role=button[name='건너뛰기']", "건너뛰기", "도면 없이 확인으로"),
    ], check=("공간 사진과 따로 받음", ["공간을 바꿀 때마다 도면 칸이 다시 보이지 않게 질문을 나눔"])),

    S("SC-02-012", "견적 받기 · 확인", "메인 > 견적 받기 > 12 확인", "FFW-03, FFW-04", "/", group="견적 받기", dialog=True,
      prep=wizard("review"), marks=[
        M(f"{DLG} dl.mj-kv", "답 요약", "지역 · 집 · 평수 · 시기 · 집 상태 · 예산 · 공정 · 사진 · 도면"),
        M(f"{DLG} dl.mj-kv >> role=button[name*='고치기'] >> nth=0", "고치기", "그 질문으로 돌아가 고친 뒤 다시 확인"),
        M(f"{DLG} .mj-wiz-foot >> role=button[name='프로젝트 만들기']", "프로젝트 만들기", "로그인 확인 → 사진 · 도면 올리기 → 프로젝트 저장 → 진행 현황", "로그인 안 했으면 로그인 뒤 이 화면으로 돌아옴"),
    ], check=("실패해도 답은 남음", ["올리다 실패하면 답과 사진이 그대로 남음", "다시 누르면 이미 올린 사진은 다시 올리지 않음"])),

    # ───────────── 프로젝트 (고객)
    S("SC-03-001", "내 프로젝트", "메인 > 마이페이지 > 내 프로젝트", "FFW-18", "/my", role="customer", group="프로젝트", marks=[
        M(".mj-mynav", "마이페이지 탭", "내 프로젝트 · 내 정보 · 설정"),
                M(".mj-pcard >> nth=0 >> .mj-pcard-lines", "공정별 상태 한 줄", "내 차례 · 업체 차례 · 일정 확정 중 하나와 할 일 한 문장"),
        M(".mj-pcard >> nth=0 >> .mj-btn-pri", "할 일 버튼", "지금 해야 할 일 하나로 바로 이동"),
        M(".mj-pcard >> nth=0 >> role=link[name='프로젝트 보기']", "프로젝트 보기", "진행 현황으로 이동"),
        M(btn("새 견적 받기"), "새 견적 받기", "견적 받기 창을 엶"),
    ], check=("내 프로젝트", ["진행 중인 프로젝트를 위에, 끝난 프로젝트는 '지난 프로젝트'로 접어 둠"])),

    S("SC-03-002", "프로젝트 진행 현황", "내 프로젝트 > 프로젝트 보기", "FFW-18", "/projects/{pid}", role="customer", group="프로젝트", marks=[
        PNAV,
        M(panel("지금 단계"), "지금 단계", "지금 상태와 다음에 할 일 · 버튼 하나"),
        M(sec("올린 사진"), "올린 사진 · 도면", "공간별 장수 · 본인 · 관리자만 봄"),
        M(sec("기본정보"), "기본정보", "견적 받기에서 답한 내용"),
    ], check=("실제 프로젝트", ["저장된 답 · 사진을 API에서 읽어 보여 줌", "예상 공정표 · 표준견적서 등 1~6단계는 아직 연결 전이라 흐리게 표시"])),

    S("SC-03-003", "진행 현황 (예시)", "내 프로젝트 > 예시 프로젝트 보기", "FFW-18 ~ FFW-21", "/projects/p1", role="customer", group="프로젝트", marks=[
        M(panel("지금 단계"), "지금 단계", "상태 설명 · 다음 할 일 버튼"),
        M(sec("공정별 진행"), "공정별 진행", "공정마다 가견적 · 실측 · 실측 견적 · 확정 업체 · 공사기간"),
    ], check=("예시 데이터", ["업체 · 견적 · 공정표 API를 만들기 전이라 예시 데이터로 그린 화면 (3~6단계 공통)"])),

    S("SC-03-004", "예상 공정표", "프로젝트 > 1 예상 공정표", "FAG-01", "/projects/p1/plan", role="customer", group="프로젝트", top=h1("예상 공정표"), h=960, marks=[
        M(btn("그림 파일로 저장"), "그림 파일로 저장", "공정표를 PNG로 저장"),
        M("main table >> nth=0", "작업별 예상 일정", "위 줄 월 · 아래 줄 일 · 하루 한 칸", "휴무일(일요일 · 공휴일)은 회색 칸 · 목공 → 도배 순서"),
    ], check=("에이전트 FAG-01", ["날짜 · 기간은 계산 엔진이, 순서 설명 · 참고사항은 에이전트가 만듦", "LLM이 실패하면 계산 결과만 보여 주고 '설명을 만들지 못했어요'라고 알림", "에이전트가 쓴 글에는 AI 안내 문구를 붙임"])),

    S("SC-03-004", "예상 공정표 · 이유와 할 일", "프로젝트 > 1 예상 공정표 > 아래", "FAG-01", "/projects/p1/plan", role="customer", group="프로젝트", part=2, top=sec("이렇게 잡은 이유"), h=900, marks=[
        M(sec("이렇게 잡은 이유"), "이렇게 잡은 이유", "작업마다 기간 근거 (품 ÷ 인원 × 짐 있는 집)"),
        M(sec("참고사항"), "참고사항 · 할 일", "날짜별 고객 · 업체 할 일 (벽지 고르기, 관리사무소 신고 등)"),
    ], check=("예상 공정표", ["실제 일정은 업체 확정 뒤 확정 공정표로 따로 보여 줌"])),

    S("SC-03-005", "표준견적서", "프로젝트 > 2 표준견적서", "FFW-05, FBF-04", "/projects/p1/standard", role="customer", group="프로젝트", top=h1("표준견적서"), h=960, marks=[
        M(sec("기준 금액 요약"), "기준 금액 요약", "도배 · 목공 · 합계 (부가세 · 일부 자재 제외)"),
        M("main table >> nth=0", "도배 산출 내역", "항목 · 수량 · 공공 단가 · 금액", "공공 가격이 없는 줄은 '공공 가격 없음'"),
    ], check=("업체 견적이 아님", ["공공 기준 단가로 믿집이 계산한 참고 금액", "견적을 만든 때의 단가 버전을 고정해 둠"])),

    S("SC-03-005", "표준견적서 · 출처", "프로젝트 > 2 표준견적서 > 아래", "FFW-05, FBF-04", "/projects/p1/standard", role="customer", group="프로젝트", part=2, top="main table >> nth=1", h=900, marks=[
        M("main table >> nth=1", "목공 산출 내역", "몰딩 · 걸레받이 길이 기준"),
        M(sec("데이터 출처"), "데이터 출처와 적용 시점", "공고일 · 적용일 · 수량 산식"),
    ], check=("비교 기준", ["가견적 비교 화면에서 같은 줄끼리 비교하는 기준 열이 됨", "자재비 · 철거 · 짐 이동 · 이윤은 넣지 않고 업체 가견적에서 확인"])),

    S("SC-03-006", "업체 고르기 · 추천", "프로젝트 > 3 업체 고르기", "FFW-06, FFW-07, FAG-02", "/projects/p1/vendors", role="customer", group="프로젝트", top="main .mj-tabs", h=940, marks=[
        M("main .mj-tabs", "공정 탭", "도배 · 목공 · 담은 업체 수"),
        M(sec("추천 3곳"), "추천 3곳", "승인된 업체 중 시공 지역 · 공정 · 일정이 맞는 곳에서 3곳"),
        M(f"{TABPANEL} >> text=믿집이 고른 이유 >> nth=0", "믿집이 고른 이유", "추천 이유 · 살펴볼 점"),
        M("main >> role=button[name*='요청함에 담기'] >> nth=0", "요청함에 담기", "공정별로 여러 곳을 담음"),
        M("aside.mj-aside", "견적 요청함", "공정별 담은 업체 · 표준견적 금액 · 요청 확인으로"),
    ], check=("에이전트 FAG-02", ["거르기는 SQL, 점수는 계산 엔진, LLM은 상위 후보 중 3곳과 이유만", "후보 밖 업체는 버림"])),

    S("SC-03-006", "업체 고르기 · 전체 목록", "프로젝트 > 3 업체 고르기 > 전체 업체", "FFW-06, FFW-08", "/projects/p1/vendors", role="customer", group="프로젝트", part=2, top=sec("전체 업체"), h=900, marks=[
        M(field_of("업체 이름으로 찾기"), "업체 이름으로 찾기", "이름 일부로 거르기"),
        M(field_of("정렬"), "정렬", "후기 많은 순 · 평점 높은 순 · 시공 사례 많은 순"),
        M(f"{TABPANEL} label.mj-choice:has-text('마포구')", "조건 거르기", "우리 동네 시공 · 토요일 작업 · 실내건축공사업 등록"),
        M(f"{sec('전체 업체')} >> li.mj-vendor >> nth=0", "업체 카드", "믿집 확인 · 업체가 적은 정보 · 믿집 기록을 나눠 보여 줌"),
    ], check=("정보 출처를 나눔", ["믿집이 확인한 것과 업체가 적은 것을 섞지 않음", "전화번호는 보여 주지 않음"])),

    S("SC-03-007", "업체 상세", "업체 고르기 > 업체 정보 보기", "FFW-09", "/vendors/v1", role="customer", group="프로젝트", h=980, marks=[
        M(sec("시공 사례"), "시공 사례", "업체가 올린 사진과 설명 (맨 위)"),
        M(sec("업체가 적은 정보"), "업체가 적은 정보", "팀 · 경력 · A/S · 토요일 작업 · 실측비 (믿집이 확인하지 않음)"),
    ], check=("업체 상세", ["승인된 업체만 목록 · 상세 · 추천에 나옴"])),

    S("SC-03-007", "업체 상세 · 기록", "업체 고르기 > 업체 정보 보기 > 아래", "FFW-09", "/vendors/v1", role="customer", group="프로젝트", part=2, prep=lambda page, st, files: page.locator("main details >> nth=0").evaluate("e => e.open = true"), top=sec("업체가 적은 정보"), h=900, marks=[
        M(sec("믿집 기록"), "믿집 기록", "평점 · 후기 · 응답 시간 · 승인일"),
        M("main details >> nth=0", "사업자 정보", "평소에는 접어 둠 · 믿집은 거래 당사자가 아님을 안내"),
    ], check=("평점 · 후기", ["후기 기능을 만들 때 확정 업체의 고객만 쓰게 함 (지금은 예시 값)"])),

    S("SC-03-008", "가견적 요청 확인", "업체 고르기 > 요청함에 담기 > 가견적 요청 확인하기", "FFW-10", "/projects/p1/request", role="customer", group="프로젝트", prep=basket_one, top=".mj-pnav", h=900, marks=[
        M(sec("보내는 조건"), "보내는 조건", "집 · 시기 · 공정 · 사진을 담은 업체 모두에 같은 조건으로 보냄"),
        M(f"{sec('보내는 조건')} >> role=link[name*='고치기']", "고치기", "견적 받기 답을 고침"),
        M("aside.mj-aside", "받는 업체", "공정별로 담은 업체 · 더 고르기"),
        M("aside.mj-aside >> .mj-btn-pri", "가견적 요청", "요청을 보내고 가견적 비교 화면으로"),
    ], check=("같은 조건으로 요청", ["이름 · 연락처 · 동 · 호수는 보내지 않음 (실측 요청한 업체에만 보임)", "업체가 제출하면 가견적서가 바로 프로젝트에 등록됨 (FFV-03)"])),

    S("SC-03-009", "가견적 비교", "프로젝트 > 4 가견적 비교", "FFW-11, FBF-05", "/projects/p1/quotes", role="customer", group="프로젝트", top="main .mj-tabs", h=1000, marks=[
        M("main .mj-tabs", "공정 탭", "도배 · 목공 · 도착한 가견적 수"),
        M(sec("요청 상태"), "요청 상태", "업체마다 요청일 · 도착일 · 상태"),
        M("main table >> nth=0", "표준견적서와 비교", "같은 줄끼리 표준견적서 열과 업체 열을 나란히", "포함 · 묶음 · 별도 · 선택 · 실측 후 · 안 함 표시"),
    ], check=("비교 기준", ["합계에는 '포함'과 '따로 계산'만 들어감 (계산 엔진)", "표준견적서는 공공 단가가 있는 줄만 더해 업체 합계와 바로 같지 않음을 안내"])),

    S("SC-03-009", "가견적 비교 · 실측 요청", "프로젝트 > 4 가견적 비교 > 아래", "FFW-11, FFW-12", "/projects/p1/quotes", role="customer", group="프로젝트", part=2, top=sec("업체가 보낸 가견적서"), h=900, marks=[
        M(sec("업체가 보낸 가견적서"), "업체 가견적서", "포함 상태 6가지의 뜻 · 업체별 전체 가견적서 (부가세 따로)"),
        M(sec("실측 요청"), "실측 요청", "공정마다 한 곳에 실측 요청 (희망일 · 시간대 · 동 · 호수 · 동의)"),
    ], check=("실측 요청", ["실측은 공정마다 한 번에 한 곳", "동 · 호수는 업체가 요청을 확인한 뒤에 보임"])),

    S("SC-03-010", "실측 견적 · 확정 후", "프로젝트 > 5 실측 견적", "FFW-13, FFW-15", "/projects/p1/measure", role="customer", group="프로젝트", top="main .mj-tabs", h=900, marks=[
        M("main .mj-tabs", "공정 탭", "도배 · 목공"),
        M("text=실측 견적 · 부가세 별도", "실측 견적 금액", "업체가 실측 뒤 낸 금액 · 가견적과 차이"),
        M(sec("실측에서 확인한 것"), "실측에서 확인한 것", "업체가 현장에서 본 것"),
        M(sec("바뀐 줄"), "바뀐 줄", "가견적에서 바뀐 줄만 모아 보여 줌"),
        M(sec("업체 확정"), "업체 확정", "확정한 날 · 다음 단계 안내"),
    ], check=("사람이 눌러야 확정", ["업체 확정 · 다시 고르기는 고객이 누른 요청으로만 일어남"])),

    S("SC-03-010", "실측 견적 · 확정 전", "프로젝트 > 5 실측 견적 > 확정 전", "FFW-13, FFW-14, FFW-15", "/projects/p1/measure", role="customer", group="프로젝트", part=2, prep=measure_before, top="main .mj-tabs", h=900, marks=[
        M(sec("업체 확정"), "확정 · 다시 고르기", "이 업체로 확정하거나, 가견적 받은 다른 업체에 실측 요청 · 새 업체에 가견적 요청"),
    ], check=("다시 고르기", ["이전 업체는 '넘김'으로 남고 이력에 기록됨"])),

    S("SC-03-011", "확정 공정표", "프로젝트 > 6 확정 공정표", "FFW-16", "/projects/p1/schedule", role="customer", group="프로젝트", top=h1("확정 공정표"), h=980, marks=[
        M(btn("그림 파일로 저장"), "그림 파일로 저장", "PNG 저장"),
        M("main table >> nth=0", "공정별 확정 업체 · 공사기간", "공정 · 업체 · 시작일 · 종료 예정일 · 일하는 날"),
        M("main table >> nth=1", "작업별 확정 일정", "월 · 일 머리줄 · 하루 한 칸", "휴무일은 회색 칸"),
    ], check=("확정 공정표", ["확정 업체가 등록한 공사기간으로 계산 엔진이 일정을 만듦", "업체가 공사기간을 고치면 바로 반영"])),

    S("SC-03-011", "확정 공정표 · 비교와 할 일", "프로젝트 > 6 확정 공정표 > 아래", "FFW-16", "/projects/p1/schedule", role="customer", group="프로젝트", part=2, top=sec("예상 공정표와 비교"), h=700, marks=[
        M(sec("예상 공정표와 비교"), "예상 공정표와 비교", "예상 기간 → 확정 기간"),
        M(sec("공사 전에 할 일"), "공사 전에 할 일", "관리사무소 신고 · 엘리베이터 예약 등"),
    ], check=("공사기간 변경", ["공사기간은 확정 업체가 고객과 합의해 등록 · 수정"])),

    S("SC-03-012", "이력", "프로젝트 > 이력", "FFW-22", "/projects/p1/history", role="customer", group="프로젝트", h=900, marks=[
        M("main .mj-tabs", "공정으로 거르기", "전체 · 도배 · 목공"),
        M("main ol >> nth=0", "날짜별 기록", "요청 · 도착 · 실측 · 확정 · 공사기간 등록"),
    ], check=("이력", ["상태가 바뀔 때마다 같은 트랜잭션에 기록을 남김"])),

    S("SC-03-013", "내 정보 · 설정", "메인 > 마이페이지 > 내 정보 · 설정", "FFW-17", "/account", role="customer", group="프로젝트", marks=[
        M(field_of("이름"), "이름", "고칠 수 있음"),
        M(btn("저장"), "저장", "바꾼 이름을 저장"),
        M(sec("회원 탈퇴"), "회원 탈퇴", "탈퇴 화면으로 이동"),
    ], check=("내 정보", ["이메일은 로그인 아이디라 바꾸지 않음", "업체 회원도 같은 화면을 씀"])),

    S("SC-03-014", "회원 탈퇴", "내 정보 · 설정 > 회원 탈퇴", "FFW-17", "/account/withdraw", role="customer", group="프로젝트", marks=[
        M(field_of("지금 비밀번호"), "비밀번호 확인", "본인 확인 (틀리면 탈퇴 안 됨)"),
        M(btn("탈퇴하고 모두 지우기"), "탈퇴", "DB 기록과 디스크 파일을 지우고 홈으로 ('탈퇴했어요' 안내)"),
    ], check=("회원 탈퇴", ["회원 정보 · 프로젝트 · 사진 · 도면 · 로그인 기록을 바로 지움 (되살릴 수 없음)", "진행 중인 프로젝트가 있어도 탈퇴 가능", "관리자 계정은 탈퇴 화면으로 지울 수 없음"])),

    # ───────────── 업체
    S("SC-04-001", "업체 회원가입", "로그인 > 회원가입 > 업체로 가입하기", "FFV-01", "/signup/vendor", group="업체", h=1140, marks=[
        M(field_of("담당자 이름"), "담당자 이름", "업체 담당자"),
        M(field_of("이메일"), "이메일", "로그인 아이디"),
        M(field_of("비밀번호") + " >> nth=0", "비밀번호", "칸 아래 안내: 영문, 숫자, 8자 이상"),
        M(field_of("사업자등록증"), "사업자등록증", "끌어다 놓거나 눌러서 고름 (도면 칸과 같은 영역)", "JPG · PNG · PDF · 관리자와 그 업체만 봄"),
        M(sec("약관 동의"), "약관 동의", "이용약관 · 개인정보 (필수)"),
        M(btn("가입 신청하기"), "가입 신청하기", "가입 → 업체 홈 '승인 대기'로 이동"),
    ], check=("사업자등록증만 받음", ["상호 · 시공 지역 등 업체 정보는 승인 뒤 업체 정보 관리(FFV-08)에서 받음"])),

    S("SC-04-002", "업체 홈 · 승인 대기", "업체 가입 > 업체 홈", "FBF-01", "/vendor", role="pending", group="업체", h=620, marks=[
        M("main h1 >> xpath=following-sibling::*[1]", "승인 상태", "승인 대기 · 승인 · 반려 중 지금 상태를 보여 줌"),
    ], check=("승인 상태", ["승인 대기 · 승인 · 반려 중 하나를 보여 줌", "승인 전에는 견적 요청을 받지 않음"])),

    S("SC-04-002", "업체 홈 · 반려", "업체 홈 (반려됨)", "FBF-01", "/vendor", role="rejected", group="업체", part=2, h=620, marks=[
        M("text=사유 ·", "반려 사유", "관리자가 적은 사유를 그대로 보여 줌"),
        M("main >> role=link[name='탈퇴하기']", "탈퇴하기", "탈퇴한 뒤 새 사업자등록증으로 다시 가입"),
    ], check=("반려", ["반려는 사유가 꼭 있어야 함 (빈 사유는 서버가 거절)"])),

    S("SC-04-002", "업체 홈 · 승인", "업체 홈 (승인됨)", "FBF-01, FBF-02", "/vendor", role="approved", group="업체", part=3, h=620, marks=[
        M("main h1 >> xpath=following-sibling::*[1]", "승인 상태", "승인되면 업체 기능이 열림"),
    ], check=("다음에 열리는 화면", ["견적 요청함 · 가견적서 쓰기 · 실측 요청 · 실측 견적서 · 공사기간 등록 · 업체 정보 관리 (FFV-02 ~ 08)"])),

    # ───────────── 관리자
    S("SC-05-001", "회원관리", "관리자 > 회원관리", "FAD-01", "/admin/members", role="admin", group="관리자", marks=[
        M(field_of("이름 · 이메일로 찾기"), "찾기", "이름 · 이메일 일부로 거르기"),
        M(field_of("계정 상태"), "계정 상태", "전체 · 사용 중 · 정지"),
        M("main table", "회원 목록", "이름 · 이메일 · 가입일 · 프로젝트 수 · 상태"),
        M("main table >> role=button >> nth=0", "계정 정지", "정지 · 정지 풀기"),
    ], check=("예시 데이터", ["회원 목록 API를 만들기 전이라 예시 데이터로 그린 화면"])),

    S("SC-05-002", "업체관리", "관리자 > 업체관리", "FAD-03", "/admin/vendors", role="admin", group="관리자", h=640, marks=[
        M("main .mj-mynav", "상태 탭", "승인 대기 · 승인 · 반려 · 전체"),
        M("main table", "업체 가입 신청 목록", "담당자 · 이메일 · 신청일 · 상태"),
        M("main table >> a:has-text('보기')", "사업자등록증", "새 창에서 보기"),
        M("main table >> .mj-btn-row", "처리", "승인 · 반려 (반려는 사유 필수)"),
    ], check=("업체 승인", ["승인한 업체만 업체 기능을 쓰고 목록 · 추천에 나옴", "두 관리자가 동시에 처리하면 한 명만 성공 (409)"])),

    S("SC-05-003", "업체 신청 상세", "업체관리 > 업체 이름", "FAD-02", "/admin/vendors/{vid}", role="admin", group="관리자", h=900, marks=[
        M("main dl", "신청 정보", "담당자 · 이메일 · 신청일 · 상태"),
        M(sec("사업자등록증"), "사업자등록증", "미리보기 · 새 창에서 보기 (관리자와 그 업체만)"),
        M(sec("처리"), "처리", "승인 · 반려"),
    ], check=("확인할 것", ["상호 · 대표자 · 사업자등록번호 · 개업일"])),

    S("SC-05-003", "업체 신청 상세 · 반려 사유", "업체관리 > 업체 이름 > 반려", "FAD-02", "/admin/vendors/{vid}", role="admin", group="관리자", part=2, prep=reject_open, top=sec("사업자등록증"), h=700, marks=[
        M(f"{sec('처리')} >> .mj-field", "반려 사유", "300자까지 · 업체 홈에 그대로 보임"),
        M(btn("반려하기"), "반려하기", "사유가 비면 '반려 사유를 적어 주세요'"),
        M(btn("그만두기"), "그만두기", "사유 칸을 닫음"),
    ], check=("반려", ["빈 반려 사유는 DB 제약으로도 막음"])),
]
