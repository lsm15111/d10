# 화면 디자인 요소 보강안

기준일 2026-10-29 · 상태: 제안 (6장 결정 전)

## 1. 결론

- **정돈은 돼 있지만, 무엇을 받는 서비스인지 그림으로 안 보인다.**
  - 홈 첫 화면은 제목 · 한 줄 · 버튼 두 개뿐이다. 그 아래는 비어 있다.
  - 파비콘과 바닥글이 없다. 업체 시공 사례는 회색 '사진' 칸이다.
- **새 색 · 새 글꼴 없이 더한다.** 토큰(A 정돈형 + 파스텔 블루)과 Noto Sans KR은 그대로 둔다. 더할 것은 여섯 가지다.
  1. 표시(로고 마크)와 파비콘
  2. 사진 대신 우리 결과물(표준견적서)을 그림으로 쓰는 홈 첫 화면
  3. 번호 붙은 단계 띠와 '지금' 표시
  4. 도배 유형 견본 카드
  5. 시공 전 · 완공 비교
  6. 바닥글
- **레퍼런스의 큰 사진과 움직임은 가져오지 않는다.** 우리 고객은 집주인이고, 할 일은 견적 비교다. 본 사이트 대부분이 첫 화면 전에 1~3초 로딩 화면을 띄운다.
- **예시는 `/samples/design`에 있다.** 기존 화면과 공용 파일은 바꾸지 않았다. 새로 둔 것은 `frontend/app/icon.svg`(파비콘)와 `frontend/app/samples/design/` 아래 7개 파일뿐이다.
- 먼저 할 것은 셋이다: 파비콘 · 헤더 표시, 바닥글, 홈 첫 화면. 셋 다 공용 파일 한두 개만 고치면 된다.

### 예시 화면 (`/samples/design`)

| 묶음 | 보여 주는 것 | 파일 |
| --- | --- | --- |
| 01 헤더 · 파비콘 · 아이콘 · 바닥글 | 표시 + 글자 + 한 줄 설명 헤더, 브라우저 탭 제목, 파비콘 16~64px, 기능 아이콘 8개, 4칸 바닥글 | `page.tsx`, `marks.tsx` |
| 02 홈 첫 화면 | 큰 제목 + 표준견적서 미리보기(예시 프로젝트 p1 값), 01~04 단계 띠, 기준 출처 띠 | `page.tsx` |
| 03 견적 받기 창 | 묶음 4개 진행 표시(이전 · 다음으로 움직여 봄), '시작 전에 알아 두세요', 도배 유형 견본 카드 + 펼침 설명 | `ProgressDemo.tsx`, `GradeCards.tsx`, `art.tsx` |
| 04 업체 시공 사례 | 왼쪽 고정 사양표 + 오른쪽 전후 비교(끌기 · 화살표 · 버튼), 꼭 넣을 사진 3칸 | `BeforeAfter.tsx`, `art.tsx` |
| 05 내 프로젝트 · 진행 현황 | 6단계 띠 + 공정별 차례 + 버튼 하나, 빈 상태 | `page.tsx` |

- 스타일은 `samples.module.css` 한 파일이다. 색은 `globals.css` 토큰만 쓴다.
- 이 파일에서 새로 정한 값은 색이 아닌 변수 5개다: `--sd-fs-hero`(홈 제목 32~52px), `--sd-track`(큰 제목 자간 -0.02em), `--sd-gap`(묶음 간격), `--sd-dur`(180ms), `--sd-ease`. 쓰기로 하면 앞의 둘은 `globals.css`로 옮긴다(6장 6).
- 움직임은 막대 채우기 · 카드 테두리 · 손잡이 크기 변화 세 가지뿐이다. `prefers-reduced-motion`이면 `globals.css`가 모두 끈다.
- 사진 자리는 모두 그림이고, 그림마다 '그림 · 실제 사진 필요'를 붙였다.

## 2. 지금 디자인 진단

