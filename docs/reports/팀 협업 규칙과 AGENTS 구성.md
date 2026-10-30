# 작게 나누고, 한 곳에 적고, 기계로 지킨다

> 기록 · 작성 2026-10-29 · 근거: `docs/research_notes/팀 협업 규칙과 AGENTS 구성/` 노트 10개 · `AGENTS.md`는 읽기만 하고 고치지 않았다

믿집의 협업 규칙은 방향이 이미 맞다. 고칠 것은 세 가지다. 첫째, PR 단위를 **이슈 하나 · 관심사 하나 · 테스트 포함**으로 정하고, 크기는 **200줄 목표 · 400줄 경고 · 800줄 차단**으로 센다(lock · 생성 파일 제외). 둘째, 규칙을 글이 아니라 **GitHub 설정과 CI로 지킨다**. 승인 1명, squash만, PR 제목 검사, 필수 CI 하나를 ruleset으로 건다. 그런데 이 설정은 **비공개 저장소 + 무료 요금제에서는 강제되지 않는다**. 그래서 공개 여부와 요금제를 가장 먼저 정해야 한다. 셋째, `AGENTS.md`를 **140줄 · 12 KB에서 약 115줄 · 8 KB로 줄인다**. 명령 · 금지 · 도메인 규칙 · 완료 기준만 남긴다. 구조 설명과 Git 절차는 다른 문서로 옮긴다. '하지 않는다' 규칙은 권한 설정 · CI · CODEOWNERS로 막는다. 참고 저장소는 같은 스택(FastAPI + Next.js 16 + 워커)인 **Polar가 1순위**다. 기록은 '한 사실은 한 곳'으로 나눈다. 작업 상태는 GitHub Project, 검증 상태는 `docs/status.md`, 되돌리기 어려운 결정은 ADR, 회의 · 회고는 고치지 않는 날짜 파일에 둔다. 이 권고는 대부분 업계 · 오픈소스 자료에서 끌어왔다. 학생 팀을 직접 다룬 연구는 찾지 못했다.

## PR 하나는 이슈 하나, 200줄 목표, 400줄 경고

### 작은 PR의 이유는 속도가 아니라 리뷰 품질이다

