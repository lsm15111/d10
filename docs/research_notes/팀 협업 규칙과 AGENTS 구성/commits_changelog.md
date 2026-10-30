# 커밋 메시지 · 변경 기록(CHANGELOG) · 릴리스 관행 조사 — 믿집 팀 권고용

> 조사일: 2026-10-29. 각 항목 끝에 출처를 달았다. **[F]** 는 페이지를 직접 열어 확인한 출처, **[S]** 는 검색 결과 요약·스니펫만 본 출처다. 2024년 이전 자료는 "(구자료)"로 표시했다.
> 조사 도중 이 세션의 웹 검색 한도(에이전트 공유 200회)가 소진되어, 후반부는 이미 아는 1차 URL을 직접 여는 방식으로만 보강했다. 한국 대기업(토스·카카오·우아한형제들·당근)의 공개 커밋 규칙 원문은 끝내 찾지 못했다(아래 Gaps 참고).

## 1. Conventional Commits 1.0: 세부 규칙, 2025–2026 채택 현황, Angular/commitlint 기본 설정, 사용자 정의 타입(prompt/eval), scope, breaking 표시

### Takeaway
Conventional Commits는 2026-10 현재도 **1.0.0이 최신 공개 버전**이다. 규격이 정하는 것은 `feat`/`fix`와 breaking 표시(`!` 또는 `BREAKING CHANGE:` footer)뿐이고, 그 밖의 타입(`prompt`, `eval` 포함)은 명시적으로 허용된다. 다만 도구들은 기본값으로 Angular 계열 11개 타입만 알기 때문에, 사용자 정의 타입은 린터·changelog 도구마다 따로 등록해야 한다.