| 항목 | 파일 | 지금 | 문제 |
| --- | --- | --- | --- |
| 헤더 | `frontend/components/site/SiteHeader.tsx`, `globals.css` `.mj-logo` | 글자 '믿집'(22/24px) + 메뉴 '내 프로젝트' + 로그인 · 견적 받기 | 표시(마크)가 없다. 무슨 서비스인지 말해 주는 곳이 없다. 360px에서는 두 줄로 접혀(둘째 줄에 로그인 · 회원가입과 견적 받기) 헤더가 약 120px이 된다 |
| 파비콘 · 앱 아이콘 | `frontend/app/`, `frontend/public/` | 없었다. `/favicon.ico`가 404였다 | 탭을 여러 개 열면 구분이 안 된다. `apple-icon`, `manifest`도 없다. 이번에 `app/icon.svg`를 더했다(Next가 `<link rel="icon">`을 저절로 넣는다) |
| 쪽 제목 | 각 `page.tsx`의 `metadata`, `app/layout.tsx` | 템플릿 `%s · 믿집`, 쪽마다 제목이 있다 | 잘 돼 있다. 다만 홈은 '믿집' 한 단어다. 업체 상세 제목에 데모 업체의 '예시'가 없다(AGENTS.md 5장). 설명(description)은 하나뿐이고 공유 그림(OG)이 없어서 링크를 보내면 미리보기 그림이 빈다 |
| 기능 아이콘 | `components/site/AccountMenu.tsx`, `components/start/PhotoDrop.tsx` | 계정(사람), 사진 넣기, 닫기 정도 | 프로젝트 단계(`ProjectNav.tsx`)는 숫자 동그라미만 있다. 단계 구분이 글자에만 기댄다 |
| 글자 | `globals.css` `--fs-*` | KRDS 단계(13 · 15 · 17 · 19 · 22/24 · 24/32 · 28~40), 큰 제목 자간 -0.01em, 숫자 `.mj-num` | 단계는 잘 정리돼 있다. 홈 제목이 최대 40px라 다른 쪽 제목(32px)과 차이가 작아 첫인상이 약하다 |
| 색 | `globals.css` 토큰 22개 | 대비 계산이 주석에 있다 | 좋다. 다만 `components/project/GanttDownload.tsx` 캔버스에 색 값 8곳, `components/ui/AreaDiagram.tsx`에 `#fff` 2곳이 있다. 캔버스는 `getComputedStyle`로 토큰을 읽으면 된다 |
| 간격 | `app/`, `components/` | 인라인 `style={{ }}` 약 190곳. 간격 토큰이 없다 | 같은 묶음 간격이 쪽마다 10 · 12 · 14 · 18 · 20px로 다르다 |
| 빈 상태 | `app/my/page.tsx`, `app/vendors/[id]/page.tsx`, `components/project/RealProjectHub.tsx` | '아직 만든 프로젝트가 없어요.' 한 줄, 회색 '사진' 칸, '아직 연결 전이에요' | 다음에 할 일을 말해 주지 않거나 버튼 하나뿐이다 |
| 바닥글 | 없음 | — | 사업자 정보, 이용약관, 개인정보 처리방침, '거래 당사자가 아니에요' 고지를 둘 곳이 없다. `mypage-vendor-info.md` 5.6은 이 고지를 화면 아래에 두기로 했다 |
| 없는 쪽 · 오류 | `app/not-found.tsx`, `app/error.tsx` 없음 | Next 기본 화면(영어) | 화면 말 규칙(AGENTS.md 8장)과 어긋난다 |

## 3. 레퍼런스에서 가져올 것

2026-10-29에 직접 열어 봤다. awwwards는 Architecture · Real Estate 분류와 'renovation' 검색에서 골랐다. 인테리어 분류 주소(`/websites/interior-design/`)는 없어서 후보 목록으로 넘어간다.

