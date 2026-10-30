# PR description formats and PR templates — survey for the 믿집 team template

Scope note: I fetched every template from each repo's default branch (`HEAD`) on **2026-10-29**. That makes 113 real template files: 96 from popular OSS and Korean-company OSS repos, plus 17 Korean ones (15 우아한테크코스 bootcamp team repos under `woowacourse-teams`, `toss/es-hangul` and `kakao/actionbase`). I also read about 40 docs and blog pages. The shared WebSearch budget ran out early in this task, so I only fetched pages whose URLs I already knew or could guess. That is why Korean blog coverage is thin; see Gaps. The section tallies come from keyword and heading scripts run over the downloaded files, and I spot-checked the results by reading every template. Treat the counts as approximate.

## 1. What sections do popular OSS PR templates contain, and which are common vs rare?

### Takeaway
Nearly every template asks for three things: a summary of what changed, a linked issue (`Fixes/Closes #N`), and a test plan or other proof that the change works. A "why / problem" section and a checklist each appear in roughly half. Release notes, screenshots, reviewer notes and AI disclosure each appear in about a third. Breaking-change, migration, rollback, risk, type-of-change and follow-up sections are rare (under 15%). The typical template is short: median 3 visible headings and about 20 non-blank lines.

### Cited Findings
**Tally over 96 templates.** Keyword match over the full file text, including HTML guidance comments. Each template is listed in the Sources section of Q5.
- Summary / description / what changed: 83/96 (86%).
- Linked issue (`Fixes`/`Closes`/ticket): 65/96 (67%).
- Docs updated: 60/96 (62%).
- Testing / test plan / how verified: 58/96 (60%).
- Why / motivation / problem: 55/96 (57%).
- Checkbox checklist: 55/96 (57%).
- Release note / changelog / changeset: 34/96 (35%).
- Title or commit-message convention: 31/96 (32%).
- Screenshots / visual demo: 29/96 (30%).
- AI / LLM / agent disclosure: 29/96 (30%).
- Reviewer notes / focus: 29/96 (30%).
- DCO / CLA / signed commits: 18/96 (19%).
- Risk / rollback / security: 16/96. This count is inflated by "don't report vulnerabilities here" boilerplate.
- Breaking change: 13/96.
- Follow-ups / future work / TODO: 9/96.
- Type-of-change list: 8/96.
- DB/API migration: 8/96.
- Self-review: 7/96.

**Tally of visible headings only** (HTML comments stripped):
- Summary/description heading: 70/96.
- Checklist-style heading: 55.
- Testing heading: 30.
- Linked-issue heading: 25.
- Reviewer-notes heading: 25.
- Why/motivation heading: 21.
- Release-note heading: 13.
- AI heading: 12.
- Screenshot heading: 7.
- Type-of-change heading: 7.
- Docs heading: 5.
- Breaking-change heading: 4.
- Risk/rollback heading: 3.

**Size statistics:**
- Median 3 visible headings (mean 3.1).
- 14 of 96 templates are comment-only, with no visible headings: Next.js, Vite, Deno, Node, TypeScript, VS Code, Rust, Tauri, Flask, Spring Boot, Keycloak, MUI, pandas and khaiii.
- 52 of 96 have at least one checkbox; among those, the median is 5 boxes.
- Non-blank lines: median 20, minimum 2, maximum 94.