PR이 커지면 리뷰가 얕아진다. Google의 리뷰 900만 건 연구에서 변경의 **중앙값은 24줄**이었다. 작은 변경은 첫 피드백이 1시간 안에 왔다. 아주 큰 변경은 약 5시간 걸렸다. 같은 논문은 크기가 클수록 쓸모 있는 댓글이 줄어든다고 적었다 ([Google 논문](https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf)). Microsoft의 리뷰 댓글 150만 개 분석도 같다. 건드린 파일이 많을수록 쓸모 있는 댓글 비율이 낮았다 ([Microsoft Research](https://www.microsoft.com/en-us/research/?p=168510)). 반대 증거도 있다. PR 845,316개를 본 2022년 연구는 크기와 병합 시간 사이에 관계가 없다고 했다 ([arXiv 2203.05045](https://arxiv.org/abs/2203.05045)). 그러니 작은 PR을 '빨리 병합하려고' 고집할 이유는 약하다. 진짜 이유는 **리뷰어가 끝까지 읽고 결함을 찾게 하는 것**이다. 자주 인용되는 '400줄' 기준은 2006년 SmartBear/Cisco 사례에서 왔다 ([SmartBear](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)). 판매사가 낸 자료라 법칙이 아니라 관례로 쓴다.

AI 도구는 이 문제를 키운다. Faros의 개발자 1만 명 이상 측정에서 AI 사용은 **PR 리뷰 시간 91% 증가**와 함께 나타났다 ([Faros](https://www.faros.ai/blog/are-ai-coding-assistants-really-saving)). CodeRabbit은 AI가 함께 쓴 PR에서 문제가 약 **1.7배** 많았다고 했다 ([CodeRabbit](https://coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)). 둘 다 판매사 자료이고 인과를 보이지 않는다. Swarmia는 에이전트 PR이 1–5줄과 500줄 이상 양 끝에 몰린다고 적었다 ([Swarmia](https://help.swarmia.com/features/ai-tools/cloud-agents)). 그래서 에이전트 PR에는 사람 PR과 같은 상한을, 더 엄격하게 적용한다.

### 단위를 먼저 정하고, 크기는 기계로 센다

단위가 크기보다 먼저다. Google은 '한 가지 일을 하는 자기완결 변경, 관련 테스트 포함, 제출 뒤에도 시스템이 동작'을 기준으로 둔다. 그리고 **100줄은 보통 적당하고 1,000줄은 보통 너무 크다**고 한다 ([Google small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)). Kubernetes는 검토 못 할 덩어리 10개보다 작고 뻔한 PR 100개를 원한다 ([Kubernetes](https://www.kubernetes.dev/docs/guide/pull-requests/)). 믿집은 **이슈 하나 = 관심사 하나 = PR 하나**로 정한다. 제목을 '및'이나 '그리고' 없이 한 문장으로 못 쓰면 나눈다. 리팩터링 · 포맷 · 의존성 갱신은 기능과 섞지 않는다. Kent Beck의 말대로 "바꾸기 쉽게 만든 뒤, 쉬운 변경을 한다" ([Kent Beck](https://newsletter.kentbeck.com/p/tidy-first-example)).

| 항목 | 규칙 | 지키는 장치 |
| --- | --- | --- |
| 단위 | 이슈 하나 · 관심사 하나 · 테스트 포함 · 병합 뒤 main CI 초록 | 리뷰, PR 템플릿 |
| 크기 | 목표 200줄 이하(이상적 50–150). 400줄을 넘으면 본문에 나누지 못한 이유. 800줄 이상은 리뷰어가 `size-exception` 라벨을 달아야 병합. 파일 15개를 넘으면 경고 | PR 크기 라벨 Action |
| 세지 않는 것 | `frontend/pnpm-lock.yaml`, `backend/uv.lock`, `frontend/lib/backend/schema.d.ts`, 스냅샷 · 바이너리 | `.gitattributes` + 라벨러 제외 목록 |
| 세는 것 | Alembic migration, 테스트, 문서 (사람이 읽어야 한다) | — |
| 분리 | 리팩터링 · 일괄 포맷 · 의존성 갱신은 각각 따로 | 리뷰 |
| 수명 | 첫 리뷰는 같은 날 또는 다음 반나절. 병합 목표 1일, 최대 2일 | 회의에서 2일 넘은 브랜치 점검 |
| 동시 작업 | 1인당 리뷰 요청 PR 1개 + draft 1개 | 회의 점검 |

크기는 '추가 + 삭제'로 세고, 사람이 손대지 않는 파일은 뺀다. GitLab의 자동 봇은 yarn 의존성 하나 추가한 MR을 1,166줄이라며 "꽤 크다"고 했다 ([GitLab 이슈](https://gitlab.com/gitlab-org/gitlab/-/issues/24541)). 이런 오판을 막는 방법은 하나의 목록을 두 곳에 쓰는 것이다. `.gitattributes`에 `linguist-generated`를 달면 GitHub 화면에서 접힌다 ([GitHub Docs](https://docs.github.com/en/repositories/working-with-files/managing-files/customizing-how-changed-files-appear-on-github)). Kubernetes의 크기 봇도 이 표시를 보고 뺀다 ([Prow size.go](https://raw.githubusercontent.com/kubernetes-sigs/prow/main/pkg/plugins/size/size.go)). 같은 목록을 `CodelyTV/pr-size-labeler`의 `files_to_ignore`에 넣는다. 이 Action은 저장소 전체 경로로 비교하므로 `frontend/pnpm-lock.yaml`처럼 경로를 다 적는다 ([CodelyTV](https://github.com/CodelyTV/pr-size-labeler)). 라벨 구간은 Kubernetes 방식을 400에 맞춰 바꾼다: XS 10 미만, S 30 미만, M 100 미만, L 400 미만, XL 400–799, XXL 800 이상.

```gitattributes
# 기존 줄 아래에 더한다 (세 파일은 저장소에 실제로 있다)
frontend/pnpm-lock.yaml          linguist-generated=true
backend/uv.lock                  linguist-generated=true
frontend/lib/backend/schema.d.ts linguist-generated=true
```

큰 기능은 층별로 나눠 차례로 올린다. 믿집 스택에서는 ① Alembic migration + 모델(넓히기만) → ② FastAPI 엔드포인트 + pytest + 다시 만든 TS 타입 → ③ Next.js 화면 → ④ 나중에 옛 컬럼을 지우는 migration 순서가 자연스럽다. 각 PR은 혼자 병합해도 CI가 통과한다. **넓히기와 좁히기(expand · contract)는 한 PR에 넣지 않는다** ([tessl db-migrate](https://tessl.io/registry/skills/github/simstudioai/sim/db-migrate), [Unleash ADR](https://docs-new.getunleash.io/contributing/ADRs/back-end/breaking-db-changes)). 일괄 포맷 PR은 따로 올린다. squash 병합 뒤 main의 커밋 해시를 `.git-blame-ignore-revs`에 후속 PR로 더한다 ([pydata 안내](https://pst-notebook-cell-styling.readthedocs.io/en/latest/community/topics/attribution.html)). GitHub의 스택 PR(`gh stack`)은 큰 AI 생성 PR을 층으로 쪼개는 용도로 나왔지만 2026-07 기준 **공개 미리보기**다 ([GitHub 블로그](https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/), [IT Brief](https://itbrief.co.uk/story/github-puts-stacked-pull-requests-into-public-preview)). 한 달짜리 프로젝트에서는 기능 플래그보다 '메뉴에 안 걸린 화면'이나 '백엔드만 먼저'가 싸다.

### AI 에이전트가 만든 PR에는 이름 있는 사람이 책임진다

플랫폼과 오픈소스는 세 가지로 모였다. 첫째, **사람이 모든 줄을 먼저 읽는다**. LLVM은 LLM이 만든 코드와 글을 다른 사람에게 리뷰 요청하기 전에 직접 다 읽으라고 한다 ([LLVM](https://llvm.org/docs/AIToolPolicy.html)). 둘째, AI 사용을 PR에 밝힌다. 셋째, 큰 AI 생성 PR은 받지 않는다 ([Kubernetes](https://www.kubernetes.dev/docs/guide/pull-requests/)). GitHub은 Copilot PR을 맡긴 사람의 승인을 **필수 승인 수에 세지 않는다** ([GitHub Docs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output)). 믿집도 같은 원칙을 쓴다. **에이전트를 돌린 사람과 승인하는 사람은 달라야 한다.** 에이전트 PR은 draft로 연다. 작성자가 diff 전체를 읽고, 테스트 · 타입 · lint 결과를 붙인 뒤 ready로 바꾼다. 리뷰 요청 전에 `/code-review`(Claude Code)나 `/review`(Codex)로 자체 점검을 돌린다 ([Claude Code](https://code.claude.com/docs/en/best-practices), [Codex](https://learn.chatgpt.com/guides/best-practices)). 이 AI 점검은 참고일 뿐 승인이 아니다. 에이전트는 diff가 약 300줄을 넘을 것 같으면 멈추고 나누는 안을 낸다. 에이전트는 병합하지 않는다. `.github/workflows/`나 비밀값을 건드리는 변경은 사람이 따로 확인한다.

## 브랜치 · 병합 · 리뷰는 글이 아니라 저장소 설정이 지킨다

### 공개 여부와 요금제가 모든 설정을 결정한다

GitHub 무료 요금제에서 **ruleset과 브랜치 보호는 공개 저장소에서만 동작한다**. 비공개 저장소는 Pro(개인)나 Team(조직)이 있어야 한다 ([about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), [GitHub 요금제](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)). Team은 **사용자당 월 $4**다. 무료 요금제에서는 CODEOWNERS와 draft PR도 공개 저장소 전용이다 ([GitHub Pricing](https://github.com/pricing)). merge queue는 조직이 가진 공개 저장소이거나 Enterprise Cloud여야 한다 ([GitHub changelog](https://github.blog/changelog/2023-07-12-pull-request-merge-queue-is-now-generally-available/)). Actions는 공개 저장소의 표준 러너가 무료이고, 비공개는 무료 요금제 기준 월 $12어치(리눅스 약 2,000분)다 ([Actions 과금](https://docs.github.com/en/billing/concepts/product-billing/github-actions)). 5명이 하루 PR 1개씩, push 3번, 한 번에 9분이면 월 약 3,000분이다. 노트의 가정치이고 측정값이 아니지만, 무료 한도를 넘을 수 있다. 공개 저장소에서는 비밀값 push 보호가 기본으로 켜진다 ([push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)). GovBiz에서 승인 0명으로 병합되고 CI가 원격에서 강제되지 않은 일은, 비공개 + 무료 조직이었다면 이 표로 설명된다. 그래서 **비공개 + 무료 조직은 선택지에서 뺀다**. 남는 안은 공개 + 무료 조직, 비공개 + Team 조직(6명이면 월 $24), 비공개 + 개인 Pro다. 개인 Pro는 학생 개발자 팩으로 무료일 수 있지만, 자격이 '학위 · 졸업장 과정'이라 부트캠프가 해당하는지 확인해야 한다 ([GitHub Education](https://docs.github.com/en/education/about-github-education/github-education-for-students/apply-to-github-education-as-a-student)). 어느 안이든 저장소는 **조직(organization) 아래**에 둔다. issue type과 issue field가 조직 기능이기 때문이다(아래 기록 절).

### GitHub flow, 공유 저장소, ASCII 브랜치 이름

브랜치 모델은 `main` 하나에 짧은 작업 브랜치를 쓰는 GitHub flow다. git-flow를 만든 사람도 2020년에, 계속 배포하는 웹 앱은 GitHub flow 같은 단순한 방식을 쓰라고 적었다 ([nvie](https://nvie.com/posts/a-successful-git-branching-model/)). ThoughtWorks는 git-flow식 장기 브랜치를 '보류(Hold)'에 두었다 ([TW Radar](https://www.thoughtworks.com/radar/techniques/long-lived-branches-with-gitflow)). 믿집에는 구체적인 함정도 있다. `Closes #12`는 **PR이 기본 브랜치를 향할 때만** 이슈를 닫는다 ([GitHub Docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)). `develop` 브랜치를 두면 이슈 자동 닫기와 Project 자동 이동이 끊긴다. 저장소는 fork가 아니라 **공유 저장소 모델**로 쓴다. GitHub은 이 모델이 비공개 프로젝트를 하는 작은 팀에 더 흔하다고 설명한다 ([GitHub Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models)). fork에서 온 PR은 비밀값 · 브랜치 자동 삭제 · Actions 토큰이 다르게 동작한다. 브랜치 이름은 `이슈번호-영문-설명`(예: `12-quote-form-validation`)으로 쓴다. Conventional Branch 규격은 소문자 영문 · 숫자 · 하이픈만 허용하고, AI 도구용 접두어 `claude/`, `codex/`, `copilot/`을 더했다 ([conventionalbranch.org](https://conventionalbranch.org/)). Git 자체는 한글 ref 이름을 막지 않는다 ([git-check-ref-format](https://git-scm.com/docs/git-check-ref-format)). 그래도 URL 인코딩, 셸 따옴표, macOS와 Windows의 한글 정규화 차이를 피하려고 영문을 권한다.

### squash만 허용하고, PR 제목이 곧 main의 커밋이다

병합은 **squash만** 허용한다. 그러면 main에는 PR당 커밋 하나가 남는다. 되돌리기도 PR 단위로 된다. 함정이 하나 있다. GitHub의 기본 squash 메시지는 **커밋이 1개인 PR에서 PR 제목이 아니라 그 커밋 메시지를 쓴다** ([GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests)). AI 도구는 한 번에 커밋 하나를 만드는 일이 많다. 그래서 설정을 'Pull request title' 계열로 바꿔야 "PR 제목 = 커밋 제목"이 성립한다. 그다음 PR 제목만 CI에서 검사한다. `amannn/action-semantic-pull-request@v6`는 `types`, `scopes`를 받고 `prompt`, `eval` 같은 팀 타입도 등록할 수 있다 ([Action](https://github.com/amannn/action-semantic-pull-request)). 필수 체크로 쓰려면 `synchronize` 이벤트를 넣는다. CI 쪽 함정도 있다. 경로 필터(`paths:`)로 **워크플로 전체가 건너뛰어지면 필수 체크가 '대기'에 묶여 병합이 막힌다**. 조건으로 건너뛴 job은 '성공'으로 보고된다 ([GitHub Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks)). 그래서 모든 job 뒤에 집계 job `ci-ok`를 두고 그것 하나만 필수로 건다. job 이름을 바꿔도 필수 체크가 조용히 빠지지 않는다. GitHub이 만든 ruleset JSON 예시를 출발점으로 쓸 수 있다 ([ruleset-recipes](https://github.com/github/ruleset-recipes)).

| 위치 | 설정 | 값 |
| --- | --- | --- |
| Settings → General | 병합 방식 | squash만 (merge commit · rebase 끔) |
| | squash 기본 메시지 | Pull request title (결정 G2) |
| | 병합 뒤 브랜치 자동 삭제 · auto-merge · 브랜치 갱신 제안 | 켬 |
| | 권한 | 팀원은 Write, 1–2명만 Admin. Admin 우회는 일상에서 쓰지 않음 |
| Ruleset `main` | 삭제 막기 · force push 막기 · linear history | 켬 |
| | PR 필수, 승인 1명 | 켬 |
| | 새 push가 오면 승인 무효 · 마지막 push는 다른 사람이 승인 | 켬 |
| | CODEOWNERS 리뷰 필수 | 켬 (위험 경로만 지정) |
| | 대화 해결 필수 | 켬 (P1 · P2 댓글을 풀어야 병합) |
| | 필수 체크 | `ci-ok` + `pr-title`, 최신 상태(strict) 켬 |
| | 우회 목록 | 관리자 'PR로만' (조직 저장소만 가능) |
| | 서명 커밋 · 배포 필수 | 끔 (학생 팀 설정 부담) |
| CI | 워크플로 | `ci.yml` 하나 + 마지막 `ci-ok` 집계 job. 워크플로 단위 `paths:` 금지 |
| CODEOWNERS | 대상 | `AGENTS.md` · `**/AGENTS.md` · `CLAUDE.md` · `.claude/` · `.github/` · `docs/adr/` · `backend/migrations/` · `evaluation/` |

현재 `ci.yml`은 `concurrency`가 있고, 프론트 job이 백엔드 job의 `openapi.json`을 받아 타입 일치를 검사한다(`needs: backend`). 그래서 경로 필터로 백엔드를 건너뛰면 타입 검사가 깨진다. 경로 필터는 `openapi.json`을 커밋하기로 정한 뒤에만 넣는다(결정 G18). 노트에 따르면 이 CI는 **아직 한 번도 원격에서 돈 적이 없다**. 저장소를 올린 첫 주에 필수 체크가 실제로 초록이 되는지부터 본다.

### 리뷰: 승인 1명, 같은 날 응답, 댓글에 강도를 붙인다

승인은 1명으로 한다. AB180은 리뷰어를 1명에서 2명으로 늘리자 생산성이 떨어졌다고 적었다. 그 뒤 리뷰를 의도적으로 나눠 맡겼다 ([요즘IT](https://yozm.wishket.com/magazine/detail/1497/)). 리뷰어는 PR마다 돌아가며 맡고, 위험한 경로만 CODEOWNERS로 특정 사람을 부른다. 응답은 **같은 작업일 안**에 한다. Google은 리뷰 요청에 답하는 최대 시간을 1영업일로 본다 ([Google](https://google.github.io/eng-practices/review/reviewer/speed.html)). 댓글에는 강도를 붙인다. 뱅크샐러드의 **Pn 룰**은 P1 꼭 반영 · P2 적극 고려 · P3 웬만하면 · P4 선택 · P5 사소한 의견이다. 글로만 오가는 리뷰에서 가벼운 말이 막는 말로 읽히는 일을 줄이려고 만들었다 ([뱅크샐러드](https://blog.banksalad.com/tech/banksalad-code-review-culture/)). P1 · P2를 'Request changes'로 쓰고, ruleset의 '대화 해결 필수'와 묶는다. 칭찬은 Conventional Comments의 `praise:`를 빌린다 ([conventionalcomments.org](https://conventionalcomments.org/)). AI가 만든 PR은 테스트 diff와 lock 파일부터 본다. GitHub은 지워지거나 건너뛴 테스트, 지어낸 패키지를 조심하라고 한다 ([GitHub Docs](https://docs.github.com/en/copilot/tutorials/review-ai-generated-code)). AI 리뷰어는 **하나만** 켜고 승인으로 세지 않는다. Copilot 코드 리뷰는 기본적으로 필수 승인에 들어가지 않는다 ([GitHub Docs](https://docs.github.com/en/copilot/concepts/agents/code-review)). 실무 연구에서도 자동 리뷰 댓글의 73.8%가 반영됐지만 PR을 닫는 데 걸린 평균 시간은 **5시간 52분에서 8시간 20분으로 늘었다** ([arXiv 2412.18531](https://arxiv.org/abs/2412.18531)). 쓸모 있는 추가 점검이지 관문이 아니다.

### 커밋 제목과 변경 기록

커밋 제목 형식 `type(범위): 한국어 요약`은 유지한다. Conventional Commits는 `feat`, `fix` 말고 다른 타입도 허용한다. 다만 규격에 없는 타입은 이 규격 위에 만든 도구가 건너뛴다고 스스로 경고한다 ([Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)). 그래서 `prompt`, `eval`은 세 곳(PR 제목 검사, 쓴다면 commitlint, 쓴다면 변경 기록 생성기)에 등록한다. `git revert`가 만드는 `Revert "..."`는 형식에 맞지 않으므로 `revert` 타입을 더한다. 범위 `docs`는 타입 `docs`와 겹쳐 `docs(docs):`가 생기니 범위 목록에서 뺀다. 프롬프트로 버그를 고치면 `fix`인지 `prompt`인지 갈린다. "프롬프트 글만 바뀌면 `prompt`, 사용자 동작이 바뀌면 `feat`/`fix` 우선" 한 줄을 정한다. 한국어 어미는 '~한다' 평서형(`feat(api): 가견적 요청 API를 추가한다`)과 명사형(`… 추가`)이 실제로 섞여 쓰인다 ([sodalive](https://git.sodalive.net/klaus/sodalive-backend-spring-boot/src/branch/test/docs/agent-guides/%EC%BB%A4%EB%B0%8B%EB%A9%94%EC%8B%9C%EC%A7%80.md), [SSAFY 정리](https://velog.io/@kku64r/gitflow)). 하나로 정하고 예시 3–5개를 박아 둔다. AI 도구는 예시를 강하게 따른다. 로컬 훅(husky · commitlint)은 넣지 않는다. commitlint v21은 Node 22 이상을 요구하고 ([commitlint releases](https://github.com/conventional-changelog/commitlint/releases)), `--no-verify`로 쉽게 우회되며, squash 뒤에는 브랜치 커밋이 main에 남지도 않는다. 한국어 비평도 "타입을 줄이고, 강제 도구는 문화가 자리 잡은 뒤에"라고 권한다 ([braindetox](https://braindetox.kr/posts/conventional_commits_critique_2026.html)).

변경 기록(CHANGELOG)은 데모 때만 사람이 다듬는다. 2026-06에 나온 Keep a Changelog 2.0의 원칙은 **"기계는 초안을 쓰고, 사람이 고른다"**이다. 변경 기록을 PR마다 필수 체크로 만들지 말라고도 한다 ([Keep a Changelog 2.0](https://keepachangelog.com/en/2.0.0/)). PR 제목이 이미 한국어 요약이므로 GitHub 자동 릴리스 노트가 머지된 PR 목록을 초안으로 준다 ([GitHub Docs](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)). 데모 직전에 이것을 사용자 관점으로 묶어 `CHANGELOG.md`에 옮기고, 데모마다 annotated tag(`git tag -a v0.1.0 -m "1차 데모"`)와 pre-release를 만든다 ([git-tag](https://git-scm.com/docs/git-tag)). semantic-release는 사람 없이 버전을 정하는 패키지 배포 도구라 맞지 않는다 ([semantic-release](https://github.com/semantic-release/semantic-release)). release-please는 쓸 수 있지만 GITHUB_TOKEN으로 만든 PR이 다른 워크플로를 깨우지 않아 개인 토큰이 필요하다 ([release-please-action](https://github.com/googleapis/release-please-action)). 지금은 과하다.

AI 표기는 두 곳에 남긴다. 커밋 author는 **반드시 사람**이다. CPython의 CLA 봇은 `Author:`만 보고 `Co-authored-by:`는 무시해서, 에이전트가 author인 커밋을 막았다 ([discuss.python.org](https://discuss.python.org/t/cla-bot-and-ai-agents/106635)). 표기 방식은 프로젝트마다 반대다. Kubernetes는 AI 공동 저자 trailer와 AI가 쓴 커밋 메시지를 금지하고 PR 본문 공개만 받는다 ([Kubernetes](https://github.com/kubernetes/community/blob/master/contributors/guide/pull-requests.md)). 리눅스 커널은 `Assisted-by:` 태그를 쓴다 ([kernel.org](https://docs.kernel.org/process/coding-assistants.html)). Rust는 Claude Code의 기본 trailer를 '공개의 나쁜 예'로 든다. 도구 이름만 있고 무엇을 맡겼는지가 없기 때문이다 ([rustc-dev-guide](https://raw.githubusercontent.com/rust-lang/rustc-dev-guide/HEAD/src/llm-guidance/writing.md)). 그래서 trailer는 기계 검색용으로 두고, 진짜 공개는 PR 본문의 'AI 사용' 한 줄(도구 · 맡긴 일 · 사람이 확인한 것)로 한다. Claude Code는 `attribution` 설정으로 trailer를 바꾸거나 숨긴다 ([Claude Code 설정](https://code.claude.com/docs/en/settings-reference)).

### 제안하는 `.github/pull_request_template.md`

OSS 템플릿 96개의 공통 핵심은 '무엇을 · 왜 + 연결 이슈 + 검증 방법'이다. 아래 초안은 현재 AGENTS.md §6의 다섯 칸을 그대로 두고, §7의 보고 세 칸(로컬 · CI · 못 한 것)으로 검증을 나눴다. 검증 칸은 "실제로 한 것만 쓰고, CI가 보여 주는 결과는 붙이지 않는다"는 GitHub CLI 방식을 따른다 ([cli/cli](https://raw.githubusercontent.com/cli/cli/HEAD/.github/PULL_REQUEST_TEMPLATE.md)). 안 돌린 `[ ]` 칸은 지운다. GitHub이 본문의 체크박스를 모두 '열린 할 일'로 세기 때문이다 ([PostHog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md)). UI 변경의 전 · 후 스크린샷은 GitLab 기본 템플릿처럼 조건부로 요구한다 ([GitLab](https://gitlab.com/gitlab-org/gitlab/-/raw/master/.gitlab/merge_request_templates/Default.md)). 채운 본문은 약 150단어(10–15줄)를 넘지 않게 한다. 넘으면 PR을 나눠야 한다는 신호다.

```markdown
<!-- 제목 = squash 커밋 제목: type(범위): 한국어 요약
     예) feat(api): 가견적 요청 API를 추가한다 · fix(web): 견적 화면의 360px 가로 스크롤을 없앤다 -->

## 무엇을 · 왜
<!-- 2~3문장. 첫 문장은 바뀐 결과(사용자·팀이 보게 될 것), 다음은 이유. 파일 나열 X -->


요구사항: FFV-
Closes #

## 호출 흐름 (바뀐 경우만 · 아니면 이 절을 지운다)
<!-- 한 줄. 예) web → POST /api/projects → project.service → PostgreSQL -->

## 검증
<!-- 실제로 돌린 것만 [x]로 남기고 안 돌린 줄은 지운다(필요하면 '못 한 것'으로).
     결과는 한 단어(통과 / 실패: 이유). 출력·통과 개수는 붙이지 않는다. CI가 보여 준다. -->
**로컬에서 돌린 것**
- [x] `uv run pytest <대상>` → 통과
- [x] `uv run ruff check` · `uv run ruff format --check` → 통과
- [x] `pnpm typecheck` · `pnpm lint` → 통과

**CI에 맡긴 것**: 전체 pytest(PostgreSQL · Redis, migration up → down → up) · `pnpm build`

**화면** (UI가 바뀐 경우만): 폰 너비 360px, 가로 스크롤 없음 · 버튼·입력 칸 40px 이상
| 전 | 후 |
|---|---|
|   |   |

## 못 한 것 · 이유
<!-- 없으면 "없음". 남긴 일은 후속 이슈 번호와 함께 -->
- 없음

## 해당할 때만 (아니면 줄째 지운다)
- 400줄(lock·생성 파일 제외)을 넘는 이유:
- DB migration: `docker compose run --rm migrate` + `alembic check` 결과, downgrade 확인
- 새 환경변수: `.env.example`에 한국어 주석과 함께 추가함
- 기록: `docs/status.md` 행 변경 / ADR-NNNN / design 문서의 열린 결정 번호
- 리뷰어가 먼저 볼 곳:

## AI 사용
<!-- 한 줄: 도구 / 맡긴 일 / 사람이 직접 확인한 것. 안 썼으면 "없음".
     프롬프트·세션 기록은 붙이지 않는다. 작성자(사람)가 diff 전체를 읽고 설명할 수 있을 때 ready로 바꾼다. -->
- 예) Claude Code / 서비스·테스트 초안 / 작성자가 diff 전체를 읽고 pytest를 직접 돌림
```

PR 템플릿은 Markdown 하나만 둔다. GitHub은 PR에 이슈 폼을 지원하지 않고, 여러 템플릿은 `?template=` 주소로만 고를 수 있다 ([GitHub Docs](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)). 'PR title' squash 설정을 쓰면 위의 HTML 주석과 체크박스가 main 커밋에 섞이지 않는다.

## 참고할 저장소: 같은 스택인 Polar가 1순위, 별 개수는 기준이 아니다

인기와 구조는 따로 간다. 별 157k의 Open WebUI 백엔드는 `routers/`와 `models/`를 평평하게 둔 층 우선 구조다 ([Open WebUI](https://github.com/open-webui/open-webui)). 별이 많은 Documenso, Plane, Infisical, Twenty, Supabase Studio는 이제 Next.js App Router가 아니다. 예를 들어 Documenso는 React Router + Vite로 옮겼다 ([Documenso package.json](https://raw.githubusercontent.com/documenso/documenso/main/apps/remix/package.json)). vercel/commerce는 2026-10-20에 보관(archive)됐다 ([README](https://raw.githubusercontent.com/vercel/commerce/main/README.md)). 그래서 순위는 별 대신 **스택이 같은지, 2026년에도 활발한지, 규칙을 글과 검사로 남겼는지**로 매겼다.

| 순위 | 저장소 | 가져올 것 | 따라 하지 말 것 |
| --- | --- | --- | --- |
| 1 | [Polar](https://github.com/polarsource/polar) (FastAPI + Next.js 16 + 워커) | 기능별 파일 역할(`endpoints/service/repository/schemas/tasks`). "모든 DB 쿼리는 repository에" ([server/AGENTS.md](https://github.com/polarsource/polar/blob/HEAD/server/AGENTS.md)). 상태 코드가 붙은 업무 오류, 422는 입력 검증 전용 ([ADR-0002](https://github.com/polarsource/polar/blob/HEAD/handbook/engineering/decisions/0002-status-coded-polar-errors.mdx)). 테스트가 모듈 구조를 따라감. migration 단일 head 검사. OpenAPI 타입 불일치 검사 워크플로 ([workflow](https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/openapi-generate-check.yml)). ADR 목록과 루트 → 영역별 AGENTS.md | 읽기 전용 DB 세션, 약 90개 모듈 규모, 중앙 `models/` 패키지, Dramatiq, 브라우저의 교차 출처 호출 |
| 2 | [Dify](https://github.com/langgenius/dify) | import-linter `layers` 계약과 **줄어들기만 하는** 예외 목록(`unmatched_ignore_imports_alerting = error`) ([.importlinter](https://github.com/langgenius/dify/blob/HEAD/api/.importlinter)). `server.ts`의 `'server-only'` + `cache()` + 쿠키 전달 ([server.ts](https://raw.githubusercontent.com/langgenius/dify/main/web/service/console/server.ts)). `BACKEND_ARCHITECTURE.md` 같은 짧은 구조 문서 | 기능마다 포트 · 어댑터 전부, oRPC, 많은 패키지의 pnpm 작업공간, 문서 분량 |
| 3 | [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices) | 도메인 패키지 체크리스트, 모듈 이름을 붙인 교차 import, 날짜 붙인 migration 이름, `dependency_overrides` 테스트 | `requirements.txt` (uv가 이미 함) |
| 4 | [Kraken](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/) (글) | 층 계약 + 형제끼리 **독립(independence)** 계약(`account|project|vendor`). 예외 수를 빚 지표로 추적. "층은 일찍 건다" | 계약 40개 이상, 자체 린터 |
| 5 | [Sharetribe default-negotiation](https://raw.githubusercontent.com/sharetribe/web-template/main/ext/transaction-processes/default-negotiation/process.edn) | 견적 요청 → 제안 → 수락 흐름의 전이마다 **누가(고객 · 업체 · 운영자 · 시간)** 움직이는지 적는 방식, 전이별 알림 | 호스팅 서비스 백엔드라 코드는 없음 |
| 6 | [cal.diy](https://raw.githubusercontent.com/calcom/cal.diy/main/packages/prisma/schema.prisma) · [Saleor](https://raw.githubusercontent.com/saleor/saleor/main/saleor/order/models.py) | 이력 표 모양: 행위자 종류, 출처, 동작, JSON 데이터, 지워져도 남도록 FK 없이 저장 | tRPC · Prisma, Django 세부 |
| 7 | [Onyx web](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/src/lib/utilsSS.ts) | 서버 쪽 fetch 함수 모양, 같은 주소 `/api` + 리버스 프록시, compose + 가짜 LLM으로 Playwright | bun, Jest, 워크플로 52개 |
| 8 | [vercel/shop AGENTS.md](https://raw.githubusercontent.com/vercel/shop/main/AGENTS.md) | 실행 환경별 파일 이름(`server.ts`, `client.ts`, `types.ts`), `'use client'`는 잎에만, barrel 없음 | Server Action 중심 쓰기 |
| 9 | [bulletproof-react 문서](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/project-structure.md) · [dub](https://github.com/dubinc/dub/tree/main/apps/web/ui) · [토스 Frontend Fundamentals](https://frontend-fundamentals.com/code-quality/code/examples/code-directory.html) | 한 방향 import(공통 → 영역 → 화면), 영역끼리 import 금지, 영역별 폴더(믿집의 `components/<area>`와 같음) | bulletproof의 Next 14 앱, FSD 전체 |
| 10 | [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | 읽기 쉬운 operationId(`generate_unique_id_function`), compose override, `development.md` 분리 | 평평한 `models.py` · `crud.py`, SQLModel, Vite SPA |
| 11 | [matklad ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) · [C4](https://c4model.com/diagrams) · [Mermaid 상태도](https://mermaid.js.org/syntax/stateDiagram.html) | 짧은 구조 문서 형식, 맥락 · 컨테이너 그림 두 장, 상태도 + 전이 표 | arc42 12절 전부, Structurizr, C4 컴포넌트 · 코드 그림 |

참고하지 않을 것도 분명히 한다. teamhide나 fastapi_best_architecture처럼 기능 하나를 다섯 단계로 감싼 헥사고날 예제는 CRUD 기능에서 파일만 늘린다 ([teamhide](https://github.com/teamhide/fastapi-boilerplate)). Cosmic Python 저자들도 앱이 CRUD 껍데기라면 도메인 모델과 repository가 필요 없다고 쓴다 ([Cosmic Python](https://www.cosmicpython.com/book/chapter_02_repository.html)). RealWorld 구현체는 보관되거나 오래 멈춘 것이 많다. 쓸 만한 것은 '명세 + 실행되는 API 테스트'라는 생각뿐이다 ([RealWorld](https://github.com/realworld-apps/realworld)). eShop, Online Boutique 같은 마이크로서비스 예제는 EC2 한 대에서 도는 믿집과 맞지 않는다 ([eShop](https://github.com/dotnet/eShop)).

스타일은 **import 방향을 기계로 검사하는 모듈러 모놀리스**가 가장 근거가 많다. Kraken은 약 400명이 import-linter의 층 계약과 독립 계약을 PR마다 돌린다. Dify와 PostHog도 같은 도구로 경계를 지킨다 ([PostHog pyproject](https://github.com/PostHog/posthog/blob/HEAD/pyproject.toml)). 당근도 2026년에 자기 커뮤니티 시스템을 모듈러 모놀리스로 소개하며 모듈 의존 방향을 아키텍처 테스트로 확인한다고 적었다 ([당근 테크블로그](https://medium.com/daangn/%EC%B2%9C%EB%A7%8C-mau%EB%A5%BC-%EC%A7%80%ED%83%B1%ED%95%98%EB%8A%94-%EC%BB%A4%EB%AE%A4%EB%8B%88%ED%8B%B0-%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84-%EC%86%8C%EA%B0%9C%ED%95%B4%EC%9A%94-090fb4021e20)). 다만 Shopify의 회고처럼 **경계를 검사한다고 경계가 설계되지는 않는다** ([Shopify](https://shopify.engineering/a-packwerk-retrospective)). 믿집은 이미 이 구조다. 더할 것은 AGENTS.md의 층 표를 `.importlinter` 계약으로 옮기는 일이다. 유일한 예외(`auth.service → vendor.repository`)는 `ignore_imports`에 정확히 한 줄로 적는다. import-linter 2.14부터는 계약이 깨졌을 때 고치는 법을 보여 주는 `broken_contract_guidance`가 있어 한국어 안내를 넣을 수 있다 ([release notes](https://github.com/seddonym/import-linter/blob/HEAD/docs/release_notes.md)). ThoughtWorks는 2026년에 코딩 에이전트가 아키텍처 표류를 빠르게 한다며 결정적 검사를 붙이라고 했다 ([TW Radar](https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms)).

백엔드에서 팀이 정할 갈림길은 두 개다. 하나는 **commit 위치**다. Polar ADR-0003은 서비스에서 `commit()`을 부르지 않고 요청 · 작업 경계에서 한 번 commit한다 ([ADR-0003](https://github.com/polarsource/polar/blob/HEAD/handbook/engineering/decisions/0003-request-scoped-unit-of-work.mdx)). 믿집 AGENTS.md는 `service.py`가 commit하고 그 뒤 큐에 넣는다. 그냥 가져다 쓸 수 없으니 ADR로 정한다. 다른 하나는 **migration 이름**이다. 지금은 `0001`–`0006` 순번이다. 여럿이 동시에 migration을 만들면 번호와 head가 충돌한다. Polar처럼 단일 head 검사를 CI에 먼저 넣는다. 작업 큐 arq는 2025-10부터 유지보수 전용이다 ([arq #510](https://github.com/python-arq/arq/issues/510)). 설계 문서가 이미 SAQ를 탈출구로 적어 두었으니 그대로 둔다.

프론트엔드와 모노레포는 **지금 구조를 유지한다**. Turborepo의 Python 지원은 공식 문서가 '실험적'이라고 적는다 ([Turborepo](https://turborepo.dev/docs/guides/tools/python)). Plane은 pnpm 작업공간에서 Django 앱을 일부러 뺐다 ([Plane](https://raw.githubusercontent.com/makeplane/plane/preview/pnpm-workspace.yaml)). 믿집은 Next 앱 하나와 FastAPI 앱 하나뿐이고, 둘의 연결(OpenAPI → `schema.d.ts`)은 CI가 이미 검사한다. 작업공간 도구는 JS 패키지가 둘 이상 생길 때 다시 본다. 대신 규칙을 몇 개 더한다. `lib/backend/server.ts` 맨 위에 `import 'server-only'`를 넣는다. 지금 `frontend/lib` 아래 어디에도 이 줄이 없다. 넣으면 서버 코드가 브라우저로 새는 순간 빌드가 실패한다 ([Next.js 데이터 보안](https://nextjs.org/docs/app/guides/data-security)). Server Action을 쓰지 않으므로 그것이 주던 CSRF 방어도 없다. Route Handler에서는 CSRF 방어를 직접 해야 한다 ([Next.js 블로그](https://nextjs.org/blog/security-nextjs-server-components-actions)). Server Component 렌더 중에는 쿠키를 설정할 수 없다 ([cookies()](https://nextjs.org/docs/app/api-reference/functions/cookies)). 그래서 로그인 · 로그아웃 · 갱신은 반드시 브라우저 → `/api`로 하고, Server Component는 401을 받으면 로그인으로 보낸다. 화면 폴더는 지금처럼 `components/<area>`를 두되, 한 화면에서만 쓰는 조각은 `app/<route>/_components/`에 두고 두 번째로 쓰일 때 옮긴다. Next 16은 `next lint`를 없앴다 ([Next 16](https://nextjs.org/blog/next-16)). 믿집은 이미 oxlint를 따로 돌린다. oxlint에서 `plugins`를 적으면 기본 플러그인이 덮어써지므로 목록을 전부 적는다 ([oxlint plugins](https://oxc.rs/docs/guide/usage/linter/plugins.html)).

구조 문서는 일곱 개로 끝낸다. README, AGENTS.md(루트 + `backend/` · `frontend/`), 새로 쓸 1–2쪽짜리 `docs/ARCHITECTURE.md`, C4 맥락 · 컨테이너 그림과 배포 그림, ADR과 목록, 상태 기계마다 문서 하나, 실행되는 import 계약이다. matklad는 ARCHITECTURE.md를 짧게, 잘 안 바뀌는 것만, 1년에 몇 번 다시 보라고 한다 ([matklad](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)). C4는 맥락 · 컨테이너 두 장이면 대부분의 팀에 충분하다고 한다 ([c4model.com](https://c4model.com/diagrams)). 견적 흐름 문서(`quote-flow-v3.2.md`)의 ASCII 상태도는 Mermaid `stateDiagram-v2`로 바꾸면 GitHub이 PR 화면에서 그려 준다. 그 아래에 `현재 상태 | 이벤트(API) | 누가(고객 · 업체 · 관리자 · 시간) | 다음 상태 | 남기는 이력 | 알림 · jobs` 전이 표를 두고, 표 한 줄마다 테스트 하나를 만든다. 기존 Python SVG 생성기는 유지한다. 다만 스크립트마다 요소 이름을 손으로 반복하면 그림끼리 어긋난다 ([Simon Brown](https://dev.to/simonbrown/diagrams-as-code-2-0-82k)). 공통 요소 목록을 하나 두거나, CI에서 다시 그려 diff가 있으면 실패시킨다.

## 기록은 한 사실 한 곳에, PR 흐름의 부산물로 남긴다

### 오래 가는 기록은 일하면서 저절로 남는 기록이다

짧은 프로젝트에서 살아남는 기록은 PR 흐름에서 저절로 생기거나, 매주 정해진 자리에서 쓰는 것이다. 부스트캠프 AlgoITNi 팀 위키에는 날짜별 데일리 스크럼 페이지가 **3개**뿐이고, 주간 회고록은 5개, 정기 회의록은 6개다 ([AlgoITNi 위키](https://github.com/boostcampwm2023/web05-AlgoITNi/wiki)). 매일 따로 쓰는 문서는 3일 만에 멈췄다. 코레아 팀은 회고에서 "팀 내 문서 위치 숙지가 부족"하다고 적었다 ([corea 회고록](https://raw.githubusercontent.com/wiki/woowacourse-teams/2024-corea/%ED%9A%8C%EA%B3%A0%EB%A1%9D.md)). GitHub도 Project 안내에서 정보가 어긋나지 않게 **원본을 하나만 두라**고 한다 ([GitHub Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)). 이슈가 닫히거나 PR이 병합되면 Project 항목을 Done으로 옮기는 규칙은 **기본으로 켜져 있다** ([GitHub Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)). 그래서 모든 PR이 `Closes #N`만 지키면 보드는 손대지 않아도 맞는다.

| 무엇 | 유일한 원본 | 누가 · 언제 바꾸나 | 다른 곳에는 |
| --- | --- | --- | --- |
| 할 일 · 버그 · 결정이 필요한 것 | GitHub 이슈 (제목 앞에 요구사항 ID) | 누구나, 생길 때 | 디스코드 · 노션에는 링크만 |
| 지금 누가 무엇을 하나 (작업 상태) | GitHub Project의 Status 필드 | 자동(닫힘 · 병합 → Done). 시작할 때 본인이 In progress | status.md에 담당자 · 진행 중을 적지 않음 |
| 무엇이 실제로 되나 (검증 상태) | `docs/status.md` (제안 → 구현 → 검증 + 확인한 것) | 상태를 바꾸는 그 PR 안에서만 | Project에 증거를 적지 않음 |
| 되돌리기 어려운 결정 | `docs/adr/NNNN-*.md` | 결정 PR | 회의록에는 "→ ADR 0004" 링크만 |
| 아직 열린 결정 | `docs/design/*.md`의 열린 결정 항목 (+ 손댈 때 `decision` 이슈) | 이슈에서 논의 → 결정 PR이 `Closes #N` | — |
| 요구사항 ID 목록 | 요구사항 정의서 (제출물) | 기획 담당 | 이슈 · status · 화면설계서는 ID로만 참조 |
| 주간 진행 요약 | `docs/reports/YYYY-Www.md` 또는 Project 상태 업데이트 (결정 G8) | 주간 회의 서기 | — |
| 회의록 · 회고 | `docs/meetings/` · `docs/retro/` (쓴 뒤 고치지 않음) | 서기 | 결정 → ADR · 이슈, 할 일 → 이슈 |
| 대화 · 알림 · 데일리 | 디스코드 (GitHub 알림 웹훅) | 누구나 | 막힌 것만 이슈 댓글 · `blocked-by` |

현재 AGENTS.md는 "진행 현황은 `docs/status.md` 하나에만 적는다"고 한다. GitHub에 올라가면 이 문장이 Project 보드와 부딪힌다. 노트 둘이 다르게 풀었지만 합치면 답이 나온다. 두 기록은 **다른 사실**을 담는다. Project는 '누가 무엇을 하는 중인가'를, status.md는 '무엇이 증거와 함께 실제로 동작하는가'를 담는다. status.md의 '다음' 표처럼 백로그를 다시 적는 부분은 지우고 Project 보기 링크로 바꾼다. AGENTS.md 문장은 "검증 상태는 `docs/status.md` 하나에만"으로 고친다(결정 G7). 노션은 두 번째 할 일 목록으로 쓰지 않는다. 노션의 GitHub 연동은 GitHub → 노션 한 방향이고 Business 요금제가 필요하다. 옛 연동은 **2026-10-30 뒤로 갱신이 멈춘다** ([Notion Help](https://www.notion.com/help/github)). 디스코드는 웹훅 주소 끝에 `/github`를 붙여 GitHub 이벤트를 바로 받을 수 있다 ([Discord Docs](https://docs.discord.com/developers/resources/webhook)).

### 결정은 세 층으로 나누고, ADR은 한 쪽으로 쓴다

결정 기록은 되돌리기 쉬운지로 나눈다. 아마존의 '한 방향 문 · 양방향 문' 구분이 기준이다 ([Kindel](https://blog.kindel.com/2019/06/27/one-way-and-two-way-doors/)). 되돌리기 쉬운 선택(버튼 순서, 함수 이름)은 PR 본문과 이슈 댓글이면 된다. 아직 탐색 중인 질문은 `docs/design/*.md`의 열린 결정에 둔다. 되돌리기 어려운 것만 `docs/adr/`에 간다. Microsoft도 구조 · 핵심 품질 · 되돌리기 어려운 선택만 ADR로 남기라고 한다 ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)). 판별 질문은 다섯 개다. 2주 뒤에 이것을 바꾸면 다른 사람이 코드 · 데이터 · 문서를 고쳐야 하나? AGENTS.md나 에이전트가 할 수 있는 일을 바꾸나? 외부 서비스 · 공급자 · 유료 API를 고르나? 돈 · 날짜 · 상태 규칙이나 DB 스키마 관례를 바꾸나? PO의 범위 결정인가? 하나라도 '예'면 ADR이다.

설계 문서의 열린 결정에 빠진 것은 **결정할 사람과 기한**이다. Kaplan-Moss는 '결정' 단계가 없는 RFC는 멈추고, 결론이 안 나면 사실상 '안 한다'가 된다고 비판한다 ([Against RFCs](https://jacobian.org/2023/dec/1/against-rfcs/)). DACI는 승인자를 **한 명**만 두고 기한을 적는다 ([Atlassian DACI](https://www.atlassian.com/team-playbook/plays/daci)). 그래서 열린 결정마다 한 줄을 붙인다: `AR4 · 질문 · 안 A/B/C · 결정할 사람 · 기한 YYYY-MM-DD · 상태 열림|보류|결정 · 결과(ADR NNNN 또는 '설계 문서에만')`.

ADR은 PR로 제안하고 병합으로 결정한다. 영국 정부 GDS는 열린 PR을 '제안'으로, main에 들어간 ADR을 '결정'으로 본다 ([GDS Way](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html)). 이 단계를 보이게 하는 것이 중요하다. 2026년 연구에서 ADR 5,800개 중 약 **63%가 처음부터 '결정' 상태로 만들어져** 숙의 과정이 빠졌다 ([ICSA 2026](https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/34/Architecture-Decision-Records-Adoption-Impact-and-Developer-Engagement-in-Open-Sou)). ADR을 쓰는 저장소의 약 절반은 1–5개에서 멈췄다 ([Buchgeher 외](https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/)). 믿집도 전체 5–15개를 예상하고 날카롭게 쓴다. 이미 결정한 ADR을 고쳐도 되는지는 자료가 갈린다. Fowler와 Microsoft는 절대 고치지 말고 새 ADR로 대체하라고 한다 ([Fowler](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html)). Polar는 틀린 글은 그 자리에서 고치고 마음이 바뀔 때만 대체한다 ([Polar ADR 목록](https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/decisions/index.mdx)). 중간안을 권한다. 오타와 설명 보충은 고치고 `고친 날:` 한 줄을 더한다. 동작이 바뀌면 새 ADR을 쓰고 옛 파일 상태를 `대체됨 → NNNN`으로 같은 PR에서 바꾼다. 에이전트를 위해서는 상태를 **각 파일 머리에** 둔다. 에이전트는 목록 파일을 안 읽을 수 있기 때문이다 ([Tian Pan](https://tianpan.co/blog/2026-07-02-the-adr-your-agent-never-read)). 그리고 AGENTS.md에 "결정 ADR은 따르고, 제안은 참고, 대체됨은 역사"라고 적는다 ([Davidson](https://duncandavidson.com/agents-love-decisions)). 에이전트가 쓴 ADR 초안은 '무엇'은 맞아도 '왜'를 지어낼 수 있으니 사람이 맥락 · 결과를 확인한다 ([Vaughan](https://codex.danielvaughan.com/2026/04/28/codex-cli-architecture-decision-records-adr-automated-governance/)).

```markdown
# NNNN. <결정을 한 문장으로>          ← 문제가 아니라 결정을 제목으로

- 상태: 제안 | 결정 | 일부 대체됨 → NNNN | 대체됨 → NNNN | 폐기 | 거부
- 날짜: YYYY-MM-DD
- 결정한 사람: <한 명 또는 역할>
- 바꾸는 것: ADR NNNN의 <어느 부분> | 없음
- 관련: #이슈, PR #번호, docs/design/<file>.md#<ID>

## 맥락        (2~5문장, 현재형, 사실만)
## 결정        (짧은 "-다" 문장. 에이전트가 지킬 규칙은 여기에만)
## 다른 안     (안마다 한 줄: 무엇 + 왜 안 골랐나)
## 결과        (좋은 점 · 나쁜 점 · 고쳐야 할 문서·코드)
## 확인 방법   (선택: 테스트 · lint · 리뷰로 어떻게 지키나)
## 다시 볼 때  (선택: 신뢰도가 낮으면, 이런 일이 생기면 다시 본다)

<!-- docs/adr/README.md 목록 한 줄:
| 번호 | 제목 | 상태 | 날짜 | 결정한 사람 | 대체 관계 | -->
```

이 틀은 지금의 ADR 0001–0003(상태 · 결정한 사람 · 바꾸는 것 · 맥락 · 결정 · 다른 안 · 결과)에 날짜 줄, 관련 링크, 선택 절 두 개만 더한 것이다. MADR 4.0의 최소형 + Nygard와 사실상 같다 ([MADR](https://adr.github.io/madr/), [Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)). 도구는 쓰지 않는다. adr-tools와 log4brains는 오래 멈췄다.

### 이슈와 Project는 무료 조직에서 최소한으로

2025–2026년에 GitHub 이슈가 크게 자랐다. 하위 이슈(부모당 100개, 8단계), issue type, 의존 관계(`blocked-by`)가 정식 기능이 됐다 ([하위 이슈](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)). 2026-07-02에는 Priority · Effort · Start date · Target date 같은 **issue field가 무료 조직까지** 정식 출시됐다 ([GitHub changelog](https://github.blog/changelog/2026-07-02-issue-fields-are-now-generally-available)). issue type은 조직 설정에서 만든다 ([GitHub Docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/configuring-issues/managing-issue-types-in-an-organization)). 개인 계정 저장소에서 쓸 수 있다는 문서는 찾지 못했다. 그래서 저장소를 무료 조직 아래에 둔다. 이슈 폼은 기능 · 버그 · 작업 · 결정 네 개로 끝낸다. `config.yml`에서 `blank_issues_enabled: false`로 빈 이슈를 막고, 파일 이름 앞에 번호를 붙여 순서를 정한다 ([GitHub Docs](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)). 라벨은 커밋 범위와 같은 `area:web · api · calc · agent · worker · db · infra · docs`와 `decision`, `retro-action`, `blocked` 정도만 둔다. 상태는 라벨이 아니라 Project의 Status 필드로, 우선순위는 issue field로 둔다. 이슈 우선순위를 `P1` 라벨로 쓰면 리뷰 댓글의 Pn과 헷갈린다. 주 단위는 iteration 필드로, 발표 · 데모는 milestone으로 둔다. 무료 요금제는 자동 추가 규칙이 **1개**뿐이니 `is:issue,pr is:open` 하나로 저장소 전체를 넣는다 ([GitHub Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically)). 이슈 폼은 문서상 아직 '공개 미리보기'다 ([GitHub Docs](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)).

```yaml
# .github/ISSUE_TEMPLATE/1-feature.yml  (type 줄은 조직에 issue type이 있을 때만)
name: 기능
description: 요구사항 ID가 있는 화면 · API 작업
title: "[FFV-00] "
type: Feature
body:
  - type: input
    id: req
    attributes: { label: 요구사항 ID, placeholder: "FFV-03, FAG-01 (정의서 기준)" }
    validations: { required: true }
  - type: textarea
    id: what
    attributes: { label: 무엇을 · 왜, description: 두세 줄. 설계 문서가 있으면 링크 }
    validations: { required: true }
  - type: textarea
    id: done
    attributes:
      label: 완료 조건 (검증 방법)
      description: 무엇을 돌려서 확인하나요? 예) pytest test_quote.py, 360px 화면에서 버튼 40px
      value: "- [ ] \n- [ ] "
    validations: { required: true }
  - type: textarea
    id: docs
    attributes: { label: 관련 문서 · 결정, placeholder: "docs/design/quote-flow-v3.2.md, ADR 0002" }
---
# .github/ISSUE_TEMPLATE/4-decision.yml
name: 결정 필요
description: 팀이 골라야 하는 것 (design 문서의 열린 결정)
title: "[결정] "
labels: [decision]
body:
  - type: input
    attributes: { label: 결정 번호 · 문서, placeholder: "AR4 · docs/design/app-structure.md" }
    validations: { required: true }
  - type: textarea
    attributes: { label: 선택지와 장단점, value: "A) \nB) " }
    validations: { required: true }
  - type: input
    attributes: { label: 결정할 사람 · 기한, placeholder: "PO · 2026-11-05" }
    validations: { required: true }
  - type: markdown
    attributes: { value: "정해지면 ADR 또는 design 문서를 고치는 PR에서 `Closes #이 이슈`." }
```

버그 폼은 재현 순서 · 기대와 실제 · 환경(브랜치 · 화면 너비 · 브라우저) · 로그(개인정보와 `.env` 값은 지우고)를 받는다. 작업 폼은 할 일과 완료 조건만 받는다.

### 회의와 회고는 매주 한 번, 행동은 셋까지

회고는 행동으로 이어질 때만 쓸모가 있다. Retromat 저자는 회고가 행동 3–8개로 끝났을 때 실천율이 약 60%였다며 **약 3개로 줄이라**고 한다 ([Retromat](https://retromat.org/blog/retrospective-fatigue-how-to-increase-follow-through-on-action-items/)). 학생 회고는 얕아지기 쉽다. 학생 182명, 32팀의 회고 문장 963개를 본 연구에서 결정에 이유를 붙인 것은 **13%**뿐이었다 ([ICSE-SEET 2024](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-education-and-training-track/25/An-Empirical-Study-of-the-Content-and-Quality-of-Sprint-Retrospectives-in-Undergradua)). 그래서 KPT 칸마다 '왜'를 적게 하고, Try는 최대 3개를 이슈로 만든다. 다음 회고는 지난 Try 점검으로 시작한다. 마지막 회고만 4Ls(좋았던 것 · 배운 것 · 부족했던 것 · 바랐던 것)로 해서 발표의 '느낀 점'에 쓴다. 데일리는 디스코드 스레드에 비동기로 쓰고(어제 · 오늘 · 막힌 것 · 컨디션), 저장소 파일은 만들지 않는다. 회의록 · 회고 · 주간 기록은 날짜 이름의 '기록'이다. 쓴 뒤 고치지 않는다. 이슈 댓글처럼 날짜가 박힌 기록은 최신으로 유지할 의무가 없다는 Willison의 구분과 같다 ([Willison](https://simonwillison.net/2022/Nov/26/productivity/)).

```markdown
<!-- docs/meetings/2026-11-02-주간회의.md -->
# 2026-11-02 주간 회의
참석:            서기: (돌아가며)
## 안건
1.
## 정한 것 (이유 한 줄)
- … → ADR 0005 / design 문서 갱신 이슈 #
## 할 일 (모두 이슈로)
- [ ] #   담당   기한
<!-- 규칙: 이슈나 ADR에 없으면 정하지 않은 것이다. -->

<!-- docs/retro/2026-W45-kpt.md -->
# 2026-W45 회고 (KPT)
지난 Try 점검: #52 (지킴 / 못 지킴 — 왜?)
| 이름 | Keep (왜 좋았나) | Problem (왜 문제였나) |
| --- | --- | --- |
## Try (최대 3개, 각각 이슈 · 담당 · 다음 회고까지)
1. … → #

<!-- docs/reports/2026-W45.md (결정 G8에서 이 안을 고른 경우) -->
# 2026-W45 (11/02–11/08) 주간 기록
목표:            상태: 순조 / 위험 / 늦음 — 한 줄 이유
## 끝난 것 (병합된 PR)   ← gh pr list --state merged --search "merged:>=2026-11-02"
## 못 끝낸 것 → 다음 주로
## 정한 것 (ADR · 결정 이슈)
## 다음 주 목표
```

각 문서 첫 줄에 종류를 적는다. `> 살아 있는 문서 · 기준일 YYYY-MM-DD`(README · AGENTS · status · design · architecture)는 현실을 바꾸는 그 PR에서 같이 고친다. `> 기록 · 작성 YYYY-MM-DD · 고치지 않음`(ADR 본문 · 회의록 · 회고 · 주간 기록 · 조사 노트)은 새 기록을 쓰고 옛것을 링크한다. `docs/README.md`에 위의 '무엇을 어디에' 표를 둔다. 발표 직전에는 요구사항 ID → 이슈 → PR 추적표를 `gh` 스크립트로 뽑는다. 문서 링크가 깨지는지는 `lychee --offline`으로 싸게 검사할 수 있다.

## AGENTS.md: 12 KB를 8 KB로, '하지 않는다'는 장치로 막는다

### 짧고 구체적인 파일이 이긴다

지침 파일의 효과는 생각보다 작다. ETH 취리히 연구에서 사람이 쓴 지침 파일은 작업 성공률을 약 2.4% 올렸지만 통계적으로 유의하지 않았다. 비용은 **약 20% 늘었다**. 저장소 개요는 에이전트가 관련 파일을 더 빨리 찾게 하지 못했다. 반면 구체적인 지시는 거의 그대로 따랐다. `uv`를 적으면 에이전트가 작업당 약 1.6번 썼고, 안 적으면 0.01번 미만이었다 ([ETH 연구](https://arxiv.org/abs/2602.11988)). 다른 연구는 AGENTS.md가 실행 시간을 약 29%, 출력 토큰을 약 17% 줄였다고 했다 ([arXiv 2601.20404](https://arxiv.org/abs/2601.20404)). 지시가 많아질수록 지키는 비율은 떨어지고, 앞쪽 지시를 더 잘 지킨다 ([IFScale](https://arxiv.org/abs/2507.11538)). 공급사 안내도 같은 방향이다. Claude Code는 파일을 **200줄 아래**로 두라고 하고, 긴 파일은 준수율을 낮춘다고 한다. 지침은 '맥락'이지 강제 설정이 아니라고도 적는다 ([Claude Code memory](https://code.claude.com/docs/en/memory)). 대문자 강조는 규칙을 과하게 적용하게 만들고, 구조 · 파일 배치 설명은 Claude가 저장소를 직접 읽으니 쓰지 말라고 한다. 그리고 **"매번 일어나야 하는 일은 hook이나 거부 규칙으로 만들라"**고 한다 ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). Codex는 짧고 정확한 파일이 길고 모호한 파일보다 낫다고 하고, 합친 크기 상한은 기본 32 KiB다 ([Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md)). GitHub의 agents.md 2,500개 분석은 명령을 앞에 두고, 경계를 '항상 · 먼저 묻기 · 절대 안 함' 세 단으로 쓰라고 정리했다 ([GitHub 블로그](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)). 오픈소스에서 높게 평가받는 파일은 짧다. uv는 50줄, Kubernetes는 40줄로 명령 · 금지 · 다른 문서 안내가 거의 전부다 ([uv](https://github.com/astral-sh/uv/blob/HEAD/AGENTS.md), [kubernetes](https://github.com/kubernetes/kubernetes/blob/HEAD/AGENTS.md)).

### 지금 파일 진단

현재 `AGENTS.md`는 **140줄, 12,079바이트**다(로컬에서 확인). Codex 기본 한도의 약 37%를 쓴다. 한글은 UTF-8에서 글자당 3바이트라 같은 글자 수의 영어보다 바이트 한도에 2–3배 빨리 닿는다. 줄 수만 보면 GitHub 표본의 AGENTS.md 평균 142줄과 비슷하다 ([MSR 2026](https://arxiv.org/html/2510.21413)). 문제는 길이보다 구성이다. 좋은 점이 많다. ADR > 이 문서 > 습관이라는 우선순위, 바꾼 범위만 돌리는 정확한 명령, '완료는 CI 통과 때만', 보고 세 칸, 돈 · 날짜 · 상태 규칙처럼 코드만 봐서는 모를 규칙이 있다. ETH가 지침 파일에 넣으라고 한 '표준이 아닌 관행'이 바로 이것이다. 약점은 다섯 가지다. 하나, 가장 가치 있는 명령이 맨 끝(§7)에 있다. 둘, 부분 표 · 요청 흐름 설명 · 그림 안내처럼 에이전트가 코드에서 읽을 수 있는 구조 설명이 §2를 채운다. 셋, 백엔드 · 프론트 작성 규칙(§5)이 루트에 섞여 있어 모든 작업에 매번 실린다. 넷, '하지 않는다' 규칙이 §1 · §4 · §5 · §6 · §7에 흩어져 있고, 대부분 막는 장치가 없다. 다섯, 브랜치 · squash · 400줄 · PR 본문 같은 사람용 절차가 있는데, 이것은 저장소 설정과 PR 템플릿이 더 잘 지킨다. 빠진 것도 있다. ADR 상태별 취급, 에이전트 PR 규칙(draft · 공개 · 300줄에서 멈춤), 기록을 고치지 않는다는 규칙이다.

| 현재 절 | 처리 | 옮길 곳 |
| --- | --- | --- |
| 머리말 · 우선순위 · 일괄 수정 금지 | 남김. 우선순위에 'ADR 상태가 결정인 것' 명시 | — |
| §1 제품 흐름 문장 | 한 줄 링크로 줄임 | `docs/design/quote-flow-v3.2.md` |
| §1 ADR 0002 · 업체 승인 · 범위 밖 | 규칙 한 줄씩 남김 | — |
| §1 이름 표 | 그대로 남김 (화면 말과 코드 이름은 추론 불가) | — |
| §2 부분 표 · 요청 흐름 · 미들웨어 순서 | 옮김 | `docs/ARCHITECTURE.md` |
| §2 층 규칙 · 교차 호출 · 예외 하나 · `calc` 순수 | 남김 (import-linter가 생기면 한 줄로 줄임) | `.importlinter` |
| §3 돈 · 날짜 · 상태 | 그대로 남김 (가장 값진 부분) | — |
| §4 에이전트 경계 · 실패 처리 | 남김 | — |
| §4 eval 세트 개수 · 2:1 분할 | 옮김 | `evaluation/README.md` |
| §5 공통 (범위 밖 리팩터링 · 의존성 알림) | '하지 않는 것' · '먼저 묻는 것'으로 합침 | — |
| §5 backend 파일 역할 · 스레드 · 409 · Alembic · DB 제약 | 옮김 (적용된 migration 수정 금지만 루트) | `backend/AGENTS.md` |
| §5 frontend 컴포넌트 · 토큰 · '-해요' · 360px | 옮김 (schema.d.ts 손 수정 금지만 루트) | `frontend/AGENTS.md` |
| §6 브랜치 · squash · 승인 · 400줄 · PR 본문 | 옮김 (커밋 제목 형식 · 에이전트 PR 규칙만 루트) | `CONTRIBUTING.md` · PR 템플릿 · 저장소 설정 |
| §6 `.env` · 요청 시에만 커밋 | '하지 않는 것'으로 | — |
| §7 명령 | **맨 위로** 올림 | — |
| §7 반드시 테스트 · 완료 · 보고 | 남김 | — |
| §7 기록 위치 | '기록' 절로 확장 | — |

중첩 파일에는 Claude Code 함정이 있다. 루트에 `CLAUDE.md`가 있으면 Claude Code는 기본 설정에서 CLAUDE.md만 읽는다. `backend/AGENTS.md`를 만들어도 Claude는 보지 못한다. 그래서 `backend/CLAUDE.md`와 `frontend/CLAUDE.md`에 `@AGENTS.md` 한 줄씩을 같이 둔다 ([Claude Code memory](https://code.claude.com/docs/en/memory)). Windows에서는 심볼릭 링크 대신 이 import 방식이 맞다. 같은 문서가 안내하듯, 팀 커밋 형식이 Claude Code의 내장 git 지시와 부딪히면 `includeGitInstructions`와 `attribution` 설정으로 정리한다 ([Claude Code memory (한국어)](https://code.claude.com/docs/ko/memory)). Next.js 16.3부터는 `create-next-app`과 `next dev`가 AGENTS.md에 자체 블록을 관리한다 ([Next.js AI agents](https://nextjs.org/docs/app/guides/ai-agents)). 루트가 불어나지 않게 이 블록은 `frontend/AGENTS.md`에만 두거나 끈다(결정 G20).

### 글로 쓴 금지는 장치로 막는다

현재 규칙 중 '절대'에 해당하는 것은 지침 파일만으로는 지켜지지 않는다. Claude Code는 `permissions.deny`(예: `Read(./.env)`)가 모든 권한 모드에서 유지된다고 한다 ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). PreToolUse hook은 종료 코드 2로 도구 실행을 막는다 ([hooks guide](https://code.claude.com/docs/en/hooks-guide)). Codex의 기본 sandbox(`workspace-write`)는 `.git`을 읽기 전용으로 두고 네트워크를 끈다 ([Codex security](https://learn.chatgpt.com/docs/agent-approvals-security)). Cursor · Copilot에서 같은 막기가 되는지는 확인하지 못했다. 그래서 AGENTS.md 줄은 장치가 없는 도구를 위한 설명으로 남긴다.

| 규칙 | 지금 | 실제로 막는 장치 |
| --- | --- | --- |
| AI는 요청받을 때만 커밋 · 푸시 | 글 | main ruleset(PR 필수 · force push 금지) + Claude `ask`(`git push`) + Codex 기본 sandbox |
| `.env` 커밋 금지 | `.gitignore` | + 공개 저장소면 push 보호 기본 켜짐, 비공개면 CI 비밀값 검사 + Claude `deny Read(./.env)` |
| `docker compose down -v` 금지 | 글 | Claude `deny` 규칙 |
| `schema.d.ts` 손 수정 금지 | CI 타입 일치 검사 (있음) | + `linguist-generated`, 원하면 PreToolUse hook |
| 적용된 migration 수정 금지 | 글 + 테스트의 up/down | + CODEOWNERS(`backend/migrations/`) + 단일 head 검사 |
| 층 규칙 · 교차 호출 | 글 | import-linter `layers` + `independence` 계약, 예외는 `ignore_imports` 한 줄 |
| 커밋 제목 형식 | 글 | PR 제목 검사 Action (필수 체크) |
| PR 400줄 | 글 | 크기 라벨 Action (경고 · 차단) |
| squash · 승인 1명 · 완료 = CI 통과 | 글 | 저장소 설정 + ruleset 필수 체크 |
| 서버 코드 브라우저 유출 | 없음 | `lib/backend/server.ts`에 `import 'server-only'` |
| AGENTS.md · 지침 파일 변경 | 누구나 | CODEOWNERS + 코드 오너 리뷰 필수 |
| 테스트 삭제 · 건너뛰기 금지 | 글 | 완전 자동화 불가. 리뷰어가 테스트 diff를 먼저 봄 |

```jsonc
// .claude/settings.json (팀 공유용으로 커밋하는 파일, 예시)
// 규칙 문법은 Claude Code 설정 문서로 확인한 뒤 적용한다
{
  "permissions": {
    "deny": ["Read(./.env)", "Bash(docker compose down -v*)"],
    "ask":  ["Bash(git commit *)", "Bash(git push *)"]
  }
}
```

지침 파일은 코드처럼 리뷰한다. Copilot 코드 리뷰는 PR의 **head 브랜치**에 있는 지침을 읽는다 ([GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)). 팀원의 PR이 자기를 리뷰할 지침을 몰래 바꿀 수 있다는 뜻이다. 2025년에는 규칙 파일에 보이지 않는 유니코드로 지시를 숨기는 공격도 보고됐다 ([Pillar Security](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents)). 그래서 지침 파일을 CODEOWNERS에 넣는다. 지침 파일은 추가만 되고 거의 지워지지 않는 경향이 있다 ([arXiv 2511.12884](https://arxiv.org/html/2511.12884)). 유지 규칙은 넷이면 된다. 같은 실수가 두 번 나왔을 때만 줄을 더한다. 장치가 그 규칙을 지키게 되면 줄을 지우거나 한 줄로 줄인다. 다른 문서는 경로로 가리키고 내용을 베끼지 않는다. 고친 뒤에는 Claude `/context`, `/doctor prompt-audit`로 실제로 읽힌 내용과 없는 경로를 확인한다 ([Claude Code memory](https://code.claude.com/docs/en/memory)).

## 별도 절: 줄인 AGENTS.md 초안

아래는 제안이다. 현재 `AGENTS.md`는 고치지 않았다. 규칙의 내용은 현재 파일에서 그대로 가져왔고, 순서와 자리만 바꿨다. 새로 더한 것은 에이전트 PR 규칙, ADR 상태 취급, 기록 규칙, 300줄 멈춤, `revert` 타입이다. 결정 G7 · G13이 정해지면 해당 줄을 맞춘다. 116줄 · 약 8.3 KB로, 지금보다 바이트가 약 30% 적다. 이름 표와 층 블록이 그중 약 25줄이다. 노트가 권한 상한 150줄 안이고 8 KB 목표에 거의 닿는다. import-linter가 층 규칙을 맡게 되면 층 블록을 한 줄로 줄여 100줄 아래로 내려간다.

````markdown
# 믿집 작업 지침

사람과 AI 코딩 도구가 함께 지키는 규칙이다. 코드 · README만 봐서는 알 수 없는 것만 둔다.
실행 방법은 `README.md`, 구조는 `docs/ARCHITECTURE.md`, 결정은 `docs/adr/`(목록 `docs/adr/README.md`),
PR 절차는 `CONTRIBUTING.md`와 PR 템플릿, 개인정보 규칙은 `docs/design/privacy-rules.md`에 있다.
영역별 규칙: `backend/AGENTS.md`, `frontend/AGENTS.md`.

- 우선순위: 상태가 '결정'인 ADR > 이 문서 > 개인 습관. 부딪히면 우회하지 말고 고치기 전에 묻는다.
- 요청과 상관없는 기존 코드를 이 문서에 맞추려고 한꺼번에 고치지 않는다.

## 명령

| 확인할 것 | 명령 |
| --- | --- |
| backend 테스트 | `uv run pytest <대상>` |
| backend 형식 | `uv run ruff check` · `uv run ruff format --check` |
| frontend | `pnpm typecheck` · `pnpm lint` |
| API를 바꿨을 때 | `pnpm gen:api` (→ `lib/backend/schema.d.ts`) |
| migration | `docker compose run --rm migrate` → `alembic check` |
| compose · Caddy | `docker compose config --quiet` · `caddy validate` |

로컬에서는 바꾼 범위만 돌린다. 전체 pytest(실제 PostgreSQL · Redis, migration up → down → up)와 build는 CI가 PR마다 돌린다.

## 하지 않는 것

괄호는 이 규칙을 실제로 막는 장치다. 장치가 없는 도구에서도 같은 규칙을 지킨다.

- 사람이 요청하지 않은 커밋 · 푸시, 커밋 author 바꾸기, `--no-verify` (main 보호 규칙 · 도구 권한)
- `.env` 커밋. 새 환경변수는 `.env.example`에 한국어 주석과 함께 더한다 (.gitignore · 비밀값 검사)
- `docker compose down -v`. DB 볼륨 삭제는 팀원 본인이 정한다 (도구 권한)
- `lib/backend/schema.d.ts`를 손으로 고치기. `pnpm gen:api`로 다시 만든다 (CI 타입 일치 검사)
- 이미 적용된 migration 고치기. 새 revision을 더한다
- 테스트를 지우거나 건너뛰게 하거나 실패를 통과로 바꾸기
- CI에서 유료 LLM 호출(`LLM_LIVE=false` 스텁). 스텁 통과를 에이전트 품질 확인이라고 말하기
- 로그 · 오류 메시지에 입력값 · 개인정보 넣기
- 요청 범위 밖 리팩터링 · 파일 이동 · 일괄 포맷. 구현이 하나뿐인데 interface · base class · factory 만들기
- 범위 밖 기능(바닥 · 욕실 · 전기 공정, 전자계약, 결제)의 자리를 코드에 미리 만들기. 이슈로만 남긴다

## 먼저 묻는 것

- 새 의존성 · 외부 서비스
- DB 스키마 변경, LLM 공급자 변경, 네 번째 에이전트
- 되돌리기 어려운 선택. 코드보다 먼저 `상태: 제안` ADR 초안을 쓰고 사람에게 확인받는다
- 바뀔 줄이 300줄(lock · 생성 파일 제외)을 넘을 것 같을 때. 나누는 안을 먼저 낸다

## 돈 · 날짜 · 상태

- 금액 · 수량 · 기간 · 날짜는 계산 엔진 `calc`만 만든다. 화면 · 에이전트 · 프롬프트에서 계산하지 않는다.
  업체가 적은 줄 금액은 입력값이고 합계 · 부가세는 `calc`가 만든다.
- 금액은 원 단위 정수(`int`, DB `bigint`). 반올림은 `calc` 한 곳에서만. 부가세는 따로 저장하고 화면에 'VAT 별도/포함'.
- 면적은 ㎡(`numeric(7,1)`)와 기준(공급 · 전용)을 함께 저장한다. 평은 표시할 때만. 품은 0.5 단위로 올림.
- 날짜는 서울 기준 `date`, 시각은 `timestamptz`. 공휴일은 데이터로 둔다.
- 견적 줄은 표준 행 키 + 포함 상태 6종(포함 · 묶음 포함 · 따로 계산 · 선택 · 실측 후 · 안 함). 합계에는 '포함' · '따로 계산'만.
- 견적에는 만든 때의 산식 · 단가 버전을 고정한다. 기준 단가는 출처 · 적용일 · 버전과 함께 쌓고,
  수집이 일부라도 실패하면 기존 값을 그대로 둔다.
- 상태는 기능별 service 한 곳에서만 바꾼다: 허용 전이 확인 → 조건부 UPDATE(1행이 아니면 409) → 같은 트랜잭션에 이력 행.
  업체 확정 · 다시 고르기 · 공정표 확정은 사람이 누른 요청으로만 일어난다.
- 가견적서 · 실측 견적서는 업체가 써서 낸다. 믿집은 표준견적서만 계산한다(ADR 0002). 업체 기능은 관리자 승인 뒤에만 열린다.

## 경계

- frontend는 화면만: DB 접근 · LLM 호출 · 금액 계산을 하지 않는다. 쓰기는 브라우저 → 같은 주소 `/api/*`. Server Action은 쓰지 않는다.
- backend 층. 위는 아래를 부를 수 있고 반대는 안 된다. `|`끼리는 서로 import하지 않는다. CI의 import 검사가 기준이다.

  ```
  조립   main.py | worker.py
  흐름   schedule → visit → quote
  대상   account | project | vendor
  기반   files | refprice | jobs  → auth
  도구   agent → calc
  공통   shared → db | queue → config
  ```

- 다른 기능은 그 기능 service의 공개 함수로만 부른다. router끼리 import하지 않는다.
  예외는 하나: `/me`를 위한 `auth.service → vendor.repository` 함수 안 늦은 import.
- `calc`는 DB · HTTP · 시계를 모른다. 오늘 날짜는 인자로 받는다.
- 트랜잭션 안에서 외부 API · LLM을 부르지 않는다. 느린 일은 같은 트랜잭션에 `jobs` 행 → commit 뒤 큐.
- LLM SDK 호출은 `app/agent/llm.py`에서만 한다. 에이전트(FAG-01~03)는 DB에 쓰지 않고 확정 · 저장 권한이 없다.
  출력은 Pydantic으로 검사하고, 숫자가 `calc`와 다르면 버린다. 업체 추천은 후보 목록 밖의 id를 버린다.
- LLM이 실패하면 계산 결과만 보여 주고 "설명을 만들지 못했어요"라고 알린다. 규칙으로 만든 가짜 설명으로 채우지 않는다.
- API 오류는 모두 `{"error": {code, message, fields?}}`.

## 이름 (화면과 코드에서 이것만 쓴다)

| 화면 말 | 코드 이름 | 뜻 |
| --- | --- | --- |
| 표준견적서 | `standard_quote` | 공공 기준 단가로 믿집이 계산한 참고 금액. 업체 견적이 아니다 |
| 가견적 | `quote.kind = estimate` | 실측 전, 업체가 표준 행 양식에 써서 낸 견적 (FFV-03) |
| 실측 견적 | `quote.kind = final` | 업체가 실측하고 써서 낸 견적 (FFV-05) |
| 실측 | `visit` | 업체 방문 측정. 요청 → 확정 → 방문 → 견적 도착 |
| 공정표 | `schedule` | 반나절 단위 작업 순서와 날짜 |
| 기준 단가 | `ref_price` | 표준시장단가 · 시중노임단가 · 조달청 가격 등 공공 기준값 |
| 품 | `man_day` | 기능공 1명 1일 작업량 |
| 공급면적 / 전용면적 | `area_basis = supply / exclusive` | 평형(분양) / 실제 쓰는 면적 |
| 도배 유형: 저가형 / 기본형 | `grade = economy / basic` | 고객이 고르는 도배 등급 |

## 기록

- ADR: '결정'은 따른다. '제안'은 참고만, '대체됨' · '폐기'는 역사다.
- `docs/status.md`(검증 상태): '구현'은 코드가 PR에 있을 때, '검증'은 실제로 돌린 명령과 결과가 PR 본문에 있을 때만 바꾼다.
- 회의록 · 회고 · 주간 기록 · ADR 본문은 고치거나 지우지 않는다. 이슈는 직접 닫지 않는다(PR의 `Closes #N`으로 닫힌다).

## 커밋 · PR

- 제목: `type(범위): 한국어 요약`. type `feat · fix · docs · test · chore · refactor · prompt · eval · revert`,
  범위 `web · api · calc · agent · worker · db · infra`. 예: `feat(api): 가견적 요청 API를 추가한다`
- 프롬프트를 바꾸는 PR은 type `prompt`로 하고 eval 결과를 붙인다. 사용자 동작이 바뀌면 `feat`/`fix`가 우선한다.
- PR은 draft로 열고 템플릿을 채운다. 'AI 사용' 줄을 비우지 않는다. 사람이 diff 전체를 읽은 뒤 ready로 바꾼다.
  에이전트는 병합하지 않는다.

## 완료와 보고

- 완료는 최신 커밋의 필수 CI가 모두 통과했을 때만 말한다. CI를 못 보면 '검증 대기'라고 한다.
- 반드시 테스트할 것: 계산 엔진, 상태 변경과 동시 요청(409), 권한(남의 것 404, 역할이 다르면 403),
  입력 한도(본문 크기, 파일 형식 · 크기), 사진 위치 정보 삭제.
- 보고는 셋으로 나눈다: 로컬에서 돌린 명령과 결과 / CI에 맡긴 것 / 못 한 것과 그 이유.
````

옮겨 갈 내용은 아래처럼 나눈다. 각 파일은 60줄 이하로 둔다.

| 새 파일 | 담을 것 (현재 AGENTS.md에서 옮김) |
| --- | --- |
| `backend/AGENTS.md` (+ `backend/CLAUDE.md`: `@AGENTS.md`) | 기능 패키지 목록, 관리자 API는 각 router의 `/admin/...`, 파일 역할(`router · service · repository · schemas · models · client`), `app/shared/` 기준, 이벤트 루프를 막는 일은 작업 스레드로, 디스크 파일 정리, IntegrityError → 409, Alembic autogenerate는 읽고 고친 뒤 커밋(CHECK는 손으로), DB 제약(UNIQUE · FK · CHECK), JSONB 사용 범위 |
| `frontend/AGENTS.md` (+ `frontend/CLAUDE.md`: `@AGENTS.md`) | Server Component 기본, `"use client"`는 상호작용 잎에만, 데이터는 `lib/api.ts` · `lib/backend/client.ts`로만, `server.ts`는 `server-only`, 영역끼리 import 금지 · barrel 없음, `globals.css` 토큰과 `mj-` 접두어, '-해요'체 · 영어 상태값 숨김, 360px · 40px 확인, Next 관리 블록(G20) |
| `CONTRIBUTING.md` (사람용) | 브랜치 이름, 2일 안 병합, PR 크기 규칙, 리뷰 규칙(Pn · 같은 날 응답 · 승인 1명 돌아가며), 에이전트 PR의 사람 책임 |
| `docs/ARCHITECTURE.md` (새로) | 부분 표, 요청 흐름(읽기 · 쓰기 · API 안 미들웨어 순서 · 느린 일), 코드 지도, 부재로 쓴 불변식, 그림 링크 |
| `evaluation/README.md` | eval 세트(추천 20 · 공정표 15), dev와 held-out 2:1 |

## 정리: 규칙은 충분하다, 남은 일은 옮기는 것이다

이번 조사로 바뀐 판단은 하나다. 믿집에 부족한 것은 규칙이 아니다. 규칙이 **글에만 있다**는 점이 문제다. 현재 AGENTS.md의 '하지 않는다' 열두어 개 가운데 장치가 있는 것은 `.gitignore`와 CI 타입 일치 검사 정도다. 그 CI도 아직 원격에서 돈 적이 없다. 나머지 장치(ruleset · CODEOWNERS · 필수 체크) 대부분은 저장소 요금제가 정해져야 켜진다. 그래서 첫 주의 순서는 정해져 있다. 공개 여부와 조직을 정하고(G1), ruleset · PR 제목 검사 · `ci-ok`를 켜고, 첫 PR에서 squash 메시지와 trailer가 어떻게 남는지 실측한다. AGENTS.md를 줄이는 일은 그 뒤다. 장치가 생긴 규칙부터 한 줄로 줄이면 파일은 저절로 짧아진다.

기록도 같은 논리를 따른다. 학생 팀에서 문서가 죽는 이유는 게을러서가 아니라, 일과 따로 써야 하기 때문이다. 이슈 → 브랜치 → 템플릿 PR → CI → 병합 → 보드 자동 이동의 흐름 위에 기록을 얹으면, 발표 직전에 요구사항 → 이슈 → PR 추적표가 스크립트 한 번으로 나온다. 마지막 주에는 발표 준비가 기록을 밀어낸다는 점도 회고들에서 반복된다. 중간 점검 뒤로는 새 기록 종류를 만들지 않는다.

## 팀이 정할 것

노트마다 붙인 번호(D-a, C1–C8, K1–K6, R-a–R-f)가 프로젝트의 기존 열린 결정 번호(D1–D16, R1–R20, K1–K8)와 겹친다. 그래서 여기서는 **G 번호**로 다시 매기고, 같은 질문은 하나로 합쳤다.

| 번호 | 정할 것 | 선택지 | 권고 | 합친 노트 항목 |
| --- | --- | --- | --- | --- |
| G1 | 저장소 공개 여부 · 요금제 · 소유 | A 공개 + 무료 조직 / B 비공개 + Team 조직(6명 월 $24) / C 비공개 + 개인 Pro(학생 팩 자격 미확인). 비공개 + 무료 조직은 제외 | 부트캠프 규정 · 데이터 라이선스가 허락하면 A, 아니면 B. 어느 쪽이든 조직 아래 | workflow D-a~c, team R-d. ruleset · CODEOWNERS · draft PR · merge queue · Actions 분 · push 보호 · issue type/field · arm64 러너(미확인)가 모두 여기에 달림 |
| G2 | squash 기본 메시지 | PR title / PR title and description | PR title. 첫 AI PR에서 trailer 보존 여부를 실측하고 다시 봄 | commits C4, workflow §8, pr_templates §5 (노트끼리 권고가 엇갈림) |
| G3 | AI 사용 표기 | 기본 trailer 유지 + PR 본문 / `Assisted-by`로 통일 / PR 본문만(Kubernetes식) | author는 사람, PR 본문 'AI 사용' 필수, Claude 기본 trailer 유지 | commits C8, pr_unit D-c, workflow §7 |
| G4 | PR 크기 문턱 | 경고 400 + 차단 800 / 경고만. 에이전트 멈춤선 300 | 경고 400 + 800 차단(리뷰어가 `size-exception`) | pr_unit D-a, D-b |
| G5 | 스택 PR | `gh stack`(공개 미리보기) / 수동 / 안 씀 | 처음엔 안 씀. 큰 기능 하나에서 시험 | pr_unit D-d |
| G6 | 문서 PR 승인 | ADR · AGENTS.md · 회의록 모두 1명 / 회의록 · 회고는 자체 병합 | ADR · 지침 파일은 1명 + CODEOWNERS, 회의록 · 회고는 자체 병합 허용 | pr_unit D-e, team R-b |
| G7 | 진행 기록의 원본 | Project(작업 상태) + status.md(검증 상태)로 역할 분리 / status.md 하나 | 역할 분리. AGENTS.md 문장을 '검증 상태는 status.md 하나'로 | workflow §6, team Q2 |
| G8 | 주간 기록 위치 | `docs/reports/YYYY-Www.md` / Project 상태 업데이트 | `docs/reports/` (에이전트가 읽고 발표 자료로 씀) | team R-a |
| G9 | 회의록 위치 | 저장소 `docs/meetings/` / Discussions · 노션 | 저장소. 결정 · 할 일은 반드시 ADR · 이슈로. 부트캠프 제출 형식이 있으면 그것이 우선 | team R-b |
| G10 | 일정 단위 | iteration + milestone / milestone만 | 둘 다(주 = iteration, 발표 = milestone). 부담되면 milestone만 | team R-c, workflow §6 |
| G11 | 열린 결정 관리 | 결정할 사람 · 기한을 각 design 문서에 / 한 파일에. 기존 항목을 이슈로 한꺼번에 / 손댈 때 | 각 design 문서 안, 손댈 때 `decision` 이슈 | decision K4, team R-f |
| G12 | ADR 운영 | (a) 승인자 (b) 제안 단계를 열린 PR로만 / '제안'으로 병합 (c) 거부안을 파일로 남길지 (d) 결정 ADR 수정: 대체만 / 오류만 고치고 `고친 날:` (e) 머리 형식: 한국어 목록 / YAML (f) 선택 절 · 'AI 초안' 줄 | (a) '결정한 사람' 역할(PO · 기술 리드)을 CODEOWNERS로 (b) 열린 PR로만 (c) 다시 나올 주제만 '거부' 파일 (d) 중간안 (e) 한국어 목록 (f) '확인 방법'만 | decision K1–K6, reference Q6 |
| G13 | 커밋 제목 세부 | 어미 '~한다' / 명사형. scope 필수 여부. `docs` scope. `revert` 추가 · `perf/ci/build` 흡수. 로컬 훅 | '~한다', scope 선택, `docs`는 type만, `revert` 추가, 로컬 훅 없음 | commits C1–C3 · C5, workflow §7 |
| G14 | 변경 기록 · 버전 | CHANGELOG 머리말 영어 6개 / 한국어(추가 · 변경 · 폐기 예정 · 제거 · 수정 · 보안). `v0.N.0 → v1.0.0` / 날짜 태그 | 한국어 머리말, 데모마다 `v0.N.0` pre-release | commits C6, C7 |
| G15 | 트랜잭션 commit 위치 | 지금처럼 service가 commit / Polar ADR-0003처럼 요청 · 작업 경계에서 | ADR로 정함. 흐름 층(schedule → visit → quote) 구현 전에 | backend Q2 · Q6 |
| G16 | migration 파일 이름 | 순번(지금 0001–0006) / 날짜 접두 + 다시 이름 붙이기 | 단일 head 검사는 바로 넣고, 이름은 동시 작업이 늘면 바꿈 | backend Q2 |
| G17 | AI 리뷰어 | Copilot(Student) / `@codex review` / Claude Action / 안 씀 | 하나만. 승인으로 세지 않고 댓글은 기본 P3–P5 | workflow §5 |
| G18 | CI 경로 필터 | 지금 안 함 / `openapi.json`을 커밋하고 paths-filter + `ci-ok` | `ci-ok`는 바로, 경로 필터는 Actions 분이 모자랄 때 | frontend Q4, workflow §3 |
| G19 | 요구사항 정의서 사본 | CSV를 저장소에 둠 / ID만 참조 | ID만 참조 (두 번째 사본 위험) | team R-e |
| G20 | Next.js 관리 AGENTS.md 블록 | 받아들임 / `frontend/AGENTS.md`에만 / `agentRules`로 끔 | `frontend/AGENTS.md`에만 두거나 끔 | frontend Q5 |
| G21 | 리뷰 댓글 표기 | Pn 룰 / Conventional Comments | Pn + `praise:` | workflow §5, pr_templates §2 |

## 확인하지 못한 것

| 항목 | 상태 · 확인 방법 |
| --- | --- |
| squash 커밋 제목 끝에 `(#PR번호)`가 자동으로 붙는지 | 널리 관찰되지만 문서로 확인 못 함. 첫 병합에서 본다 |
| squash 옵션별로 브랜치 커밋의 `Co-authored-by` trailer가 남는지 | 공식 근거 없음. 첫 AI PR에서 실측 (G2 · G3에 영향) |
| 비공개 무료 저장소에서 auto-merge · 대화 해결 필수가 되는지, ruleset 브랜치 이름 제한의 요금제 | 문서에 없음. 저장소 설정 화면에서 확인 |
| SKN34가 학생 개발자 팩(GitHub Pro) 자격이 되는지 | 자격이 '학위 · 졸업장 과정'이라 불분명. 신청하거나 GitHub Education에 문의 |
| **arm64 러너** | 노트에 근거가 없다. 공개 · 비공개에 따라 GitHub 호스티드 arm64 리눅스 러너의 제공과 과금이 다른지 GitHub 문서로 확인해야 한다. 배포 서버 아키텍처도 정해야 한다(ADR 0003은 RDS `db.t4g.micro`만 언급, 현재 CI는 `ubuntu-latest`). G1과 함께 본다 |
| Copilot Student의 월 AI 크레딧(무료 자동 리뷰 횟수) | 요금제 페이지에 없음 |
| GitHub 스택 PR의 정식 출시 여부 | 2026-07-31 기준 공개 미리보기까지만 확인 |
| 한글 브랜치 이름이 macOS · Windows 사이에서 실제로 깨지는지, 'Create a branch'가 한글 제목을 어떻게 바꾸는지 | 근거는 파일 이름 사례뿐. UI에서 직접 확인 |
| commitlint · PR 제목 Action이 한글 제목, 'API'로 시작하는 제목을 어떻게 판정하는지 | 문서 근거 없음. 도입 전에 시험 |
| Claude Code `attribution`의 기본 문자열과 끄는 방식 | 2차 자료끼리 충돌(빈 문자열 / boolean) |
| Cursor · Copilot이 보호 경로 거부 목록을 지원하는지 | 조사하지 않음 |
| GitHub 'Files changed' 합계가 `linguist-generated`를 빼는지 | 확인 못 함. 라벨러는 자체 계산 |
| 한국 기업(토스 · 카카오 · 우아한형제들 · 당근)의 PR 크기 · ADR · 커밋 규칙 원문 | 검색 예산 소진 등으로 찾지 못함. "없다"가 아니라 "못 찾았다" |
| 학생 · 부트캠프 팀을 대상으로 한 연구 | 찾지 못함. 크기 · 길이 · 주기 권고는 모두 업계 · 오픈소스 자료에서 끌어온 것 |
| 부트캠프 규정(공개 저장소 허용, 회의록 제출 형식, 채점자가 보는 도구) | 팀이 과정 운영진에게 확인 (G1 · G9를 덮어쓸 수 있음) |
| Polar가 작업 큐 등록을 commit 뒤로 미루는지, Polar · PostHog 설정을 그대로 복사해도 되는 라이선스인지 | 코드 · 라이선스를 읽지 않음 (아이디어 차용은 문제없음) |
| Next.js rewrites의 스트리밍 · timeout 동작 | 문서 없음. 개발 환경의 챗봇 스트리밍을 직접 시험 |
| oxlint `import` 플러그인이 경로 구역 제한을 지원하는지 | 규칙 단위로 확인 못 함 |
