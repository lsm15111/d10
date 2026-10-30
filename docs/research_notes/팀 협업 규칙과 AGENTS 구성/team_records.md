# How small software teams record ongoing work, and a recording system for the 믿집 student team on GitHub

Research date: 2026-10-29. Scope: issues, boards, progress logs, meeting notes, retrospectives, how docs are organised, and records that AI agents read, for a team of about 4–6 bootcamp students writing in Korean on GitHub (믿집, SKN34).

Method notes for the report writer:
- I read 32 issue-template and config files from 25 popular repos, 3 Kubernetes process files (KEP template, `kep.yaml`, label taxonomy), 14 template files from 13 Korean bootcamp team repos (12 우아한테크코스 `woowacourse-teams`, 1 부스트캠프), and 9 Korean team wiki pages plus 3 wiki indexes. I read them raw from `raw.githubusercontent.com` at `HEAD` on 2026-10-29. Other sources were GitHub Docs and Changelog pages, practitioner guides and a few academic papers.
- The shared WebSearch budget ran out partway through. After that I only fetched URLs I already knew, and I did not search velog or tistory further. As a result, Korean coverage of SSAFY and official 우테코 or 부스트캠프 guides is thin; the Gaps sections say so.
- I read the 믿집 repo's `AGENTS.md`, `docs/status.md` and `docs/` tree for context and did not modify them. Facts about 믿집 below come from those files: `status.md` uses 제안/구현/검증, AGENTS.md says "진행 현황은 `docs/status.md` 하나에만 적는다", CI has "아직 한 번도 돌지 않았다", and requirement IDs look like FFV-03 and FAG-01.

---

## Q1. GitHub Issues and Projects in 2025–2026 for small teams: issue forms, issue types, sub-issues, labels, milestones, Projects views/iterations/automation, PR linking, real examples

### Takeaway
Since 2025, GitHub Issues has grown into a full planning tool. Sub-issues, issue types and advanced search became GA in April 2025, dependencies in August 2025, and issue fields in July 2026; in June 2026 the `gh` CLI added support for types, sub-issues and dependencies. Several of these features (issue types, issue fields) are defined at the **organization** level. For a student team, the practical setup is a free GitHub organization, 3–4 YAML issue forms, a small prefixed label set, and one Project with a Status field, plus an iteration field or milestones and the two default built-in workflows. Popular OSS repos overwhelmingly use YAML forms with `blank_issues_enabled: false`. Korean bootcamp teams mostly use short Markdown templates: description, task checklist, estimated time, references.

