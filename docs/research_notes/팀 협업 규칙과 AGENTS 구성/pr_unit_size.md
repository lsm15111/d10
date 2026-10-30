# PR unit and size for a small student team (믿집, SKN34, Oct 2026)

Research date: 2026-10-29. Scope: what one PR should contain, how large it should be, and how to split, count and enforce size, including PRs written by AI agents. Classic studies (pre-2023) are labelled **[classic]**. Vendor data is labelled **[vendor]** because these companies sell review or metrics tools.

---

## 1. Empirical evidence: change size vs review quality, defect detection, merge time

### Takeaway
Most of the evidence says reviews get worse as changes get bigger: fewer useful comments, lower defect density found, more cursory reviews, and more bugs per developer once AI makes PRs larger. The evidence that small PRs *merge faster* is mixed. A large MSR 2022 study and a 2025 Sourcery analysis found no relation between size and time-to-merge. So the case for small PRs rests mainly on **review quality and risk**, not raw speed.

### Cited Findings
**Classic inspection/review studies**
- **[classic, 2006, vendor-linked]** The SmartBear/Cisco MeetingPlace case study recommends reviewing no more than 200–400 LOC at a time and says the ability to find defects drops beyond 400 LOC. It recommends an inspection rate under 500 LOC/hour and sessions of at most 60–90 minutes, and says a 200–400 LOC review over 60–90 minutes should find 70–90% of defects. — [SmartBear best practices](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)
- The Cisco study is described as about 2,500 reviews, 50 developers and 3.2M LOC over 10 months. Commentators note that the figures are specific to that codebase and that the study promotes SmartBear's own tool (Code Collaborator). — [SlideShare summary](https://www.slideshare.net/slideshow/w10-30218870/30218870); [Mike Conley blog](https://mikeconley.ca/blog/tag/loc/); [OpenStack-dev thread](https://lists.openstack.org/pipermail/openstack-dev/2013-August/013985.html)
- **[classic, 2020 blog citing 2006 data]** Defect density found was highest below 200 changed lines and generally fell as reviews got larger. Defect discovery rates fall after about 60–90 minutes of review. — [tekin.co.uk](https://tekin.co.uk/2020/05/proof-your-thousand-line-pull-requests-create-more-bugs)
- **[classic, Microsoft Research, MSR 2015]** Bosu, Greiler and Bird analysed 1.5M review comments across five Microsoft projects. The more files a change touches, the lower the share of review comments that are useful to the author. — [Microsoft Research](https://www.microsoft.com/en-us/research/?p=168510); [RDEL #16 summary](https://rdel.substack.com/p/rdel-16-what-makes-a-code-review); [Greiler slides](https://www.slideshare.net/mgreiler/on-to-code-review-lessons-learned-at-microsoft)
- **[classic, FSE 2013]** Rigby and Bird found that review parameters (interval, reviewer count) converge across Google (Android, Chrome), Microsoft (Bing, Office, SQL), AMD and OSS. Peer review increased the number of distinct files a developer knows by 66–150%. — [Microsoft Research: Convergent Software Peer Review Practices](https://www.microsoft.com/research/publication/convergent-software-peer-review-practices/); [paper PDF](https://users.ece.utexas.edu/~miryung/teaching/EE379K-Spring2014/Papers/Paper%204.pdf)

**Google's modern code review (ICSE-SEIP 2018) [classic]**, verified from the paper PDF:
- Data: 9M reviewed changes, 12 interviews, 44 survey respondents. — [Google Research](https://research.google/pubs/modern-code-review-a-case-study-at-google/)
- Over 35% of changes modify a single file and about 90% modify fewer than 10 files. Over 10% change a single line. The **median change is 24 lines**, compared with AMD at 44 lines and Lucent at 263; OSS medians are 11–32 lines. — [paper PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf)
- Median time to initial feedback is **under 1 hour for small changes and about 5 hours for very large ones**. The overall median review latency is **under 4 hours**, against 14.7–19.8 hours at Microsoft/AMD/Chrome OS in Rigby and Bird. **70% of changes are committed less than 24 hours after being mailed.** The median reviewer count is 1, and fewer than 25% of changes have more than one reviewer. — [paper PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf)
- The paper says the number of useful comments decreases and review latency increases with change size, and that Google strongly encourages "small, incremental changes". — [paper PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf)

**Counter-evidence on merge speed**
- **[classic, MSR 2022]** Kudrjavets et al. studied 845,316 PRs from 100 popular GitHub projects in 10 languages, plus 401,790 Gerrit/Phabricator reviews. PR size and composition "do not relate to time-to-merge", which the authors present as a negative result against industry belief. — [arXiv 2203.05045](https://arxiv.org/abs/2203.05045); [MSR 2022 listing](https://conf.researchr.org/details/msr-2022/msr-2022-technical-papers/21/Do-Small-Code-Changes-Merge-Faster-A-Multi-Language-Empirical-Investigation)
- **[vendor, Jul 2025]** Sourcery looked at one year of PRs from 200+ (233) top OSS projects. It found almost no correlation between PR size and review time; 46.4% of PRs were under 100 lines and 10.9% over 500. It suggests large PRs may get less thorough review rather than slower review. — [Sourcery](https://sourcery.ai/blog/code-review-timing)
- **[vendor, 2022]** Jellyfish analysed about 2M PRs from 102 companies. Size had only a weak positive correlation with review comments (0.22 and 0.17). About 48% of PRs get zero comments. It recommends PRs under 200 lines. — [Jellyfish](https://jellyfish.co/blog/larger-pull-requests/)
- **[vendor]** Greptile looked at about 24,300 merged PRs across 100 organisations and reports an inverse relation between files changed and merge speed, which contradicts Kudrjavets. — [Greptile](https://www.greptile.com/what-affects-merge-time)
- **[classic, controlled experiment]** Di Biase et al. ran an experiment with 28 developers. Decomposing a change led to fewer wrongly reported issues, but did not increase the number of defects found or improve understanding of the rationale. — [arXiv 1805.10978](https://arxiv.org/abs/1805.10978)

**Vendor size data 2023–2026**
- **[vendor, Jul 2023]** Graphite argues "the ideal code change is 50 lines", within a 25–100 line range. Its claims: 50-line changes are reviewed and merged about 40% faster than 250-line changes, are about 15% less likely to be reverted, and get about 40% more comments per line. PRs under 10 lines have the highest chance of a "blind stamp". Caveats: Graphite users skew small, and a "revert" means "Revert" appears in the title. — [Graphite](https://graphite.com/blog/the-ideal-pr-is-50-lines-long)
- **[vendor]** LinearB's benchmarks come from 3,694,690 PRs across 2,022 organisations and include PR size, but are presented as "reference points, not rigid targets". LinearB's help docs say bug and stall risk rise sharply past 400–800 lines. — [LinearB benchmarks](https://linearb.helpdocs.io/article/q42n7g3ybk-benchmarks); [LinearB managing large PRs](https://linearb.helpdocs.io/article/drons87w53-managing-large-pull-requests)
- An older LinearB benchmark republished on LeadDev puts elite cycle time under 42 hours, with pickup under 1 hour. — [LeadDev](https://zporigin.leaddev.com/?p=8745)
- Typo recommends PRs under 200 lines, and Cubic claims PRs over 400 lines catch fewer bugs. These are both vendor posts without visible data. — [Typo](https://typoapp.io/blog/reduce-pr-cycle-time); [Cubic](https://www.cubic.dev/blog/does-pr-size-actually-matter)
- **[vendor]** Graphite reports that the median active reviewer receives 3 review requests per week, with a 71.5% review rate. — [Graphite research](https://graphite.com/research/review-request-frequency)

**AI era (2025–2026)**
- **[vendor, 2025]** Faros AI telemetry on 10k+ developers and 1,255 teams links AI use to 98% more PRs merged and **91% longer PR review time**, with no company-level gain. Reported PR-size growth varies by source: +51.3% in a Faros FAQ, +154% in a secondary write-up. — [Faros blog](https://www.faros.ai/blog/are-ai-coding-assistants-really-saving); [Augment summary](https://www.augmentcode.com/guides/ai-productivity-paradox-engineering-delivery)
- **[vendor, 2026]** Faros "Acceleration Whiplash" covered about 22k developers. It reports bugs per developer +54%, incident-to-PR ratio more than 3×, median review time 5×, and 31% more PRs merged with no review. — [Faros research](https://faros.ai/research/ai-acceleration-whiplash)
- **[vendor, Dec 2025]** CodeRabbit compared 470 OSS PRs (320 AI-co-authored, 150 human-only). AI-involved PRs averaged 10.83 issues against 6.45, about 1.7×. The authors note it was hard to tell which PRs were AI-authored. — [CodeRabbit](https://coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report); [The Register](https://www.theregister.com/2025/12/17/ai_code_bugs/)
- **[vendor, 2026]** Swarmia's docs say agent PRs initially cluster at the extremes, in the 1–5 line and 500+ line buckets, and should move toward the middle as usage matures. — [Swarmia agent batch size](https://help.swarmia.com/features/ai-tools/cloud-agents); [Swarmia changelog 2026-02-02](https://www.swarmia.com/changelog/2026-02-02-ai-agent-metrics/)
- GitHub Octoverse 2025: on average 43.2M PRs merged per month, up 23% year over year, with the growth tied partly to AI. — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- DORA 2025 (about 5,000 respondents) calls AI an "amplifier" of existing strengths and dysfunctions. — [DORA 2025 report](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/); [DX newsletter summary](https://newsletter.getdx.com/p/doras-2025-research-on-the-impact)

**Review latency interventions**
- **[Meta, 2022]** Meta's north-star metric is the P75 of "Time In Review", with reviewer "eyeball time" as a guardrail. NudgeBot reduced time in review by 6.8% and time to first action by 9.9% in an A/B test on more than 30k engineers. — [Meta engineering](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/); [FSE 2022](https://2022.esec-fse.org/details/fse-2022-research-papers/26/Using-Nudges-to-Accelerate-Code-Reviews-at-Scale)
- **[Microsoft, TOSEM 2022]** Nudge reduced resolution time of overdue PRs by 60% across 8,500 PRs in 147 repositories. — [arXiv 2011.12468](https://arxiv.org/abs/2011.12468v5)

### Inferences
- Size thresholds converge loosely: **ideal ~25–200 lines, warning ~400, too large ~1,000**. The 400 figure comes from one vendor-linked 2006 study and is reinforced by later vendor data, so it works as a convention, not a law.
- The strongest justification for a cap is reviewer attention and defect finding, plus the AI-era observation that output grows faster than review capacity. Expect small PRs to *improve quality and reduce reverts and conflicts*, not necessarily to cut merge time.
- Files touched matters as well as lines (Microsoft; Google's "200 lines across 50 files"), so a rule should not use line count alone.

### Gaps
- I could not see LinearB's actual per-tier PR-size thresholds (for example, whether "elite" means under N lines); the page doesn't list them.
- I found no 2023–2026 peer-reviewed study isolating PR size vs defect escape for *small student teams*. Every dataset is industry or OSS.
- The Faros PR-size figures (+51% vs +154%) conflict, and both are vendor telemetry with no causal design.

---

## 2. How major organisations define the PR unit (Google, Meta, GitLab, Shopify, Kubernetes, Korean companies)

### Takeaway
Organisations agree on the unit: **one self-contained change that does one thing, includes its tests, and leaves main working.** Size numbers are secondary heuristics (Google: ~100 lines reasonable, 1,000 too large). Korean companies' public blogs rarely publish numeric PR-size rules. What exists is "작은 단위로 쪼개기" plus automating style and build checks so reviewers don't have to.

### Cited Findings
- **Google eng-practices:** the right size is "one self-contained change" that addresses one thing, usually part of a feature, and includes related tests, with the system working after submission. "100 lines is usually a reasonable size for a CL, and 1000 lines is usually too large." A 200-line change spread across 50 files is usually too large. Reviewers may reject a CL for size alone. "When in doubt, write CLs that are smaller than you think." — [Google eng-practices: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- Google exceptions: deleting a whole file counts as about one line, and changes from a trusted automatic refactoring tool may be larger. When a CL truly cannot be small (said to be "very rarely true"), do a refactoring CL first, or get reviewers' consent in advance. — [Google eng-practices: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- A secondary source reports the eng-practices GitHub repo was archived on 2025-11-21 while the static site remains, and secondary summaries quote different target numbers. — [pasqualepillitteri.it](https://pasqualepillitteri.it/en/news/3317/google-code-review-guidelines-internal-principles-industry-standard); [DeployHQ](https://www.deployhq.com/blog/google-code-review-playbook-deployment-velocity)
- **Meta (Phabricator):** stacks of diffs are "a series of changes, each standing alone but also building on the previous changes". Stacking lets reviewers discuss each change in isolation and keeps refactorings apart from functional changes. — [Meta developers blog 2022](https://developers.facebook.com/blog/post/2022/11/15/meta-developers-workflow-exploring-tools-used-to-code/?locale=fr_FR); [Pragmatic Engineer: Stacked diffs](https://newsletter.pragmaticengineer.com/p/stacked-diffs)
- **GitLab:** engineers should "always seek to create smaller merge requests". Tactics include moving edge cases to follow-up issues and splitting off complex refactors; with "one commit, one logical change", each commit can be its own MR. Horizontal (by-stack) splits must be explained in a linked plan. — [GitLab handbook: Iteration](https://handbook.gitlab.com/handbook/engineering/workflow/iteration)
- GitLab contributor docs ask whether a feature can start with "only backend/API code" and say "the smaller an MR is, the more likely it will be merged quickly". GitLab's Danger bot asks authors to break up MRs above a size threshold. — [GitLab MR workflow mirror](https://ciii.frc.utn.edu.ar/gitlab/help/development/contributing/merge_request_workflow.md); [GitLab blog 2021](https://about.gitlab.com/blog/iteration-and-code-review/); [GitLab issue 30646](https://gitlab.com/gitlab-org/gitlab/-/work_items/30646)
- **Kubernetes:** "We'd rather have 100 small, obvious pull requests than 10 unreviewable monoliths." Small commits and PRs "get reviewed faster and are more likely to be correct". Unrelated fixes go in separate PRs, and repo-wide PRs should be split by SIG ownership. — [Kubernetes contributor guide: pull requests](https://www.kubernetes.dev/docs/guide/pull-requests/)
- **Shopify [vendor case study]:** Graphite claims a 33% increase in PRs shipped per developer after Shopify adopted stacking in its monorepo, where one product change spans API, frontend and mobile. — [Graphite customer: Shopify](https://graphite.com/customer/shopify)
- **Atlassian:** treat reviewers as customers and make smaller PRs. Endless "in review" columns are among the most common retro complaints. — [Atlassian: written unwritten guide to PRs](https://www.atlassian.com/blog/git/written-unwritten-guide-pull-requests)
- **Graphite guidance:** each PR should "achieve a clear goal… and not depend on other unmerged branches". Don't mix bug fixes, features and refactors. — [Graphite: managing PR size](https://graphite.com/guides/best-practices-managing-pr-size)
- **Counterpoint (Elli engineering):** "Don't do small pull requests" argues that blind splitting doesn't guarantee delivery speed. For big refactors and complex logic, pair programming worked better for them. — [Elli](https://www.elli.eco/en/about-elli/news/newsroom/elli-engineering/dont-do-small-pull-requests)
- **Korean sources (weak):**
  - HeyDealer's team recommends splitting PRs and commits into the smallest units, standardising PRs with GitHub templates, and keeping build and convention checks away from reviewers. I saw only a search snippet; the page returned 403. — [theteams.kr HeyDealer](https://www.theteams.kr/teams/8261/post/73201)
  - A Korean wiki guide says "한 PR은 한 가지 목적만 다룬다. 작을수록 리뷰가 빠르고 정확하다" and tells reviewers to ask for splits when a PR is too big. — [wikidocs 253113](https://wikidocs.net/253113)
  - A 2026 Korean dev blog says review latency is mostly decided by the author, and that a ~120-line diff with clear what/why/verification is ideal. It also suggests splitting by layer (DB schema, API, UI) or by feature and separating refactors. — [youngju.dev (2026-05)](https://www.youngju.dev/blog/culture/2026-05-14-authoring-reviewable-pull-requests-small-prs-description-stacked-deep-dive-guide-2026); [youngju.dev (2026-03)](https://www.youngju.dev/blog/culture/2026-03-14-effective-code-review-culture-best-practices)
  - A Korean Git/GitHub guide covers PRs as a communication tool. — [braindetox.kr](https://braindetox.kr/posts/git_github_guide_04_pr_review.html)
  - AB180 reports that review adds workload and that some PRs sit in review for a long time. — [요즘IT AB180](https://yozm.wishket.com/magazine/detail/1497)
  - Kakao's if(kakao)24 talk covers its review philosophy and an internal AI reviewer (CodeBuddy), but gives no size rule. — [Kakao SpeakerDeck](https://speakerdeck.com/kakao/ifkakao24-28)
  - Woowahan's 2017 mobile git-flow post is cited by Korean blogs for feature-named branches. — [velog Git Flow vs GitHub Flow](https://velog.io/@gmlstjq123/Git-Flow-VS-Github-Flow); [velog Git Flow 전략](https://velog.io/@jeiho/231226)
  - A Korean bootcamp team used fixed PR/review/merge deadlines (PR by Tue/Thu 19:00, review by 22:00, merge Wed/Fri 09:00). — [Notion team page](https://arrow-season-125.notion.site/24c7e9dd351b4fcf99e7651faaa60077)

### Inferences
- "One concern per PR" is the operative definition. Line caps exist so that "one concern" can be checked mechanically.
- Korean industry practice in public sources leans on templates, CI-automated conventions and a "small units" norm rather than published numbers. 믿집 can adopt Google/Kubernetes language without conflicting with Korean norms.

### Gaps
- I could not find primary posts from toss.tech, techblog.woowahan.com, tech.kakao.com, medium.com/daangn or engineering.linecorp.com with explicit PR-size rules. Searches returned only job ads and secondary summaries. This should be stated as "not found", not "doesn't exist".
- I found no official Stripe engineering post on PR size.

---

## 3. Splitting strategies: vertical vs horizontal, refactor-first, flags, stacked PRs, draft PRs, migrations, generated code, formatting

### Takeaway
The standard toolkit:
- **refactor/tidy first** in its own PR;
- **vertical slices** when a slice stays small;
- **horizontal layers with stubs**, or a **stack**, when it doesn't;
- **feature flags** only as a last resort to merge incomplete work;
- **separate PRs for schema migrations (expand → contract), dependency/lockfile bumps and formatting-only changes**;
- **generated code kept in the PR that caused it but excluded from size and collapsed in the diff**.

GitHub's native stacked PRs (via `gh stack`) reached public preview in mid-2026. GitHub explicitly pitches them for breaking up giant AI-generated PRs.

### Cited Findings
**General splitting**
- Google lists five strategies:
  - stacking (start the next CL on top of the pending one);
  - splitting by files or reviewer groups (for example, proto vs code using it, or code vs config);
  - **horizontal** slicing with shared stubs or API signatures;
  - **vertical** slicing into full-stack parallel tracks;
  - a grid combining both.

  Refactorings stay separate from feature or bug-fix CLs, and small cleanups may stay. Logic changes need tests in the same CL. Every dependent CL must leave the system working. — [Google eng-practices: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- Kent Beck's rule is "make the change easy, then make the easy change". Tidyings go in their own PRs ("as little tidying per PR as possible"), structural and behavioural changes in separate PRs or commits. When the two get tangled, untangle them or restart tidying-first. — [Kent Beck newsletter](https://newsletter.kentbeck.com/p/tidy-first-example); [Kent Beck: Getting untangled](https://tidyfirst.substack.com/p/getting-untangled); [Henrik Warne review](https://henrikwarne.com/2024/01/10/tidy-first/)
- Feature/release toggles are temporary and should be removed once the feature ships. Fowler, as summarised by others, treats release toggles as a last choice and prefers splitting a feature into small, independently releasable parts. Unleash gives release toggles an expected lifetime of 40 days. — [Wikipedia: Feature toggle](https://en.wikipedia.org/wiki/Feature_toggle); [InfoQ 2016](https://www.infoq.com/news/2016/02/featuretoggles/); [Unleash toggle types](https://git.laurivan.com/Mirrors/unleash.unleash/blame/commit/99b27061aae9d77f8fd62f1ac993b39b9ba410ce/docs/feature-toggle-types.md)
- Mergify notes that teams keep branches short by splitting large features with feature flags and stacked PRs. — [Mergify short-lived branches](https://mergify.com/learn/trunk-based-development/short-lived-branches)

**Stacked PRs (2026 status)**
- InfoQ (April 2026) reported GitHub launching stacked PRs via the `gh-stack` CLI extension. IT Brief (31 July 2026) reported public preview rolling out across all repositories. Each PR in a stack targets the branch below it, branch protection and required checks still gate main, and merge queues handle stacks in order. — [InfoQ](https://infoq.com/news/2026/04/github-stacked-prs); [IT Brief](https://itbrief.co.uk/story/github-puts-stacked-pull-requests-into-public-preview); [DevOps.com](https://devops.com/github-brings-stacked-pull-requests-out-of-the-shadows/); [GitHub docs: stacked PRs](https://docs.github.com/en/pull-requests/how-tos/stacked-pull-requests)
- GitHub blog (4 Aug 2026), "Turn one giant AI-generated PR into a reviewable stack":
  - It contrasts a deferred 1,721-line PR with four layers: data catalog, search API, chat wiring, grounded UI.
  - Each layer should be "small enough to hold in a reviewer's head" and runs its own validation.
  - Install the agent skill (`gh skill install github/gh-stack`), assign layers to specialised agents, and confirm CI runs on every layer.
  - Use `gh stack rebase` locally rather than the web "Rebase stack" button, which commits unsigned as the clicking user.

  — [GitHub blog](https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/)
- Other stacking tools:
  - Graphite: a chain of small dependent PRs, each tested, reviewed and merged independently. — [Graphite: stacked PRs](https://graphite.com/blog/stacked-prs); [Graphite: reviewing stacks](https://graphite.com/docs/best-practices-for-reviewing-stacks)
  - Modular's open-source `stack-pr`. — [Modular stack-pr](https://www.modular.com/blog/announcing-stack-pr-an-open-source-tool-for-managing-stacked-prs-on-github)
  - GitLab has an older issue requesting stacked diffs in MRs. — [GitLab issue 52229](https://gitlab.com/gitlab-org/gitlab-ce/-/issues/52229)
- Trade-off: stacking means more frequent rebasing of small diffs. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/stacked-diffs)

**Draft PRs**
- A draft PR cannot be merged until it is marked "Ready for review", and marking it ready requests reviews from code owners. Code owners aren't auto-requested on drafts. — [GitHub docs: changing the stage of a PR](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request); [GitHub docs: about code owners](https://docs.github.com/en/enterprise-server@3.14/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

**Migrations**
- Never combine expand and contract in one PR. A deploy runs the migration before new code rolls out, so old code must keep working against the new schema. Dropping or renaming a column must come in a later PR, after nothing reads it. — [tessl db-migrate skill](https://tessl.io/registry/skills/github/simstudioai/sim/db-migrate)
- Unleash's ADR requires all migrations in separate PRs and asks reviewers to flag `DROP COLUMN`/`RENAME TO` that skipped the expand phase. — [Unleash ADR: breaking DB changes](https://docs-new.getunleash.io/contributing/ADRs/back-end/breaking-db-changes)
- Prisma recommends a database per branch so migrations from different PRs don't collide. Redgate calls the pattern "Parallel Change" and separates DB deploys from feature releases. — [Prisma blog](https://www.prisma.io/blog/ship-risky-schema-changes-without-a-shared-staging-database); [Redgate Simple Talk](https://www.red-gate.com/simple-talk/blogs/reordering-deployments-in-database-devops/)

**Generated code and lockfiles**
- Marking paths `linguist-generated` in `.gitattributes` hides them by default in GitHub diffs and excludes them from language stats. They can still be expanded. — [GitHub docs: customizing how changed files appear](https://docs.github.com/en/repositories/working-with-files/managing-files/customizing-how-changed-files-appear-on-github); [Medium (2018)](https://medium.com/@clarkbw/1f1989c09dfd)
- GitLab asked for the same diff minimisation. — [Gitaly issue 4832](https://gitlab.com/gitlab-org/gitaly/-/issues/4832)
- GitLab's Danger bot told an author that an MR adding a yarn dependency was "quite big" (1,166 lines). The issue proposes excluding `Gemfile.lock`, `yarn.lock` and generated GraphQL docs from the count. — [GitLab issue 24541](https://gitlab.com/gitlab-org/gitlab/-/issues/24541)
- LangChain's labeler excludes `uv.lock` by basename because lockfile-only PRs were mislabelled. — [semanticdiff: langchain commit](https://app.semanticdiff.com/gh/langchain-ai/langchain/commit/a9d31b30f835b73e0d9c5c246465d0266fd487fb)
- For OpenAPI→TS types, the common pattern is to commit the generated file and fail CI when regeneration produces a `git diff`. Pin Node/Prettier versions to avoid false drift. — [Capgo: openapi-typescript](https://capgo.app/blog/openapi-typescript/); [Scope3 CI parity guide](https://docs.agentic.scope3.com/docs/CI_LOCAL_PARITY)

**Formatting-only changes**
- Put formatting in its own PR and list its commit hashes in `.git-blame-ignore-revs`, which GitHub's blame view honours. With squash merge, the hash on main differs from the branch hash, so add it in a follow-up PR. pydata-sphinx-theme rebase-merges formatting PRs for this reason. — [pydata/pst docs](https://pst-notebook-cell-styling.readthedocs.io/en/latest/community/topics/attribution.html); [eslint/markdown PR 601](https://github.com/eslint/markdown/pull/601); [codidact thread](https://software.codidact.com/posts/293029/293051); [nilearn issue 3653](https://github.com/nilearn/nilearn/issues/3653)

### Inferences
- For 믿집's FastAPI + Alembic + OpenAPI→TS + Next.js stack, a natural vertical feature splits into three stackable layers:
  1. Alembic migration + SQLAlchemy model (expand only);
  2. FastAPI endpoint + pytest + regenerated OpenAPI TS types;
  3. Next.js UI.

  Each layer can merge green on its own, because the API layer doesn't need the UI and the UI consumes the committed types.
- Feature flags add cleanup debt. For a one-month student project, prefer "unlinked route/page not in nav" or backend-only endpoints over a flag system.
- GitHub's native stacking is in public preview and new. Manual stacking (base = previous branch, retarget after merge) also works, but squash merge rewrites history, so upper branches need `git rebase --onto`. `gh stack` automates this cascading rebase.

### Gaps
- I didn't confirm whether GitHub stacked PRs are GA as of 2026-10-29. The latest source I found (31 July 2026) says public preview.
- I didn't fetch Fowler's Feature Toggles article directly; the points above come from secondary summaries.

---

## 4. Branching model and PR lifetime: trunk-based vs GitHub flow vs git-flow; WIP limits

### Takeaway
For a short project with continuous deploys, the git-flow author himself recommends **GitHub flow**. Trunk-based guidance caps feature-branch life at **about 2 days** (stricter readings: under 1 day) with one developer per branch. In the agent era, "one developer plus their agents" counts as one unit. DORA links high performance to **≤3 active branches** and merging to trunk at least daily. 믿집's "merge within 2 days" is at the permissive edge of this guidance.

### Cited Findings
- trunkbaseddevelopment.com: a short-lived feature branch should last only "a couple of days"; longer risks becoming a long-lived feature branch. Time waiting for review counts toward that. One developer per branch (two if pairing). The site's agentic-coding update:
  - One developer and their agents form one unit.
  - Human review becomes the bottleneck.
  - AI-assisted review and CI should handle what machines can.
  - Keep each agent's change small and integrate one at a time.

  — [trunkbaseddevelopment.com: short-lived feature branches](https://trunkbaseddevelopment.com/short-lived-feature-branches/)
- DORA: teams that have "three or fewer active branches" perform better (2016–2017 data). Measure the active branch count and make it visible. — [DORA: trunk-based development](https://dora.dev/capabilities/trunk-based-development/)
- Secondary sources say "fewer than three" branches and merge at least daily; one cites a 24-hour line, another "hours or a day". — [Infobip summary](https://www.infobip.com/developers/wp-json/wp/v2/posts/1852); [Mergify](https://mergify.com/learn/trunk-based-development/short-lived-branches); [Unleash TBD guide](https://getunleash.io/trunk-based-development)
- Gitflow has more, longer-lived branches and larger commits than trunk-based development. — [Atlassian: trunk-based development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development)
- nvie's "Note of reflection" (5 March 2020): teams doing continuous delivery should adopt "a much simpler workflow (like GitHub flow)". git-flow still fits explicitly versioned software that supports several versions in the field. — [nvie.com](https://nvie.com/posts/a-successful-git-branching-model/)
- An archived Microsoft DevOps post says git-flow assumes long-lived feature branches and is poorly suited to CD. — [Microsoft archive](https://learn.microsoft.com/en-us/archive/blogs/technet/devops/a-git-workflow-for-continuous-delivery)
- GitHub flow: branch off the default branch, open a PR, review, merge, delete the branch. Branch protection can block merge until requirements are met. — [GitHub docs: GitHub flow](https://docs.github.com/en/enterprise-server@3.22/get-started/using-github/github-flow)
- Squash merge folds a PR into one commit on the base branch; the trade-off is losing per-commit history. With a merge queue, the queue controls the merge method. — [GitHub docs: about merge methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github)
- Google's latency benchmarks: median initial feedback under 1 hour for small changes, overall median under 4 hours, 70% committed within 24 hours. — [Google paper PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf)
- Meta and Microsoft show that nudging stale PRs measurably cuts review time. — [Meta engineering](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/); [Microsoft Nudge](https://arxiv.org/abs/2011.12468v5)
- Meta's companion paper found day of week was the strongest predictor of review time (weekend diffs wait). — [FSE 2022 industry paper](https://2022.esec-fse.org/details/fse-2022-industry/7/Understanding-Why-We-Cannot-Model-How-Long-a-Code-Review-Will-Take-An-Industrial-Cas)

### Inferences
- With 4–6 people, DORA's "≤3 active branches" is too tight literally. A practical WIP limit is **≤1 open ready-for-review PR per person, plus at most one draft**, and the team checks branches older than 2 days at daily stand-up (the human "nudge").
- Bootcamp schedules (classes, weekends) make the Meta day-of-week effect likely. A **first-review SLA of the same or next half-day**, rather than hours, is realistic.
- Squash merge plus Conventional-Commit PR titles gives one commit per PR on main. That makes reverts easy and suits a short project.

### Gaps
- I found no study of branch lifetime specifically in student or bootcamp teams.

---

## 5. Rules for PRs produced by AI coding agents (2025–2026)

### Takeaway
Platform vendors and OSS projects have converged on three rules:
1. **A named human owns and has read every line before requesting review.** Reviewers are never the first to check agent output.
2. **Disclose AI use in the PR.** Kubernetes forbids AI attribution trailers, while LLVM and the Linux kernel use `Assisted-by`.
3. **Large AI-generated PRs are not acceptable.** Split them, for example into stacks.

GitHub makes the approval of whoever launched the agent **not count** toward required approvals, and gates Actions runs on agent PRs behind human approval.

### Cited Findings
**Platform and vendor guidance**
- **GitHub Copilot cloud/coding agent:**
  - "Your approval of a Copilot pull request won't count" toward required approvals; another reviewer must approve.
  - Workflows don't run on Copilot pushes until a human clicks "Approve and run workflows".
  - Reviewers should be alert to changes in `.github/workflows/`, since workflows can access secrets.

  — [GitHub docs: review output from Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output); [GitHub docs: responsible use of Copilot coding agent](https://docs.github.com/en/copilot/responsible-use/copilot-coding-agent)
- **OpenAI Codex best practices:**
  - Frame every task as Goal / Context / Constraints / **Done when**, so Codex "stay[s] scoped… and produce[s] work that's easier to review".
  - "Keep one chat per coherent unit of work."
  - AGENTS.md should hold "engineering conventions and PR expectations" and "what done means and how to verify work".
  - Ask Codex to review the diff for bugs and regressions, and use `/review` against the base branch.
  - The page states "At OpenAI, Codex reviews 100% of PRs".

  — [Codex best practices](https://learn.chatgpt.com/guides/best-practices)
- **Anthropic Claude Code best practices:**
  - Give Claude a check to run (tests, typecheck, CI) and ask for *evidence* (the command and its output), because "'All tests pass' on its own tells you very little".
  - Use `/code-review`, which reviews the diff in a fresh subagent that never saw the conversation.
  - Define a read-only reviewer subagent (`tools: Read, Grep, Glob`) to check the diff against the spec before opening the PR, and tell it to "skip style".
  - Claude opens PRs via `gh`.

  — [Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Claude Code common workflows](https://code.claude.com/docs/en/common-workflows.md)
- **GitHub stacked PRs for agents:** an agent skill teaches stack workflows, and you can assign each layer to a specialised agent. — [GitHub blog (Aug 2026)](https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/)
- **trunkbaseddevelopment.com:** keep each agent's change small and integrate them one at a time; human review is the bottleneck. — [TBD site](https://trunkbaseddevelopment.com/short-lived-feature-branches/)

**Open-source AI contribution policies**
- **Kubernetes:**
  - Disclose AI use in the PR description.
  - No AI co-authors, AI co-signing or AI-attributing trailers.
  - "Large AI generated PRs and AI generated commit messages are not allowed."
  - "Do not leave the first review of AI generated changes to the reviewers."
  - Respond to review comments without AI tools.
  - PRs are closed if the author can't explain the change.

  — [Kubernetes contributor guide](https://www.kubernetes.dev/docs/guide/pull-requests/); [K8s dev announcement](https://groups.google.com/a/kubernetes.io/g/dev/c/7Y9016gdFZw/m/NQbEfZQvAgAJ); [Kubernetes blog (2026-06-26)](https://kubernetes.io/blog/2026/06/26/open-source-maintainership-in-the-age-of-ai/)
- **LLVM:**
  - Contributors "must read and review all LLM-generated code or text before they ask other project members to review it" and must answer reviewers' questions.
  - Label substantial tool-generated content (for example an `Assisted-by` trailer).
  - Write PR descriptions yourself.
  - Autonomous agents acting without human approval, including the GitHub `@claude` agent, are banned.
  - No AI on `good first issue`s.
  - "Extractive" contributions (worth less than the review time they cost) can be labelled and refused; reducing size or complexity makes a contribution less extractive.

  — [LLVM AI Tool Use Policy](https://llvm.org/docs/AIToolPolicy.html); [LLVM RFC](https://discourse.llvm.org/t/rfc-llvm-ai-tool-policy-human-in-the-loop/89159); [Phoronix](https://www.phoronix.com/news/LLVM-Human-In-The-Loop)
- **Linux kernel:** AI-assisted patches carry an `Assisted-by` tag, whose format changed between docs versions. AI agents must not add `Signed-off-by`; the human submitter reviews and certifies. — [kernel docs: AI coding assistants (next)](https://docs.kernel.org/next/process/coding-assistants.html); [kernel docs 7.0](https://kernel.org/doc/html/v7.0/process/coding-assistants.html)
- **Ghostty:**
  - All AI use must be disclosed, with the tool and extent.
  - If you can't explain your change without AI, don't contribute.
  - AI PRs are allowed only for accepted issues and must be human-tested.

  These points come from secondary summaries. — [feedbagel summary](https://feedbagel.com/post/ghostty-projects-ai-usage-policy-transparency-and-human-oversight-requirements); [1984commitlog](https://1984commitlog.substack.com/p/the-driver-not-the-car); [arXiv 2605.16706](https://arxiv.org/pdf/2605.16706)
- **JupyterHub and earthaccess:** disclose the tool(s), version and how they were used, and specify which code is AI-generated; PRs without disclosure are rejected. Autonomous agent-submitted PRs are prohibited. — [Jupyter Compass LLM policy](https://compass.hub.jupyter.org/contribute/llm/); [earthaccess AI policy](https://earthaccess.readthedocs.io/en/latest/contributor/ai-policy/)
- **Other projects:**
  - PPSSPP (2026-05-11): agent PRs must state the scope of AI involvement or may be closed. — [PPSSPP AI policy](https://www.ppsspp.org/docs/development/ai-policy)
  - BeeWare (2026-04-24): asks for an `Assisted-by` trailer. — [BeeWare AI policy](https://beeware-docs-tools.readthedocs.io/latest/content_test_bed/how-to/contribute/policies/ai-policy/)
  - FiPy: a human must answer review feedback. — [FiPy AI policy](https://pages.nist.gov/fipy/en/purge_README-like/AI_POLICY.html)
  - Blockly: open debate on AI co-author credit. — [Blockly AI policy thread](https://groups.google.com/g/blockly/c/hazyV4Uu8w0)
- **Restrictive end:**
  - Gentoo (April 2024) and NetBSD (2024) ban AI-generated code; QEMU declines it, with a 2026 proposal to relax this. — [SSD Nodes overview](https://www.ssdnodes.com/learn/ai-assisted-code-open-source-policies); [Linuxiac NetBSD](https://linuxiac.com/netbsd-new-policy-prohibits-usage-of-ai-code/); [The Register QEMU](https://www.theregister.com/a/5248638)
  - tldraw auto-closed external PRs from January 2026. — [GIGAZINE](https://www.gigazine.net/gsc_news/en/20260124-tldraw-pause-ext-contrib); [codenote: external PR shutdowns](https://codenote.net/en/posts/oss-external-pr-shutdown-2026/)
  - curl's PR policy judges code quality regardless of tool; it closed its bug bounty on 31 January 2026 over AI slop reports. — [codenote: curl/Ghostty/tldraw](https://codenote.net/en/posts/oss-ai-slop-contribution-policy-shift/); [It's FOSS](https://itsfoss.com/news/curl-closes-bug-bounty-program/); [opensourcesecurity.io](https://opensourcesecurity.io/2025/2025-05-curl_vs_ai_with_daniel_stenberg/)
  - RedMonk surveyed about 70 organisations' generative-AI policies (February 2026). — [RedMonk](https://redmonk.com/kholterhoff/2026/02/26/generative-ai-policy-landscape-in-open-source/); [LeadDev](https://leaddev.com/software-quality/open-source-has-a-big-ai-slop-problem)

**Empirical data on agent PRs**
- The AIDev dataset has 932,791 agentic PRs. Across agents, average acceptance is 0.66 for Claude Code and 0.45 for Copilot (lowest, with the most review discussion). Results vary with dataset filters. — [arXiv 2602.04226](https://www.arxiv.org/pdf/2602.04226); [arXiv 2602.02345](https://arxiv.org/html/2602.02345v1); [arXiv 2602.08915 (MSR'26)](https://arxiv.org/html/2602.08915v1); [arXiv 2607.21832](https://arxiv.org/pdf/2607.21832)

### Inferences
- The disclosure-trailer split (Kubernetes bans AI trailers; LLVM, the kernel and BeeWare want `Assisted-by`) is a **team choice**. For a student team where every author is known, a PR-template checkbox plus a tool/scope line is enough. Whether to keep Claude Code's default `Co-Authored-By` trailer should be one explicit decision.
- GitHub's rule that "the launcher's approval doesn't count" maps directly onto 믿집's "1 approval": the approver must be **a different human from the one who ran the agent**. An AI review bot (Codex or Claude review) is advisory and never counts as the approval.
- Agents tend toward very large diffs (Swarmia's extremes; Faros size growth). The size cap should apply to agent PRs **at least as strictly** as to human ones, with AGENTS.md telling the agent to stop and propose a split.

### Gaps
- I didn't find an official Anthropic or OpenAI document that sets a numeric PR-size limit for agent output. Their guidance is about scoping, verification and review, not line counts.
- I couldn't load Ghostty's AI_POLICY.md directly; its points come from secondary summaries.

---

## 6. Counting PR size fairly and enforcing it (labels, Actions, Danger, CODEOWNERS)

### Takeaway
Count **additions + deletions, excluding generated, vendored and lockfiles**. Do the exclusion mechanically: mark the files `linguist-generated` in `.gitattributes`, which both collapses them in GitHub diffs and is honoured by Prow-style counters, and mirror the same list in the labeler's ignore setting. Add a **file-count and "one concern"** check, because lines alone miss sprawl. Enforce with a size labeler (warn or fail on XL), an optional Danger rule, and CODEOWNERS plus required reviews. Kubernetes/Prow's buckets (XS < 10, S < 30, M < 100, L < 500, XL < 1000, XXL ≥ 1000) are the de facto label scheme.

### Cited Findings
- **Prow size plugin (Kubernetes):** XS 0–9, S 10–29, M 30–99, L 100–499, XL 500–999, XXL 1000+. It counts additions plus deletions and skips files matched by `.generated_files` or marked `linguist-generated` in `.gitattributes` at the base commit. — [kubernetes-sigs/prow size.go](https://raw.githubusercontent.com/kubernetes-sigs/prow/main/pkg/plugins/size/size.go); [pkg.go.dev size plugin](https://beta.pkg.go.dev/sigs.k8s.io/prow/pkg/plugins/size)
- **CodelyTV/pr-size-labeler:** defaults are xs ≤ 10, s ≤ 100, m ≤ 500, l ≤ 1000, XL above that. Options: `fail_if_xl` to block merge, `message_if_xl`, and `files_to_ignore`. `files_to_ignore` uses whitespace- or newline-separated Bash globs matched against the **full repo path**, so a plain `package-lock.json` matches only the root file; use `*/package-lock.json` for subfolders. `ignore_line_deletions` is also available. — [CodelyTV/pr-size-labeler](https://github.com/CodelyTV/pr-size-labeler); [StepSecurity advisor](https://app.stepsecurity.io/action-advisor/CodelyTV/pr-size-labeler)
- **Other labelers:** coverwallet/pr-labeler takes an `exclude_files` regex, and srvaroa/labeler supports size labels with exclusions. — [coverwallet/pr-labeler](https://github-redirect.dependabot.com/coverwallet/pr-labeler); [srvaroa/labeler](https://github.com/srvaroa/labeler)
- Mergeable's size validator has an `ignore` glob for generated files. — [Mergeable size validator](https://mergeable.readthedocs.io/en/latest/validators/size.html)
- **Danger thresholds seen in the wild:** `risk` warns above 500 lines; a tutorial uses 300; a plugin's `branchSize.maxLines` defaults to 2,000 and can warn or fail; OpenStreetMap warns above 500 and auto-labels; Cerner Terra uses 1,000. — [risk README](https://cdn.jsdelivr.net/npm/risk@0.0.5/README.md); [TabNews tutorial](https://www.tabnews.com.br/ghostnetrn/como-automatizar-revisoes-de-codigo-com-o-danger-js); [danger-plugin-kirinus](https://danger.systems/js/plugins/danger-plugin-kirinus); [OSM rails-dev](https://lists.openstreetmap.org/pipermail/rails-dev/2024-August/033529.html); [Snyk danger examples](https://snyk.io/advisor/npm-package/danger/example)
- An example Claude Code review workflow labels PRs xs/s/m/l and fails anything over 800 lines with a "split into smaller, focused PRs" message. — [openskillindex PR-standards skill](https://openskillindex.com/skills/versoxbt-claude-initial-setup-pr-standards)
- OSS Insight buckets PRs into six size intervals (xs–xxl) by changed lines. — [OSS Insight](https://ossinsight.io/analyze/GraphiteEditor/Graphite)
- **CODEOWNERS:**
  - The file lives in root, `docs/` or `.github/` on the base branch, uses `.gitignore` patterns, and the last match wins.
  - Owners are auto-requested, except on drafts.
  - "Require review from Code Owners" is enabled through branch protection or rulesets.
  - Owners need write access.

  — [GitHub docs: about code owners](https://docs.github.com/en/enterprise-server@3.14/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners); [Aviator CODEOWNERS guide](https://www.aviator.co/blog/a-modern-guide-to-codeowners)
- Google: files touched matters too (200 lines across 50 files is too large), and deleting a file counts as about one line. — [Google eng-practices](https://google.github.io/eng-practices/review/developer/small-cls.html)

### Inferences
- Combining one `.gitattributes` list with the labeler's `files_to_ignore` makes "excluding lock/generated files" auditable rather than honour-based.
- Exclude **lockfiles and machine-generated artefacts only**. Do *not* exclude hand-edited Alembic migrations, tests or docs: they need review.
- A two-tier gate fits a small team: **warn plus mandatory justification above 400; fail above ~800 unless an `size-exception` label is applied by the reviewer**. This avoids blocking legitimate scaffolding PRs while keeping the default pressure.

### Gaps
- I didn't verify whether GitHub's own "Files changed" counter excludes `linguist-generated` files from the +/− totals. Prow and the labelers compute their own counts.

---

## 7. Synthesis: concrete recommendation for 믿집 (AGENTS.md §6 revision)

### Takeaway
Keep the current draft (issue-named branch, ≤2-day merge, squash merge, 1 approval, ≤400 lines excluding lock/generated files). It is consistent with Google, SmartBear, LinearB and Kubernetes guidance. Five things would tighten it:
- define the **unit** as "one issue = one concern = one self-contained PR";
- add a **target of ≤200 lines** under the 400 ceiling;
- make exclusions mechanical;
- add explicit rules for **migrations, generated code, formatting and dependency bumps**;
- add an **AI-agent PR section**: human owner, disclosure, an approver who is not the launcher, same size cap, stack/split.

### Cited Findings
Each proposed rule and its grounding:

| Rule | Grounding |
|---|---|
| **Unit of work:** one PR addresses one issue and one concern, includes its tests, and leaves `main` green (CI passes). The title describes the change in one sentence with no "and/및". Refactors, formatting and dependency bumps are never mixed with features. | [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html); [Kubernetes guide](https://www.kubernetes.dev/docs/guide/pull-requests/); [Graphite PR size guide](https://graphite.com/guides/best-practices-managing-pr-size); [Kent Beck](https://newsletter.kentbeck.com/p/tidy-first-example) |
| **Size:** target ≤200 changed lines (ideal 50–150); soft cap 400, above which the PR body must say why it can't be split; hard cap ~800 needing a reviewer-applied `size-exception` label; also warn above ~15 non-excluded files. | [SmartBear](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/); [Graphite 50 lines](https://graphite.com/blog/the-ideal-pr-is-50-lines-long); [Jellyfish](https://jellyfish.co/blog/larger-pull-requests/); [Google](https://google.github.io/eng-practices/review/developer/small-cls.html); [Microsoft usefulness study](https://www.microsoft.com/en-us/research/?p=168510) |
| **Counting:** additions + deletions, excluding (a) lockfiles (per AGENTS.md §5/§7 the stack uses pnpm and uv, so `frontend/pnpm-lock.yaml` and `backend/uv.lock`), (b) the generated OpenAPI type file `frontend/lib/backend/schema.d.ts` (AGENTS.md says it's produced by `pnpm gen:api` and must not be hand-edited), (c) snapshots and binary assets. Mark them `linguist-generated` in `.gitattributes` and mirror them in `pr-size-labeler` `files_to_ignore` (full-path globs). File deletions count as ~1 line. Alembic migrations are hand-reviewed per AGENTS.md §5, so they **count**. | [GitHub linguist-generated docs](https://docs.github.com/en/repositories/working-with-files/managing-files/customizing-how-changed-files-appear-on-github); [Prow size.go](https://raw.githubusercontent.com/kubernetes-sigs/prow/main/pkg/plugins/size/size.go); [CodelyTV labeler](https://github.com/CodelyTV/pr-size-labeler); [GitLab issue 24541](https://gitlab.com/gitlab-org/gitlab/-/issues/24541) |
| **Labels:** Prow buckets (size/XS < 10, S < 30, M < 100, L < 400, XL 400–799, XXL ≥ 800), with the L/XL boundary adapted to 400. | [Prow](https://raw.githubusercontent.com/kubernetes-sigs/prow/main/pkg/plugins/size/size.go) |
| **Splitting order for a full-stack feature:** stack or sequence ① Alembic migration + model (expand only) → ② FastAPI endpoint + pytest + regenerated TS types (same PR, so the CI drift check passes) → ③ Next.js UI → ④ contract/cleanup migration later. Use draft PRs for early feedback; consider `gh stack` (public preview) or manual base-branch stacking. | [Google splitting strategies](https://google.github.io/eng-practices/review/developer/small-cls.html); [tessl expand/contract](https://tessl.io/registry/skills/github/simstudioai/sim/db-migrate); [Unleash ADR](https://docs-new.getunleash.io/contributing/ADRs/back-end/breaking-db-changes); [GitHub stacked PR blog](https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/); [GitHub draft PR docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request) |
| **Exceptions (pre-agreed, labelled):** formatting-only or mass-rename PRs (no behaviour change, the tool command in the body, hash added to `.git-blame-ignore-revs` in a follow-up because of squash); one-time scaffolding or bootstrap; dependency bumps (`chore(deps)`, lockfile excluded); trusted codemod output. Each still gets 1 approval. | [Google exceptions](https://google.github.io/eng-practices/review/developer/small-cls.html); [pydata blame-ignore guide](https://pst-notebook-cell-styling.readthedocs.io/en/latest/community/topics/attribution.html) |
| **Lifetime and WIP:** first review within the same or next half-day; merge in ≤1 day target, 2 days max; ≤1 ready PR plus ≤1 draft per person; PRs or branches older than 2 days are raised at stand-up. GitHub flow plus squash merge, not git-flow. | [TBD site](https://trunkbaseddevelopment.com/short-lived-feature-branches/); [DORA](https://dora.dev/capabilities/trunk-based-development/); [Google latency](https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf); [Meta NudgeBot](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/); [nvie](https://nvie.com/posts/a-successful-git-branching-model/) |

**AI-agent PR rules:**
1. A named human owner (the person who ran the agent) has read the whole diff, can explain it, and replies to review comments personally.
2. Disclose the tool and scope in the PR template.
3. Agent PRs open as **Draft** until self-review is done and evidence (test, typecheck, lint output) is attached.
4. Run an AI self-review (`/code-review`, Codex `/review`) before requesting human review. It is advisory and never counts as the approval.
5. The approver must be a different human from the launcher.
6. The same size cap applies. AGENTS.md tells agents "one issue per session; if the diff would exceed ~300 lines, stop and propose a split or stack".
7. Agents never merge, and changes to `.github/workflows/`, `infra/` or secrets need explicit human sign-off.

Grounding: [Kubernetes AI guidance](https://www.kubernetes.dev/docs/guide/pull-requests/); [LLVM policy](https://llvm.org/docs/AIToolPolicy.html); [GitHub Copilot review docs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output); [Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Codex best practices](https://learn.chatgpt.com/guides/best-practices); [Faros](https://faros.ai/research/ai-acceleration-whiplash); [Swarmia](https://help.swarmia.com/features/ai-tools/cloud-agents)

### Inferences
- **Decisions to surface to the team rather than decide here:**
  - (D-a) soft cap 400 vs 300 for agent PRs;
  - (D-b) hard fail at 800 vs warn-only;
  - (D-c) keep or strip `Co-Authored-By: Claude…` trailers (Kubernetes forbids AI trailers; LLVM, the kernel and BeeWare want `Assisted-by`);
  - (D-d) adopt `gh stack` (public preview) or manual stacking;
  - (D-e) whether ADR/docs-only PRs need 1 approval or can self-merge.
- Size caps are a means. If the team routinely files `size-exception`, the problem is issue granularity at planning time: split issues, not just PRs.
- Because the evidence on merge speed is mixed, the team should judge the rule by reverts, review-comment usefulness and stale-PR count over the project, not just cycle time.

### Gaps
- There is no published evidence specific to 4–6-person bootcamp teams using AI agents. The recommendation extrapolates from industry and OSS data.
- Paths above come from AGENTS.md (loaded as context): `lib/backend/schema.d.ts`, `pnpm gen:api`, uv, and CI in `.github/workflows/ci.yml`. I didn't confirm that the lockfiles exist at exactly `frontend/pnpm-lock.yaml` and `backend/uv.lock`; check before writing globs. I modified no project files except this note.
- AGENTS.md §4 already requires `prompt`-type PRs to attach eval results. Prompt-change PRs are a natural "one concern" unit and should stay separate from code PRs.

#### Source index (every URL used above)
1. https://google.github.io/eng-practices/review/developer/small-cls.html
2. https://pasqualepillitteri.it/en/news/3317/google-code-review-guidelines-internal-principles-industry-standard
3. https://www.deployhq.com/blog/google-code-review-playbook-deployment-velocity
4. https://research.google/pubs/modern-code-review-a-case-study-at-google/
5. https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf
6. https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
7. https://www.slideshare.net/slideshow/w10-30218870/30218870
8. https://mikeconley.ca/blog/tag/loc/
9. https://lists.openstack.org/pipermail/openstack-dev/2013-August/013985.html
10. https://tekin.co.uk/2020/05/proof-your-thousand-line-pull-requests-create-more-bugs
11. https://www.microsoft.com/en-us/research/?p=168510
12. https://rdel.substack.com/p/rdel-16-what-makes-a-code-review
13. https://www.slideshare.net/mgreiler/on-to-code-review-lessons-learned-at-microsoft
14. https://www.microsoft.com/research/publication/convergent-software-peer-review-practices/
15. https://users.ece.utexas.edu/~miryung/teaching/EE379K-Spring2014/Papers/Paper%204.pdf
16. https://arxiv.org/abs/2203.05045
17. https://conf.researchr.org/details/msr-2022/msr-2022-technical-papers/21/Do-Small-Code-Changes-Merge-Faster-A-Multi-Language-Empirical-Investigation
18. https://sourcery.ai/blog/code-review-timing
19. https://jellyfish.co/blog/larger-pull-requests/
20. https://www.greptile.com/what-affects-merge-time
21. https://arxiv.org/abs/1805.10978
22. https://graphite.com/blog/the-ideal-pr-is-50-lines-long
23. https://linearb.helpdocs.io/article/q42n7g3ybk-benchmarks
24. https://linearb.helpdocs.io/article/drons87w53-managing-large-pull-requests
25. https://zporigin.leaddev.com/?p=8745
26. https://typoapp.io/blog/reduce-pr-cycle-time
27. https://www.cubic.dev/blog/does-pr-size-actually-matter
28. https://graphite.com/research/review-request-frequency
29. https://www.faros.ai/blog/are-ai-coding-assistants-really-saving
30. https://www.augmentcode.com/guides/ai-productivity-paradox-engineering-delivery
31. https://faros.ai/research/ai-acceleration-whiplash
32. https://coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report
33. https://www.theregister.com/2025/12/17/ai_code_bugs/
34. https://help.swarmia.com/features/ai-tools/cloud-agents
35. https://www.swarmia.com/changelog/2026-02-02-ai-agent-metrics/
36. https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
37. https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/
38. https://newsletter.getdx.com/p/doras-2025-research-on-the-impact
39. https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/
40. https://2022.esec-fse.org/details/fse-2022-research-papers/26/Using-Nudges-to-Accelerate-Code-Reviews-at-Scale
41. https://2022.esec-fse.org/details/fse-2022-industry/7/Understanding-Why-We-Cannot-Model-How-Long-a-Code-Review-Will-Take-An-Industrial-Cas
42. https://arxiv.org/abs/2011.12468v5
43. https://developers.facebook.com/blog/post/2022/11/15/meta-developers-workflow-exploring-tools-used-to-code/?locale=fr_FR
44. https://newsletter.pragmaticengineer.com/p/stacked-diffs
45. https://handbook.gitlab.com/handbook/engineering/workflow/iteration
46. https://ciii.frc.utn.edu.ar/gitlab/help/development/contributing/merge_request_workflow.md
47. https://about.gitlab.com/blog/iteration-and-code-review/
48. https://gitlab.com/gitlab-org/gitlab/-/work_items/30646
49. https://www.kubernetes.dev/docs/guide/pull-requests/
50. https://graphite.com/customer/shopify
51. https://www.atlassian.com/blog/git/written-unwritten-guide-pull-requests
52. https://graphite.com/guides/best-practices-managing-pr-size
53. https://www.elli.eco/en/about-elli/news/newsroom/elli-engineering/dont-do-small-pull-requests
54. https://www.theteams.kr/teams/8261/post/73201
55. https://wikidocs.net/253113
56. https://www.youngju.dev/blog/culture/2026-05-14-authoring-reviewable-pull-requests-small-prs-description-stacked-deep-dive-guide-2026
57. https://www.youngju.dev/blog/culture/2026-03-14-effective-code-review-culture-best-practices
58. https://braindetox.kr/posts/git_github_guide_04_pr_review.html
59. https://yozm.wishket.com/magazine/detail/1497
60. https://speakerdeck.com/kakao/ifkakao24-28
61. https://velog.io/@gmlstjq123/Git-Flow-VS-Github-Flow
62. https://velog.io/@jeiho/231226
63. https://arrow-season-125.notion.site/24c7e9dd351b4fcf99e7651faaa60077
64. https://newsletter.kentbeck.com/p/tidy-first-example
65. https://tidyfirst.substack.com/p/getting-untangled
66. https://henrikwarne.com/2024/01/10/tidy-first/
67. https://en.wikipedia.org/wiki/Feature_toggle
68. https://www.infoq.com/news/2016/02/featuretoggles/
69. https://git.laurivan.com/Mirrors/unleash.unleash/blame/commit/99b27061aae9d77f8fd62f1ac993b39b9ba410ce/docs/feature-toggle-types.md
70. https://mergify.com/learn/trunk-based-development/short-lived-branches
71. https://infoq.com/news/2026/04/github-stacked-prs
72. https://itbrief.co.uk/story/github-puts-stacked-pull-requests-into-public-preview
73. https://devops.com/github-brings-stacked-pull-requests-out-of-the-shadows/
74. https://docs.github.com/en/pull-requests/how-tos/stacked-pull-requests
75. https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/
76. https://graphite.com/blog/stacked-prs
77. https://graphite.com/docs/best-practices-for-reviewing-stacks
78. https://www.modular.com/blog/announcing-stack-pr-an-open-source-tool-for-managing-stacked-prs-on-github
79. https://gitlab.com/gitlab-org/gitlab-ce/-/issues/52229
80. https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request
81. https://docs.github.com/en/enterprise-server@3.14/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
82. https://tessl.io/registry/skills/github/simstudioai/sim/db-migrate
83. https://docs-new.getunleash.io/contributing/ADRs/back-end/breaking-db-changes
84. https://www.prisma.io/blog/ship-risky-schema-changes-without-a-shared-staging-database
85. https://www.red-gate.com/simple-talk/blogs/reordering-deployments-in-database-devops/
86. https://docs.github.com/en/repositories/working-with-files/managing-files/customizing-how-changed-files-appear-on-github
87. https://medium.com/@clarkbw/1f1989c09dfd
88. https://gitlab.com/gitlab-org/gitaly/-/issues/4832
89. https://gitlab.com/gitlab-org/gitlab/-/issues/24541
90. https://app.semanticdiff.com/gh/langchain-ai/langchain/commit/a9d31b30f835b73e0d9c5c246465d0266fd487fb
91. https://capgo.app/blog/openapi-typescript/
92. https://docs.agentic.scope3.com/docs/CI_LOCAL_PARITY
93. https://pst-notebook-cell-styling.readthedocs.io/en/latest/community/topics/attribution.html
94. https://github.com/eslint/markdown/pull/601
95. https://software.codidact.com/posts/293029/293051
96. https://github.com/nilearn/nilearn/issues/3653
97. https://trunkbaseddevelopment.com/short-lived-feature-branches/
98. https://dora.dev/capabilities/trunk-based-development/
99. https://www.infobip.com/developers/wp-json/wp/v2/posts/1852
100. https://getunleash.io/trunk-based-development
101. https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development
102. https://nvie.com/posts/a-successful-git-branching-model/
103. https://learn.microsoft.com/en-us/archive/blogs/technet/devops/a-git-workflow-for-continuous-delivery
104. https://docs.github.com/en/enterprise-server@3.22/get-started/using-github/github-flow
105. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github
106. https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output
107. https://docs.github.com/en/copilot/responsible-use/copilot-coding-agent
108. https://learn.chatgpt.com/guides/best-practices
109. https://code.claude.com/docs/en/best-practices
110. https://code.claude.com/docs/en/common-workflows.md
111. https://groups.google.com/a/kubernetes.io/g/dev/c/7Y9016gdFZw/m/NQbEfZQvAgAJ
112. https://kubernetes.io/blog/2026/06/26/open-source-maintainership-in-the-age-of-ai/
113. https://llvm.org/docs/AIToolPolicy.html
114. https://discourse.llvm.org/t/rfc-llvm-ai-tool-policy-human-in-the-loop/89159
115. https://www.phoronix.com/news/LLVM-Human-In-The-Loop
116. https://docs.kernel.org/next/process/coding-assistants.html
117. https://kernel.org/doc/html/v7.0/process/coding-assistants.html
118. https://feedbagel.com/post/ghostty-projects-ai-usage-policy-transparency-and-human-oversight-requirements
119. https://1984commitlog.substack.com/p/the-driver-not-the-car
120. https://arxiv.org/pdf/2605.16706
121. https://compass.hub.jupyter.org/contribute/llm/
122. https://earthaccess.readthedocs.io/en/latest/contributor/ai-policy/
123. https://www.ppsspp.org/docs/development/ai-policy
124. https://beeware-docs-tools.readthedocs.io/latest/content_test_bed/how-to/contribute/policies/ai-policy/
125. https://pages.nist.gov/fipy/en/purge_README-like/AI_POLICY.html
126. https://groups.google.com/g/blockly/c/hazyV4Uu8w0
127. https://www.ssdnodes.com/learn/ai-assisted-code-open-source-policies
128. https://linuxiac.com/netbsd-new-policy-prohibits-usage-of-ai-code/
129. https://www.theregister.com/a/5248638
130. https://www.gigazine.net/gsc_news/en/20260124-tldraw-pause-ext-contrib
131. https://codenote.net/en/posts/oss-external-pr-shutdown-2026/
132. https://codenote.net/en/posts/oss-ai-slop-contribution-policy-shift/
133. https://itsfoss.com/news/curl-closes-bug-bounty-program/
134. https://opensourcesecurity.io/2025/2025-05-curl_vs_ai_with_daniel_stenberg/
135. https://redmonk.com/kholterhoff/2026/02/26/generative-ai-policy-landscape-in-open-source/
136. https://leaddev.com/software-quality/open-source-has-a-big-ai-slop-problem
137. https://www.arxiv.org/pdf/2602.04226
138. https://arxiv.org/html/2602.02345v1
139. https://arxiv.org/html/2602.08915v1
140. https://arxiv.org/pdf/2607.21832
141. https://raw.githubusercontent.com/kubernetes-sigs/prow/main/pkg/plugins/size/size.go
142. https://beta.pkg.go.dev/sigs.k8s.io/prow/pkg/plugins/size
143. https://github.com/CodelyTV/pr-size-labeler
144. https://app.stepsecurity.io/action-advisor/CodelyTV/pr-size-labeler
145. https://github-redirect.dependabot.com/coverwallet/pr-labeler
146. https://github.com/srvaroa/labeler
147. https://mergeable.readthedocs.io/en/latest/validators/size.html
148. https://cdn.jsdelivr.net/npm/risk@0.0.5/README.md
149. https://www.tabnews.com.br/ghostnetrn/como-automatizar-revisoes-de-codigo-com-o-danger-js
150. https://danger.systems/js/plugins/danger-plugin-kirinus
151. https://lists.openstreetmap.org/pipermail/rails-dev/2024-August/033529.html
152. https://snyk.io/advisor/npm-package/danger/example
153. https://openskillindex.com/skills/versoxbt-claude-initial-setup-pr-standards
154. https://ossinsight.io/analyze/GraphiteEditor/Graphite
155. https://www.aviator.co/blog/a-modern-guide-to-codeowners

Note on source depth: about 35 of these were fetched in full (Google page and PDF, SmartBear, Graphite, Jellyfish, Sourcery, arXiv abstracts, GitHub docs and blog, Codex/Claude Code docs, Kubernetes guide, LLVM policy, Prow source, CodelyTV README, TBD site). The rest were used through search-result snippets and are cited only for the specific claim shown in the snippet.
