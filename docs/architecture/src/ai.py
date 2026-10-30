import sys

from svgkit import Svg

s = Svg(1800, 1290, "믿집 AI 구조 (첨부안 반영)",
        "첨부한 AI 시스템 아키텍처(예상 공정표 · 업체 추천 에이전트, RAG(pgvector), PostgreSQL, LLM)를 믿집 규칙에 맞춘 구조. 숫자는 계산 엔진만 만들고, 에이전트는 설명 · 고르기만 한다.")

s.text(24, 42, "믿집 AI 구조 (첨부안 반영)", "t-title")
s.text(24, 70, "예상 공정표 · 업체 추천 · 확정 공정표 에이전트 · 숫자(금액 · 기간 · 날짜 · 점수)는 계산 엔진만 만든다 · 배지 = 첨부안과 비교", "t-sub")
s.text(1330, 66, "첨부안과 비교", "b-small")
lx = 1440
for k, t in [("keep", "유지"), ("chg", "바꿈"), ("add", "더함"), ("drop", "뺌")]:
    w = s.badge(lx + 44, 66, k)
    lx += 86

# ── 1. 사용자 입력
s.rect(16, 92, 1768, 172, "grp")
s.text(30, 118, "사용자 입력 (견적 받기 질문 흐름)", "g-label")
s.card(30, 132, 570, 118, "기본 정보", [("지역(시 · 군 · 구) · 집 종류 · 평수 · 준공 연도", None, "b-small"), ("시기 · 집 상태 · 예산(선택)", None, "b-small"), ("첨부안의 스타일 · 특이사항은 추가 요청사항에서 받음", None, "b-mute")], kind="keep", gap=24)
s.card(615, 132, 570, 118, "선택 공정", [("도배(저가형 · 기본형) · 목공(몰딩 · 걸레받이 · 문 · 평탄화)", None, "b-small"), ("공간별 사진 · 도면", None, "b-small"), ("타일 · 전기는 1차 범위 밖 (AGENTS.md 1장)", None, "b-mute")], kind="chg", gap=24)
s.card(1200, 132, 570, 118, "추가 요청사항 (자유 글)", [("스타일 · 일정 조건 · 특이사항 · 선택 · 500자까지", None, "b-small"), ("지금 화면에는 없음 → 넣을지 정할 것", None, "b-small"), ("프롬프트에는 연락처 · 주소를 가리고 '자료'로만 넣음", None, "b-mute")], kind="keep", gap=24)

s.arrow([(900, 264), (900, 300)], "ar", "POST /projects 저장 → 같은 트랜잭션에 jobs(project_created) → worker", 912, 288)

# ── 2. 계산 엔진
s.rect(16, 302, 1768, 112, "box-core")
s.text(32, 330, "계산 엔진 calc (숫자는 여기서만 만든다 · DB · HTTP · 시계를 모르는 순수 함수)", "b-title")
s.badge(1770, 329, "add")
s.text(32, 362, "공정표 초안: 수량 → 품(0.5 올림) → 기간 · 날짜 (휴무일 데이터)", "b-small")
s.text(620, 362, "표준견적서: 기준 단가 × 수량 (단가 · 산식 버전 고정)", "b-small")
s.text(1205, 362, "추천 점수: 후보 거르기(승인 · 지역 · 공정 · 일정) → 점수", "b-small")
s.text(32, 394, "첨부안의 '소요 기간(참고)', '조건 기반 필터링', '적합도 판단'에서 숫자와 거르기를 LLM에서 이쪽으로 옮겼다 (AGENTS.md 3장: LLM이 낸 숫자는 검산 없이 쓰지 않음)", "b-mute")


# ── 3. 에이전트 레이어
s.rect(16, 436, 1768, 436, "grp")
s.text(30, 462, "AI 에이전트 레이어 (3개 · worker 안에서 실행 · 결과 저장 · 상태 변경은 각 기능 service)", "g-label")
s.arrow([(900, 414), (900, 474)], "ar", "계산 결과 + 근거 id를 넘김", 912, 452)
agents = [
    ("① 예상 공정표 에이전트 (FAG-01)", "chg", "LLM + RAG (pgvector)",
     [("1. 입력 정리", "프로젝트 답 · calc 공정표 초안 · 추가 요청사항(가림)"),
      ("2. RAG 검색", "공정별 시공 가이드 · 체크리스트 → 근거 문서 id"),
      ("3. LLM 작성", "작업 설명 · 주의사항 · 준비할 일 (날짜 · 기간은 쓰지 않음)"),
      ("4. 검산", "날짜 · 기간이 calc와 같은지 · 목공 → 도배 순서 · 휴무일")]),
    ("② 업체 추천 에이전트 (FAG-02)", "chg", "LLM · pgvector는 나중 (업체 소개 · 포트폴리오 유사도)",
     [("1. 후보 거르기 (SQL)", "승인 업체 · 시공 지역 · 공정 · 일정 가능"),
      ("2. 점수 (calc)", "규칙 점수로 상위 10곳 · 예산은 거르기에 쓰지 않음"),
      ("3. LLM 고르기", "3곳 + 추천 이유 (후보 id 안에서만)"),
      ("4. 검산", "후보 밖 id · 지역 밖 업체면 버림 (치명 오류)")]),
    ("③ 확정 공정표 에이전트 (FAG-03)", "add", "첨부안에 없음 · 요구사항 v3.2에 있음",
     [("1. 입력", "확정 업체가 등록한 공사기간 (FFV-06 · 07)"),
      ("2. 일정 (calc)", "반나절 단위 · 휴무일 · 공정 순서"),
      ("3. LLM 작성", "순서 설명 · 할 일 (관리사무소 신고 등)"),
      ("4. 검산", "휴무일 작업 · 겹침 · 도배가 목공보다 먼저면 버림")]),
]
for i, (title, kind, tag, steps) in enumerate(agents):
    x = 30 + i * 585
    s.rect(x, 476, 570, 300, "box-ai")
    s.text(x + 16, 504, title, "b-title")
    s.badge(x + 556, 503, kind)
    s.text(x + 16, 528, tag, "b-mute")
    for j, (h, d) in enumerate(steps):
        yy = 544 + j * 56
        s.rect(x + 16, yy, 538, 48, "box-sub", rx=8)
        s.text(x + 30, yy + 20, h, "s-title")
        s.text(x + 30, yy + 39, d, "b-mute")