| 사이트 | 본 것 | 가져올 것 | 믿집 어디에 |
| --- | --- | --- | --- |
| 3.3디자인스페이스 문의 (`/inquiry`) | 한 쪽짜리 긴 문의서. 질문은 22px 굵은 문장, 보기는 45px 칸. '도배 공사'를 고르면 실크 · 합지를 설명하는 '알아보기'가 펼쳐진다. 답에 따라 문장이 채워지는 '나의 공사범위' 요약. 3,000만 원 미만 공사는 받지 않는다고 미리 적었다 | 질문을 문장으로 쓰기(이미 한다), 자재 '알아보기' 펼침, 받지 않는 조건을 먼저 알리기 | 견적 받기 창 도배 유형 질문, 시작 전 안내 |
| 3.3디자인스페이스 홈 · 사례 | 2열 사례 카드: 사진 + 제목 + '단지명 아파트 32평 인테리어'. 사례 상세 맨 위: 번호, 완공일, 공사기간 48일, 공사 범위 '방 3 \| 욕실 2', 공간별 바로가기. 오른쪽 아래 '견적 요청하기' 떠 있는 버튼 | 사례 상세 맨 위 사실 한 줄(끝난 달 · 기간 · 공간), 공간 바로가기 | 업체 시공 사례 |
| INSHOW (`interiorshow.kr`) | 첫 화면은 전면 사진 + 글자 로고 + 버튼 2개(PORTFOLIO · CONSULTANT)뿐. 사례 목록은 번호(12, 11 …)와 '대장동 62PY', 벽 · 바닥 자재 이름과 규격 두 줄. 사례 상세는 왼쪽 '항목 : 자재' 사양표, 오른쪽 사진 3열. 상담 신청 전 안내: 답까지 2주 이상, 디자인비 평당 10만 원 VAT 별도, 관리실에서 받은 건축 도면을 달라 | 사양표 + 사진 배치, 신청 전 안내(걸리는 시간 · 비용 · 준비물) | 업체 시공 사례, 견적 받기 첫 질문 위 |
| [Loam House](https://residences.loamhouse.com.au/) (awwwards Honorable Mention, 분양) | '01 / THE PROPOSITION' 식 번호 묶음과 위쪽 묶음 메뉴. 큰 숫자 + 단위('88 RESIDENCES', '86–275 SQUARE METRES'). 그림마다 'ARTIST'S IMPRESSION' 표시. 3단계 문의(YOU · REACH YOU · ENQUIRY)와 연락처 안심 문구, 전화 대안. `prefers-reduced-motion` 규칙이 있다 | 번호 묶음, 숫자 + 단위를 크게, 그림에 '그림'이라고 적기, 연락처 안심 문구 | 홈, 표준견적서, 사진 자리 표시, 견적 받기 시작 전 안내 |
| [Storey Architecture](https://www.storeyarchitecture.co.uk/) (awwwards HM) | 'SPATIAL BRIEF INTAKE' 문의서. 종이 질감 위에 01) ~ 06) 번호 질문. 전면 사진 위 흰 글자. 첫 화면 전 검은 로딩 화면 | 질문 번호 | 견적 받기 확인 단계('이대로 프로젝트를 만들까요?')를 번호 붙은 요청서처럼 |
| [Woonpact](https://woonpact.gent/) (awwwards HM, 임대주택 정책) | 01 ~ '05 / 05' 일정 띠, '지금 단계' 표시, 사진 대신 단순 그림 | 단계 띠 + '지금' 표시 | 내 프로젝트 카드, 진행 현황 |
| [Halcyon Lighting](https://www.halcyon.co.nz/) (awwwards HM, 조명) | 제품 카드: 품번(M80-T1) + 이름 + 사양 칸(LUMENS 730LM · WATTS 9W …), '+3' 마감 색 | 견본 카드의 '이름 + 사양 2열' | 도배 유형 카드, 나중에 목공 항목(몰딩 형태 · 높이) |
| [NYC Renovation](https://nycrenovation.com/) (awwwards Nominee, 리모델링) | Step 01~04 공정. 바닥글에 면허 번호 두 개. 경력 숫자가 서로 다르다(37년 · 20년 이상 · since 2008 · since 1987) | 면허 · 사업자 정보를 바닥글에 | 바닥글. 숫자는 반면교사 |
| [RS.D Agencements](https://www.rsd-agencements.com/) (awwwards HM, 아파트 리노베이션) | 묶음 번호가 01 · 03 · 04 · 05 · 05 · 07로 건너뛰고 겹친다. 실적 숫자 4칸이 '0'으로 보인다(움직이는 숫자가 안 돈 경우). 폰 화면 아래 '전화 · 무료 견적' 고정 바. '48시간 안에 견적' 약속 | 폰 아래 고정 바, 답이 오기까지 걸리는 시간 알리기 | 업체 상세 폰 화면(이미 제안됨), 가견적 요청 확인 |
| [Rogers-O'Brien](https://r-o.com/) (awwwards Nominee, 시공사) | 실적 4칸, 지역 사무소, 바닥글에 'Accessibility Statement' 링크 | 바닥글에 접근성 안내 링크 | 바닥글 |

- 본 것 중 가져올 것이 없던 곳: BAM Rénovation(채용 위주), AllHaus(지역 고르기 화면뿐).
- `interiorshow.kr`은 박람회 사이트가 아니라 INSHOW라는 인테리어 회사 사이트였다.

## 4. 화면별 적용안

### 4.1 헤더 (`#chrome`)

- 표시 + '믿집' + 한 줄 설명 '도배 · 목공 견적 비교'. 640px 미만에서는 한 줄 설명을 숨긴다.
- 메뉴는 '내 프로젝트' 하나 그대로 둔다. 메뉴가 하나라 햄버거 버튼으로 숨기지 않는다.
- 360px: '로그인 · 회원가입' 버튼을 글자 링크 '로그인'으로 줄여 한 줄에 둔다(6장 3).
- 고칠 파일: `components/site/SiteHeader.tsx`, `globals.css` `.mj-logo`.

### 4.2 파비콘 · 쪽 제목 · 기능 아이콘

- 파비콘: `app/icon.svg`를 더했다. 지붕 + 'ㅁ' 칸 모양이고 `--accent`와 같은 파랑이다. 파비콘은 CSS 변수를 못 읽어 값을 직접 쓴다.
- 쪽마다 파비콘을 바꾸지 않는다. 쪽 구분은 지금처럼 제목 '화면 이름 · 믿집'으로 한다.
- 홈 제목은 '믿집 · 아파트 도배 · 목공 견적 비교'처럼 설명을 붙인다. 업체 상세 제목에는 '(예시)'를 붙인다.
- 다음에 둘 것: `app/apple-icon.png`(180px), `app/manifest.ts`(이름 · 색), `app/opengraph-image.tsx`(표시 + 한 줄, 사진 없이). 표시를 정한 뒤 만든다(6장 12).
- 기능 아이콘 8개: 진행 현황 · 예상 공정표 · 표준견적서 · 업체 고르기 · 가견적 비교 · 실측 견적 · 확정 공정표 · 이력.
  - 24px 격자, 선 1.8px, 둥근 끝. 계정 아이콘과 같은 굵기다.
  - `ProjectNav` 단계와 진행 현황 줄 앞에만 쓴다. 버튼마다 붙이지 않는다. 색은 글자색을 따른다.

### 4.3 바닥글 (`#chrome`)

- 새 파일 `components/site/SiteFooter.tsx`를 고객 화면 아래에 둔다.
- 4칸: 한 줄 소개 / 서비스(견적 받기 · 내 프로젝트 · 기준 단가 출처) / 약관 · 정책(이용약관 · 개인정보 처리방침 · 문의) / 사업자 정보.
- 개인정보 처리방침은 굵게 해서 다른 링크와 구분한다.
- 맨 아래 한 줄: '믿집은 거래 당사자가 아니에요. 계약과 대금은 업체와 직접 해요.' (`mypage-vendor-info.md` 7장 6과 함께 정한다)
- 사업자 정보 칸은 값이 정해질 때까지 비워 둔다. 지어낸 번호를 넣지 않는다.

### 4.4 홈 (`#home`)

- 첫 화면 오른쪽에 **표준견적서 미리보기**를 둔다. 고지서형 표(B 시안)를 그대로 쓴다.
  - 금액은 예시 프로젝트 표준견적서 값(`getStandardQuote`)을 `won()`으로 형식만 바꾼다. 화면에서 계산하지 않는다.
  - '참고 금액이에요. 업체 견적이 아니에요.'와 빠진 항목 수를 함께 적는다.
  - 사진을 쓰지 않으니 촬영 허락이나 지어낸 집 문제가 없다.
- 제목은 32~52px, 자간 -0.02em으로 한 단계 키운다.
- 아래에 01~04 단계 띠: 집 정보 고르기 → 기준부터 보기 → 가견적 비교하기 → 실측하고 확정하기. 프로젝트 안 1~6 단계와 섞이지 않게 홈에서는 두 자리 번호로 쓴다.
- 기준 출처 띠: 표준시장단가 · 시중노임단가 · 조달청 가격 · 표준품셈. AGENTS.md 6장 '화면에 기준을 적는다'와 맞다.
- '업체 n곳 · 견적 n건' 같은 실적 숫자는 실제 기록이 쌓이기 전에는 두지 않는다.

### 4.5 견적 받기 창 (`#quote`)

- **진행 표시:** '1 / 9' 막대 하나를 묶음 4개로 바꾼다.
  - 묶음: 집 정보 · 일정 · 예산 · 공정 · 사진 · 확인. 위에 '일정 · 예산 · 묶음 2 / 4'와 '질문 5 / 10'.
  - 지금 묶음의 칸만 채운다. 도배 · 목공을 더해 질문이 늘어도 막대가 뒤로 가지 않는다.
  - 화면 읽기: 묶음 목록에 `aria-current="step"`, 질문 수는 `aria-live`. 질문이 바뀌면 제목으로 초점을 옮긴다(지금과 같다).
- **시작 전에 알아 두세요(3줄):** 질문 9~11개 · 저절로 저장 / 평형 · 사진이 있으면 좋지만 없어도 됨 / 업체에는 구까지만 보이고 동 · 호수와 연락처는 실측 확정과 동의 뒤에만(AGENTS.md 5장).
  - 넣을 곳은 첫 질문 위나 `/start` 쪽 옆 칸이다(6장 7).
- **도배 유형:** 글자 라디오 두 개를 견본 카드 두 장으로 바꾼다.
  - 카드: 견본 그림 + 이름 + 한 줄 + 사양 2열(벽지 · 이음 · 물걸레 · 표준견적서). 카드 전체가 라디오이고, 이름은 제목만 읽힌다.
  - 아래에 '실크와 합지는 무엇이 다른가요?' 펼침.
  - 어떤 유형에 어떤 벽지가 들어가는지는 아직 정하지 않았다. 정하기 전에는 '예시 구성' 배지를 달고 단가는 '정한 뒤 보여요'로 둔다.
- 고칠 파일: `components/start/Wizard.tsx`(`mj-wiz-head`와 도배 단계), `globals.css` `.mj-progress`.

### 4.6 내 프로젝트 · 진행 현황 (`#project`)

- 카드 한 장: 이름 + 지역 · 만든 날 / 6단계 띠 / 공정별 줄 / 주 버튼 하나.
  - 단계 띠: 끝난 단계는 ✓ 채운 동그라미, 지금 단계는 테두리 + '지금' 배지, 남은 단계는 아이콘만.
  - 공정별 줄: '내 차례'는 강조색 배지, '업체 차례'는 테두리 배지, '새로 왔어요'는 warn 배지. 강조색은 '내 차례'에만 쓴다(`mypage-vendor-info.md` 5.3).
- 폰(640px 미만): 단계 이름은 지금 단계만 보이고 나머지는 화면 읽기용으로만 남긴다.
- 공정 상태 · 차례 · 다음 할 일은 API가 정해서 준다. 화면이 계산하지 않는다.
- 빈 상태: 선 그림 + '아직 만든 프로젝트가 없어요' + 할 일 3줄 + 버튼.
- 고칠 파일: `app/my/page.tsx`, `app/projects/[id]/page.tsx` '지금 단계' 판.

### 4.7 업체 고르기 · 업체 상세 시공 사례 (`#case`)

- 업체 상세 포트폴리오: 회색 '사진' 칸을 사례 카드(대표 사진 + '구 · 평수대 · 공정' 제목 + 사실 한 줄)로 바꾼다.
- 사례 상세: 왼쪽 고정 사양표, 오른쪽 전후 비교와 꼭 넣을 사진 3칸(완공 전경 · 이음매 근접 · 천장 경계선).
  - 사양표 항목은 `vendor-portfolio.md` 3장 그대로다: 벽지 종류, 천장, 기존 벽지, 초배, 끝선 마감, 자재.
  - '자재'처럼 업체가 적은 값에는 '믿집이 확인하지 않은 정보예요'를 붙인다.
- 전후 비교: 그림 전체에 범위 입력을 겹쳐 끌기 · 화살표 키 · 버튼 3개(시공 전 · 반씩 · 완공)가 모두 된다. '시공 전 · 완공' 표시를 늘 붙인다.
- 배지: '믿집에서 진행한 공사'는 믿집 기록과 연결될 때만. 아니면 '업체 등록 사례'.
- 업체 고르기 카드(`components/vendors/VendorPicker.tsx`): 사례가 쌓이면 대표 사진 하나를 작게 넣는다. 지금은 넣지 않는다.
- 사진은 업체가 올린 것만 쓴다. 예시의 그림은 실제 사진이 필요하다는 표시다.

## 5. 하지 않을 것

| 하지 않을 것 | 이유 | 본 곳 |
| --- | --- | --- |
| 첫 화면 로딩 화면 · 글자가 서서히 나타나는 효과 | 1~3초 빈 화면이 뜨고, 느린 폰에서는 더 길다 | Storey, Loam House, Halcyon, 3.3디자인스페이스 |
| 스크롤 가로채기 · 큰 패럴랙스 · WebGL | 어디까지 봤는지 놓치고, 멀미가 나고, 배터리를 쓴다 | awwwards 수상작 다수 |
| 전면 사진 위 흰 글자 | 사진에 따라 대비 4.5:1이 깨진다 | INSHOW, Storey |
| 작고 옅은 글자 | INSHOW 사례 설명은 11.4px · #888 회색 글자(흰 바탕이어도 대비 3.5:1로 4.5:1에 못 미친다). 3.3디자인 입력 칸은 회색 밑줄과 옅은 안내 글 | INSHOW, 3.3디자인스페이스 |
| 자간을 크게 좁힌 한글 제목 | 56px에 -4px(-0.07em)는 받침끼리 붙는다. 믿집은 -0.02em까지 | 3.3디자인스페이스 |
| 움직이며 올라가는 숫자 | 스크립트가 안 돌면 0으로 보인다 | RS.D |
| 근거 없는 실적 숫자 · 평점 | AGENTS.md 5장. 서로 안 맞는 숫자는 믿음을 깎는다 | NYC Renovation |
| 세리프 제목 글꼴 추가 | 글꼴 파일이 늘고, 고급 인테리어 느낌은 '기준 · 비교' 도구와 맞지 않는다 | Loam House |
| 렌더 · 스톡 사진 | 지어낸 집처럼 보인다. 꼭 쓰면 '예시 그림'이라고 적는다 | Loam House(ARTIST'S IMPRESSION 표시) |
| 데스크톱에서 메뉴를 햄버거 버튼에 숨기기 | 메뉴가 하나뿐이다 | 3.3디자인스페이스 |
| 종이 질감 · 클립 같은 소품 장식 | 내용보다 눈에 먼저 들어온다 | Storey |
| 단계마다 다른 아이콘 색 | 색은 상태(내 차례 · 새로 왔어요)에만 쓴다 | — |
| 반짝이 · 보라 그라데이션 · 이모지 표시 | AGENTS.md 8장 | — |

## 6. 정할 것

1. **표시(마크):** 지붕 + 'ㅁ' 칸 (권장, `app/icon.svg`) / 글자만 / 따로 디자인.
2. **헤더 한 줄 설명 '도배 · 목공 견적 비교':** 640px 이상에서 보임 (권장) / 넣지 않음.
3. **폰 헤더:** '로그인 · 회원가입'을 글자 링크 '로그인'으로 줄여 한 줄 (권장) / 지금처럼 두 줄.
4. **바닥글:** 고객 화면 전부에 4칸 바닥글 (권장) / 홈에만 / 두지 않음.
5. **홈 첫 화면 그림:** 표준견적서 미리보기 (권장) / 벽 · 도면 그림 / 실제 사진(촬영 허락 필요).
6. **홈 제목 크기:** 32~52px 새 토큰 `--fs-hero`와 `--track-tight: -0.02em`을 `globals.css`에 더함 (권장) / 지금 `--fs-display`(최대 40px).
7. **견적 받기 진행 표시와 시작 전 안내:** 묶음 4개 + 질문 수, 안내는 첫 질문 위 (권장) / 안내는 `/start` 쪽에만 / 지금 막대 하나.
8. **도배 유형 카드:** 견본 그림 카드 + 펼침 설명, 실제 견본 사진이 생기면 교체 (권장) / 지금 글자 라디오. 등급마다 무엇이 들어가는지는 따로 정한다(AGENTS.md 1장).
9. **전후 비교:** 끌기 슬라이더 + 버튼 3개 (권장) / 두 장 나란히(폰에서는 위아래).
10. **기능 아이콘:** 8개 한 세트를 `ProjectNav` · 진행 현황에만 (권장) / 넣지 않음.
11. **간격 토큰:** `--sp-1`~`--sp-7`(4 · 8 · 12 · 16 · 24 · 32 · 48px)을 더하고, 인라인 style은 그 화면을 고칠 때 옮김 (권장) / 지금대로.
12. **앱 아이콘 · 공유 그림:** 표시를 정한 뒤 `apple-icon.png` · `manifest` · OG 그림을 만듦 (권장) / 나중에.
13. **없는 쪽 · 오류 화면:** `app/not-found.tsx`, `app/error.tsx`를 한국어로 (권장) / Next 기본 화면.

## 7. 확인하지 못한 것

- 실제 폰(iOS Safari, 삼성 인터넷)에서 전후 비교를 끌어 보지 못했다. 그림 위 범위 입력이 세로 스크롤을 막는지는 모른다. 막히면 손잡이만 끌게 바꾼다.
- 파비콘이 어두운 탭 바에서 어떻게 보이는지 보지 못했다. 파란 바탕 위 흰 선이라 괜찮을 것으로 본다. 16px 가독성은 화면 캡처로만 봤다.
- 개인정보 처리방침 링크를 다른 링크와 구분해 보이라는 권고는 개인정보위 작성지침에서 본 것으로 기억한다. 이번에 원문을 다시 읽지 않았다.
- awwwards 사이트는 첫 화면과 글 위주로 봤다. 움직임은 화면 캡처 몇 장으로 판단했다. Halcyon은 로딩 화면 때문에 카드 모양을 글로만 확인했다.
- 예시 화면은 1280px · 360px에서 가로 스크롤 없음, 콘솔 오류 없음, 버튼 높이 40px 이상을 확인했다. 화면 읽기 프로그램으로 직접 읽어 보지는 않았다.

## 출처

- 3.3디자인스페이스: [문의하기](https://www.33design.space/inquiry), [홈](https://www.33design.space/), [사례 2285](https://www.33design.space/portfolio/2285)
- INSHOW (인테리어쇼): [홈](http://www.interiorshow.kr/index.php), [포트폴리오](http://www.interiorshow.kr/bbs/board.php?bo_table=sub1_2), [사례 상세](http://www.interiorshow.kr/bbs/board.php?bo_table=sub1_2&wr_id=311), [상담 신청 안내](http://www.interiorshow.kr/theme/nero/subpage/sub2_1.php)
- awwwards 목록: [Architecture](https://www.awwwards.com/websites/architecture/), [Real Estate](https://www.awwwards.com/websites/real-estate/), ['renovation' 검색](https://www.awwwards.com/websites/?text=renovation)
- awwwards 소개 쪽: [Loam House](https://www.awwwards.com/sites/loam-house), [Storey Architecture](https://www.awwwards.com/sites/storey-architecture), [Woonpact](https://www.awwwards.com/sites/woonpact), [Halcyon Lighting](https://www.awwwards.com/sites/halcyon-lighting-2), [NYC Renovation](https://www.awwwards.com/sites/nyc-renovation), [RS.D Agencements](https://www.awwwards.com/sites/rs-d-agencements-renovation), [Rogers-O'Brien](https://www.awwwards.com/sites/rogers-obrien-construction), [BAM Rénovation](https://www.awwwards.com/sites/bam-renovation), [AllHaus](https://www.awwwards.com/sites/allhaus)
- 실제 사이트: [Loam House](https://residences.loamhouse.com.au/), [Storey](https://www.storeyarchitecture.co.uk/), [Woonpact](https://woonpact.gent/), [Halcyon](https://www.halcyon.co.nz/), [NYC Renovation](https://nycrenovation.com/), [RS.D](https://www.rsd-agencements.com/), [Rogers-O'Brien](https://r-o.com/), [BAM Rénovation](https://www.bam-renovation.com/), [AllHaus](https://moderncraftaz.com/)
- 믿집 문서: `docs/design/vendor-portfolio.md`(사례 항목 · 사진 역할 · 전후 짝), `docs/design/mypage-vendor-info.md`(내 프로젝트 카드 · 업체 상세 · 고지), `AGENTS.md` 1 · 5 · 6 · 8장