### Cited Findings
**규격 본문 (1.0.0)**
- 형식은 `<type>[optional scope]: <description>` + 빈 줄 + 본문(선택) + 빈 줄 + footer(선택)이다. 규칙 1: "Commits MUST be prefixed with a type". 규칙 4: scope는 괄호 안의 명사이며 선택이다. 규칙 5: 콜론과 공백 바로 뒤에 description이 와야 한다 — [F][Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- 규칙 11~13·16: breaking change는 prefix(`feat(api)!:`)나 footer(`BREAKING CHANGE:`, 대문자 필수, `BREAKING-CHANGE`와 동치) 중 하나로 반드시 표시한다. `!`를 쓰면 footer를 생략할 수 있다 — [F][Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- 규칙 14: "Types other than feat and fix MAY be used". 규칙 15: `BREAKING CHANGE`를 뺀 모든 요소는 대소문자를 구분하지 않는다(일관성만 권장) — [F][Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- 버전 매핑: `fix`→PATCH, `feat`→MINOR, breaking→MAJOR. 그 밖의 타입은 breaking이 아니면 버전에 영향을 주지 않는다 — [F][Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- FAQ:
  - 여러 타입에 걸치는 변경은 "whenever possible" 커밋을 나눈다.
  - squash 워크플로에서는 리드 메인테이너가 머지 메시지를 고칠 수 있으므로 모든 기여자가 규격을 지킬 필요는 없다.
  - 규격에 없는 타입을 쓰면 "tools built on the spec will skip that commit".
  - revert는 규격이 정의하지 않는다. 대신 `revert:` 타입 + `Refs:` footer를 제안한다.
  - 초기 개발 단계에서도 이미 출시된 것처럼 다루라고 한다.
  — [F][Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- 공식 저장소 README는 변경을 `content/next/`에 모은다고만 말한다. 1.1/2.0 같은 새 공개 버전은 보이지 않는다 — [F][conventionalcommits.org repo](https://github.com/conventional-commits/conventionalcommits.org)
- 한국어 번역(`/ko/v1.0.0/`)이 있다. type은 "타입", scope는 "적용 범위", footer는 "꼬리말", BREAKING CHANGE는 "단절적 변경"으로 옮겼다. 버전 메뉴에 `v1.0.0-beta.4` 표기가 남아 있고 오탈자("Sementic", `feet` 예시)도 보인다 — [F][Conventional Commits 한국어](https://www.conventionalcommits.org/ko/v1.0.0/)

**Angular 원조 규칙과 commitlint 기본 설정**
- Angular의 헤더는 `<type>(<scope>): <short summary>`이다. 타입은 build·ci·docs·feat·fix·perf·refactor·test 8개다. summary는 명령형 현재형, 첫 글자 소문자, 마침표 금지다. **본문은 docs를 뺀 모든 타입에서 필수이고 20자 이상**이다. footer에는 `BREAKING CHANGE:`, `DEPRECATED:`, `Fixes #`를 쓴다. revert는 `revert:` + 원 커밋 헤더, 본문에 "This reverts commit <SHA>"와 이유를 적는다. scope는 "changelog 독자가 보는 npm 패키지 이름"이다 — [F][Angular commit-message-guidelines](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md)
- `@commitlint/config-conventional`의 `type-enum`은 build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test(11개)다. 주요 규칙은 다음과 같다 — [F][config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)
  - error: `type-case` 소문자, `subject-case`가 sentence/start/pascal/upper-case이면 안 됨, `subject-full-stop` 금지, `header-max-length` 100, `body-max-line-length`/`footer-max-line-length` 100.
  - warning: `body-leading-blank`, `footer-leading-blank`.
  - URL이 든 줄은 길이 규칙에서 빠진다.
- commitlint 규칙 레퍼런스: `scope-enum`은 목록이 비어 있거나 메시지에 scope가 없으면 항상 통과한다. `scope-case` 기본은 lower-case다. `subject-max-length` 기본은 Infinity다. `signed-off-by`·`trailer-exists` 같은 trailer 규칙도 있다. 레퍼런스 예시의 `header-max-length`는 72인데, config-conventional은 100으로 덮어쓴다 — [F][commitlint rules](https://commitlint.js.org/reference/rules.html)
- 사용자 정의 타입은 `extends: ['@commitlint/config-conventional']` 뒤에 `'type-enum': [2, 'always', [...]]`로 목록 전체를 교체해 등록한다. level 값은 0=끔, 1=경고, 2=에러다. `scope-enum`도 같은 형식이다. `ignores`, `defaultIgnores`(merge·revert·semver 태그 무시), `helpUrl`, `prompt` 옵션이 있다 — [F][commitlint configuration](https://commitlint.js.org/reference/configuration.html)
- commitlint 최신은 **v21.2.4 (2026-10-18)**다. v21.0.0 (2026-05-08)에서 **최소 Node 22**로 올렸다("chore!: minimum node version v22") — [F][commitlint releases](https://github.com/conventional-changelog/commitlint/releases); [S][newreleases commitlint 21.0.0](https://newreleases.io/project/npm/commitlint/release/21.0.0)

**다른 대형 저장소 사례**
- Vue core는 정규식 `/^(revert: )?(feat|fix|docs|dx|style|refactor|perf|test|workflow|build|ci|chore|types|wip)(\(.+\))?: .{1,50}/`로 검사한다. 사용자 정의 타입(`dx`, `workflow`, `types`, `wip`)이 들어 있다. changelog에는 feat·fix·perf와 breaking만 나간다 — [F][vuejs/core commit-convention](https://github.com/vuejs/core/blob/main/.github/commit-convention.md)
- Electron은 PR 제목에 semantic prefix를 **반드시** 붙인다(fix, feat, docs, test, build, ci, perf, refactor, style). 첫 줄은 50자 이하(최대 72), 고유명사 외 소문자다. squash로 머지하므로 PR 제목이 중요하다 — [F][Electron pull-requests.md](https://github.com/electron/electron/blob/main/docs/development/pull-requests.md)
- Blockly는 자체 타입(chore, deprecate, feat, fix, docs, release)을 쓴다. 커밋이 여러 개인 PR은 PR 제목을, 단일 커밋 PR은 그 커밋을 린트한다. squash 시 PR 제목이 커밋 메시지가 된다 — [F][Blockly commits guide](https://docs.blockly.com/guides/contribute/get-started/commits)
- Kubernetes는 Conventional Commits를 쓰지 않는다. 제목을 kind/area 라벨로 시작하는 것만 권한다(예: `etcd: update ...`) — [F][Kubernetes pull-requests.md](https://github.com/kubernetes/community/blob/master/contributors/guide/pull-requests.md)
- Next.js(구자료 스냅샷)도 PR 제목에 `feat:`·`test:` 접두어를 쓰고 `type: next` 같은 라벨을 단다. 공식 규칙 원문은 확인하지 못했다 — [S][github.fr next.js pulls](https://github.fr/vercel/next.js/pulls)

**채택 현황 (2025–2026)**
- Wikipedia가 인용한 Kong et al. 2025: GitHub JS 프로젝트 381개 중 360개(약 94.5%)에 CC 형식 커밋이 하나 이상 있었고, 80% 이상이 CC 형식인 프로젝트는 198개(약 52%)였다. Zeng et al. 2025에 따르면 CC를 채택하지 않은 프로젝트에서도 약 10%의 커밋이 그 형식을 따른다 — [F][Wikipedia: Conventional Commits](https://en.wikipedia.org/wiki/Conventional_Commits_Specification)
- 소규모 2025 연구: 4개 저장소 커밋 1,294건(2025년 2분기)의 CC 준수율은 24.34%에 그쳤다 — [S][Revista GPT (usach)](https://journals.usach.cl/ojs/index.php/revistagpt/en/article/view/7559)
- ICSE 2025 분류 연구는 CC를 10개 범주 분류 과제로 본다 — [S][A First Look at Conventional Commits Classification](https://pure.bit.edu.cn/zh/publications/a-first-look-at-conventional-commits-classification/)

**비판**
- Sumner Evans(2026-06-02)의 주장은 다음과 같다.
  - type 우선·scope 선택 구조는 "exactly backwards"다.
  - type 접두어는 description과 중복되고 글자를 낭비한다.
  - 하나의 변경이 여러 타입에 걸쳐 오분류된다.
  - commit 로그는 개발자용이고 changelog는 사용자용이라 독자가 다르다.
  - 자동 버전 계산은 revert와 숨은 breaking 앞에서 신뢰하기 어렵다.
  - 대안으로 scope 우선의 "Scoped Commits"를 제안한다 — [F][Stop Using Conventional Commits](https://sumnerevans.com/posts/software-engineering/stop-using-conventional-commits/); [F][scopedcommits.com](https://scopedcommits.com/)
- 한국어 2026 비평의 결론은 CC가 "changelog 생성·버전 계산 자동화가 있을 때만 비용을 돌려준다"는 것이다. "본질은 기계가 읽는 커밋 메시지". 소규모 팀이라면 타입을 feat·fix·chore·docs 수준으로 줄이고, 강제 도구는 문화가 자리 잡은 뒤에 얹으라고 권한다 — [F][braindetox: Conventional Commits 비판 2026](https://braindetox.kr/posts/conventional_commits_critique_2026.html)
- 그 밖의 반론:
  - 가시성이 목표라면 커밋보다 PR 제목을 개선하라는 의견(Eclipse Che, 2021, 구자료) — [S][eclipse che-dev](https://www.eclipse.org/lists/che-dev/msg04192.html)
  - HN 사용자 경험담(효과 없음 vs 구조가 있는 편이 낫다) — [S][HN](https://hn.svelte.dev/item/30950377)
  - type보다 scope를 앞에 둬야 한다는 논쟁 — [S][ecosistemastartup](https://ecosistemastartup.com/?p=85841)

### Inferences
- 믿집의 `prompt`·`eval`은 규격상 합법이다(규칙 14). 다만 CC FAQ가 경고하듯 기본 설정의 도구(commitlint config-conventional, semantic-release, release-please 기본 섹션)는 이 타입들을 거부하거나 changelog에서 뺀다. **세 곳에 등록해야 한다**: PR 제목 검사(types 입력), commitlint(쓴다면), changelog 생성기(쓴다면).
- `prompt`와 `feat/fix`는 겹칠 수 있다. 예를 들어 프롬프트를 고쳐 버그를 잡으면 `fix(agent)`인지 `prompt(agent)`인지 갈린다. "프롬프트 텍스트·템플릿만 바뀐 변경 = prompt, 사용자 동작이 바뀌면 feat/fix 우선" 같은 우선순위 규칙을 한 줄 정해 두면 오분류(Evans 비판의 핵심)가 줄어든다.
- scope 목록에 `docs`가 있고 type에도 `docs`가 있어 `docs(docs):`라는 중복 표기가 생긴다. Angular처럼 "문서 내용 변경은 scope 없이 `docs:`"로 정하고, scope `docs`는 문서 사이트·문서 인프라를 뜻하게 하거나 아예 빼는 편이 깔끔하다.
- revert용 타입이 초안에 없다. `git revert`가 만드는 `Revert "..."` 기본 제목은 CC 형식이 아니므로, PR 제목 검사에 `revert` 타입을 추가하거나 예외 처리를 둬야 한다.
- 한국어 description은 `subject-case` 규칙과 충돌할 가능성이 낮다(한글에는 대소문자가 없다). 그러나 "API 응답 ..."처럼 영어 대문자 단어로 시작하면 upper/start-case 판정에 걸릴 수 있다. 도입 전에 `echo "feat(api): API 응답 캐시 추가" | npx commitlint`로 확인할 필요가 있다(아직 검증하지 않음).

### Gaps
- Conventional Commits 1.0.0 정식 공개일(일반적으로 2019년으로 알려짐)은 이번에 1차 출처로 확인하지 못했다.
- commitlint `subject-case`가 한글 subject와 영문 대문자로 시작하는 한글 subject를 실제로 어떻게 판정하는지 공식 문서 근거가 없다. 테스트가 필요하다.
- 2025–2026 대규모 채택 통계(Octoverse 등)는 찾지 못했다. 위 수치는 소규모 학술 표본이다.

## 2. 커밋 메시지 품질 지침(Beams 7원칙·리눅스 커널·Git·tpope) vs PR 제목이 중요한 squash 머지 워크플로, GitHub squash 기본 메시지

### Takeaway
고전 지침들은 다섯 가지로 수렴한다: 짧은 제목(50자 권장, 72자 상한), 명령형, 마침표 없음, 빈 줄로 본문 분리, 본문에는 "무엇·왜". squash 머지에서는 이 품질이 **PR 제목과 PR 본문**으로 옮겨간다. GitHub에서는 저장소 설정을 "Pull request title(…)"로 바꿔야 PR 제목이 실제 커밋 제목이 된다. 기본값 그대로면 단일 커밋 PR은 PR 제목 대신 그 커밋의 메시지를 쓴다.

### Cited Findings
- Chris Beams(2014-08-31, 구자료)의 7원칙은 다음과 같다. "If applied, this commit will ___" 테스트를 제시하고, GitHub이 72자를 넘는 제목을 자른다고 언급한다 — [F][How to Write a Git Commit Message](https://cbea.ms/git-commit/)
  1. 제목과 본문을 빈 줄로 분리한다.
  2. 제목은 50자로 제한한다.
  3. 제목 첫 글자를 대문자로 쓴다.
  4. 제목 끝에 마침표를 찍지 않는다.
  5. 제목은 명령형으로 쓴다.
  6. 본문은 72자에서 줄바꿈한다.
  7. 본문에는 "how"가 아니라 "what·why"를 쓴다.
- tpope(2008-04-19, 구자료): 약 50자 제목, 빈 줄, 72자 줄바꿈, 명령형("Fix bug", "Fixed bug" 아님). 글머리표는 허용한다 — [F][A Note About Git Commit Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
- Git 프로젝트 규칙 — [F][Git SubmittingPatches](https://git-scm.com/docs/SubmittingPatches)
  - 제목은 `area: summary` 형식이고 50자가 soft limit이다. 콜론 뒤 첫 단어는 소문자, 마침표는 쓰지 않는다.
  - 본문에는 현재 코드의 문제(현재형), 정당화, 검토한 대안, 리뷰에서 해소된 우려를 적는다.
  - 외부 링크에 의존하지 않는다. 설명이 너무 길어지면 커밋을 나눠야 한다는 신호로 본다.
  - trailer로 `Co-authored-by:`, `Helped-by:`, `Reported-by:` 등을 쓴다.
- 리눅스 커널 — [F][Linux kernel submitting-patches](https://www.kernel.org/doc/html/latest/process/submitting-patches.html)
  - 제목은 "subsystem: summary phrase"이고 70~75자 이내다.
  - 본문은 문제와 사용자 영향부터 쓰고, 명령형을 쓰며, 75열에서 줄바꿈한다.
  - 패치당 논리적 변경은 하나다. 각 패치 시점에서 빌드·동작해야 한다(bisect 때문).
  - `Fixes: <12자 이상 SHA> ("제목")` 형식과 Link:·Closes: 태그를 쓴다. 리뷰어용 메모는 `---` 아래에 둔다.
- Kubernetes — [F][Kubernetes pull-requests.md](https://github.com/kubernetes/community/blob/master/contributors/guide/pull-requests.md)
  - 50자 이하(72자 초과 금지), 명령형, 첫 단어 대문자, 마침표 금지.
  - 커밋 메시지에 GitHub closing 키워드(fixes #…)나 @멘션을 넣으면 `do-not-merge/invalid-commit-message` 라벨이 붙는다.
  - "sausage" 커밋(리뷰 반영·수정)은 squash하고, 독립적인 "layer" 커밋은 squash하지 않는다.
- GitHub squash 기본 메시지 — [F][GitHub Docs: Configuring commit squashing](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests)
  - 옵션은 4가지다: Default message / Pull request title / Pull request title and commit details / Pull request title and description.
  - Default message는 **커밋 1개인 PR이면 그 커밋의 제목·메시지, 2개 이상이면 PR 제목 + 커밋 목록**을 쓴다.
- 연혁: 2022-05-11에 "Default to PR title for squash merge commits" 옵션이 추가됐다(Settings → Pull Requests → Allow squash merging). 2022-08-23에 PR title+description 등 세부 옵션과 REST API 파라미터(`squash_merge_commit_title`, `squash_merge_commit_message`)가 추가됐다 — [F][GitHub changelog 2022-05-11](https://github.blog/changelog/2022-05-11-default-to-pr-titles-for-squash-merge-commit-messages/); [S][GitHub changelog 2022-08-23](https://github.blog/changelog/2022-08-23-new-options-for-controlling-the-default-commit-message-when-merging-a-pull-request/)
- squash는 짧게 사는 단일 논리 변경 브랜치에 적합하다. 오래 사는 브랜치는 이후 PR에서 이미 해결한 충돌이 다시 생길 수 있다(merge commit이나 rebase 권장). rebase 머지는 GitHub이 committer 정보와 SHA를 항상 새로 만든다 — [F][GitHub Docs: About pull request merges](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges)
- amannn/action-semantic-pull-request README는 "squash & merge" + "Default to PR title for squash merge commits" 조합을 권한다. 단일 커밋 검증(`validateSingleCommit`)은 legacy 옵션으로 분류한다 — [F][action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request)
- release-please도 squash 머지를 "highly" 권장한다. `BEGIN_COMMIT_OVERRIDE`(머지 후 릴리스 노트 수정)는 squash에서만 동작한다 — [F][release-please](https://github.com/googleapis/release-please)
- git-cliff도 PR 하나를 커밋 하나로 매핑하기 위해 squash 머지를 권한다 — [F][git-cliff docs](https://git-cliff.org/docs/)
- CC FAQ: squash 워크플로에서는 메인테이너가 머지 메시지를 정리하므로 일반 기여자의 부담이 없다 — [F][Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- ADR 사례: PR 제목 검사를 필수 CI 게이트로 두고 squash와 결합해 "PR 제목 = main의 단일 커밋"을 만들었다 — [S][RAES ADR 0006](https://raes-environment-packs.readthedocs.io/en/latest/decisions/adrs/0006-conventional-commit-releases.html)

### Inferences
- 믿집 초안의 "squash 머지로 PR 제목이 커밋이 된다"가 성립하려면 저장소 설정을 **"Pull request title" 또는 "Pull request title and description"**으로 명시해야 한다. Default message로 두면 커밋 1개짜리 PR(AI 도구가 한 번에 커밋하는 경우가 흔함)은 PR 제목 대신 브랜치 커밋 메시지가 main에 들어간다.
- "PR title and description"을 고르면 PR 본문이 main 커밋 본문이 된다. PR 템플릿의 체크리스트·스크린샷 마크다운까지 커밋 본문에 섞이므로, 템플릿 맨 위를 "왜/무엇" 2~4줄 요약으로 두거나 "PR title"만 쓰고 맥락은 PR에 남기는 쪽이 낫다. 이것은 팀이 선택할 트레이드오프다.
- 한국어 제목의 길이: 50/72자 기준은 영문(ASCII)을 전제로 한다. 한글은 터미널에서 2열 폭이므로 GitHub·터미널 표시 기준으로 "type(scope): " 포함 약 40~50자(한글 약 30~35자)를 권장선으로 잡는 것이 합리적이다. 이는 추론이며 실측 근거는 없다.
- squash 환경에서도 브랜치 커밋은 리뷰 중 "무엇을 했는지" 기록으로 남는다. 다만 main 이력에는 PR 제목·본문만 남으므로 품질 관리의 무게중심은 PR 제목 리뷰로 옮겨간다.

### Gaps
- GitHub이 squash 머지 때 다른 커밋 작성자를 `Co-authored-by:`로 자동 추가하는지, 그리고 "PR title and description" 옵션에서도 브랜치 커밋의 `Co-authored-by` trailer를 유지하는지 공식 문서로 확인하지 못했다(About merges 페이지에 언급 없음). AI co-author trailer 유지 여부와 직결되므로 실제 저장소에서 테스트해야 한다.
- GitHub UI가 현재 커밋 제목을 몇 자에서 자르는지(Beams 2014년 72자 언급)에 대한 2026년 기준 공식 수치는 없다.

## 3. 강제 도구: commitlint + husky/lefthook, PR 제목 검사 Action, pre-commit 계열 — 소규모 팀에 도움인가 방해인가

### Takeaway
squash 머지 팀에서 강제할 가치가 있는 것은 **PR 제목 하나**다. 서버 쪽 Action(amannn/action-semantic-pull-request v6)으로 PR 제목만 검사하는 방식이 가장 싸고 우회도 어렵다. 로컬 훅(husky/lefthook + commitlint)은 `--no-verify`로 쉽게 우회되고 Node 22+ 의존성이 생기며, squash로 브랜치 커밋이 어차피 사라지므로 학생 팀에는 선택 사항으로 두는 것이 적절하다.

### Cited Findings
- amannn/action-semantic-pull-request — [F][action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request); [F][releases](https://github.com/amannn/action-semantic-pull-request/releases)
  - 검사 대상은 PR 제목이다. `types`(줄 단위 정규식, 기본값은 Commitizen 목록), `scopes`, `requireScope`, `disallowScopes`, `subjectPattern`/`subjectPatternError`, `ignoreLabels`, `wip`, `headerPattern` 옵션이 있다.
  - 권한은 `pull-requests: read`이고, `wip`을 쓸 때만 write가 필요하다. 예시 워크플로는 `pull_request_target`에서 `opened/reopened/edited` 이벤트를 쓰고, 필수 체크로 걸 때는 `synchronize`를 추가하라고 한다.
  - 현재 메이저는 **v6**이다. v6.0.0(2025-08-13)은 Node 24·ESM으로 전환했다. v6.1.0(2025-08-19)은 types 정규식 지원을 추가했다. v6.1.1(2025-08-22)이 최신이다.
- commitlint 로컬 설정(husky v9 방식) — [F][commitlint local setup](https://commitlint.js.org/guides/local-setup.html)
  - `npm i -D husky` → `npx husky init` → `.husky/commit-msg`에 `npx --no -- commitlint --edit $1`을 넣는다. 훅 파일 이름은 반드시 `commit-msg`여야 한다.
  - 문서 스스로 "로컬 훅은 우회될 수 있으니 CI에서도 린트하라"고 권한다.
- commitlint CI 가이드는 PR 범위의 모든 커밋을 `--from base.sha --to head.sha`로 검사한다. PR 제목 검사나 squash는 다루지 않는다 — [F][commitlint CI setup](https://commitlint.js.org/guides/ci-setup.html)
- husky 최신 태그는 v9.1.7이다(페이지에 연도 없음. v9.1.5에서 `pre-merge-commit` 지원) — [F][husky releases](https://github.com/typicode/husky/releases)
- lefthook은 Go로 만든 의존성 없는 단일 바이너리다. npm·pipx·gem·Homebrew·winget으로 설치하고 `lefthook.yml`에 `commit-msg` job을 정의한다. `parallel: true`로 병렬 실행할 수 있다. 최신은 v2.2.2다 — [F][lefthook](https://github.com/evilmartians/lefthook)
- 비교 블로그(2026, 2차 자료): husky는 Node 생태계 설치 기반이 가장 크고, lefthook은 다언어·대형 저장소에 유리하다고 정리한다. "10배 빠름" 같은 수치는 검증되지 않았다 — [S][pkgpulse husky vs lefthook 2026](https://www.pkgpulse.com/guides/husky-vs-lefthook-vs-lint-staged-git-hooks-nodejs-2026)
- Python 진영 — [F][conventional-pre-commit](https://github.com/compilerla/conventional-pre-commit); [F][Commitizen](https://commitizen-tools.github.io/commitizen/)
  - conventional-pre-commit은 pre-commit의 `commit-msg` stage에서 동작한다. 허용 타입을 인자로 받고 `--strict`, `--force-scope`, `--scopes api,client` 옵션이 있다. Python 3.8+이 필요하다.
  - Commitizen(Python)은 `cz commit`으로 대화형 작성을 돕는다. `cz bump`는 SemVer 증가, 태그 생성, Keep a Changelog 형식 changelog 갱신까지 처리한다. 문서 푸터 날짜는 2026-08-20이다.
- 한국 사례: 인포그랩(2023, 구자료)은 husky + commitlint(`commitlint.config.ts`)를 쓴다. `prepare-commit-msg` 훅에서 타입을 입력하면 이모지를 자동으로 붙이고, 브랜치 이름의 이슈 번호를 footer에 넣는다 — [F][GeekNews: Husky·Commitlint로 팀 컨벤션 자동화](https://news.hada.io/topic?id=9394)
- 반대 관점(한국어, 2026): 형식 검사부터 강제하면 "내용 없는 메시지가 늘어난다"고 본다. 커밋 템플릿과 `git commit -v`로 쓰기 쉽게 만들고, 훅은 "이슈 번호 누락처럼 기계가 확실히 판정할 수 있는 항목에만" 쓰며, 본문의 질은 코드 리뷰에서 보라고 권한다 — [F][braindetox: 커밋 메시지는 아직 사람이 쓴다](https://braindetox.kr/posts/commit_message_authorship.html)
- Keep a Changelog 2.0: "Do not make a changelog edit a required check on every change"(CI는 기계적인 부분만 맡긴다) — [F][Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/)
- changesets 문서도 changeset이 없는 기여를 막지 말라고 권한다 — [F][changesets intro](https://github.com/changesets/changesets/blob/main/docs/intro-to-using-changesets.md)
- 커밋 템플릿(`git config commit.template .gitmessage.txt`)으로 규칙을 안내하는 방식은 우테코 8기 프리코스(2025-10) 참가자도 썼다 — [F][velog brokenfinger 우테코 8기](https://velog.io/@brokenfinger/우아한-테크-코스-8기-프리코스-1주차1-git-commit-convention)

### Inferences
- 믿집 구성(squash, PR 제목 = 커밋, AI 도구가 요청 시에만 커밋)에서는 PR 제목 Action 하나로 "main에 들어가는 모든 커밋 제목"이 100% 검사된다. 로컬 commitlint는 브랜치 커밋만 검사하는데, 그 커밋은 squash로 사라지므로 비용 대비 효과가 낮다.
- 이 Action은 `types`/`scopes`를 정규식으로 받는다. `prompt`·`eval`을 그대로 등록할 수 있고 scope 목록도 enum으로 고정할 수 있다. `requireScope: false`를 기본으로 두면 범위가 여러 곳인 PR에서 실랑이가 줄어든다.
- `subjectPattern`으로 "한글로 시작"(예: `^[가-힣]`)을 강제할 수는 있다. 하지만 "API", "OCR" 같은 영문 약어로 시작하는 정당한 제목이 막히므로 경고 수준의 리뷰 관행으로 두는 편이 낫다.
- 비공개 저장소이고 포크 PR이 없다면 `pull_request_target`(포크 대응용이고 보안 주의가 필요함) 대신 `pull_request`로 충분할 가능성이 높다. 이는 추론이며 팀 저장소 구조에 따라 다르다.
- AI 코딩 도구는 로컬 훅이 있으면 훅 실패 시 메시지를 스스로 고치는 경향이 있다. 따라서 훅이 AI 커밋 품질 보조 장치가 될 수도 있다. 반면 `--no-verify` 우회를 막으려면 에이전트 규칙(AGENTS.md)에 금지 문구가 필요하다.

### Gaps
- 소규모 학생 팀에서 강제 도구 도입이 협업 만족도·준수율에 미친 영향을 측정한 연구는 찾지 못했다(의견성 블로그만 있음).
- husky v9.1.7의 정확한 릴리스 연도는 페이지에 표시되지 않았다.

## 4. CHANGELOG와 릴리스: Keep a Changelog 1.1/2.0, release-please, semantic-release, changesets, git-cliff, GitHub 자동 릴리스 노트(.github/release.yml), 앱의 버전 체계(SemVer/CalVer/날짜 태그), 데모·발표용 릴리스 노트

### Takeaway
2026-06-07에 나온 **Keep a Changelog 2.0.0**의 원칙이 이번 결정의 기준점으로 가장 적합하다. 요지는 "Machines can draft, but humans curate", 생성된 changelog는 "raw material at best", 릴리스 노트는 changelog에서 뽑아 쓰고 둘을 따로 유지하지 말 것, 에이전트용 지시문은 AGENTS.md/CLAUDE.md에 둘 것이다. 앱(라이브러리가 아님)이고 일정이 데모 중심이라면 완전 자동(semantic-release)보다 **GitHub 자동 생성 노트나 release-drafter를 초안으로 쓰고, 사람이 다듬은 CHANGELOG.md + 데모마다 annotated tag/GitHub Release**를 두는 조합이 비용 대비 효과가 가장 크다.

### Cited Findings
**Keep a Changelog**
- 1.1.0(2019-02-15): 원칙은 "Changelogs are for humans, not machines", 최신 버전이 위, 버전·섹션 링크, 날짜는 ISO 8601이다. 변경 유형은 6개(Added·Changed·Deprecated·Removed·Fixed·Security)이고 맨 위에 `Unreleased` 섹션을 둔다. 철회된 릴리스는 `[YANKED]`로 표시한다. "Using commit log diffs as changelogs is a bad idea". 한국어 번역이 있다 — [F][Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/); [S][Keep a Changelog 한국어 1.0.0](https://keepachangelog.com/ko/1.0.0)
- **2.0.0(2026-06-07)** — [F][Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/)
  - 형식은 그대로("breaks the guidance, not the format")이고 6개 유형도 유지된다("There are only six types on purpose"). Dependencies와 Known issues는 유형이 아니다.
  - breaking은 해당 유형 안에서 `**Breaking:**` 표시로 적는다(예: "- **Breaking:** parse() now returns a result object instead of raising"). Security 항목은 CVE로 시작한다.
  - "You do not have to use Semantic Versioning … Calendar versioning, a plain number, or a date all work"(어떤 체계를 쓰는지만 밝히면 된다). 버전 머리말에 짧은 요약을 둘 수 있다(선택).
  - 릴리스 노트: "Keep the changelog as the record, and write the release notes from it rather than maintaining two". 호스트가 생성한 노트는 호스트 DB에 갇힌다("the convenience is the hook").
  - 자동화·AI: "Machines can draft, but humans curate", "A generated changelog is raw material at best". 코딩 에이전트를 쓰면 "record that brief where they read it, for example an AGENTS.md or CLAUDE.md file". brief는 사용자 관점의 주목할 변경만, 6개 유형으로 분류하고, breaking을 표시하라는 내용이다.
  - commit과 changelog 항목은 "written for different people, and one does not convert cleanly into the other".
  - 번역본은 "out of date until they catch up"이다. 한국어 번역은 아직 1.x 기준이다.
- Common Changelog(더 엄격한 하위 규격): Unreleased 섹션이 없고, 유형은 Changed·Added·Removed·Fixed 순서이며, 항목마다 커밋·PR 링크와 작성자를 붙인다. breaking은 `**Breaking:**` 접두어로 맨 앞에 두고 명령형으로 쓴다. "Don't take the easy way out with full automation"(changelog 작성 자체가 버전 번호를 검토하는 단계라는 논리) — [F][Common Changelog](https://common-changelog.org/)
- GitLab은 커밋 trailer `Changelog: added|fixed|changed|…`로 CHANGELOG를 생성한다. 다중 커밋 MR은 첫 커밋에 trailer를 단다(squash 대비). 사용자 관점 결과를 쓰고("Fix 500 errors caused by …" 식), 리팩터링·테스트·문서 전용 변경은 제외한다 — [F][GitLab changelog entries](https://docs.gitlab.com/development/changelog/)

**생성 도구**
- **release-please**(googleapis) — [F][release-please](https://github.com/googleapis/release-please); [F][releases](https://github.com/googleapis/release-please/releases); [F][customizing.md](https://github.com/googleapis/release-please/blob/main/docs/customizing.md)
  - Conventional Commits를 파싱해 "Release PR"을 계속 갱신한다. 그 PR을 머지하면 CHANGELOG.md·버전 파일 갱신, 태그, GitHub Release가 만들어진다. 패키지 배포는 하지 않는다.
  - `Release-As: x.y.z` footer로 버전을 강제할 수 있다. 릴리스 단위는 feat·fix·deps다. `simple` 타입은 version.txt + CHANGELOG.md를 쓴다.
  - 최신은 **v17.11.2(2026-08-24)**다.
- release-please-action은 **v4**다. 권한은 `contents/issues/pull-requests: write`이고 "Allow GitHub Actions to create and approve pull requests"를 켜야 할 수 있다. **GITHUB_TOKEN으로 만든 PR·릴리스는 다른 워크플로를 트리거하지 않으므로** 릴리스 PR에서 CI를 돌리려면 PAT가 필요하다 — [F][release-please-action](https://github.com/googleapis/release-please-action)
- changelog 섹션 사용자화(`changelog-sections`의 type/section/hidden)는 공식 customizing 문서에 없었다. 커뮤니티 예시만 확인했다 — [S][dev.to: automate release notes](https://dev.to/sofiama/automate-release-notes-aka-changelog-gcn); [S][Flagsmith release-please-config](https://fr.github.com/Flagsmith/flagsmith/blob/main/release-please-config.json)
- **semantic-release** — [F][semantic-release](https://github.com/semantic-release/semantic-release); [F][releases](https://github.com/semantic-release/semantic-release/releases)
  - 릴리스 브랜치 push마다 CI가 다음 버전 계산·노트·태그·배포를 사람 개입 없이 처리한다. 기본은 Angular 규약이다. README는 전부 "package" 배포 관점으로 쓰여 있다.
  - 2026-10 현재 v26.0.0-beta.5(2026-10-24)이고, v26은 Node ^22.22.2 또는 >=24.15를 요구한다.
- **changesets** — [F][changesets](https://github.com/changesets/changesets); [F][intro](https://github.com/changesets/changesets/blob/main/docs/intro-to-using-changesets.md)
  - 기여자가 bump 종류와 요약을 담은 `.changeset` 파일을 PR에 함께 넣는다. `changeset version`이 버전·changelog를 만들고 `changeset publish`가 npm에 배포한다. 모노레포·패키지 중심이다.
  - main 브랜치는 v3 개발 중이고 v2는 유지보수 브랜치다.
- **git-cliff** — [F][git-cliff docs](https://git-cliff.org/docs/); [F][git-cliff git config](https://git-cliff.org/docs/configuration/git)
  - v2.14.0이다. `cliff.toml`의 `commit_parsers` 정규식으로 그룹을 매핑하므로 `{ message = "^prompt", group = "Prompts" }`처럼 사용자 정의 타입을 쉽게 추가한다.
  - `filter_unconventional`, `protect_breaking_commits`, `commit_preprocessors`를 지원하고 PR 제목·번호·작성자 등 원격 메타데이터를 쓸 수 있다.
- **release-drafter v7**은 PR이 머지될 때마다 초안 릴리스를 갱신한다. 라벨, **conventional commit 제목**, 변경 파일 경로로 분류할 수 있다. autolabeler가 브랜치·제목·본문 정규식으로 라벨을 단다. 라벨로 다음 버전을 정하고 `$CHANGES`, `$CONTRIBUTORS`, `$NEXT_MINOR_VERSION` 같은 템플릿 변수를 쓴다 — [F][release-drafter](https://github.com/release-drafter/release-drafter)
- **GitHub 자동 생성 릴리스 노트** — [F][GitHub Docs: Automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
  - 릴리스 화면에서 "Generate release notes"를 누르면 머지된 PR 목록, 기여자, 전체 비교 링크가 채워진다.
  - `.github/release.yml`의 `changelog.exclude.labels/authors`와 `categories[].title/labels`(와일드카드 `"*"`)로 분류한다. 분류는 **라벨 기반**이다.
  - 문서는 게시 전에 "include all (and only) the information you want"를 검토하라고 한다.
- actions/labeler는 변경 경로 glob이나 브랜치 이름으로 PR에 라벨을 자동으로 단다(`.github/labeler.yml`, 예시는 v6, 최신 v7은 ESM). 권한은 `pull-requests: write`이고 라벨 생성에는 `issues: write`가 필요하다 — [F][actions/labeler](https://github.com/actions/labeler)
- GitHub Releases는 Git 태그 기반이고 노트·자산(최대 1,000개, 각 2 GiB 미만)·소스 아카이브를 담는다. write 권한자만 관리할 수 있다 — [F][GitHub Docs: About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- **Immutable releases**가 2025-10-28 GA됐다. 켜면 새 릴리스의 자산·태그를 삭제하거나 이동할 수 없다. 기존 릴리스는 재게시 전까지 변경 가능하다. 저장소 전체에 일괄 적용(all-or-nothing)되어 롤링 태그(nightly)와 충돌한다(GoReleaser 사례) — [S][GitHub changelog: immutable releases GA](https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/); [S][GitHub Docs: immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases); [S][GoReleaser: immutable releases](https://goreleaser.com/blog/immutable-releases/); [S][community discussion #178351](https://github.com/orgs/community/discussions/178351)
- Git 태그: "Annotated tags are meant for release while lightweight tags are meant for private or temporary object labels". `git describe`는 lightweight 태그를 기본으로 무시한다. `git tag -a v1.0 -m "…"`로 만든다 — [F][git-tag](https://git-scm.com/docs/git-tag)

**버전 체계 (앱 기준)**
- SemVer 2.0.0 — [F][semver.org](https://semver.org/)
  - **선언된 public API가 전제**다. 0.y.z는 초기 개발 단계이고 "Anything MAY change at any time"이다.
  - FAQ: "If your software is being used in production, it should probably already be 1.0.0". "v1.2.3 is not a semantic version"(v는 태그 접두어일 뿐이다).
  - pre-release는 `-alpha.1`, 빌드 메타데이터는 `+…` 형식이다.
- CalVer: `YYYY`/`YY`/`0M`/`0D`/`MICRO`/`MODIFIER`를 조합한다(`MM`·`DD` 표기는 폐기됐다). 예: Ubuntu `YY.0M`, pip `YY.MINOR.MICRO`, yt-dlp `YYYY.0M.0D[.MICRO]`. 범위가 크고 계속 바뀌거나, 시간에 민감하거나, 비기술 독자를 상대하는 프로젝트에 적합하다. breaking 신호가 없으므로 changelog와 기한부 폐기 정책을 함께 둘 것을 권한다 — [F][calver.org](https://calver.org/)
- SensioLabs(2025-01-31): 라이브러리는 SemVer, **애플리케이션·플랫폼은 CalVer**(예: `2024.2.0`), 혼합안(앱은 날짜, 재사용 컴포넌트는 SemVer)을 권한다 — [F][SensioLabs SemVer vs CalVer](https://sensiolabs.com/blog/2025/semantic-vs-calendar-versioning)
- Frontside(2022, 구자료): 웹·모바일 앱은 사용자가 버전 번호를 거의 보지 않는다. 외부 일정이 없으면 SemVer가 개발자에게 더 단순하다. 어떤 체계든 명시하고 문서화해 일관되게 쓰는 것이 핵심이다 — [F][Frontside: SemVer or CalVer by project type](https://frontside.com/blog/2022-02-09-semver-or-calver-by-project-type/)
- Gramps Web은 웹 API는 CalVer, 백엔드는 SemVer로 섞어 쓴다 — [S][gramps-web discussion #286](https://github.com/gramps-project/gramps-web/discussions/286). 버전 체계 일반론 — [S][fale.io versioning](https://fale.io/blog/2024/07/31/on-software-versioning-schema); [S][aboutcode software versioning](https://aboutcode.org/blog/software-versioning/)
- ZeroVer(풍자, 2018): Neovim·React Native·FastAPI·Zig처럼 성숙한 도구도 오랫동안 0.x에 머문다. 버전 번호가 성숙도를 말해 주지 않는다는 풍자다 — [F][0ver.org](https://0ver.org/)

**릴리스 노트 작성 지침 (데모·발표용 참고)**
- Kubernetes — [F][Kubernetes release-notes guide](https://github.com/kubernetes/community/blob/master/contributors/guide/release-notes.md)
  - 사용자나 운영자가 볼 수 있는 변경만 노트를 쓴다. 테스트·빌드 인프라·미출시 버그 수정은 제외하고, 그런 PR은 `NONE`이라고 적는다.
  - 과거형, 문장 첫 글자 대문자, Markdown 링크를 쓴다. 무엇이 추가·변경·수정·제거됐는지와 영향받는 기능을 명시한다.
  - 사용자 조치가 필요하면 "action required"를 넣는다.
- Electron PR 템플릿은 `Notes:` 한 줄에 앱 개발자 관점으로 "capitalized, punctuated, past tense, and no longer than 80 characters"라고 쓰게 한다 — [F][Electron PR template](https://github.com/electron/electron/blob/main/.github/PULL_REQUEST_TEMPLATE.md)
- 일반 가이드(한국어): 릴리스 노트에는 새 기능·변경·버그 수정·API 변경·보안을 담는다 — [S][ClickUp 릴리스 노트 작성법](https://clickup.com/ko/blog/128870/how-to-write-release-notes). Azure SDK 한국어 정책은 릴리스마다 자동 PR이 생성되고 엔지니어링 리드가 검토한다(스니펫만 확인, 원문은 404) — [S][Azure SDK 한국어 릴리스 노트](https://azure.github.io/azure-sdk-korean/policies_releasenotes.html)
- 한국어 위키독스 장("릴리즈 노트와 CHANGELOG 자동화"): 릴리스 노트 생성 프롬프트를 `.github/prompts/release-notes.md` 같은 별도 파일로 관리해 PR로 개선하라고 한다. 원문은 403이라 스니펫만 확인했다 — [S][wikidocs 443811](https://wikidocs.net/443811)
- release-please 도입 사례(Theodo, 2022, 구자료): Terraform 모듈 태그·changelog 작성 부담 때문에 도입했다 — [S][Theodo release-please](https://cloud.theodo.com/en/blog/release-please)

### Inferences
- **semantic-release는 부적합하다.** 패키지 배포 중심이고, 사람이 버전을 정하지 않으며, Node 22+ CI 설정이 필요하다. 데모 일정에 맞춰 "이번 릴리스를 언제 끊을지"를 사람이 정해야 하는 믿집에는 맞지 않는다.
- **release-please는 가능하지만 과하다.** Release PR이 늘 하나 열려 있어야 하고, 사용자 정의 타입 섹션 설정(prompt/eval)과 GITHUB_TOKEN 트리거 제약(PAT 필요)이 따른다. 기본 섹션 제목도 영어다. 출시 후 운영 단계로 넘어가면 재검토할 만하다.
- **changesets는 npm 패키지·모노레포용이라 해당 없음**에 가깝다.
- **현실적인 조합(제안):**
  - (a) PR 제목이 이미 `type(scope): 한국어 요약`이므로 GitHub 자동 생성 노트만으로도 "머지된 PR 목록 + 기여자"가 한국어로 나온다.
  - (b) 유형별 분류가 필요하면 `.github/release.yml` 카테고리를 쓴다. 이때는 라벨이 필요하므로 release-drafter autolabeler(제목 정규식 `^feat` → `type:feat`)나 actions/labeler(경로 → `scope:web` 등)로 라벨을 자동으로 단다.
  - (c) 데모 직전에 사람(또는 AGENTS.md brief를 받은 AI)이 그 초안을 CHANGELOG.md의 해당 버전 섹션으로 다듬고, GitHub Release 본문은 CHANGELOG에서 옮긴다(KaC 2.0 "둘을 따로 유지하지 말 것").
- **버전 체계:** 믿집은 외부가 의존하는 public API가 없는 앱이므로 SemVer의 MAJOR/MINOR 의미는 약하다. 다만 "0.x = 공개 전, 1.0.0 = 실제 출시"라는 상징성은 발표·출시 스토리텔링에 유용하다. SemVer FAQ도 "production이면 1.0.0"이라고 한다. 선택지는 아래 §7 결정 항목에 정리했다.
- 데모용 GitHub Release는 pre-release로 표시해 "출시본"과 구분하는 것이 자연스럽다. Immutable releases는 학생 팀이 태그를 잘못 찍었을 때 되돌릴 수 없게 만들 수 있으므로 출시 전까지는 켜지 않는 것이 안전하다. 이는 추론이다.
- 데모 릴리스 노트는 commit/PR 목록이 아니라 청중(심사위원·사용자) 관점의 짧은 요약이어야 한다(KaC·Common Changelog·Kubernetes·GitLab 공통). PR 목록은 접힌 "전체 변경" 링크로만 남기는 구성이 적합하다.

### Gaps
- release-please의 `changelog-sections`(사용자 정의 타입·hidden)와 `bump-minor-pre-major` 같은 0.x 단계 옵션은 공식 문서로 확인하지 못했다(customizing.md에 없음. manifest 문서나 schema 확인 필요).
- git-cliff 정규식 엔진의 한글(유니코드) 처리 여부를 문서로 확인하지 못했다(Rust regex는 일반적으로 유니코드를 지원하지만 검증하지 않았다).
- GitHub 자동 생성 노트가 라벨 없이 PR 제목 접두어로 분류하는 기능은 문서에 없다(라벨 전용으로 보인다).
- "데모·발표용 릴리스 노트"를 직접 다룬 1차 자료는 찾지 못했다. 위 권고는 일반 릴리스 노트 지침에서 추론한 것이다.

## 5. AI 보조 커밋: Co-authored-by trailer, 2025–2026 공개(disclosure) 규범, AI 생성 커밋 메시지의 위험

### Takeaway
2026년의 주류 규범은 두 가지다. 첫째, "AI 사용은 허용하되 사람이 저자로서 전적으로 책임지고 공개한다"(Fedora·LLVM·Linux·Ghostty·SSW). 둘째, **공개 방식은 프로젝트마다 크게 다르다.** `Co-authored-by`/`Assisted-by` trailer를 권하는 곳(Fedora·LLVM·Linux·SSW)이 있는가 하면, AI co-author trailer와 AI가 쓴 커밋 메시지를 금지하고 PR 본문에 공개하게 하는 곳(Kubernetes)도 있다. AI 생성 메시지의 핵심 위험은 diff 요약은 잘하지만 "왜"를 지어내거나 빠뜨린다는 점이다.

### Cited Findings
**도구별 기본 동작**
- Claude Code — [F][Claude Code settings-reference index](https://code.claude.com/docs/en/settings-reference); [S][ClaudeLog attribution](https://claudelog.com/faqs/attribution-setting-claude-code/); [F][DeployHQ: Claude Code Co-Authored-By](https://www.deployhq.com/blog/how-to-use-git-with-claude-code-understanding-the-co-authored-by-attribution); [S][zenn: attribution](https://zenn.dev/dk_/articles/8e4726b71f7803?locale=en); [S][wmedia: remove co-authored-by](https://wmedia.es/en/tips/claude-code-remove-co-authored-by-claude)
  - 공식 설정 색인에 `attribution`(커밋·PR attribution 사용자화), `attribution.commit`("Change or hide the trailer Claude Code adds to commits"), `attribution.pr`, `attribution.sessionUrl`이 있다. `includeCoAuthoredBy`는 "Deprecated; use attribution"이다.
  - 2차 자료에 따르면 기본값은 커밋에 `Co-Authored-By: Claude <noreply@anthropic.com>`, PR에 "Generated with [Claude Code]" 문구다. 빈 문자열(`"commit": ""`)로 숨긴다는 설명과 boolean(`commits`/`pullRequests`, v2.0.62)이라는 설명이 엇갈린다.
  - 설정을 꺼도 모델이 직접 trailer를 쓸 수 있어 CLAUDE.md 규칙을 이중으로 두라는 팁도 있다.
- (관찰) 이 조사 세션 자체의 Claude Code 환경은 커밋 끝에 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, PR 본문 끝에 `🤖 Generated with [Claude Code](https://claude.com/claude-code)`를 붙이도록 지시받고 있다. 즉 현재 trailer에는 모델명이 들어간다. 웹 출처가 아니라 세션 시스템 지시에서 관찰한 사실이다.
- noreply 주소는 실제 GitHub 계정에 연결되지 않으므로 사용자의 기여 그래프에는 영향이 없다(2차 자료) — [F][DeployHQ](https://www.deployhq.com/blog/how-to-use-git-with-claude-code-understanding-the-co-authored-by-attribution)
- GitHub Copilot coding agent의 커밋은 **Copilot이 author, 작업을 맡긴 사람이 co-author**다. 2026-03-20부터 세션 로그 링크 `Agent-Logs-Url` trailer가 붙는다 — [F][GitHub changelog 2026-03-20](https://github.blog/changelog/2026-03-20-trace-any-copilot-coding-agent-commit-to-its-session-logs)
- Copilot PR을 squash 머지하면 마지막 커밋 author인 Copilot이 main 커밋 author가 되어 blame과 기여 이력이 왜곡된다는 보고가 있다 — [S][community discussion #179983](https://github.com/orgs/community/discussions/179983)
- CPython CLA 봇은 git `Author:` 필드만 보고 `Co-authored-by:`는 무시한다. 에이전트 bot이 author인 커밋은 CLA 검사에서 막힌다. 해결책은 author를 사람으로 고치는 force-push나 에이전트 git name/email 설정이다. "Claude Code on the web"의 기본 author 주소도 같은 문제를 일으킨다. 같은 스레드에서 AI용 Co-authored-by는 "authorship보다 marketing"이라는 의견도 나왔다(2026-03-22~) — [F][discuss.python.org: CLA bot and AI agents](https://discuss.python.org/t/cla-bot-and-ai-agents/106635)
- VS Code — [S][penligent: VS Code Copilot co-author](https://www.penligent.ai/hackinglabs/ko/?p=5124); [F][heise 2026-05-03](https://heise.de/-11279554)
  - v1.110에서 `git.addAICoAuthor`가 기본 off로 추가됐고, 2026-04-16 PR로 기본 활성화로 바뀌었다.
  - heise 테스트(v1.118)에서는 기본값이 `chatAndAgent`였고 trailer는 `Co-authored-by: Copilot <copilot@github.com>`이었다.
  - 동의 없는 표기, 쓰지도 않았는데 표기되는 문제로 반발이 일었다. 끄려면 `"git.addAICoAuthor": "off"`로 설정한다.
- 그 밖의 trailer 도구: Pi 확장은 `Co-Authored-By`(모델)와 `Generated-By`(도구 버전)를 함께 단다. madeby는 Co-Authored-By·Generated-by·Assisted-by trailer를 AI 공개 신호로 집계한다 — [S][pi-co-authored-by](https://cdn.jsdelivr.net/gh/bruno-garcia/pi-co-authored-by@main/README.md); [S][madeby](https://socket.dev/npm/package/madeby)
- GitHub co-author 표기법: `Co-authored-by: name <email>`를 한 줄에 하나씩 쓴다. 기여로 집계하려면 GitHub 계정에 연결된 이메일(또는 noreply)을 써야 한다. 빈 줄 개수(1줄 vs 2줄)에 대한 문서 불일치가 이슈로 보고돼 있다. 기능 자체는 2017-01 도입이다(구자료) — [S][GitHub Docs: commit with multiple authors](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors); [S][github/docs issue #36812](https://github.com/github/docs/issues/36812); [S][GitHub blog 2017](https://github.blog/2017-01-10-commit-together-with-co-authors)
- git trailer 형식은 메시지 끝의 `key: value` 블록이다. 앞에 빈 줄이 있어야 한다. key는 ASCII 영숫자와 하이픈만 쓴다. `git interpret-trailers`나 `git commit --trailer`로 추가한다 — [F][git-interpret-trailers](https://git-scm.com/docs/git-interpret-trailers)

**프로젝트 정책 (2024–2026)**
- Linux kernel: `Assisted-by: LLM [TOOL1] [TOOL2]`(예: `Assisted-by: LLM coccinelle sparse`). "AI agents MUST NOT add Signed-off-by tags". 사람이 검토·라이선스·책임을 진다. submitting-patches는 Assisted-by를 빠뜨리면 "may impede the acceptance"라고 쓴다 — [F][kernel coding-assistants](https://www.kernel.org/doc/html/latest/process/coding-assistants.html); [F][submitting-patches](https://www.kernel.org/doc/html/latest/process/submitting-patches.html)
- Git 프로젝트: DCO 충족 여부가 불분명하다. **AI가 쓴 것처럼 보이는 패치·커밋 메시지·문서, 장황하고 과하게 격식적인 "AI slop", 제출자가 설명하지 못하는 내용은 거절**한다 — [F][Git SubmittingPatches](https://git-scm.com/docs/SubmittingPatches)
- Kubernetes(AI Guidance): AI 사용은 PR 본문에 공개한다("This PR was written in part with the assistance of generative AI" 정도면 충분). **AI를 co-author로 올리거나 AI로 co-sign하거나 `assisted-by`/`co-developed` trailer를 쓰는 것은 금지**다. 대형 AI 생성 PR과 **AI가 쓴 커밋 메시지도 금지**다. 리뷰 답변을 AI에 의존해서도 안 된다 — [F][Kubernetes pull-requests.md](https://github.com/kubernetes/community/blob/master/contributors/guide/pull-requests.md)
- LLVM: 사람이 먼저 전부 읽고 검토해야 한다. 상당 부분이 도구로 생성됐으면 PR 본문·커밋 메시지 등에 표시한다(예: `Assisted-by:`). 사람 승인 없이 프로젝트 공간에서 움직이는 에이전트(예: GitHub `@claude`)는 금지다. "extractive" 기여 개념을 두고, good first issue에는 AI를 금지한다 — [F][LLVM AI Tool Use Policy](https://llvm.org/docs/AIToolPolicy.html); [S][LLVM RFC](https://discourse.llvm.org/t/rfc-llvm-ai-tool-policy-human-in-the-loop/89159); [S][It's FOSS](https://itsfoss.com/news/llvm-ai-policy/)
- Fedora(2025-10-22 승인): 기여자가 저자로서 전적으로 책임진다. 상당 부분을 AI 출력에서 그대로 가져왔다면 공개가 의무이고, git에서는 `Assisted-by:` trailer를 권장한다. 문법 교정 수준은 공개하지 않아도 된다. 1차 페이지는 봇 차단으로 열지 못해 번역본과 보도로 확인했다 — [S][Fedora AI-Assisted Contributions Policy (ca)](https://docs.fedoraproject.org/ca/council/policy/ai-contribution-policy/); [S][Phoronix](https://www.phoronix.com/news/Fedora-Allows-AI-Contributions); [S][Linuxiac](https://linuxiac.com/fedora-opens-the-door-to-ai-tools)
- Ghostty: "All AI usage in any form must be disclosed"(도구와 비중), 사람이 전부 이해해야 하며, AI 생성 미디어는 금지다. slop 제출자는 공개 차단 목록에 오른다. 2025-08 PR #8289에서 공개 의무를 도입했고 2026-01에 AI_POLICY.md로 확대했다 — [F][Ghostty AI_POLICY.md](https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md); [S][codenote: OSS AI policy shift](https://codenote.net/en/posts/oss-ai-slop-contribution-policy-shift/); [S][GeekNews Ghostty](https://news.hada.io/topic?id=26082)
- QEMU: master 문서는 여전히 AI 생성 콘텐츠를 "DECLINE"한다(2025-06 도입). 완화안(기계적 변경·테스트·문서·20줄 이하 버그 수정 허용, `AI-used-for:` 태그)이 보도됐지만 문서에는 아직 반영되지 않았다 — [F][QEMU code-provenance](https://www.qemu.org/docs/master/devel/code-provenance.html); [S][Linuxiac: QEMU may relax](https://linuxiac.com/qemu-may-relax-its-ban-on-ai-generated-contributions/); [S][Phoronix QEMU](https://www.phoronix.com/news/QEMU-Patch-Allows-Some-AI); [S][patchew QEMU policy v5](https://patchew.org/QEMU/20250616092241.212898-1-armbru@redhat.com)
- Gentoo(2024-04)와 NetBSD(2024-05)는 AI 생성 코드를 금지했고 Debian은 동참하지 않았다(2024, 현재 상태는 확인하지 않음) — [S][The Register 2024](https://www.theregister.com/2024/05/18/distros_ai_code/); [S][LWN Gentoo](https://lwn.net/Articles/970072/); [S][Linuxiac NetBSD](https://linuxiac.com/netbsd-new-policy-prohibits-usage-of-ai-code/)
- curl은 AI slop 보안 신고 문제로 AI 정책 초안을 냈고(2025-05), 버그 바운티를 종료했다(2026-01) — [S][curl mailing list 2025-05](https://curl.se/mail/lib-2025-05/0013.html); [S][The Register 2026-01-21](https://www.theregister.com/2026/01/21/curl_ends_bug_bounty/)
- SSW 규칙: AI가 커밋하면 AI co-author에 더해 **검토·승인한 사람 본인도 Co-authored-by로 추가**한다. 큰 작업은 에이전트에게 "구현 흐름을 이야기하듯"(모델→로직→API→UI→테스트) 논리적 순서로 나눠 커밋하게 한다. Copilot과 Cursor는 자동 표기가 없으니 AGENTS.md 등으로 설정한다 — [F][SSW: attribute AI-assisted commits](https://www.ssw.com.au/rules/attribute-ai-assisted-commits-with-co-authors)

**규모와 위험**
- Claude Code 표기 커밋은 2026년 초 공개 GitHub 커밋의 약 4~4.5%였다(SemiAnalysis 추정 4%, Conffab 주간 4.5%). 측정 방법에 따라 30~40%씩 흔들린다(2차 자료) — [S][Conffab](https://conffab.com/?p=10304); [S][thenote: SemiAnalysis 4%](https://thenote.app/post/en/analysis-claude-code-currently-authors-4-of-all-public-github-commits-and-is-on-mdhhnbu3jf); [S][amplifying.ai tracker](https://amplifying.ai/coding-agents/claude-code)
- 연구 — [F][arXiv 2502.18904](https://arxiv.org/abs/2502.18904); [S][SANER 2024 preliminary study](https://conf.researchr.org/details/saner-2024/saner-2024-early-research-achievement--era--track-/81/Using-Large-Language-Models-for-Commit-Message-Generation-A-Preliminary-Study); [S][arXiv 2401.05926](https://arxiv.org/html/2401.05926v1)
  - ICSE'25(Wu et al., arXiv 2502.18904): in-context learning 기반 LLM 커밋 메시지는 주관 평가에서 SOTA를 "significantly outperforms"한다.
  - 같은 논문에 대한 검색 요약은 저성능 원인의 약 36%가 낮은 품질의 정답 메시지, 약 10.5%가 맥락 부족이라고 전한다. 초록에서는 수치를 확인하지 못했다.
  - SANER 2024: 사람 평가에서 LLM 출력이 366개 중 78%에서 최선으로 판정됐다.
- 반론(한국어, 2026): 커밋 메시지는 "변경 내용에 남지 않는 정보"를 붙잡아 두는 자리이고 이는 모델이 복원할 수 없다. 버린 대안, 일부러 건드리지 않은 범위, 임시방편의 해제 조건, 측정 조건, 외부 근거, 확신 정도가 그런 정보다. 오타·포맷·의존성 갱신처럼 변경 자체가 설명이 되는 커밋만 자동 생성에 맡기라고 한다. trailer로 표기해도 "책임이 넘어가지 않는다" — [F][braindetox: 커밋 메시지는 아직 사람이 쓴다](https://braindetox.kr/posts/commit_message_authorship.html)
- 한국어 커밋 설정 팁: Cursor는 기본으로 영어 커밋 메시지를 만든다. CLAUDE.md 같은 규칙 파일에 "커밋 메시지: 한국어로 작성"을 넣으라는 Q&A가 있다 — [S][인프런 Q&A](https://www.inflearn.com/community/questions/1770300/커밋-이름을-커서가-자동으로-하도록-버튼을-누르면-영어로-이름이-나와요)
- 한국 저장소의 에이전트용 커밋 규칙(sodalive): description은 한글 명령형 또는 간결한 현재형, `Refs: #123` footer, 에이전트 서명 문구와 `Co-authored-by: Sisyphus` 줄은 제거한다. 커밋 직전·직후에 `check-commit-message-rules.sh`를 실행한다 — [F][sodalive agent-guides/커밋메시지.md](https://git.sodalive.net/klaus/sodalive-backend-spring-boot/src/branch/test/docs/agent-guides/%EC%BB%A4%EB%B0%8B%EB%A9%94%EC%8B%9C%EC%A7%80.md)

### Inferences
- 믿집 초안("AI 도구는 co-author trailer를 달고, 요청받을 때만 커밋")은 Fedora·LLVM·Linux·SSW 방향과 맞는다. Kubernetes 방식과는 반대지만, 학생 프로젝트에서는 평가자에게 AI 사용을 투명하게 보이는 편이 이익이다.
- **squash 함정:** main에 남는 것은 squash 커밋 하나다. 브랜치 커밋의 `Co-Authored-By: Claude …`가 squash 메시지에 유지되는지는 GitHub 옵션에 따라 다르다("PR title"만 고르면 본문이 비어 trailer가 사라질 가능성이 높다. 미검증). 따라서 두 가지 장치를 함께 둘 것을 권한다.
  - (1) PR 템플릿에 "AI 사용: 도구/범위/사람 검토 여부" 칸을 둔다(Kubernetes·Ghostty식 공개).
  - (2) squash 시 trailer를 유지하는 옵션("PR title and commit details" 등)을 실제로 테스트하거나, 머지하는 사람이 squash 대화상자에 trailer를 남기는 규칙을 둔다.
- **author는 반드시 사람이어야 한다.** CLA 봇 사례에서 보듯 에이전트 bot이나 기본 주소가 author가 되면 기여 집계와 책임 추적이 어긋난다. 로컬 Claude Code는 사용자 git 설정으로 커밋하므로 대체로 문제가 없지만, 클라우드·웹 에이전트는 확인해야 한다.
- AI가 쓴 커밋·PR 메시지는 "무엇"은 정확해도 "왜"가 빈약하거나 그럴듯하게 지어질 수 있다. 사람이 PR 제목과 요약의 "왜"를 확인하거나 고치는 것을 리뷰 체크 항목으로 넣는 것이 위험 대비책이다.
- AGENTS.md에는 다음을 명시하면 에이전트 간 일관성이 생긴다.
  - 커밋 언어(한국어 요약), 타입·scope 목록, "요청 시에만 커밋/푸시".
  - `--no-verify` 금지, author 설정 변경 금지, co-author trailer 유지 또는 형식.
  - changelog brief(KaC 2.0 권고).

### Gaps
- Claude Code `attribution.commit`의 정확한 기본 문자열과 비활성화 방식(빈 문자열 vs boolean)을 공식 문서 본문으로 확인하지 못했다(설정 페이지가 44만 자라 해당 부분까지 읽지 못함). 2차 출처 사이에 충돌이 있다.
- GitHub squash 머지에서 브랜치 커밋의 `Co-authored-by` trailer가 보존되는지에 대한 공식 근거가 없다(§2 Gaps와 동일).
- 한국 기업이나 교육기관의 AI 커밋 공개 정책은 찾지 못했다.

## 6. 한국어 자료: 커밋 컨벤션 · 깃모지 · 한글 커밋 메시지 관행, 회사·교육과정별 규칙

### Takeaway
한국 팀의 사실상 표준은 **"영문 소문자 type(+선택 scope) + 한글 제목"**이다. 교육과정(우테코·SSAFY·부스트캠프·코드스테이츠)은 AngularJS/Udacity 규약이나 `[type] 제목 (이슈키)` 같은 변형을 쓰고, 일부 팀은 gitmoji를 쓴다. 한글 제목의 어미(명령형·"~한다" 평서·명사형 "~추가")를 비교한 권위 있는 자료는 없다. 실제로는 여러 어미가 섞여 쓰이므로 팀이 하나로 정해야 한다.

### Cited Findings
- 한국어 블로그와 팀 문서 다수가 `<type>(scope): <description>`, 소문자 type, 한글 description(명령형 또는 간결한 현재형) 조합을 쓴다. type 자체를 한글로 쓰는 사례는 드물다 — [S][검색 종합: velog new_wisdom 등](https://velog.io/@new_wisdom/Clean-Coding-Commit-Message-Conventions); [F][sodalive 커밋메시지.md](https://git.sodalive.net/klaus/sodalive-backend-spring-boot/src/branch/test/docs/agent-guides/%EC%BB%A4%EB%B0%8B%EB%A9%94%EC%8B%9C%EC%A7%80.md)
- sodalive 실제 커밋 제목은 "~한다" 평서형이다. 예: `refactor(commit): 커밋 정책을 commit-policy 스킬로 분리한다`, `fix(commit): AGENTS 규칙과 커밋 메시지 검사 스크립트를 정합화한다` — [S][sodalive commit 211eb35](https://git.sodalive.net/klaus/sodalive-backend-spring-boot/commit/211eb3507cd502a73e1a4cf3c377d63523718538); [S][sodalive commit fe5eefd](https://git.sodalive.net/klaus/sodalive-backend-spring-boot/commit/fe5eefde3119e5333523072f45afba63ccc90285)
- 우아한테크코스 — [F][velog new_wisdom (2020)](https://velog.io/@new_wisdom/Clean-Coding-Commit-Message-Conventions); [F][velog brokenfinger 우테코 8기](https://velog.io/@brokenfinger/우아한-테크-코스-8기-프리코스-1주차1-git-commit-convention); [S][velog ariul-dev](https://velog.io/@ariul-dev/Convention-Git-Commit-Message-Conventions)
  - 2020년 과제 글은 AngularJS 계열 규약(feat·fix·docs·style·refactor·test·chore, 명령형, 소문자, 마침표 없음, 줄당 100자)을 번역해 정리했다. 예시는 영어다.
  - 8기 프리코스(2025-10-14)도 미션에서 "AngularJS Git Commit Message Conventions"를 요구했다. 참가자는 `.gitmessage.txt` 템플릿을 만들었다. 한글·영어 중 무엇을 쓸지는 명시되지 않았다.
- SSAFY(2022 재학생 정리): 형식은 `[타입] 제목 (지라이슈번호)`이고 제목·본문은 한글이다. 예: `[feat] 댓글 작성 기능 구현 (S07P22A602-85)`(명사형 종결). MR 제목은 `[분야] 작업 내용`이다 — [F][velog kku64r SSAFY Git 규칙](https://velog.io/@kku64r/gitflow)
- 부스트캠프 팀(2021 무렵 HackMD): gitmoji + 이슈 번호를 앞에 붙이고, Feat·Doc·Chore·Refactor·Fix·Layout 타입별 이모지 표를 둔다 — [S][HackMD 부스트캠프 팀 그라운드룰](https://hackmd.io/@Y_B76FeeRPizZr7JOIxW5Q/HycaJa78K)
- 코드스테이츠 사전 프로젝트 후기: 컨벤션·Gitflow·이슈 정책을 팀원 다수가 동의하는 방식으로 합의하라고 한다 — [S][velog rmaomina](https://velog.io/@rmaomina/pre-project-github-features-convensions)
- Udacity 스타일 정리(2024-06-25): type 첫 글자를 대문자로 쓴다(Feat, Fix, Design, Rename, Remove 등). 제목은 50자 이하, 마침표 없음, 명령조다. 한글 예시를 함께 싣고 "알아보기 쉽고 구분하기 쉽게"가 목적이라고 한다 — [F][velog julia8024 Udacity Style](https://velog.io/@julia8024/Git-깃-커밋-컨벤션-feat.-Udacity-Style)
- 요즘IT(2023-04-14): `<type>: <description>`, 7개 타입, 50자 이내, body는 72자, footer에 `Closes #`. 한국어 사용 여부는 언급하지 않는다 — [F][요즘IT 커밋 컨벤션](https://yozm.wishket.com/magazine/detail/1974)
- 인포그랩(2023): 커밋 종류별 이모지, 컴포넌트 이름은 대문자·페이지/함수 이름은 소문자로 구분, 세부 사항은 body에 쓴다. 댓글에는 "이모지가 가독성을 높인다"는 주장에 대한 반론이 있다 — [F][GeekNews 9178](https://news.hada.io/topic?id=9178); [F][GeekNews 9394](https://news.hada.io/topic?id=9394)
- gitmoji 형식은 `<intention> [scope?][:?] <message>`이고 intention은 유니코드(🐛)나 `:shortcode:`로 쓴다. 유니코드는 글자 수가 적지만 일부 터미널에서 깨질 수 있다 — [F][gitmoji specification](https://gitmoji.dev/specification); [F][gitmoji about](https://gitmoji.dev/about)
- 개인 dotfiles 규칙 사례: 개인 프로젝트는 한국어가 기본이고 오픈소스만 영어로 쓴다. gitmoji는 금지다 — [S][tomevault sskim91 dotfiles](https://tomevault.io/tome/sskim91/dotfiles/git-commit)
- 언어 선택 — [S][velog changonna](https://velog.io/@changonna/Git-Commit-Message-작성법); [F][braindetox 커밋 메시지 저자](https://braindetox.kr/posts/commit_message_authorship.html); [S][freeCodeCamp 한국어](https://www.freecodecamp.org/korean/news/writing-good-commit-messages-a-practical-guide/)
  - 영문으로 써야 하는 것은 아니며 구성원이 합의한 언어를 쓰면 된다. "50자 이하"는 영문 기준이다.
  - 저장소를 읽을 사람의 범위로 정한다. 오픈소스이거나 외국인이 합류할 예정이면 영어, 사내 전용이면 정확도를 위해 한국어를 쓸 수 있다. 어느 쪽이든 일관성이 중요하다.
- 국립국어원 자료는 명사형 어미 '-음'(있음/없음) 표기를 설명한다. 명사형 종결을 쓸 때 표기 참고용이다 — [S][국립국어원 새국어소식](https://www.korean.go.kr/nkview/nknews/200502/79_3.html)
- 한국어 CC 번역본과 Keep a Changelog 한국어 번역이 있다(1.x 기준) — [F][CC 한국어](https://www.conventionalcommits.org/ko/v1.0.0/); [S][KaC 한국어](https://keepachangelog.com/ko/1.0.0)
- Google Blockly의 한국어 안내 페이지는 docs.blockly.com 영문 페이지로 리다이렉트된다 — [F][Blockly commits](https://docs.blockly.com/guides/contribute/get-started/commits)

### Inferences
- 믿집 초안(`type(범위): 한국어 요약`)은 한국 팀의 가장 흔한 형식과 일치하므로 학습 비용이 거의 없다. gitmoji는 type과 중복되고 PR 제목 검사 정규식을 복잡하게 만든다. 넣지 않는 것을 권한다.
- 어미는 "명령형 현재"라는 영어 규칙을 한국어로 옮기는 방식이 셋으로 갈린다.
  - ① "~한다" 평서형(sodalive): "If applied, this commit will…"과 의미상 가장 가깝다.
  - ② 명사형 "~ 추가/구현"(SSAFY): 가장 짧다.
  - ③ "~하기" 혹은 명령형 "~하라": 거의 쓰지 않는다.
  - 셋 다 실제로 쓰이므로 하나로 정하고 예시 3~5개를 AGENTS.md와 CONTRIBUTING에 박아 두는 것이 핵심이다. AI 도구는 예시를 강하게 따라간다.
- 이슈 번호는 SSAFY식 제목 괄호 대신 PR 본문의 `Closes #123`으로 두면 제목 글자 수를 아낄 수 있다. squash 커밋에 PR 번호 `(#123)`가 자동으로 붙는 것도 고려한 판단이다(GitHub 기본 동작으로 알려져 있으나 이번에 문서로 확인하지 않음).

### Gaps
- 토스·카카오·네이버·우아한형제들·당근 같은 한국 기업의 공개 커밋 규칙 원문은 찾지 못했다. 검색에 기술블로그 글이 잡히지 않았고 검색 예산도 소진됐다.
- SKN(SK네트웍스 AI 부트캠프) 과정이 공식 커밋 규칙을 제시하는지는 확인하지 못했다.
- 한글 제목 어미별 가독성·선호를 비교한 조사는 존재하지 않는 것으로 보인다(검색 결과 없음).

## 7. 믿집 팀을 위한 구체 권고 (커밋 형식 · 강제 여부 · CHANGELOG · 태그/버전 · 데모 릴리스 노트)

### Takeaway
권고 요지는 다음과 같다.
- 초안 형식 `type(scope): 한국어 요약`은 유지한다. 타입에 `revert`를 더하고 `docs` 중복을 정리한다.
- GitHub 설정을 "Squash only + PR title(±description)"으로 바꾸고, PR 제목만 서버 쪽 Action으로 검사한다. 로컬 훅은 선택 사항으로 둔다.
- CHANGELOG.md는 Keep a Changelog 2.0 형식으로 데모·출시 때만 사람이 다듬는다. GitHub 자동 노트나 release-drafter를 초안으로 쓴다.
- 데모마다 annotated tag와 pre-release GitHub Release를 만들고, 출시 시 `v1.0.0`을 찍는다.
- AI 사용은 trailer와 PR 템플릿 두 곳에 공개하고, 사람이 author이자 책임자가 된다.

### Cited Findings
- squash 기본 메시지가 커밋 1개 PR에서는 PR 제목이 아니라 커밋 메시지를 쓰므로 설정 변경이 필요하다 — [F][GitHub Docs squash](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests)
- PR 제목 검사 Action v6는 `types`·`scopes` 정규식과 `requireScope` 옵션을 지원한다 — [F][action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request)
- 로컬 훅은 우회 가능하므로 CI 검사가 필요하다 — [F][commitlint local setup](https://commitlint.js.org/guides/local-setup.html)
- "Machines can draft, but humans curate". changelog brief를 AGENTS.md/CLAUDE.md에 기록한다. 비SemVer(날짜 등)도 괜찮다. 릴리스 노트는 changelog에서 뽑는다 — [F][Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/)
- 라벨 기반 자동 노트 카테고리 — [F][GitHub release.yml](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes); conventional 제목 기반 분류 — [F][release-drafter](https://github.com/release-drafter/release-drafter)
- annotated tag는 릴리스용이다 — [F][git-tag](https://git-scm.com/docs/git-tag). SemVer 0.y.z와 production이면 1.0.0 — [F][semver.org](https://semver.org/). 애플리케이션은 CalVer도 흔하다 — [F][SensioLabs](https://sensiolabs.com/blog/2025/semantic-vs-calendar-versioning); [F][calver.org](https://calver.org/)
- AI 공개는 trailer(Fedora·LLVM·Linux·SSW) 또는 PR 본문(Kubernetes)으로 한다. 사람이 책임진다 — §5 출처들

### Inferences
**권고안 A — 커밋/PR 제목 규칙**
- 형식은 `type(scope)!?: 한국어 요약`이다. type은 소문자 영어, scope는 선택이며 하나만 쓴다(여러 곳이면 생략하거나 주된 곳 하나), 마침표는 쓰지 않는다.
- type은 `feat · fix · docs · test · chore · refactor · prompt · eval`에 **`revert`를 추가**한다. `perf`·`ci`·`build`는 `chore`/`refactor`로 흡수해 목록을 작게 유지한다(braindetox·CC 비판이 공통으로 "타입을 줄이라"고 함). 각 타입의 정의를 한 줄씩 적는다.
  - prompt: 프롬프트·시스템 지시·템플릿 텍스트만 바뀐 경우.
  - eval: 평가 세트·채점 스크립트·평가 결과.
  - 사용자 동작이 바뀌면 feat/fix가 우선한다.
- scope는 `web · api · calc · agent · worker · db · infra`를 쓴다. `docs`는 type으로만 쓰거나, scope로 남긴다면 "문서 사이트·문서 도구"로 의미를 한정한다.
- `!`는 팀원 환경을 깨는 변경에 쓴다. 예: DB 스키마 재생성이 필요한 경우, `.env` 키 변경, API 계약 변경(`feat(api)!: 견적 응답 필드명을 변경한다`). 본문에는 `BREAKING CHANGE:` 대응 방법을 적는다.
- 길이는 제목 전체 72자 이하(commitlint 기본 100은 상한)이고, 한글은 약 35자 이내를 권장한다.
- 본문에는 "왜"를 쓴다. 이슈는 PR 본문의 `Closes #N`으로 연결한다.

**권고안 B — GitHub 설정과 강제 수준**
- Settings → Pull Requests: merge commit과 rebase를 끄고 squash만 허용한다. 기본 메시지는 "Pull request title and description"(또는 "Pull request title")로 둔다.
- `.github/workflows/pr-title.yml`에 amannn v6를 둔다. `types`에 위 9개, `scopes`에 위 enum, `requireScope: false`. 필수 체크로 걸려면 `synchronize` 트리거를 넣는다. 비공개 저장소라면 `pull_request` 트리거를 검토한다.
- 로컬 commitlint/husky는 도입하지 않거나 "원하는 사람만 쓰는 옵션"으로 둔다. 학생 팀은 Node 버전이 제각각이고, squash로 브랜치 커밋이 사라지며, AI 도구가 커밋을 만든다는 점이 근거다.
- PR 템플릿 맨 위에는 요약(왜/무엇 2~4줄)을 두고, 그 아래 "AI 사용(도구·범위·사람 검토)", "릴리스 노트용 한 줄(사용자 관점, 과거형)"을 둔다(Electron `Notes:`·Kubernetes `release-note` 방식).

**권고안 C — CHANGELOG**
- 루트의 `CHANGELOG.md`는 Keep a Changelog 2.0 형식이다. 맨 위에 `## [Unreleased]`를 두고, 유형은 영어 6개(Added/Changed/Deprecated/Removed/Fixed/Security)를 쓰거나 한국어 번역(추가/변경/폐기 예정/제거/수정/보안)을 쓴다. 이 선택은 결정 항목이다.
- 매 PR마다 changelog를 고치게 하지 않는다(KaC 2.0이 required check로 만들지 말라고 함). 데모나 출시 직전에 머지된 PR 제목 목록(자동 노트나 release-drafter 초안)을 보고 사람이 사용자 관점으로 묶어 쓴다. `chore`·`test`·`refactor`·`eval`은 원칙적으로 제외하고, 데모에서 보여 줄 평가 결과처럼 의미가 있을 때만 넣는다.
- AGENTS.md에 "changelog brief"를 기록한다: 사용자에게 보이는 변경만, 6개 유형, breaking 표시, 한국어, PR 번호 링크. AI가 초안을 쓰고 사람이 확정한다.
- 자동화 도구(release-please·semantic-release·changesets)는 지금은 도입하지 않는다. 출시 후 정기 배포가 생기면 release-please `simple` 타입이나 git-cliff를 재검토한다(사용자 정의 타입 등록 필요).
- 선택 보강: release-drafter의 conventional 제목 분류나 `.github/release.yml` + 라벨로 GitHub Release 초안을 유형별로 정리할 수 있다. 라벨은 autolabeler나 actions/labeler로 자동으로 단다.

**권고안 D — 태그·버전**
- 앱이므로 public API 기반 SemVer는 의미가 약하다. 다만 발표와 출시 서사에는 단순한 단계 번호가 유리하다. 두 안을 결정 항목으로 제시한다.
  - D-a: `v0.1.0`(첫 데모/MVP), `v0.2.0`, … 공개 출시 시 `v1.0.0`. 데모 사이의 긴급 수정은 `v0.2.1`.
  - D-b(CalVer): `v2026.10.29`처럼 데모·배포일 태그를 쓴다. 날짜 자체가 정보이고 breaking 판단이 필요 없다.
- 어느 쪽이든 annotated tag(`git tag -a v0.1.0 -m "1차 데모"`)와 GitHub Release를 쓰고, 데모 빌드는 "pre-release"로 표시한다. Immutable releases는 출시 전까지 끄는 편이 안전하다.
- 체계는 CHANGELOG 맨 위에 한 줄로 명시한다(KaC 2.0, Frontside 공통 권고).

**권고안 E — 데모·발표용 릴리스 노트 템플릿(제안)**
- 제목은 `v0.N.0 — N차 데모 (YYYY-MM-DD)`로 한다.
- 구성:
  - ① 한 문단 요약: 이번 데모에서 무엇을 보여 주는가.
  - ② 주요 기능 3~5개: 사용자 관점, 과거형 또는 명사형 통일, 화면 캡처나 GIF.
  - ③ 바뀐 점과 고친 점: CHANGELOG의 해당 섹션 발췌.
  - ④ 알려진 한계와 다음 계획.
  - ⑤ 데모 시나리오와 배포 URL, 시연 계정 안내(비밀값 제외).
  - ⑥ 기여자.
  - ⑦ 전체 변경 비교 링크(자동 생성 "Full Changelog").
- PR 목록 전체를 그대로 붙이지 않는다(Common Changelog·KaC). 이 노트를 발표 슬라이드의 "릴리스 히스토리" 장의 원천으로 쓴다.

**권고안 F — AI 보조 커밋**
- Claude Code 등 도구가 붙이는 co-author trailer는 유지한다(투명성). 커밋 author는 반드시 사람의 git 계정이어야 한다(CLA 봇·Copilot squash 사례).
- squash 후에도 AI 사용 사실이 남도록 PR 템플릿에 AI 사용 칸을 둔다. 선택한 squash 옵션에서 trailer가 보존되는지 첫 PR에서 실측한다.
- AI가 쓴 PR 제목과 요약은 사람이 "왜"를 확인한 뒤 머지한다. 에이전트는 요청 시에만 커밋하고 푸시하며, `--no-verify`와 author 변경을 금지한다. 이 규칙을 AGENTS.md에 명시한다.

**현행 `mitjip/AGENTS.md`와의 정합 (2026-10-29 기준 파일 확인)**
- 이미 반영된 것:
  - §6 커밋 제목 형식·타입·범위 목록, squash merge, 승인 1명, PR 400줄 이하.
  - PR 본문 구조: 무엇을 왜 / 호출 흐름 / 검증 결과 / 못 한 것 / `Closes #N`.
  - "AI 코딩 도구는 사람이 요청했을 때만 커밋·푸시".
  - §4 "프롬프트를 바꾸는 PR은 커밋 type `prompt`로 하고 eval 결과를 붙인다". 따라서 `prompt` 타입의 정의는 이미 "프롬프트 변경 PR"로 정해져 있다.
- 이 조사에서 더할 만한 것:
  - ① `revert` 타입과 `docs(docs)` 중복 정리.
  - ② squash 기본 메시지 설정(PR title 계열)과 PR 제목 검사 Action.
  - ③ PR 본문에 "AI 사용" 칸과 "릴리스 노트 한 줄" 칸.
  - ④ CHANGELOG.md 형식, 갱신 시점, changelog brief.
  - ⑤ 태그와 버전 체계.
  - ⑥ AI 커밋 author는 사람으로 하고 trailer는 유지한다는 규칙, `--no-verify` 금지.
- 되돌리기 어려운 항목(C7 버전 체계, C4 squash 설정)은 AGENTS.md 우선순위 규칙에 따라 `docs/adr/`에 남길 후보다.

**팀이 정해야 할 결정 항목(제안 ID, 기존 D/R/S/K 체계와 별개)**
- C1. 한글 제목 어미: "~한다" 평서형 vs 명사형("~ 추가") 중 무엇으로 통일할까?
- C2. scope 필수 여부(권고: 선택)와 `docs` scope 유지 여부.
- C3. `revert` 추가, `perf/ci/build` 흡수에 동의하는가? `prompt`와 `feat/fix`의 우선순위 규칙은?
- C4. squash 기본 메시지: "PR title" vs "PR title and description".
- C5. 로컬 commitlint/husky를 둘까(권고: 두지 않음), PR 제목 검사를 필수 체크로 걸까?
- C6. CHANGELOG 유형 머리말: 영어 6개 vs 한국어 번역.
- C7. 버전 체계: `v0.x → v1.0.0`(SemVer식) vs CalVer 날짜 태그.
- C8. AI 공개 위치: trailer + PR 템플릿 둘 다(권고) vs 한쪽만.

### Gaps
- 위 권고 중 실측이 필요한 것:
  - squash 옵션별 trailer 보존.
  - commitlint·Action 정규식의 한글 처리.
  - GitHub squash 커밋 제목의 `(#PR번호)` 자동 부가 여부.
- 팀의 실제 저장소 설정(공개/비공개, 포크 사용, 브랜치 보호 규칙)을 모르므로 `pull_request` vs `pull_request_target` 선택은 확정하지 않았다.

### 참고한 전체 URL 목록 (F = 직접 열람, S = 검색 결과·스니펫만 확인, X = 열람 실패)
**규격·공식 문서**
- F https://www.conventionalcommits.org/en/v1.0.0/
- F https://www.conventionalcommits.org/ko/v1.0.0/
- F https://github.com/conventional-commits/conventionalcommits.org
- F https://en.wikipedia.org/wiki/Conventional_Commits_Specification
- F https://keepachangelog.com/en/1.1.0/
- F https://keepachangelog.com/en/2.0.0/
- S https://keepachangelog.com/ko/1.0.0
- F https://common-changelog.org/
- F https://semver.org/
- F https://calver.org/
- F https://0ver.org/
- F https://git-scm.com/docs/SubmittingPatches
- F https://git-scm.com/docs/git-interpret-trailers
- F https://git-scm.com/docs/git-tag
- F https://www.kernel.org/doc/html/latest/process/submitting-patches.html
- F https://www.kernel.org/doc/html/latest/process/coding-assistants.html
- F https://cbea.ms/git-commit/
- F https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
- F https://scopedcommits.com/
- F https://gitmoji.dev/about
- F https://gitmoji.dev/specification

**GitHub 문서·변경 로그**
- F https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests
- F https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges
- F https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes
- F https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
- S https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors
- S https://github.com/github/docs/issues/36812
- S https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases
- F https://github.blog/changelog/2022-05-11-default-to-pr-titles-for-squash-merge-commit-messages/
- S https://github.blog/changelog/2022-08-23-new-options-for-controlling-the-default-commit-message-when-merging-a-pull-request/
- S https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/
- F https://github.blog/changelog/2026-03-20-trace-any-copilot-coding-agent-commit-to-its-session-logs
- S https://github.blog/2017-01-10-commit-together-with-co-authors
- S https://github.com/orgs/community/discussions/178351
- S https://github.com/orgs/community/discussions/179983

**도구**
- F https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional
- F https://commitlint.js.org/reference/rules.html
- F https://commitlint.js.org/reference/configuration.html
- F https://commitlint.js.org/guides/local-setup.html
- F https://commitlint.js.org/guides/ci-setup.html
- F https://github.com/conventional-changelog/commitlint/releases
- S https://newreleases.io/project/npm/commitlint/release/21.0.0
- F https://github.com/amannn/action-semantic-pull-request
- F https://github.com/amannn/action-semantic-pull-request/releases
- F https://github.com/typicode/husky/releases
- F https://github.com/evilmartians/lefthook
- S https://www.pkgpulse.com/guides/husky-vs-lefthook-vs-lint-staged-git-hooks-nodejs-2026
- F https://github.com/compilerla/conventional-pre-commit
- F https://commitizen-tools.github.io/commitizen/
- F https://github.com/googleapis/release-please
- F https://github.com/googleapis/release-please/releases
- F https://github.com/googleapis/release-please/blob/main/docs/customizing.md
- F https://github.com/googleapis/release-please-action
- S https://dev.to/sofiama/automate-release-notes-aka-changelog-gcn
- S https://fr.github.com/Flagsmith/flagsmith/blob/main/release-please-config.json
- S https://cloud.theodo.com/en/blog/release-please
- F https://github.com/semantic-release/semantic-release
- F https://github.com/semantic-release/semantic-release/releases
- F https://github.com/changesets/changesets
- F https://github.com/changesets/changesets/blob/main/docs/intro-to-using-changesets.md
- F https://git-cliff.org/docs/
- F https://git-cliff.org/docs/configuration/git
- F https://github.com/release-drafter/release-drafter
- F https://github.com/actions/labeler
- S https://github.com/release-it/keep-a-changelog
- S https://goreleaser.com/blog/immutable-releases/

**대형 프로젝트 규칙**
- F https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md
- F https://github.com/vuejs/core/blob/main/.github/commit-convention.md
- F https://github.com/electron/electron/blob/main/docs/development/pull-requests.md
- F https://github.com/electron/electron/blob/main/.github/PULL_REQUEST_TEMPLATE.md
- F https://github.com/kubernetes/community/blob/master/contributors/guide/pull-requests.md
- F https://github.com/kubernetes/community/blob/master/contributors/guide/release-notes.md
- F https://docs.blockly.com/guides/contribute/get-started/commits
- F https://docs.gitlab.com/development/changelog/
- S https://github.fr/vercel/next.js/pulls
- S https://raes-environment-packs.readthedocs.io/en/latest/decisions/adrs/0006-conventional-commit-releases.html
- S https://github.com/gramps-project/gramps-web/discussions/286

**AI 정책·도구**
- F https://code.claude.com/docs/en/settings
- F https://code.claude.com/docs/en/settings-reference
- S https://claudelog.com/faqs/attribution-setting-claude-code/
- F https://www.deployhq.com/blog/how-to-use-git-with-claude-code-understanding-the-co-authored-by-attribution
- S https://zenn.dev/dk_/articles/8e4726b71f7803?locale=en
- S https://wmedia.es/en/tips/claude-code-remove-co-authored-by-claude
- F https://heise.de/-11279554
- S https://www.penligent.ai/hackinglabs/ko/?p=5124
- F https://www.ssw.com.au/rules/attribute-ai-assisted-commits-with-co-authors
- S https://cdn.jsdelivr.net/gh/bruno-garcia/pi-co-authored-by@main/README.md
- S https://socket.dev/npm/package/madeby
- F https://discuss.python.org/t/cla-bot-and-ai-agents/106635
- F https://llvm.org/docs/AIToolPolicy.html
- S https://discourse.llvm.org/t/rfc-llvm-ai-tool-policy-human-in-the-loop/89159
- S https://itsfoss.com/news/llvm-ai-policy/
- X https://docs.fedoraproject.org/en-US/council/policy/ai-contribution-policy/ (봇 차단)
- S https://docs.fedoraproject.org/ca/council/policy/ai-contribution-policy/
- S https://www.phoronix.com/news/Fedora-Allows-AI-Contributions
- S https://linuxiac.com/fedora-opens-the-door-to-ai-tools
- F https://www.qemu.org/docs/master/devel/code-provenance.html
- S https://linuxiac.com/qemu-may-relax-its-ban-on-ai-generated-contributions/
- S https://www.phoronix.com/news/QEMU-Patch-Allows-Some-AI
- S https://patchew.org/QEMU/20250616092241.212898-1-armbru@redhat.com
- F https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md
- S https://codenote.net/en/posts/oss-ai-slop-contribution-policy-shift/
- S https://news.hada.io/topic?id=26082
- S https://www.theregister.com/2024/05/18/distros_ai_code/
- S https://lwn.net/Articles/970072/
- S https://linuxiac.com/netbsd-new-policy-prohibits-usage-of-ai-code/
- S https://curl.se/mail/lib-2025-05/0013.html
- S https://www.theregister.com/2026/01/21/curl_ends_bug_bounty/
- S https://conffab.com/?p=10304
- S https://thenote.app/post/en/analysis-claude-code-currently-authors-4-of-all-public-github-commits-and-is-on-mdhhnbu3jf
- S https://amplifying.ai/coding-agents/claude-code
- F https://arxiv.org/abs/2502.18904
- S https://arxiv.org/html/2401.05926v1
- S https://conf.researchr.org/details/saner-2024/saner-2024-early-research-achievement--era--track-/81/Using-Large-Language-Models-for-Commit-Message-Generation-A-Preliminary-Study

**비판·연구·버전 체계 논의**
- F https://sumnerevans.com/posts/software-engineering/stop-using-conventional-commits/
- F https://braindetox.kr/posts/conventional_commits_critique_2026.html
- F https://braindetox.kr/posts/commit_message_authorship.html
- S https://www.eclipse.org/lists/che-dev/msg04192.html
- S https://hn.svelte.dev/item/30950377
- S https://ecosistemastartup.com/?p=85841
- S https://journals.usach.cl/ojs/index.php/revistagpt/en/article/view/7559
- S https://pure.bit.edu.cn/zh/publications/a-first-look-at-conventional-commits-classification/
- F https://sensiolabs.com/blog/2025/semantic-vs-calendar-versioning
- F https://frontside.com/blog/2022-02-09-semver-or-calver-by-project-type/
- S https://fale.io/blog/2024/07/31/on-software-versioning-schema
- S https://aboutcode.org/blog/software-versioning/

**한국어 자료**
- F https://yozm.wishket.com/magazine/detail/1974
- F https://git.sodalive.net/klaus/sodalive-backend-spring-boot/src/branch/test/docs/agent-guides/%EC%BB%A4%EB%B0%8B%EB%A9%94%EC%8B%9C%EC%A7%80.md
- S https://git.sodalive.net/klaus/sodalive-backend-spring-boot/commit/211eb3507cd502a73e1a4cf3c377d63523718538
- S https://git.sodalive.net/klaus/sodalive-backend-spring-boot/commit/fe5eefde3119e5333523072f45afba63ccc90285
- F https://velog.io/@new_wisdom/Clean-Coding-Commit-Message-Conventions
- F https://velog.io/@brokenfinger/우아한-테크-코스-8기-프리코스-1주차1-git-commit-convention
- S https://velog.io/@ariul-dev/Convention-Git-Commit-Message-Conventions
- F https://velog.io/@julia8024/Git-깃-커밋-컨벤션-feat.-Udacity-Style
- F https://velog.io/@kku64r/gitflow
- S https://velog.io/@rmaomina/pre-project-github-features-convensions
- S https://velog.io/@changonna/Git-Commit-Message-작성법
- S https://hackmd.io/@Y_B76FeeRPizZr7JOIxW5Q/HycaJa78K
- F https://news.hada.io/topic?id=9178
- F https://news.hada.io/topic?id=9394
- S https://www.freecodecamp.org/korean/news/writing-good-commit-messages-a-practical-guide/
- S https://tomevault.io/tome/sskim91/dotfiles/git-commit
- S https://www.inflearn.com/community/questions/1770300/커밋-이름을-커서가-자동으로-하도록-버튼을-누르면-영어로-이름이-나와요
- S https://www.korean.go.kr/nkview/nknews/200502/79_3.html
- S https://clickup.com/ko/blog/128870/how-to-write-release-notes
- X https://wikidocs.net/443811 (403, 스니펫만)
- X https://azure.github.io/azure-sdk-korean/policies_releasenotes.html (404, 스니펫만)
- S https://pure.bit.edu.cn/zh/publications/a-first-look-at-conventional-commits-classification/ (중복 표기 생략)