s.rect(30, 790, 1740, 70, "box-sub")
s.text(46, 816, "공통 규칙: llm.py 한 곳 · 공급자 하나 · 프롬프트 버전 · Pydantic 스키마 검사 · 실행 기록(입력 스냅숏 · 모델 · 프롬프트 버전 · 비용 · 시간)은 jobs 행", "b-small")
s.text(46, 842, "CI는 스텁(LLM_LIVE=false) · LLM이 실패하면 계산 결과만 보이고 '설명을 만들지 못했어요' · 화면에 AI가 쓴 글이라는 안내 · eval 추천 20 · 공정표 15", "b-small")
s.badge(1756, 816, "add")

# ── 4. RAG
s.arrow([(315, 900), (315, 874)], "ar", "근거 문서", 325, 892)
s.arrow([(900, 900), (900, 874)], "ar-d", "나중", 910, 892)
s.rect(16, 902, 1768, 76, "box-data")
s.text(32, 930, "RAG 검색 (pgvector · 같은 PostgreSQL)", "b-title")
s.badge(1770, 929, "chg")
s.text(360, 930, "공정 · 주제 · 버전으로 먼저 거르고 → 벡터 검색 상위 5개 → 문서 id · 출처 · 적용일을 근거로 함께 넘김", "b-small")
s.text(32, 960, "따로 두는 벡터 DB · 검색 서비스는 없다 → app/agent/retrieval.py 함수 하나 · 첨부안의 'RAG 검색 레이어'는 층이 아니라 함수", "b-mute")

# ── 5. 데이터 레이어
s.rect(16, 998, 1768, 276, "grp")
s.text(30, 1024, "데이터 레이어", "g-label")
s.arrow([(600, 1012), (600, 980)], "ar")
s.rect(30, 1038, 1150, 222, "box-data")
s.text(46, 1066, "PostgreSQL 17 + pgvector (원본 하나 · 벡터 DB를 따로 두지 않음)", "b-title")
s.card(46, 1080, 366, 166, "구조 데이터 (SQL로 읽음)", [("ref_prices: 표준시장단가 · 노임단가 · 조달청", None, "b-small"), ("holidays · 업체(승인 · 지역 · 공정 · 평점 · 후기)", None, "b-small"), ("프로젝트 · 공간 · 공정", None, "b-small"), ("첨부안의 공공데이터 → RAG를 표로 옮김", None, "b-mute")], cls="box-sub", kind="chg", title_cls="s-title", gap=24)
s.card(424, 1080, 366, 166, "RAG 문서 (rag_chunks · 벡터)", [("공정별 시공 가이드 · 체크리스트 (팀이 씀)", None, "b-small"), ("공개 기준 문서 (이용 조건 확인 뒤)", None, "b-small"), ("믿집 완공 사례 (고객 동의 뒤 · 나중)", None, "b-small"), ("열: 출처 · 적용일 · 버전 · 이용 조건", None, "b-mute")], cls="box-sub", kind="chg", title_cls="s-title", gap=24)
s.card(802, 1080, 362, 166, "넣지 않음", [("커뮤니티 글 (약관 · 저작권 · 개인정보)", None, "b-small"), ("지어낸 사례 · 실적", None, "b-small"), ("믿집 밖 시공 건수 (셀 수 없음)", None, "b-small"), ("privacy-rules.md", None, "b-mute")], cls="box-off", kind="drop", title_cls="s-title", gap=24)

s.arrow([(1182, 1150), (1194, 1150)], "ar")
s.arrow([(1194, 1170), (1182, 1170)], "ar")
s.card(1196, 1038, 574, 222, "LLM 공급자 (ADR로 하나)", [
    ("첨부안: OpenAI API (GPT-4o · GPT-4.1 · GPT-4.1 mini)", None, "b-small"),
    ("→ 공급자 하나로 정하고 작업별 모델은 ADR에 적는다", None, "b-small"),
    ("임베딩 모델도 같은 ADR에서 정한다", None, "b-small"),
    ("질문 이해 · 근거 기반 답 · 결과 작성은 그대로", None, "b-small"),
    ("모델 이름은 정하는 날 공급자 목록으로 다시 확인", None, "b-mute")], cls="box-ext", kind="chg", gap=26)

open(sys.argv[1], "w", encoding="utf-8").write(s.render())
print("ok")