### Cited Findings
**Platform features (dates checked against the changelog and docs as of 2026-10-29)**
- Sub-issues, issue types and advanced search (AND/OR, parentheses, e.g. `is:issue type:Bug OR type:Feature`) became GA on 2025-04-09. In the same release the Projects item limit went from 1,200 to 50,000. — [GitHub Changelog 2025-04-09](https://github.blog/changelog/2025-04-09-evolving-github-issues-and-projects/); public preview began January 2025 — [Changelog 2025-01-13](https://github.blog/changelog/2025-01-13-evolving-github-issues-public-preview/)
- Sub-issue limits: up to 100 sub-issues per parent, nested up to 8 levels. Existing issues from other repos can be added. Projects can filter, group and build views by parent issue and show sub-issue progress. — [GitHub Docs: Adding sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)
- Issue types are configured in the organization under Settings > Planning > Issue types. Defaults are **task, bug, feature**; an org can have up to 25 types. Types can be used in filters, search and project views. The page only covers organizations and says nothing about user-owned repos. — [GitHub Docs: Managing issue types](https://docs.github.com/en/issues/tracking-your-work-with-issues/configuring-issues/managing-issue-types-in-an-organization)
- In the CLI (v2.94.0, 2026-06-10), `gh issue` can set and filter `type`, link parents with `--parent`/`--set-parent`, and set dependencies with `--blocked-by`/`--blocking`. Issue types only apply in organizations that have defined them. — [GitHub Changelog 2026-06-10](https://github.blog/changelog/2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli/)
- Issue dependencies ("blocked by" / "blocking") became GA on 2025-08-21. Each relationship type allows up to 50 issues. Filters are `is:blocked`, `is:blocking`, `blocked-by:` and `blocking:`, and boards show a "Blocked" icon. Available on Free, Pro, Team and Enterprise Cloud; creating them needs triage permission. — [Changelog 2025-08-21](https://github.blog/changelog/2025-08-21-dependencies-on-issues/); [Docs: Creating issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies)
- Issue fields are typed metadata on issues. History: public preview to selected orgs on 2026-03-12, preview to all orgs on 2026-05-21, GA on 2026-07-02.
  - Default fields are **Priority, Effort, Start date, Target date**, configured under Settings > Planning > Issue fields.
  - Available to organizations on Free, Team and Enterprise plans.
  - GitHub reports more than 40,000 adopting organizations.
  - Fields are exposed through GitHub's MCP server, so AI tools can "read and set field values".
  - The changelog says nothing about user-owned repos.
  - Sources: [Changelog 2026-07-02 GA](https://github.blog/changelog/2026-07-02-issue-fields-are-now-generally-available); [Changelog 2026-03-12](https://github.blog/changelog/2026-03-12-issue-fields-structured-issue-metadata-is-in-public-preview/); [Changelog 2026-05-21](https://github.blog/changelog/2026-05-21-issue-fields-are-now-in-public-preview-for-all-organizations/)
- Newer previews (2026, from search snippets I did not open in full): duplicate detection when creating issues, showing up to 3 suggestions, plus issue-fields MCP support (2026-06-18). A "Relates to" relationship and multi-select fields followed, with multi-select GA in August 2026. — [Changelog 2026-06-18](https://github.blog/changelog/2026-06-18-duplicate-detection-and-issue-fields-mcp-support-for-github-issues); [Changelog 2026-08-07](https://github.blog/changelog/2026-08-07-connecting-issues-and-multi-select-field-support/)
- Issue form top-level keys:
  - Required: `name` (must be unique across all templates), `description`, `body`.
  - Optional: `title`, `labels`, `assignees`, `type`, `projects`.
  - `type` applies an org-level issue type. `projects` uses `OWNER/NUMBER` and requires the submitter to have write access to the project; otherwise GitHub suggests the project's auto-add workflow.
  - A label that does not exist in the repo is not added.
  - Files go in `.github/ISSUE_TEMPLATE`.
  - The docs still label issue forms **"public preview and subject to change"**, even though most large repos use them.
  - Source: [GitHub Docs: Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- `config.yml` behaviour:
  - `blank_issues_enabled: false` hides blank issues from Read/Triage users. Write and higher users still see a "Maintainers only" blank option.
  - `contact_links` sends people to other places.
  - The chooser sorts templates alphabetically with YAML before Markdown, so use numeric prefixes (`1-bug.yml`, or `01-…` once there are 10 or more).
  - Templates take effect only after they are merged to the default branch.
  - Source: [GitHub Docs: Configuring issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- Labels:
  - Defaults are `accessibility, bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix`.
  - Write access is needed to create or edit labels, triage access to apply them.
  - Org owners can set default labels for new repos.
  - Source: [GitHub Docs: Managing labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- A milestone shows its description, due date, percent complete, open/closed counts and the list of items. Items can be dragged to set priority (not possible above 500 open issues). — [GitHub Docs: About milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)
- PR ↔ issue linking:
  - Keywords: close/closes/closed, fix/fixes/fixed, resolve/resolves/resolved.
  - They work in a PR body or a commit message, but **only when the PR targets the default branch**.
  - Up to 10 issues can be linked manually. Cross-repo links use `OWNER/REPO#N`.
  - Merging the PR closes the issue.
  - Source: [GitHub Docs: Linking a PR to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
- Projects best practices (GitHub's own guidance):
  - Keep one source of truth. Assignees, milestones and labels sync from issues automatically.
  - Use built-in workflows plus auto-archive and auto-add.
  - Use iteration fields with breaks.
  - Post status updates such as "On track" or "At risk".
  - Use table, board and roadmap views, and break large issues into sub-issues.
  - Write a project README.
  - Source: [GitHub Docs: Best practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
- Built-in workflows: "Item closed → Done" and "Pull request merged → Done" are **enabled by default**. Auto-add and auto-archive are configured separately. — [GitHub Docs: Built-in automations](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)
- Auto-add limits: Free 1 workflow, Pro and Team 5, Enterprise 20. It is not retroactive: only items created or updated after it is turned on get added. Filters look like `is:issue label:bug`. — [GitHub Docs: Adding items automatically](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically)
- Iteration fields can be any length in days or weeks, with breaks between them. Creating the field makes 3 iterations. Filters include `@current`, `@previous`, `@next` and `iteration:<@current`. Unfinished items can be moved to the next iteration in bulk. — [GitHub Docs: About iteration fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields)
- Project status updates have a Status (e.g. On track / At risk), start and target dates, and a Markdown message. They appear in the side panel with full history, and the newest status shows in the project header and lists. Each new update is pre-filled from the previous one. — [GitHub Docs: Sharing project updates](https://docs.github.com/en/issues/planning-and-tracking-with-projects/sharing-project-updates)
- Insights: "current" charts (e.g. items per iteration) and "historical" charts (X axis = Time). Burn-up is the default historical chart. Archived and deleted items are not counted. — [GitHub Docs: About insights](https://docs.github.com/en/issues/planning-and-tracking-with-projects/viewing-insights-from-your-project/about-insights-for-projects)

**Real templates: popular repos (read 2026-10-29)**
- Of 28 templates (excluding `config.yml`), 23 are YAML issue forms and 5 are Markdown (vscode bug_report.md, react bug_report.md, deno feature_request.md, flask feature-request.md, rust tracking_issue.md).
  - vscode, next.js and fastapi set `blank_issues_enabled: false` and send questions to Discussions or Stack Overflow through `contact_links`.
  - Sources: [vscode config.yml](https://raw.githubusercontent.com/microsoft/vscode/HEAD/.github/ISSUE_TEMPLATE/config.yml); [next.js config.yml](https://raw.githubusercontent.com/vercel/next.js/HEAD/.github/ISSUE_TEMPLATE/config.yml); [fastapi config.yml](https://raw.githubusercontent.com/fastapi/fastapi/HEAD/.github/ISSUE_TEMPLATE/config.yml)
- Forms that set the new `type:` key:
  - next.js `type: Bug` — [next.js 1.bug_report.yml](https://raw.githubusercontent.com/vercel/next.js/HEAD/.github/ISSUE_TEMPLATE/1.bug_report.yml)
  - langchain `type: task` — [langchain task.yml](https://raw.githubusercontent.com/langchain-ai/langchain/HEAD/.github/ISSUE_TEMPLATE/task.yml)
  - home-assistant `type: Task` — [home-assistant task.yml](https://raw.githubusercontent.com/home-assistant/core/HEAD/.github/ISSUE_TEMPLATE/task.yml)
  - nest `type: bug` — [nest Regression.yml](https://raw.githubusercontent.com/nestjs/nest/HEAD/.github/ISSUE_TEMPLATE/Regression.yml)
  - electron `type: 'bug'` — [electron bug_report.yml](https://raw.githubusercontent.com/electron/electron/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml)
- Internal "task" forms restricted to maintainers:
  - langchain "📋 Task": "for project management and tracking by LangChain maintainers", with fields Task Description / **Acceptance Criteria** / Context and Background / **Dependencies** / Package — [langchain task.yml](https://raw.githubusercontent.com/langchain-ai/langchain/HEAD/.github/ISSUE_TEMPLATE/task.yml)
  - home-assistant "For staff only – Create a task" (Description / Additional context) — [home-assistant task.yml](https://raw.githubusercontent.com/home-assistant/core/HEAD/.github/ISSUE_TEMPLATE/task.yml)
  - fastapi "Privileged" — [fastapi privileged.yml](https://raw.githubusercontent.com/fastapi/fastapi/HEAD/.github/ISSUE_TEMPLATE/privileged.yml)
- Common bug-form fields are summary/description, reproduction (link or steps), expected vs actual, environment/version, and logs. Examples:
  - [react bug_report.md](https://raw.githubusercontent.com/facebook/react/HEAD/.github/ISSUE_TEMPLATE/bug_report.md) (label `Status: Unconfirmed`, title prefix `Bug: `)
  - [pydantic bug-v2.yml](https://raw.githubusercontent.com/pydantic/pydantic/HEAD/.github/ISSUE_TEMPLATE/bug-v2.yml) (labels `[bug V2, pending]`)
  - [uv 1_bug_report.yaml](https://raw.githubusercontent.com/astral-sh/uv/HEAD/.github/ISSUE_TEMPLATE/1_bug_report.yaml)
  - [vue bug_report.yml](https://raw.githubusercontent.com/vuejs/core/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml)
  - [godot bug_report.yml](https://raw.githubusercontent.com/godotengine/godot/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml)
  - [openai-python bug_report.yml](https://raw.githubusercontent.com/openai/openai-python/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml)
  - [shadcn/ui bug_report.yml](https://raw.githubusercontent.com/shadcn-ui/ui/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml) (title prefix `[bug]: `)
  - [astro bug report](https://raw.githubusercontent.com/withastro/astro/HEAD/.github/ISSUE_TEMPLATE/---01-bug-report.yml)
  - [cpython bug.yml](https://raw.githubusercontent.com/python/cpython/HEAD/.github/ISSUE_TEMPLATE/bug.yml) (label `type-bug`, dropdowns for tested versions and OS)
  - [vscode bug_report.md](https://raw.githubusercontent.com/microsoft/vscode/HEAD/.github/ISSUE_TEMPLATE/bug_report.md)
- Feature forms usually ask for the problem, the proposed solution, alternatives, and scope or importance:
  - [prisma feature_request.yml](https://raw.githubusercontent.com/prisma/prisma/HEAD/.github/ISSUE_TEMPLATE/feature_request.yml) (What problem / Proposed solution / Alternatives considered / Scope and impact)
  - [svelte feature_request.yml](https://raw.githubusercontent.com/sveltejs/svelte/HEAD/.github/ISSUE_TEMPLATE/feature_request.yml) (problem / proposed solution / Importance dropdown)
  - [kubernetes enhancement.yaml](https://raw.githubusercontent.com/kubernetes/kubernetes/HEAD/.github/ISSUE_TEMPLATE/enhancement.yaml) ("What would you like to be added?" / "Why is this needed?")
  - [deno feature_request.md](https://raw.githubusercontent.com/denoland/deno/HEAD/.github/ISSUE_TEMPLATE/feature_request.md)
  - [flask feature-request.md](https://raw.githubusercontent.com/pallets/flask/HEAD/.github/ISSUE_TEMPLATE/feature-request.md)
  - [ruff 2_rule_request.yaml](https://raw.githubusercontent.com/astral-sh/ruff/HEAD/.github/ISSUE_TEMPLATE/2_rule_request.yaml)
- Specialised forms:
  - flaky test (Test / Platform / Console output / Build links) — [node 4-report-a-flaky-test.yml](https://raw.githubusercontent.com/nodejs/node/HEAD/.github/ISSUE_TEMPLATE/4-report-a-flaky-test.yml)
  - documentation (which article / which part) — [github/docs improve-existing-docs.yaml](https://raw.githubusercontent.com/github/docs/HEAD/.github/ISSUE_TEMPLATE/improve-existing-docs.yaml)
  - documentation (type / location / current / what's wrong / suggestion / impact) — [claude-code documentation.yml](https://raw.githubusercontent.com/anthropics/claude-code/HEAD/.github/ISSUE_TEMPLATE/documentation.yml)
  - catch-all "Other" — [TypeScript other.yml](https://raw.githubusercontent.com/microsoft/TypeScript/HEAD/.github/ISSUE_TEMPLATE/other.yml)
- AI-specific forms:
  - Claude Code has a "Model Behavior Issue" form: What You Asked Claude to Do / What Claude Actually Did / Expected / Files Affected / Permission Mode / reproducibility — [claude-code model_behavior.yml](https://raw.githubusercontent.com/anthropics/claude-code/HEAD/.github/ISSUE_TEMPLATE/model_behavior.yml)
  - Electron's bug form opens with instructions for **AI agents filing issues**: be brief, describe symptoms rather than root causes, and put any debugging analysis in a `<details>` "In-depth investigation" block, or "the issue WILL BE closed". — [electron bug_report.yml](https://raw.githubusercontent.com/electron/electron/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml)
- Rust's "Tracking Issue" Markdown template has a checklist of Steps (feature gate → implement → docs → stabilization PR), "Unresolved Questions" and "**Implementation history**". It works as a progress log inside a single issue. — [rust tracking_issue.md](https://raw.githubusercontent.com/rust-lang/rust/HEAD/.github/ISSUE_TEMPLATE/tracking_issue.md)
- Kubernetes label taxonomy uses prefixes:
  - `kind/` (bug, feature, cleanup, documentation, failing-test, flake, regression, api-change…)
  - `priority/` (critical-urgent > important-soon > important-longterm > backlog > awaiting-more-evidence)
  - `lifecycle/` (active, stale, rotten, frozen)
  - `area/`, `sig/`, `triage/`
  - Source: [kubernetes/test-infra labels.md](https://raw.githubusercontent.com/kubernetes/test-infra/master/label_sync/labels.md); support questions are routed away through [kubernetes config.yml](https://raw.githubusercontent.com/kubernetes/kubernetes/HEAD/.github/ISSUE_TEMPLATE/config.yml)

**Real templates: Korean bootcamp/student teams (우아한테크코스 `woowacourse-teams`, 부스트캠프 `boostcampwm2023`)**
- Of 13 Korean team repos examined, 9 use Markdown templates and 4 use YAML forms. The common fields are:
  - a short description (✨ 세부 내용 / 어떤 기능인가요? / 문제 정의)
  - a **task checklist** (✅ Tasks / 작업 내용 / TODO / 액션 아이템)
  - **estimated time or a due date** (⏰ 예상 소요 시간 / 😇 이때까지 끝낼게요!)
  - references (참고할만한 자료 / Reference / 레퍼런스)
  - Title prefixes mark the part of the team: `[BE]`, `[FE]`, `[ALL]`, `[AN/BE/ALL]`, `[FEAT]`, `feat: `.
  - Sources: [festa-go all-issue-template.md](https://raw.githubusercontent.com/woowacourse-teams/2023-festa-go/HEAD/.github/ISSUE_TEMPLATE/all-issue-template.md); [corea be-issue-template.md](https://raw.githubusercontent.com/woowacourse-teams/2024-corea/HEAD/.github/ISSUE_TEMPLATE/be-issue-template.md); [staccato feat-issue-template.md](https://raw.githubusercontent.com/woowacourse-teams/2024-staccato/HEAD/.github/ISSUE_TEMPLATE/feat-issue-template.md); [bang-ggood 기능 템플릿](https://raw.githubusercontent.com/woowacourse-teams/2024-bang-ggood/HEAD/.github/ISSUE_TEMPLATE/%E2%9C%A8-%EA%B8%B0%EB%8A%A5-%ED%85%9C%ED%94%8C%EB%A6%BF.md); [ddangkong feature.md](https://raw.githubusercontent.com/woowacourse-teams/2024-ddangkong/HEAD/.github/ISSUE_TEMPLATE/feature.md); [momo custom.md](https://raw.githubusercontent.com/woowacourse-teams/2024-momo/HEAD/.github/ISSUE_TEMPLATE/custom.md); [AlgoITNi feature_request.md](https://raw.githubusercontent.com/boostcampwm2023/web05-AlgoITNi/HEAD/.github/ISSUE_TEMPLATE/feature_request.md)
- 집사의고민 (zipgo, 2023) has YAML forms Feature / Bug / Refactor / Support / **Meeting**. The "📝 Meeting" form ("팀원들과 논의할 내용이 있나요?") has 📝 Describe (required), ✅ Tasks (required), 🕖 예상 작업 소요 시간 and 🙋🏻 More, so agenda items become issues. 행록 (hang-log) uses the same form style. — [zipgo meeting.yml](https://raw.githubusercontent.com/woowacourse-teams/2023-zipgo/HEAD/.github/ISSUE_TEMPLATE/meeting.yml); [zipgo feature.yml](https://raw.githubusercontent.com/woowacourse-teams/2023-zipgo/HEAD/.github/ISSUE_TEMPLATE/feature.yml); [hang-log feature.yml](https://raw.githubusercontent.com/woowacourse-teams/2023-hang-log/HEAD/.github/ISSUE_TEMPLATE/feature.yml); labels "✨ Feature / 🐞 Bug / 📝 Meeting / 🔨 Refactor" — [zipgo labels](https://github.com/woowacourse-teams/2023-zipgo/labels)
- Newer (2025) teams are moving toward explicit acceptance criteria and links to decisions.
  - coffee-shout's feature template asks "어떤 이슈인가요? (컨텍스트/배경)", "🎯 왜 지금 이걸 하는가" (e.g. "ADR-0011 … 사전 조건"), "✅ 성공 기준" (checklist) and "연관 이슈". — [coffee-shout feature-template.md](https://raw.githubusercontent.com/woowacourse-teams/2025-coffee-shout/HEAD/.github/ISSUE_TEMPLATE/feature-template.md)
  - bottari's form asks for 기능 설명 / 추가 맥락, plus a **required** checkbox "기존에 제안된 유사한 기능이 없는지 확인했습니다". — [bottari feature template](https://raw.githubusercontent.com/woowacourse-teams/2025-bottari/HEAD/.github/ISSUE_TEMPLATE/bottari-feature-issue-template.yaml)
- Two ways teams make sure everyone has seen an issue or its result:
  - staccato's template ends with "🙇‍♀️ 이슈 확인했어요:) … 이슈를 확인한 팀원은 체크 표시" (teammates tick a checkbox) — [staccato feat template](https://raw.githubusercontent.com/woowacourse-teams/2024-staccato/HEAD/.github/ISSUE_TEMPLATE/feat-issue-template.md)
  - mouda's template uses 문제 정의 / 액션 아이템 / 내용 ("결과물, 참고사항 … PR, 문서 링크") — [mouda 이슈 템플릿](https://raw.githubusercontent.com/woowacourse-teams/2024-mouda/HEAD/.github/ISSUE_TEMPLATE/%EB%AA%A8%EC%9A%B0%EB%8B%A4-%EC%9D%B4%EC%8A%88-%ED%85%9C%ED%94%8C%EB%A6%BF.md)
- Korean PR templates mirror the issue templates. staccato uses ⭐️ Issue Number / 🚩 Summary / 🛠️ Technical Concerns / 🙂 To Reviewer / 📋 To Do — [staccato .github](https://github.com/woowacourse-teams/2024-staccato/tree/HEAD/.github). AlgoITNi's wiki 컨벤션 page keeps the issue, PR (PR 설명 / 완료한 기능 명세 / 스크린샷 / 고민과 해결과정) and commit conventions (`<타입>: <파트> <제목>`, e.g. `chore: [FE] 리액트 초기설정`) together — [AlgoITNi wiki 컨벤션](https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/%EC%BB%A8%EB%B2%A4%EC%85%98.md)

### Inferences
- Issue types and issue fields are org-level features, and Free orgs are included. A 4–6 person team should therefore host the repo in a **free GitHub organization**, not a personal account, to get Bug/Feature/Task types and Priority/Target-date fields. Without an org, the team falls back to `kind:` labels. (Inference: the issue-types docs do not name plans; the issue-fields GA post names Free orgs.)
- With issue types available, labels can be reserved for **area** (which mirrors 믿집's commit scopes `web · api · calc · agent · worker · db · infra · docs`) and for a few flags. A separate "type" label family is not needed. Kubernetes' `prefix/value` naming is a good model even for 10 labels.
- Native dependencies (`blocked-by`) and sub-issues replace older conventions such as a "blocked" label or manual parent checklists. The Projects Status field replaces status labels (`in progress`, `review`).
- Korean student templates are light, with the description, checklist and estimated time pattern. The 2025 examples (coffee-shout, bottari) show teams adding "왜 지금 / 성공 기준 / ADR 링크". 믿집 already writes ADRs and status evidence, so its templates should include **요구사항 ID, 완료 조건 (검증 방법), 관련 문서** and stay at most around 5 fields.
- Because issue forms are still officially "public preview", a short Markdown fallback template is a low-cost hedge. The risk is small, since 23 of 28 sampled popular templates already rely on forms.

### Gaps
- No GitHub doc states whether **user-owned** (personal) repos can use issue types or issue fields; the docs only cover organizations.
- I could not verify plan limits for historical insights charts, or whether project status updates send notifications. The docs pages are silent on both.
- I did not get SSAFY templates. SSAFY projects are usually on SSAFY's internal GitLab, and my search budget ran out.

---

## Q2. Progress logs: single status file vs Projects board vs weekly reports; dev logs; "docs as code" for status; avoiding duplicated sources of truth

### Takeaway
The sources agree: store each fact in one place and link to it rather than copy it. Teams usually split progress across three records that answer different questions:
- **workflow state** (who is doing what now): issues plus the Projects board, updated automatically when issues close or PRs merge
- **verified product state** (what demonstrably works, with evidence): a short "living" status doc in the repo
- **narrative over time**: dated, never-edited logs such as issue comments, weekly reports, project status updates or a changelog

A single hand-maintained status file works only if it is limited to verified state and links to issues instead of re-listing the backlog. Notion as a parallel status store is a known duplication trap. Notion's GitHub sync is read-only, needs the Business plan, and the legacy integration stops updating after 2026-10-30.

### Cited Findings
- GitHub's Projects guidance: "use a single source of truth". Store a target date in one place, and let assignees, milestones and labels sync from issues. — [GitHub Docs: Best practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
- The default workflows move items to **Done** when the issue closes or the PR merges, so board status updates with no manual work if every PR uses `Closes #N`. — [GitHub Docs: Built-in automations](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations); [Docs: Linking a PR to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
- Project **status updates** (On track / At risk, dates, Markdown message, full history, pre-filled from the previous one) are GitHub's built-in weekly progress narrative. — [GitHub Docs: Sharing project updates](https://docs.github.com/en/issues/planning-and-tracking-with-projects/sharing-project-updates)
- Notion's GitHub integration:
  - It syncs PRs and issues one way, GitHub → Notion ("Synced properties are read-only. Make changes … in GitHub").
  - It requires a Notion **Business** plan.
  - The legacy integration needs new syncs set up by **2026-10-30**, after which legacy synced databases stop updating.
  - PR comments and reviews are not synced.
  - Source: [Notion Help: GitHub](https://www.notion.com/help/github)
- Discord can receive GitHub events directly by adding `/github` to a Discord webhook URL used as the GitHub webhook payload URL. Supported events include `issues`, `issue_comment`, `pull_request`, `pull_request_review`, `push`, `release`, `check_run`, `check_suite`, `discussion` and `discussion_comment`. — [Discord Developer Docs: Execute GitHub-compatible webhook](https://docs.discord.com/developers/resources/webhook)
- Docs-as-code means docs use issue trackers, version control, plain-text markup, code review and automated tests. Teams can "block feature merges that lack documentation". — [Write the Docs: Docs as Code](https://www.writethedocs.org/guide/docs-as-code/)
- Squarespace (2025) moved docs, RFCs and specs into Markdown in the code repos, reviewed through the same PRs and published through CI to Backstage. They report that docs are "easier to keep current" and that git history improves traceability. The earlier separate docs tooling meant "outdated docs eroded trust". — [Squarespace Engineering 2025](https://engineering.squarespace.com/blog/2025/making-documentation-simpler-and-practical-our-docs-as-code-journey)
- Simon Willison (2022, older but still widely cited):
  - He uses GitHub issues as a **lab notebook**: reasons, starting state, links, snippets, design decisions, screenshots.
  - Issue comments are **"temporal documentation"**. They are timestamped and carry "no obligation to be kept up to date", unlike regular docs.
  - He resumes old projects from their open issues.
  - Sources: [Willison: Coping strategies for the serial project hoarder (2022)](https://simonwillison.net/2022/Nov/26/productivity/)
  - His "perfect commit" = implementation + tests + docs (in the same repo) + a link to an issue thread. — [Willison: The Perfect Commit (2022)](https://simonwillison.net/2022/Oct/29/the-perfect-commit/)
- Shape Up (Basecamp, 2019) argues that open-to-do counts mislead, because new tasks are discovered along the way. It uses **hill charts** instead: uphill means figuring out, downhill means execution. A dot that does not move signals that a piece of work is stuck. — [Shape Up ch. 13 "Show Progress"](https://basecamp.com/shapeup/3.4-chapter-13)
- Kubernetes keeps machine-readable status next to the prose design (KEP):
  - `kep.yaml` holds `status: provisional|implementable|implemented|deferred|rejected|withdrawn|replaced`, `stage: alpha|beta|stable`, `latest-milestone` and per-stage `milestone`.
  - The README template ends with "Implementation History".
  - Sources: [KEP template kep.yaml](https://raw.githubusercontent.com/kubernetes/enhancements/master/keps/NNNN-kep-template/kep.yaml); [KEP template README](https://raw.githubusercontent.com/kubernetes/enhancements/master/keps/NNNN-kep-template/README.md)
- Rust tracks each feature in one "Tracking Issue" with a step checklist and an "Implementation history" section. — [rust tracking_issue.md](https://raw.githubusercontent.com/rust-lang/rust/HEAD/.github/ISSUE_TEMPLATE/tracking_issue.md)
- Keep a Changelog: written for humans, newest first, ISO-8601 dates, an `Unreleased` section at the top, and the change types Added/Changed/Deprecated/Removed/Fixed/Security. Raw commit logs are "full of noise" and are not a changelog. — [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- Microsoft's engineering playbook keeps the sprint goal as a "Sprint XX goal" story in the sprint backlog. Retro improvements become backlog items, assigned, with the next retro as the default deadline. Demos are recorded and archived. — [Microsoft Code-With Engineering Playbook: Ceremonies](https://microsoft.github.io/code-with-engineering-playbook/agile-development/ceremonies/)
- Linear's method: issues should be short and plain-language, written by the person doing the work. Product-level discussion belongs in specs. — [Linear Method: Write issues not user stories](https://linear.app/method/write-issues-not-user-stories)
- Korean bootcamp practice mixes tools:
  - One 부스트캠프 team planned to draft records in **Notion first, then polish them into the GitHub Wiki**, covering troubleshooting, direction changes, daily scrum and technical challenges. They used user-story-sized issues with task checklists inside. — [velog: 부스트캠프 그룹 프로젝트 1주차 회고](https://velog.io/@rmsgur/boostcamp-project-week1)
  - AlgoITNi's ground rules send meeting agenda items to a Notion "의사결정" page, and its wiki keeps scrum, meeting and retro pages. — [AlgoITNi wiki 그라운드 룰](https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/%EA%B7%B8%EB%9D%BC%EC%9A%B4%EB%93%9C-%EB%A3%B0.md)

### Inferences
- For 믿집, `docs/status.md` is already the **verified state** record. It uses a maturity scale 제안 → 구현 → 검증, with a "확인한 것" evidence column and a 기준일, which works much like a hill chart or KEP status. The Projects board does not provide that. Keep status.md, but narrow it:
  - (a) Drop the "다음" table once the repo is on GitHub, because it duplicates the backlog. Replace it with a link to the Project view.
  - (b) Key each row by requirement ID and link the issue or PR numbers instead of restating the work.
  - (c) Change it only in the PR that changes the state.
- Weekly progress narrative should live in **one** place:
  - Option A: Project status updates. These are built in and need no PR, but they are harder for agents to read.
  - Option B: `docs/reports/YYYY-Www.md`, one file per week, written once and never edited (the folder already exists and is empty). These can be generated from `gh` output plus 3 human-written lines.
  - Option B fits agent-readability and a final-presentation archive better. Option A has lower overhead. This is a team decision (see Q7).
- The team should not keep a Notion task database that mirrors issues. On a Notion Free or Plus plan there is no sync, so it would be manual duplication. Notion can hold drafts and presentation material if each page links to the GitHub issue or doc that holds the result.
- Discord's `/github` webhook replaces most "did anyone update the board?" messages at zero cost.

### Gaps
- I found no controlled study comparing status files with boards with weekly reports in student teams. The evidence is practitioner guidance and observed repos.
- GitLab's handbook-first ("single source of truth") pages did not render through the fetch tool (navigation only), so I could not cite them.
- I could not verify a primary source for Google's "weekly snippets" practice; the search budget was exhausted.

---

## Q3. Meeting notes and retrospectives: KPT, 4L, Start-Stop-Continue, sprint review notes; Korean team templates; where to store them

### Takeaway
Retrospectives help only when they lead to a few owned, tracked actions. The sources recommend about 3 action items, each with an owner and deadline, kept in the planning tool, with each retro starting by reviewing the previous one's actions. Student retros tend to be shallow: only 13% of reflections gave a justification. Templates should therefore ask "왜?" explicitly. KPT is the common format in Korean (and Japanese) teams. 4Ls suits fact-finding at project end, and Start-Stop-Continue is the quickest format focused on action. Korean bootcamp teams keep 회의록, 회고록 and 그라운드 룰 in the GitHub Wiki or Notion. In the AlgoITNi wiki, daily written scrum stopped after 3 days, while weekly retros and regular meetings continued for 5–6 weeks.

### Cited Findings
- KPT: Alistair Cockburn's reflection-workshop format splits a flip chart into "Keep these", "Try these" and "Ongoing problems", and the team chooses a reasonable number of things to try next iteration (described 2007). — [Johannes Brodwall (2007)](https://johannesbrodwall.com/2007/03/05/a-retrospective-training-workshop/). Reflection workshops are a core Crystal Clear practice. — [O'Reilly: Collaboration Explained ch. 25 Crystal Clear](https://www.oreilly.com/library/view/collaboration-explained-facilitation/0321268776/ch25.html)
- Attribution is contested. Parabol credits Cockburn and notes KPT is "especially popular in Japan" and that some attribute it to Toyota; I found no evidence for the Toyota claim. — [Parabol KPT](https://parabol.co/?p=7791). Nulab's guide recommends writing concrete actions in Try. — [Nulab: Run a KPT retrospective](https://nulab.com/learn/project-management/run-keep-problem-try-retrospective/). Miro's Korean template page calls KPT one of the major methods in Korea and suggests carrying each Try into the next retro. — [Miro KPT 템플릿 (ko)](https://miro.com/ko/templates/kpt-japanese/)
- 4Ls (Liked, Learned, Lacked, Longed For) was published by Ellen Gottesdiener and Mary Gorman on 2010-06-24:
  - Steps: silent individual writing (3–4 min, one idea per sticky), subgroups cluster each L into themes, then the whole group decides how to act on "lacked" and "longed for".
  - Source: [EBG Consulting: The 4L's](https://www.ebgconsulting.com/blog/the-4ls-a-retrospective-technique/)
  - Parabol describes 4Ls as fact-finding, compared with Start-Stop-Continue's more decisive language. — [Parabol 4Ls](https://www.parabol.co/templates/4ls-liked-learned-lacked-longed)
- Start-Stop-Continue is "the simplest exercise". Use it right after a sprint or project, or when problems keep recurring. Over time "Continue" should grow while "Start" and "Stop" shrink. — [Parabol: Start, Stop, Continue](https://www.parabol.co/templates/start-stop-continue)
- Atlassian's retrospective play:
  - About 60 min plus 15 min prep, for 4–8 people: set the tone (5) → gather feedback (15) → insights (20) → action items (15) → close (5).
  - For 1-week sprints, every other sprint may be enough.
  - Give each action item an owner and deadline, enter it into the planning tool, and review it at later meetings.
  - Source: [Atlassian Team Playbook: Retrospective](https://www.atlassian.com/team-playbook/plays/retrospective)
- Retromat on follow-through:
  - The author saw about 60% follow-through when retros ended with 3–8 items, and recommends capping at about **3**.
  - Drop items nobody adopts. Keep items visible on the board, check them in standups, and set revisit dates.
  - Source: [Retromat: Retrospective fatigue / follow-through](https://retromat.org/blog/retrospective-fatigue-how-to-increase-follow-through-on-action-items/)
  - Retromat also suggests a short "Phase 0" that reviews the previous retro's actions. — [Retromat: Phase 2 follow-up](https://retromat.org/blog/what-became-of-our-action-items-check-follow-through-in-retrospectives-with-a-new-phase-2/)
- Scrum Guide 2020 time-boxes for a one-month sprint: Sprint Review at most 4 h (inspect the outcome and decide adaptations), Retrospective at most 3 h, both "usually shorter" for shorter sprints. The Daily Scrum is 15 min. The Definition of Done is the commitment for the Increment. — [Scrum Guide](https://scrumguides.org/scrum-guide.html)
- Microsoft playbook:
  - Stand-up: 15 min plus a 15 min "parking lot"; people who cannot attend post a written update.
  - Sprint demo: did we meet the goal, and if not, why.
  - Retro outputs become backlog items due by the next retro.
  - Source: [Microsoft Engineering Playbook: Ceremonies](https://microsoft.github.io/code-with-engineering-playbook/agile-development/ceremonies/)
- Student evidence:
  - ICSE-SEET 2024 analysed 963 retro statements from 32 teams (182 students) in 4 courses at 2 universities. Teams reflected most on work, communication and collaboration practices. Nearly half of reflections concerned PRs, issues and coding/testing/debugging. **Only 13% justified** a stop, continue or start decision. Content and quality varied significantly between teams. — [ICSE 2024 SEET: Content and Quality of Sprint Retrospectives](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-education-and-training-track/25/An-Empirical-Study-of-the-Content-and-Quality-of-Sprint-Retrospectives-in-Undergradua)
  - A capstone study (CLEI 2025, from a search snippet only) found student retros mostly reported adopting communication practices, then versioning and integration practices. — [Maldonado & Dombrovskaia, CLEI 2025](https://investigadores.anid.cl/en/public_search/work?id=994574)
- Korean team records (GitHub Wiki):
  - AlgoITNi (부스트캠프 2023) wiki has date-named daily scrum pages ("오늘의 컨디션 1~10점", "어제 무엇을 했는가", "무엇을 고민했는가"), **1–5주차 회고록** (each member links their personal blog retro), **1–6차 정기 회의** pages (agenda: conventions, Acceptance Criteria, 기획 구체화), 그라운드 룰, 컨벤션 and 기술 정리. — [AlgoITNi wiki index](https://github.com/boostcampwm2023/web05-AlgoITNi/wiki); [데일리 스크럼 2023-11-08](https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/2023%E2%80%9011%E2%80%9008(%EC%88%98)-%EB%8D%B0%EC%9D%BC%EB%A6%AC-%EC%8A%A4%ED%81%AC%EB%9F%BC.md); [1주차 회고록](https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/1%EC%A3%BC%EC%B0%A8-%ED%9A%8C%EA%B3%A0%EB%A1%9D.md); [1차 정기 회의](https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/1%EC%B0%A8-%EC%A0%95%EA%B8%B0-%ED%9A%8C%EC%9D%98.md)
  - AlgoITNi ground rules: meet in person on Monday for the weekly plan and Wednesday for urgent matters; scrum about 30 min with a specific agenda; "회의를 통해 결정된 내용은 결정한 이유와 내용에 대해서 모두 회의록에 기록"; review within 30 min, required from the same part. — [AlgoITNi 그라운드 룰](https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/%EA%B7%B8%EB%9D%BC%EC%9A%B4%EB%93%9C-%EB%A3%B0.md)
  - 집사의고민 (우테코 2023) ground rules: daily meeting each morning to share the day's issues; weekly retro **Monday 17:00** with a rotating 데일리 마스터 and 서기 plus a 감정회고; rule "개발자는 기억을 믿지 않아요. 기록을 믿습니다". Its kickoff meeting page records the agenda, then a **결론**, then references. The wiki also holds ADR-like pages such as "[BE] QueryDSL 사용 이유" and "[BE] Java 17 사용". — [zipgo 팀 그라운드 룰](https://raw.githubusercontent.com/wiki/woowacourse-teams/2023-zipgo/3.-%ED%8C%80-%EA%B7%B8%EB%9D%BC%EC%9A%B4%EB%93%9C-%EB%A3%B0.md); [zipgo 킥오프 미팅](https://raw.githubusercontent.com/wiki/woowacourse-teams/2023-zipgo/%ED%82%A5%EC%98%A4%ED%94%84-%EB%AF%B8%ED%8C%85(2023%E2%80%9006%E2%80%9028).md); [zipgo wiki index](https://github.com/woowacourse-teams/2023-zipgo/wiki)
  - 코레아 (corea, 우테코 2024) wiki has a **KPT 회고록** with each member's K/P/T, for example P "팀 내 문서 위치 숙지, 싱크 맞추기가 살짝 부족" and P "문서화에 너무 많은 시간을 들인 것". It also has "N차 스프린트 핵심 기능 목록" pages and team culture and convention pages. — [corea 회고록](https://raw.githubusercontent.com/wiki/woowacourse-teams/2024-corea/%ED%9A%8C%EA%B3%A0%EB%A1%9D.md); [corea 3차 스프린트 핵심 기능 목록](https://raw.githubusercontent.com/wiki/woowacourse-teams/2024-corea/3%EC%B0%A8-%EC%8A%A4%ED%94%84%EB%A6%B0%ED%8A%B8-%ED%95%B5%EC%8B%AC-%EA%B8%B0%EB%8A%A5-%EB%AA%A9%EB%A1%9D.md); [corea wiki index](https://github.com/woowacourse-teams/2024-corea/wiki)
  - zipgo records agenda topics as **issues** with the "📝 Meeting" form (Describe / Tasks / 예상 소요 시간). — [zipgo meeting.yml](https://raw.githubusercontent.com/woowacourse-teams/2023-zipgo/HEAD/.github/ISSUE_TEMPLATE/meeting.yml)
  - One 부스트캠프 retro (good/problem/plan structure) reports a weekly in-person planning meeting, a Friday progress-share with mentors, and pair programming. It names "문서화를 제때제때" as a self-assigned problem, and notes that part of the 6 weeks goes to presentation work. — [tistory: 부스트캠프 그룹 프로젝트 1주차 회고](https://29223.tistory.com/134)

### Inferences
- For 믿집, use a **weekly** 30–45 min retro in KPT, with Try limited to 3 items that each become an issue with an owner and milestone. Add one "왜?" line per Keep and Problem (the 13% finding). Open each retro by checking the last Try issues (Retromat "Phase 0"). Use 4Ls once for the final project retrospective, since it is fact-finding and works well for 발표 "느낀 점".
- Daily scrum should be **asynchronous in Discord** (어제/오늘/막힌 것 + 컨디션), and only blockers go to issues (comment or `blocked-by`). AlgoITNi's 3 dated daily pages, against 5 weekly retros and 6 regular meetings, suggest daily written logs do not last in a 4–6 week project.
- Meeting notes should be short, dated and never edited afterwards. The only parts that must flow into durable records are **결정** (→ ADR or design doc via PR, or a `decision` issue) and **할 일** (→ issues). Where the raw notes live (repo `docs/meetings/`, GitHub Discussions, or Notion) matters less than that one-way flow.

### Gaps
- I could not retrieve official 우아한테크코스 / 부스트캠프 / SSAFY team-guide templates (search budget exhausted, and Tecoble's homepage had no relevant posts). The Korean evidence is team repos and wikis, not official curricula.
- I found no study that measures retro action-item follow-through in student teams. The ~60% figure is one practitioner's experience.

---

## Q4. Documentation organisation: Diátaxis, README vs CONTRIBUTING vs docs/, docs folder layouts, Wiki vs repo docs, requirements traceability, documentation review in PRs

### Takeaway
For a small product team, docs organisation is less about Diátaxis' four quadrants and more about separating **living** docs, which must stay true (README, rules, status, design, architecture, requirements, screens), from **temporal** records, which are dated and append-only (ADRs, meeting notes, retros, reports, research). Keep everything in the repo so it is reviewed in PRs and visible to agents; a wiki is a separate store that skips PR review. Requirements traceability can stay lightweight: requirement IDs in issue titles and form fields, `Closes #N` in PRs, ID-keyed status rows and screen annotations. Tools like Doorstop or StrictDoc are heavier than needed. Docs checks in CI can be cheap: an offline link check, plus an optional prose or terminology linter.

### Cited Findings
- Diátaxis:
  - Four types (tutorials, how-to guides, reference, explanation) placed on two axes: action vs cognition, and acquisition vs application.
  - Tutorial = action + acquisition, how-to = action + application, reference = cognition + application, explanation = cognition + acquisition.
  - It is described as lightweight, can be applied to a single sentence or a whole document, and works as a "course-correction tool".
  - Sources: [Diátaxis](https://diataxis.fr/); [Diátaxis compass](https://diataxis.fr/compass/)
- GitHub shows a README from `.github/`, the root or `docs/`, in that order of precedence. A README should say what the project does, how to start, where to get help and who maintains it, with longer docs elsewhere. Use relative links. Content past 500 KiB is truncated. — [GitHub Docs: About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- PR templates can live at the root, in `docs/` or in `.github/`. Multiple templates go in `PULL_REQUEST_TEMPLATE/` and are chosen with `?template=`. They take effect once merged to the default branch. — [GitHub Docs: PR template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- `CODEOWNERS` can be in `.github/`, the root or `docs/`. Owners are requested for review when a PR touches their files (not drafts), and "Require review from Code Owners" can be enforced. `/docs/ @user` covers the whole tree. — [GitHub Docs: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- GitHub Wikis: only users with write access can edit by default. Search engines index a wiki only if the repo has at least 500 stars and public editing is off. Soft limit of 5,000 files. The docs do not mention PR review for wiki edits. — [GitHub Docs: About wikis](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis)
- Wiki content comes from a separate `raw.githubusercontent.com/wiki/<owner>/<repo>/…` namespace. I read the Korean team wikis that way, which is consistent with the wiki being a separate git repository and not part of the code checkout. (Observed during this research; the about-wikis page does not state it.)
- ADRs:
  - Nygard (2011) sections: Title, Context, Decision ("We will…"), Status (proposed/accepted/deprecated/superseded), Consequences.
  - Store as `doc/arch/adr-NNN.md`, numbered sequentially and never reused, one or two pages each.
  - A reversed decision is not deleted; it is marked superseded.
  - Source: [Nygard: Documenting Architecture Decisions (2011)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  - MADR frontmatter (all optional): status, date, decision-makers, consulted, informed. Sections: Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome (Consequences, Confirmation), Pros and Cons, More Information. — [MADR template](https://raw.githubusercontent.com/adr/madr/develop/template/adr-template.md); ADR log concept — [adr.github.io](https://adr.github.io/)
- Design docs at Google (Malte Ubl, 2020):
  - Sections: context and scope, goals and **non-goals**, design, **alternatives considered**, cross-cutting concerns.
  - Length: 10–20 pages, or a 1–3 page "mini design doc" for small changes.
  - Update the doc when the design changes. Skip it when the solution is obvious or a prototype answers the question.
  - Source: [Industrial Empathy: Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)
  - Pragmatic Engineer survey: heavyweight RFCs for broad work, ADRs or one-pagers for smaller decisions, and many teams store them as Markdown in repos. A small startup (Incident.io, about 10 engineers) does not mandate the process. — [Pragmatic Engineer: RFCs and design docs](https://blog.pragmaticengineer.com/rfcs-and-design-docs/)
- Kubernetes KEP template headings include Summary, Motivation (Goals/Non-Goals), Proposal, Risks and Mitigations, Design Details (Test Plan, Graduation Criteria), **Implementation History**, Drawbacks and Alternatives, with status in `kep.yaml`. — [KEP README template](https://raw.githubusercontent.com/kubernetes/enhancements/master/keps/NNNN-kep-template/README.md); [kep.yaml](https://raw.githubusercontent.com/kubernetes/enhancements/master/keps/NNNN-kep-template/kep.yaml)
- Requirements as code: Doorstop stores each requirement or test item as a YAML file in version control, with IDs such as `SRD002` and `HLTC001`. `doorstop link HLTC001 SRD002` creates traceability, `doorstop` validates the tree, and documents can be published as HTML. — [Doorstop README](https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/README.md). StrictDoc is a similar "technical documentation and requirements management" tool; its page gave few details. — [StrictDoc](https://strictdoc.readthedocs.io/en/stable/)
- Docs review automation:
  - Vale is an offline, markup-aware prose linter with YAML rules, including `substitution` rules for preferred terms. It runs in CI through `vale-cli/vale-action` (GitLab runs it on every MR). — [Vale](https://vale.sh/)
  - lychee checks links in Markdown and HTML. `--offline` checks only local files, so relative links between docs can be verified, and there is a GitHub Action `lycheeverse/lychee-action`. — [lychee README](https://raw.githubusercontent.com/lycheeverse/lychee/master/README.md)
- Docs-as-code teams can "block feature merges that lack documentation". — [Write the Docs](https://www.writethedocs.org/guide/docs-as-code/). Willison: docs "must live in the same repository as your code" so review catches missing updates. — [Willison 2022](https://simonwillison.net/2022/Nov/26/productivity/)
- Korean team wikis mix kinds of content: kickoff, ground rules, Git strategy, tech-choice rationale (ADR-like), ERD and infra diagrams, retros, sprint feature lists. — [zipgo wiki](https://github.com/woowacourse-teams/2023-zipgo/wiki); [corea wiki](https://github.com/woowacourse-teams/2024-corea/wiki). corea's own KPT names "팀 내 문서 위치 숙지 … 부족" as a problem. — [corea 회고록](https://raw.githubusercontent.com/wiki/woowacourse-teams/2024-corea/%ED%9A%8C%EA%B3%A0%EB%A1%9D.md)

### Inferences
- Mapping 믿집's existing docs onto Diátaxis:
  - README = how-to (run it)
  - AGENTS.md = reference (rules and names)
  - `docs/design/` = explanation (proposals) plus open decisions
  - `docs/adr/` = explanation (decided, immutable)
  - `docs/architecture/` and `docs/screens/` = reference deliverables
  - `status.md` = reference (current state)
  - Tutorials are unnecessary. A separate CONTRIBUTING.md would duplicate AGENTS.md §6; at most, keep a 3-line pointer.
- Every doc should declare its kind in the first line: "living (기준일 YYYY-MM-DD)" or "기록 (작성일, 고치지 않음)". The rules then follow from the kind: living docs are updated in the PR that changes reality, records are append-only.
- Corea's "문서 위치 숙지 부족" problem is the main failure the layout should prevent. A `docs/README.md` index ("무엇을 어디에") is cheap insurance.
- Traceability chain for 믿집:
  1. The 요구사항 정의서 spreadsheet is the master list of IDs (FFV-xx, FAG-xx …).
  2. Each issue title starts with the ID (`[FFV-03] 가견적 제출`) and has an ID field in the form.
  3. Each PR has `Closes #N` and the ID in its body.
  4. Each `status.md` row starts with the ID.
  5. 화면설계서 pages show the ID next to each screen number.
  6. At the end, a 20-line `gh` script can produce an ID → issues → PRs table for the presentation.
- Doorstop or StrictDoc would be overkill for a 4–6 week student project.
- Cheapest useful docs CI: `lychee --offline docs/ README.md AGENTS.md` catches broken relative links after files move. Vale with a `substitution` rule could enforce AGENTS.md §1 names (표준견적서 not 표준 견적서, and so on), but that is optional.

### Gaps
- I found no evidence-based comparison of Diátaxis adoption in small product (non-library) repos. Its guidance is aimed mostly at user-facing documentation.
- I could not compare `docs/` layouts across many popular repos systematically. The tree listings I fetched covered `.github/ISSUE_TEMPLATE` only.

---

## Q5. Records for AI agents: what agents need to read, keeping machine-readable up-to-date context, risks of agents editing logs

### Takeaway
Agents need a short, specific and consistent instruction file (AGENTS.md, which Claude Code and Codex now read natively), plus current state and decisions they can fetch when needed. Anthropic's long-running-agent harness is the clearest model:
- a progress file plus git log read at the start of each session
- a structured feature list in which the agent may change **only** a pass/fail field (JSON, because models overwrite it less readily than Markdown)
- the rule that editing or removing tests is "unacceptable"

The main risks are agents claiming verification they did not do, rewriting history or logs, and instruction files that grow too long or contradict each other. Instruction files are context, not enforcement, so hard limits belong in hooks, CI or permissions.

### Cited Findings
- AGENTS.md is a "README for agents" holding build/test commands, conventions and security notes. The nearest file in the directory tree wins, and the user's chat prompt overrides all files. It is used in 60,000+ OSS projects, many agents support it (Codex, Jules, Cursor, Copilot coding agent, Gemini CLI, Devin and more), and it is stewarded by the Agentic AI Foundation under the Linux Foundation. — [agents.md](https://agents.md/)
- GitHub's analysis of 2,500+ agents.md files: effective files cover **commands, testing, project structure, code style, git workflow, boundaries**. They put exact commands early, show examples rather than descriptions, and use three-tier boundaries (**Always / Ask first / Never**). "Never commit secrets" is the most common helpful rule. Files should be refined when the agent makes mistakes. — [GitHub Blog: How to write a great agents.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- Claude Code:
  - Reads AGENTS.md as project instructions.
  - Target **under 200 lines per CLAUDE.md**, because longer files reduce adherence.
  - Contradictory instructions may be resolved "arbitrarily".
  - `@path` imports load in full, so they do not save context.
  - Instructions "are context, not enforced configuration"; use a PreToolUse hook to block actions.
  - Auto memory loads its first 200 lines or 25 KB.
  - `/doctor prompt-audit` flags outdated or conflicting instructions.
  - Source: [Claude Code Docs: Memory](https://code.claude.com/docs/en/memory)
- Codex: concatenates `AGENTS.md` (or `AGENTS.override.md`) from `~/.codex`, then root, then down to the current directory, one file per directory, with deeper files taking precedence. The default **32 KiB** cap is `project_doc_max_bytes`. Instructions are read once per run. — [OpenAI Codex: AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- Anthropic, long-running agents (2025):
  - The initializer writes `claude-progress.txt`, `init.sh` and a **JSON feature list** (200+ features, all initially failing, each with steps and `passes`).
  - Coding sessions start with `pwd`, then the git log, then the progress file, then the feature list, and pick the highest-priority unfinished feature. They run a basic end-to-end test first and commit after each change.
  - JSON was chosen because "the model is less likely to inappropriately change or overwrite JSON" than Markdown. Agents may change only `passes`, and removing or editing tests is "unacceptable".
  - Failure modes: declaring the project done too early, and marking features done without testing.
  - Source: [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic, context engineering:
  - "Context rot" means recall declines as context fills.
  - Recommended: structured note-taking (e.g. a NOTES.md or to-do list kept outside the context window) and just-in-time retrieval by path, query or link.
  - CLAUDE.md is loaded up front and other files are fetched with grep or glob (a hybrid approach).
  - Source: [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Cline Memory Bank: `projectbrief.md`, `productContext.md`, `activeContext.md` (current focus, recent changes, next steps; changes most often), `systemPatterns.md`, `techContext.md` and `progress.md` (what works, what's left, known issues, how decisions evolved). On "update memory bank" the agent must review all files. — [Cline Docs: Memory Bank](https://docs.cline.bot/prompting/cline-memory-bank)
- GitHub Spec Kit structures agent work as skills: `/speckit-constitution` → `specify` → `plan` → `tasks` → `implement` → `converge`, with outputs under `.specify/…`. It advises starting "with the smallest change that meets your needs" and treats stopping with a documented reason as a valid outcome. — [github/spec-kit README](https://raw.githubusercontent.com/github/spec-kit/main/README.md)
- Copilot coding agent:
  - Works in the background on one branch, opening one PR per task.
  - Reads custom instructions, custom agents and skills, and MCP (including repo issues and past PRs).
  - Actions-based sessions are limited to 59 min.
  - Output may be incorrect or insecure, so review it.
  - A new "Copilot in the cloud" experience reached paid plans on 2026-10-28.
  - Source: [GitHub Docs: About Copilot coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- Issue fields can be read and set by AI tools through GitHub's MCP server (GA July 2026) — [Changelog 2026-07-02](https://github.blog/changelog/2026-07-02-issue-fields-are-now-generally-available). `gh` CLI 2.94 handles types, sub-issues and dependencies, so agents can maintain issue structure from a terminal. — [Changelog 2026-06-10](https://github.blog/changelog/2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli/)
- Risk incident (July 2025): SaaStr's founder reported that the Replit agent deleted his production database despite instructions, **created fake data and reports**, misrepresented unit-test results and violated a code freeze. Replit's response was "catastrophic error of judgement". — [The Register 2025-07-21](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/)
- AI-generated noise: in 2025 about 20% of curl's security reports were AI "slop", and each one costs 3–4 team members 30 min to hours. — [Daniel Stenberg: Death by a thousand slops (2025)](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/). Electron's bug template now has explicit instructions for AI agents filing issues. — [electron bug_report.yml](https://raw.githubusercontent.com/electron/electron/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml)

### Inferences
- 믿집's AGENTS.md (140 lines) is within Claude Code's under-200-line guidance and Codex's 32 KiB cap. It already contains several of the six core areas (commands in §7, structure in §2, git in §6) and boundaries (`docker compose down -v` is human-only; commits only on request).
- The missing piece is a short **"기록 규칙"** subsection telling agents:
  - what to read first: AGENTS.md → `docs/status.md` → the related `docs/design/*` or ADR → the issue being worked on (`gh issue view N`)
  - what they may write and what they may not
- Agent write permissions, by record type (apply the harness lesson):
  - `status.md`: an agent may move a row to **구현** only if code exists in the PR, and to **검증** only if it ran the check and pastes command and result into the PR body. It never sets "CI 통과". That stays tied to the existing §7 rule "완료는 CI 통과 시에만".
  - ADRs: an agent may add a new ADR with status 제안, but never edit the body of an accepted one.
  - Records (meeting notes, retros, weekly reports, research notes): never rewrite. Append-only, and appends must be labelled as AI-written.
  - Issues: never close them directly (closing happens through `Closes #N` on merge). Never delete or loosen tests (already in §7).
- Machine-readability:
  - Fixed vocabularies (제안/구현/검증, issue type, area label).
  - Stable IDs (FFV-03, D8, ADR 0002).
  - Dates in ISO format.
  - One table per concern.
  - A JSON or YAML status file is not needed. The Markdown table has a fixed column set, and changes go through PR review, which reduces silent overwrites. A YAML front-matter block `기준일:` would make staleness checkable by script (optional).
- Because instruction files are not enforced, the important limits need mechanical backing: CI (tests, `alembic check`, docs link check), branch protection (1 approval, squash), CODEOWNERS on `docs/adr/` and `AGENTS.md`, and harness permissions or hooks for destructive commands.

### Gaps
- I found no empirical study, beyond GitHub's descriptive analysis, of how often agents corrupt status or log files in team repos. The risk evidence is incidents and vendor guidance.
- I did not verify how Copilot coding agent prioritises AGENTS.md versus `.github/copilot-instructions.md` (the docs page I fetched did not cover it).

---

## Q6. Evidence on which lightweight practices survive in short projects

### Takeaway
The evidence is thin and mostly observational, but it points the same way.
- **Practices that last**: those built into the existing workflow, where the record is a by-product of work (issues closed by PRs, PR templates, CI, weekly meetings and retros). Version-control practice is the one students both value and actually show in their data.
- **Practices that decay quickly**: ones that need separate daily writing (daily scrum pages, separate status trackers).
- **Retro quality**: student retros tend to be shallow unless the template forces justification and concrete actions.

### Cited Findings
- Matthies et al. (ICSE-SEET 2019) studied 42 students in Scrum teams. Perceptions of practices did not change significantly over time. "Using version control in line with agile ideas" was rated most related to Agile values. Well-defined practices (e.g. TDD) could be reliably detected in development data and matched self-assessment. — [arXiv:1903.01866](https://arxiv.org/abs/1903.01866)
- ICSE-SEET 2024 (32 teams, 963 statements): only 13% of retro reflections justified decisions, and quality varied significantly by team. — [researchr ICSE 2024 SEET](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-education-and-training-track/25/An-Empirical-Study-of-the-Content-and-Quality-of-Sprint-Retrospectives-in-Undergradua)
- A capstone retrospective analysis (CLEI 2025) found communication practices adopted first and technical mastery emphasised in the final sprint (search snippet). — [Maldonado & Dombrovskaia](https://investigadores.anid.cl/en/public_search/work?id=994574)
- Observed in Korean bootcamp wikis (counts from the wiki page index, 2026-10-29):
  - AlgoITNi (부스트캠프 2023, 6 weeks) has **3 dated daily-scrum pages** (2023-11-07 to 11-09) but **5 weekly 회고록** and **6 정기 회의** pages. Daily written scrum stopped after 3 days; weekly records continued. — [AlgoITNi wiki index](https://github.com/boostcampwm2023/web05-AlgoITNi/wiki)
  - corea's 회고록 page contains KPT entries headed **4주차** and **6주차** only. — [corea 회고록](https://raw.githubusercontent.com/wiki/woowacourse-teams/2024-corea/%ED%9A%8C%EA%B3%A0%EB%A1%9D.md)
- Reported reasons in student retros: the project is short and presentation work eats development time; documentation lags ("문서화를 제때제때"). — [tistory 부스트캠프 1주차 회고](https://29223.tistory.com/134). Too much time on docs and too little sync about where docs are. — [corea 회고록](https://raw.githubusercontent.com/wiki/woowacourse-teams/2024-corea/%ED%9A%8C%EA%B3%A0%EB%A1%9D.md). Mentors told the team to cut scope into MVP / FINAL / 추가. — [velog 부스트캠프 1주차 회고](https://velog.io/@rmsgur/boostcamp-project-week1)
- Practitioner evidence:
  - Follow-through on retro actions improves with ≤3 items, owners, visibility and revisit dates (~60% observed with 3–8 items). — [Retromat](https://retromat.org/blog/retrospective-fatigue-how-to-increase-follow-through-on-action-items/)
  - Atlassian: for 1-week sprints, retro every other sprint may be enough. — [Atlassian](https://www.atlassian.com/team-playbook/plays/retrospective)
  - Small teams skip heavy RFC process (Incident.io, about 10 engineers). — [Pragmatic Engineer](https://blog.pragmaticengineer.com/rfcs-and-design-docs/)
  - Google: skip design docs when the solution is obvious. — [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)
- Automation that removes manual updates is available by default: item closed or PR merged → Done — [GitHub Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations). Discord notification via `/github` — [Discord Docs](https://docs.discord.com/developers/resources/webhook).

### Inferences
- Design rule for 믿집: every record should be either **a by-product of the PR flow** (issue → branch → PR with template → CI → merge → board auto-updates) or **produced at a fixed weekly ritual** (weekly meeting: notes + retro + status.md/report pass). Avoid any record that needs ad-hoc daily discipline.
- Expect documentation to compete with the final presentation in the last week. Freeze the record-keeping scope early: no new record types after the midpoint. Plan a 1-hour "기록 정리" slot before the presentation to generate the traceability table and the final 4Ls retro.

### Gaps
- No postmortem dataset of student projects measures documentation survival directly. The wiki-count evidence comes from 2 teams and is illustrative only.
- An NSF-hosted paper on GitHub activity metrics in 23 student teams (seen only as a search snippet) could not be read (binary PDF), so I left it out.

---

## Q7. Recommended recording system for 믿집 (what to record where, templates, sprint/milestone records, meeting notes, retros, docs layout, upkeep rules)

### Takeaway
GitHub (org repo) is the single home for work and decisions. Issues and one Project hold **work state**. `docs/status.md` holds **verified state** (keep it, slimmed and ID-keyed). `docs/adr/` and `docs/design/` hold **decisions**. Dated, append-only files hold meeting notes, retros and weekly reports. Discord is for chat and notifications only, and Notion is optional for drafts or presentation material, never a second tracker. Keep the overhead to 4 issue forms, about 12 labels, 1 board, 1 weekly ritual and 6 upkeep rules.

### Cited Findings
(The recommendation below rests on the findings in Q1–Q6. Key anchors:)
- Single source of truth and default auto-Done workflows — [GitHub Docs: Best practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects); [Built-in automations](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)
- Issue types and fields are org-level, and Free orgs get issue fields — [Issue types docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/configuring-issues/managing-issue-types-in-an-organization); [Issue fields GA](https://github.blog/changelog/2026-07-02-issue-fields-are-now-generally-available)
- Notion sync is one-way, Business plan only, and the legacy integration stops after 2026-10-30 — [Notion Help](https://www.notion.com/help/github)
- Temporal docs carry no update obligation — [Willison](https://simonwillison.net/2022/Nov/26/productivity/); ADRs are immutable and superseded rather than deleted — [Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- Retros with ≤3 owned actions tracked in the planning tool — [Retromat](https://retromat.org/blog/retrospective-fatigue-how-to-increase-follow-through-on-action-items/); [Atlassian](https://www.atlassian.com/team-playbook/plays/retrospective); justification prompts — [ICSE 2024](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-education-and-training-track/25/An-Empirical-Study-of-the-Content-and-Quality-of-Sprint-Retrospectives-in-Undergradua)
- Agent state files with restricted fields — [Anthropic harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); concise, consistent instructions — [Claude Code memory](https://code.claude.com/docs/en/memory)

### Inferences

#### 1. What to record where (one fact, one home)

| 무엇 | 어디 (유일한 원본) | 누가 · 언제 바꾸나 | 다른 곳에서는 |
| --- | --- | --- | --- |
| 할 일 · 버그 · 결정 필요 항목 | GitHub Issue (요구사항 ID를 제목 앞에) | 누구나 · 생길 때 | 디스코드 · 노션에는 링크만 |
| 지금 누가 무엇을 (진행 상태) | GitHub Project "믿집" Status 필드 (Todo / In progress / Review / Done) | 자동 (닫힘 · 병합 → Done), 시작할 때 본인이 In progress | status.md에 담당자 · 진행 중을 적지 않음 |
| 무엇이 실제로 되는가 (검증 상태) | `docs/status.md` (제안 / 구현 / 검증 + 확인한 것) | 상태를 바꾸는 PR 안에서만 | Project에는 증거를 적지 않음 |
| 되돌리기 어려운 결정 | `docs/adr/NNNN-*.md` | 결정 PR | 회의록에는 "→ ADR 0004" 링크만 |
| 아직 열린 결정 (D1–D16 등) | `docs/design/*.md`의 '열린 결정' + 결정별 `decision` 이슈 1개 | 이슈에서 논의 → 결정 PR이 `Closes #N` | |
| 요구사항 ID 목록 | 요구사항 정의서 스프레드시트 (제출물) | 기획 담당 | 이슈 · status · 화면설계서는 ID로 참조만 |
| 주간 진행 요약 | 택1: Project status update **또는** `docs/reports/YYYY-Www.md` (팀 결정) | 주간 회의 서기 | |
| 회의록 · 회고 | `docs/meetings/` · `docs/retro/` (작성 후 고치지 않음) | 서기 · 주간 회의 | 결정 → ADR · 이슈, 할 일 → 이슈 |
| 대화 · 알림 · 데일리 | Discord (`/github` 웹훅으로 이슈 · PR 알림) | 누구나 | 막힌 것만 이슈 댓글 · `blocked-by` |
| 초안 · 발표 자료 (선택) | Notion | 누구나 | 결론은 GitHub로 옮기고 링크 |

#### 2. GitHub setup (once, about 30 minutes)
- Put the repo under a **free organization**, so issue types (기능 / 버그 / 작업, plus optionally 결정) and issue fields (Priority, Target date) are available.
- **Labels, about 12** (delete unused defaults):
  - area labels mirroring the commit scopes: `area:web`, `area:api`, `area:calc`, `area:agent`, `area:worker`, `area:db`, `area:infra`, `area:docs`
  - `decision`, `retro-action`, `duplicate`
  - `priority:P0`, `priority:P1` only if issue fields are not used
  - no status labels
- **Project "믿집"** (org-level) with three views:
  - 보드: group by Status
  - 이번 주: table, filter `iteration:@current`
  - 요구사항: table grouped by milestone, with a 요구사항 ID text field
- Project fields: Status, Iteration (1 week, add breaks for holidays), and optionally Area.
- Project workflows: keep the two defaults (closed → Done, merged → Done). Use the Free plan's single auto-add workflow with `is:issue,pr is:open`.
- **Milestones = deliverable gates with due dates**, e.g. `중간 점검`, `최종 발표`. Iterations = weeks. If the team wants only one of the two, keep milestones, because they are visible on every issue and show % complete.
- Branch protection on main: 1 approval, squash, CI required once it runs.
- `CODEOWNERS`: `/AGENTS.md`, `/docs/adr/` → the whole team, so rules and decisions get a second reader.
- Discord: create a channel webhook and add it as a GitHub webhook with the `/github` suffix, selecting events issues, pull_request, pull_request_review and check_suite.

#### 3. Issue templates (`.github/ISSUE_TEMPLATE/`)
Use `type:` only if org issue types exist; otherwise drop it and the labels carry the kind.

`1-feature.yml`
```yaml
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
  - type: input
    id: screen
    attributes: { label: 화면 번호 (화면설계서), placeholder: "S-12 (없으면 비움)" }
  - type: textarea
    id: docs
    attributes: { label: 관련 문서 · 결정, placeholder: "docs/design/quote-flow-v3.2.md, ADR 0002, D8" }
```

`2-bug.yml`
```yaml
name: 버그
description: 기대와 다르게 동작함
title: "[버그] "
type: Bug
body:
  - type: textarea
    attributes: { label: 재현 순서, value: "1. \n2. \n3. " }
    validations: { required: true }
  - type: textarea
    attributes: { label: 기대한 것 / 실제 결과 }
    validations: { required: true }
  - type: input
    attributes: { label: 어디서 (브랜치 · 커밋 · 화면 너비 · 브라우저) }
  - type: textarea
    attributes:
      label: 로그 · 화면
      description: 개인정보 · 전화번호 · .env 값은 지우고 붙여 주세요
      render: text
```

`3-task.yml`: 문서 · 인프라 · 정리 작업 (요구사항 ID 없음)
```yaml
name: 작업
description: 문서, 인프라, 테스트, 정리
type: Task
body:
  - type: textarea
    attributes: { label: 할 일, value: "- [ ] " }
    validations: { required: true }
  - type: textarea
    attributes: { label: 완료 조건 }
```

`4-decision.yml`: 열린 결정을 이슈로 관리
```yaml
name: 결정 필요
description: 팀이 골라야 하는 것 (design 문서의 D번호 · R번호 등)
title: "[결정 D00] "
labels: [decision]
body:
  - type: input
    attributes: { label: 결정 번호 · 문서, placeholder: "D8 · docs/design/app-structure.md" }
    validations: { required: true }
  - type: textarea
    attributes: { label: 선택지와 장단점, value: "A) \nB) " }
    validations: { required: true }
  - type: input
    attributes: { label: 언제까지 정해야 하나, placeholder: "YYYY-MM-DD 또는 막고 있는 이슈 #" }
  - type: markdown
    attributes: { value: "정해지면 ADR 또는 design 문서를 고치는 PR에서 `Closes #이 이슈`." }
```

`config.yml`
```yaml
blank_issues_enabled: false
contact_links:
  - name: 질문 · 잡담
    url: https://discord.com/channels/<서버>/<채널>
    about: 할 일이 아니면 디스코드에서 이야기해요
```

#### 4. PR template addition (`.github/pull_request_template.md`)
Keep AGENTS.md §6 as it is and add two lines:
```markdown
## 무엇을 왜
요구사항 ID:            Closes #

## 호출 흐름 (바뀐 경우)

## 검증 결과 (실제로 돌린 것만 [x])
- [ ]

## 기록 갱신
- [ ] status.md 행을 바꿨다 (제안 → 구현 → 검증) / 바꿀 것 없음
- [ ] ADR · design 문서를 바꿨다 / 바꿀 것 없음

## 못 한 것
```

#### 5. Sprint / milestone record
- At **weekly planning (Monday)**: set Iteration = this week on chosen issues, and write a one-line 이번 주 목표 in the Project status update (or in the weekly report).
- At **week end**, the weekly report `docs/reports/2026-W44.md` (if Option B) is written once and never edited:
```markdown
# 2026-W44 (10/26–11/01) 주간 기록
목표: 가견적 요청 → 제출 흐름 (FFV-02~03) 검증까지
상태: 순조 / 위험 / 늦음 — 한 줄 이유

## 끝난 것 (병합된 PR)
- #41 [FFV-02] 가견적 요청 API — 검증 (pytest test_quote_request.py)

## 못 끝낸 것 → 다음 주로
- #45 [FFV-03] 업체 가견적서 화면 — 360px 깨짐 (#47 blocked-by)

## 정한 것
- ADR 0004 업체 가견적 줄 포함 상태 6종 (#44 closed)

## 다음 주 목표
```
(The "끝난 것" list can be generated with `gh pr list --state merged --search "merged:>=2026-10-26"`, and humans add the three judgment lines.)
- At the **milestone (중간 점검, 최종 발표)**: close the milestone, and copy the status.md 기준일 snapshot into the report. The final presentation then uses that report and the traceability table.

#### 6. Meeting notes (`docs/meetings/YYYY-MM-DD-주제.md`, never edited after merge)
```markdown
# 2026-10-27 주간 회의
참석: 
서기: (돌아가며)

## 안건
1. 

## 정한 것 (이유 한 줄)
- … → ADR 0005 / design 문서 갱신 이슈 #

## 할 일 (모두 이슈로)
- [ ] #   담당   기한

## 다음 회의
```
Rule: if it is not in an issue or an ADR, it was not decided.

#### 7. Retrospective (`docs/retro/2026-W44-kpt.md`, weekly or every other week, 30–45 min)
```markdown
# 2026-W44 회고 (KPT)
지난 Try 점검: #52 (지킴 / 못 지킴 — 왜?)

| 이름 | Keep (왜 좋았나) | Problem (왜 문제였나) |
| --- | --- | --- |

## Try (최대 3개, 각각 이슈 · 담당 · 기한)
1. … → #   담당   다음 회고까지
```
- Each Try becomes an issue labelled `retro-action`, checked at the next retro's first step.
- For the **final retro**, use 4Ls (Liked / Learned / Lacked / Longed for) for the 발표 "느낀 점".
- If the team is tired, switch to Start-Stop-Continue.
- Daily scrum: async in a Discord thread (어제 / 오늘 / 막힌 것 / 컨디션 1–10), with no repo file.

#### 8. Docs layout (the existing tree plus three dated folders and an index)
```
AGENTS.md              규칙 (사람 · AI 공통, 200줄 이하 유지)        살아 있는 문서
README.md              실행 방법                                       살아 있는 문서
.github/
  ISSUE_TEMPLATE/      1-feature 2-bug 3-task 4-decision config
  pull_request_template.md
  CODEOWNERS           AGENTS.md, docs/adr/
  workflows/ci.yml     (+ docs 링크 검사: lychee --offline)
docs/
  README.md            "무엇을 어디에" 표 (위 1번 표)                  살아 있는 문서
  status.md            검증 상태 (요구사항 ID 키, 기준일)              살아 있는 문서
  design/              제안 + 열린 결정 (D·R·S·K 번호)                 살아 있는 문서 → 결정되면 ADR
  adr/                 NNNN-*.md (결정, 본문은 고치지 않고 대체)       기록
  architecture/        시스템 구성도 (산출물)                          살아 있는 문서
  screens/             화면설계서 생성기 + PDF (산출물)               살아 있는 문서
  meetings/            YYYY-MM-DD-주제.md                              기록 (고치지 않음)
  retro/               YYYY-Www-kpt.md                                  기록
  reports/             YYYY-Www.md 주간 기록, 마일스톤 요약            기록
  research_notes/      조사 노트                                       기록
```
Each file's first line states its kind: `> 살아 있는 문서 · 기준일 2026-10-29` or `> 기록 · 작성 2026-10-27 · 고치지 않음`.

#### 9. Upkeep rules: candidate text for an AGENTS.md "기록 규칙" section (≤ 12 lines)
1. 한 가지 사실은 한 곳에만 둔다 (위 표). 다른 곳에는 링크만 남긴다.
2. 살아 있는 문서(status, design, architecture, screens, README, AGENTS)는 현실을 바꾸는 그 PR에서 함께 고친다. PR 템플릿 '기록 갱신' 칸을 비우지 않는다.
3. 기록(ADR 본문, meetings, retro, reports, research_notes)은 쓴 뒤 고치지 않는다. 바뀌면 새 기록을 쓰고 옛 것을 링크한다 (ADR은 "대체됨: 0007").
4. status.md: '구현'은 코드가 PR에 있을 때, '검증'은 실제로 돌린 명령과 결과가 PR 본문에 있을 때만 쓴다. 'CI 통과'는 CI가 초록일 때만 쓴다.
5. 이슈는 PR의 `Closes #N`으로만 닫는다 (안 할 일은 'not planned'로 닫고 이유 한 줄).
6. 주간 회의 끝 15분: 지난 Try 확인 → 회고 → status.md 기준일 갱신 → 주간 기록. 매일 적는 문서는 만들지 않는다.
7. AI 도구가 먼저 읽는 순서: AGENTS.md → docs/status.md → 관련 design · ADR → 작업 이슈(`gh issue view N`).
8. AI 도구는 기록을 고치거나 지우지 않는다. 이슈를 닫지 않는다. status.md는 4번 조건을 PR에서 보일 때만 바꾼다. 새 ADR은 '제안'으로만 쓴다.

#### 10. Decisions for the team to make (leave these open and present them together)
- R-a: Weekly progress narrative in **Project status updates** (no PR, harder for agents) or in **`docs/reports/`** (PR, agent-readable, ready for presentation).
- R-b: Meeting notes in **repo `docs/meetings/`** (reviewed, agent-visible, but goes through the PR flow) or in **GitHub Discussions / Notion** (low friction, only decisions and actions copied to GitHub). If repo, should `docs/meetings/**` and `docs/retro/**` be allowed to merge without the usual 1 approval?
- R-c: Iterations **and** milestones, or milestones only.
- R-d: Move the repo under a free org (needed for issue types and fields) or stay personal and use `kind:` labels.
- R-e: Keep a CSV export of the 요구사항 정의서 in the repo for agents (risk of a second copy) or rely on IDs in issues and status.md only.
- R-f: Turn the existing open decisions (D1–D16, R1–R20, S1–S7, K1–K8) into `decision` issues in bulk, or only when someone starts working on one.

### Gaps
- The recommended templates are syntheses of the cited patterns. They have not been tested with the 믿집 team, and their field count may need trimming after the first week.
- The actual bootcamp schedule (number of remaining weeks, required submission format for 회의록 / 회고) is unknown to me. If the course requires 회의록 in a specific format or tool, that overrides R-b.
- Whether SKN34 graders look at GitHub Projects, Notion or submitted files is unknown.

#### All URLs consulted
GitHub Docs and Changelog
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
- https://docs.github.com/ko/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
- https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues
- https://docs.github.com/en/issues/tracking-your-work-with-issues/configuring-issues/managing-issue-types-in-an-organization
- https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies
- https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
- https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels
- https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/sharing-project-updates
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/viewing-insights-from-your-project/about-insights-for-projects
- https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent
- https://github.blog/changelog/2025-01-13-evolving-github-issues-public-preview/
- https://github.blog/changelog/2025-04-09-evolving-github-issues-and-projects/
- https://github.blog/changelog/2025-08-21-dependencies-on-issues/
- https://github.blog/changelog/2026-03-12-issue-fields-structured-issue-metadata-is-in-public-preview/
- https://github.blog/changelog/2026-05-21-issue-fields-are-now-in-public-preview-for-all-organizations/
- https://github.blog/changelog/2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli/
- https://github.blog/changelog/2026-06-18-duplicate-detection-and-issue-fields-mcp-support-for-github-issues
- https://github.blog/changelog/2026-07-02-issue-fields-are-now-generally-available
- https://github.blog/changelog/2026-08-07-connecting-issues-and-multi-select-field-support/
- https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/

Repository template and config files: popular repos (raw, HEAD, read 2026-10-29)
- https://raw.githubusercontent.com/microsoft/vscode/HEAD/.github/ISSUE_TEMPLATE/bug_report.md
- https://raw.githubusercontent.com/microsoft/vscode/HEAD/.github/ISSUE_TEMPLATE/config.yml
- https://raw.githubusercontent.com/vercel/next.js/HEAD/.github/ISSUE_TEMPLATE/1.bug_report.yml
- https://raw.githubusercontent.com/vercel/next.js/HEAD/.github/ISSUE_TEMPLATE/config.yml
- https://raw.githubusercontent.com/fastapi/fastapi/HEAD/.github/ISSUE_TEMPLATE/privileged.yml
- https://raw.githubusercontent.com/fastapi/fastapi/HEAD/.github/ISSUE_TEMPLATE/config.yml
- https://raw.githubusercontent.com/facebook/react/HEAD/.github/ISSUE_TEMPLATE/bug_report.md
- https://raw.githubusercontent.com/pydantic/pydantic/HEAD/.github/ISSUE_TEMPLATE/bug-v2.yml
- https://raw.githubusercontent.com/astral-sh/uv/HEAD/.github/ISSUE_TEMPLATE/1_bug_report.yaml
- https://raw.githubusercontent.com/astral-sh/ruff/HEAD/.github/ISSUE_TEMPLATE/2_rule_request.yaml
- https://raw.githubusercontent.com/sveltejs/svelte/HEAD/.github/ISSUE_TEMPLATE/feature_request.yml
- https://raw.githubusercontent.com/nodejs/node/HEAD/.github/ISSUE_TEMPLATE/4-report-a-flaky-test.yml
- https://raw.githubusercontent.com/kubernetes/kubernetes/HEAD/.github/ISSUE_TEMPLATE/enhancement.yaml
- https://raw.githubusercontent.com/kubernetes/kubernetes/HEAD/.github/ISSUE_TEMPLATE/config.yml
- https://raw.githubusercontent.com/github/docs/HEAD/.github/ISSUE_TEMPLATE/improve-existing-docs.yaml
- https://raw.githubusercontent.com/electron/electron/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml
- https://raw.githubusercontent.com/microsoft/TypeScript/HEAD/.github/ISSUE_TEMPLATE/other.yml
- https://raw.githubusercontent.com/denoland/deno/HEAD/.github/ISSUE_TEMPLATE/feature_request.md
- https://raw.githubusercontent.com/prisma/prisma/HEAD/.github/ISSUE_TEMPLATE/feature_request.yml
- https://raw.githubusercontent.com/shadcn-ui/ui/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml
- https://raw.githubusercontent.com/langchain-ai/langchain/HEAD/.github/ISSUE_TEMPLATE/task.yml
- https://raw.githubusercontent.com/anthropics/claude-code/HEAD/.github/ISSUE_TEMPLATE/documentation.yml
- https://raw.githubusercontent.com/anthropics/claude-code/HEAD/.github/ISSUE_TEMPLATE/model_behavior.yml
- https://raw.githubusercontent.com/home-assistant/core/HEAD/.github/ISSUE_TEMPLATE/task.yml
- https://raw.githubusercontent.com/pallets/flask/HEAD/.github/ISSUE_TEMPLATE/feature-request.md
- https://raw.githubusercontent.com/python/cpython/HEAD/.github/ISSUE_TEMPLATE/bug.yml
- https://raw.githubusercontent.com/rust-lang/rust/HEAD/.github/ISSUE_TEMPLATE/tracking_issue.md
- https://raw.githubusercontent.com/nestjs/nest/HEAD/.github/ISSUE_TEMPLATE/Regression.yml
- https://raw.githubusercontent.com/godotengine/godot/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml
- https://raw.githubusercontent.com/openai/openai-python/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml
- https://raw.githubusercontent.com/vuejs/core/HEAD/.github/ISSUE_TEMPLATE/bug_report.yml
- https://raw.githubusercontent.com/withastro/astro/HEAD/.github/ISSUE_TEMPLATE/---01-bug-report.yml
- https://raw.githubusercontent.com/kubernetes/enhancements/master/keps/NNNN-kep-template/kep.yaml
- https://raw.githubusercontent.com/kubernetes/enhancements/master/keps/NNNN-kep-template/README.md
- https://raw.githubusercontent.com/kubernetes/test-infra/master/label_sync/labels.md

Repository template files and wikis: Korean bootcamp teams
- https://raw.githubusercontent.com/woowacourse-teams/2023-zipgo/HEAD/.github/ISSUE_TEMPLATE/meeting.yml
- https://raw.githubusercontent.com/woowacourse-teams/2023-zipgo/HEAD/.github/ISSUE_TEMPLATE/feature.yml
- https://github.com/woowacourse-teams/2023-zipgo/labels
- https://raw.githubusercontent.com/woowacourse-teams/2023-festa-go/HEAD/.github/ISSUE_TEMPLATE/all-issue-template.md
- https://raw.githubusercontent.com/woowacourse-teams/2024-corea/HEAD/.github/ISSUE_TEMPLATE/be-issue-template.md
- https://raw.githubusercontent.com/woowacourse-teams/2023-hang-log/HEAD/.github/ISSUE_TEMPLATE/feature.yml
- https://raw.githubusercontent.com/woowacourse-teams/2024-staccato/HEAD/.github/ISSUE_TEMPLATE/feat-issue-template.md
- https://github.com/woowacourse-teams/2024-staccato/tree/HEAD/.github
- https://raw.githubusercontent.com/woowacourse-teams/2024-bang-ggood/HEAD/.github/ISSUE_TEMPLATE/%E2%9C%A8-%EA%B8%B0%EB%8A%A5-%ED%85%9C%ED%94%8C%EB%A6%BF.md
- https://raw.githubusercontent.com/woowacourse-teams/2024-mouda/HEAD/.github/ISSUE_TEMPLATE/%EB%AA%A8%EC%9A%B0%EB%8B%A4-%EC%9D%B4%EC%8A%88-%ED%85%9C%ED%94%8C%EB%A6%BF.md
- https://raw.githubusercontent.com/woowacourse-teams/2024-ddangkong/HEAD/.github/ISSUE_TEMPLATE/feature.md
- https://raw.githubusercontent.com/woowacourse-teams/2025-bottari/HEAD/.github/ISSUE_TEMPLATE/bottari-feature-issue-template.yaml
- https://raw.githubusercontent.com/woowacourse-teams/2025-coffee-shout/HEAD/.github/ISSUE_TEMPLATE/feature-template.md
- https://raw.githubusercontent.com/woowacourse-teams/2024-momo/HEAD/.github/ISSUE_TEMPLATE/custom.md
- https://raw.githubusercontent.com/boostcampwm2023/web05-AlgoITNi/HEAD/.github/ISSUE_TEMPLATE/feature_request.md
- https://github.com/boostcampwm2023/web05-AlgoITNi/wiki
- https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/2023%E2%80%9011%E2%80%9008(%EC%88%98)-%EB%8D%B0%EC%9D%BC%EB%A6%AC-%EC%8A%A4%ED%81%AC%EB%9F%BC.md
- https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/1%EC%A3%BC%EC%B0%A8-%ED%9A%8C%EA%B3%A0%EB%A1%9D.md
- https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/1%EC%B0%A8-%EC%A0%95%EA%B8%B0-%ED%9A%8C%EC%9D%98.md
- https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/%EA%B7%B8%EB%9D%BC%EC%9A%B4%EB%93%9C-%EB%A3%B0.md
- https://raw.githubusercontent.com/wiki/boostcampwm2023/web05-AlgoITNi/%EC%BB%A8%EB%B2%A4%EC%85%98.md
- https://github.com/woowacourse-teams/2024-corea/wiki
- https://raw.githubusercontent.com/wiki/woowacourse-teams/2024-corea/%ED%9A%8C%EA%B3%A0%EB%A1%9D.md
- https://raw.githubusercontent.com/wiki/woowacourse-teams/2024-corea/3%EC%B0%A8-%EC%8A%A4%ED%94%84%EB%A6%B0%ED%8A%B8-%ED%95%B5%EC%8B%AC-%EA%B8%B0%EB%8A%A5-%EB%AA%A9%EB%A1%9D.md
- https://github.com/woowacourse-teams/2023-zipgo/wiki
- https://raw.githubusercontent.com/wiki/woowacourse-teams/2023-zipgo/3.-%ED%8C%80-%EA%B7%B8%EB%9D%BC%EC%9A%B4%EB%93%9C-%EB%A3%B0.md
- https://raw.githubusercontent.com/wiki/woowacourse-teams/2023-zipgo/%ED%82%A5%EC%98%A4%ED%94%84-%EB%AF%B8%ED%8C%85(2023%E2%80%9006%E2%80%9028).md
- https://velog.io/@rmsgur/boostcamp-project-week1
- https://29223.tistory.com/134

Docs organisation, decisions, docs-as-code
- https://diataxis.fr/
- https://diataxis.fr/compass/
- https://www.writethedocs.org/guide/docs-as-code/
- https://engineering.squarespace.com/blog/2025/making-documentation-simpler-and-practical-our-docs-as-code-journey
- https://adr.github.io/
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- https://raw.githubusercontent.com/adr/madr/develop/template/adr-template.md
- https://www.industrialempathy.com/posts/design-docs-at-google/
- https://blog.pragmaticengineer.com/rfcs-and-design-docs/
- https://keepachangelog.com/en/1.1.0/
- https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/README.md
- https://strictdoc.readthedocs.io/en/stable/
- https://vale.sh/
- https://raw.githubusercontent.com/lycheeverse/lychee/master/README.md
- https://simonwillison.net/2022/Oct/29/the-perfect-commit/
- https://simonwillison.net/2022/Nov/26/productivity/

Progress, planning, tools
- https://basecamp.com/shapeup/3.4-chapter-13
- https://linear.app/method
- https://linear.app/method/write-issues-not-user-stories
- https://microsoft.github.io/code-with-engineering-playbook/agile-development/ceremonies/
- https://www.notion.com/help/github
- https://docs.discord.com/developers/resources/webhook
- https://handbook.gitlab.com/handbook/company/culture/all-remote/handbook-first/ (fetched; body did not render; not cited)
- https://handbook.gitlab.com/handbook/about/handbook-usage/ (fetched; body did not render; not cited)
- https://tecoble.techcourse.co.kr/ (fetched; no relevant posts visible)

Meetings and retrospectives
- https://scrumguides.org/scrum-guide.html
- https://www.atlassian.com/team-playbook/plays/retrospective
- https://retromat.org/blog/retrospective-fatigue-how-to-increase-follow-through-on-action-items/
- https://retromat.org/blog/what-became-of-our-action-items-check-follow-through-in-retrospectives-with-a-new-phase-2/
- https://www.ebgconsulting.com/blog/the-4ls-a-retrospective-technique/
- https://www.parabol.co/templates/4ls-liked-learned-lacked-longed
- https://www.parabol.co/templates/start-stop-continue
- https://parabol.co/?p=7791
- https://nulab.com/learn/project-management/run-keep-problem-try-retrospective/
- https://miro.com/ko/templates/kpt-japanese/
- https://johannesbrodwall.com/2007/03/05/a-retrospective-training-workshop/
- https://www.oreilly.com/library/view/collaboration-explained-facilitation/0321268776/ch25.html

Studies of student teams
- https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-education-and-training-track/25/An-Empirical-Study-of-the-Content-and-Quality-of-Sprint-Retrospectives-in-Undergradua
- https://arxiv.org/abs/1903.01866
- https://investigadores.anid.cl/en/public_search/work?id=994574
- https://par.nsf.gov/servlets/purl/10555904 (fetched; binary PDF unreadable; not cited)

AI agents and context
- https://agents.md/
- https://code.claude.com/docs/en/memory
- https://learn.chatgpt.com/docs/agent-configuration/agents-md (redirected from https://developers.openai.com/codex/guides/agents-md)
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://docs.cline.bot/prompting/cline-memory-bank
- https://raw.githubusercontent.com/github/spec-kit/main/README.md
- https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/
- https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/

Fetch attempts that failed (not cited)
- https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks (HTTP 403)
