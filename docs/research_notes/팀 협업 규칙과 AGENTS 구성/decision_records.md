# Decision records for a small student team (ADR vs RFC/design doc vs issue), researched 2026-10-29

Scope: how software teams record decisions (ADRs, RFCs, design docs, decision logs), and a concrete recommendation for 믿집. 믿집 is an SKN34 team of about 4–6 people on GitHub. It already has `docs/adr/0001–0003` (Korean fields: 상태, 결정한 사람, 바꾸는 것, 맥락, 결정, 다른 안, 결과), `docs/design/*.md` with numbered open decisions (AR1–AR13, T1–T4, AI1–AI6), and `docs/status.md` as its only progress log. AGENTS.md says irreversible decisions go to `docs/adr/` and progress goes only to `docs/status.md`. AI coding agents also read these docs.

Method note: WebSearch hit its shared per-turn budget partway through. The remaining sources are direct fetches of primary pages whose URLs were already known. About 110 distinct URLs were consulted; the full list is at the end of the last section. Korean company blogs (Kakao, Toss, 우아한형제들) on ADRs were not found before the budget ran out (see Gaps).

---

## 1. ADR formats and tooling in 2025–2026 (Nygard, MADR 4, Y-statements, Tyree/Akerman, tools, AWS/Google/Microsoft/GDS/ThoughtWorks)

### Takeaway
Nygard's five-part ADR (2011) is still the most-used format. MADR 4.0.0 (2024-09-17) is the current maintained Markdown template: full, minimal and bare variants, plus optional YAML front matter for status, date, decision-makers, consulted and informed. Big-vendor guidance (AWS 2022/2025, Google Cloud 2024, Microsoft 2026, UK GDS 2026, UK DSIT/GDS framework 2025) agrees on the core: one decision per short Markdown file in the repo, with context, options, decision and consequences, and a status lifecycle that supersedes old records rather than editing them. Tooling is optional and mostly stale. Plain files plus an index are enough for a small team.

