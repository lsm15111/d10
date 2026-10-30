# 화면설계서

- 결과: [믿집-화면설계서.pdf](믿집-화면설계서.pdf) (52쪽, 1280×720 가로), 같은 내용의 PPT: [믿집-화면설계서.pptx](믿집-화면설계서.pptx) (표 · 글 · 번호 표시를 PowerPoint에서 고칠 수 있음), HTML: [화면설계서.html](화면설계서.html)
- 구성: 표지 → 버전 기록(2쪽) → 화면 목록(3쪽) → 화면마다 한 쪽(캡처 · 번호 · Description · Check Point)
- 화면 흐름은 따로 그림으로: [화면흐름.png](화면흐름.png)
- 견적 받기 창은 열려도 주소가 바뀌지 않아서, URL 칸에는 같은 질문을 한 화면으로 보여 주는 `/start`를 적는다.
- 형식은 다른 팀 산출물(SKN05 FinPilot 화면설계서)을 따랐다: 위에 화면명 · 화면 경로 · 요구사항 ID · 화면 ID 표, 왼쪽 캡처에 번호, 오른쪽에 번호별 설명
- 캡처는 실제로 돌아가는 화면이다 (2026-10-29, 로컬 개발 서버, 1440×900). 프로젝트 3~6단계 · 회원관리는 API를 만들기 전이라 예시 데이터로 그린 화면이고, 해당 쪽 Check Point에 적었다.

## 고칠 곳

| 무엇 | 파일 |
| --- | --- |
| 화면 · 번호 · 설명 · Check Point | `src/screens.py` (`SCREENS`) |
| 팀 이름 · 작성자 · 버전 기록 | `src/build.py` 위쪽 `TEAM` · `WRITER` · `HISTORY` (고칠 때마다 한 줄 더한다) |
| 쪽 모양 (표 · 색 · 글자 크기) | `src/build.py`의 `CSS` |

## 다시 만들기

웹(3100)과 API · DB · Redis를 띄운 뒤 실행한다. 캡처용 시험 계정 5개(고객 1 · 업체 3 · 관리자 1)와 프로젝트 1개를 만들고, 비밀번호는 `MJ_SCREENS_STATE` 파일에만 둔다. 이 파일은 저장소 밖 경로로 정한다.

```bash
docker compose up -d db redis api
```

```bash
cd docs/screens/src && MJ_SCREENS_STATE=/tmp/mj-screens.json python capture.py shots
```

```bash
cd docs/screens/src && python build.py
```

PPT는 build.py가 만든 `shots/deck.json`으로 만든다. pptxgenjs가 필요하다 (`npm install pptxgenjs@3.12.0`, 저장소 밖에 설치했다면 `NODE_PATH`로 위치를 알려 준다).

```bash
cd docs/screens/src && node pptx.js
```

```bash
cd docs/screens/src && MJ_SCREENS_STATE=/tmp/mj-screens.json python capture.py cleanup
```

- `capture.py shots SC-03-004`처럼 화면 ID를 주면 그 화면만 다시 찍는다.
- 표시할 요소를 못 찾거나 캡처 범위 밖이면 마지막에 '문제' 목록으로 알려 준다.
- cleanup은 시험 계정만 지운다: 고객 · 업체는 탈퇴 API(사진 · 사업자등록증 파일까지), 관리자는 탈퇴가 막혀 있어 SQL로.
- 필요한 것: Python 3.12 + `pip install playwright==1.63.0 Pillow==12.3.0`, Node 24 + `pptxgenjs@3.12.0`, 설치된 Chrome (`channel="chrome"`), Windows 글꼴 `malgun.ttf`(시험용 사업자등록증 그림).