**Minimal "summary + test plan" family:**
- React: Summary / How did you test this change? It asks for "the exact commands you ran and their output, screenshots / videos", and warns that empty PRs will likely be closed — [react](https://raw.githubusercontent.com/facebook/react/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- The same shape appears in [jest](https://raw.githubusercontent.com/jestjs/jest/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [react-native](https://raw.githubusercontent.com/facebook/react-native/HEAD/.github/PULL_REQUEST_TEMPLATE.md) (which adds a categorized Changelog line), [tailwindcss](https://raw.githubusercontent.com/tailwindlabs/tailwindcss/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [ruff](https://raw.githubusercontent.com/astral-sh/ruff/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [uv](https://raw.githubusercontent.com/astral-sh/uv/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [bun](https://raw.githubusercontent.com/oven-sh/bun/HEAD/.github/pull_request_template.md) (two headings, 3 lines) and [turborepo](https://raw.githubusercontent.com/vercel/turborepo/HEAD/.github/pull_request_template.md).

**Problem → Solution → test family:**
- Supabase: Problem / Solution / Review instructions (a numbered procedure for the reviewer) / Checklist — [supabase](https://raw.githubusercontent.com/supabase/supabase/HEAD/.github/pull_request_template.md).
- n8n: Summary / Why / How to test / Related tickets / Review-merge checklist. The first checklist line has the author take responsibility for code they have seen and run — [n8n](https://raw.githubusercontent.com/n8n-io/n8n/HEAD/.github/pull_request_template.md).
- Strapi: What does it do? / Why is it needed? / How to test it? / Related issues — [strapi](https://raw.githubusercontent.com/strapi/strapi/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Grafana: What is this feature? / Why do we need it? / Who is it for? / Which issues? / Special notes for reviewer — [grafana](https://raw.githubusercontent.com/grafana/grafana/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Fluent UI: Previous Behavior / New Behavior / Related Issues — [fluentui](https://raw.githubusercontent.com/microsoft/fluentui/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Angular and NestJS: current behavior / new behavior / breaking change, plus a PR-type checklist — [angular](https://raw.githubusercontent.com/angular/angular/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [nest](https://raw.githubusercontent.com/nestjs/nest/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**Motivation / Modifications / Result** (LINE's Armeria). The Result section holds `Closes #N` and says what users will experience after the merge. The guide says this shape helps maintainers write release notes — [armeria template](https://raw.githubusercontent.com/line/armeria/HEAD/.github/PULL_REQUEST_TEMPLATE.md); [Armeria developer guide](https://armeria.dev/community/developer-guide).

**Kubernetes:**
- Sections: kind label (`/kind bug|feature|…`) / what + why / linked issues / special notes for reviewer / a `release-note` code block (write NONE if not user-facing) / AI usage disclosure (YES/NO + how) — [kubernetes](https://raw.githubusercontent.com/kubernetes/kubernetes/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Helm uses a lighter Kubernetes-style form: what / why / special notes, plus 3 "if applicable" boxes — [helm](https://raw.githubusercontent.com/helm/helm/HEAD/.github/pull_request_template.md).

**Release-note-driven templates:**
- Prometheus: a release-notes block in the form `[TYPE] Component: description`, or NONE — [prometheus](https://raw.githubusercontent.com/prometheus/prometheus/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Mattermost: a release-note block is always required. It is needed for API/config changes, schema migrations, user-visible changes and deprecations; otherwise write NONE — [mattermost](https://raw.githubusercontent.com/mattermost/mattermost/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Electron: a `Notes:` line for app developers — [electron](https://raw.githubusercontent.com/electron/electron/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Zed: a `Release Notes:` line — [zed](https://raw.githubusercontent.com/zed-industries/zed/HEAD/.github/pull_request_template.md).
- Moby: an optional one-sentence changelog in present-tense imperative — [moby](https://raw.githubusercontent.com/moby/moby/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Ant Design: a bilingual English/Chinese changelog table — [ant-design](https://raw.githubusercontent.com/ant-design/ant-design/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Changesets: TanStack Query has a "Release Impact" pair of boxes (changeset added vs docs/CI-only) — [TanStack query](https://raw.githubusercontent.com/TanStack/query/HEAD/.github/pull_request_template.md). Astro asks for a changeset — [astro](https://raw.githubusercontent.com/withastro/astro/HEAD/.github/PULL_REQUEST_TEMPLATE.md). Backstage does the same — [backstage](https://raw.githubusercontent.com/backstage/backstage/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**Risk, rollback and migration (rare but concrete):**
- Superset lists DB-migration boxes: migration is atomic, supports rollback and is backwards-compatible; upgrade and downgrade were tested; runtime and downtime estimates are given — [superset](https://raw.githubusercontent.com/apache/superset/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Terraform has "Rollback Plan" and "Changes to Security Controls" sections — [terraform](https://raw.githubusercontent.com/hashicorp/terraform/HEAD/.github/pull_request_template.md).
- Kibana's "Identify risks" section asks for severity and mitigation per risk — [kibana](https://raw.githubusercontent.com/elastic/kibana/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Envoy uses labelled one-line fields: Commit Message / Additional Description / Risk Level / Testing / Docs Changes / Release Notes / Platform Specific Features — [envoy](https://raw.githubusercontent.com/envoyproxy/envoy/HEAD/PULL_REQUEST_TEMPLATE.md).
- Directus's checklist includes "Database migration added" and "Environment variables documented" — [directus](https://raw.githubusercontent.com/directus/directus/HEAD/.github/pull_request_template.md).

**Screenshot rules:**
- GitLab's default MR template has a Before/After table. It says screenshots are required for UI changes and strongly recommended otherwise. It also offers an optional viewport-size table (xs/sm/md/lg/xl) — [GitLab Default.md](https://gitlab.com/gitlab-org/gitlab/-/raw/master/.gitlab/merge_request_templates/Default.md).
- Django requires light and dark mode screenshots for UI changes — [django](https://raw.githubusercontent.com/django/django/HEAD/.github/pull_request_template.md).
- Cal.com strongly recommends a video or image demo of before/after — [cal.com](https://raw.githubusercontent.com/calcom/cal.com/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Cypress asks "How has the user experience changed?", with before/after screenshots or "No change" — [cypress](https://raw.githubusercontent.com/cypress-io/cypress/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Airflow asks for before/after screenshots or a recording for UI changes — [airflow](https://raw.githubusercontent.com/apache/airflow/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Immich puts screenshots in a collapsed `<details>` block — [immich](https://raw.githubusercontent.com/immich-app/immich/HEAD/.github/pull_request_template.md).

**Reviewer-focus sections:**
- GitHub CLI: Key points (tradeoffs accepted, alternatives rejected) and Notes for reviewers (where review should start, what you are unsure about) — [cli/cli](https://raw.githubusercontent.com/cli/cli/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Directus: "Review Notes / Questions / Concerns" — [directus](https://raw.githubusercontent.com/directus/directus/HEAD/.github/pull_request_template.md).
- Prisma: "Notes for the reviewer", including follow-ups intentionally deferred — [prisma](https://raw.githubusercontent.com/prisma/prisma/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- ESLint: "Is there anything you'd like reviewers to focus on?" — [eslint](https://raw.githubusercontent.com/eslint/eslint/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**Follow-up / not-done sections (rare):**
- Vercel AI SDK has a "Future Work" section — [vercel/ai](https://raw.githubusercontent.com/vercel/ai/HEAD/.github/pull_request_template.md).
- Nextcloud has a "TODO" section — [nextcloud](https://raw.githubusercontent.com/nextcloud/server/HEAD/.github/pull_request_template.md).
- PostHog's collapsed agent block has a "Follow-ups" field — [posthog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md).

**Gatekeeping preambles, aimed at outside contributors:**
- SQLAlchemy and Alembic auto-close PRs that don't reference an issue labelled `open for pull requests` — [sqlalchemy](https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/HEAD/.github/pull_request_template.md), [alembic](https://raw.githubusercontent.com/sqlalchemy/alembic/HEAD/.github/pull_request_template.md).
- Pydantic requires the author to be assigned to the issue — [pydantic](https://raw.githubusercontent.com/pydantic/pydantic/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- TypeScript requires an issue in the Backlog milestone — [TypeScript](https://raw.githubusercontent.com/microsoft/TypeScript/HEAD/.github/pull_request_template.md).
- LangChain requires an approved, assigned issue — [langchain](https://raw.githubusercontent.com/langchain-ai/langchain/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Legal and DCO boilerplate: Sentry has a "Legal Boilerplate" section — [sentry](https://raw.githubusercontent.com/getsentry/sentry/HEAD/.github/PULL_REQUEST_TEMPLATE.md). Node embeds the full DCO 1.1 text in a comment — [node](https://raw.githubusercontent.com/nodejs/node/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**Long checklist templates:**
- Home Assistant: 21 boxes, and asks for exactly one type-of-change box. If multiple boxes apply, it says to split the PR — [home-assistant](https://raw.githubusercontent.com/home-assistant/core/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Ant Design: 17 type boxes — [ant-design](https://raw.githubusercontent.com/ant-design/ant-design/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Istio: 17 area boxes for routing review — [istio](https://raw.githubusercontent.com/istio/istio/HEAD/.github/pull_request_template.md).
- Argo CD: 14 boxes — [argo-cd](https://raw.githubusercontent.com/argoproj/argo-cd/HEAD/.github/pull_request_template.md).

**Checkbox semantics differ by project:**
- Vercel AI says not to edit the list and to leave inapplicable items unchecked — [vercel/ai](https://raw.githubusercontent.com/vercel/ai/HEAD/.github/pull_request_template.md).
- Cypress asks for `[na]` — [cypress](https://raw.githubusercontent.com/cypress-io/cypress/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Electron says to remove items that don't apply — [electron](https://raw.githubusercontent.com/electron/electron/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- PostHog deliberately uses plain bullets instead of checkboxes, because GitHub counts every checkbox in the body as an open task — [posthog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md).

**Projects with no template at the standard paths** (as of 2026-10-29):
- FastAPI, Mastodon, Vue core, Nuxt, Playwright, Excalidraw, shadcn/ui, openai/codex, anthropics/claude-code, Discourse, Ghostty, and daangn's stackflow and seed-design. My script tried `.github/`, root and `docs/` with both filename cases, plus two `.github/PULL_REQUEST_TEMPLATE/` filenames. It could not list `.github/` through the API because of the unauthenticated rate limit.
- Mastodon instead documents PR-description rules in CONTRIBUTING: write for users and admins, not developers; the PR title becomes the main-branch commit and feeds the changelog; start titles with Add/Change/Deprecate/Remove/Fix — [Mastodon CONTRIBUTING](https://raw.githubusercontent.com/mastodon/mastodon/HEAD/CONTRIBUTING.md).
- FastAPI's contributing doc has no PR template section — [FastAPI contributing.md](https://raw.githubusercontent.com/fastapi/fastapi/HEAD/docs/en/docs/contributing.md).

### Inferences
- The common core is **what + why + linked issue + how verified**. The current AGENTS.md §6 body (무엇을 왜 / 검증 결과 / `Closes #N`) already matches it.
- **호출 흐름** is project-specific, the closest analogue being PostHog's before/after diagram rule for architecture changes. **못 한 것** is rare in OSS (9/96 have any follow-up/TODO section), but it fits AGENTS.md §7's "못 한 것과 그 이유" reporting rule.
- Compared with the OSS core, the 믿집 draft lacks four things:
  1. A UI-screenshot rule. 30% of OSS templates have one, and GitLab requires screenshots for UI changes. The team's 360px check could carry it.
  2. An AI-use line, now in 30% of templates.
  3. A reviewer-focus line, in 30% of OSS and 12/15 Korean bootcamp templates.
  4. A conditional migration/rollback line for Alembic. This is rare in OSS, but this stack runs migrations up→down→up in CI.
- Type-of-change checkbox lists (8/96) are better handled with labels. Storybook and Kibana move this to labels.

### Gaps
- The tally is keyword- and heading-based. Guidance written only inside HTML comments counts in the first tally but not in the heading tally. I did not hand-code all 96 files section by section.
- For the "no template" repos, I couldn't rule out a non-standard filename inside a `PULL_REQUEST_TEMPLATE/` subdirectory, because the GitHub API was rate-limited (60 requests/hour unauthenticated; reset 14:30 UTC).
- I did not verify Vercel's org-wide default template (a `.github` repo), beyond `vercel/next.js`, `vercel/turborepo` and `vercel/ai`.

## 2. Korean company / team PR templates and rules — sections, tone, review-priority marking (Pn 룰), screenshot rules

### Takeaway
Korean bootcamp team templates are tiny: a median of about 12 lines and 2–5 sections. They almost always have "연관 이슈 + 작업 내용 + 리뷰어에게 / 참고사항". They almost never have a verification section or an AI-use line, and screenshots are optional. Korean company OSS repos (Toss, NAVER, Kakao, LINE, NHN) mostly use short English templates. Some are bilingual (Kakao). The Pn rule (P1–P5 review-comment priority) comes from 뱅크샐러드's 2020 code-review-culture post, which pairs it with a D-n review-deadline rule and a context-heavy PR template.

### Cited Findings
**15 우아한테크코스 team templates** (`woowacourse-teams`, 2022–2025; fetched 2026-10-29):
- Linked issue (`close #`, `resolved #`, `Closed`): 13/15. Only hang-log and zipgo lack one.
- 작업 내용 / summary: 15/15.
- 리뷰어 요청 / 참고 / 논의 section: 12/15.
- Screenshots: 3/15 (emmsale optional, ddangkong "Test Screenshot", bottari optional Before/After table).
- Any test/verification item: 1/15 (ddangkong's "테스트가 전부 통과되었나요?" box).
- Why/As-Is: 2/15 (mouda "PR의 목적", ddangkong As-Is/To-Be).
- AI-use line: 0/15.

Sources: [2022-gong-check](https://raw.githubusercontent.com/woowacourse-teams/2022-gong-check/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [2022-moamoa](https://raw.githubusercontent.com/woowacourse-teams/2022-moamoa/HEAD/.github/pull_request_template.md), [2023-baton](https://raw.githubusercontent.com/woowacourse-teams/2023-baton/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [2023-dong-gle](https://raw.githubusercontent.com/woowacourse-teams/2023-dong-gle/HEAD/.github/pull_request_template.md), [2023-emmsale](https://raw.githubusercontent.com/woowacourse-teams/2023-emmsale/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [2023-hang-log](https://raw.githubusercontent.com/woowacourse-teams/2023-hang-log/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [2023-zipgo](https://raw.githubusercontent.com/woowacourse-teams/2023-zipgo/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [2024-bang-ggood](https://raw.githubusercontent.com/woowacourse-teams/2024-bang-ggood/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [2024-corea](https://raw.githubusercontent.com/woowacourse-teams/2024-corea/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [2024-ddangkong](https://raw.githubusercontent.com/woowacourse-teams/2024-ddangkong/HEAD/.github/pull_request_template.md), [2024-friendogly](https://raw.githubusercontent.com/woowacourse-teams/2024-friendogly/HEAD/.github/pull_request_template.md), [2024-mouda](https://raw.githubusercontent.com/woowacourse-teams/2024-mouda/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [2024-staccato](https://raw.githubusercontent.com/woowacourse-teams/2024-staccato/HEAD/.github/pull_request_template.md), [2025-bottari](https://raw.githubusercontent.com/woowacourse-teams/2025-bottari/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [2025-coffee-shout](https://raw.githubusercontent.com/woowacourse-teams/2025-coffee-shout/HEAD/.github/pull_request_template.md).

**Patterns in those Korean team templates:**
- Emoji headings: 🛠️ Issue / ✅ Tasks / 📝 Note in dong-gle; #️⃣ 연관된 이슈 / 📝 작업 내용 / 💬 리뷰어 요구사항 in emmsale; ⭐️ / 🚩 / 🛠️ / 🙂 / 📋 in staccato.
- 예상 vs 실제 소요 시간: emmsale; "Time Difference" in dong-gle.
- As-Is / To-Be: ddangkong.
- Process self-checks: ddangkong checks tests passed, all commits pushed, merge branch, Assignee and Label set. coffee-shout checks the merge target branch (dev).
- Platform prefix in titles: `[BE|FE] issue00: 제목` in moamoa; `[AN]` / `[BE]` / `[ALL]` in bottari.
- "없으면 삭제해 주세요" (delete the section if empty): friendogly.
- Sources: the [dong-gle](https://raw.githubusercontent.com/woowacourse-teams/2023-dong-gle/HEAD/.github/pull_request_template.md), [emmsale](https://raw.githubusercontent.com/woowacourse-teams/2023-emmsale/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [staccato](https://raw.githubusercontent.com/woowacourse-teams/2024-staccato/HEAD/.github/pull_request_template.md), [ddangkong](https://raw.githubusercontent.com/woowacourse-teams/2024-ddangkong/HEAD/.github/pull_request_template.md), [coffee-shout](https://raw.githubusercontent.com/woowacourse-teams/2025-coffee-shout/HEAD/.github/pull_request_template.md), [moamoa](https://raw.githubusercontent.com/woowacourse-teams/2022-moamoa/HEAD/.github/pull_request_template.md), [bottari](https://raw.githubusercontent.com/woowacourse-teams/2025-bottari/HEAD/.github/PULL_REQUEST_TEMPLATE.md) and [friendogly](https://raw.githubusercontent.com/woowacourse-teams/2024-friendogly/HEAD/.github/pull_request_template.md) templates above.

**Toss OSS:**
- es-toolkit:
  - Its title format is `<type>[function names]: <description>`.
  - Per-change-type checklists sit in a comment.
  - It says PR descriptions from external contributors must be written by a human.
  - It says not to paste test output, because CI runs the suite; benchmarks are the exception because CI doesn't run them.
  - Docs must be changed in all four languages, including Korean.
  - [es-toolkit](https://raw.githubusercontent.com/toss/es-toolkit/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- slash and suspensive: Overview + one-box PR checklist — [slash](https://raw.githubusercontent.com/toss/slash/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [suspensive](https://raw.githubusercontent.com/toss/suspensive/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- es-hangul: the same shape, with a Korean comment — [es-hangul](https://raw.githubusercontent.com/toss/es-hangul/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- frontend-fundamentals: Key Changes + Before/After comparison table — [frontend-fundamentals](https://raw.githubusercontent.com/toss/frontend-fundamentals/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- overlay-kit: a long generic template with 11 boxes (Description / Changes / Motivation / How tested / Screenshots / Types / Checklist / Further Comments) — [overlay-kit](https://raw.githubusercontent.com/toss/overlay-kit/HEAD/.github/pull_request_template.md).
- react-simplikit: Overview + 4 tooling boxes (tests, `yarn run fix`, coverage, JSDoc) — [react-simplikit](https://raw.githubusercontent.com/toss/react-simplikit/HEAD/.github/pull_request_template.md).

**NAVER OSS:**
- billboard.js and egjs-flicking use only Issue / Details — [billboard.js](https://raw.githubusercontent.com/naver/billboard.js/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [egjs-flicking](https://raw.githubusercontent.com/naver/egjs-flicking/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- fixture-monkey: Summary / Description / How Has This Been Tested? / Is the Document updated? — [fixture-monkey](https://raw.githubusercontent.com/naver/fixture-monkey/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**NHN TOAST UI Editor:** the title carries the issue type and closing type, e.g. `feat: add new feature (close #111)`, with `close` / `fix` / `ref` closing types. It has a 6-box checklist — [tui.editor](https://raw.githubusercontent.com/nhn/tui.editor/HEAD/docs/PULL_REQUEST_TEMPLATE.md).

**Kakao OSS:**
- khaiii: bilingual Korean/English headings (설명 / 개발자를 위한 가이드 / 체크 리스트), with a friendly line saying they love Hangul. Its boxes cover the develop branch, tests and lint — [khaiii](https://raw.githubusercontent.com/kakao/khaiii/HEAD/.github/pull_request_template.md).
- kakao_flutter_sdk: bilingual 설명 / 관련 이슈 / 체크리스트 — [kakao_flutter_sdk](https://raw.githubusercontent.com/kakao/kakao_flutter_sdk/HEAD/.github/pull_request_template.md).
- actionbase (newer): Summary / Changes / How to Test, plus an "AI Assistance" box with a `Tool / model:` line. It is the only Korean-company template in my set with an AI line — [actionbase](https://raw.githubusercontent.com/kakao/actionbase/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**뱅크샐러드 Pn 룰** (blog post dated 2020-11-24):
- The levels:
  - P1 꼭 반영해주세요 (request changes)
  - P2 적극적으로 고려해주세요 (request changes)
  - P3 웬만하면 반영해 주세요 (comment; accept it, explain why not, or plan it in a ticket)
  - P4 반영해도 좋고 넘어가도 좋습니다 (approve)
  - P5 그냥 사소한 의견입니다 (approve)
- Why they introduced it: online review carries only text, so tone is easily misread and a light remark can become a blocker. The levels make the reviewer's intent explicit, and the team also uses them in Slack.
- D-n rule: the author states a review deadline. D-0 means urgent (outage or build failure); D-2 is the most common; D-3 to D-5 are for low priority.
- PR template content: product plan, tech plan, changes, design, and what was tested vs still needs testing. It assumes the reviewer has no context. Authors link spec and Figma, and a GIF is recommended for complex interactions.
- PR size: a 1,000-line limit that excludes tests. Over time, PRs settled at about 200–300 lines and reviews finished in 1–2 days.
- Source: [뱅크샐러드 코드 리뷰 문화](https://blog.banksalad.com/tech/banksalad-code-review-culture/).

**뱅크샐러드 deploy-process post** (2020-02-29):
- Only `master` is long-lived, and merges are squash merges, so one PR is one revertible commit.
- A PR merges after CI (lint + unit tests) and approval from at least one service owner. Each repo has at least 3 owners.
- One PR should be a deployable unit.
- The post does not mention PR templates.
- Source: [하루에 1000번 배포하는 조직 되기](https://blog.banksalad.com/tech/become-an-organization-that-deploys-1000-times-a-day/).

**LINE Engineering** (2018-12-05, LINE NOW QA engineer):
- Authors should explain why, how, and the risks; state what was done and tested; and say where reviewers should focus.
- Use GitHub issue/PR templates and attach screenshots.
- Keep each PR to one idea and send PRs early.
- The post cites a Cisco study: reviewing 300–400 lines in 60–90 minutes finds 70–90% of defects.
- Reviewers should praise generously.
- Source: [효과적인 코드 리뷰를 위해서](https://engineering.linecorp.com/ko/blog/effective-codereview).

**Kakao tech blog:** a post titled "효과적인 코드리뷰를 위한 리뷰어의 자세" (by kay.gw, in a 2022 onboarding context) exists. Its body is JavaScript-rendered, and neither WebFetch nor curl could read it, so I cite no content from it — [tech.kakao.com/posts/498](https://tech.kakao.com/posts/498).

### Inferences
- A 4–6 person Korean student team will expect a short template with emoji or Korean headings.
- The bootcamp norm leaves out evidence of verification. That is the weakest point of the norm and exactly where 믿집's AGENTS.md is stricter (local vs CI vs not done). The template should keep that strictness but in very few lines.
- Pn fits review **comments**, not the PR body. Put it in a review-comment convention: AGENTS.md or CONTRIBUTING, plus saved replies. D-n can be an optional line in the PR body (리뷰 기한), but with a 2-day branch lifetime (AGENTS.md §6), D-1 is effectively the default.
- Screenshot norms: Korean templates make screenshots optional, while GitLab makes them required for UI changes. 믿집 already has a concrete UI check (360px, 40px touch targets). So "UI가 바뀐 경우 360px 전/후 스크린샷" is a natural, conditional requirement.

### Gaps
- I couldn't retrieve posts on PR templates or review rules from 우아한형제들 (techblog.woowahan.com returned a "보안 위배 접근 제한" page to curl), 토스 (toss.tech), 당근 (Medium returned a Cloudflare challenge), 쏘카 (my guessed URL 404'd), 컬리 (no response), or velog/tistory bootcamp posts. The WebSearch budget was exhausted, so I couldn't discover their URLs. The 우아한테크코스 team repos stand in for "부트캠프 팀 프로젝트 템플릿".
- I couldn't read the Kakao reviewer-attitude article body (client-rendered).
- I found no primary source showing Pn adoption outside 뱅크샐러드. Its wide Korean adoption is folk knowledge that I didn't verify.

## 3. GitHub features for PR records (templates, query params, forms, closing keywords, draft PRs, labels, milestones, CODEOWNERS, required reviewers, comment conventions, saved replies)

### Takeaway
GitHub PR templates are plain Markdown only; issue forms "are not supported for pull requests". You can keep multiple templates in a `PULL_REQUEST_TEMPLATE/` folder, but you pick one with a `?template=` URL parameter, so a single default file suits a small team best. `Closes #N` works only when the PR targets the default branch. Rulesets and branch protection can require approvals, Code Owner review, resolved conversations and passing checks. Draft PRs can't be merged and don't ping code owners. Squash-merge settings decide whether the PR title alone or the title plus body becomes the commit message.

### Cited Findings
**Template locations and selection:**
- A template can live at the repo root, in `docs/`, or in `.github/` as `pull_request_template.md`.
- Multiple templates go in a `PULL_REQUEST_TEMPLATE/` subdirectory, and you select one with the `template` query parameter.
- Templates become available once merged to the default branch. Org-level defaults are possible through a default community health file.
- Source: [GitHub Docs: Creating a PR template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository).

**Query parameters:**
- Supported: `quick_pull`, `title`, `body`, `labels`, `milestone`, `assignees`, `projects`, `template`.
- Example: `…/compare/main...my-branch?quick_pull=1&template=issue_template.md`.
- Insufficient permission gives 404; an over-long URL gives 414.
- Source: [GitHub Docs: Query parameters for PRs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/using-query-parameters-to-create-a-pull-request).

**Forms:**
- GitHub says outright that issue forms are not supported for pull requests and that you should use PR templates instead.
- Issue forms themselves are in public preview.
- Source: [GitHub Docs: Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms).

**Closing keywords:**
- Keywords: close/closes/closed/fix/fixes/fixed/resolve/resolves/resolved. They are case-insensitive and may take a colon.
- They are interpreted only when the PR targets the default branch.
- Cross-repo syntax is `Fixes owner/repo#100`.
- Multiple issues need the full syntax each time (`Resolves #10, resolves #123`).
- Keywords in commit messages also close issues on merge to the default branch, but that PR is then not listed as a linked PR.
- Source: [GitHub Docs: Linking a PR to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

**Draft PRs:**
- Draft PRs cannot be merged.
- Code owners are not auto-requested until the PR is marked ready for review.
- Source: [GitHub Docs: About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

**CODEOWNERS:**
- The file can live in `.github/`, the repo root or `docs/`; GitHub uses the first one it finds in that order. It must be on the PR's base branch.
- The last matching pattern wins.
- Owners need explicit write access. Paths are case sensitive. The file must be under 3 MB.
- "Require review from Code Owners" is satisfied by any one listed owner.
- Draft PRs don't request owners.
- Source: [GitHub Docs: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

**Ruleset rules:**
- "Require a pull request before merging" has these sub-options: required approvals count, dismiss stale approvals on new commits, require Code Owner review, require approval of the most recent push by someone else, and require conversation resolution.
- Required status checks can be strict (branch must be up to date) or loose.
- Source: [GitHub Docs: Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).

**Squash commit message options:**
- Default: for a single commit, that commit's message; for several, the PR title plus a list of commits.
- PR title only.
- PR title and commit details.
- PR title and description.
- Source: [GitHub Docs: Configuring commit squashing](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests).

**Automatically generated release notes:**
- They list merged PRs and contributors, grouped by label categories in `.github/release.yml`.
- You can exclude by labels or authors; a `"*"` category catches everything else.
- Source: [GitHub Docs: Automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes).

**Saved replies:**
- Saved replies are per user (tied to the personal account, usable across repos), with a maximum of 100.
- Source: [GitHub Docs: About saved replies](https://docs.github.com/en/get-started/writing-on-github/working-with-saved-replies/about-saved-replies).

**Co-author trailers:**
- Format: one `Co-authored-by: NAME <email>` line per co-author, after a blank line.
- The email must be linked to the person's GitHub account for credit.
- Source: [GitHub Docs: Commit with multiple authors](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors).

**Copilot PR summary:**
- It can insert an AI summary into the description or a comment.
- It ignores existing description content, so start blank, and review the summary before posting.
- Source: [GitHub Docs: Copilot PR summary](https://docs.github.com/en/copilot/how-tos/use-copilot-for-common-tasks/create-a-pr-summary).

**Conventional Comments:**
- Format: `<label> [decorations]: <subject>`, followed by an optional discussion.
- Labels: praise, nitpick, suggestion, issue, todo, question, thought, chore, note; optional typo, polish, quibble.
- Decorations: `(blocking)`, `(non-blocking)`, `(if-minor)`, plus small org-defined ones such as security, test or ux.
- Source: [conventionalcomments.org](https://conventionalcomments.org/).
- GitLab reviewers use Conventional Comments and mark optional suggestions as non-blocking. Once only non-blocking comments remain, the MR can move on. Authors push review fixes as separate commits and move out-of-scope items to follow-up issues — [GitLab code review guidelines](https://docs.gitlab.com/development/code_review/).

**Labels and bots in templates:**
- Kubernetes uses `/kind …` commands. `/hold` and a `WIP` title prefix add do-not-merge labels — [kubernetes template](https://raw.githubusercontent.com/kubernetes/kubernetes/HEAD/.github/PULL_REQUEST_TEMPLATE.md); [k8s PR guide](https://raw.githubusercontent.com/kubernetes/community/HEAD/contributors/guide/pull-requests.md).
- Storybook maintainers apply `ci:*`, `qa:needed` / `qa:skip` and exactly one changelog-category label — [storybook](https://raw.githubusercontent.com/storybookjs/storybook/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Kibana uses `release_note:*` and `backport:*` labels — [kibana](https://raw.githubusercontent.com/elastic/kibana/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Nextcloud has checkboxes for "Labels added" and "Milestone added" — [nextcloud](https://raw.githubusercontent.com/nextcloud/server/HEAD/.github/pull_request_template.md).
- Grafana adds the label "add to what's new" for release docs — [grafana](https://raw.githubusercontent.com/grafana/grafana/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**Draft-first conventions:**
- PyTorch asks for every PR to be opened as a draft — [pytorch](https://raw.githubusercontent.com/pytorch/pytorch/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- PostHog's agent rules make drafts the default, because drafts run only a narrow CI subset — [posthog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md).
- Fluent UI promotes a draft to Ready for Review, which auto-assigns reviewers — [fluentui](https://raw.githubusercontent.com/microsoft/fluentui/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Rails, by contrast, asks contributors **not** to open drafts, because drafts still notify every watcher — [rails](https://raw.githubusercontent.com/rails/rails/HEAD/.github/pull_request_template.md).
- Home Assistant switches a PR to draft while CI failures are being fixed — [HA perfect PR](https://contributors.home-assistant.io/start/pull-requests/).

### Inferences
**Recommended setup for 믿집** (team of 4–6, `main` only, squash merge, 1 approval):
- **One** `.github/pull_request_template.md`. Skip `PULL_REQUEST_TEMPLATE/` variants: they need `?template=` URLs nobody will remember. If a docs-only or decision variant is wanted later, put the link in AGENTS.md.
- A ruleset on `main`:
  - 1 approval.
  - Dismiss stale approvals.
  - Require conversation resolution. This pairs well with Pn: P1 and P2 threads must be resolved.
  - Required CI checks.
  - Optionally CODEOWNERS (`/backend/`, `/frontend/`, `/docs/adr/`) with "Require review from Code Owners". Any one owner suffices, so it won't deadlock a small team.
- AI agents should open PRs as **drafts**. A human marks the PR ready after reading the diff; that is also when code owners get requested.
- Labels (`area:web/api/calc/agent/worker/db/infra/docs`, plus type) should replace any type-of-change checkboxes. A `.github/release.yml` can turn merged PRs into per-milestone (발표) notes.
- Saved replies (per member, up to 100) can hold Pn or Conventional-Comment prefixes. They can't be shared org-wide, so the prefix list itself belongs in AGENTS.md.

### Gaps
- None of the fetched pages said which GitHub plans support draft PRs, rulesets or required reviews on **private** repos. If 믿집's repo is private under a Free org/account, check enforceability in repo settings.
- I didn't confirm whether HTML comments in the PR body are carried into the squash commit message under "PR title and description", or whether GitHub appends `(#PR)` to squash titles.
- I didn't verify whether GitHub shows a template-picker UI for PR templates (as it does for issues); the docs describe only the query parameter.

## 4. How to document verification honestly, and how to describe AI-agent involvement (2025–2026 practice)

### Takeaway
2025–2026 templates are converging on a few rules:
- Report **only actions actually performed and results actually observed**.
- Don't paste CI-covered test output or pass counts; link the CI run instead.
- Say explicitly what you did **not** test.
- For UI changes, show before/after.

For AI, 29/96 templates now carry some disclosure. The strong ones ask for the **extent and purpose** of AI use and a named, accountable human, not just a tool name. The default "🤖 Generated with Claude Code" and `Co-Authored-By` trailer are attribution, not disclosure; Rust calls them bad examples. Several projects require the PR description itself to be written by a human.

### Cited Findings
**Honest verification:**
- GitHub CLI:
  - Report only actions you actually performed, in factual first person.
  - Don't present planned or expected scenarios as testing.
  - Automated results such as unit tests and coverage don't belong in the description, because CI shows them.
  - If you didn't exercise the change, write `Not tested` and say why.
  - Screenshots or GIFs are preferred, and Given/When/Then is allowed only for steps actually executed.
  - [cli/cli](https://raw.githubusercontent.com/cli/cli/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- PostHog:
  - Agents must not claim manual testing they haven't done. They state what they couldn't do and list only the automated tests they actually ran.
  - Don't recite pass counts for suites CI runs; link the evidence and say what you didn't check.
  - A "Test rationale" names the regression and the closest existing test.
  - [posthog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md).
- Rust's rustc-dev-guide:
  - Don't report which UI tests you ran, because CI runs them; do report manual testing or benchmarks.
  - Re-read the whole diff, not your conversation with the agent.
  - It recommends a different model for adversarial local review.
  - [rustc-dev-guide LLM writing guidance](https://raw.githubusercontent.com/rust-lang/rustc-dev-guide/HEAD/src/llm-guidance/writing.md).
- es-toolkit: no test output, because CI runs it; benchmarks pasted because CI doesn't — [es-toolkit](https://raw.githubusercontent.com/toss/es-toolkit/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Vercel AI SDK: "End-to-End Verification" explains how the change was verified end to end and excludes unit/integration tests and lint — [vercel/ai](https://raw.githubusercontent.com/vercel/ai/HEAD/.github/pull_request_template.md).
- Storybook's manual-testing section is mandatory, and you must state explicitly if none is needed. It describes how a *separate maintainer* should verify, not how you did — [storybook](https://raw.githubusercontent.com/storybookjs/storybook/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- **The opposite school** (list commands): React wants the exact commands run and their output — [react](https://raw.githubusercontent.com/facebook/react/HEAD/.github/PULL_REQUEST_TEMPLATE.md). Prisma wants the suites you ran listed, with the reason for each — [prisma](https://raw.githubusercontent.com/prisma/prisma/HEAD/.github/PULL_REQUEST_TEMPLATE.md). Docker Compose has per-command checkboxes (`make test`, `make e2e-compose`, `make lint`, `make fmt`, "Manually tested (describe)") — [docker/compose](https://raw.githubusercontent.com/docker/compose/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Accountability lines:
  - Home Assistant: the author understands the code and can explain how it works; generated code was reviewed — [home-assistant](https://raw.githubusercontent.com/home-assistant/core/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - n8n: seen it, run it, take responsibility — [n8n](https://raw.githubusercontent.com/n8n-io/n8n/HEAD/.github/pull_request_template.md).
  - Electron: built and tested; reviewed and verified — [electron](https://raw.githubusercontent.com/electron/electron/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Cal.com: self-review — [cal.com](https://raw.githubusercontent.com/calcom/cal.com/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Zed: reviewed my diff for quality, security, reliability and performance — [zed](https://raw.githubusercontent.com/zed-industries/zed/HEAD/.github/pull_request_template.md).
- Migration and rollback evidence:
  - Superset: upgrade *and* downgrade tested, rollback supported, runtime estimate — [superset](https://raw.githubusercontent.com/apache/superset/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Terraform: a Rollback Plan section — [terraform](https://raw.githubusercontent.com/hashicorp/terraform/HEAD/.github/pull_request_template.md).
  - GitLab: database MRs must carry the information DB reviewers need, and DB changes ship before the feature that depends on them — [GitLab code review](https://docs.gitlab.com/development/code_review/).

**AI disclosure patterns** in templates (29/96 mention AI; 12/96 have a visible AI heading):
- (a) **Binary choice:**
  - Django: exactly one of "No AI tools were used" or "AI used, tools disclosed, output fully reviewed". It also bans requesting an automated AI review — [django](https://raw.githubusercontent.com/django/django/HEAD/.github/pull_request_template.md).
  - pandas: exactly one of two boxes. The "used AI" box requires naming the tool, model version and effort setting, e.g. `claude opus 4.8 (xhigh)` — [pandas](https://raw.githubusercontent.com/pandas-dev/pandas/HEAD/.github/PULL_REQUEST_TEMPLATE.md); [pandas automated contributions policy](https://pandas.pydata.org/docs/dev/development/contributing.html).
  - Also Prettier — [prettier](https://raw.githubusercontent.com/prettier/prettier/HEAD/.github/PULL_REQUEST_TEMPLATE.md), Nextcloud — [nextcloud](https://raw.githubusercontent.com/nextcloud/server/HEAD/.github/pull_request_template.md), and Kakao actionbase (`Tool / model:`) — [actionbase](https://raw.githubusercontent.com/kakao/actionbase/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- (b) **Extent/purpose lists:**
  - ESLint: four boxes — didn't use AI; AI for the description or translation; AI to understand the codebase; AI wrote files and I reviewed them — [eslint](https://raw.githubusercontent.com/eslint/eslint/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - scikit-learn: keep the uses that apply — code generation, test/benchmark generation, documentation, research — [scikit-learn](https://raw.githubusercontent.com/scikit-learn/scikit-learn/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - NumPy: tools, how they were used, and which code or text is AI-generated; all interactions with reviewers must be human — [numpy](https://raw.githubusercontent.com/numpy/numpy/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Kubernetes: YES/NO plus how — [kubernetes](https://raw.githubusercontent.com/kubernetes/kubernetes/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Immich: to what degree an LLM was used — [immich](https://raw.githubusercontent.com/immich-app/immich/HEAD/.github/pull_request_template.md).
  - Docker Compose: tool and extent — [docker/compose](https://raw.githubusercontent.com/docker/compose/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Moby: tools and roughly how much of the work — [moby](https://raw.githubusercontent.com/moby/moby/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- (c) **Structured agent context:**
  - PostHog's "🤖 Agent context" section:
    - Autonomy: human-driven (agent-assisted) vs fully autonomous.
    - Agent: tool plus exact model.
    - Skills invoked.
    - A collapsed block with Session / Decisions / Follow-ups / Read closely.
  - PostHog's agent rules:
    - Paraphrase prompts, never paste them.
    - Assign the directing human as DRI.
    - Don't add a human Co-authored-by just for attribution.
    - Agent PRs always need human review.
  - [posthog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md).
  - GitHub CLI's "Authorship and follow-up" section asks two things. Who wrote this: a human; an agent under close human direction; or an agent independently. Who answers review comments: a named human; an agent drafting replies that a named human reads; or nobody. It also says the description must be "diegetic": don't narrate how the PR was produced or refer to private conversations — [cli/cli](https://raw.githubusercontent.com/cli/cli/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - PyTorch: "Summary (human written only)" plus a separate "Agent details (if applicable)" — [pytorch](https://raw.githubusercontent.com/pytorch/pytorch/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- (d) **Human-written descriptions:**
  - Next.js and es-toolkit require external contributors' PR descriptions to be written by a human — [next.js](https://raw.githubusercontent.com/vercel/next.js/HEAD/.github/pull_request_template.md), [es-toolkit](https://raw.githubusercontent.com/toss/es-toolkit/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Rust bans LLM-created PR descriptions and LLM-authored commit messages — [rustc-dev-guide](https://raw.githubusercontent.com/rust-lang/rustc-dev-guide/HEAD/src/llm-guidance/writing.md).
  - Vite asks you to use your own words — [vite](https://raw.githubusercontent.com/vitejs/vite/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - LangChain may ignore large AI-written descriptions — [langchain](https://raw.githubusercontent.com/langchain-ai/langchain/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Hugging Face asks first-time contributors not to use code agents — [transformers](https://raw.githubusercontent.com/huggingface/transformers/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**Trailers and attribution:**
- Rust's disclosure guidance:
  - Disclose the *extent* and *purpose* of LLM use, written by yourself.
  - Its good examples describe what the LLM did; for instance, it traced cache misses and reviewed history.
  - It lists "🤖 Generated with Claude Code" and `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>` as **bad** examples.
  - [rustc-dev-guide](https://raw.githubusercontent.com/rust-lang/rustc-dev-guide/HEAD/src/llm-guidance/writing.md).
- Rust's template notes that the PR description becomes part of the merge commit message. It offers `homu-ignore` markers to keep the LLM disclosure out of permanent history — [rust](https://raw.githubusercontent.com/rust-lang/rust/HEAD/.github/pull_request_template.md).
- Linux kernel:
  - Tag format: `Assisted-by: LLM [TOOL1] [TOOL2]`.
  - AI agents must not add `Signed-off-by`; only humans certify the DCO and take responsibility.
  - Anything not built, tested or reproduced must be stated explicitly.
  - [Linux kernel: AI coding assistants](https://docs.kernel.org/process/coding-assistants.html).
- Airflow:
  - Template: an AI checkbox plus a commented `Generated-by: [Tool Name] following [the guidelines]` line — [airflow template](https://raw.githubusercontent.com/apache/airflow/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Guidelines: run all relevant checks locally, state AI use in the description, and remove unrelated AI-introduced changes — [Airflow PR guidelines](https://raw.githubusercontent.com/apache/airflow/HEAD/contributing-docs/05_pull_requests.rst).
- Claude Code (2026 docs):
  - It adds `Co-Authored-By: <model name> <noreply@anthropic.com>` to commits and `🤖 Generated with [Claude Code](https://claude.com/claude-code)` to PR descriptions by default.
  - Both are customizable or hideable through the `attribution` setting (`commit`, `pr`, `sessionUrl`). `includeCoAuthoredBy` has been deprecated since v2.0.62.
  - User instructions in CLAUDE.md or memory take precedence over these lines unless managed settings set them.
  - [Claude Code settings reference](https://code.claude.com/docs/en/settings-reference.md).
- Policies:
  - Ghostty: all AI use must be disclosed with the tool and extent; the human must fully understand the code. Maintainers are exempt — [Ghostty AI_POLICY.md](https://raw.githubusercontent.com/ghostty-org/ghostty/HEAD/AI_POLICY.md); [Ghostty CONTRIBUTING](https://raw.githubusercontent.com/ghostty-org/ghostty/HEAD/CONTRIBUTING.md).
  - Electron: there must be a human in the loop. Contributors read, can answer questions about, and built and tested their contributions. Passing maintainer feedback to an LLM and posting its reply is disallowed — [Electron AI policy](https://raw.githubusercontent.com/electron/governance/HEAD/policy/ai.md).
- AGENTS.md (agents.md) is now read by Codex, Copilot coding agent, Cursor, Gemini CLI and others. Its example has a `## PR instructions` section (title format; run lint/test before committing). That is where agent-facing PR rules usually live, separate from the human template — [agents.md](https://agents.md/).

### Inferences
**Verification section for 믿집.** AGENTS.md §7 already mandates three buckets: local commands, left to CI, not done + why. Map them one-to-one:
- (1) "로컬에서 돌린 것": only commands actually run, one line each, with the result in a word. No output, no pass counts.
- (2) "CI에 맡긴 것": name the suites and link the run. Don't restate the results.
- (3) "못 한 것 · 이유": write "없음" if there is nothing.

This reconciles the React/Prisma school (name what you ran) with the cli/PostHog/Rust school (don't paste CI-visible results).

**Checkboxes.** Use `- [x]` only for lines actually run, and delete lines not run (moving them to 못 한 것 if relevant). Leaving `[ ]` boxes in the body creates permanently "open tasks" in GitHub's task count (PostHog's reason for avoiding them), and it blurs "not applicable" with "not done".

**AI disclosure.** A **one-line, extent-and-purpose** disclosure fits a team where everyone uses agents and reviewers are teammates, not gatekeepers: 도구·모델 / 맡긴 일 / 사람이 직접 확인한 것. A binary checkbox or a bare trailer does not. Keep the Co-Authored-By trailer: it is current practice per the repo attribution setup, and it is machine-searchable. But don't treat it as the disclosure (Rust's point).

**Accountability.** Add one line in the spirit of HA and n8n: "작성자(사람)가 diff 전체를 읽고 설명할 수 있다". It matches AGENTS.md "AI 코딩 도구는 사람이 요청했을 때만 커밋 · 푸시한다". Agent-opened PRs stay as drafts until that is true.

**Don't paste agent transcripts or prompts.** Paraphrase decisions; follow PostHog and GitHub CLI's diegetic rule.

### Gaps
- I didn't verify OpenAI Codex's default commit and PR attribution behavior in 2026; I found no fetched source.
- Fedora's AI contribution policy page blocked automated access (Anubis), so I couldn't confirm its `Assisted-by` recommendation.
- I found no empirical study, only policies, on whether AI disclosure lines change review outcomes.

## 5. What makes PR descriptions useful later (squash commit messages, release notes, onboarding) vs noise; length guidance — and the recommended 믿집 template

### Takeaway
A PR description is useful later when its first line or title states the change as a permanent record ("what" in imperative form, plus "why"). It should stand alone without opening files or chat logs, link the issue, and say what users will notice. It becomes noise when it replays the diff file by file, pastes CI output, carries long checklists and legal boilerplate, or narrates the agent session. Aim for about 150 words or fewer (PostHog), or 1–3 sentences of summary (Prisma, LangChain, n8n). Keep PRs to about 100–400 lines (Google, GitLab, LINE, 뱅크샐러드, AGENTS.md's 400).

### Cited Findings
**Permanent record:**
- Google:
  - A CL description is a permanent public record of what changed and why.
  - The first line is a short, standalone, imperative summary; the body gives problem, approach, shortcomings and context.
  - Vague descriptions like "Fix bug" or "Phase 1" are bad.
  - Re-review the description before submitting, because the CL may have changed during review.
  - Tool-generated descriptions should follow the same rules.
  - [Google eng-practices: CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html).
- Kubernetes: commit messages are the permanent record of what and why; messages like "Address review comments" add no value. Squash "sausage" commits; keep "layer" commits — [k8s PR guide](https://raw.githubusercontent.com/kubernetes/community/HEAD/contributors/guide/pull-requests.md).
- Kubernetes website: title the first commit so that the squashed message makes sense — [kubernetes/website](https://raw.githubusercontent.com/kubernetes/website/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**Title flows into history and changelogs:**
- Mastodon: the PR title becomes the main-branch commit and changelog entry. Use Add/Change/Deprecate/Remove/Fix, and describe from the user's perspective — [Mastodon CONTRIBUTING](https://raw.githubusercontent.com/mastodon/mastodon/HEAD/CONTRIBUTING.md).
- Hugging Face: the PR title appears in the release notes — [transformers](https://raw.githubusercontent.com/huggingface/transformers/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- n8n: the title automatically goes into the changelog, unless `(no-changelog)` is used — [n8n](https://raw.githubusercontent.com/n8n-io/n8n/HEAD/.github/pull_request_template.md).
- Title formats:
  - Grafana: `<FeatureArea>: Describe your change` — [grafana](https://raw.githubusercontent.com/grafana/grafana/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Prometheus: `area: short description` — [prometheus](https://raw.githubusercontent.com/prometheus/prometheus/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Deno and Tauri give good/bad title examples; for instance, "fix #7123" is bad — [deno](https://raw.githubusercontent.com/denoland/deno/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [tauri](https://raw.githubusercontent.com/tauri-apps/tauri/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - Superset asks for Conventional Commits titles — [superset](https://raw.githubusercontent.com/apache/superset/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
  - PostHog: `type(scope): description`, lowercase, under 72 characters — [posthog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md).
- Conventional Commits: `<type>[scope]: <description>`; `!` or a `BREAKING CHANGE:` footer marks breaking changes; footers use git-trailer style tokens — [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
- Commit-message rules: subject at most 50 characters, imperative, body explains what and why — [Chris Beams, 2014](https://cbea.ms/git-commit/).
- Keep a Changelog types: Added / Changed / Deprecated / Removed / Fixed / Security, with an Unreleased section; written for people — [keepachangelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

**Length and shape:**
- PostHog:
  - The body must stand on its own for a reader who opens no files.
  - Aim for 150 words or fewer; diagrams, code blocks and `<details>` don't count.
  - A section with nothing in it gets one bullet: "- None."
  - One fact per bullet, under 25 words.
  - If the body needs more than 150 words, suggest a stack of PRs.
  - [posthog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md).
- PyTorch: up to one paragraph; overly verbose descriptions are treated as spam — [pytorch](https://raw.githubusercontent.com/pytorch/pytorch/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Prisma: one or two sentences on *why*, not file-by-file *what* — [prisma](https://raw.githubusercontent.com/prisma/prisma/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- LangChain: 1–2 sentences as a simple user story — [langchain](https://raw.githubusercontent.com/langchain-ai/langchain/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- n8n: 1–3 sentences of background, in prose, not a list of edits; add a rejected alternative only if a reviewer would ask — [n8n](https://raw.githubusercontent.com/n8n-io/n8n/HEAD/.github/pull_request_template.md).
- Astro: short, concise bullets — [astro](https://raw.githubusercontent.com/withastro/astro/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Next.js maintainers: minimal description that someone outside the team can understand; summarize a Slack thread's conclusion rather than just linking it — [next.js](https://raw.githubusercontent.com/vercel/next.js/HEAD/.github/pull_request_template.md).
- PostHog: for each user-noticeable change, say what the user will now see; mark the rest as mechanical — [posthog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md).
- Armeria's Result section: what users experience after the merge — [Armeria guide](https://armeria.dev/community/developer-guide).
- Atlassian (2019):
  - Group the changed files by concept in the description.
  - Use descriptive titles, not just issue keys.
  - Don't rely on the auto-generated commit log.
  - Use inline navigation comments.
  - Explain code in code comments, not in the PR.
  - Add screenshots for front-end changes.
  - [Atlassian: written and unwritten guide to PRs](https://www.atlassian.com/blog/git/written-unwritten-guide-pull-requests).
- GitHub blog (2015, updated 2022): state the purpose, give context and links, say what kind of feedback you want and by when, and @mention people with a reason — [GitHub blog: perfect PR](https://github.blog/developer-skills/github/how-to-write-the-perfect-pull-request/).
- Michael Lynch (2020): self-review in the reviewer's diff view; automate the easy checks; scope narrowly; separate functional from non-functional changes; break up large changes — [mtlynch.io](https://mtlynch.io/code-review-love/).

**PR size:**
- Google: about 100 lines is usually reasonable and about 1,000 is usually too large; the number of files matters too. Separate refactors from features — [Google eng-practices: small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html).
- GitLab: target about 200 lines, split by CODEOWNERS concern, ship DB changes first — [GitLab code review](https://docs.gitlab.com/development/code_review/).
- 뱅크샐러드: a 1,000-line cap, which settled to 200–300 — [뱅크샐러드](https://blog.banksalad.com/tech/banksalad-code-review-culture/).
- LINE: about 300–400 lines per review session — [LINE](https://engineering.linecorp.com/ko/blog/effective-codereview).
- Home Assistant: one thing per PR; no more than five open PRs at once — [HA perfect PR](https://contributors.home-assistant.io/start/pull-requests/).
- Calcom flags PRs over 500 lines or 10 files as too large — [cal.com](https://raw.githubusercontent.com/calcom/cal.com/HEAD/.github/PULL_REQUEST_TEMPLATE.md).

**Noise examples:**
- Sentry's legal boilerplate in the body — [sentry](https://raw.githubusercontent.com/getsentry/sentry/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Node's full DCO text, inside a comment — [node](https://raw.githubusercontent.com/nodejs/node/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Social-handle and "cute animal" prompts — [langchain](https://raw.githubusercontent.com/langchain-ai/langchain/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [moby](https://raw.githubusercontent.com/moby/moby/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [docker/compose](https://raw.githubusercontent.com/docker/compose/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- A 21-box checklist — [home-assistant](https://raw.githubusercontent.com/home-assistant/core/HEAD/.github/PULL_REQUEST_TEMPLATE.md).
- Pasted CI results — [cli/cli](https://raw.githubusercontent.com/cli/cli/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [rustc-dev-guide](https://raw.githubusercontent.com/rust-lang/rustc-dev-guide/HEAD/src/llm-guidance/writing.md).
- Agent-session narration — [cli/cli](https://raw.githubusercontent.com/cli/cli/HEAD/.github/PULL_REQUEST_TEMPLATE.md), [posthog](https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md).

### Inferences
**Squash setting.** AGENTS.md §6 specifies squash merge and the commit title `type(범위): 한국어 요약`. Two rules follow:
- The **PR title must already be in that commit format**, because the squash commit takes the PR title (GitHub squash options).
- Set the repo's default squash message to "Pull request title" or "Default". Avoid "title and description": the body has checkboxes, HTML guidance comments and tables, which are noisy in `git log`. Rust has to use `homu-ignore` for exactly this. The PR page stays the full record; the commit links back through `Closes #N` and the PR reference.

**What each section is for, and what to leave out:**

| 섹션 | 목적 (나중에 누가 읽나) | 넣지 말 것 |
|---|---|---|
| 제목 | squash 커밋 제목이자 변경 이력·발표 노트의 한 줄 (`type(범위): 한국어 요약`) | 이슈 번호만 (`#12 수정`), 마침표, 영어 상태값 |
| 무엇을 · 왜 | 2–3문장: 사용자/팀이 보게 될 결과 + 이유. 리뷰어·3주 뒤의 나·새 팀원용 | 파일별 변경 나열, 코드 설명(→ 코드 주석), 채팅·프롬프트 붙여넣기 |
| 요구사항 · Closes | 요구사항 ID(예: FFV-02)와 이슈 자동 닫기 (main 대상일 때만 동작) | `Fixes`를 비-기본 브랜치 PR에 기대하기 |
| 호출 흐름 (바뀐 경우) | 구조 변경 한 줄; 다음 사람이 경로를 따라가게 | 안 바뀌었는데 채우기 → 절째 지움 |
| 검증 | 로컬에서 실제로 돌린 명령(한 줄·결과 한 단어) / CI에 맡긴 것 / UI면 360px 전·후 스크린샷 | 테스트 출력·통과 개수 붙여넣기, 안 돌린 걸 `[ ]`로 남기기, "아마 될 것" |
| 못 한 것 · 이유 | 남은 위험과 후속 이슈; `status.md` '검증 대기'와 연결 | 비워 두기 (없으면 "없음") |
| 해당할 때만 | migration(up/down·`alembic check`), 새 env(`.env.example`), ADR·status 갱신, 리뷰어가 먼저 볼 곳 | 해당 없음 줄 남기기 |
| AI 사용 | 한 줄: 도구·모델 / 맡긴 일 / 사람이 확인한 것 | 세션 로그, 프롬프트, "🤖 Generated…"만 남기기 |

**Length rules for the team:**
- The filled body should be **about 150 단어** (roughly 10–15 lines) or fewer, excluding the screenshot table and code.
- If it needs more, the PR is probably over the 400-line rule; split it.
- One fact per bullet.
- Delete empty optional sections rather than writing "N/A". The exceptions are 못 한 것 and AI 사용, which always get "없음" when empty.

**Recommended `.github/pull_request_template.md`** (Korean; about 30 lines including comments; comments are invisible in the rendered PR):

```markdown
<!-- 제목 = squash 커밋 제목: type(범위): 한국어 요약
     예) feat(api): 가견적 요청 API 추가 · fix(web): 견적 화면 360px 가로 스크롤 제거 -->

## 무엇을 · 왜
<!-- 2~3문장. 첫 문장은 바뀐 결과(사용자·팀이 보게 될 것), 다음은 이유. 파일 나열 X -->


요구사항: FFV-
Closes #

## 호출 흐름 (바뀐 경우만 · 아니면 이 절을 지운다)
<!-- 한 줄. 예) web → POST /api/projects → project.service → PostgreSQL -->

## 검증
<!-- 실제로 돌린 것만 [x]로 남기고 안 돌린 줄은 지운다(필요하면 '못 한 것'으로).
     결과는 한 단어(통과 / 실패: 이유). 출력·통과 개수는 붙이지 않는다 — CI가 보여 준다. -->
**로컬에서 돌린 것**
- [x] `uv run pytest <대상>` → 통과
- [x] `uv run ruff check` · `uv run ruff format --check` → 통과
- [x] `pnpm typecheck` · `pnpm lint` → 통과

**CI에 맡긴 것**: 전체 pytest(PostgreSQL·Redis, migration up→down→up) · `pnpm build`

**화면** (UI가 바뀐 경우만): 폰 너비 360px, 가로 스크롤 없음 · 버튼 40px 이상
| 전 | 후 |
|---|---|
|   |   |

## 못 한 것 · 이유
<!-- 없으면 "없음". 확인 못 한 것, 남긴 일은 후속 이슈 번호와 함께 -->
- 없음

## 해당할 때만 (아니면 줄째 지운다)
- DB migration: `docker compose run --rm migrate` + `alembic check` 결과, downgrade 확인 여부
- 새 환경변수: `.env.example`에 한국어 주석과 함께 추가함
- 기록: `docs/status.md` 행 변경 / ADR-NNNN
- 리뷰어가 먼저 볼 곳:

## AI 사용
<!-- 한 줄: 도구·모델 / 맡긴 일 / 사람이 직접 확인한 것. 안 썼으면 "없음".
     프롬프트·세션 로그는 붙이지 않는다. -->
- 예) Claude Code (Opus 5.5) / 서비스·테스트 초안 / 작성자가 diff 전체를 읽고 pytest를 직접 돌림
```

**Why this shape.**
- It keeps AGENTS.md §6's five parts in order (무엇을 왜 / 호출 흐름 / 검증 / 못 한 것 / Closes).
- It splits 검증 into §7's three buckets (local / CI / not done).
- It adds the four OSS-consensus gaps from Q1 as conditional lines: UI screenshot, AI line, reviewer focus, migration/rollback.
- The sibling `team_records.md` draft's "기록 갱신" (status.md / ADR) becomes one conditional line instead of two checkboxes, avoiding unchecked-box noise.

**Companion rules** (these belong in AGENTS.md or CONTRIBUTING, not the template):
- AI agents open PRs as drafts. The human author marks the PR ready only after reading the whole diff.
- Review comments carry a Pn prefix (P1 꼭 / P2 적극 고려 / P3 웬만하면 / P4 선택 / P5 사소), or Conventional Comments `(blocking)` / `(non-blocking)`. P1 and P2 threads must be resolved before merge (ruleset "require conversation resolution").
- Use labels, not checkboxes, for type and area.
- Optional: a `.github/release.yml` to group merged PRs by label for milestone (발표) notes.

### Gaps
- I couldn't measure how long real 믿집-style PR bodies run in practice. The 150-word target comes from PostHog's template, not from a study.
- I didn't verify whether `(#PR number)` is auto-appended to squash commit titles. The sibling note `commits_changelog.md` also flags this as unverified.
- I found no source on how GitHub renders very long PR bodies in the squash dialog.

### Sources consulted (full URL list)

All template files were read from the default branch (`HEAD`) on 2026-10-29.

**PR/MR template files (113)**
1. https://raw.githubusercontent.com/facebook/react/HEAD/.github/PULL_REQUEST_TEMPLATE.md
2. https://raw.githubusercontent.com/vercel/next.js/HEAD/.github/pull_request_template.md
3. https://raw.githubusercontent.com/vercel/turborepo/HEAD/.github/pull_request_template.md
4. https://raw.githubusercontent.com/vercel/ai/HEAD/.github/pull_request_template.md
5. https://raw.githubusercontent.com/django/django/HEAD/.github/pull_request_template.md
6. https://raw.githubusercontent.com/kubernetes/kubernetes/HEAD/.github/PULL_REQUEST_TEMPLATE.md
7. https://raw.githubusercontent.com/rust-lang/rust/HEAD/.github/pull_request_template.md
8. https://raw.githubusercontent.com/microsoft/vscode/HEAD/.github/pull_request_template.md
9. https://raw.githubusercontent.com/supabase/supabase/HEAD/.github/pull_request_template.md
10. https://raw.githubusercontent.com/PostHog/posthog/HEAD/.github/pull_request_template.md
11. https://raw.githubusercontent.com/getsentry/sentry/HEAD/.github/PULL_REQUEST_TEMPLATE.md
12. https://raw.githubusercontent.com/grafana/grafana/HEAD/.github/PULL_REQUEST_TEMPLATE.md
13. https://raw.githubusercontent.com/home-assistant/core/HEAD/.github/PULL_REQUEST_TEMPLATE.md
14. https://raw.githubusercontent.com/angular/angular/HEAD/.github/PULL_REQUEST_TEMPLATE.md
15. https://raw.githubusercontent.com/sveltejs/svelte/HEAD/.github/PULL_REQUEST_TEMPLATE.md
16. https://raw.githubusercontent.com/nodejs/node/HEAD/.github/PULL_REQUEST_TEMPLATE.md
17. https://raw.githubusercontent.com/denoland/deno/HEAD/.github/PULL_REQUEST_TEMPLATE.md
18. https://raw.githubusercontent.com/oven-sh/bun/HEAD/.github/pull_request_template.md
19. https://raw.githubusercontent.com/tailwindlabs/tailwindcss/HEAD/.github/PULL_REQUEST_TEMPLATE.md
20. https://raw.githubusercontent.com/prisma/prisma/HEAD/.github/PULL_REQUEST_TEMPLATE.md
21. https://raw.githubusercontent.com/nestjs/nest/HEAD/.github/PULL_REQUEST_TEMPLATE.md
22. https://raw.githubusercontent.com/pallets/flask/HEAD/.github/pull_request_template.md
23. https://raw.githubusercontent.com/pandas-dev/pandas/HEAD/.github/PULL_REQUEST_TEMPLATE.md
24. https://raw.githubusercontent.com/numpy/numpy/HEAD/.github/PULL_REQUEST_TEMPLATE.md
25. https://raw.githubusercontent.com/scikit-learn/scikit-learn/HEAD/.github/PULL_REQUEST_TEMPLATE.md
26. https://raw.githubusercontent.com/pytorch/pytorch/HEAD/.github/PULL_REQUEST_TEMPLATE.md
27. https://raw.githubusercontent.com/huggingface/transformers/HEAD/.github/PULL_REQUEST_TEMPLATE.md
28. https://raw.githubusercontent.com/langchain-ai/langchain/HEAD/.github/PULL_REQUEST_TEMPLATE.md
29. https://raw.githubusercontent.com/microsoft/TypeScript/HEAD/.github/pull_request_template.md
30. https://raw.githubusercontent.com/helm/helm/HEAD/.github/pull_request_template.md
31. https://raw.githubusercontent.com/prometheus/prometheus/HEAD/.github/PULL_REQUEST_TEMPLATE.md
32. https://raw.githubusercontent.com/hashicorp/terraform/HEAD/.github/pull_request_template.md
33. https://raw.githubusercontent.com/elastic/kibana/HEAD/.github/PULL_REQUEST_TEMPLATE.md
34. https://raw.githubusercontent.com/apache/airflow/HEAD/.github/PULL_REQUEST_TEMPLATE.md
35. https://raw.githubusercontent.com/apache/superset/HEAD/.github/PULL_REQUEST_TEMPLATE.md
36. https://raw.githubusercontent.com/mattermost/mattermost/HEAD/.github/PULL_REQUEST_TEMPLATE.md
37. https://raw.githubusercontent.com/rails/rails/HEAD/.github/pull_request_template.md
38. https://raw.githubusercontent.com/godotengine/godot/HEAD/.github/PULL_REQUEST_TEMPLATE.md
39. https://raw.githubusercontent.com/electron/electron/HEAD/.github/PULL_REQUEST_TEMPLATE.md
40. https://raw.githubusercontent.com/storybookjs/storybook/HEAD/.github/PULL_REQUEST_TEMPLATE.md
41. https://raw.githubusercontent.com/mui/material-ui/HEAD/.github/PULL_REQUEST_TEMPLATE.md
42. https://raw.githubusercontent.com/ant-design/ant-design/HEAD/.github/PULL_REQUEST_TEMPLATE.md
43. https://raw.githubusercontent.com/withastro/astro/HEAD/.github/PULL_REQUEST_TEMPLATE.md
44. https://raw.githubusercontent.com/vitejs/vite/HEAD/.github/PULL_REQUEST_TEMPLATE.md
45. https://raw.githubusercontent.com/eslint/eslint/HEAD/.github/PULL_REQUEST_TEMPLATE.md
46. https://raw.githubusercontent.com/prettier/prettier/HEAD/.github/PULL_REQUEST_TEMPLATE.md
47. https://raw.githubusercontent.com/cypress-io/cypress/HEAD/.github/PULL_REQUEST_TEMPLATE.md
48. https://raw.githubusercontent.com/calcom/cal.com/HEAD/.github/PULL_REQUEST_TEMPLATE.md
49. https://raw.githubusercontent.com/n8n-io/n8n/HEAD/.github/pull_request_template.md
50. https://raw.githubusercontent.com/appwrite/appwrite/HEAD/.github/PULL_REQUEST_TEMPLATE.md
51. https://raw.githubusercontent.com/strapi/strapi/HEAD/.github/PULL_REQUEST_TEMPLATE.md
52. https://raw.githubusercontent.com/directus/directus/HEAD/.github/pull_request_template.md
53. https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/HEAD/.github/pull_request_template.md
54. https://raw.githubusercontent.com/sqlalchemy/alembic/HEAD/.github/pull_request_template.md
55. https://raw.githubusercontent.com/pydantic/pydantic/HEAD/.github/PULL_REQUEST_TEMPLATE.md
56. https://raw.githubusercontent.com/encode/starlette/HEAD/.github/pull_request_template.md
57. https://raw.githubusercontent.com/astral-sh/ruff/HEAD/.github/PULL_REQUEST_TEMPLATE.md
58. https://raw.githubusercontent.com/astral-sh/uv/HEAD/.github/PULL_REQUEST_TEMPLATE.md
59. https://raw.githubusercontent.com/zed-industries/zed/HEAD/.github/pull_request_template.md
60. https://raw.githubusercontent.com/tauri-apps/tauri/HEAD/.github/PULL_REQUEST_TEMPLATE.md
61. https://raw.githubusercontent.com/TanStack/query/HEAD/.github/pull_request_template.md
62. https://raw.githubusercontent.com/immich-app/immich/HEAD/.github/pull_request_template.md
63. https://raw.githubusercontent.com/nextcloud/server/HEAD/.github/pull_request_template.md
64. https://raw.githubusercontent.com/openai/openai-python/HEAD/.github/pull_request_template.md
65. https://raw.githubusercontent.com/toss/es-toolkit/HEAD/.github/PULL_REQUEST_TEMPLATE.md
66. https://raw.githubusercontent.com/toss/suspensive/HEAD/.github/PULL_REQUEST_TEMPLATE.md
67. https://raw.githubusercontent.com/toss/slash/HEAD/.github/PULL_REQUEST_TEMPLATE.md
68. https://raw.githubusercontent.com/line/armeria/HEAD/.github/PULL_REQUEST_TEMPLATE.md
69. https://raw.githubusercontent.com/nhn/tui.editor/HEAD/docs/PULL_REQUEST_TEMPLATE.md
70. https://raw.githubusercontent.com/naver/billboard.js/HEAD/.github/PULL_REQUEST_TEMPLATE.md
71. https://raw.githubusercontent.com/kakao/khaiii/HEAD/.github/pull_request_template.md
72. https://raw.githubusercontent.com/microsoft/fluentui/HEAD/.github/PULL_REQUEST_TEMPLATE.md
73. https://raw.githubusercontent.com/facebook/docusaurus/HEAD/.github/PULL_REQUEST_TEMPLATE.md
74. https://raw.githubusercontent.com/docker/compose/HEAD/.github/PULL_REQUEST_TEMPLATE.md
75. https://raw.githubusercontent.com/moby/moby/HEAD/.github/PULL_REQUEST_TEMPLATE.md
76. https://raw.githubusercontent.com/cli/cli/HEAD/.github/PULL_REQUEST_TEMPLATE.md
77. https://raw.githubusercontent.com/github/docs/HEAD/.github/PULL_REQUEST_TEMPLATE.md
78. https://raw.githubusercontent.com/freeCodeCamp/freeCodeCamp/HEAD/.github/PULL_REQUEST_TEMPLATE.md
79. https://raw.githubusercontent.com/keycloak/keycloak/HEAD/docs/pull_request_template.md
80. https://raw.githubusercontent.com/argoproj/argo-cd/HEAD/.github/pull_request_template.md
81. https://raw.githubusercontent.com/istio/istio/HEAD/.github/pull_request_template.md
82. https://raw.githubusercontent.com/envoyproxy/envoy/HEAD/PULL_REQUEST_TEMPLATE.md
83. https://raw.githubusercontent.com/kubernetes/website/HEAD/.github/PULL_REQUEST_TEMPLATE.md
84. https://raw.githubusercontent.com/backstage/backstage/HEAD/.github/PULL_REQUEST_TEMPLATE.md
85. https://gitlab.com/gitlab-org/gitlab/-/raw/master/.gitlab/merge_request_templates/Default.md
86. https://raw.githubusercontent.com/toss/frontend-fundamentals/HEAD/.github/PULL_REQUEST_TEMPLATE.md
87. https://raw.githubusercontent.com/toss/overlay-kit/HEAD/.github/pull_request_template.md
88. https://raw.githubusercontent.com/toss/react-simplikit/HEAD/.github/pull_request_template.md
89. https://raw.githubusercontent.com/naver/fixture-monkey/HEAD/.github/PULL_REQUEST_TEMPLATE.md
90. https://raw.githubusercontent.com/naver/egjs-flicking/HEAD/.github/PULL_REQUEST_TEMPLATE.md
91. https://raw.githubusercontent.com/kakao/kakao_flutter_sdk/HEAD/.github/pull_request_template.md
92. https://raw.githubusercontent.com/pmndrs/zustand/HEAD/.github/pull_request_template.md
93. https://raw.githubusercontent.com/facebook/react-native/HEAD/.github/PULL_REQUEST_TEMPLATE.md
94. https://raw.githubusercontent.com/google/gson/HEAD/.github/pull_request_template.md
95. https://raw.githubusercontent.com/spring-projects/spring-boot/HEAD/.github/PULL_REQUEST_TEMPLATE.md
96. https://raw.githubusercontent.com/jestjs/jest/HEAD/.github/PULL_REQUEST_TEMPLATE.md
97. https://raw.githubusercontent.com/toss/es-hangul/HEAD/.github/PULL_REQUEST_TEMPLATE.md
98. https://raw.githubusercontent.com/kakao/actionbase/HEAD/.github/PULL_REQUEST_TEMPLATE.md
99. https://raw.githubusercontent.com/woowacourse-teams/2022-gong-check/HEAD/.github/PULL_REQUEST_TEMPLATE.md
100. https://raw.githubusercontent.com/woowacourse-teams/2022-moamoa/HEAD/.github/pull_request_template.md
101. https://raw.githubusercontent.com/woowacourse-teams/2023-baton/HEAD/.github/PULL_REQUEST_TEMPLATE.md
102. https://raw.githubusercontent.com/woowacourse-teams/2023-dong-gle/HEAD/.github/pull_request_template.md
103. https://raw.githubusercontent.com/woowacourse-teams/2023-emmsale/HEAD/.github/PULL_REQUEST_TEMPLATE.md
104. https://raw.githubusercontent.com/woowacourse-teams/2023-hang-log/HEAD/.github/PULL_REQUEST_TEMPLATE.md
105. https://raw.githubusercontent.com/woowacourse-teams/2023-zipgo/HEAD/.github/PULL_REQUEST_TEMPLATE.md
106. https://raw.githubusercontent.com/woowacourse-teams/2024-bang-ggood/HEAD/.github/PULL_REQUEST_TEMPLATE.md
107. https://raw.githubusercontent.com/woowacourse-teams/2024-corea/HEAD/.github/PULL_REQUEST_TEMPLATE.md
108. https://raw.githubusercontent.com/woowacourse-teams/2024-ddangkong/HEAD/.github/pull_request_template.md
109. https://raw.githubusercontent.com/woowacourse-teams/2024-friendogly/HEAD/.github/pull_request_template.md
110. https://raw.githubusercontent.com/woowacourse-teams/2024-mouda/HEAD/.github/PULL_REQUEST_TEMPLATE.md
111. https://raw.githubusercontent.com/woowacourse-teams/2024-staccato/HEAD/.github/pull_request_template.md
112. https://raw.githubusercontent.com/woowacourse-teams/2025-bottari/HEAD/.github/PULL_REQUEST_TEMPLATE.md
113. https://raw.githubusercontent.com/woowacourse-teams/2025-coffee-shout/HEAD/.github/pull_request_template.md

**Docs, policies and blogs (40)**
114. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
115. https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/using-query-parameters-to-create-a-pull-request
116. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
117. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests
118. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
119. https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes
120. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
121. https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors
122. https://docs.github.com/en/get-started/writing-on-github/working-with-saved-replies/about-saved-replies
123. https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
124. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
125. https://docs.github.com/en/copilot/how-tos/use-copilot-for-common-tasks/create-a-pr-summary
126. https://conventionalcomments.org/
127. https://www.conventionalcommits.org/en/v1.0.0/
128. https://keepachangelog.com/en/1.1.0/
129. https://cbea.ms/git-commit/
130. https://google.github.io/eng-practices/review/developer/cl-descriptions.html
131. https://google.github.io/eng-practices/review/developer/small-cls.html
132. https://github.blog/developer-skills/github/how-to-write-the-perfect-pull-request/
133. https://www.atlassian.com/blog/git/written-unwritten-guide-pull-requests
134. https://mtlynch.io/code-review-love/
135. https://docs.gitlab.com/development/code_review/
136. https://raw.githubusercontent.com/kubernetes/community/HEAD/contributors/guide/pull-requests.md
137. https://contributors.home-assistant.io/start/pull-requests/
138. https://armeria.dev/community/developer-guide
139. https://raw.githubusercontent.com/mastodon/mastodon/HEAD/CONTRIBUTING.md
140. https://raw.githubusercontent.com/fastapi/fastapi/HEAD/docs/en/docs/contributing.md
141. https://docs.kernel.org/process/coding-assistants.html
142. https://raw.githubusercontent.com/rust-lang/rustc-dev-guide/HEAD/src/llm-guidance/writing.md
143. https://raw.githubusercontent.com/ghostty-org/ghostty/HEAD/AI_POLICY.md
144. https://raw.githubusercontent.com/ghostty-org/ghostty/HEAD/CONTRIBUTING.md
145. https://raw.githubusercontent.com/electron/governance/HEAD/policy/ai.md
146. https://raw.githubusercontent.com/apache/airflow/HEAD/contributing-docs/05_pull_requests.rst
147. https://pandas.pydata.org/docs/dev/development/contributing.html
148. https://code.claude.com/docs/en/settings-reference.md (also https://code.claude.com/docs/en/settings)
149. https://agents.md/
150. https://blog.banksalad.com/tech/banksalad-code-review-culture/
151. https://blog.banksalad.com/tech/become-an-organization-that-deploys-1000-times-a-day/
152. https://engineering.linecorp.com/ko/blog/effective-codereview
153. https://tech.kakao.com/posts/498 (same article as https://tech.kakao.com/2022/03/17/2022-newkrew-onboarding-codereview/; title only, body not retrievable)

**Tried but unusable:**
- Access blocked: https://docs.fedoraproject.org/en-US/council/policy/ai-contribution-policy/ (Anubis), and techblog.woowahan.com/2712, /2553, /7638, /9475 ("보안 위배 접근 제한").
- 404 or irrelevant: https://tech.socarcorp.kr/dev/2022/04/14/code-review.html, https://www.44bits.io/ko/post/pull-request-template, https://techblog.lycorp.co.jp/ko/how-to-write-a-good-pull-request, and https://toss.tech/article/firesidechat_frontend_2 (an unrelated topic).
- Challenge page or empty response: medium.com/daangn (Cloudflare), helloworld.kurly.com, tech.devsisters.com, tech.inflab.com, hyperconnect.github.io.
- Repos with no template at the standard paths: fastapi/fastapi, mastodon/mastodon, vuejs/core, nuxt/nuxt, microsoft/playwright, excalidraw/excalidraw, shadcn-ui/ui, openai/codex, anthropics/claude-code, discourse/discourse, ghostty-org/ghostty, daangn/stackflow, daangn/seed-design, line/line-bot-sdk-python, woowacourse/java-racingcar, woowacourse-teams/2024-haeng-dong, woowacourse-teams/2024-pengcook, and others.
