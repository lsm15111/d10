# GitHub branching, merging and code-review workflow for a small student team (믿집, SKN34, Oct 2026)

Research date: 2026-10-29. Scope: branching model, fork vs shared repo, branch naming, GitHub rulesets/branch protection and plan availability, merge methods, code review (human + AI), issue→branch→PR linkage, commit conventions. Labels: **[classic]** = pre-2023 source still cited; **[vendor]** = source sells a related product; **[secondary]** = third-party summary, not primary; **[2026]** = confirmed current as of 2026. The shared WebSearch budget ran out partway through; the rest of the research used direct WebFetch of known primary URLs (no search engines). The full URL list is at the end of section 8.

---

## 1. Branching model: GitHub flow vs trunk-based vs git-flow vs release branches (2026, student team)

### Takeaway
For one web product with a single production version and CI, the sources agree. A single `main` branch plus short-lived (≤1–2 days), single-owner topic branches merged via PR is the right model. This is GitHub flow, or "scaled trunk-based development" when branches stay very short. Git-flow's own author, ThoughtWorks (Hold, 2020), Fowler and Atlassian/AWS all say git-flow is for explicitly versioned or multi-version software, not continuously delivered web apps. Release branches are an optional add-on only if the team must freeze a demo build.

### Cited Findings
**Primary/authoritative positions**
- GitHub flow steps: create a short descriptive branch, commit and push often, open a PR (draft for early feedback), address review, merge after approval, delete the branch. "Make a separate branch for each set of unrelated changes." — [GitHub Docs: GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- Trunk-based development: developers "collaborate on code in a single branch called 'trunk'" and "resist any pressure to create other long-lived development branches." Very small teams may commit directly to trunk. Once a project has "more than a couple of developers", it needs a build server, and short-lived feature branches are used "for code-review and build checking (CI)". — [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/)
- Short-lived feature branches "should only last a couple of days", with "the developer count [staying] at one (or two if pair-programming)". The 2026 page adds that for agentic work the unit is one developer plus that developer's agents. "Time spent waiting for review counts towards the branch's short life." — [TBD: short-lived feature branches](https://trunkbaseddevelopment.com/short-lived-feature-branches/)
- DORA's trunk-based capability: three or fewer active branches, merge to trunk at least daily, no code freezes. Heavy or asynchronous code review is called a pitfall that leads to batching. DORA recommends synchronous review, required automated tests via branch protection, and builds of a few minutes. — [DORA: trunk-based development](https://dora.dev/capabilities/trunk-based-development/)
- Fowler: git-flow was designed for multiple versions in production. Many single-production web apps adopted it and found it "more complicated than necessary", and many teams "claiming git-flow" actually run something like GitHub flow. GitHub flow suits a single production version with a release-ready mainline. He personally prefers CI on high-trust teams and advises: "whenever you're considering using a branch, figure out how you are going to merge." Pre-integration review (PRs) adds latency; Ship/Show/Ask is a middle path. — [Fowler: Patterns for Managing Source Code Branches](https://martinfowler.com/articles/branching-patterns.html)
- **[classic]** Vincent Driessen's 2020 "note of reflection" on git-flow: web apps are "typically continuously delivered, not rolled back", so teams should "adopt a much simpler workflow" like GitHub flow. Git-flow still fits explicitly versioned software. — [nvie.com: A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
- **[classic]** ThoughtWorks Technology Radar put "Long-lived branches with Gitflow" on **Hold** (May 2020): "long-lived branches are the opposite of continuously integrating all changes." — [ThoughtWorks Radar](https://www.thoughtworks.com/radar/techniques/long-lived-branches-with-gitflow)
- Microsoft's 2026 branching guidance is "keep your branch strategy simple": feature branches for everything, PRs into main, and a high-quality up-to-date main with a branch policy (required PR, auto-added reviewers, required build). Release branches like `release/20` are only for coordinating releases. — [Microsoft Learn: Git branching guidance (updated 2026-05)](https://learn.microsoft.com/en-us/azure/devops/repos/git/git-branching-guidance)
- AWS Prescriptive Guidance (Korean edition): the trunk strategy suits "작고 성숙한 개발 팀" with strong communication, not large or distributed teams with big scheduled releases. GitHub flow is also described as suiting small mature teams doing continuous delivery, with frequent merge conflicts as a con. — [AWS 트렁크 전략 장단점](https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/choosing-git-branch-approach/advantages-and-disadvantages-of-the-trunk-strategy.html); [AWS GitHub 플로우 장단점](https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/choosing-git-branch-approach/advantages-and-disadvantages-of-the-git-hub-flow-strategy.html); [AWS 깃플로우 장단점](https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/choosing-git-branch-approach/advantages-and-disadvantages-of-the-gitflow-strategy.html)
- Atlassian (Korean page) defines TBD as frequent small merges into trunk. — [Atlassian KO: trunk-based development](https://www.atlassian.com/ko/continuous-delivery/continuous-integration/trunk-based-development). The Atlassian Gitflow tutorial page returned only navigation when fetched, so its "legacy" wording could not be verified. — [Atlassian Gitflow tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

**Korean companies (what they actually published)**
- **[classic]** 우아한형제들 배민프론트개발팀 Android part (2017-10-30), "우린 Git-flow를 사용하고 있어요": git-flow (master/develop plus feature/release), **fork-based** (upstream = team repo, origin = personal fork). The author merges after peer approval, uses rebase/squash to keep the graph simple, and runs QA on release branches for app-store releases. This is a mobile app with versioned store releases, which is git-flow's intended case. — [우아한형제들 기술블로그](https://techblog.woowahan.com/2553/)
- **[classic]** 뱅크샐러드 (2020-02-29), "하루에 1000번 배포하는 조직 되기": they dropped git-flow, "master branch를 제외한 모든 branch를 제거했습니다", and work on short master-based branches. "하나의 Pull Request는 배포 가능한 단위여야 합니다." The rules were CI (lint + unit tests) required, at least one service-owner approval (≥3 owners per repo), **squash and merge**, revert per PR, and commit-train deploys via GitHub Deployments/Actions and a Slack deploybot. — [뱅크샐러드 기술블로그](https://blog.banksalad.com/tech/become-an-organization-that-deploys-1000-times-a-day/)
- GeekNews linked trunkbaseddevelopment.com and the Banksalad write-up as the readable Korean TBD reference. — [GeekNews TBD](https://news.hada.io/topic?id=1669); [GeekNews weekly #35 "Git-Flow 와 TBD, 하루에 1000번 배포하기"](https://news.hada.io/weekly/202010)
- Korean bootcamp and student posts mostly copy git-flow. One example (2025-08) uses develop/feature/release/hotfix, **fork** the org repo, `feature/{issue-number}-{feature-name}`, PR to develop, and a team lead who alone reviews and merges. — [velog daram_dev: Git 공통 규칙 정리](https://velog.io/@daram_dev/Git-공통-규칙-정리). A goorm bootcamp TIL uses feature→dev→main with prefixes feat/fix/hotfix/chore/docs/refactor and no rebase. — [velog maruru301](https://velog.io/@maruru301/goormTIL-Git-협업-48). Other velog posts compare Git-Flow, GitHub-Flow and GitLab-Flow. — [velog kw2577](https://velog.io/@kw2577/Git-branch-전략); [velog calm0_0](https://velog.io/@calm0_0/GIT-브랜치-전략); [wikidocs 277135](https://wikidocs.net/277135)

**Popular OSS projects (for calibration)**
- Kubernetes: PRs need `/lgtm` (reviewer) and `/approve` (OWNERS approver). The Tide bot batches and merges, authors squash near the end on request, and AI-assisted work "must be disclosed". — [Kubernetes contributor guide: pull requests](https://www.kubernetes.dev/docs/guide/pull-requests/)
- Next.js: works from a `canary` branch, every PR needs maintainer review, trivial PRs are likely closed, and protected branches require **verified signed commits**. — [Next.js contributing.md](https://github.com/vercel/next.js/blob/canary/contributing.md)
- release-please (Google): "We **highly** recommend that you use squash-merges", citing linear history, bisect and accurate release notes. — [googleapis/release-please](https://github.com/googleapis/release-please)

### Inferences
- 믿집 is one web product (Next.js + FastAPI) with one production or demo deployment, so git-flow's develop/release/hotfix branches add cost with no matching benefit. GitHub flow on `main` with the existing "merge within 2 days" rule effectively *is* scaled trunk-based development, and it matches TBD's "couple of days" and DORA's daily-merge guidance.
- There is a concrete git-flow trap for this team: GitHub closing keywords (`Closes #12`) only work when the PR targets the **default branch** (see §6). Under git-flow, PRs into `develop` never auto-close issues unless `develop` is made the default branch. That is one more reason to use `main` only.
- An optional `release/<demo-name>` (or a tag) is justified only if the team must freeze a build for a bootcamp presentation while work continues. Microsoft's guidance says fix on main and cherry-pick to the release branch.
- The Korean company examples split along the same line as the global sources. Woowahan's git-flow case was a versioned mobile app (2017). Banksalad's web/backend services moved to master-only plus squash (2020).

### Gaps
- No primary 2024–2026 posts from 토스, 카카오, or 당근 on branch strategy were found. Search returned only generic articles, and the Kakao tech blog URLs fetched (`tech.kakao.com/posts/498`, the 2022 newkrew onboarding post) returned no body text. Claims about what Toss, Kakao or Daangn "use" cannot be sourced from this research.
- No quantitative study of student or bootcamp teams comparing branching models was found.

---

## 2. Fork vs shared-repo branches, branch naming, GitHub "Create a branch" for an issue, Korean in branch names

### Takeaway
A small private team should use the **shared repository model**: everyone has Write and pushes topic branches to one repo. GitHub says it "is more common with small teams and organizations collaborating on private projects". Forks are for untrusted outside contributors, and they break several automations (secrets, auto-delete, Actions tokens). For naming, keep the issue number first and the description in **ASCII lowercase kebab-case**, not Korean. If AI agents create branches, consider an agent prefix (`claude/`, `codex/`, `copilot/`).

### Cited Findings
- GitHub: the fork-and-pull model is "popular with open-source projects because it reduces friction for new contributors". The shared repository model is "more common with small teams and organizations collaborating on private projects". — [GitHub Docs: collaborative development models](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models)
- Fork side effects: for a PR from a fork, "Automatically delete head branches" uses the *fork's* setting, and deletion needs write access to the fork. — [GitHub Docs: automatic deletion of branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches). Validating PR titles with `pull_request` "fails for fork PRs because the GitHub token isn't available", so `pull_request_target` is needed. — [amannn/action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request). On public repos GitHub withholds secrets from fork-PR runs, so the Claude review workflow "runs only on pull requests from branches in the same repository". — [Claude Code GitHub Actions docs](https://code.claude.com/docs/en/github-actions). Stacked PRs: "Cross-fork stacks are not supported." — [GitHub Docs: about stacked PRs](https://docs.github.com/en/pull-requests/get-started/about-stacked-prs)
- Rulesets apply to "pushes to a repository and its fork network". For forks, "only people with bypass permission in the root repository can bypass push rules". — [GitHub Docs: about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- "Create a branch" from an issue: anyone with write permission can do it from the issue's **Development** sidebar. By default it creates the branch "in the current repository, and from the default branch". "When you create a pull request for one of these branches, it is automatically linked to the issue." The feature "is currently in public preview and subject to change." — [GitHub Docs: creating a branch for an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-a-branch-for-an-issue)
- **[classic]** GitHub's 2022 announcement says the branch name "is suggested for you based on the title of the issue" and can be edited. — [GitHub blog 2022-03-21: Start working on GitHub Issues faster](https://github.blog/2022-03-21-start-working-on-github-issues-faster). A third-party app offers configurable formats such as `issue-15-Fix_nasty_bug`. — [robvanderleek/create-issue-branch](https://github.com/robvanderleek/create-issue-branch). GitLab's equivalent feature uses an "issue ID + hyphenated title" pattern. — [GitLab issue 21143](https://gitlab.com/gitlab-org/gitlab-ce/issues/21143)
- Git itself allows non-ASCII bytes in ref names. The only character-level bans are ASCII control chars, space, `~ ^ : ? * [ \`, `..`, `@{`, a leading `-` for branches, and a trailing `.`/`.lock`. — [git-check-ref-format](https://git-scm.com/docs/git-check-ref-format)
- Hangul normalization risk: macOS stores filenames in NFD while Windows and Linux use NFC, and Git compares raw bytes, so visually identical Hangul names can differ. — [daleseo.com: 유니코드와 UTF-8](https://daleseo.com/unicode/); [juejin: git NFD vs NFC](https://juejin.cn/post/7666446436604198939); [gist: Pusnow NFD](https://gist.github.com/Pusnow/aa865fa21f9557fa58d691a8b79f8a6d). These sources discuss **filenames**, not ref names (see Gaps).
- Conventional Branch 1.1.0: `<type>/<description>` with `feature/` (or `feat/`), `bugfix/` (or `fix/`), `hotfix/`, `release/`, `chore/`. v1.1.0 adds **AI-agent prefixes** `ai/`, `claude/`, `codex/`, `copilot/`, `cursor/`. Names use lowercase a–z, 0–9 and hyphens only (the grammar excludes non-ASCII), and ticket numbers are encouraged, e.g. `feature/issue-123-new-login`. — [conventionalbranch.org](https://conventionalbranch.org/)
- Microsoft's suggested names: `users/username/description`, `users/username/workitem`, `bugfix/description`, `feature/feature-name`, `feature/feature-area/feature-name`, `hotfix/description`. — [Microsoft Learn: Git branching guidance](https://learn.microsoft.com/en-us/azure/devops/repos/git/git-branching-guidance)
- **[classic]** Woowahan named branches by feature, not by person ("누구나 알아보기 쉽다"), as summarised by a velog post. — [velog kw2577](https://velog.io/@kw2577/Git-branch-전략)
- Korean student examples: `feature/{issue-number}-{feature-name}` (e.g. `feature/2-userinfo-api`), though that post's own examples drift to `feat/9-userLogin-api`. — [velog daram_dev](https://velog.io/@daram_dev/Git-공통-규칙-정리). Another uses `[Feat]/#13_1`, which mixes brackets, `#` and uppercase. — [velog rmaomina](https://velog.io/@rmaomina/pre-project-github-features-convensions)
- Rulesets can restrict branch names ("Restrict branch names" / commit metadata, testable in "Evaluate" mode), and patterns use fnmatch (`qa/**/*` for nested). — [GitHub Docs: creating rulesets for a repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)

### Inferences
- GovBiz's "fork-based branches" problem goes away with the shared-repo model: one remote, branches visible to everyone, auto-delete working, and Actions secrets available for CI and AI-review workflows.
- The draft rule `이슈번호-짧은-설명` is sound and matches GitHub's issue-to-branch flow. One clarification is needed: "짧은 설명" should be ASCII kebab-case (`12-quote-form-validation`), not Korean (`12-견적-폼-검증`). This follows from Conventional Branch's grammar, the NFC/NFD risk on mixed macOS/Windows teams, URL-encoding in links, and shell quoting. Since GitHub suggests names from the issue title, a Korean title will likely produce a Korean slug that must be edited by hand. This is inferred from "suggested based on title" and was not tested.
- Type prefixes (`feat/`) in branch names duplicate the PR title's Conventional Commit type, and after a squash merge the branch name is discarded. Requiring them adds little. The one prefix worth allowing is the agent prefix (`claude/12-…`, `codex/12-…`, `copilot/…`), because these tools often name branches themselves and it makes AI-authored work visible in the branch list.
- Enforcement options: (a) a ruleset "Restrict branch names" pattern if the plan supports it (unverified, see Gaps), or (b) a tiny CI job that checks `github.head_ref` against a regex like `^((claude|codex|copilot)/)?[0-9]+-[a-z0-9]+(-[a-z0-9]+)*$`.

### Gaps
- GitHub Docs do not state the exact default name format of "Create a branch" (whether it is `{number}-{slug}`) or how it slugifies Hangul titles. Verify in the UI.
- No source confirmed that Hangul **branch names** (as opposed to filenames) break between macOS and Windows clients. `core.precomposeunicode` covers working-tree filenames; behaviour for refs is unverified.
- Which plans allow ruleset "Restrict branch names / commit metadata" was not stated on the fetched page. Older docs tied metadata restrictions to Enterprise, but that is unverified for 2026.

---

## 3. Rulesets / branch protection in 2026: required checks, approvals, stale-approval dismissal, conversation resolution, linear history, merge queue, CODEOWNERS, auto-delete — Free vs Pro vs Team

### Takeaway
**Plan availability decides everything.** On **GitHub Free (personal or org), rulesets and protected branches only work on public repositories.** Private repos need Pro (personal account) or Team (org, $4/user/month) for rulesets, protected branches, required reviewers, CODEOWNERS and draft PRs. Merge queue is free only for **public repos owned by an organization**; private repos need Enterprise Cloud. If GovBiz was a private repo in a Free org, that alone would explain why "0 approvals" and "CI not required remotely" were possible (inference, see §8). For 믿집, the public/private decision should be made together with the plan decision.

### Cited Findings
**Plan availability (verify again before acting; GitHub changes these)**
- "Rulesets are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, and GitHub Enterprise Cloud." Push rulesets are available on Team for private/internal repos. (Wording taken from the docs page via search snippet.) — [GitHub Docs: about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets). The fetched page also says organization-level rulesets are "For organizations on the GitHub Enterprise plan". That conflicts with the creating-rulesets page, which says "For customers on GitHub Team and GitHub Enterprise plans you can also create rulesets for repositories in an organization." — [GitHub Docs: creating rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- GitHub's plans page: Free gives "unlimited private repositories with a limited feature set". Under "Advanced tools and insights in private repositories", **Pro and Team** list Protected branches, Code owners, Required pull request reviewers, Multiple pull request reviewers and Wikis. Team adds Team pull request reviewers. — [GitHub Docs: GitHub's plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)
- Pricing page (Oct 2026): Free $0; **Team $4/user/month**; Enterprise $21/user/month. On Free, Code owners and **Draft pull requests are public-repos-only**, and Required reviewers and Multiple reviewers are listed as Team features. Actions minutes: Free 2,000/month, Team 3,000/month; free for public repos. — [GitHub Pricing](https://github.com/pricing)
- Actions billing (2026) is expressed in dollars: Free $12, Pro $18, Team $18 included compute per month for private repos. Linux 2-core is $0.006/min (≈2,000 / 3,000 min). Artifact storage is 500 MB / 1 GB / 2 GB. "Standard GitHub-hosted runners in public repositories" are free, and self-hosted runners are free. — [GitHub Docs: Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- **Merge queue**: "Merge queue is available on private and public repos on the GitHub Enterprise Cloud plan" plus all public repos owned by organizations (GA 2023-07-12). — [GitHub changelog: merge queue GA](https://github.blog/changelog/2023-07-12-pull-request-merge-queue-is-now-generally-available/). Current docs say the same; personal-account repos are excluded. — [GitHub Docs: merging with a merge queue](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue); [Graphite guide](https://graphite.dev/guides/github-merge-queue); [Zenn korosuke613 (JP)](https://zenn.dev/korosuke613/scraps/d7b3e3c5db452f). **[classic]** limited beta: [2021 changelog](https://github.blog/changelog/2021-10-27-pull-request-merge-queue-limited-beta/)
- A merge queue needs CI triggered on `merge_group`: "You must use the merge_group event to trigger your GitHub Actions workflow when a pull request is added to a merge queue". Otherwise required checks never report and the merge fails. Third-party CI must watch `gh-readonly-queue/{base_branch}` branches. — [GitHub Docs: managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- **[vendor]** Mergify's free plan has "Zero cost for open source projects and private teams of up to 5", including Merge Queue (active user = opened or pushed to a PR in the last 30 days). — [Mergify pricing](https://mergify.com/pricing)
- Bypass lists and push restrictions: "Actors may only be added to bypass lists when the repository belongs to an organization." Push restrictions work "in all repositories owned by an organization using GitHub Team or GitHub Enterprise Cloud", and in public repos of Free orgs. — [GitHub Docs: about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- Personal-account repos: "Repositories owned by personal accounts have a single owner who has full control". On private repos the owner "can only grant write access to collaborators". For granular roles, GitHub suggests using an organization. — [GitHub Docs: personal account repo permissions](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-personal-account-settings/permission-levels-for-a-personal-account-repository)
- Education: "Free GitHub Pro while you are a student" is part of the Student Developer Pack. — [GitHub Student Developer Pack](https://education.github.com/pack). Eligibility requires enrolment "in a degree- or diploma-granting program, such as a high school, college, university, or homeschool", plus proof documents, age 13+, and a verified academic email if the school issues one. Bootcamps are not mentioned. — [GitHub Docs: apply to GitHub Education as a student](https://docs.github.com/en/education/about-github-education/github-education-for-students/apply-to-github-education-as-a-student). "Verified academic faculty can apply for GitHub Team for teaching or academic research", and qualifying nonprofits get free Team. — [GitHub Docs: discounted plans](https://docs.github.com/en/billing/concepts/discounted-plans). The education landing page lists "GitHub Copilot Student and Codespaces" for students. — [github.com/education](https://github.com/education). University guides describe the faculty-approved route to an org on Team. — [UCL guide](https://www.ucl.ac.uk/advanced-research-computing/expertise/research-software-development/research-software-development-tools/support-ucl-researchers); [Brown gitbook](https://gitbook.brown.edu/cis-cloud-services/github)

**Rules and what they do (rulesets)**
- Branch ruleset rules: restrict creations/updates/deletions (deletions on by default); require linear history; require deployments; require signed commits; **require a pull request** with sub-options:
  - required approvals (0–10);
  - dismiss stale approvals;
  - require review from code owners;
  - require approval of most recent reviewable push;
  - require conversation resolution;
  - allowed merge methods;
  - "Additional approval for unattributed Copilot pull requests" (public preview, on by default);
  - path-based Required reviewers (teams; "not available on user-owned repositories").

  Also: **require status checks** (strict = branch must be up to date; loose = not), **block force pushes** (on by default), require code scanning results. — [GitHub Docs: available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- Rulesets vs classic protection: multiple rulesets can layer (the most restrictive wins), they can be toggled without deleting, and "Anyone with read access can view a repository's active rulesets". Enforcement can be Active, Disabled, or "Evaluate" (for testing metadata rules). — [about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets); [creating rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- Bypass can be "Always allow" or "For pull requests only" (the bypasser must still open a PR). Actors can be admins, maintain/write roles, teams, GitHub Apps or Dependabot. Rulesets can be imported from JSON, and GitHub publishes ready-made JSON in `github/ruleset-recipes`. — [creating rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository); [github/ruleset-recipes](https://github.com/github/ruleset-recipes) (includes "Require pull requests and conventional commits" and "Branch protection best practices")
- **[2026]** The Rule insights dashboard became GA on Aug 25, 2026. It shows how rulesets are evaluated and enforced at repo and org level. — [GitHub changelog, Aug 2026](https://github.blog/changelog/month/08-2026/)
- Stale approvals: approvals are dismissed when "the reviewed diff changes, such as after new pushes or a related merge into the target branch". Most-recent-push approval is an alternative that is "less protective". A "request changes" review blocks merging until it is resolved or dismissed. Required checks must report success, skipped or neutral. — [about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- Signed-commit rule: unsigned commits on a PR branch can block even squash merges until they are rewritten and signed. — [about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- **Required checks in a monorepo**: if a *workflow* is skipped by path, branch or commit-message filtering, its checks "stay in a 'Pending' state and block merging". A *job* skipped by a conditional "reports 'Success'". — [GitHub Docs: troubleshooting required status checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks). `dorny/paths-filter@v4` provides per-filter outputs (`backend`, `frontend`) so jobs can use `if:` conditions inside one always-running workflow, because GitHub's built-in path filters "don't work on a level of individual jobs or steps". — [dorny/paths-filter](https://github.com/dorny/paths-filter)
- CODEOWNERS can live in `.github/`, the repo root or `docs/`, with the first found used. "The last matching pattern takes the most precedence." Owners need explicit write access. Approval from **any one** listed owner satisfies "Require review from Code Owners". Give the CODEOWNERS file itself an owner, and keep the file under 3 MB. — [GitHub Docs: about code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- Auto-delete head branches: an admin enables it under Settings → General → Pull Requests. Protection rules can prevent deletion. — [GitHub Docs: automatic deletion of branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches)
- Auto-merge appears only on PRs that can't merge yet because required reviews or checks are pending. It is disabled if someone without write access pushes or changes the base. — [GitHub Docs: automatically merging a PR](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request)
- Roles: **Write** can approve required reviews, merge, enable auto-merge, act as code owner, and manage labels/milestones. **Maintain** adds pushing to protected branches and PR merge settings. Only **Admin** manages rulesets and branch protection and "merge[s] PRs on protected branches without approving reviews". — [GitHub Docs: repository roles for an organization](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization)
- Secret push protection: "push protection for users" is on by default and blocks pushing secrets to **public** repos. Repo-level push protection "Requires GitHub Secret Protection to be enabled". — [GitHub Docs: about push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- **[secondary, 2026]** A news summary says GitHub Code Quality became GA on July 20, 2026. On Aug 7, 2026, enabling Code Quality stopped auto-adding Copilot as a reviewer through its generated ruleset; to keep automatic reviews, a ruleset must be edited or added (Team/Enterprise Cloud). — [vpsranking summary](https://vpsranking.com/news/ai/ai-2026-08-07-github-code-quality-copilot-review/) (the primary changelog entry was not opened)

### Inferences
- **Choosing a plan.** "Enforced" below means rules are enforced on the remote.
  - **(A) Public repo in a Free organization:** rulesets, required approvals, required checks, CODEOWNERS, draft PRs, bypass lists, merge queue, free Actions and default secret push protection. Cost $0, but code and docs are public.
  - **(B) Private repo in a Free organization:** none of the protections are enforced. This repeats GovBiz's failure mode, and Actions is capped at about 2,000 Linux min/month.
  - **(C) Private repo in a Team organization:** everything except merge queue. Cost $4 × 6 = $24/month.
  - **(D) Private repo in one student's personal account with Pro** (free via Student Pack *if* SKN34 qualifies): rulesets and required reviews are enforced. However, all collaborators are Write, there are no bypass lists, no team-based reviewers and no merge queue, and one person owns the repo.

  Option A or C is preferable; option B should be ruled out explicitly.
- **CI minutes on a private repo (Free, rough estimate).** Assume 5 people × ~1 PR/day × ~3 pushes × (backend ruff+pytest with Postgres/Redis ≈ 5 min + frontend drift/typecheck/lint/build ≈ 4 min). That is ≈ 135 min/day, or ≈ 3,000 min/month over 22 working days, which exceeds the Free $12 (~2,000 min) allowance. A public repo has no cap. On private, use `concurrency: cancel-in-progress`, path-based job skipping and dependency caching. These numbers are assumptions, not measurements.
- **Required-check design for this monorepo.** Do not use workflow-level `paths:` filters on required workflows, because they leave checks Pending forever. Instead, run one always-triggered workflow with `dorny/paths-filter` and conditional jobs. Ideally add a final aggregator job that `needs:` all jobs, uses `if: always()`, and fails when any needed job failed, then mark **only that one check** as required. That way renaming jobs doesn't silently drop a required check. The aggregator pattern is common practice; no fetched GitHub doc states it.
- **Strict ("up to date") checks.** This repo has an OpenAPI type-drift check, which can pass on two branches separately and fail after both merge (semantic conflict). That argues for strict ON. The cost is "Update branch" churn. If churn hurts and the repo is a public org repo, enable merge queue (add `merge_group:` to the workflow triggers). For 4–6 people, a merge queue is optional rather than required.
- **Stale approvals and the most-recent-push rule.** Enable both "Dismiss stale approvals" and "Require approval of most recent reviewable push". AI agents and fix-up pushes are exactly the case where a post-approval change slips in. Combined with strict checks, a base-update merge *may* dismiss approval when the diff changes, which needs monitoring.
- Do **not** require signed commits for students: setup friction is high, and rebase-merge can't be signed by GitHub. Next.js does require them, but it is a large OSS project.

### Gaps
- Whether auto-merge and "Require conversation resolution" are available on Free private repos was not stated in the fetched pages.
- Whether a ruleset's "Automatically request Copilot code review" works in a Free org whose members hold individual Copilot Student licenses is unclear. The docs describe personal automatic review on Pro/Pro+/Max and ruleset-based review in repos.
- Whether SKN34 (a bootcamp, likely not degree/diploma-granting) qualifies students for the Student Developer Pack (GitHub Pro) or instructors for GitHub Team via education is unconfirmed. Apply, or ask GitHub Education support.
- The exact plan availability of ruleset metadata restrictions (commit message or branch name patterns) and "Require code scanning results" on private Team repos was not confirmed.

---

## 4. Merge methods: squash vs merge commit vs rebase — history, Conventional Commits, changelogs, git bisect; how squash messages are generated

### Takeaway
**Squash merge as the only allowed method, with the squash message defaulting to the PR title**, is the right fit. It gives one Conventional-Commit-formatted commit per PR on `main`, so contributors' WIP commits don't matter. It also gives linear history, per-PR revert, and a release-please/changelog-compatible log. Its downsides (lost intra-PR granularity and blame detail, pain for long-lived or stacked branches) are minor when PRs are small and branches live under 2 days.

### Cited Findings
- The three methods:
  - **Merge commit** keeps all commits plus a merge commit.
  - **Squash** combines everything into one commit, so original commit timing, authorship and SHAs are lost.
  - **Rebase-merge** replays commits individually; GitHub "Always updates the committer information and creates new commit SHAs" and cannot sign them.

  Squash caveat: continuing to work on a head branch after a squash-merge causes previously squashed commits to reappear and "conflicts that you have to repeatedly resolve". — [GitHub Docs: about merge methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github)
- Default squash message options: "Default message" / "Pull request title" / "Pull request title and commit details" / "Pull request title and description". The legacy "Default message" uses "the commit title and message if the pull request contains only 1 commit" and "the pull request title and list of commits if the pull request contains 2 or more commits". — [GitHub Docs: configuring commit squashing](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests)
- **[classic]** Since Dec 2019, GitHub will "automatically credit every commit author in the pull request as a co-author on the squash commit". — [GitHub changelog 2019-12-19](https://github.blog/changelog/2019-12-19-improved-attribution-when-squashing-commits/). GitLab does not do this (open issue). — [GitLab work item 593408](https://gitlab.com/gitlab-org/gitlab/-/work_items/593408)
- "Require linear history" blocks merge commits and needs squash or rebase merging enabled. — [about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- Conventional Commits FAQ: "Do all my contributors need to use the Conventional Commits specification? No! If you use a squash based workflow on Git lead maintainers can clean up the commit messages as they're merged." — [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- release-please "**highly** recommend[s]" squash merges (linear history, bisect, accurate release notes, no failing intermediate commits on main). Multiple changes in one squash commit can be expressed with footers, and monorepos use a manifest config. — [googleapis/release-please](https://github.com/googleapis/release-please)
- With squash merging, the PR title becomes the commit message on main. Enable "Default to PR title for squash merge commits" and validate titles. — [amannn/action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request)
- Bisect: `git bisect --first-parent` follows only first parents, so a merged branch with broken intermediate commits doesn't produce false positives. — [git-bisect docs](https://git-scm.com/docs/git-bisect). **[classic]** SciPy maintainers say squash makes bisect easier because each commit passed tests; others counter with `--first-parent`. — [SciPy-Dev 2021-08 thread](https://www.python.org/pipermail/scipy-dev/2021-August/024991.html) (also [024992](https://www.python.org/pipermail/scipy-dev/2021-August/024992.html), [024994](https://www.python.org/pipermail/scipy-dev/2021-August/024994.html), [024995](https://www.python.org/pipermail/scipy-dev/2021-August/024995.html))
- **[classic]** Downsides raised in a Julia discussion (2021): squash loses per-commit messages for `git blame`, and big PRs become one big diff. Counterpoints: split logically separate changes into separate PRs, and treat the PR discussion as the rationale record. GitHub rebase-merge "loses the connection to the original PR". — [Julia Discourse: downsides of squash merging](https://discourse.julialang.org/t/downsides-of-using-squash-merging/68317)
- Atomic Object (2024-01-11): make squash the **default** on small teams with process control, because the default matters most. Keep merge-commit available for multi-logical-change PRs. Squash helps newer developers. — [Atomic Object: To Squash or Not to Squash](https://spin.atomicobject.com/squash-merge/). Opposite view: merges preserve WIP and the merge point, and are better for bisect if every commit builds. — [Ghostty Developer FAQ mirror](https://git.uoc.run.place/Applied-Software/ghostty/wiki/Developer-FAQ); [dev.to igorsantos07](https://dev.to/igorsantos07/my-preferred-merge-strategy-for-pull-requests-1lo5)
- Kubernetes: don't squash during review (add fix-up commits so reviewers see deltas). Squash near LGTM, keep independent layered changes as separate commits, and the `tide/merge-method-squash` label lets the bot squash. — [Kubernetes PR guide](https://www.kubernetes.dev/docs/guide/pull-requests/)
- Stacked PRs: squash hides lineage, so dependent branches keep the old commits and need rebasing. — [Echobind](https://echobind.com/post/stacked-pull-requests-with-squash-merge); [Matt Rickard](https://blog.matt-rickard.com/p/stacked-pull-requests); [GitKraken](https://www.gitkraken.com/?p=9226). **[2026]** GitHub's native stacked PRs (public preview; the docs' campaign tag says "public-preview-2026") use `gh stack`, merge bottom-up, rebase the remaining layers automatically, support merge/squash/rebase, are merge-queue aware, and don't support cross-fork stacks. — [GitHub Docs: about stacked PRs](https://docs.github.com/en/pull-requests/get-started/about-stacked-prs)
- **[classic]** Banksalad uses squash and merge so it can revert per PR. — [뱅크샐러드](https://blog.banksalad.com/tech/become-an-organization-that-deploys-1000-times-a-day/). Woowahan used rebase and squash to keep the graph simple. — [우아한형제들](https://techblog.woowahan.com/2553/)

### Inferences
- With squash-only, the quality of `main`'s history depends entirely on **PR titles**, not on individual commits. So the existing title convention `type(범위): 한국어 요약` should be enforced on the **PR title** (a CI check), and the team can relax enforcement on in-branch commits. That avoids husky friction for Windows users and AI agents.
- Recommended repo setting: allow **squash only**, with the default commit message set to **"Pull request title and description"**, plus a PR template whose description is short and ends with `Closes #N`. The closing keyword then lands in the squash commit body too, and works from commit messages on the default branch. Alternatively choose "Pull request title" only if descriptions get long or noisy. The trade-off: "title and description" keeps the rationale in `git log`, while "title" keeps logs terse.
- Branches deleted on merge plus a 2-day merge window remove most of squash's documented pain (re-squashed commits, repeated conflicts). If people need to build on unmerged work, use GitHub's native stacked PRs or wait for the base to merge, rather than branching off a branch.
- `git bisect` stays reliable because each `main` commit corresponds to a PR that passed required checks.

### Gaps
- GitHub appends `(#PR-number)` to squash commit titles. This is widely observed but was not stated in the fetched docs page, so verify on first merge.
- It was not verified whether `Co-authored-by:` trailers inside individual commit messages (e.g. from Claude Code) survive in the squash commit under each default-message option. The 2019 changelog covers commit *authors*, not trailers in messages.

---

## 5. Code review for students: SLA, reviewer count, checklists, Conventional Comments, Pn rule, pairing, reviewing AI-generated code, avoiding rubber stamps, AI reviewers

### Takeaway
For 4–6 students, the evidence supports:
- 1 required human approval, rotated across the team;
- a review response SLA of the same working day (≤24h, with Google's 1 business day as the outer bound);
- small PRs;
- an explicit comment-severity vocabulary (Banksalad's **Pn rule** in Korean, or Conventional Comments);
- a PR template that forces "what/why/how tested/AI used";
- an AI reviewer as an *extra*, non-approving pass, never a substitute for the human approval.

AI-authored code measurably needs more scrutiny, and AI reviewers help but also add noise and latency.

### Cited Findings
**Speed and size**
- "One business day is the maximum time it should take to respond to a code review request". Individual responses matter more than total time, and "LGTM with comments" is fine for optional or minor points. — [Google eng-practices: speed of code reviews](https://google.github.io/eng-practices/review/reviewer/speed.html)
- "favor approving a CL once it is in a state where it definitely improves the overall code health of the system", because "there is no such thing as 'perfect' code". Prefix optional points with "Nit:". — [Google eng-practices: the standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- "100 lines is usually a reasonable size for a CL, and 1000 lines is usually too large". Separate refactors from features, and include tests in the same CL. — [Google eng-practices: small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- **[classic]** Google stats as summarised in Korean (2021): reviews average ~4h, 75% of reviews have one reviewer, and 90% touch fewer than 10 files. At Microsoft, 75% of ~60k developers review daily. — [삼성SDS 인사이트 리포트 2021-03-12](https://www.samsungsds.com/kr/insights/global_code_review.html). The primary paper abstract (9M reviewed changes, 12 interviews, 44 survey respondents) — [Sadowski et al., Modern Code Review: A Case Study at Google](https://research.google/pubs/modern-code-review-a-case-study-at-google/)
- **[classic, vendor]** SmartBear/Cisco: review 200–400 LOC at a time; defect-finding drops beyond 400 LOC; under ~500 LOC/hour. — [SmartBear best practices](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/); [tekin.co.uk](https://tekin.co.uk/2020/05/proof-your-thousand-line-pull-requests-create-more-bugs); [Mike Conley](https://mikeconley.ca/blog/tag/loc/). The sibling note `pr_unit_size.md` covers size in depth.

**Reviewer count, rotation, purpose**
- Microsoft: "Two reviewers is an optimal number [based on research]". Avoid assigning the same reviewers to many PRs, and distribute review responsibility across the team. — [Microsoft Learn: Git branching guidance](https://learn.microsoft.com/en-us/azure/devops/repos/git/git-branching-guidance). The cited paper's abstract does **not** state "two is optimal"; it reports converging review parameters and that review increases the files a developer knows by 66–150%. — [Rigby & Bird 2013, Convergent contemporary software peer review practices](https://www.microsoft.com/en-us/research/publication/convergent-software-peer-review-practices/). The "two reviewers" claim therefore rests on Microsoft's reading of the paper.
- **[classic]** Bacchelli & Bird (ICSE 2013): "while finding defects remains the main motivation for review, reviews are less about defects than expected". They provide "knowledge transfer, increased team awareness" and alternative solutions, and "code and change understanding is the key aspect". — [Microsoft Research](https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/)
- AB180 (요즘IT, 2022-05-24): moving from 1 to 2 reviewers hurt productivity, so they distributed reviews deliberately. They set a 4h SLA (at latest next morning), stated estimated review time in requests, and "버그는 테스트로 막는다". — [요즘IT: 생산성 있는 Review 문화가 되기까지](https://yozm.wishket.com/magazine/detail/1497/). Related Korean articles: [요즘IT 1903](https://yozm.wishket.com/magazine/detail/1903); [요즘IT 2420](https://yozm.wishket.com/magazine/detail/2420/); [GeekNews 6886](https://news.hada.io/topic?id=6886)
- DORA: asynchronous review that leaves the author waiting is a pitfall; prefer synchronous review (ask a reviewer right away). — [DORA TBD](https://dora.dev/capabilities/trunk-based-development/)
- Ship/Show/Ask (Rouan Wilsenach, 2021-09-08): "Ship" = merge without review, "Show" = PR then merge immediately, "Ask" = wait for review. Mandatory approval policies "signal low trust". Junior engineers should Show and Ask more. Regulated contexts still need review. — [martinfowler.com: Ship/Show/Ask](https://martinfowler.com/articles/ship-show-ask.html)

**Comment vocabularies**
- Conventional Comments: `<label> [decorations]: <subject>`, with labels praise / nitpick / suggestion / issue / todo / question / thought / chore / note and decorations (non-blocking) / (blocking) / (if-minor). — [conventionalcomments.org](https://conventionalcomments.org/)
- **[classic]** 뱅크샐러드 **Pn 룰** (2020-11-24):
  - **P1** "꼭 반영해주세요" (Request changes)
  - **P2** "적극적으로 고려해주세요" (Request changes)
  - **P3** "웬만하면 반영해 주세요" (Comment; explain or file a follow-up ticket)
  - **P4** "반영해도 좋고 넘어가도 좋습니다" (Approve)
  - **P5** "그냥 사소한 의견입니다" (Approve)

  Review deadlines use a **D-n** tag (D-0 only for incidents; D-2 is most common). The author must give full context (spec, design links, test list, GIFs). PRs were capped at 1,000 lines early on, later typically 200–300 lines reviewed in 1–2 days. — [뱅크샐러드: 코드 리뷰 문화](https://blog.banksalad.com/tech/banksalad-code-review-culture/)
- Student/bootcamp norms: "코드리뷰는 지적이 아니라 협업"; LGTM / conditional approval; enforce style with Prettier and ESLint rather than in review. — [velog maruru301](https://velog.io/@maruru301/goormTIL-Git-협업-48). A team-lead-only review model. — [velog daram_dev](https://velog.io/@daram_dev/Git-공통-규칙-정리). Fixed review days and merge days in one notion-based team. — [notion BE team page](https://terrific-beryl-003.notion.site/BE-1-1740ff5456af80179841fe1e3ce27f46)

**Reviewing AI-generated code**
- GitHub's tutorial for AI code review:
  1. Run tests and static analysis first.
  2. Check fit with purpose and architecture ("Does this code solve the right problem?").
  3. Assess quality.
  4. Scrutinise dependencies ("Watch out for hallucinated or suspicious packages").
  5. Look for AI pitfalls ("Watch for tests that are deleted or skipped, instead of fixed").
  6. Have teammates review complex or sensitive changes.
  7. Automate routine checks.
  8. Document expectations in CONTRIBUTING.md.

  — [GitHub Docs: review AI-generated code](https://docs.github.com/en/copilot/tutorials/review-ai-generated-code)
- **[vendor]** CodeRabbit (2025-12-17) analysed 470 OSS PRs (320 AI-co-authored, 150 human). AI PRs had 10.83 vs 6.45 issues per PR (≈1.7×), logic/correctness ≈1.75×, security up to 2.74×, readability >3×. Authorship labelling is uncertain ("cannot guarantee"). — [CodeRabbit report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report); coverage: [The Register](https://www.theregister.com/2025/12/17/ai_code_bugs/), [Business Wire](https://www.businesswire.com/news/home/20251217666881/en/CodeRabbits-State-of-AI-vs-Human-Code-Generation-Report), [IT Brief](https://itbrief.co.uk/story/study-finds-ai-generated-code-far-buggier-than-human-work), [dev.to](https://dev.to/coderabbitai/our-new-report-ai-code-creates-17x-more-problems-7lh)
- **[vendor]** AI-assisted changes often exceed 400 lines at the 75th percentile vs 157 lines unassisted, and large diffs degrade review. — [CodeRabbit guide](https://www.coderabbit.ai/guides/code-review-best-practices-for-ai-generated-code). Other guides: ask the agent for its reasoning, assumptions and omissions first, review lockfiles and dependencies before the implementation, and scrutinise tests as closely as production code. — [Aviator 2026 guide](https://www.aviator.co/blog/?p=5968). "AI is notorious for writing tests that 'pass' by mocking the very thing they are supposed to verify." — [Rollbar](https://rollbar.com/blog/ai-pull-requests)
- METR RCT (2025-07-10): 16 experienced OSS developers on 246 tasks were **19% slower** with AI (Cursor + Claude 3.5/3.7) while believing they were ~20% faster. METR's Feb 2026 update says the original results "no longer reflect current impact". — [METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/); [eWeek](https://eweek.com/news/news-ai-tools-slow-developer-productivity-study)
- DORA 2025: "AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses". — [DORA 2025 report](https://dora.dev/research/2025/dora-report/)
- Disclosure norms: Kubernetes requires AI-assisted work to be disclosed and fully explainable. — [Kubernetes PR guide](https://www.kubernetes.dev/docs/guide/pull-requests/). Ghostty: "All AI usage in any form must be disclosed"; name the tool and the extent, and the human must understand every change. — [Ghostty AI_POLICY.md](https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md). The Linux kernel uses an `Assisted-by: LLM [TOOL…]` tag, AI must never add `Signed-off-by`, and the human takes full responsibility. — [kernel.org: AI coding assistants](https://docs.kernel.org/process/coding-assistants.html)

**AI reviewers (Copilot, Codex, Claude, CodeRabbit)**
- Copilot code review: "By default, Copilot's reviews do not count toward required approvals". If Copilot approvals are enabled, it "can submit an approving review that satisfies your repository's required-approval rule". It reviews any language, and Copilot "is not guaranteed to spot all problems". It excludes dependency manifests and lockfiles, logs and SVGs. It reads `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md` and the root `AGENTS.md` from the **head branch**. It is billed in AI credits, with an estimated per-review cost of Lite ≈$0.25, Balanced ≈$1.50 (default), Max ≈$10. Copilot Free doesn't include it. — [GitHub Docs: Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review)
- Copilot plans (Oct 2026): **Student — free for verified students, code review included**. Pro $10/month, Pro+ $39, Max $100, Business $19/seat, Enterprise $39/seat. Free has only "Review selection" in VS Code. — [GitHub Docs: Copilot plans](https://docs.github.com/en/copilot/get-started/plans). **[secondary]** Copilot moved to usage-based AI-credit billing on June 1, 2026. — [userjot](https://userjot.com/blog/github-copilot-pricing-guide-2025); [fast.io](https://fast.io/resources/github-copilot-free-access/); [toolsforhumans](https://www.toolsforhumans.ai/ai-tools/github-copilot); [docs.github.com/fr plans](https://docs.github.com/fr/copilot/get-started/plans)
- Automatic Copilot review: as a personal setting (Pro/Pro+/Max) or via a ruleset rule "Automatically request Copilot code review", with options "Review new pushes" and "Review draft pull requests". — [GitHub Docs: configure automatic review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/configure-automatic-review). **[2026]** Since Aug 27, 2026, it also covers bot-authored PRs (including Copilot cloud-agent PRs) and very large PRs. — [GitHub changelog Aug 2026](https://github.blog/changelog/month/08-2026/)
- Copilot-authored PRs: the requester's "approval of a Copilot pull request won't count" toward required approvals. Workflows don't run until a human clicks **Approve and run workflows**. — [GitHub Docs: review Copilot PRs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/review-copilot-prs); [reviewing a PR created by Copilot](https://docs.github.com/en/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot). A Microsoft Learn module phrases it as the requester "cannot approve", which is imprecise. — [MS Learn module](https://learn.microsoft.com/en-us/training/modules/github-copilot-code-agent/3-assign-track-troubleshoot-copilot-code-agent-tasks). Since 2026-03-13, admins can optionally skip workflow approval, with the caveat that workflows may expose tokens or secrets. — [GitHub changelog 2026-03-13](https://github.blog/changelog/2026-03-13-optionally-skip-approval-for-copilot-coding-agent-actions-workflows/)
- Codex review on GitHub: `@codex review` (optionally with a focus) or Automatic review. Custom rules go in a `## Code Review Rules` section of the nearest `AGENTS.md`. "In GitHub, Codex flags only P0 and P1 issues so review comments stay focused on high-priority risks." — [Codex GitHub integration docs](https://learn.chatgpt.com/docs/third-party/github)
- Claude: the `anthropics/claude-code-action@v1` review workflow uses the `code-review` plugin with `--comment` to post inline comments. It skips drafts and trivial PRs, needs `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`, and consumes Actions minutes plus API tokens. Commits pushed with the default `GITHUB_TOKEN` don't trigger CI. — [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
- Empirical evidence on LLM reviewers:
  - Beko (ICSE 2025 SEIP) used a Qodo PR-Agent-based tool on 4,335 PRs, 1,568 of which were auto-reviewed. 73.8% of comments were resolved, but average PR closure time **rose from 5h52m to 8h20m**. Practitioners reported faulty or irrelevant comments and a "minor" quality improvement. — [arXiv 2412.18531](https://arxiv.org/abs/2412.18531); [ICSE SEIP listing](https://conf.researchr.org/details/icse-2025/icse-2025-software-engineering-in-practice/8/Automated-Code-Review-In-Practice); [Bilkent thesis](https://repository.bilkent.edu.tr/items/8e7ac28e-5120-4c6e-84e3-e7d288c336f0)
  - Atlassian (ASE 2025 industry) studied 4,000 LLM and human comments. Resolution rates were readability 43.3%, bugs 41.9%, maintainability 36.2%, design 28.6%, and the strengths were complementary. — [alphaxiv 2510.05450 overview](https://www.alphaxiv.org/overview/2510.05450v1); [ASE 2025 listing](https://conf.researchr.org/details/ase-2025/ase-2025-industry-showcase/58/What-Types-of-Code-Review-Comments-Do-Developers-Most-Frequently-Resolve-)

### Inferences
- **Approval count.** With 4–6 people, require **1 human approval** and rotate the reviewer per PR (e.g. a round-robin list in CONTRIBUTING or CODEOWNERS by area). Two required approvals would stall a student team (as AB180 found). Use CODEOWNERS only for high-risk paths (`backend/alembic/**`, `.github/**`, `infra/**`, prompt/eval assets) so one specific owner must look.
- **SLA.** "First response the same working day, review done ≤24h, merge ≤2 days after opening." Adopt Banksalad's D-n tag in the PR title or label (D-0 for blocking incidents, D-1 default). This matches the 2-day merge rule.
- **Severity vocabulary.** Use the **Pn rule** (Korean, intuitive, maps onto GitHub's Request changes / Comment / Approve), and keep Conventional Comments' `praise:` for positive notes. Don't mix Pn with issue *priority* labels; use Issue Fields "Priority" for issues (§6).
- **Anti-rubber-stamp measures that are cheap for students:**
  - a PR template with required sections "왜 / 무엇을 / 어떻게 테스트했는지 / 스크린샷 / AI 사용 여부와 범위";
  - "Require conversation resolution";
  - "Dismiss stale approvals";
  - reviewers must run or check one thing (open the Vercel/preview URL, or read the test diff);
  - for agent-authored PRs, the reviewer reads tests and any changed lockfiles first (GitHub/Aviator/Rollbar guidance);
  - pair or mob review (synchronous, DORA) for schema migrations, auth and payment-like flows.

  The template item is synthesis; each piece is sourced above.
- **AI PR accounting.** When Claude Code or Codex creates a PR under a student's account, that student is the author and cannot count as the approver. Another student must approve (GitHub authors cannot approve their own PRs, as per GitHub's review model). Require AI disclosure in the PR body and a `Co-authored-by`/`Assisted-by` trailer (§7). Add an `ai-assisted` label if useful.
- **AI reviewer stance.** Turn on **one** AI reviewer as a free or cheap first pass. Copilot code review via the Copilot Student plan is likely the cheapest for students; otherwise Codex `@codex review` or the Claude action. Keep "Copilot approvals count" **off**, and treat AI comments as at most Pn P3–P5 unless a human upgrades them. The evidence (73.8% resolved but slower PR closure; category-dependent usefulness) supports "useful extra pass, never the gate".

### Gaps
- No controlled study specific to student teams on review SLA or reviewer count was found.
- Copilot Student's monthly AI-credit allowance (and so how many automatic reviews are free) wasn't stated on the plans page fetched.
- Banksalad's Pn rule article dates from 2020. Whether Banksalad still uses it in 2026 is unknown.

---

## 6. Issue tracking: templates/forms, labels, Projects, milestones, sprints, sub-issues, issue types (2025–26), closing keywords, docs/status.md vs Projects

### Takeaway
GitHub-native planning matured a lot in 2025–26. Sub-issues, org-level **issue types**, org-level **issue fields** (GA 2026-07-02, including Free orgs), "Relates to" links (GA 2026-09-25), better label management (GA 2026-08-27), Projects iteration fields and built-in automations together cover a student team's needs without Jira or Notion. Several of these (types, fields) require the repo to live in an **organization**. Pick one source of truth for status (the Project), and make `docs/status.md` either generated or link-only.

### Cited Findings
- Issue forms: YAML files in `.github/ISSUE_TEMPLATE/` with required `name`, `description`, `body` and optional `title`, `labels`, `assignees`, `projects` (`OWNER/NUMBER`) and **`type`** ("The issue type that will be automatically added to issues created with this template"). Element types are markdown, input, textarea, dropdown, checkboxes and upload, with `validations.required`. Status: "Issue forms are currently in public preview and subject to change." — [GitHub Docs: syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- `config.yml`: `blank_issues_enabled: false` (Write+ users still see "Maintainers only" blank issues) and `contact_links`. Templates are ordered alphabetically, so prefix them `01-…`. — [GitHub Docs: configuring issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- Issue types are org-level: "The default types are task, bug, and feature". "You can create up to 25 issue types". — [GitHub Docs: managing issue types](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization). REST API support arrived in March 2025, and the "Private repositories only" option was retired then. — [GitHub changelog 2025-03-18](https://github.blog/changelog/2025-03-18-github-issues-projects-rest-api-support-for-issue-types); [changelog 2025-03-06](https://github.blog/changelog/2025-03-06-github-issues-projects-api-support-for-issues-advanced-search-and-more/)
- **[2026]** Issue fields GA (2026-07-02) "for all GitHub organizations on Free, Team, Enterprise". The default fields are **Priority, Effort, Start date, Target date**, and custom single-selects are allowed. Admins choose which fields show per issue type. Field names support non-English characters, and fields are accessible through GitHub's MCP server. — [GitHub changelog: issue fields GA](https://github.blog/changelog/2026-07-02-issue-fields-are-now-generally-available)
- **[2026]** "Relates to" issue relationship and private saved views GA (2026-09-25). — [GitHub changelog Sep 2026](https://github.blog/changelog/month/09-2026/). Better label management (suggested labels, label archiving) GA (2026-08-27). — [GitHub changelog Aug 2026](https://github.blog/changelog/month/08-2026/). GitHub Agentic Workflows GA (2026-10-28) for reasoning tasks like issue triage and CI-failure analysis. — [GitHub changelog Oct 2026](https://github.blog/changelog/month/10-2026/)
- Sub-issues: "up to 100 sub-issues" per parent, "up to eight levels" of nesting, cross-repo, shown in Projects (group or filter by parent), and `gh issue create --parent`. — [GitHub Docs: adding sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)
- Default labels: bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix. — [GitHub Docs: managing labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- Milestones track issues and PRs within one repo, with a description, due date and % complete. — [GitHub Docs: about milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)
- Iteration fields give sprints of any length in days or weeks, with breaks, `@current`/`@next` filters, bulk-moving unfinished items, and a roadmap view. — [GitHub Docs: iteration fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields)
- Built-in Projects workflows: **Item closed → Done** and **PR merged → Done** are on by default. Optional workflows: item added → Todo, auto-add from a repo by filter, auto-archive. — [GitHub Docs: built-in automations](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations). Maximum **auto-add workflows: Free 1, Pro 5, Team 5, Enterprise 20**; filters `is:`, `label:`, `reason:`, `assignee:`, `no:`. — [GitHub Docs: adding items automatically](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically); [community discussion 137767](https://github.com/orgs/community/discussions/137767); [cpython PR 136831 (scope unclear)](https://github.com/python/cpython/pull/136831)
- Projects best practices: break work into sub-issues so PRs are smaller, use README/status updates, multiple views, custom and iteration fields, and "To prevent information from getting out of sync, maintain a single source of truth." — [GitHub Docs: best practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
- Closing keywords: close/closes/closed/fix/fixes/fixed/resolve/resolves/resolved, which are "interpreted only when the pull request targets the repository's default branch". They also work in commit messages merged to the default branch. Cross-repo form: `Fixes owner/repo#100`. Manual linking via the Development sidebar allows up to 10 issues per PR. — [GitHub Docs: linking a PR to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
- Korean student practice: an issue = one task, milestones for "Bare Minimum" vs "Advanced", a Projects kanban with WIP limits and daily kanban meetings, `[FE|BE] 제목` issue titles, labels FE/BE/기능추가/리팩토링/에러, and short PR bodies (≤300 chars). — [velog rmaomina](https://velog.io/@rmaomina/pre-project-github-features-convensions)

### Inferences
- **Labels (minimal taxonomy, mirrors commit scopes):** `area:web`, `area:api`, `area:calc`, `area:agent`, `area:worker`, `area:db`, `area:infra`, `area:docs`. Add a few process labels: `blocked`, `needs-decision`, `ai-assisted`, and optionally `D-0`/`D-1`/`D-2` review-deadline labels.
  - **Kind** goes in **issue types** (Task/Bug/Feature + custom `Prompt`, `Eval`) when the repo is in an org; otherwise use `type:*` labels.
  - **Priority** goes in **Issue fields → Priority**, not `P1` labels, to avoid clashing with Pn review comments.
  - **Status** should never be a label; use the Project's Status field.
- **Sprints vs milestones:** use a Projects **iteration** field for 1-week sprints, and **milestones** for bootcamp checkpoints (e.g. 중간발표, 최종발표, 배포 데모) because milestones have due dates and % complete. Use sub-issues to split epics such as "견적 플로우" into PR-sized issues.
- **Flow:** issue (form) → "Create a branch" from the issue (rename to ASCII `12-…`) → draft PR auto-linked → `Closes #12` in the PR body → squash-merge to main closes the issue → Project item moves to Done. This only works with PRs targeting `main`, which is another argument against `develop`.
- **docs/status.md vs Projects:** GitHub's guidance is to keep one source of truth. Note the current rule in `mitjip/AGENTS.md` §7: "진행 현황은 `docs/status.md` 하나에만 적는다". That leaves two consistent options, and **the team must pick one**:
  - (a) keep `docs/status.md` as the only status record and use Projects just as a board of issue/PR links, with no separate status prose;
  - (b) amend the rule so the Project's Status field is the source of truth and `docs/status.md` holds narrative, decisions and links to saved views (or a generated weekly snapshot).

  Either way, don't hand-maintain the same checklist in both places. With a Free org, only one auto-add workflow is available, so point it at `is:issue,pr is:open` for the monorepo.

### Gaps
- Whether issue forms remain "public preview" in late 2026 or have quietly gone GA isn't clear. The docs still say public preview.
- Whether issue types and issue fields can be used on repos owned by a **personal account** (option D in §3) is not stated. The docs only describe org-level management.

---

## 7. Commit message conventions: Conventional Commits with Korean summaries, commitlint/husky/lefthook, PR-title linting, co-author trailers for AI tools

### Takeaway
`type(scope): 한국어 요약` is compatible with Conventional Commits. The spec only fixes `feat`/`fix` semantics, allows extra types, and says nothing against non-English descriptions, and a Korean translation exists. Since squash-merge makes the PR title the commit, the most robust enforcement is a **required CI check on the PR title** with the team's custom types and scopes. Local hooks (husky or lefthook + commitlint) should be optional conveniences. AI attribution should use a consistent trailer, and Claude Code's is configurable.

### Cited Findings
- Spec: `<type>[optional scope]: <description>`, with an optional body and footers, `!` or `BREAKING CHANGE:` for majors, `fix`→PATCH, `feat`→MINOR. Other types are allowed with no SemVer effect. Elements are case-insensitive except BREAKING CHANGE. — [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Korean translation: "<타입>[적용 범위(선택 사항)]: <설명>". — [Conventional Commits 한국어](https://www.conventionalcommits.org/ko/v1.0.0/)
- `@commitlint/config-conventional`:
  - `type-enum` = build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test;
  - `type-case` lower;
  - `subject-case` never sentence/start/pascal/upper;
  - `subject-full-stop` never `.`;
  - `header-max-length` 100;
  - body and footer lines ≤100 (URLs exempt).

  — [commitlint config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/@commitlint/config-conventional); [commitlint.js.org](https://commitlint.js.org/)
- commitlint in CI: `fetch-depth: 0`, then `npx commitlint --from ${{ github.event.pull_request.base.sha }} --to ${{ github.event.pull_request.head.sha }}` on PRs and `--last` on push. — [commitlint CI setup](https://commitlint.js.org/guides/ci-setup.html)
- PR-title lint: `amannn/action-semantic-pull-request@v6` validates titles against Conventional Commits, with options `types`, `scopes`, `requireScope`, `disallowScopes`, `subjectPattern` and `ignoreLabels`. Use the `pull_request_target` trigger with `opened`/`edited`/`reopened` and add `synchronize` if it's a required check. Pair it with squash and "Default to PR title". — [amannn/action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request)
- Husky: ~2 kB, no dependencies, uses Git `core.hooksPath`, supports Windows, nested projects and monorepos, and installs via npm `prepare`. — [husky](https://typicode.github.io/husky/). Lefthook (Evil Martians): `lefthook.yml` plus `lefthook install`, `parallel: true`, per-job `glob`, `stage_fixed`, and installs via npm, Homebrew, winget, scoop or apt. A "With commitlint" example exists. — [lefthook.dev](https://lefthook.dev/)
- **[classic]** Chris Beams' 7 rules (2014): blank line after subject, subject ~50 chars (72 max), capitalise, no trailing period, imperative mood, wrap body at 72, explain *what/why* not *how*. — [cbea.ms: How to Write a Git Commit Message](https://cbea.ms/git-commit/)
- Korean team example: `type: 제목` + body + `closed #N` footer, types feat/fix/build/chore/ci/docs/style/refactor/test/perf, subject ≤50 chars, no period. — [velog daram_dev](https://velog.io/@daram_dev/Git-공통-규칙-정리). A bootcamp backend team used `#이슈번호` in commits and `[태그] 한 일(#이슈번호)` PR titles. — [notion BE team page](https://terrific-beryl-003.notion.site/BE-1-1740ff5456af80179841fe1e3ce27f46)
- Co-author trailers: `Co-authored-by: NAME <email>`, one per line after a blank line. The email must be linked to the co-author's GitHub account for it to count as their contribution. — [GitHub Docs: commits with multiple authors](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors)
- Claude Code `attribution` setting: `attribution.commit` ("Change or hide the trailer Claude Code adds to commits"), `attribution.pr` ("…attribution line in pull request descriptions"), `attribution.sessionUrl`. `includeCoAuthoredBy` is "Deprecated; use `attribution`". — [Claude Code settings reference](https://code.claude.com/docs/en/settings-reference). Team-shared settings go in a committed `.claude/settings.json`. — [Claude Code settings](https://code.claude.com/docs/en/settings). **[secondary]** Key names and a reported bug: [claudelog](https://claudelog.com/faqs/attribution-setting-claude-code/); [deployhq](https://www.deployhq.com/blog/how-to-use-git-with-claude-code-understanding-the-co-authored-by-attribution); [anthropics/claude-code#14241](https://github.com/anthropics/claude-code/issues/14241); [#22585](https://github.com/anthropics/claude-code/issues/22585); [zenn dk_](https://zenn.dev/dk_/articles/8e4726b71f7803?locale=en)
- Linux kernel AI tag: `Assisted-by: LLM [TOOL1] [TOOL2]`, never AI `Signed-off-by`. — [kernel.org coding assistants](https://docs.kernel.org/process/coding-assistants.html)
- AGENTS.md is an open format (Linux Foundation's Agentic AI Foundation) read by Codex, Copilot coding agent, Cursor, Jules, Gemini CLI and others. Suggested sections include build/test commands and "Commit message and pull request guidelines". In monorepos, "The closest AGENTS.md to the edited file wins." — [agents.md](https://agents.md/). Copilot code review also reads the root `AGENTS.md`. — [Copilot code review docs](https://docs.github.com/en/copilot/concepts/agents/code-review)

### Inferences
- **The team's custom types break config-conventional's `type-enum`** (`prompt`, `eval` are not in it), so any commitlint config must override `type-enum` (and `scope-enum` for web/api/calc/agent/worker/db/infra/docs). The same lists go into `action-semantic-pull-request`'s `types` and `scopes` with `requireScope: true` if scopes are mandatory. Consider adding `ci`/`build`/`perf`/`style`/`revert` or mapping them to `chore` deliberately.
- Korean subjects pass `subject-case` because Hangul has no letter case. `header-max-length: 100` counts characters (Hangul syllables are 1 each). In practice a ≤50-character Korean summary is a good norm. Neither was tested.
- **Enforcement split:**
  - (1) **Required**: PR-title check in CI. It's the only thing that reaches `main` under squash.
  - (2) **Optional**: lefthook or husky `commit-msg` with commitlint for those who want it. Lefthook is a single binary and handles the `frontend/` + `backend/` monorepo with `root`/`glob`. Husky expects the Node project at the repo root or needs a subfolder config.
  - Don't block PRs on individual commit messages; AI agents and GitHub's web UI produce varied ones.
- **AI attribution policy:** keep Claude Code's default `Co-Authored-By:` trailer (or set `attribution.commit` to a team-standard string) in a committed `.claude/settings.json`. Configure Codex and other tools to add an equivalent trailer, and require the PR body's "AI 사용" section. If the trailer email isn't linked to a GitHub account, GitHub won't show it as a contributor, but the record stays in git history.
- Put the commit/PR conventions in **AGENTS.md (root)** with path-specific AGENTS.md in `frontend/` and `backend/`. Copilot review, Codex review ("Code Review Rules" section) and Claude all read these, so humans and agents follow one rulebook.

### Gaps
- Whether `Co-authored-by` trailers in branch commits survive a squash merge depends on the default-message option and wasn't verified (see §4).
- Codex's default commit attribution behaviour (whether it adds a trailer) wasn't found in the fetched docs.

---

## 8. Recommended workflow and settings checklist for 믿집 (synthesis of §1–7)

### Takeaway
Use **GitHub flow on `main` in a shared repo inside a GitHub organization**:
- ASCII branch names `<issue#>-<desc>` (agents may use `claude/`, `codex/`, `copilot/`);
- **squash-only** merges with **PR title as the Conventional Commit** (`type(범위): 한국어 요약`), enforced by a required title check;
- a **ruleset on `main`** requiring a PR, **1 approval**, stale-approval dismissal, most-recent-push approval, conversation resolution, linear history, and **one required aggregated CI check** (strict/up-to-date);
- CODEOWNERS on risky paths, and auto-delete branches;
- Projects (iterations = sprints) plus milestones (presentations), issue forms, `area:*` labels, and `Closes #N` linking.

The repo must be **public (Free org)** or **private on GitHub Team ($4/user/month)**. A private repo on a Free org enforces none of this.

### Cited Findings
(All supporting citations are in §1–7. The mappings below each cite the deciding source.)
- GovBiz's failures map to these settings:
  - fork-based branches → shared repo model ([GitHub Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models));
  - 0 required approvals → ruleset "Required approvals: 1" ([available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets));
  - CI not required remotely → ruleset "Require status checks to pass" ([available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)), which only works on private repos with Pro/Team/Enterprise ([about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets); [GitHub's plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)).
- Prebuilt ruleset JSON to start from: "Branch protection best practices" and "Require pull requests and conventional commits". — [github/ruleset-recipes](https://github.com/github/ruleset-recipes)

### Inferences
**Decision first (owner: team, with the bootcamp):**
- **D-a. Public repo in a Free org.** Pros: every protection is enforced, merge queue is available, Actions are free, push protection for secrets is on by default, and the repo doubles as a portfolio. Cons: code, docs, prompts and eval data are public, so check bootcamp rules and data licences (e.g. any 조달청/건축HUB data stored in the repo, `.env` hygiene).
- **D-b. Private repo in an org on GitHub Team (~$24/month for 6).** Pros: everything is enforced except merge queue. Cons: it costs money, and Actions is capped at ~3,000 min.
- **D-c. Private repo on a personal Pro account (Student Pack, if eligible).** This is a fallback only: one owner, all collaborators Write, no bypass lists, no team reviewers, no merge queue.
- **Reject:** a private repo in a Free org. It reproduces GovBiz.

**Repository settings (Settings → General)**
- [ ] Default branch `main`; no `develop`.
- [ ] Merge button: **Allow squash merging only**. Squash default message = **"Pull request title and description"** (or "Pull request title").
- [ ] Merge commits OFF, rebase merging OFF.
- [ ] "Always suggest updating pull request branches" ON, "Allow auto-merge" ON, **"Automatically delete head branches" ON**.
- [ ] Members get **Write**; one or two members get **Admin** (ruleset owners); nobody uses Admin to bypass day-to-day.

**Ruleset `main-protection` (Settings → Rules → Rulesets, target: default branch, Active)**
- [ ] Restrict deletions ON; Block force pushes ON.
- [ ] Require linear history ON.
- [ ] Require a pull request before merging:
  - [ ] Required approvals **1**
  - [ ] Dismiss stale approvals ON
  - [ ] Require approval of the most recent reviewable push ON
  - [ ] Require review from Code Owners ON (CODEOWNERS limited to risky paths)
  - [ ] Require conversation resolution ON
  - [ ] Allowed merge methods: **squash**
  - [ ] Keep "Additional approval for unattributed Copilot PRs" ON (default).
- [ ] Require status checks to pass: **strict / up-to-date ON**. Required checks: `ci-ok` (aggregator) + `pr-title`.
- [ ] Bypass list: Admins as **"For pull requests only"** (org repos only); no "Always" bypass.
- [ ] Optional, public org repo only: **Require merge queue** if "Update branch" churn becomes painful. Add `merge_group:` to the CI triggers first.
- [ ] Don't require signed commits or deployments for now.

**CI (GitHub Actions)**
- [ ] One `ci.yml` on `pull_request` (+ `push: main`, + `merge_group` if using a queue). Use `dorny/paths-filter@v4` to set `backend`/`frontend` outputs and conditional jobs: backend = ruff + pytest with Postgres/Redis services; frontend = OpenAPI drift + typecheck + lint + build.
- [ ] Final `ci-ok` job with `needs: [all jobs]`, `if: always()`, which fails if any needed job failed or was cancelled. Mark **only `ci-ok`** as required, and don't use workflow-level `paths:` filters on required workflows.
- [ ] `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }` plus dependency caching, which matters on a private repo's minute budget.
- [ ] `pr-title.yml`: `amannn/action-semantic-pull-request@v6` on `pull_request_target` (opened, edited, reopened, synchronize) with `types: feat fix docs test chore refactor prompt eval`, `scopes: web api calc agent worker db infra docs`, `requireScope: true` (if mandated).
- [ ] Optional: a branch-name check job with a regex like `^((claude|codex|copilot)/)?[0-9]+-[a-z0-9]+(-[a-z0-9]+)*$`.

**Branch and PR conventions (CONTRIBUTING.md + AGENTS.md)**
- [ ] Branch: `<이슈번호>-<ascii-kebab-설명>` (e.g. `12-quote-form-validation`); agents: `claude/12-…`, `codex/12-…`, `copilot/…`. No Korean in branch names. One owner per branch (plus their agents). Merge within 2 days or split the work.
- [ ] Start from the issue's **Development → Create a branch** (edit the suggested name to ASCII), or `git switch -c 12-… origin/main`.
- [ ] Open a **draft PR** early. The PR title follows `type(범위): 한국어 요약`, and the body uses the template.
  - Template sections: 왜 (context/issue), 무엇을 (changes), 어떻게 테스트했는지 (commands, screenshots, preview URL), 리뷰 포인트, AI 사용 여부/도구/범위, `Closes #12`.
- [ ] Size norm: ≈≤400 changed lines excluding lockfiles and generated OpenAPI types. Refactors go in separate PRs (see `pr_unit_size.md`).

**Review rules**
- [ ] 1 approval from a rotating reviewer, plus code owners for `backend/alembic/**`, `.github/**`, `infra/**` and prompt/eval assets.
- [ ] SLA: first response the same working day, review ≤24h. Use a D-n label or tag in the request (D-0 = blocker).
- [ ] Comments use the **Pn rule**: P1/P2 → Request changes, P3 → Comment, P4/P5 → Approve. `praise:` is encouraged.
- [ ] The reviewer must actually exercise the change (run it, open the preview, or read the tests first). For AI-authored PRs, check deleted or skipped tests, mocks hiding behaviour, new dependencies and lockfiles, and invented APIs.
- [ ] Synchronous pair review for DB migrations, auth and quote/price-calculation logic.
- [ ] One AI reviewer (Copilot code review via Copilot Student, *or* `@codex review`, *or* the Claude review action) as an extra pass. Its approval never counts, and its comments default to P3–P5.

**Commits and attribution**
- [ ] Squash commit = PR title, so in-branch commits are free-form. Optional local lefthook `commit-msg` + commitlint with custom `type-enum`/`scope-enum`.
- [ ] AI trailer policy: keep `Co-Authored-By:` from Claude Code (team `.claude/settings.json` `attribution`), or standardise on `Assisted-by: <tool>`. The PR body also has an AI disclosure section.

**Issues and Projects**
- [ ] Put the repo in an org so you get issue types (Task/Bug/Feature + Prompt/Eval) and issue fields (Priority/Effort/Start/Target).
- [ ] Issue forms: `01-feature.yml`, `02-bug.yml`, `03-task.yml`, `04-prompt-eval.yml`, with `blank_issues_enabled: false`.
- [ ] Labels: `area:{web,api,calc,agent,worker,db,infra,docs}`, `blocked`, `needs-decision`, `ai-assisted`. No status labels and no P-labels on issues.
- [ ] Project: Status (Todo/In progress/In review/Done), an **Iteration** field (1-week sprints), and views (Board by Status, Table by assignee, Roadmap by Target date). Built-in workflows: closed → Done and merged → Done (default), plus one auto-add workflow (Free = 1).
- [ ] Milestones = presentation and demo checkpoints; sub-issues for epics.
- [ ] Status source of truth: either keep the current AGENTS.md rule (`docs/status.md` only) or amend it so the Project Status field is authoritative and `docs/status.md` links to it. This is a team decision (see §6). Never duplicate task status by hand.

### Gaps
- Whether the bootcamp allows a public repo (data, licences, evaluation integrity) is a team decision outside this research.
- Plan facts were verified on 2026-10-29 pages. GitHub changes plan features often, so re-check [GitHub's plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) and [pricing](https://github.com/pricing) before buying Team.
- The strict-checks + stale-dismissal combination may cause re-approval churn. This was not measured and should be watched in the first two weeks.

### Source list (all URLs consulted)

**Fetched directly (read in full or in part via WebFetch)**
1. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
2. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
3. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
4. https://docs.github.com/en/get-started/learning-about-github/githubs-plans
5. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
6. https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue
7. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests
8. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
9. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches
10. https://docs.github.com/en/billing/concepts/discounted-plans
11. https://education.github.com/benefits (redirected) → https://github.com/education
12. https://docs.github.com/en/copilot/concepts/agents/code-review
13. https://docs.github.com/en/copilot/get-started/plans
14. https://trunkbaseddevelopment.com/
15. https://martinfowler.com/articles/branching-patterns.html
16. https://nvie.com/posts/a-successful-git-branching-model/
17. https://docs.github.com/en/get-started/using-github/github-flow
18. https://dora.dev/capabilities/trunk-based-development/
19. https://techblog.woowahan.com/2553/
20. https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow (body not retrievable)
21. https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-git-branch-approach/welcome.html (body not retrievable)
22. https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models
23. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-a-branch-for-an-issue
24. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
25. https://velog.io/@rmaomina/pre-project-github-features-convensions
26. https://google.github.io/eng-practices/review/reviewer/speed.html
27. https://conventionalcomments.org/
28. https://google.github.io/eng-practices/review/developer/small-cls.html
29. https://blog.banksalad.com/tech/banksalad-code-review-culture/
30. https://tech.kakao.com/posts/498 (body not retrievable)
31. https://docs.github.com/en/copilot/tutorials/review-ai-generated-code
32. https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors
33. https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/review-copilot-prs
34. https://code.claude.com/docs/en/settings
35. https://www.conventionalcommits.org/en/v1.0.0/
36. https://commitlint.js.org/
37. https://code.claude.com/docs/en/settings-reference
38. https://github.com/conventional-changelog/commitlint/tree/master/@commitlint/config-conventional
39. https://github.com/amannn/action-semantic-pull-request
40. https://lefthook.dev/
41. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
42. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues
43. https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations
44. https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels
45. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization
46. https://github.blog/changelog/2026-07-02-issue-fields-are-now-generally-available
47. https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-iteration-fields
48. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github
49. https://github.com/googleapis/release-please
50. https://docs.github.com/en/pull-requests/get-started/about-stacked-prs
51. https://spin.atomicobject.com/squash-merge/
52. https://discourse.julialang.org/t/downsides-of-using-squash-merging/68317
53. https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks
54. https://docs.github.com/en/billing/concepts/product-billing/github-actions
55. https://github.blog/changelog/2023-07-12-pull-request-merge-queue-is-now-generally-available/
56. https://github.blog/changelog/2019-12-19-improved-attribution-when-squashing-commits/
57. https://github.com/dorny/paths-filter
58. https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
59. https://research.google/pubs/modern-code-review-a-case-study-at-google/
60. https://google.github.io/eng-practices/review/reviewer/standard.html
61. https://martinfowler.com/articles/ship-show-ask.html
62. https://trunkbaseddevelopment.com/short-lived-feature-branches/
63. https://learn.microsoft.com/en-us/azure/devops/repos/git/git-branching-guidance
64. https://conventional-branch.github.io/ → https://conventionalbranch.org/
65. https://www.thoughtworks.com/radar/techniques/long-lived-branches-with-gitflow
66. https://blog.banksalad.com/tech/become-an-organization-that-deploys-1000-times-a-day/
67. https://tech.kakao.com/2022/03/17/2022-newkrew-onboarding-codereview/ (body not retrievable)
68. https://www.samsungsds.com/kr/insights/global_code_review.html
69. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
70. https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization
71. https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request
72. https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection
73. https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md
74. https://github.com/pricing
75. https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/configure-automatic-review
76. https://code.claude.com/docs/en/github-actions
77. https://developers.openai.com/codex/integrations/github → https://learn.chatgpt.com/docs/third-party/github
78. https://dora.dev/research/2025/dora-report/
79. https://education.github.com/pack
80. https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically
81. https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
82. https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
83. https://git-scm.com/docs/git-check-ref-format
84. https://git-scm.com/docs/git-bisect
85. https://cbea.ms/git-commit/
86. https://www.conventionalcommits.org/ko/v1.0.0/
87. https://typicode.github.io/husky/
88. https://commitlint.js.org/guides/ci-setup.html
89. https://www.microsoft.com/en-us/research/publication/convergent-software-peer-review-practices/
90. https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/
91. https://arxiv.org/abs/2412.18531
92. https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report
93. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
94. https://docs.kernel.org/process/coding-assistants.html
95. https://github.com/vercel/next.js/blob/canary/contributing.md
96. https://fastapi.tiangolo.com/contributing/ (no branching details on page)
97. https://www.kubernetes.dev/docs/guide/pull-requests/
98. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
99. https://mergify.com/pricing
100. https://velog.io/@daram_dev/Git-공통-규칙-정리
101. https://yozm.wishket.com/magazine/detail/1497/
102. https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-personal-account-settings/permission-levels-for-a-personal-account-repository
103. https://github.com/github/ruleset-recipes
104. https://velog.io/@maruru301/goormTIL-Git-협업-48
105. https://docs.github.com/en/education/about-github-education/github-education-for-students/apply-to-github-education-as-a-student
106. https://github.blog/changelog/2026-03-13-optionally-skip-approval-for-copilot-coding-agent-actions-workflows/
107. https://github.blog/changelog/month/08-2026/
108. https://github.blog/changelog/month/09-2026/
109. https://github.blog/changelog/month/10-2026/

**Seen in search results (snippet-level; cited only where noted)**
- https://docs.github.com/en/enterprise-server@3.17/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets
- https://docs.github.com/en/enterprise-cloud@latest/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue
- https://github.blog/changelog/2021-10-27-pull-request-merge-queue-limited-beta/
- https://github.blog/changelog/label/velocity/
- https://graphite.dev/guides/github-merge-queue
- https://zenn.dev/korosuke613/scraps/d7b3e3c5db452f
- https://buildkite.com/blog/using-github-mergequeue-in-pipelines
- https://aicoolies.com/reviews/mergify-review
- https://freetier.co/directory/products/mergify
- https://vpsranking.com/news/ai/ai-2026-08-07-github-code-quality-copilot-review/
- https://github.blog/changelog/month/06-2025/page/2/
- https://www.ucl.ac.uk/advanced-research-computing/expertise/research-software-development/research-software-development-tools/support-ucl-researchers
- https://gitbook.brown.edu/cis-cloud-services/github
- https://ithelp.brown.edu/kb/articles/requesting-a-github-org
- https://blog.nachonacho.com/best/github-promo-codes/
- https://www.toolsforhumans.ai/ai-tools/github-copilot
- https://userjot.com/blog/github-copilot-pricing-guide-2025
- https://docs.github.com/fr/copilot/get-started/plans
- https://fast.io/resources/github-copilot-free-access/
- https://samexpert.com/github-copilot-licensing-guide/
- https://velog.io/@kw2577/Git-branch-전략
- https://velog.io/@jeiho/231226
- https://wikidocs.net/277135
- https://www.glukhov.org/post/2025/06/gitflow-steps-and-alternatives/
- https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development
- https://www.atlassian.com/ko/continuous-delivery/continuous-integration/trunk-based-development
- https://graphite.dev/blog/stop-using-feature-branches
- https://flagsmith.com/blog/trunk-based-development
- https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/choosing-git-branch-approach/advantages-and-disadvantages-of-the-trunk-strategy.html
- https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/choosing-git-branch-approach/trunk-branching-strategy.html
- https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/choosing-git-branch-approach/advantages-and-disadvantages-of-the-git-hub-flow-strategy.html
- https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/choosing-git-branch-approach/advantages-and-disadvantages-of-the-gitflow-strategy.html
- https://news.hada.io/topic?id=1669
- https://news.hada.io/weekly/202010
- https://www.techtarget.com/searchsoftwarequality/tip/Compare-trunk-based-development-to-feature-based-approaches
- https://nira.com/git-flow-vs-github-flow/
- https://velog.io/@calm0_0/GIT-브랜치-전략
- https://velog.io/@zz1996zz/Git-Flow
- https://www.hatica.io/blog/best-git-branching-strategies/
- https://www.datacamp.com/ko/tutorial/git-branching-strategy-guide
- https://page.gitlab.com/resources-ebook-branching-strategies-ko-kr.html
- https://terrific-beryl-003.notion.site/BE-1-1740ff5456af80179841fe1e3ce27f46
- https://daleseo.com/unicode/
- https://gist.github.com/Pusnow/aa865fa21f9557fa58d691a8b79f8a6d
- https://juejin.cn/post/7666446436604198939
- https://github.blog/2022-03-21-start-working-on-github-issues-faster
- https://github.com/robvanderleek/create-issue-branch
- https://gitlab.com/gitlab-org/gitlab-ce/issues/21143
- https://yozm.wishket.com/magazine/detail/1903
- https://yozm.wishket.com/magazine/detail/2420/
- https://news.hada.io/topic?id=6886
- https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
- https://tekin.co.uk/2020/05/proof-your-thousand-line-pull-requests-create-more-bugs
- https://mikeconley.ca/blog/tag/loc/
- https://www.atlassian.com/blog/add-ons/code-review-best-practices
- https://www.theregister.com/2025/12/17/ai_code_bugs/
- https://www.businesswire.com/news/home/20251217666881/en/CodeRabbits-State-of-AI-vs-Human-Code-Generation-Report
- https://itbrief.co.uk/story/study-finds-ai-generated-code-far-buggier-than-human-work
- https://dev.to/coderabbitai/our-new-report-ai-code-creates-17x-more-problems-7lh
- https://www.aviator.co/blog/?p=5968
- https://www.coderabbit.ai/guides/code-review-best-practices-for-ai-generated-code
- https://rollbar.com/blog/ai-pull-requests
- https://www.alphaxiv.org/overview/2510.05450v1
- https://conf.researchr.org/details/icse-2025/icse-2025-software-engineering-in-practice/8/Automated-Code-Review-In-Practice
- https://conf.researchr.org/details/ase-2025/ase-2025-industry-showcase/58/What-Types-of-Code-Review-Comments-Do-Developers-Most-Frequently-Resolve-
- https://repository.bilkent.edu.tr/items/8e7ac28e-5120-4c6e-84e3-e7d288c336f0
- https://eweek.com/news/news-ai-tools-slow-developer-productivity-study
- https://diginomica.com/node/29061
- https://docs.github.com/en/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot
- https://learn.microsoft.com/en-us/training/modules/github-copilot-code-agent/3-assign-track-troubleshoot-copilot-code-agent-tasks
- https://claudelog.com/faqs/attribution-setting-claude-code/
- https://github.com/anthropics/claude-code/issues/22585
- https://github.com/anthropics/claude-code/issues/14241
- https://www.deployhq.com/blog/how-to-use-git-with-claude-code-understanding-the-co-authored-by-attribution
- https://zenn.dev/dk_/articles/8e4726b71f7803?locale=en
- https://github.blog/changelog/2025-03-18-github-issues-projects-rest-api-support-for-issue-types
- https://github.blog/changelog/2025-03-06-github-issues-projects-api-support-for-issues-advanced-search-and-more/
- https://github.com/orgs/community/discussions/137767
- https://github.com/python/cpython/pull/136831
- https://www.python.org/pipermail/scipy-dev/2021-August/024991.html
- https://www.python.org/pipermail/scipy-dev/2021-August/024992.html
- https://www.python.org/pipermail/scipy-dev/2021-August/024994.html
- https://www.python.org/pipermail/scipy-dev/2021-August/024995.html
- https://git.uoc.run.place/Applied-Software/ghostty/wiki/Developer-FAQ
- https://dev.to/igorsantos07/my-preferred-merge-strategy-for-pull-requests-1lo5
- https://echobind.com/post/stacked-pull-requests-with-squash-merge
- https://blog.matt-rickard.com/p/stacked-pull-requests
- https://www.gitkraken.com/?p=9226
- https://gitlab.com/gitlab-org/gitlab/-/work_items/593408