### Cited Findings
**Nygard original (2011)**
- Nygard's format: Title (short noun phrase), Context (neutral statement of the forces), Decision ("We will…", active voice), Status (proposed / accepted / deprecated / superseded, with a reference to the replacement), Consequences ("all consequences", positive, negative and neutral). Files live at `doc/arch/adr-NNN.md`, numbered sequentially and never reused. "The whole document should be one or two pages long." Write full sentences, not bullet fragments. — [Nygard 2011, Cognitect](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- Nygard's rationale: "small, modular documents have at least a chance at being updated". Without recorded reasons, new developers can only blindly accept or blindly reverse past decisions. An ADR is "a conversation with a future developer". Reversed decisions stay in place, marked superseded. — [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- The arc42 FAQ restates the same five parts and stresses listing negative and neutral consequences. — [arc42 FAQ C-9-3](https://faq.arc42.org/questions/C-9-3/)

**MADR (current: 4.0.0, released 2024-09-17; no later release on the releases page as of 2026-10)**
- The 4.0.0 full template has front matter `status`, `date`, `decision-makers`, `consulted`, `informed`. Headings: Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome (→ Consequences, → Confirmation), Pros and Cons of the Options, More Information. Status examples: `proposed | rejected | accepted | deprecated | … | superseded by ADR-0123`. — [MADR 4.0.0 adr-template.md](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md)
- The 4.0.0 minimal template has only the Title, Context and Problem Statement, Considered Options, and Decision Outcome → Consequences ("Good, because… / Bad, because…"). It has no front matter. — [MADR 4.0.0 minimal](https://github.com/adr/madr/blob/4.0.0/template/adr-template-minimal.md)
- Changes in 4.0.0-beta: added bare and minimal templates, renamed "Validation" to "Confirmation" and "Deciders" to "Decision Makers", quoted the status value for YAML, and removed the ADR link from `status`. 3.0.0 had merged positive and negative consequences into one "Consequences" section, added `consulted`/`informed`, and moved the default folder to `docs/decisions`. — [MADR releases](https://github.com/adr/madr/releases)
- MADR file naming is `NNNN-title-with-dashes.md`, lowercase with dashes, in a `decisions/` folder. Large projects can use per-category subfolders with numbering local to each folder. Confirmation says how compliance is checked (review, tests such as ArchUnit) and is optional. — [adr.github.io/madr](https://adr.github.io/madr/)
- Zimmermann's MADR primer: Context, Considered Options, Decision Outcome and Consequences are the core. Drivers, Pros/Cons, Confirmation and More Information are supplemental. Keep the context to a few sentences, list the chosen option first, avoid pseudo-alternatives, and record confidence and a revisit date under More Information. Pick a format early and stick to it. — [Zimmermann, MADR primer (2022)](https://www.ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html)

**Y-statements**
- Short form: "In the context of <use case>, facing <concern> we decided for <option> to achieve <quality>, accepting <downside>." The long form adds "and neglected <other options>" and "because <rationale>". — [adr.github.io ADR templates](https://adr.github.io/adr-templates/)
- Zimmermann created Y-statements because richer templates were too costly to maintain and sponsors wanted compact summaries. He presented them at SATURN 2012 and later in IEEE Software/InfoQ. The name comes from "Y", pronounced "why". A "because" clause may be added. — [Zimmermann, AD making & justifications (2020, updated 2026-09-12)](https://www.ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html)
- adr.github.io credits Y-statements to "Sustainable Architectural Decisions" (Zdun et al.) and links a WICSA 2015 comparison of seven templates. — [adr.github.io](https://adr.github.io/)

**Tyree/Akerman and other templates**
- Joel Parker Henderson's catalog lists Nygard ("simple and popular"), Tyree & Akerman ("more sophisticated"), Alexandrian, Business case (costs/SWOT), MADR, Planguage, and others (EdgeX, arc42, Merson, Zimmermann Y-statements, lean ITDs). Advice: name files with a present-tense imperative verb phrase such as `choose-database.md`, record one decision per ADR, and timestamp items that change, such as costs. — [joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)
- The AWS example ADR adds a **Compliance** section (how the rule is enforced, e.g., protected branches, one approval) and a **Notes** section (author, version, changelog) to Title/Status/Date/Context/Decision/Consequences. — [AWS Prescriptive Guidance appendix](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/appendix.html)
- The Harmel-Law Advice Process template adds an **Advice** section (who advised, when, what) and lists options with the chosen one first. Its statuses are Draft, Proposed, Adopted, Superseded, Retired. — [Harmel-Law, Scaling the Practice of Architecture, Conversationally (2021)](https://martinfowler.com/articles/scaling-architecture-conversationally.html)

**Vendor and government guidance**
- **AWS Prescriptive Guidance (March 2022)**: an ADR "becomes immutable" when accepted, and a new ADR supersedes it. The owner submits it as **Proposed** and runs a review meeting that starts with 10–15 minutes of silent reading. Outcomes are Accepted, Rework (stays Proposed) or Rejected (with the reason recorded, "to prevent future discussions on the same topic"). On acceptance the owner adds timestamp, version and stakeholders. Code reviewers link the ADR when a change violates it. — [AWS ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html); dated March 2022 per [AWS guide (Korean)](https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/architectural-decision-records/welcome.html) and [InfoQ 2022-06-07](https://www.infoq.com/news/2022/06/aws-adr-guide/)
- AWS best practices: any member can own an ADR, history is kept (old ADR marked Superseded), regular reviews make ADRs "stabilize in two or three sprints" on greenfield projects, storage is central (Git or wiki) and linked from the project's main docs page, and non-compliant legacy code becomes tech-debt tasks. — [AWS ADR best practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html)
- AWS Architecture Blog (2025-03-20) draws on 200+ ADRs from teams of fewer than 10 up to 100 people. Its advice: 30–45-minute meetings, a readout style with 10–15 minutes of reading and written comments, fewer than 10 participants, one decision per ADR, design exploration in a separate design document referenced from the ADR, every comment resolved, one to three readouts ("most decisions are reversible"), and the new ADR linked from the old one. — [AWS Architecture Blog, Master ADRs (2025)](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- **Google Cloud (last updated 2024-08-16)**: write an ADR when no existing basis for a decision exists, when the team's solution isn't documented anywhere accessible, or when weighing two or more options. "Store your ADRs close to your application code." Suggested sections: authors/team, context/problem, functional and non-functional requirements, critical user journey, options, decision and rationale, optional timestamp. Revisions record the previous decision and the reason for the change. — [Google Cloud ADR overview](https://docs.cloud.google.com/architecture/architecture-decision-records); Korean section names (작성자 및 팀, 컨텍스트 및 해결하고자 하는 문제, …) in [the Korean version](https://docs.cloud.google.com/architecture/architecture-decision-records?hl=ko)
- **Microsoft Azure Well-Architected (ms.date 2026-04-10)**: include "only choices that affect the system's structure, key quality attributes, or are difficult to reverse". "The ADR serves as an append-only log. Don't go back and edit accepted records." Link superseding records to each other, record the decision's **confidence level**, give multi-phase decisions one record per phase, keep records "pithy, assertive, on-topic, and factual", and do not turn records into design guides (link supplemental docs instead). — [Microsoft Learn ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record); Korean translation (추가 전용 로그, 신뢰도 수준, 제안됨/수락됨/대체됨) in [ko-kr version](https://learn.microsoft.com/ko-kr/azure/well-architected/architect-role/architecture-decision-record)
- **UK GDS Way (reviewed 2026-03-05)**: use the Nygard format in version control. On GitHub, *the PR status is the proposed state*, so no explicit status is needed, and an ADR in `main` is treated as accepted. An ADR may be updated for clarifications or added consequences. If the decision was never implemented, it may be changed with reviewer agreement. If it was partly implemented, a new ADR is needed. A superseded ADR gets "Status: superseded" under its heading and a link to the new one. An ADR "is not a full description of a system". — [GDS Way: Documenting architecture decisions](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html)
- **UK DSIT/GDS ADR framework (2025-11-04)**: fields are Title, Date, Status, Context, Decision, Consequences, Stakeholders consulted, and Links to supporting documents. Team-level decisions are made locally with no extra approval unless they affect other teams or shared platforms. — [gov.uk ADR framework](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework)
- GOV.UK and MoJ repos use Nygard plus adr-tools in practice. Each starts with "0001 record architecture decisions" (2021, 2023). MoJ publishes its ADRs openly ("making things open makes things better"). — [govuk-infrastructure ADR 0001](https://docs.publishing.service.gov.uk/repos/govuk-infrastructure/architecture/decisions/0001-record-architecture-decisions.html); [MoJ Observability ADR 0001](https://observability-platform.service.justice.gov.uk/architecture-decision-records/0001-record-architecture-decisions.html); [Hackney Data Platform ADR 001](https://playbook.hackney.gov.uk/Data-Platform-Playbook/architecture-decisions/records/record-architecture-decisions)
- **ThoughtWorks Radar**: "Lightweight ADRs" went Trial (Nov 2016) → Adopt (Nov 2017, May 2018), with a preference for source control over wikis. *Older fact*: the blip is no longer on the current Radar. — [TW Radar](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- **Martin Fowler bliki (2026-03-24)**: an ADR is "just a couple of pages", typically one, written inverted-pyramid with the most important material first. Include serious alternatives, confidence, and the product-context changes that would trigger re-evaluation. Once accepted it is never reopened; a new ADR supersedes it. Store in `doc/adr`, monotonic numbers, e.g., `0001-HTMX-for-active-web-pages`. "Writing… clarifies thinking", especially in groups. — [Fowler, ArchitectureDecisionRecord](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html)
- Microsoft's Engineering Playbook keeps a `decision-log.md` table summarizing ADRs next to `doc/adr`. It suggests submitting an ADR as a PR in Proposed and switching it to Accepted before merge, and using the work-item ID to avoid number clashes when people write in parallel. — [MS Code-With Engineering Playbook: Decision log](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/decision-log/)

**Tooling (status as of 2026)**
- adr.github.io tooling list: adr-tools (bash, Nygard; many ports), `adrs` (Rust), log4brains (static site, MADR 2.1.2, no numbers in filenames), ADR Manager (web UI plus a VS Code extension, MADR 2.1.2), adr-log (index generator, marked unmaintained), pyadr, dotnet-adr, Backstage ADR plugin (MADR 2.1.2/3.x), adr-viewer, Talo, commercial tools (Loqbooq, ReflectRally, adr.zone). Several tools are explicitly unmaintained. — [adr.github.io/adr-tooling](https://adr.github.io/adr-tooling/)
- adr-tools commands: `adr init` (default `doc/adr`), `adr new`, and `adr new -s <n>`, which supersedes ADR n and updates its status. 5.7k stars and 38 open PRs; no releases listed. — [npryce/adr-tools](https://github.com/npryce/adr-tools)
- log4brains: docs-as-code static site, MADR default, avoids numbered filenames "to avoid git merge issues", 1.6k stars, no release dates shown. — [thomvaill/log4brains](https://github.com/thomvaill/log4brains)
- ADR Manager began as a University of Stuttgart undergraduate research project. It manages only MADRs in `docs/adr` of GitHub repos via OAuth. — [adr/adr-manager](https://github.com/adr/adr-manager)
- pyadr is "pre-alpha". It uses an `XXXX-` placeholder name while proposed and renames to the next free ID on accept/reject (avoids number races). It has `pyadr toc` for `index.md`; deprecate/supersede are not implemented. — [pyadr](https://github.com/opinionated-digital-center/pyadr)
- adr.github.io news: the Azure Well-Architected Framework added ADRs (2024-11-10), and a JavaLand 2026 talk covered ADR/MADR/eADR (2026-03-10). — [adr.github.io](https://adr.github.io/)

### Inferences
- 믿집's current ADR shape (상태 · 결정한 사람 · 바꾸는 것 · 맥락 · 결정 · 다른 안 · 결과) already equals **MADR-minimal + Nygard**. 결정한 사람 maps to MADR `decision-makers`, 다른 안 to Considered Options, and 바꾸는 것 to a supersedes/amends link. Switching to the full MADR or Tyree/Akerman would add weight without benefit for a 4–6-person, few-week project.
- Compared with MADR 4 and Microsoft, the fields worth adding are a separate **date**, a **back-link on the replaced ADR**, and **links to issue/PR**. **Confirmation** (how we check it, e.g., a test or lint rule) and **confidence / revisit trigger** are optional. These are cheap and help both humans and AI agents.
- No tool is needed. adr-tools, log4brains and pyadr are aging or pre-alpha. A hand-maintained `docs/adr/README.md` index is sufficient at 3–15 ADRs.

### Gaps
- Exact field list of the Tyree & Akerman template (IEEE Software 2005): the catalog page links it, but the template file could not be fetched (404). It is described only as "more sophisticated".
- The WICSA 2015 seven-template comparison was not read directly.
- Whether log4brains or adr-tools had releases in 2025–2026 could not be confirmed (release sections were empty on the fetched pages).

---

## 2. RFC and design doc practices (Google, Uber, Squarespace, Sourcegraph, HashiCorp, Rust, React, PEP, Oxide, KEP, Go, Swift, Ember, TC39), and what suits a small team

### Takeaway
RFCs and design docs are for exploring a problem *before* deciding: alternatives, open questions and review. ADRs record the outcome. Spotify's flow states it most clearly: big change → RFC → ADR; small change → ADR directly. What transfers to a small team is cheap: a short template with Goals/Non-goals, Alternatives and Unresolved questions; a named decider plus a review deadline; review in a PR; and an explicit "decide" step. Heavy machinery (councils, FCP bots, multi-stage pipelines) does not transfer.

### Cited Findings
**Google design docs (Malte Ubl, 2020; older fact but still the canonical description)**
- Sections: Context and scope; Goals and **non-goals**; the actual design; **Alternatives considered** ("one of the most important sections"); Cross-cutting concerns (security, privacy, observability). 10–20 pages for large projects, a **"mini design doc" of 1–3 pages** for incremental work. Skip the doc when the solution is unambiguous, when it would just be an implementation manual, or when prototyping is faster. Lifecycle: create → review → implement and iterate (update the doc or write amendments) → maintain/learn. — [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)

**Uber and industry surveys (Orosz)**
- Uber's lightweight plan doc lists approvers at the top, is mailed to engineers (later per-domain lists), and uses templates that grew from questions reviewers kept asking. If the team already agrees, writing it down "should take only a few hours". Orosz advises adopting an RFC habit while the team is small. (First published 2018-10-03, updated 2022-09-21.) — [Orosz, Scaling Engineering Teams via RFCs](https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/)
- At 2,000+ engineers Uber hit noise (hundreds of RFCs a week), unclear scope (each team chose when an RFC was needed) and poor discoverability (Google Docs scattered across folders). Fixes: a searchable tool, lightweight versus heavy templates, and tiered review. "For small changes: don't bother. Just make the change." "The effort to write an RFC should be proportionate to the complexity of the task." (2022-06-21) — [Pragmatic Engineer, RFCs and design docs](https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs)
- Company terminology survey (2022, updated 2024-02-07). Spotify, Glovo and Peloton use both RFCs/design docs and ADRs; Wise and Comcast use ADRs; Stedi has an RFC plus a Decision Record; Amazon uses PR/FAQ docs; PRDs often sit alongside engineering docs. — [Orosz, Companies using RFCs or design docs](https://blog.pragmaticengineer.com/rfcs-and-design-docs/)

**Squarespace, HashiCorp, Sourcegraph, Attentive, PointFive**
- Squarespace (2019): approvers answer **"yes" or "not yet"**, never "no", and can approve conditionally ("Yes, if…"). The free-text status says what kind of review the author wants. Architecture Review is a one-hour session with at most ~10 people: 50 minutes of discussion, then 10 minutes in which each person says whether they are comfortable. Meeting notes are linked as the approval record. — [Squarespace, The Power of "Yes, if"](https://engineering.squarespace.com/blog/2019/the-power-of-yes-if); [Reilly announcement](https://noidea.dog/blog/yes-if)
- HashiCorp RFC header: Summary, Created, Status (**WIP / In-Review / Approved / Obsolete**), Owner, Contributors, PRD link, Approvers. Body: Overview ("one or two paragraphs"), Background (a newcomer can follow the links), Proposal, **Abandoned Ideas** (so others don't repeat the same path), Example implementation/UX/UI. — [HashiCorp RFC template](https://www.hashicorp.com/how-hashicorp-works/articles/rfc-template)
- Sourcegraph RFC metadata: Recommender, Date, Status (starts WIP), **Decider**, Input providers, **Approvers each with a review deadline**, Approvals, Team. Sections: Summary (write last), Background (facts only), Problem (why now), Proposal, Definition of success. — [Sourcegraph RFC template (Slab copy)](https://slab.com/library/templates/sourcegraph-rfc-template-proposal/). The handbook URL now redirects to Notion: [handbook.sourcegraph.com/communication/rfcs](https://handbook.sourcegraph.com/communication/rfcs)
- Attentive (2026-07-06): write an RFC when the problem is non-trivial, has cost implications, uncertain scale, or touches teams you don't work with daily, "once the design has concrete shape but before implementation details are locked in". Statuses: Draft / In Review / Changes Requested / Approved-Closed / Blocked-Discarded. Default review window is **one week**, with RACI roles. Avoid "perpetual drafts", and split RFCs longer than about 10–12 pages. — [Attentive, RFC process for teams](https://tech.attentive.com/articles/rfc-process-for-teams)
- PointFive (2025-03-18): a **Mini RFC** (problem, solution, implementation details, success metrics, **open questions**) can be "written in under an hour" and reviewed asynchronously. The full Tech-Spec RFC is reserved for big projects. — [PointFive, tailoring RFCs](https://www.pointfive.co/engineering/engineering-blog/writing-technical-specifications-the-art-of-tailoring-rfcs)
- Vimeo/Increment (2021): a small, distributed team added estimated size, required skills, a "definition of done", and an **unsolved questions** section ("lowers the barrier to starting a draft"). It tracked RFCs with a GitHub project board, labels and Slack, and proposed the process itself as RFC #1. — [Increment, Planning with RFCs](https://increment.com/planning/planning-with-requests-for-comments/)

**Open-source processes**
- Rust: RFCs are for "substantial" changes, not refactors or minor additions. Copy `0000-template.md` and **rename the file to the PR number**. A Final Comment Period with disposition merge/close/postpone lasts 10 days. An accepted RFC is "active" (not a promise to implement), gets a tracking issue, and is not substantially changed afterwards; substantial changes need a new RFC. — [Rust RFCs README](https://github.com/rust-lang/rfcs/blob/master/README.md)
- The Rust template's **Unresolved questions** splits open items into: to resolve before merge, to resolve during implementation, and out of scope. It also has "Rationale and alternatives", "Prior art" and "Future possibilities". — [Rust 0000-template.md](https://github.com/rust-lang/rfcs/blob/master/0000-template.md)
- React: RFCs are for new API surface, removals and new conventions. There is a 3-day final comment period, merge = active, and active RFCs *can* be modified in follow-up PRs to stay in sync. — [reactjs/rfcs](https://github.com/reactjs/rfcs)
- PEP 1: one key proposal per PEP. Statuses: Draft, Active, Accepted, Provisional, Deferred, Rejected, Withdrawn, Final, Superseded. Headers include Author, **PEP-Delegate** (the named decider), Discussions-To, Replaces, Superseded-By, and **Resolution** (a link to the decision post). Resolved PEPs are **historical documents**; current docs live elsewhere. — [PEP 1](https://peps.python.org/pep-0001/)
- Oxide RFDs: "timely rather than polished". States are prediscussion, ideation, discussion, published, committed, abandoned. A 4-digit number is reserved, with a branch per RFD and discussion in a PR (3–5 business days suggested). Published RFDs can be corrected via new PRs, and the process changes itself through RFD 1. — [Oxide RFD 1](https://rfd.shared.oxide.computer/rfd/0001); tooling (CSV metadata API, short URLs, chat bot, rendered site) in [Oxide blog 2020-07-24](https://oxide.computer/blog/rfd-1-requests-for-discussion)
- Kubernetes KEPs keep YAML metadata (title, **status**, authors, owning-sig, reviewers, approvers, creation-date, last-updated, see-also, replaces, superseded-by). Statuses: provisional, implementable, implemented, deferred, rejected, withdrawn, replaced. The metadata exists for tooling and filtering, presubmit checks validate it, and KEP names carry the tracking issue number. — [KEP-0000](https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md); [KEPs README](https://github.com/kubernetes/enhancements/blob/master/keps/README.md)
- Go: **issue first**, with a design doc only if the discussion asks for one. Docs are named `design/NNNN-shortname.md` with the issue number. The review committee meets weekly. Labels: Incoming → Active → Likely Accept/Decline (~1-week final comment) → Accepted/Declined, or **Hold** while information is missing. — [golang/proposal](https://github.com/golang/proposal/blob/master/README.md)
- Swift Evolution: a review manager, at least 10 days of review, and outcomes Accepted / Accepted with revisions / Returned for revision / Rejected / Withdrawn / Implemented. — [Swift Evolution process](https://github.com/swiftlang/swift-evolution/blob/main/process.md)
- Ember stages: Proposed → Exploring → Accepted → Ready for Release → Released → Recommended, plus Discontinued/Closed. Merging opens an automatic "advance" PR to track implementation. — [emberjs/rfcs](https://github.com/emberjs/rfcs)
- TC39 stages 0–4 (with 2.7) are driven by a **champion**. — [TC39 process](https://tc39.es/process-document/)
- Mozilla Android Components: an RFC is for changes touching multiple components or public APIs, with async PR discussion. Accepted = merged; rejected = PR closed and revivable later. No deadline is specified. — [mozac RFC 0001](https://mozac.org/rfc/0001-rfc-process)
- Giant Swarm keeps the RFC `state` (review/approved/declined/obsolete) in a YAML header checked by CI. The process "does not dictate how" the decision is reached; the author sets the state before merge. — [Giant Swarm handbook](https://handbook.giantswarm.io/docs/rfcs/decision-process)
- Cosmos SDK: "An ADR documents a decision that has already been made", whereas "An RFC is used to replace synchronous communication." Proposed ADRs are merged with their open issues noted, and faulty ones are merged as Rejected. Statuses: Draft, Proposed, Last Call, Accepted, Rejected, Superseded, Abandoned, plus Implemented/Not Implemented. Write in the present tense and avoid the first person. — [Cosmos SDK ADR process](https://docs.cosmos.network/sdk/v0.53/build/architecture/PROCESS)

**RFC → ADR relationship and critiques**
- Spotify (2020): backfill undocumented decisions (often found in peer review when a competing pattern appears). For a big change with no "blessed" solution → write an RFC, then an ADR for its outcome. For a small change → write an ADR directly. "Almost always!" write one, and keep small ones lightweight. — [Spotify Engineering, When should I write an ADR](https://engineering.atspotify.com/2020/4/when-should-i-write-an-architecture-decision-record); [InfoQ summary](https://www.infoq.com/news/2020/04/architecture-decision-records/)
- AWS: keep design exploration in a separate design doc referenced from the ADR. — [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/). Konishi: "the design doc as working material and the ADR as the output". — [Konishi, ADR operational patterns (2026)](https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html)
- Kaplan-Moss (2023-12-01): RFCs are "document and discuss" with no decide step. An undecided RFC defaults to "no". They reward exhaustion (overlong docs) and ignore expertise and power structures. The fix is "document, discuss, and then decide", with an explicit model (hierarchical, vote, or real consensus). — [Kaplan-Moss, Against RFCs](https://jacobian.org/2023/dec/1/against-rfcs/)
- brandur (2023-03-11): Heroku's RFCs stalled on contentious topics, and Stripe's committee favored high-status engineers. He recommends defaulting to "yes", low-touch reviews, minimal overhead, and a respected tiebreaker. — [brandur, RFCs and review councils](https://brandur.org/fragments/rfcs-and-review-councils)

### Inferences
- 믿집's `docs/design/*.md`, with numbered open decisions, already is an RFC/design-doc layer. What is missing, per Kaplan-Moss, Sourcegraph, DACI and PEP, is a **named decider and a deadline per open decision**, plus an explicit "decided → ADR NNNN" pointer when it closes.
- Transferable pieces: Go's "issue first, doc only if needed"; Rust's Unresolved-questions split; Google's Non-goals and Alternatives; Squarespace's "yes / not yet / yes, if"; and Rust/PEP's rule that resolved proposals are history, with living rules in AGENTS.md.
- Not transferable: review councils, FCP bots, multi-stage (Ember/TC39/KEP) pipelines, and mailing-list distribution.

### Gaps
- Kakao, Toss and 우아한형제들 internal RFC or design-doc practices: no primary Korean company blog post was retrieved before the search budget ran out (see section 4 Gaps).
- The Uber RFC section of the Pragmatic Engineer article is paywalled; only the public part was read.

---

## 3. Product (PO) decision logs vs technical ADRs, open questions and decision backlogs, decision owner and deadlines

### Takeaway
Product decision logs (DACI, Aha, LaunchNotes) and ADRs share a core: what, who decided, when, why, and options. Product frameworks add two things ADR templates usually lack: **one named Approver** and a **due date** for decisions still open. Architecture guidance adds *when* a decision is ready (Zimmermann's START: stakeholders known, "most responsible moment", at least two options, requirements, template). For a small team, open questions belong next to the proposal (Rust "Unresolved questions", HashiCorp "Abandoned ideas", PointFive "Open questions"), each with an owner and a deadline. Decisions that turn out irreversible get promoted to an ADR.

### Cited Findings
- DACI: Driver (drives to a decision by the target date), **only one Approver**, Contributors (advise, don't vote), Informed. The decision doc header holds status, impact, people, **due date** and outcome. Body: background, data, decision factors, an options table (pros, cons, cost), action items with owners, and the outcome. Best for 3–6 people, about 60 minutes. — [Atlassian Team Playbook: DACI](https://www.atlassian.com/team-playbook/plays/daci); [Confluence DACI template](https://www.atlassian.com/software/confluence/templates/decision)
- Aha decision log: per decision, record date, category, owner/stakeholders, options, rationale, impact, and roadblocks or delays. Decide upfront which decision types to log and which to skip, log chronologically as decisions happen, and review periodically. — [Aha! decision log template](https://www.aha.io/roadmapping/guide/templates/create/decision-log)
- LaunchNotes: a decision log is a "single source of truth for all decisions", with fields description, decision maker, date, rationale, impact. — [LaunchNotes glossary](https://www.launchnotes.com/glossary/decision-log-template-in-product-management-and-operations)
- MADR 3.0.0-beta was renamed "Markdown *Any* Decision Records", and 4.0 reverted the name while noting MADR can still record any decision. MADR's `consulted`/`informed` fields map to RACI/DACI. — [adr.github.io/madr](https://adr.github.io/madr/); Zimmermann also argues for "ADR = Any Decision Record?" (linked from [AD practices](https://adr.github.io/ad-practices/))
- Fowler (2026): the broader practice of short decision records is useful outside software architecture. — [Fowler bliki](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html)
- Incident.io uses RFCs for non-technical proposals too, and Stedi pairs RFCs with a separate "Decision Record" template. — [Orosz company list](https://blog.pragmaticengineer.com/rfcs-and-design-docs/)
- Zimmermann's **START Definition of Ready**: **S**takeholders identified (RACI); **T**ime: the "most responsible moment" has come; **A**lternatives: at least two; **R**equirements/drivers documented; **T**emplate chosen. — [Zimmermann, Definition of Ready (2023)](https://ozimmer.ch/practices/2023/12/01/ADDefinitionOfReady.html)
- Zimmermann's **ecADR Definition of Done**: Evidence (PoC/spike/expert), Criteria (at least two alternatives compared), Agreement (peer and team challenged it), Documentation (lean template), and Realization/Review plan, which includes *when the decision will be revisited or expire*. Effort scales with cost and risk. — [Zimmermann, Definition of Done (2020)](https://www.ozimmer.ch/practices/2020/05/22/ADDefinitionOfDone.html)
- Sourcegraph RFCs name a **Decider** and give **each approver a review deadline**. — [Sourcegraph RFC template](https://slab.com/library/templates/sourcegraph-rfc-template-proposal/)
- PEP-Delegate is the person appointed to make the final call, and a Resolution link points to the decision. — [PEP 1](https://peps.python.org/pep-0001/)
- Go's **Hold** status covers proposals paused for missing information. Rust "postponed" means the RFC is closed but may be reopened. — [Go proposal](https://github.com/golang/proposal/blob/master/README.md); [Rust RFCs](https://github.com/rust-lang/rfcs/blob/master/README.md)
- Rust's Unresolved questions (before merge / before stabilization / out of scope); PointFive's Mini RFC "open questions"; Increment's "unsolved questions" section. — [Rust template](https://github.com/rust-lang/rfcs/blob/master/0000-template.md); [PointFive](https://www.pointfive.co/engineering/engineering-blog/writing-technical-specifications-the-art-of-tailoring-rfcs); [Increment](https://increment.com/planning/planning-with-requests-for-comments/)
- Cosmos: a merged Proposed ADR "should clearly document outstanding issues either in ADR document notes or in a GitHub Issue". — [Cosmos SDK ADR process](https://docs.cosmos.network/sdk/v0.53/build/architecture/PROCESS)
- GDS: review unimplemented ADRs regularly, and an issue tracker can help track follow-through. — [GDS Way](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html)
- Bezos's Type 1 (one-way door, irreversible: slow, deliberate, consultative) vs Type 2 (two-way door: decided "quickly by high judgment individuals or small groups"). The risk is applying the heavy process to everything. Decide with about 70% of the desired information (2015/2016 letters, as relayed). — [Kindel, One-way and two-way doors (2019)](https://blog.kindel.com/2019/06/27/one-way-and-two-way-doors/)
- UK framework: team-level decisions are made locally with no extra approval unless they affect other teams or shared platforms. — [gov.uk ADR framework](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework)
- AWS: a rejected ADR records why, "to prevent future discussions on the same topic". — [AWS ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)

### Inferences
- In 믿집, PO decisions that change rules agents and code must follow (e.g., ADR 0002, "업체가 견적서를 써서 낸다", decided by PO) belong in `docs/adr/`, the same as technical ones. Reversible product choices (UI wording, ordering, colors) stay in issues or design docs. The one-way/two-way-door test is the dividing line, which matches AGENTS.md "되돌리기 어려운 결정은 docs/adr/".
- Each open item in `docs/design/*.md` (AR1–AR13, T1–T4, AI1–AI6) should carry four short attributes: **결정할 사람** (one person or role, per DACI), **기한** (date), **상태** (열림 / 보류 / 결정), and, once closed, **어디에 남겼나** (ADR NNNN, or "design doc only, reversible"). This covers Sourcegraph's Decider plus deadline, DACI's due date, Go's Hold, and PEP's Resolution link without a new file.
- Keeping open decisions inside the design docs, rather than in a separate backlog file, respects AGENTS.md's "progress only in docs/status.md". `status.md` can then list only *blocked-by-decision* items by ID with no copies (a choice for the team; see section 6).

### Gaps
- No empirical study compares product decision logs with technical ADRs in small teams. The evidence is vendor templates and practitioner advice.
- Recommended due-date conventions for student or bootcamp teams were not found. A 2–3-day window is an inference from AGENTS.md's 2-day branch rule and Attentive's one-week default.

---

## 4. Lifecycle and maintenance: statuses, superseding, PR review, sprawl, index, Korean language and length

### Takeaway
The consensus lifecycle is Proposed → Accepted → (Deprecated | Superseded by NNNN), with Rejected optional. Accepted ADRs are append-only and a change gets a new ADR with two-way links. GDS and Oxide allow clarifications, and Joel Parker Henderson reports that living documents with dated updates worked better. On GitHub the PR is the review venue: GDS treats the open PR as "proposed" and main as "accepted". Teams find ADRs later through an index file, in-file status, and pointers from code and from AGENTS.md. Sprawl is prevented by a significance bar (hard to reverse, cross-cutting, security or operations). Keep each ADR to one page; split or link anything longer.

### Cited Findings
**Statuses compared**
- Nygard: proposed, accepted, deprecated, superseded. — [Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- MADR 4: proposed, rejected, accepted, deprecated, superseded by ADR-NNNN. — [MADR template](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md)
- AWS: Proposed, Accepted, Rejected, Superseded; Korean: 제안됨, 수락됨, 거부됨, 대체됨, with ADR 소유자 for owner and 결정 로그 for decision log. — [AWS ko ADR 프로세스](https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- Microsoft: Proposed, Accepted, Superseded (Korean 제안됨/수락됨/대체됨). — [MS Learn ko-kr](https://learn.microsoft.com/ko-kr/azure/well-architected/architect-role/architecture-decision-record)
- MS Engineering Playbook: Proposed, Accepted, Deprecated, Superseded. — [Decision log](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/decision-log/)
- KEP (provisional → implementable → implemented; deferred, rejected, withdrawn, replaced), PEP (9 statuses), Cosmos (consensus status plus implementation status), HashiCorp (WIP / In-Review / Approved / Obsolete), Giant Swarm (review / approved / declined / obsolete), Harmel-Law (Draft / Proposed / Adopted / Superseded / Retired). — [KEP-0000](https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md); [PEP 1](https://peps.python.org/pep-0001/); [Cosmos](https://docs.cosmos.network/sdk/v0.53/build/architecture/PROCESS); [HashiCorp](https://www.hashicorp.com/how-hashicorp-works/articles/rfc-template); [Giant Swarm](https://handbook.giantswarm.io/docs/rfcs/decision-process); [Harmel-Law](https://martinfowler.com/articles/scaling-architecture-conversationally.html)

**Immutability vs living documents (conflicting views)**
- Immutable / append-only: AWS ("becomes immutable"), Microsoft ("append-only log… Don't go back and edit accepted records"), Fowler ("never reopened or edited"), BrainGrid ("an ADR is immutable"). — [AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html); [MS Learn](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record); [Fowler](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html); [BrainGrid (2026-08-04)](https://www.braingrid.ai/blog/architecture-decision-records-for-ai-coding-agents)
- Softer: GDS allows clarifications and added consequences, and allows changing an unimplemented decision with reviewer agreement. — [GDS Way](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html). Oxide allows corrections to published RFDs via new PRs. — [Oxide RFD 1](https://rfd.shared.oxide.computer/rfd/0001). React keeps active RFCs in sync via follow-up PRs. — [reactjs/rfcs](https://github.com/reactjs/rfcs). Henderson: "living documents with dated updates have worked better than strict immutability", especially for vendor, pricing and license changes. — [joelparkerhenderson](https://github.com/joelparkerhenderson/architecture-decision-record)
- Davidson's middle path (2026-09-01): each ADR holds only its current text and Git serves as the changelog. No amendment logs; one `Updated:` line after `Date:` when an accepted ADR changes substantively; a `Superseded-On:` line paired with `Supersedes:` on the replacement. — [Davidson, Coding agents love decision records](https://duncandavidson.com/agents-love-decisions)
- adr-tools `adr new -s N` automatically updates the old ADR's status, so two-way superseding links are standard practice. — [adr-tools](https://github.com/npryce/adr-tools)

**Review in PRs**
- GDS: the open PR (or a draft PR) is the proposal, merging to `main` = accepted, and reviewers should come from affected disciplines and teams. — [GDS Way](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html)
- MS Playbook: open the PR in Proposed and switch to Accepted before merge. — [MS decision log](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/decision-log/)
- Dataverket: a new ADR starts `status: proposed`, with no accepted-state wording until acceptance. Branch `adr/…`, commit type `docs:`, PR description covers problem, decision, alternatives and reviewers. — [Dataverket, propose an ADR](https://dataverket.codeberg.page/guides/propose-an-adr/)
- CODEOWNERS (`/docs/adr/ @org/team`) auto-requests reviews, and branch protection can require code-owner approval. Draft PRs don't trigger requests until marked ready. — [GitHub Docs: CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- Zimmermann's review checklist asks: relevant enough? options valid and complete? criteria mutually exclusive and collectively exhaustive and prioritized? rationale sound? consequences objective? actionable, traceable, and with a **validity period or review date**? Review anti-patterns: Pass Through, Copy Edit, Power Game, Groundhog Day, and others. — [Zimmermann, How to review ADRs (2023)](https://www.ozimmer.ch/practices/2023/04/05/ADRReview.html)
- AWS: every software change gets at least one approval, and reviewers link the violated ADR in code review. — [AWS ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)

**Avoiding sprawl; finding ADRs later**
- Microsoft: record only decisions that affect structure or key quality attributes, or that are difficult to reverse. — [MS Learn](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- AWS scope list: structure, non-functional requirements, dependencies, interfaces (APIs/contracts), construction techniques (libraries, frameworks, tools, processes). — [AWS ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- Zimmermann's ASR test: business value or risk, key stakeholder concern, new quality-of-service needs, unpredictable external dependencies, cross-cutting impact, first-of-a-kind, past trouble. Qualitative, not a weighted score. — [Zimmermann, Architectural Significance Test (2020)](https://www.ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html)
- Henderson: skip ADRs for small, temporary (workarounds, experiments), single-developer, or already-standardized decisions. — [joelparkerhenderson](https://github.com/joelparkerhenderson/architecture-decision-record)
- Konishi (2026-05-08, updated 2026-09-09) recommends an index (`docs/adr/index.md` or `README.md`) with number, title and status, optionally rebuilt by CI from front matter. Other practices: a PR-template checkbox ("does this change introduce/modify an architectural decision?"), blocked body edits on Accepted ADRs, a quarterly one-hour review, short code comments at architectural seams pointing to the ADR, bidirectional links between tickets/design docs and ADRs, a separate Y-statement log for small decisions, and storage in the code repo rather than a wiki. Length: Nygard 1–2 pages, MADR 2–4, Y-statement one paragraph. — [Konishi](https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html)
- Microsoft Playbook: a `decision-log.md` table of executive summaries. — [MS decision log](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/decision-log/)
- Cosmos: add an entry to the README list in the same PR. — [Cosmos](https://docs.cosmos.network/sdk/v0.53/build/architecture/PROCESS)
- AWS: "Project members skim the headlines of each ADR to get an overview", so titles matter. — [AWS ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- GDS: a title describes the decision, not the problem. — [GDS Way](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html). MADR: a title "representative of solved problem and found solution". — [MADR template](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md)
- Microsoft: split multi-phase decisions into one record per phase. — [MS Learn](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record). Polishchuk: don't combine many decisions in one ADR unless they are tightly coupled. — [jopr.org, 10 ADR anti-patterns (2026-06-21)](https://jopr.org/blog/detail/10-adr-antipatterns)

**Numbering and naming**
- Nygard: sequential, never reused. MADR: `NNNN-title-with-dashes.md`. Fowler: monotonic, e.g., `0001-HTMX-for-active-web-pages`. Henderson: imperative verb phrase. — [Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions); [MADR](https://adr.github.io/madr/); [Fowler](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html); [Henderson](https://github.com/joelparkerhenderson/architecture-decision-record)
- Ways to avoid parallel-number collisions: Rust renames to the PR number; Go uses the issue number; KEP prefixes the tracking issue; MS Playbook suggests the work-item ID; pyadr uses `XXXX-` until accepted; log4brains drops numbers. — [Rust](https://github.com/rust-lang/rfcs/blob/master/README.md); [Go](https://github.com/golang/proposal/blob/master/README.md); [KEP README](https://github.com/kubernetes/enhancements/blob/master/keps/README.md); [MS](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/decision-log/); [pyadr](https://github.com/opinionated-digital-center/pyadr); [log4brains](https://github.com/thomvaill/log4brains)

**Linking to PRs and issues**
- GitHub closing keywords (`Closes #N`, etc.) work only when the PR targets the default branch; cross-repo syntax is `owner/repo#N`. — [GitHub Docs: linking PRs to issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
- PR templates live at `.github/pull_request_template.md` (or root/docs, or a `PULL_REQUEST_TEMPLATE/` folder for several). — [GitHub Docs: PR templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- Issue forms (`.github/ISSUE_TEMPLATE/*.yml`) support `labels`, `assignees`, and input/textarea/dropdown/checkbox elements with `required` validation. They can be used for a "decision request" form. — [GitHub Docs: issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- PEP's Resolution header links to the decision thread; Rust records "RFC PR" and "Rust Issue" links in its header; KEP keeps `see-also`, `replaces` and `superseded-by`. — [PEP 1](https://peps.python.org/pep-0001/); [Rust template](https://github.com/rust-lang/rfcs/blob/master/0000-template.md); [KEP-0000](https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md)

**Language and length**
- Nygard: one to two pages, in full sentences. Fowler: usually one page, inverted pyramid, link supporting material. Microsoft: "pithy, assertive, on-topic, and factual". AWS: one decision per ADR, exploration in a separate doc. Cosmos: present tense, no first person. Google mini design docs: 1–3 pages. Attentive: split above about 10–12 pages. — [Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions); [Fowler](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html); [MS Learn](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record); [AWS blog](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/); [Cosmos](https://docs.cosmos.network/sdk/v0.53/build/architecture/PROCESS); [Google](https://www.industrialempathy.com/posts/design-docs-at-google/); [Attentive](https://tech.attentive.com/articles/rfc-process-for-teams)
- Korean terms in official translations: AWS uses "아키텍처 결정 레코드", 제안됨/수락됨/거부됨/대체됨, ADR 소유자, 결정 로그. Microsoft uses "아키텍처 의사 결정 레코드", 추가 전용 로그, 신뢰도 수준. Google uses "아키텍처 결정 레코드(ADR)" and "ADR을 사용해야 하는 경우". These are machine translations; the English versions prevail if they differ. — [AWS ko welcome](https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/architectural-decision-records/welcome.html); [MS ko-kr](https://learn.microsoft.com/ko-kr/azure/well-architected/architect-role/architecture-decision-record); [Google ko](https://docs.cloud.google.com/architecture/architecture-decision-records?hl=ko)
- Toss publishes a Korean technical-writing guide (technical-writing.dev, GitHub `toss/technical-writing`). It covers choosing the document type by purpose, information structure, sentence refinement, and "AI와 함께 쓰기". Specific sentence-length rules were not visible on the fetched pages. — [technical-writing.dev](https://technical-writing.dev/); [toss/technical-writing](https://github.com/toss/technical-writing)
- Toss's 2026 Technical Writer posting describes building a standard for "AI와 독자 모두에게 가치 있는 문서" and automating document review with AI pipelines. This is a job ad, not a practice report. — [Toss careers](https://toss.im/career/job-detail?job_id=7809324003) (seen in search results only)

### Inferences
- For 믿집, use the **GDS pattern** adapted to AGENTS.md (squash merge, 1 approval). Open the ADR PR as `상태: 제안`. Merging with the status line changed to `결정 (YYYY-MM-DD)` makes it accepted, in the same PR. Require approval from the 결정한 사람 (PO or tech lead) via CODEOWNERS on `/docs/adr/`. If the team rejects it, close the PR. Merge it as `거부` only when the rejection reason should be kept to stop the debate returning (AWS's reason).
- Use Korean status words consistently and keep them machine-parseable: **제안 / 결정 / 대체됨(→ NNNN) / 폐기 / 거부**. The existing files use "결정" for accepted. That is clearer in Korean than 수락됨 and should stay. Add `폐기` (deprecated) for decisions withdrawn without a replacement.
- For immutability, take Davidson's middle path. Keep the 결정 text fixed. Allow typo and clarification edits plus one `고친 날:` line. Anything that changes behavior is a new ADR whose `바꾸는 것:` names the exact part replaced ("ADR 0001 맥락의 에이전트 목록"). The old file gets `상태: 일부 대체됨 → 0002` or `대체됨 → 0005`, in the same PR. This fixes 0002/0001's current one-way link.
- Index: `docs/adr/README.md`, a one-line-per-ADR table (번호 · 제목 · 상태 · 날짜 · 결정한 사람 · 대체 관계), updated in the same PR as the Cosmos rule requires. At 3–20 ADRs, no CI generator is needed.
- Numbering: keep 4-digit sequential numbers. The second PR to merge renumbers on a clash (Rust-style rename). A small team rarely writes two ADRs at once, so issue-number names add noise.
- Length: **one screen to one page**, 결정 written as short declarative "-다" sentences like the existing ADRs. Exploration stays in `docs/design/`, and the ADR links to it.

### Gaps
- **Korean company practice (Kakao, Toss, 우아한형제들, LINE, 당근, 뱅크샐러드)**: searches found no Korean company blog post on ADRs or RFC processes, and the search budget ran out before more targeted queries. Only Korean translations of AWS, Microsoft and Google pages and Toss's writing guide were verified. The report should say Korean industry evidence is thin rather than infer it.
- No source gives Korean-specific ADR length guidance.

---

## 5. Evidence and critiques: are ADRs kept up to date, failure modes, and what AI agents need from decision docs

### Takeaway
Empirical evidence is thin but consistent. On GitHub, ADR adoption is low but growing. About half of ADR-using repos stop at 1–5 records, and about 63% of ADRs are *created already "accepted"*, so the deliberation step is skipped. Correlations with code quality are small. Action research finds that teams perceive ADRs as useful but struggle with how much to write, where to store it, and keeping it current. Critics argue decision docs freeze stale assumptions. For AI agents, 2026 practitioner sources converge: decision files in the repo, **status inside each file**, a pointer and precedence rule in AGENTS.md (accepted = binding, proposed = context, superseded = history), short single-ruling text, links at code seams, and human review of any agent-drafted rationale.

### Cited Findings
**Studies**
- Buchgeher et al., IEEE Access 11 (June 2023), "Using ADRs in Open Source Projects – An MSR Study on GitHub": adoption is low but rising each year, about 50% of ADR repos contain only 1–5 ADRs ("tried but not definitively adopted"), most use Nygard's template, and systematic use is a team activity by two or more users over a longer period. — [JKU research portal](https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/)
- de Santana Junior et al., ICSA 2026 (26 June 2026): 921 repos and 5,800 ADRs. About 3,674 (~63%) were created with "accepted" or an equivalent status, "skipping the deliberation ADRs are meant to record". ADR length and update frequency show mostly small correlations with code smells and issue-resolution time, and adoption is "inconsistent". — [ICSA 2026 paper page](https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/34/Architecture-Decision-Records-Adoption-Impact-and-Developer-Engagement-in-Open-Sou)
- Ahmeti, Linder, Groner, Wohlrab, ECSA 2024 (LNCS 14889), action research over 3 months with 7 interviews at a microservice company: "the decision on where documentation is stored has a massive influence on its perceived usefulness". ADRs helped documentation culture, knowledge transfer and prioritization, while shared or distributed components stayed unresolved. — [Chalmers record](https://research.chalmers.se/publication/542849)
- Ahmeti, Linder, Wohlrab, womENcourage 2023, two months of action research: "ADRs are perceived as useful". Challenges were culture and organization, tacit knowledge, documentation process and tools, with worries about documenting too much or too little, placement, and keeping it current. — [Chalmers record](https://research.chalmers.se/en/publication/538920)
- Zimmermann et al.'s adoption model (2023) has Levels 1–5 plus an envisioned Level 6 (automated capture). "A small startup may be well served by Levels 2 to 3", and "less is more". Start by answering one "why" question about an existing design. — [Zimmermann, AD adoption model](https://ozimmer.ch/practices/2023/04/21/ADAdoptionModel.html)

**LLMs and ADRs (research)**
- Dhar, Vaidhyanathan, Varma (ICSA 2024, arXiv 2403.01709): GPT-4 zero-shot generated relevant Decision sections from Context but below human level. GPT-3.5 few-shot and fine-tuned Flan-T5 were comparable. — [arXiv 2403.01709](https://arxiv.org/abs/2403.01709)
- DRAFT (arXiv 2504.08207, 2025-04-11), tested on 4,911 ADRs: plain prompting "does not produce quality" design decisions, while few-shot, RAG and fine-tuning each help and their combination is best. ADR adoption is limited by manual effort and tool support. — [arXiv 2504.08207](https://arxiv.org/abs/2504.08207)
- Gupta, Dhar, Feitosa, Vaidhyanathan (arXiv 2604.03826, April 2026), on 750 repos of sequential ADRs: context-aware prompting substantially improves generation, and **a recency window of the last ~3–5 ADRs** is the best trade-off. Retrieval helps only marginally, mainly for cross-cutting decisions. "Context engineering matters more than model scale." — [arXiv 2604.03826](https://arxiv.org/abs/2604.03826)

**Failure modes (practitioner)**
- Zimmermann's creation anti-patterns: Fairy Tale (pros only), Sales Pitch, Free Lunch Coupon (hidden costs), Dummy Alternative, Sprint (one option, short-term), Tunnel Vision, Maze, Blueprint/Policy in Disguise, Mega-ADR, Novel/Epic, False urgency, Problem-solution mismatch, Pseudo-accuracy (weighted scoring). Good practices: disclose confidence, split into short-, mid- and long-term stages, and match length to complexity. — [Zimmermann, How to create ADRs (2023)](https://www.ozimmer.ch/practices/2023/04/03/ADRCreation.html)
- Polishchuk (2026-06-21) lists 10 anti-patterns: none at all; ADR as developer docs; ADR as architecture overview; many decisions in one; editing instead of superseding; no alternatives; hidden trade-offs; "letting AI make the trade-off for you"; writing after the fact; writing and approving alone. — [jopr.org](https://jopr.org/blog/detail/10-adr-antipatterns)
- Konishi: the typical arc is enthusiastic adoption, a few careful months, then quiet abandonment ("the format gets chosen but the operating model does not"). — [Konishi (2026)](https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html)
- Ard (2025-07-25), critique: ADRs and RFCs are disguised waterfall that freezes untested assumptions and becomes approval gates. "If your ADR is accurate after three sprints, you're ignoring what the code is trying to tell you." Prefer generated docs, inline comments and READMEs that describe the current state. — [Ard, Good Docs Describe, Bad Docs Prescribe](https://rethinkingsoftware.substack.com/p/good-docs-describe-bad-docs-prescribe)
- Kaplan-Moss (2023): processes with no decide step stall, and "rewarding exhaustion" favors long docs. — [Against RFCs](https://jacobian.org/2023/dec/1/against-rfcs/)
- Increment (2021): a well-written RFC that no one reads has little value, and templates bloat. — [Increment](https://increment.com/planning/planning-with-requests-for-comments/)
- AWS: ADRs don't fix non-compliant legacy code; create tech-debt tasks. — [AWS best practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html)
- GitHub mobile team (2020): ADRs are for your future self, your peers ("decision socialization") and future teammates. Writing one before the PR makes reviews better. — [GitHub Blog, Why write ADRs](https://github.blog/engineering/architecture-optimization/why-write-adrs/)

**What AI coding agents need (2025–2026)**
- Davidson (2026-09-01): agents start with little memory and a narrow view, and records in the repo give them intent. His AGENTS.md rules: **accepted ADRs are binding** (on conflict, stop and propose a change); **proposed = non-binding context**; **superseded = historical only**; propose a new or updated ADR when a change introduces a durable decision; keep ADRs succinct with Git as the changelog; no amendment logs; state each rule once and cross-reference it elsewhere. Pitfalls: agents **overfit** to obsolete ADRs (layering workarounds instead of flagging the mismatch) and inflate clarifications into amendments. — [Davidson](https://duncandavidson.com/agents-love-decisions)
- Tian Pan (2026-07-02): agents re-propose rejected ideas because rejection reasoning isn't visible in code, possibly across several PRs at once. Put the **status in the superseded file's own header**, because "an agent may never read an index". Point to `docs/adr/` from CLAUDE.md/AGENTS.md and summarize load-bearing decisions there. Add code comments like "see ADR-0031" at the point of decision. Update the ADR chain and the instruction-file summaries in the same diff, audit those summaries (they carry the most authority and the most drift), and backfill ADRs for ideas that keep getting re-proposed. — [The ADR Your Agent Never Read](https://tianpan.co/blog/2026-07-02-the-adr-your-agent-never-read)
- Vaughan (2026-04-28, updated 2026-10-28): agent-drafted ADRs "capture what was decided but may fabricate the why", so humans must verify Context and Consequences. Record agent involvement (model, prompt summary, human review outcome). List active decisions in AGENTS.md, tell the agent not to contradict accepted ADRs, and require a *proposed* ADR before implementing an uncovered architectural choice. Optional conformance checks can run in CI or hooks. "Agents scaffold systems in minutes; teams need hours or days to audit them." — [Vaughan, ADRs with Codex CLI](https://codex.danielvaughan.com/2026/04/28/codex-cli-architecture-decision-records-adr-automated-governance/)
- BrainGrid (2026-08-04): write records only for contested or non-obvious decisions ("a pile of trivial ADRs goes stale quickly"), and instruct the agent to read the decisions folder before architectural changes. — [BrainGrid](https://www.braingrid.ai/blog/architecture-decision-records-for-ai-coding-agents)
- Machine-readable metadata precedent: KEP YAML (status, replaces, superseded-by) supports tooling and presubmit checks, Giant Swarm's CI validates the RFC state header, and Konishi suggests CI read MADR front matter to build the index. — [KEP-0000](https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md); [Giant Swarm](https://handbook.giantswarm.io/docs/rfcs/decision-process); [Konishi](https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html)
- Agent loaders: Claude Code reads AGENTS.md when no CLAUDE.md exists, or via `@AGENTS.md` import. Imports load fully, so they "don't reduce context cost". Target "under 200 lines per CLAUDE.md file". Instructions are context, not enforcement, so use hooks to block actions. — [Claude Code memory docs](https://code.claude.com/docs/en/memory). Codex concatenates AGENTS.md from the repo root down to the current directory, closer files override, and the default cap is 32 KiB (`project_doc_max_bytes`). — [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Copilot reads `.github/copilot-instructions.md`, path-scoped `*.instructions.md`, and the nearest AGENTS.md; its sample prompt caps generated instructions at "no longer than 2 pages". — [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot). AGENTS.md is now stewarded by the Agentic AI Foundation (Linux Foundation) and used by 60k+ projects. It does not mention ADRs. — [agents.md](https://agents.md/)
- Anthropic (2025-09-29): context rot; aim for "the smallest possible set of high-signal tokens"; just-in-time retrieval via file paths; a hybrid of a small upfront doc plus grep/glob. — [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Böckeler (2026-02-05): keep the always-loaded file small and use path-scoped rules or skills. "There are no unit tests for context engineering." — [Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html)
- ThoughtWorks Radar (Apr 2026), GitHub Spec Kit (Assess): a "constitution" covering scope, domain, tech versions, standards and repo structure keeps agents within architectural boundaries, but warns of **instruction bloat / context rot**. — [TW Radar: GitHub Spec Kit](https://www.thoughtworks.com/radar/languages-and-frameworks/github-spec-kit)

### Inferences
- The ICSA 2026 "63% created as accepted" finding argues for a visible `제안` stage in 믿집: an open PR, or `상태: 제안` while discussion is ongoing. AI-drafted ADRs especially should start as 제안 until a human 결정한 사람 approves, which matches AGENTS.md's "AI 도구는 사람이 요청했을 때만 커밋".
- The "Context Matters" result (last 3–5 ADRs as context) and the Tian Pan/Davidson advice both point to the same layout: an ordered, numbered folder with status in each file header and a short index. AGENTS.md should point to the folder, not copy the ADRs, because of the Claude 200-line and Codex 32 KiB limits.
- Davidson's overfitting warning suggests one AGENTS.md line telling agents that when an accepted ADR seems wrong for the current task, they ask rather than work around it. AGENTS.md's "서로 부딪히면 고치기 전에 묻는다" already does this and should explicitly cover ADRs.
- The failure modes (abandonment, too much or too little, stale summaries) argue for **fewer, sharper ADRs**. At 믿집's scale and timeline, expect about 5–15 ADRs in total, not dozens.

### Gaps
- No study measures ADR effects in student or bootcamp teams, or in teams under about 6 people.
- No controlled study shows that agents follow ADRs better with YAML front matter than with plain header lines. The recommendation rests on practitioner reports and tooling precedent.
- The 63% figure comes from the ICSA 2026 abstract; the full paper's method was not read.

---

## 6. Concrete recommendation for 믿집 (when to use which record, template, naming, numbering, status, links, open decisions, staying light)

### Takeaway
Keep the current three-layer structure and tighten it. Use **issues/PRs** for reversible, local choices, **`docs/design/*.md`** as the RFC layer where open decisions live (each with a decider, deadline and state), and **`docs/adr/`** for one-way-door decisions only. Keep the existing Korean ADR template, which is effectively MADR-minimal plus Nygard. Add a few parseable header lines (날짜, 관련, two-way 대체 links), a one-table index, a PR-template checkbox, and AGENTS.md rules telling agents how to treat each status. No tooling, no review meetings beyond PR review, and one page per ADR.

### Cited Findings
- Match effort to reversibility: two-way doors are decided quickly by a person or small group, and one-way doors deliberately. — [Kindel/Bezos](https://blog.kindel.com/2019/06/27/one-way-and-two-way-doors/). Only "difficult to reverse" or structural choices go into ADRs. — [MS Learn](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record). "For small changes: don't bother." — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs)
- A big change gets an RFC and then an ADR; a small change gets an ADR directly; undocumented decisions are backfilled. — [Spotify](https://engineering.atspotify.com/2020/4/when-should-i-write-an-architecture-decision-record)
- ADR = decision already made; RFC = discussion. — [Cosmos](https://docs.cosmos.network/sdk/v0.53/build/architecture/PROCESS). Design doc as working material, ADR as the output. — [Konishi](https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html)
- Issue first, design doc only if needed. — [Go proposal](https://github.com/golang/proposal/blob/master/README.md)
- The PR is the proposal, merge = accepted, superseded files are marked and linked. — [GDS Way](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html)
- One named approver; due date on open decisions. — [DACI](https://www.atlassian.com/team-playbook/plays/daci). Decider plus reviewer deadlines. — [Sourcegraph](https://slab.com/library/templates/sourcegraph-rfc-template-proposal/)
- A small team sits best at adoption Levels 2–3; "less is more". — [Zimmermann adoption model](https://ozimmer.ch/practices/2023/04/21/ADAdoptionModel.html)
- Agent rules: accepted binding, proposed context, superseded history; status in each file; pointers from AGENTS.md; links at code seams. — [Davidson](https://duncandavidson.com/agents-love-decisions); [Tian Pan](https://tianpan.co/blog/2026-07-02-the-adr-your-agent-never-read)
- Confidence and revisit triggers are worth recording. — [MS Learn](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record); [Fowler](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html); [Zimmermann DoD](https://www.ozimmer.ch/practices/2020/05/22/ADDefinitionOfDone.html)
- Compliance/Confirmation sections say how a rule is enforced. — [AWS appendix](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/appendix.html); [MADR](https://adr.github.io/madr/)

### Inferences
**A. Which record when (decision table for 믿집)**
| Situation | Record | Example |
|---|---|---|
| Reversible, local to one feature or one person, easy to change in a later PR | PR body "무엇을 왜" + issue comment. No ADR | button order, a helper's name, test fixture shape |
| Open question still being explored, several options, needs a decider | `docs/design/<topic>.md` open decision item (ID, options, 결정할 사람, 기한, 상태) | AR1–AR13, T1–T4, AI1–AI6 |
| Decision that is hard to reverse, crosses packages or layers, changes AGENTS.md rules, picks an external provider, money/date/state rules, data schema conventions, scope in/out, or a PO rule agents must follow | `docs/adr/NNNN-slug.md` (one decision per file) | 0001 stack, 0002 vendor-written quotes, 0003 OpenAI + RDS |
| A decision that keeps being re-proposed by people or agents | Backfill an ADR (Spotify, Tian Pan) | — |
| Progress, what's done or blocked | `docs/status.md` only (existing rule). Blocked-by-decision items referenced by ID, not copied | "AR4 결정 대기 → 견적 화면 보류" |

Quick test before writing an ADR (any "yes" → ADR): if we change this in 2 weeks, must others change code, data or docs? Does it change AGENTS.md or what an agent may do? Does it choose an external service, provider or paid API? Does it change money, date or state rules or the DB schema convention? Is it a PO scope decision?

**B. Template**: keep the existing Korean ADR template, add 3 header lines, and keep 2 optional sections.
```
# NNNN. <결정을 한 문장으로>            ← title states the decision, not the problem (GDS/MADR)

- 상태: 제안 | 결정 | 일부 대체됨 → NNNN | 대체됨 → NNNN | 폐기 | 거부
- 날짜: YYYY-MM-DD                    ← separate line (now embedded in 상태)
- 결정한 사람: <한 명 또는 역할>        ← one approver (DACI)
- 바꾸는 것: ADR NNNN의 <어느 부분> | 없음   ← = Supersedes/amends
- 관련: #이슈, PR #번호, docs/design/<file>.md#<ID>
## 맥락        (2–5문장, 현재형, 사실만)
## 결정        (짧은 "-다" 문장 / 목록. 에이전트가 지킬 규칙은 여기에만)
## 다른 안     (안마다 한 줄: 무엇 + 왜 안 골랐나)
## 결과        (좋은 점 · 나쁜 점 · 고쳐야 할 문서/코드)
## 확인 방법   (선택: 테스트·lint·리뷰로 어떻게 지키는지)
## 다시 볼 때  (선택: 신뢰도 낮음/이런 일이 생기면 다시 본다)
```
- Why not YAML front matter? Plain `- 키: 값` header lines are already greppable and readable for agents. YAML front matter (MADR 4 style) is the alternative if the team later wants CI to build the index (see choice K-c).
- Length: aim for one screen and stay under one page. Exploration, diagrams and comparisons go in `docs/design/` and are linked under 관련.
- Y-statement as an optional one-liner at the top of 결정 for long ADRs: "<맥락>에서 <문제>를 두고 <안>을 골랐다. <얻는 것>을 위해 <감수할 것>을 받아들인다."

**C. Naming and numbering**: `docs/adr/NNNN-kebab-slug.md` (existing). Use the next free 4-digit number; on collision, the later PR renumbers before merge. Never reuse numbers.

**D. Status lifecycle and PR flow**
1. Open a branch `이슈번호-adr-slug` and a PR with `상태: 제안`. The commit type is `docs(docs)` per AGENTS.md.
2. Review in the PR within the decision deadline. CODEOWNERS on `/docs/adr/` can auto-request the PO or tech lead.
3. On approval, change the status in the same PR to `결정` with the date, update the index, update the old ADR's status line (`대체됨 → NNNN`) if superseding, and update AGENTS.md lines that restate the rule. Then squash merge.
4. If rejected, close the PR. Merge it with `거부` only if the reason should block future re-proposals (AWS).
5. After 결정: no edits to 결정 except typos and clarifications (add `- 고친 날:`). Changes go in a new ADR.

**E. Links**
- ADR → issue/PR/design via the `관련` line.
- PR body adds `ADR: NNNN` next to `Closes #N`.
- Design doc open item → `결정: ADR NNNN` when closed.
- Code → a one-line comment at the seam only (`# ADR 0002: 합계는 calc에서만`).
- AGENTS.md → keeps the precedence line plus a status rule (below), not copies of ADR bodies.

**F. Open decisions**: in each `docs/design/*.md`, one line or short block per open decision: `AR4 · 질문 · 안 A/B/C · 결정할 사람 · 기한 YYYY-MM-DD · 상태 열림|보류|결정 · 결과(ADR NNNN 또는 '설계 문서에만')`. When an item closes as a one-way door, promote it to an ADR. When it closes as a two-way door, mark 결정 with date and person in the design doc and stop there.

**G. AGENTS.md additions for agents (a few lines)**
- "`docs/adr/`에서 상태가 결정인 ADR은 따른다. 제안은 참고만, 대체됨·폐기는 역사다. 결정 ADR과 작업이 부딪히면 우회하지 말고 묻는다."
- "되돌리기 어려운 선택을 새로 하게 되면 코드보다 먼저 `상태: 제안` ADR 초안을 만들고 사람에게 확인받는다. AI가 쓴 맥락 · 결과는 사람이 확인한다."
- "ADR 목록은 `docs/adr/README.md`."

**H. Keeping it light**: no ADR tooling, no review meetings beyond PR review, one page per ADR, an index table, and a PR-template checkbox: "되돌리기 어려운 결정을 새로 하거나 바꾸나요? → ADR 링크". Expect about 5–15 ADRs for the whole project.

**User-owned choices to surface (K1–K6, for the parent to present together)**
- K1. Who approves ADRs: the PO only for product rules and the tech lead for technical ones, or both for every ADR? (Recommended: the role named in 결정한 사람, enforced via CODEOWNERS.)
- K2. Where an ADR sits while 제안: an open PR only (GDS style, recommended), or also merged as 제안 (Cosmos style)?
- K3. Whether to keep rejected proposals as merged `거부` files (AWS) or just close the PR (Konishi).
- K4. Where the "decided by / deadline" for open decisions lives: inside each design doc (recommended), or a single `docs/design/open-decisions.md`. Neither goes in `docs/status.md`, per AGENTS.md.
- K5. Whether to add the optional sections (확인 방법, 다시 볼 때) and an `AI 초안: 예/아니오` line (Vaughan-style attribution).
- K6. Header format: Korean bullet lines (recommended, matches 0001–0003), YAML front matter (MADR 4), or Korean bullets now and YAML later if CI-generated indexes are wanted.

### Gaps
- No source evaluates ADR practice in time-boxed bootcamp teams. The table above is an inference from industry and open-source practice plus the 믿집 context.
- Whether 0001–0003 already contain decisions that should be split (Microsoft's "one decision per record", or multi-phase decisions) was not assessed. Only 0002 was read.

### Sources consulted (full URL list, ~110)
Fetched or read directly:
1. https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
2. https://adr.github.io/madr/
3. https://adr.github.io/
4. https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
5. https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html
6. https://docs.cloud.google.com/architecture/architecture-decision-records
7. https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html
8. https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
9. https://adr.github.io/adr-templates/
10. https://adr.github.io/adr-tooling/
11. https://adr.github.io/ad-practices/
12. https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework
13. https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
14. https://www.ozimmer.ch/practices/2023/04/03/ADRCreation.html
15. https://www.ozimmer.ch/practices/2023/04/05/ADRReview.html
16. https://www.ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html
17. https://www.industrialempathy.com/posts/design-docs-at-google/
18. https://rfd.shared.oxide.computer/rfd/0001
19. https://github.com/rust-lang/rfcs/blob/master/README.md
20. https://peps.python.org/pep-0001/
21. https://www.hashicorp.com/how-hashicorp-works/articles/rfc-template
22. https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/
23. https://blog.pragmaticengineer.com/rfcs-and-design-docs/
24. https://jacobian.org/2023/dec/1/against-rfcs/
25. https://brandur.org/fragments/rfcs-and-review-councils
26. https://github.com/reactjs/rfcs
27. https://increment.com/planning/planning-with-requests-for-comments/
28. https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html
29. https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/decision-log/
30. https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/34/Architecture-Decision-Records-Adoption-Impact-and-Developer-Engagement-in-Open-Sou
31. https://arxiv.org/abs/2604.03826
32. https://research.chalmers.se/publication/542849
33. https://duncandavidson.com/agents-love-decisions
34. https://tianpan.co/blog/2026-07-02-the-adr-your-agent-never-read
35. https://codex.danielvaughan.com/2026/04/28/codex-cli-architecture-decision-records-adr-automated-governance/
36. https://www.braingrid.ai/blog/architecture-decision-records-for-ai-coding-agents
37. https://research.jku.at/en/publications/using-architecture-decision-records-in-open-source-projects-an-ms/
38. https://www.atlassian.com/team-playbook/plays/daci
39. https://www.aha.io/roadmapping/guide/templates/create/decision-log
40. https://github.com/joelparkerhenderson/architecture-decision-record
41. https://github.com/npryce/adr-tools
42. https://github.com/thomvaill/log4brains
43. https://engineering.atspotify.com/2020/4/when-should-i-write-an-architecture-decision-record
44. https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html
45. https://rethinkingsoftware.substack.com/p/good-docs-describe-bad-docs-prescribe
46. https://jopr.org/blog/detail/10-adr-antipatterns
47. https://dataverket.codeberg.page/guides/propose-an-adr/
48. https://github.com/adr/madr/releases
49. https://www.ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html
50. https://www.ozimmer.ch/practices/2020/05/22/ADDefinitionOfDone.html
51. https://ozimmer.ch/practices/2023/12/01/ADDefinitionOfReady.html
52. https://github.blog/engineering/architecture-optimization/why-write-adrs/
53. https://github.com/kubernetes/enhancements/blob/master/keps/README.md
54. https://github.com/rust-lang/rfcs/blob/master/0000-template.md
55. https://martinfowler.com/articles/scaling-architecture-conversationally.html
56. https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md
57. https://agents.md/
58. https://github.com/adr/madr/blob/4.0.0/template/adr-template-minimal.md
59. https://github.com/adr/madr/blob/4.0.0/template/adr-template.md
60. https://technical-writing.dev/
61. https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/architectural-decision-records/welcome.html
62. https://code.claude.com/docs/en/memory
63. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
64. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
65. https://github.com/golang/proposal/blob/master/README.md
66. https://github.com/swiftlang/swift-evolution/blob/main/process.md
67. https://tc39.es/process-document/
68. https://github.com/emberjs/rfcs
69. https://handbook.giantswarm.io/docs/rfcs/decision-process
70. https://arxiv.org/abs/2504.08207
71. https://research.chalmers.se/en/publication/538920
72. https://www.thoughtworks.com/radar/languages-and-frameworks/github-spec-kit
73. https://www.infoq.com/news/2022/06/aws-adr-guide/
74. https://noidea.dog/blog/yes-if
75. https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/
76. https://engineering.squarespace.com/blog/2019/the-power-of-yes-if
77. https://docs.arc42.org/section-9/
78. https://www.atlassian.com/software/confluence/templates/decision
79. https://slab.com/library/templates/sourcegraph-rfc-template-proposal/
80. https://tech.attentive.com/articles/rfc-process-for-teams
81. https://oxide.computer/blog/rfd-1-requests-for-discussion
82. https://github.com/peter-evans/lightweight-architecture-decision-records
83. https://learn.microsoft.com/ko-kr/azure/well-architected/architect-role/architecture-decision-record
84. https://github.com/toss/technical-writing
85. https://arxiv.org/abs/2403.01709
86. https://blog.kindel.com/2019/06/27/one-way-and-two-way-doors/
87. https://docs.cosmos.network/sdk/v0.53/build/architecture/PROCESS
88. https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/appendix.html
89. https://ozimmer.ch/practices/2023/04/21/ADAdoptionModel.html
90. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
91. https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html
92. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
93. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
94. https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
95. https://docs.cloud.google.com/architecture/architecture-decision-records?hl=ko
96. https://learn.chatgpt.com/docs/agent-configuration/agents-md (redirected from https://developers.openai.com/codex/guides/agents-md)
97. https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
98. https://github.com/opinionated-digital-center/pyadr
99. https://github.com/adr/adr-manager
100. https://docs.publishing.service.gov.uk/repos/govuk-infrastructure/architecture/decisions/0001-record-architecture-decisions.html
101. https://observability-platform.service.justice.gov.uk/architecture-decision-records/0001-record-architecture-decisions.html
102. https://mozac.org/rfc/0001-rfc-process
103. https://www.infoq.com/news/2020/04/architecture-decision-records/
104. https://www.pointfive.co/engineering/engineering-blog/writing-technical-specifications-the-art-of-tailoring-rfcs
105. https://www.ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html
106. https://faq.arc42.org/questions/C-9-3/
107. https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs
108. https://playbook.hackney.gov.uk/Data-Platform-Playbook/architecture-decisions/records/record-architecture-decisions
109. https://www.launchnotes.com/glossary/decision-log-template-in-product-management-and-operations

Attempted, but no usable content (404, 403, redirect or empty): https://handbook.sourcegraph.com/communication/rfcs (→ Notion), https://www.redhat.com/en/blog/architecture-decision-records (404), https://www.redhat.com/ko/blog/architecture-decision-records (404), https://doaj.org/article/f838f2a538ea48e7a3b15ce99befe612 (403), https://medium.com/olzzio/y-statements-10eb07b5a177 (403), https://wikidocs.net/368393 (403), https://www.youngju.dev/blog/culture/2026-04-15-engineering-writing-rfc-adr-design-doc-6-pager-eng-blog-changelog-slack-ai-writing-deep-dive-guide-2025 (empty), https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/ and …/workflow/ (navigation only), https://techcommunity.microsoft.com/blog/azurearchitectureblog/-/4463013 (title only: "How Great Engineers Make Architectural Decisions — ADRs, Trade-offs, and an ATAM-Lite Checklist"), https://docs.structurizr.com/ui/decisions (404), https://www.aboutamazon.com/news/company-news/2015-letter-to-shareholders (404), https://realpython.com/ref/software-engineering-glossary/architecture-decision-record/ (403), https://www.ozimmer.ch/practices/2020/04/16/AnatomyOfADR.html (404), Tyree & Akerman template paths in joelparkerhenderson repo (404), https://docs.cosmos.network/main/build/architecture/PROCESS (404).

Seen only in search results (not fetched; used only where noted): https://www.infoq.com/news/2022/06/aws-adr-guide/ (also fetched), https://toss.im/career/job-detail?job_id=7809324003, https://www.youngju.dev/tags/adr, https://wikidocs.net/356856, https://www.hostragons.com/ko/블로그/건축-결정-기록-adr-소프트웨어-문서/, https://miro.com/ko/templates/architecture-decision-record-template/, https://plutus.readthedocs.io/en/stable/adr/0001-record-architecture-decisions.html, https://adrs.flashpack.com/, https://practical.li/engineering-playbook/software-design/architecture/adr/, https://www.appunite.com/blog/what-is-adr, https://www.amazonaws.cn/blog-selection/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/, https://www.atlassian.com/blog/teamwork/daci-method-for-better-project-decisions, https://practicalengineeringmanagement.notion.site/RFC-Template-f1cb7627d410419a9b7dcbd5a48df367, https://works.hashicorp.com/articles/rfc-template, https://datatracker.ietf.org/doc/help/state/status-change/, https://forum.bors.tech/t/show-status-on-accepted-rfcs/434, https://16.reactjs.org/blog/2017/12/07/introducing-the-react-rfc-process.html, https://www.infoq.com/news/2017/12/react-rfc-process, https://devblogs.microsoft.com/blog/spec-driven-development-spec-kit, https://www.augmentcode.com/guides/github-spec-kit-practical-guide-sdd-workflow, https://github.com/sa4s-serc/ArchAI_ADR, https://www.oreilly.com/radar/?p=19867, https://smithery.ai/skills/claylo/capturing-decisions, https://barkingiguana.com/writing/living-documentation-when-the-wiki-starts-lying/, https://resources.rework.com/libraries/leadership/one-way-and-two-way-door-decisions, https://fortune.com/2017/05/11/jeff-bezos-shareholder-letter, https://docs.wikimedia.org/Wikibase/master/php/docs_adr_index.html, https://www.github.com/topics/madr, https://eventcatalog.dev/docs/development/guides/resources/adrs/introduction, https://conf.researchr.org/details/ecsa-2024/ecsa-2024-research-papers/9/Introducing-Architecture-Decision-Records-in-Practice-An-Action-Research-Study.
