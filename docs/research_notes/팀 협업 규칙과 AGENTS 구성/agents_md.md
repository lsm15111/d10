# AGENTS.md and similar AI coding-agent instruction files: what to include, what to leave out, and a minimal AGENTS.md for 믿집

Research date: all pages fetched and real files downloaded on **2026-10-29**. Anything dated earlier is labelled with its own publication date. WebSearch was unavailable after the first query because the shared per-turn search budget was used up. All sources below were therefore fetched directly from known URLs, or downloaded as raw files from GitHub (`raw.githubusercontent.com/<repo>/HEAD/<file>`). The GitHub REST API rate-limited this IP partway through, so nested-file counts per repo could not be gathered.

Project file read for tailoring (read-only, **not modified**): `mitjip/AGENTS.md` is 140 lines and 12,079 bytes, Korean, with 7 sections. `mitjip/CLAUDE.md` is one line, `@AGENTS.md`.

---

## Q1. The AGENTS.md format: stewardship, which tools read it, nested precedence, and size limits

### Takeaway
AGENTS.md is a plain-Markdown format with no schema. OpenAI released it in August 2025, and the Agentic AI Foundation (Linux Foundation) has stewarded it since December 2025. In 2026 almost every major coding agent reads it, including Claude Code natively from v2.1.277. Most tools resolve nested files with a "nearest file wins / closer file is read later" rule. The only hard limits are tool-specific: Codex 32 KiB combined, Windsurf/Devin 12,000 characters per rule file, Factory 80,000 characters, and Claude Code 4 MiB per file (40,000 characters for lazily loaded subdirectory files on 200K-context models).

### Cited Findings
**Format and stewardship**
- The site describes AGENTS.md as "a README for agents". It is standard Markdown with "no required fields", and any headings work. — [agents.md](https://agents.md/)
- The site says AGENTS.md is "stewarded by the Agentic AI Foundation under the Linux Foundation". It claims use by "over 60k open-source projects". — [agents.md](https://agents.md/)
- The Linux Foundation announced the Agentic AI Foundation (AAIF) on **2025-12-09**. Founding projects: MCP (from Anthropic), goose (from Block), and AGENTS.md (from OpenAI, "released in August 2025"). Adoption is given as "more than 60,000 open source projects and agent frameworks". There are 8 platinum members: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft and OpenAI. — [Linux Foundation press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- The format repo `agentsmd/agents.md` is MIT-licensed, includes a `Technical_Charter.pdf`, and had about 25.2k stars when read. Its sample AGENTS.md has only three sections: dev environment tips, testing instructions, and PR instructions. — [github.com/agentsmd/agents.md](https://github.com/agentsmd/agents.md)
- Sections the site lists as popular: project overview, build and test commands, code style, testing instructions, security considerations. Optional extras: commit/PR guidelines, security gotchas, large datasets, deployment. — [agents.md](https://agents.md/)

**Which tools read it (as of 2026-10-29)**
- The agents.md site lists: Codex, Jules, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, UiPath, JetBrains Junie, Amp, Cursor, RooCode, Gemini CLI, Kilo Code, Phoenix, Semgrep, GitHub Copilot coding agent, Ona, Windsurf, and Augment Code. — [agents.md](https://agents.md/)
- **Claude Code** reads AGENTS.md natively from **v2.1.277**. By default it reads AGENTS.md only when there is no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the working directory or any directory above it. If a CLAUDE.md exists, Claude reads only the CLAUDE.md files, unless that CLAUDE.md imports AGENTS.md. Setting "Project instructions" (`claude-md-or-agents-md` is the default; `claude-md-and-agents-md`, `claude-md` and `managed-only` are the others) changes this. `AGENTS.override.md`, `AGENTS.local.md` and `.agents/` are not read. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Claude Code says a `CLAUDE.md` containing `@AGENTS.md` "you can leave". It never causes a double read. A CLAUDE.md that only tells Claude in prose to read AGENTS.md is weaker, because Claude sees AGENTS.md only "if it decides to open the file". — [Claude Code memory docs](https://code.claude.com/docs/en/memory) (the Korean edition says the same: [code.claude.com/docs/ko/memory](https://code.claude.com/docs/ko/memory))
- Claude Code on **Windows**: prefer the `@AGENTS.md` import over a symlink. Creating a symlink needs Administrator rights or Developer Mode. Git also checks a symlink out as a one-line text file unless `core.symlinks` is enabled. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- **GitHub Copilot** has three instruction types. Repository-wide is `.github/copilot-instructions.md`. Path-specific is `.github/instructions/*.instructions.md` with an `applyTo` glob. Agent instructions are AGENTS.md "anywhere in the repository", where "the nearest AGENTS.md file in the directory tree will take precedence", or a single root CLAUDE.md or GEMINI.md. — [GitHub Docs: add repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- **Copilot support matrix:** AGENTS.md is read by the GitHub.com cloud agent, GitHub.com code review (which also reads `REVIEW.md`), VS Code chat (AGENTS.md only), the VS Code, JetBrains, Eclipse and Xcode cloud agents, and Copilot CLI (which also reads CLAUDE.md and GEMINI.md). It is **not** read by GitHub.com chat, VS Code code review, Visual Studio, or JetBrains chat/review. Those surfaces read only `copilot-instructions.md` and some also read `*.instructions.md`. — [GitHub Docs: support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- Copilot coding agent added AGENTS.md support, including nested files, on **2025-08-28**. — [GitHub changelog](https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/)
- **VS Code:** `chat.useAgentsMdFile` (on by default) attaches the root AGENTS.md. `chat.useNestedAgentsMdFiles` is experimental and **off by default**. `chat.useClaudeMdFile` also exists. — [VS Code custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- **Cursor:** AGENTS.md is supported at the root and in subdirectories. Nested files "are combined with parent directories, with more specific instructions taking precedence". Project Rules in `.cursor/rules` must be `.mdc`; a plain `.md` file there is ignored. Rules have four modes: Always Apply, Apply to Specific Files (`globs`), Apply Intelligently (`description`), and Manual. Precedence is Team Rules, then Project Rules, then User Rules. — [Cursor rules docs](https://cursor.com/docs/context/rules)
- **Gemini CLI** concatenates every GEMINI.md it finds (global, workspace and ancestors, plus just-in-time on file access) and sends them with every prompt. Setting `context.fileName`, for example `["AGENTS.md","GEMINI.md"]`, lets it use AGENTS.md. It supports `@file.md` imports, `/memory show` and `/memory reload`. The page also says Gemini CLI was replaced by **Antigravity CLI on 2026-06-18**; I did not verify this elsewhere. — [Gemini CLI GEMINI.md docs](https://geminicli.com/docs/cli/gemini-md/)
- **Windsurf** (docs now branded Devin Desktop / Cascade): a root AGENTS.md is an always-on rule, and a subdirectory AGENTS.md is "automatically scoped by glob" to that directory. Limits: global rules file 6,000 characters; each workspace rule file 12,000 characters. — [Devin Desktop/Windsurf memories & rules](https://docs.devin.ai/desktop/cascade/memories)
- **Jules** "automatically looks for a file named AGENTS.md in the root of your repository". — [Jules docs](https://jules.google/docs/)
- **Aider** has no native AGENTS.md support on its conventions page. You load a conventions file read-only with `/read` or `--read`, or always with `read:` in `.aider.conf.yml`. agents.md suggests `read: AGENTS.md`. — [Aider conventions](https://aider.chat/docs/usage/conventions.html); [agents.md FAQ](https://agents.md/)
- **Amp** reads AGENTS.md in the cwd, in parents up to `$HOME`, and in subtrees when it reads a file there. Personal files are `~/.config/amp/AGENTS.md`; there are also system-wide and workspace files. It falls back to AGENT.md or CLAUDE.md. `@`-mentions and `globs:` frontmatter give conditional inclusion. — [Amp AGENTS.md docs](https://ampcode.com/docs/customize/agents-md)
- **Factory Droid** searches from the cwd up to the git root, including `.factory/`, `.agents/` and `.agent/`, and also reads CLAUDE.md variants. Precedence: the current request, then nested files, then the root file, then personal defaults. — [Factory AGENTS.md docs](https://docs.factory.com/cli/configuration/agents-md)

**Nested precedence and size limits**
- **Codex discovery:** the global file comes first (`~/.codex/AGENTS.override.md` or `AGENTS.md`). Codex then walks from the project root (git root) down to the cwd, taking at most one file per directory (`AGENTS.override.md`, then `AGENTS.md`, then `project_doc_fallback_filenames`). It concatenates them root-first, so closer files "appear later and override earlier guidance". — [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) (redirected from developers.openai.com/codex/guides/agents-md)
- **Codex size limit:** `project_doc_max_bytes` defaults to **32 KiB**. Once the combined size reaches the limit, Codex stops adding files. Raise the limit or split into nested files. — [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- The agents.md FAQ says the nearest AGENTS.md to the edited file wins, and that "explicit user chat prompts override everything". — [agents.md](https://agents.md/)
- **Claude Code** concatenates files rather than overriding: ancestors first, closer files last. Subdirectory CLAUDE.md files load on demand. Any file over 4 MiB is skipped. Lazily loaded subdirectory files and path-scoped rules are truncated above **40,000 characters** on 200K-context models, or above 200,000/150,000 characters on 1M-context models. — [Claude Code memory docs (KO)](https://code.claude.com/docs/ko/memory)
- **Factory** caps initial instruction loads at 80,000 characters and dynamic Read-path discovery at 40,000 characters. It calls these "caps, not targets". — [Factory AGENTS.md docs](https://docs.factory.com/cli/configuration/agents-md)

### Inferences
- 믿집's setup, a root `CLAUDE.md` containing only `@AGENTS.md`, is the officially blessed cross-tool pattern. It is also the right choice on Windows, rather than a symlink.
- **Important caveat for nested files:** because 믿집 has a root CLAUDE.md, Claude Code's default mode reads CLAUDE.md files only. A future `backend/AGENTS.md` would be read by Codex, Copilot, Cursor and Windsurf, but **not by Claude Code**. To fix that, you would need one of: a `backend/CLAUDE.md` containing `@AGENTS.md`; the user-level setting `claude-md-and-agents-md`; or a `.claude/rules/*.md` file with `paths:`. This follows from the "When Claude Code reads AGENTS.md" rules in the memory docs.
- At 12,079 bytes, 믿집's file uses about 37% of Codex's 32 KiB default. Hangul takes 3 bytes per character in UTF-8, so a Korean file reaches byte-based limits roughly 2–3× faster per character than English text.
- Copilot surfaces that ignore AGENTS.md are GitHub.com chat, VS Code code review, Visual Studio, and JetBrains chat/review. A teammate using any of these needs a `.github/copilot-instructions.md`. Two real repos (apache/superset, home-assistant/frontend) solve this with a symlink to `../AGENTS.md`. On Windows clones, symlinks have the problem described above.

### Gaps
- Zed's rules documentation URL returned 404, so Zed's file-priority order is not verified. The zed repo itself symlinks AGENTS.md, CLAUDE.md and GEMINI.md to `.rules`.
- I could not open the AAIF technical charter PDF, so the format's governance process (how changes to the spec are made) is unknown.
- Copilot's 4,000-character code-review limit, which appears in some older blog posts, was not confirmed on the current GitHub Docs page.

---

## Q2. Official vendor guidance: what each says to include and to avoid

### Takeaway
The vendors broadly agree. Keep the file short and specific. Put exact build, test and lint commands first. Record only what the agent cannot discover from the code: non-obvious conventions, gotchas, and decisions. Move procedures and partial-codebase rules into skills, path-scoped rules or nested files. Never rely on the file to *enforce* anything, and use hooks, permissions or sandboxes for real "never" rules instead. Anthropic now explicitly calls ALL-CAPS/IMPORTANT emphasis and architecture or layout descriptions outdated advice.

### Cited Findings
**Anthropic / Claude Code** (docs read 2026-10-29)
- Target "under 200 lines per CLAUDE.md file". "Longer files consume more context and reduce adherence." Imports organize content but do not reduce context cost. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Write instructions concrete enough to verify. Examples: "Use 2-space indentation" rather than "Format code properly"; "Run `npm test` before committing"; "API handlers live in `src/api/handlers/`". — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Contradictions: "Claude may pick one arbitrarily". Review files periodically, or run `/doctor prompt-audit` (v2.1.283+), which flags outdated instructions, references to nonexistent files, and conflicts. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- CLAUDE.md is delivered "as a user message after the system prompt", and there is "no guarantee of strict compliance". — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Belongs in the file: exact test, typecheck and lint commands (including how to run a single test); places where the code is misleading; decisions that are not in the repo; and "anything you've had to correct twice already". The page's sample CLAUDE.md is 12 lines in three sections: Commands, Conventions, Gotchas. — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- "What you can stop doing": adding IMPORTANT or ALL CAPS, because emphasis "mostly makes Claude over-apply the rule"; and describing architecture and file layout, because "Claude reads the repo itself". — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- "If something has to happen every time, make it a hook, a deny rule, or a managed setting." Examples given: `Never read .env` goes in `permissions.deny`; "don't touch migrations" becomes a PreToolUse hook; "always run formatter" becomes a PostToolUse hook. Keep the enforced set small; if you reach 40 hooks, most are probably preferences. — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- Put team procedures, such as a release, in skills (`.claude/skills/<name>/SKILL.md`). Skills load only when relevant. Use `disable-model-invocation: true` for workflows with side effects. — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- `/doctor` suggests removing content Claude can derive from the codebase (directory layout, dependency lists, architecture overviews). It keeps pitfalls, rationale, and rules that differ from tool defaults. — [Claude Code memory docs (KO)](https://code.claude.com/docs/ko/memory)
- If CLAUDE.md sets commit or PR rules, turn off the built-in git rules with `includeGitInstructions` and set attribution with `attribution`, to avoid conflicts. — [Claude Code memory docs (KO)](https://code.claude.com/docs/ko/memory)
- The older Anthropic engineering post "Claude Code best practices" (April 2025) now **308-redirects** to the current docs page above. Its older advice, such as emphasising with IMPORTANT, has been superseded. — [anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- Anthropic's context-engineering post (2025-09-29) recommends the "smallest possible set of high-signal tokens". Prompts should sit at the "right altitude": neither brittle hard-coded logic nor vague guidance. It notes that CLAUDE.md is "naively dropped into context up front" while glob/grep fetch the rest just in time. — [Anthropic: effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**OpenAI Codex** (docs read 2026-10-29)
- Contents: repo layout and important directories, how to run, build, test and lint commands, engineering conventions and PR expectations, constraints and "do-not" rules, and "What done means and how to verify work". — [Codex best practices](https://learn.chatgpt.com/guides/best-practices)
- "A short, accurate `AGENTS.md` is more useful than a long file full of vague rules." Add rules only after repeated mistakes. Move task-specific guidance (planning, review, architecture) into separate files. "When Codex makes the same mistake twice, ask it for a retrospective and update `AGENTS.md`." `/init` scaffolds a starter file. — [Codex best practices](https://learn.chatgpt.com/guides/best-practices)
- A `## Code Review Rules` section belongs in the AGENTS.md closest to the governed code. Keep rules concise, state the behaviour to flag and the safe path, and leave formatting and lint to CI. — [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

**GitHub Copilot**
- The onboarding prompt asks for: a repo summary (type, languages, frameworks, runtimes); build, test, run and lint steps in order, with versions and commands "validated by running it"; project layout and CI checks; and non-obvious dependencies. The file must not be task-specific and should be "no longer than 2 pages". — [GitHub Docs: add repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- Personal instructions take priority over repository instructions, which take priority over organization instructions. All relevant sets are sent to the model, so "avoid conflicting instructions". Copilot code review reads instructions from the **head branch** of the PR. — [GitHub Docs: add repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- The coding-agent guide recommends build, test and CI commands, a structure map, and key guidelines, for example "Run `make fmt` before committing". Pre-install dependencies with `copilot-setup-steps.yml`. Write well-scoped issues with acceptance criteria. — [GitHub Docs: get the best results](https://docs.github.com/en/copilot/tutorials/coding-agent/get-the-best-results)
- VS Code tips: "Keep your instructions short and self-contained", "Include the reasoning behind rules", "Show preferred and avoided patterns with concrete code examples", "Focus on non-obvious rules", and skip conventions linters already enforce. Sources are additive, so do not rely on precedence to resolve conflicts. — [VS Code custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)

**Cursor**
- "Keep rules under 500 lines" (guidance, not a hard limit). Split large rules into composable rules. Use concrete examples. "Reference files instead of copying their contents". Start simple and add a rule when the agent repeats a mistake. Don't copy full style guides (use a linter), and don't document common commands the agent already knows. — [Cursor rules docs](https://cursor.com/docs/context/rules)

**Windsurf / Devin Desktop, Factory, Amp, Aider, Jules**
- Windsurf/Devin: keep rules short, specific and clear; skip generic advice like "write good code"; use bullets and headings; XML-style tags can group rules. — [Devin Desktop/Windsurf rules](https://docs.devin.ai/desktop/cascade/memories)
- Factory recommends these sections: overview, commands (install, run, test, lint, typecheck, build, regeneration), repo map, conventions, testing rules, generated files, security rules, PR expectations. "Smaller files are usually better." Put commands first and write checkable rules. **Do not include:** secrets or private hostnames, full copies of long docs, stale directory inventories, personal preferences that conflict with project rules, temporary task notes, or instructions to skip validation. — [Factory AGENTS.md docs](https://docs.factory.com/cli/configuration/agents-md)
- Amp: in large repos, keep the top-level file general and put subproject specifics in subtree AGENTS.md files. — [Amp AGENTS.md docs](https://ampcode.com/docs/customize/agents-md)
- Aider's example conventions file is two lines (prefer httpx; use types). It changed the agent's output measurably, so even tiny files work for concrete preferences. — [Aider conventions](https://aider.chat/docs/usage/conventions.html)
- Jules: keep AGENTS.md current. — [Jules docs](https://jules.google/docs/)

**Practitioner guidance (older, labelled)**
- GitHub blog (Matt Nigh, **2025-11-19**), from an analysis of over 2,500 agents.md files: most fail by being "too vague". The best files put commands early with flags; prefer code examples over prose ("one real code snippet…beats three paragraphs"); state the stack with versions; and set boundaries. "Never commit secrets" was the most common helpful constraint. It suggests a three-tier boundary list: **Always do / Ask first / Never do**. It names six core areas: commands, testing, project structure, code style, git workflow, boundaries. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- HumanLayer (**2025-11-25**): "< 300 lines is best", and their own root file is under 60 lines. They claim frontier models follow about 150–200 instructions consistently and that Claude Code's system prompt already holds about 50. They advise progressive disclosure through an `agent_docs/` folder with short descriptions and `file:line` pointers rather than snippets, warn against using the file as a linter, and against `/init` auto-generation. — [HumanLayer blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

### Inferences
- Across 8+ vendors, the common core is: (1) exact verification commands; (2) non-inferable conventions and gotchas; (3) boundaries. The common "don't" list is: generic advice, style rules a linter enforces, copied docs, architecture or layout the agent can read, temporary notes, and secrets.
- On emphasis, current vendor docs have moved away from 2024–25 habits. Plain, specific sentences are preferred, and a hard rule should become a hook, permission or CI check rather than gain more capital letters.

### Gaps
- I found no official Gemini/Antigravity guidance on length or content beyond the GEMINI.md page.
- HumanLayer's "150–200 instructions" figure is a practitioner claim, not a measured result. The closest measured data is IFScale (Q4).

---

## Q3. Real AGENTS.md / CLAUDE.md / copilot-instructions files in popular repos: sections, length, style

### Takeaway
I downloaded instruction files from 89 well-known repos on 2026-10-29. 80 had at least one file, giving 133 file URLs: 90 substantive files and 44 one-line pointer or symlink files. The typical substantive file is about 100–135 lines and about 6–7 KB. 71% are 200 lines or fewer, and 31% are 60 lines or fewer. Commands appear in 86% of files. Prohibition phrasing ("never" / "do not") appears in 81%. A dedicated security section appears in only about 20%. The dominant multi-tool pattern is a single AGENTS.md as source of truth, with CLAUDE.md (and sometimes GEMINI.md or copilot-instructions) as a symlink or `@AGENTS.md` import.

### Cited Findings
**Corpus and method.** Files were fetched as `raw.githubusercontent.com/<repo>/HEAD/{AGENTS.md, CLAUDE.md, .github/copilot-instructions.md, GEMINI.md}`, root level only. Lines, bytes, headings, code fences and keywords were counted with a local script. Topic detection is keyword or heading regex, so treat percentages as approximate. The full URL list is at the end of this section.

**Coverage**
- Of 89 repos tried, **80 had at least one root file**. 69 had AGENTS.md, 39 had CLAUDE.md, **34 had both**, and 21 had copilot-instructions. No root file was found in 9 repos: openai/codex, continuedev/continue, dagger/dagger, hashicorp/terraform, immich-app/immich, jj-vcs/jj, microsoft/semantic-kernel, open-webui/open-webui, tailwindlabs/tailwindcss. — the per-repo URLs listed below
- openai/codex, the originator of AGENTS.md, had **no** AGENTS.md at the root or at `codex-rs/` on 2026-10-29. The top-level listing shows no AGENTS.md or CLAUDE.md. — [github.com/openai/codex](https://github.com/openai/codex)

**Pointer / sync pattern**
- 44 files under 200 bytes were pointers: **26 symlinks**, **13 `@AGENTS.md` imports**, and **5 prose pointers**. Examples:
  - symlinks: PostHog, airflow, superset, cal.com, prisma, pnpm and openai-agents-* (CLAUDE.md → AGENTS.md); bun, pytorch and twenty (the reverse, AGENTS.md → CLAUDE.md); zed (all → `.rules`); transformers (→ `.ai/AGENTS.md`); ClickHouse (→ `.claude/CLAUDE.md`)
  - imports: sentry, grafana, ruff, n8n, gutenberg, supabase, strapi, tldraw, goose
  - prose pointers: llama.cpp's CLAUDE.md, lobe-chat's GEMINI.md, pydantic's AGENTS.md ("Read and follow CONTRIBUTING.md…"), ClickHouse's copilot-instructions
  — [URLs below](#real-file-url-list)
- superset and home-assistant/frontend symlink `.github/copilot-instructions.md` to `../AGENTS.md`. — [superset](https://github.com/apache/superset/blob/HEAD/.github/copilot-instructions.md); [HA frontend](https://github.com/home-assistant/frontend/blob/HEAD/.github/copilot-instructions.md)

**Length (90 substantive files)**
- All types: median **108 lines**, mean 150, range 5–539; median 6.6 KB; quartiles 45 / 108 / 227 lines.
  - AGENTS.md (n=61): median **135 lines**, mean 164.
  - CLAUDE.md (n=10 substantive): median 73.
  - copilot-instructions (n=18): median 99.5.
- Buckets: **28** files ≤60 lines, **36** at 61–200, **21** at 201–400, **5** over 400. The five longest: vercel/next.js 539, duckdb 501, pnpm 500, n8n 458, deno CLAUDE.md 434.
- **4 AGENTS.md files exceed Codex's 32 KiB default**, so Codex would stop adding project docs at its limit unless it is raised: PostHog 46,162 B, openai-agents-js 39,478 B, openai-agents-python 38,241 B, pnpm 33,947 B. — [PostHog](https://github.com/PostHog/posthog/blob/HEAD/AGENTS.md), [openai-agents-js](https://github.com/openai/openai-agents-js/blob/HEAD/AGENTS.md), [openai-agents-python](https://github.com/openai/openai-agents-python/blob/HEAD/AGENTS.md), [pnpm](https://github.com/pnpm/pnpm/blob/HEAD/AGENTS.md)

**Section and topic prevalence (90 files)**
- Content signals:
  - Build, test or lint commands mentioned: **86%**.
  - Fenced code blocks: 63%.
  - Links or `@` references to other `.md` docs: 54%.
- Headings (H2/H3) by category:
  - code style/conventions 64%
  - git/commit/PR/review 62%
  - testing 54%
  - commands/build/dev 51%
  - structure/architecture 51%
  - AI/agent workflow 44%
  - overview 33%
  - docs/references 31%
  - restrictions/gotchas/rules 28%
  - setup/environment 24%
  - security 20%
  - dependencies 12%
  - debugging 7%
- Prohibition phrasing ("never", "do not", "don't", "avoid") appears in **73 of 90 files (81%)**. All-caps MUST, NEVER or IMPORTANT is rarer and concentrated in a few files, for example autogen's copilot-instructions with 20 NEVERs.
- Topics of prohibition lines (keyword-classified, rough):
  - comment/doc/prose style: 47%
  - git operations (commit, push, force, co-author): 44%
  - scope creep and unrequested refactors: 37%
  - dependency changes: 31%
  - generated, snapshot or lock files: 31%
  - skipping or weakening tests: 28%
  - secrets: 20%
  - public API / breaking changes: 14%
  - destructive commands: 14%
  - migrations or schema: 14%
  - agent creating PRs or issues: 11%
  - AI disclosure / co-author trailers: 10%

**Representative minimal files**
- astral-sh/uv AGENTS.md, **50 lines, no headings**: a flat list of `ALWAYS` / `NEVER` / `PREFER` / `AVOID` bullets that opens with "Read CONTRIBUTING.md". Examples: "NEVER update all dependencies in the lockfile…use `cargo update --precise`"; "NEVER assume clippy warnings or test failures are pre-existing"; "DO NOT leak our conversation…into code comments, pull request descriptions". — [uv AGENTS.md](https://github.com/astral-sh/uv/blob/HEAD/AGENTS.md)
- ghostty-org/ghostty, **41 lines**: Commands (build, targeted test with filter, format), libghostty-vt, Directory Structure (3 lines), and Issue/PR guidelines ("Never create an issue." / "Never create a PR."). — [ghostty AGENTS.md](https://github.com/ghostty-org/ghostty/blob/HEAD/AGENTS.md)
- kubernetes/kubernetes, **40 lines**: Communication Preferences, then **Constraints** ("Generated files are read-only… Run `make update`"; "Never `go mod tidy`"), then Contributor Guidelines (disclose AI use; no `Co-authored-by:`), then Commands, then Style. — [kubernetes AGENTS.md](https://github.com/kubernetes/kubernetes/blob/HEAD/AGENTS.md)
- temporalio/temporal, **43 lines**: a persona, a "MUST REVIEW" pointer to `.github/copilot-instructions.md`, a project structure list, development commands, and a 3-step workflow (inspect → implement → run tests and lint). — [temporal AGENTS.md](https://github.com/temporalio/temporal/blob/HEAD/AGENTS.md)
- sveltejs/svelte, **16 lines**: requires reading CONTRIBUTING.md and filling in the PR template, forbids submitting without the full test suite, and links to the security policy and a skill. — [svelte AGENTS.md](https://github.com/sveltejs/svelte/blob/HEAD/AGENTS.md)
- facebook/react CLAUDE.md, **14 lines**: a monorepo split (the compiler has its own instructions) and the current active work. — [react CLAUDE.md](https://github.com/facebook/react/blob/HEAD/CLAUDE.md)
- microsoft/vscode AGENTS.md is **6 lines** and points to a 163-line `.github/copilot-instructions.md`. — [vscode AGENTS.md](https://github.com/microsoft/vscode/blob/HEAD/AGENTS.md), [vscode copilot-instructions](https://github.com/microsoft/vscode/blob/HEAD/.github/copilot-instructions.md)
- Restrictions about AI-authored contributions are becoming common. llama.cpp: "AI-generated code is allowed… not allowed is submitting code you do not understand". pydantic-ai: no `Co-Authored-By` Claude trailer. airflow: never list an agent as co-author. — [llama.cpp](https://github.com/ggml-org/llama.cpp/blob/HEAD/AGENTS.md), [pydantic-ai](https://github.com/pydantic/pydantic-ai/blob/HEAD/AGENTS.md), [airflow](https://github.com/apache/airflow/blob/HEAD/AGENTS.md)

**Published corpus studies (for comparison)**
- 253 CLAUDE.md files from 242 repos have shallow hierarchies (one main heading plus subsections). They are dominated by operational commands, implementation notes, and high-level architecture. — [Chatlatanagulchai et al., arXiv:2509.14744 (2025-09)](https://arxiv.org/abs/2509.14744)
- 2,303 context files from 1,925 repos:
  - Median words: Copilot 535, Claude Code 485, Codex 335.5.
  - Structure: one H1; median 6–7 H2s.
  - Share of files covering each category: testing 75.9%, implementation details 70.8%, architecture 68.1%, development process 65.1%, build and run 63.0%, overview 59.0%; **security 14.8%, performance 14.5%**.
  — [Agent READMEs, arXiv:2511.12884 (v1 2025-11, v2 2026-08)](https://arxiv.org/html/2511.12884)
- Of 10,000 sampled GitHub repos, only **466 (5%)** had any of the four formats. Mean length in lines: AGENTS.md 142 (SD 231), CLAUDE.md 287, Copilot 310, GEMINI.md 106. Top AGENTS.md headings: conventions, contribution guidelines, architecture, build commands; security was among the rarest. — [Mohsenimofidi et al., MSR 2026, arXiv:2510.21413](https://arxiv.org/html/2510.21413)

### Inferences
- 믿집's 140 lines sit almost exactly at the AGENTS.md median (135) of large, mature OSS projects. By size alone it is not an outlier. Its 7 sections, however, carry more architecture and process prose than the minimal exemplars (uv, ghostty, kubernetes, svelte), which are mostly commands, constraints and pointers.
- The best-regarded short files share a pattern: **commands, then constraints/never-list, then pointers to CONTRIBUTING, the PR template or docs**, with little or no architecture narrative.

### Gaps
- Nested AGENTS.md counts per repo could not be gathered because the GitHub API rate-limited this IP. Only root files were sampled.
- The sample is biased toward large, famous projects. It says little about small student or team repos.

#### Real file URL list
80 repos, 133 files (raw content fetched via raw.githubusercontent.com/<repo>/HEAD/<file> on 2026-10-29):
- **ClickHouse/ClickHouse**: [.github/copilot-instructions.md](https://github.com/ClickHouse/ClickHouse/blob/HEAD/.github/copilot-instructions.md) (pointer → prose: "Read and follow the Review Instructions section in .claude/skills/review/SKILL.md"); [AGENTS.md](https://github.com/ClickHouse/ClickHouse/blob/HEAD/AGENTS.md) (pointer → `.claude/CLAUDE.md`)
- **PostHog/posthog**: [AGENTS.md](https://github.com/PostHog/posthog/blob/HEAD/AGENTS.md) (344 lines, 46162 B); [CLAUDE.md](https://github.com/PostHog/posthog/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **TanStack/router**: [AGENTS.md](https://github.com/TanStack/router/blob/HEAD/AGENTS.md) (42 lines, 5567 B)
- **WordPress/gutenberg**: [.github/copilot-instructions.md](https://github.com/WordPress/gutenberg/blob/HEAD/.github/copilot-instructions.md) (30 lines, 3001 B); [AGENTS.md](https://github.com/WordPress/gutenberg/blob/HEAD/AGENTS.md) (105 lines, 11669 B); [CLAUDE.md](https://github.com/WordPress/gutenberg/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **angular/angular**: [AGENTS.md](https://github.com/angular/angular/blob/HEAD/AGENTS.md) (40 lines, 2052 B)
- **anthropics/claude-agent-sdk-python**: [CLAUDE.md](https://github.com/anthropics/claude-agent-sdk-python/blob/HEAD/CLAUDE.md) (85 lines, 4111 B)
- **apache/airflow**: [AGENTS.md](https://github.com/apache/airflow/blob/HEAD/AGENTS.md) (254 lines, 23160 B); [CLAUDE.md](https://github.com/apache/airflow/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **apache/datafusion**: [AGENTS.md](https://github.com/apache/datafusion/blob/HEAD/AGENTS.md) (73 lines, 2840 B); [CLAUDE.md](https://github.com/apache/datafusion/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **apache/iceberg**: [AGENTS.md](https://github.com/apache/iceberg/blob/HEAD/AGENTS.md) (270 lines, 17459 B)
- **apache/superset**: [.github/copilot-instructions.md](https://github.com/apache/superset/blob/HEAD/.github/copilot-instructions.md) (pointer → `../AGENTS.md`); [AGENTS.md](https://github.com/apache/superset/blob/HEAD/AGENTS.md) (317 lines, 16740 B); [CLAUDE.md](https://github.com/apache/superset/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`); [GEMINI.md](https://github.com/apache/superset/blob/HEAD/GEMINI.md) (pointer → `AGENTS.md`)
- **appwrite/appwrite**: [AGENTS.md](https://github.com/appwrite/appwrite/blob/HEAD/AGENTS.md) (335 lines, 29024 B); [CLAUDE.md](https://github.com/appwrite/appwrite/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **astral-sh/ruff**: [AGENTS.md](https://github.com/astral-sh/ruff/blob/HEAD/AGENTS.md) (240 lines, 20264 B); [CLAUDE.md](https://github.com/astral-sh/ruff/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **astral-sh/ty**: [AGENTS.md](https://github.com/astral-sh/ty/blob/HEAD/AGENTS.md) (6 lines, 323 B)
- **astral-sh/uv**: [AGENTS.md](https://github.com/astral-sh/uv/blob/HEAD/AGENTS.md) (50 lines, 3746 B)
- **biomejs/biome**: [AGENTS.md](https://github.com/biomejs/biome/blob/HEAD/AGENTS.md) (89 lines, 5178 B)
- **block/goose**: [.github/copilot-instructions.md](https://github.com/block/goose/blob/HEAD/.github/copilot-instructions.md) (102 lines, 4637 B); [AGENTS.md](https://github.com/block/goose/blob/HEAD/AGENTS.md) (133 lines, 6212 B); [CLAUDE.md](https://github.com/block/goose/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **calcom/cal.com**: [AGENTS.md](https://github.com/calcom/cal.com/blob/HEAD/AGENTS.md) (245 lines, 9225 B); [CLAUDE.md](https://github.com/calcom/cal.com/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **cline/cline**: [.github/copilot-instructions.md](https://github.com/cline/cline/blob/HEAD/.github/copilot-instructions.md) (58 lines, 3804 B); [AGENTS.md](https://github.com/cline/cline/blob/HEAD/AGENTS.md) (35 lines, 5449 B)
- **cockroachdb/cockroach**: [CLAUDE.md](https://github.com/cockroachdb/cockroach/blob/HEAD/CLAUDE.md) (149 lines, 5673 B)
- **denoland/deno**: [.github/copilot-instructions.md](https://github.com/denoland/deno/blob/HEAD/.github/copilot-instructions.md) (353 lines, 12567 B); [CLAUDE.md](https://github.com/denoland/deno/blob/HEAD/CLAUDE.md) (434 lines, 11866 B)
- **dotnet/aspnetcore**: [.github/copilot-instructions.md](https://github.com/dotnet/aspnetcore/blob/HEAD/.github/copilot-instructions.md) (97 lines, 9863 B)
- **dotnet/runtime**: [.github/copilot-instructions.md](https://github.com/dotnet/runtime/blob/HEAD/.github/copilot-instructions.md) (106 lines, 14665 B)
- **duckdb/duckdb**: [AGENTS.md](https://github.com/duckdb/duckdb/blob/HEAD/AGENTS.md) (501 lines, 18534 B); [CLAUDE.md](https://github.com/duckdb/duckdb/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **elastic/kibana**: [AGENTS.md](https://github.com/elastic/kibana/blob/HEAD/AGENTS.md) (104 lines, 7574 B)
- **excalidraw/excalidraw**: [.github/copilot-instructions.md](https://github.com/excalidraw/excalidraw/blob/HEAD/.github/copilot-instructions.md) (46 lines, 1638 B); [AGENTS.md](https://github.com/excalidraw/excalidraw/blob/HEAD/AGENTS.md) (5 lines, 373 B); [CLAUDE.md](https://github.com/excalidraw/excalidraw/blob/HEAD/CLAUDE.md) (35 lines, 1295 B)
- **facebook/react**: [CLAUDE.md](https://github.com/facebook/react/blob/HEAD/CLAUDE.md) (14 lines, 359 B)
- **getsentry/sentry**: [AGENTS.md](https://github.com/getsentry/sentry/blob/HEAD/AGENTS.md) (135 lines, 7002 B); [CLAUDE.md](https://github.com/getsentry/sentry/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **getsentry/sentry-javascript**: [AGENTS.md](https://github.com/getsentry/sentry-javascript/blob/HEAD/AGENTS.md) (129 lines, 7928 B)
- **getsentry/sentry-python**: [AGENTS.md](https://github.com/getsentry/sentry-python/blob/HEAD/AGENTS.md) (101 lines, 4962 B); [CLAUDE.md](https://github.com/getsentry/sentry-python/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **ggml-org/llama.cpp**: [AGENTS.md](https://github.com/ggml-org/llama.cpp/blob/HEAD/AGENTS.md) (252 lines, 11761 B); [CLAUDE.md](https://github.com/ggml-org/llama.cpp/blob/HEAD/CLAUDE.md) (pointer → `IMPORTANT: Ensure you’ve thoroughly reviewed the [AGENTS.md]`)
- **ghostty-org/ghostty**: [AGENTS.md](https://github.com/ghostty-org/ghostty/blob/HEAD/AGENTS.md) (41 lines, 1466 B)
- **google-gemini/gemini-cli**: [GEMINI.md](https://github.com/google-gemini/gemini-cli/blob/HEAD/GEMINI.md) (97 lines, 4610 B)
- **grafana/grafana**: [AGENTS.md](https://github.com/grafana/grafana/blob/HEAD/AGENTS.md) (181 lines, 10740 B); [CLAUDE.md](https://github.com/grafana/grafana/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **grafana/loki**: [AGENTS.md](https://github.com/grafana/loki/blob/HEAD/AGENTS.md) (67 lines, 2563 B)
- **home-assistant/core**: [.github/copilot-instructions.md](https://github.com/home-assistant/core/blob/HEAD/.github/copilot-instructions.md) (198 lines, 12690 B); [AGENTS.md](https://github.com/home-assistant/core/blob/HEAD/AGENTS.md) (58 lines, 5708 B); [CLAUDE.md](https://github.com/home-assistant/core/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **home-assistant/frontend**: [.github/copilot-instructions.md](https://github.com/home-assistant/frontend/blob/HEAD/.github/copilot-instructions.md) (pointer → `../AGENTS.md`); [AGENTS.md](https://github.com/home-assistant/frontend/blob/HEAD/AGENTS.md) (67 lines, 4623 B); [CLAUDE.md](https://github.com/home-assistant/frontend/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **huggingface/transformers**: [.github/copilot-instructions.md](https://github.com/huggingface/transformers/blob/HEAD/.github/copilot-instructions.md) (40 lines, 3529 B); [AGENTS.md](https://github.com/huggingface/transformers/blob/HEAD/AGENTS.md) (pointer → `.ai/AGENTS.md`); [CLAUDE.md](https://github.com/huggingface/transformers/blob/HEAD/CLAUDE.md) (pointer → `.ai/AGENTS.md`)
- **kubernetes/kubernetes**: [AGENTS.md](https://github.com/kubernetes/kubernetes/blob/HEAD/AGENTS.md) (40 lines, 1885 B)
- **langchain-ai/langchain**: [AGENTS.md](https://github.com/langchain-ai/langchain/blob/HEAD/AGENTS.md) (391 lines, 20580 B)
- **langchain-ai/langgraph**: [AGENTS.md](https://github.com/langchain-ai/langgraph/blob/HEAD/AGENTS.md) (99 lines, 4234 B)
- **langfuse/langfuse**: [AGENTS.md](https://github.com/langfuse/langfuse/blob/HEAD/AGENTS.md) (pointer → `.agents/AGENTS.md`)
- **lobehub/lobe-chat**: [AGENTS.md](https://github.com/lobehub/lobe-chat/blob/HEAD/AGENTS.md) (199 lines, 16172 B); [GEMINI.md](https://github.com/lobehub/lobe-chat/blob/HEAD/GEMINI.md) (pointer → `# GEMINI.md  Please follow instructions @./AGENTS.md`)
- **makeplane/plane**: [AGENTS.md](https://github.com/makeplane/plane/blob/HEAD/AGENTS.md) (46 lines, 2944 B)
- **mastra-ai/mastra**: [AGENTS.md](https://github.com/mastra-ai/mastra/blob/HEAD/AGENTS.md) (19 lines, 1760 B); [CLAUDE.md](https://github.com/mastra-ai/mastra/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **mattermost/mattermost**: [AGENTS.md](https://github.com/mattermost/mattermost/blob/HEAD/AGENTS.md) (19 lines, 742 B)
- **microsoft/TypeScript**: [.github/copilot-instructions.md](https://github.com/microsoft/TypeScript/blob/HEAD/.github/copilot-instructions.md) (145 lines, 5835 B)
- **microsoft/autogen**: [.github/copilot-instructions.md](https://github.com/microsoft/autogen/blob/HEAD/.github/copilot-instructions.md) (226 lines, 8858 B)
- **microsoft/playwright**: [.github/copilot-instructions.md](https://github.com/microsoft/playwright/blob/HEAD/.github/copilot-instructions.md) (11 lines, 635 B); [AGENTS.md](https://github.com/microsoft/playwright/blob/HEAD/AGENTS.md) (178 lines, 8790 B)
- **microsoft/vscode**: [.github/copilot-instructions.md](https://github.com/microsoft/vscode/blob/HEAD/.github/copilot-instructions.md) (163 lines, 12839 B); [AGENTS.md](https://github.com/microsoft/vscode/blob/HEAD/AGENTS.md) (6 lines, 271 B)
- **modelcontextprotocol/python-sdk**: [AGENTS.md](https://github.com/modelcontextprotocol/python-sdk/blob/HEAD/AGENTS.md) (167 lines, 8714 B); [CLAUDE.md](https://github.com/modelcontextprotocol/python-sdk/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **modelcontextprotocol/typescript-sdk**: [CLAUDE.md](https://github.com/modelcontextprotocol/typescript-sdk/blob/HEAD/CLAUDE.md) (15 lines, 1294 B)
- **mozilla/pdf.js**: [AGENTS.md](https://github.com/mozilla/pdf.js/blob/HEAD/AGENTS.md) (205 lines, 7076 B)
- **n8n-io/n8n**: [AGENTS.md](https://github.com/n8n-io/n8n/blob/HEAD/AGENTS.md) (458 lines, 24174 B); [CLAUDE.md](https://github.com/n8n-io/n8n/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **nodejs/node**: [AGENTS.md](https://github.com/nodejs/node/blob/HEAD/AGENTS.md) (65 lines, 3083 B)
- **nuxt/nuxt**: [AGENTS.md](https://github.com/nuxt/nuxt/blob/HEAD/AGENTS.md) (12 lines, 948 B)
- **openai/openai-agents-js**: [AGENTS.md](https://github.com/openai/openai-agents-js/blob/HEAD/AGENTS.md) (249 lines, 39478 B); [CLAUDE.md](https://github.com/openai/openai-agents-js/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **openai/openai-agents-python**: [AGENTS.md](https://github.com/openai/openai-agents-python/blob/HEAD/AGENTS.md) (215 lines, 38241 B); [CLAUDE.md](https://github.com/openai/openai-agents-python/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **oven-sh/bun**: [AGENTS.md](https://github.com/oven-sh/bun/blob/HEAD/AGENTS.md) (pointer → `CLAUDE.md`); [CLAUDE.md](https://github.com/oven-sh/bun/blob/HEAD/CLAUDE.md) (240 lines, 17554 B)
- **pnpm/pnpm**: [AGENTS.md](https://github.com/pnpm/pnpm/blob/HEAD/AGENTS.md) (500 lines, 33947 B); [CLAUDE.md](https://github.com/pnpm/pnpm/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **prisma/prisma**: [AGENTS.md](https://github.com/prisma/prisma/blob/HEAD/AGENTS.md) (135 lines, 11516 B); [CLAUDE.md](https://github.com/prisma/prisma/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **pydantic/pydantic**: [AGENTS.md](https://github.com/pydantic/pydantic/blob/HEAD/AGENTS.md) (pointer → `Read and follow CONTRIBUTING.md, in particular the "Pull Req`)
- **pydantic/pydantic-ai**: [AGENTS.md](https://github.com/pydantic/pydantic-ai/blob/HEAD/AGENTS.md) (176 lines, 19427 B); [CLAUDE.md](https://github.com/pydantic/pydantic-ai/blob/HEAD/CLAUDE.md) (pointer → `AGENTS.md`)
- **pytorch/pytorch**: [.github/copilot-instructions.md](https://github.com/pytorch/pytorch/blob/HEAD/.github/copilot-instructions.md) (128 lines, 4835 B); [AGENTS.md](https://github.com/pytorch/pytorch/blob/HEAD/AGENTS.md) (pointer → `CLAUDE.md`); [CLAUDE.md](https://github.com/pytorch/pytorch/blob/HEAD/CLAUDE.md) (366 lines, 16518 B)
- **ray-project/ray**: [AGENTS.md](https://github.com/ray-project/ray/blob/HEAD/AGENTS.md) (110 lines, 4320 B)
- **remix-run/react-router**: [AGENTS.md](https://github.com/remix-run/react-router/blob/HEAD/AGENTS.md) (159 lines, 7415 B); [CLAUDE.md](https://github.com/remix-run/react-router/blob/HEAD/CLAUDE.md) (27 lines, 988 B)
- **sst/opencode**: [AGENTS.md](https://github.com/sst/opencode/blob/HEAD/AGENTS.md) (209 lines, 16508 B)
- **strapi/strapi**: [AGENTS.md](https://github.com/strapi/strapi/blob/HEAD/AGENTS.md) (264 lines, 12282 B); [CLAUDE.md](https://github.com/strapi/strapi/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **supabase/supabase**: [.github/copilot-instructions.md](https://github.com/supabase/supabase/blob/HEAD/.github/copilot-instructions.md) (88 lines, 6608 B); [AGENTS.md](https://github.com/supabase/supabase/blob/HEAD/AGENTS.md) (76 lines, 6918 B); [CLAUDE.md](https://github.com/supabase/supabase/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **sveltejs/svelte**: [AGENTS.md](https://github.com/sveltejs/svelte/blob/HEAD/AGENTS.md) (16 lines, 667 B)
- **temporalio/sdk-typescript**: [AGENTS.md](https://github.com/temporalio/sdk-typescript/blob/HEAD/AGENTS.md) (25 lines, 1522 B)
- **temporalio/temporal**: [.github/copilot-instructions.md](https://github.com/temporalio/temporal/blob/HEAD/.github/copilot-instructions.md) (155 lines, 13456 B); [AGENTS.md](https://github.com/temporalio/temporal/blob/HEAD/AGENTS.md) (43 lines, 2483 B)
- **tldraw/tldraw**: [AGENTS.md](https://github.com/tldraw/tldraw/blob/HEAD/AGENTS.md) (229 lines, 13890 B); [CLAUDE.md](https://github.com/tldraw/tldraw/blob/HEAD/CLAUDE.md) (pointer → `@AGENTS.md`)
- **twentyhq/twenty**: [AGENTS.md](https://github.com/twentyhq/twenty/blob/HEAD/AGENTS.md) (pointer → `CLAUDE.md`); [CLAUDE.md](https://github.com/twentyhq/twenty/blob/HEAD/CLAUDE.md) (61 lines, 6610 B)
- **vercel/ai**: [AGENTS.md](https://github.com/vercel/ai/blob/HEAD/AGENTS.md) (326 lines, 13733 B)
- **vercel/next.js**: [AGENTS.md](https://github.com/vercel/next.js/blob/HEAD/AGENTS.md) (539 lines, 31539 B)
- **vitejs/vite**: [.github/copilot-instructions.md](https://github.com/vitejs/vite/blob/HEAD/.github/copilot-instructions.md) (51 lines, 1632 B)
- **vitest-dev/vitest**: [.github/copilot-instructions.md](https://github.com/vitest-dev/vitest/blob/HEAD/.github/copilot-instructions.md) (12 lines, 323 B); [AGENTS.md](https://github.com/vitest-dev/vitest/blob/HEAD/AGENTS.md) (267 lines, 18766 B)
- **vllm-project/vllm**: [AGENTS.md](https://github.com/vllm-project/vllm/blob/HEAD/AGENTS.md) (164 lines, 6358 B)
- **withastro/astro**: [AGENTS.md](https://github.com/withastro/astro/blob/HEAD/AGENTS.md) (166 lines, 8925 B)
- **zed-industries/zed**: [AGENTS.md](https://github.com/zed-industries/zed/blob/HEAD/AGENTS.md) (pointer → `.rules`); [CLAUDE.md](https://github.com/zed-industries/zed/blob/HEAD/CLAUDE.md) (pointer → `.rules`); [GEMINI.md](https://github.com/zed-industries/zed/blob/HEAD/GEMINI.md) (pointer → `.rules`)

---

## Q4. Evidence on effectiveness: do instruction files help, and do long files hurt?

### Takeaway
The best controlled evidence (ETH Zürich, CTXbench, 2026) finds that context files do **not** reliably raise task success. They add **about 20% cost**, and LLM-generated files are slightly negative. Agents do follow the specific instructions in them very faithfully, for example using a named tool about 160× more often, and developer-written files beat LLM-generated ones by about 7 points. Other studies show efficiency gains: −29% runtime and −17% output tokens. A small "docs index" in AGENTS.md beat on-demand skills in Vercel's evals. Instruction-following degrades as instruction count and context length grow, so short, targeted, human-written files with non-obvious rules are the evidence-backed choice.

### Cited Findings
- **ETH Zürich, "Evaluating AGENTS.md"** (Gloaguen, Mündler-Sasahara, Müller, Raychev, Vechev; v1 2026-02-12, v3 2026-09-29). Benchmarks: SWE-bench Lite (300 tasks, 11 repos) and **CTXbench** (138 instances from 12 repos that ship their own context files).
  - LLM-generated files: about **−0.5%** success on SWE-bench Lite and about **−2%** on CTXbench (not significant).
  - Developer-written files: about **+2.4%** (not significant).
  - Developer-written vs LLM-generated: about **+7%** on CTXbench (p = 0.038).
  - Cost rose about **+20–23%**, with 2.45–3.92 extra steps.
  - When `uv` was mentioned, agents used it about 1.6 times per instance, versus under 0.01 when it was not. Repo-specific tools: 2.5 vs under 0.05.
  - **Repository overviews did not help** agents reach the relevant files faster.
  - Recommendations: omit LLM-generated files; human-written files should include only what is not already in the README (specific conventions, non-functional requirements); evaluate before adopting.
  — [arXiv:2602.11988 abstract](https://arxiv.org/abs/2602.11988); [full text v3](https://arxiv.org/html/2602.11988v3)
- **Lulla et al., "On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents"** (v1 2026-01-28, v2 2026-03-30). 124 PRs across 10 repos, with and without AGENTS.md. Median wall-clock runtime fell about **28.64%**, output tokens about **16.58%**, with "comparable task completion behavior". — [arXiv:2601.20404](https://arxiv.org/abs/2601.20404)
- **Vercel, "AGENTS.md outperforms skills in our agent evals"** (2026-01-27). The eval used Next.js 16 APIs absent from training data.
  - Baseline: 53%.
  - Skill (default): 53%; the skill was never invoked in 56% of cases.
  - Skill with explicit instruction to invoke: 79%.
  - **AGENTS.md docs index: 100%**.
  - A 40 KB index compressed to **8 KB** (−80%) kept 100%.
  - A "MUST invoke the skill" wording caused anchoring; "explore project first, then invoke skill" did better.
  — [Vercel blog](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **IFScale, "How Many Instructions Can LLMs Follow at Once?"** (2025-07-15, older). Across 20 frontier models, even the best reach only **68% accuracy at 500 simultaneous instructions**. There are distinct degradation patterns and a **bias toward earlier instructions** (primacy). — [arXiv:2507.11538](https://arxiv.org/abs/2507.11538)
- **Chroma, "Context Rot"** (2025-07-14, older). Across 18 models, performance gets "increasingly unreliable as input length grows". A single distractor hurts, and models did much better on focused prompts (about 300 tokens) than on full ones (about 113k tokens). — [Chroma research](https://www.trychroma.com/research/context-rot)
- **"Lost in the Middle"** (Liu et al., 2023, older). Models use information best at the beginning or end of the context, and worst in the middle. — [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Vendor statements match these results:
  - Claude: longer files "reduce adherence"; contradictory instructions are resolved arbitrarily; emphasis leads to over-application. — [Claude Code memory docs](https://code.claude.com/docs/en/memory); [best practices](https://code.claude.com/docs/en/best-practices)
  - Codex: "short, accurate" beats "long…vague". — [Codex best practices](https://learn.chatgpt.com/guides/best-practices)
- Conflict-resolution semantics differ by tool:
  - Codex: closer files read later override.
  - Cursor: on conflict, "earlier sources take precedence" (Team over Project over User), while nested AGENTS.md is more specific.
  - Copilot and VS Code: all sources are additive; avoid conflicts.
  - Claude: concatenated; may pick either.
  - Factory: user request > nested > root > personal.
  — [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md); [Cursor](https://cursor.com/docs/context/rules); [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions); [VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-instructions); [Claude](https://code.claude.com/docs/en/memory); [Factory](https://docs.factory.com/cli/configuration/agents-md)

### Inferences
- For 믿집, the instructions most likely to pay off are the ones agents follow literally and could not guess: exact commands (`uv run pytest`, `pnpm gen:api`), team-specific invariants (integer won, the calc-only rule, conditional UPDATE with history), and hard boundaries. Narrative overviews, such as the product flow paragraph or the parts table, are the content type ETH found unhelpful.
- Because the same rule can be read differently across tools (override vs additive vs arbitrary), a single source of truth with **no duplicated or contradictory rules** across AGENTS.md, nested files, ADRs and README matters more than wording.
- Primacy bias and context rot argue for putting the 5–10 most important rules (verification commands and never-rules) **near the top** of the file.

### Gaps
- No study found compares, within a single repo, short (≤60 lines) vs long (≥300 lines) human-written AGENTS.md. The length–adherence link is inferred from IFScale, context-rot and vendor statements.
- No study found measures the effect of Korean-language instruction files, or of mixed Korean/English files.
- No controlled study found on "MUST/NEVER vs plain wording" in instruction files, beyond Vercel's single anecdote and Anthropic's guidance.

---

## Q5. What belongs in AGENTS.md vs README/CONTRIBUTING/ADRs/docs, how to phrase restrictions, security, verification, and protecting files

### Takeaway
AGENTS.md should hold the facts every session needs and the agent cannot infer: commands, gotchas, team decisions, and boundaries. Multi-step procedures go to skills or docs. Rules for one area go to nested AGENTS.md or path-scoped rules. Rationale and history go to ADRs. Human onboarding goes to README and CONTRIBUTING. Restrictions should be specific, checkable and give the reason, ideally naming the safe alternative. Anything that must never happen (secrets, destructive commands, protected paths) needs a deterministic control: permission deny rules, hooks, Codex sandbox, CODEOWNERS or branch protection, or CI. The AGENTS.md line then serves as an explanation, not as the enforcement.

### Cited Findings
**Placement / progressive disclosure**
- Claude: keep facts needed every session. If an entry is "a multi-step procedure or only matters for one part of the codebase", move it to a skill or a path-scoped rule (`.claude/rules/*.md` with `paths:`). Personal preferences go in a git-ignored `CLAUDE.local.md`. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Codex: move task-specific guidance (planning, code review, architecture) into separate markdown files. Nested AGENTS.md files hold local rules. — [Codex best practices](https://learn.chatgpt.com/guides/best-practices)
- Cursor: "Reference files instead of copying their contents" so rules stay short and don't go stale. — [Cursor rules docs](https://cursor.com/docs/context/rules)
- Copilot: path-specific `.github/instructions/*.instructions.md` with `applyTo` (cloud agent and code review). — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- HumanLayer: an `agent_docs/` folder listed in the root file with one-line descriptions. — [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- ETH: include only what is not already in the README; overviews are not helpful. — [arXiv:2602.11988v3](https://arxiv.org/html/2602.11988v3)
- Real-world pattern: 54% of sampled files link to other `.md` docs. svelte, uv and pydantic delegate to CONTRIBUTING.md and the PR template rather than restating them. — Q3 corpus; [svelte](https://github.com/sveltejs/svelte/blob/HEAD/AGENTS.md); [pydantic](https://github.com/pydantic/pydantic/blob/HEAD/AGENTS.md)
- Claude strips block-level HTML comments (`<!-- -->`) in CLAUDE.md before injection, so maintainer notes cost no tokens. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)

**Phrasing restrictions**
- Use concrete, verifiable wording (the Claude examples in Q2). "Include the reasoning behind rules." "Show preferred and avoided patterns." — [Claude memory docs](https://code.claude.com/docs/en/memory); [VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- Codex review rules should state the behaviour to flag **and the safe path**. — [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- Factory: write checkable rules; "Be careful" is a bad rule. — [Factory](https://docs.factory.com/cli/configuration/agents-md)
- The GitHub blog's three-tier "Always / Ask first / Never" boundary list. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- Avoid ALL-CAPS emphasis on current models because it causes over-application. A rule that cannot bend belongs in a hook or deny rule. — [Claude best practices](https://code.claude.com/docs/en/best-practices)
- Real example of a "never" paired with its alternative: uv's "NEVER update all dependencies… ALWAYS use `cargo update --precise`". Kubernetes: "Never hand-edit `zz_generated.*`… Run `make update`." — [uv](https://github.com/astral-sh/uv/blob/HEAD/AGENTS.md); [kubernetes](https://github.com/kubernetes/kubernetes/blob/HEAD/AGENTS.md)

**Security and enforcement**
- Claude: `permissions.deny`, for example `Read(./.env)` and `Read(./secrets/**)`, holds in every permission mode, including auto and bypass. "your 'never' rules belong in deny rules or hooks". `ask` rules are possible, for example `Bash(git push *)`. — [Claude best practices](https://code.claude.com/docs/en/best-practices)
- Claude PreToolUse hook to block protected files: the script checks paths against patterns such as `.env`, `package-lock.json` and `.git/` and exits with **code 2** to block. Claude receives the stderr reason as feedback. — [Claude hooks guide](https://code.claude.com/docs/en/hooks-guide)
- Claude: CLAUDE.md is "context, not enforced configuration"; use a PreToolUse hook to block regardless of what Claude decides. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Codex sandbox: `read-only`, `workspace-write` (the default "Auto"), and `danger-full-access`. In `workspace-write`, `.git`, `.agents`, `.codex` and `.aws` stay read-only recursively, and network is **off by default**. Approval policies are `on-request`, `never` and `granular`; `untrusted` is retired. — [Codex agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)
- Factory: never put secrets, credentials, tokens or private hostnames in AGENTS.md; no instructions to skip validation without a narrow reason. — [Factory](https://docs.factory.com/cli/configuration/agents-md)
- Security content is rare in practice: 14.8% of 2,303 files; 20% of the Q3 sample had a security heading. — [arXiv:2511.12884](https://arxiv.org/html/2511.12884); Q3 corpus
- **"Rules File Backdoor"** (Pillar Security, **2025-03-18**, older): hidden instructions in rule files using zero-width or bidirectional Unicode affected Cursor and Copilot. These are invisible in GitHub PR review. GitHub added a hidden-Unicode warning in May 2025. Recommendation: treat AI config files with "the same scrutiny as executable code". — [Pillar Security](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents)
- Copilot code review reads custom instructions from the PR's **head branch**. — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- CODEOWNERS automatically requests reviews from owners of changed files. With "Require review from Code Owners" branch protection, an owner's approval is needed to merge. The file lives in `.github/`, the root, or `docs/`. — [GitHub Docs: CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

**Verification commands / definition of done**
- Claude: "the single most useful line in your CLAUDE.md is the command that runs" your test suite or typecheck. Enforcement before finishing is a `Stop` hook (exit 2), not a sentence. — [Claude best practices](https://code.claude.com/docs/en/best-practices)
- Codex: include "What done means and how to verify work". — [Codex best practices](https://learn.chatgpt.com/guides/best-practices)
- agents.md: if commands are listed, the agent "will attempt to execute relevant programmatic checks and fix failures before finishing". — [agents.md](https://agents.md/)
- Copilot: commands should be "validated by running it". — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- Real-world: dotnet/runtime has "Do not finish work with any tests commented out or disabled…". uv has "NEVER assume clippy warnings or test failures are pre-existing". — [dotnet/runtime](https://github.com/dotnet/runtime/blob/HEAD/.github/copilot-instructions.md); [uv](https://github.com/astral-sh/uv/blob/HEAD/AGENTS.md)

### Inferences
- For 믿집, `docker compose down -v`, committing `.env`, and push or commit without a request are exactly the "zero-exception" rules the docs say belong in deterministic controls. Examples: Claude `permissions.deny`/`ask` (`Bash(docker compose down -v*)`, `Bash(git push *)`, `Read(./.env)`), a `.gitignore` plus a secret-scan check in CI, and Codex's default sandbox (which already makes `.git` read-only). The AGENTS.md line stays as a one-line explanation for tools without such controls.
- Generated or protected files are prime candidates for a PreToolUse hook (Claude) and for CI checks that diff-regenerate (`pnpm gen:api` then `git diff --exit-code`). In 믿집 these are `lib/backend/schema.d.ts` and already-applied Alembic migrations.
- 믿집's backend layer rules (the import-direction table) are mechanical. An import-linting CI check would enforce them more reliably than prose. This is an inference; I did not research specific Python import-linter tools.
- Because the Copilot code-review agent reads the PR head branch's instructions, protecting `AGENTS.md`, `CLAUDE.md`, `.claude/**` and `.github/copilot-instructions.md` with CODEOWNERS ensures a teammate's PR cannot silently change the instructions that review it.

### Gaps
- I found no official cross-tool mechanism to mark files as "agent must not edit" inside AGENTS.md itself. Enforcement is always tool-specific: Claude hooks/permissions, Codex sandbox, Cursor/Copilot none found.
- Whether Cursor or Copilot honour any deny-list for protected paths was not researched.

---

## Q6. Maintenance: ownership, PR review, testing instruction files, keeping tools in sync

### Takeaway
Instruction files behave like configuration code. They change often, and mostly by addition: deletions are rare, so they bloat unless pruned. Vendors advise adding a rule only after a repeated mistake. Verify what each tool actually loaded with `/context`, `/memory`, `codex "Summarize the current instructions"` or `/memory show`. Audit for stale or conflicting content with `/doctor prompt-audit`. Keep one source of truth, AGENTS.md, with CLAUDE.md as an `@AGENTS.md` import. Review changes like code, with owners.

### Cited Findings
- 59–67% of context files were modified in multiple commits, with median intervals between commits of about 22–68 hours. 92% of sampled commits were substantive instruction edits. Additions dominated (66 of 100 commits), deletions were rare, and the median deletion was under 15 words. The authors say files evolve like configuration code. — [Agent READMEs, arXiv:2511.12884](https://arxiv.org/html/2511.12884)
- In the MSR study, 50% of AGENTS.md files were never changed after creation, and 6% had 10 or more commits. Change types: add instructions 78, modify 59, add sections 26, remove instructions 23, remove sections 2. — [arXiv:2510.21413](https://arxiv.org/html/2510.21413)
- When to add a rule:
  - Claude: when it repeats the same mistake a second time, when code review catches something it should know, when you retype the same correction, or when a new teammate would need the context. — [Claude memory docs (KO)](https://code.claude.com/docs/ko/memory)
  - Codex: "same mistake twice" → retrospective → update. — [Codex best practices](https://learn.chatgpt.com/guides/best-practices)
  - Cursor: add a rule when the agent repeats a mistake. — [Cursor](https://cursor.com/docs/context/rules)
- Testing and verification:
  - Claude: `/context` lists loaded memory files; the `InstructionsLoaded` hook logs which files loaded and why; `/doctor prompt-audit` reports outdated, nonexistent-reference and conflicting content. — [Claude memory docs](https://code.claude.com/docs/en/memory)
  - Codex: `codex --ask-for-approval never "Summarize the current instructions."` and `codex --cd subdir … "Show which instruction files are active."`; `-c log_dir=…`; there is no cache, so restart to reload. — [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  - Gemini: `/memory show` and `/memory reload`. — [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/)
  - ETH: evaluate context files rigorously before adoption. — [arXiv:2602.11988](https://arxiv.org/abs/2602.11988)
- Sync across tools:
  - Claude: an `@AGENTS.md` import plus Claude-only lines below it; a symlink is not recommended on Windows; `/init` and `/import` can pull in Cursor, Copilot, Windsurf and Cline rules. — [Claude memory docs](https://code.claude.com/docs/en/memory)
  - Gemini: `context.fileName`. Aider: `read:`. — [agents.md FAQ](https://agents.md/)
  - The real-world split is 26 symlinks vs 13 imports among pointer files (Q3).
- agents.md: "Treat AGENTS.md as living documentation." Jules: keep it current. — [agents.md](https://agents.md/); [Jules](https://jules.google/docs/)
- Ownership: CODEOWNERS plus "Require review from Code Owners". — [GitHub Docs: CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- Treat rule files with "the same scrutiny as executable code", and check for hidden Unicode. — [Pillar Security (2025-03)](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents)
- Factory: no temporary task notes in AGENTS.md (use an issue, PR or spec), and no stale directory inventories. — [Factory](https://docs.factory.com/cli/configuration/agents-md)

### Inferences
- The default drift is "add-only". A student team needs an explicit pruning trigger, such as each sprint or milestone, or whenever a rule becomes enforced by CI, a hook or a linter.
- Directory inventories and file lists go stale fastest. Claude's audit specifically flags references to files that no longer exist. A cheap CI step could check that every backticked path in AGENTS.md exists. This is an inference, and I found no off-the-shelf tool for it.
- HTML-comment maintainer notes are stripped by Claude only. Other tools likely send them to the model, so don't rely on that trick in a shared AGENTS.md. This is inferred from the absence of such a statement in other vendors' docs.

### Gaps
- I found no published guidance on how often to review instruction files, and no reports of student or small-team practices.
- No tool was found that unit-tests AGENTS.md compliance, apart from building your own evals (ETH, Vercel).

---

## Q7. Recommendation for 믿집: a minimal AGENTS.md (section list), size, and keeping it current

### Takeaway
Keep AGENTS.md as the single shared file, imported by CLAUDE.md. Cut it to roughly **60–100 lines (about 5–8 KB in Korean)**. Keep six blocks: purpose and pointers, commands, domain invariants, boundaries (always / ask first / never), definition of done, and the term table. Move the architecture narrative, the parts table, request-flow detail, backend and frontend file conventions, and Git or PR process to docs, CONTRIBUTING, the PR template, or nested files. Enforce the zero-exception "never" rules with permissions, hooks or CI, rather than prose alone. Everything in this section is synthesis from Q1–Q6: inferences with the supporting citations noted.

### Cited Findings (the basis for each recommendation)
- Size anchors:
  - Claude: under 200 lines. — [Claude memory](https://code.claude.com/docs/en/memory)
  - Cursor: under 500 lines per rule. — [Cursor](https://cursor.com/docs/context/rules)
  - Copilot template: at most 2 pages. — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
  - HumanLayer: under 300 lines, ideally under 60. — [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
  - Codex: 32 KiB combined. — [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  - Windsurf: 12,000 characters per file. — [Devin/Windsurf](https://docs.devin.ai/desktop/cascade/memories)
  - Real-world median: 108–135 lines; 31% of files are ≤60 lines (Q3).
- Content anchors:
  - Commands, places where the code misleads, decisions, repeated corrections. — [Claude best practices](https://code.claude.com/docs/en/best-practices)
  - Constraints, do-not rules and what "done" means. — [Codex best practices](https://learn.chatgpt.com/guides/best-practices)
  - Non-standard practices only; overviews unhelpful. — [ETH](https://arxiv.org/html/2602.11988v3)
  - Six core areas plus three-tier boundaries. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- Enforcement anchors: hooks and deny rules for "never" — [Claude best practices](https://code.claude.com/docs/en/best-practices). Codex sandbox — [Codex security](https://learn.chatgpt.com/docs/agent-approvals-security). CODEOWNERS — [GitHub Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

### Inferences

**(a) Recommended section list for the root `AGENTS.md`**, mapped against 믿집's current sections 1–7:

0. **One-line purpose and pointers (2–4 lines).** Say what the file is, and that the README covers running the app, `docs/design/` the rationale, and `docs/adr/` the decisions. Keep the current priority line (ADR > this file > habits; ask when they conflict) and the "don't retrofit unrelated code" line. *Keep, already good.*
1. **Commands (about 8–12 lines, near the top).** Use the exact local commands from section 7: `uv run pytest <target>`, `uv run ruff check`, `uv run ruff format --check`, `pnpm typecheck`, `pnpm lint`, `pnpm gen:api`, `docker compose run --rm migrate` plus `alembic check`, `docker compose config --quiet`, `caddy validate`. Note in one line what CI runs. *Move up from section 7; this is the highest-value content per Claude, Codex and the GitHub blog.*
2. **Domain invariants agents cannot infer (about 10–15 lines).** Use a compressed section 3:
   - money as integer won, rounding and VAT handled in `calc` only;
   - ㎡ stored with its basis; Seoul `date` / `timestamptz`;
   - state changes are service-only, using conditional UPDATE → 409 plus a history row in the same transaction;
   - the `calc` purity rule;
   - quote version pinning.

   *Keep; these are the "non-standard practices" ETH says context files are good for.*
3. **Architecture boundaries as rules, not description (about 6–10 lines).** Keep the layer import-direction block and the 3–4 boundary rules:
   - the frontend does no DB access, LLM calls or money math;
   - cross-feature calls go only through service public functions;
   - one documented exception;
   - LLM calls only in `app/agent/llm.py`, and agents never write to the DB.

   *Move the parts table, the request-flow walkthrough and the diagram reference to `docs/architecture/`. Claude and ETH say overviews and layout are derivable or unhelpful. Consider enforcing import direction in CI.*
4. **Boundaries: Always / Ask first / Never (about 10–15 lines).**
   - *Always*: build only the requested feature; follow existing patterns; record a changed call flow in the PR.
   - *Ask first*: new dependencies or external services; schema or migration changes; a fourth agent; prompt changes, which need eval results.
   - *Never*:
     - commit or push unless asked;
     - commit `.env`;
     - run `docker compose down -v`;
     - edit generated `schema.d.ts` by hand;
     - edit applied migrations;
     - delete, skip or weaken tests;
     - make paid LLM calls in CI;
     - put PII in logs;
     - refactor, move files or bulk-format beyond the request;
     - pre-build out-of-scope features (floor, bath, electrical, payment).

   *Consolidated from sections 1, 4, 5, 6 and 7. For each zero-exception "never", also add a deterministic control: Claude `permissions.deny`/`ask` in `.claude/settings.json`, CI checks, branch protection.*
5. **Definition of done and report format (about 5 lines).** Say "done" only when required CI passes on the latest commit, otherwise "검증 대기" (awaiting verification). The report has three parts: local commands run, what was left to CI, and what wasn't done. Keep the must-test list as one compact line: calc, state/409, authorization 404/403, input limits, EXIF removal. *Keep from section 7.*
6. **Term table (screen word ↔ code name).** *Keep.* Agents cannot infer these names from the screens, and they are the vocabulary of every task. Drop the long product-flow sentence and link to the requirements doc instead.

**Move out of the root AGENTS.md**
- Backend package and file conventions (`router/service/repository/schemas/models/client`, shared rules, async-thread offload, IntegrityError → 409, Alembic workflow) go to `backend/AGENTS.md`.
- Frontend conventions (Server Component default, `lib/api.ts`, tokens, `mj-` prefix, '-해요' tone, 360px/40px checks) go to `frontend/AGENTS.md`.
- **Claude Code caveat:** because the root CLAUDE.md exists, also add `backend/CLAUDE.md` and `frontend/CLAUDE.md`, each containing `@AGENTS.md`, or use `.claude/rules/*.md` with `paths:`. Otherwise Claude will not see the nested AGENTS.md files (Q1).
- Branch naming, squash, 2-day merge, PR ≤400 lines and the PR body fields go to `CONTRIBUTING.md` and `.github/pull_request_template.md`. Keep only the commit-title format line in AGENTS.md, because agents write commit messages. In Claude Code, the team commit format may conflict with built-in git instructions; the docs suggest the `includeGitInstructions` and `attribution` settings.
- Eval set details (20/15 split, dev:held-out 2:1) go to `evaluation/README.md` or `backend/app/agent/AGENTS.md`.
- Progress notes and decisions are already in `docs/status.md` and `docs/adr/`. Keep them out, as Factory advises: no temporary notes.

**(b) Size guidance**
- Target **60–100 lines** for the root file, a hard ceiling of **150 lines**, and **≤8 KB** in UTF-8 Korean. Nested files should each be ≤60 lines.
- Rationale:
  - every line costs attention in every session, and context files add about 20% cost (ETH);
  - instruction-following degrades as count rises (IFScale);
  - the Claude <200 and Copilot 2-page limits;
  - Korean's 3 bytes per character against Codex's byte limit;
  - well-regarded OSS exemplars run 16–50 lines.
- Order matters: put commands and never-rules in the first screen (primacy bias).

**(c) Rules for keeping it current**
1. **Add only on evidence:** a rule goes in after an agent or teammate makes the same mistake twice, or code review flags something the file should have said (Claude, Codex, Cursor).
2. **Every line must pass the test** "would an agent make a mistake without this, and can it not find it in the code or README?" Otherwise delete it or move it to docs (Claude best practices, ETH).
3. **Promote, then prune:** once a rule is enforced by CI, a linter, a hook or a permission, shrink it to a one-line pointer or delete it, because the file is not a linter (Cursor, HumanLayer, Claude).
4. **Point, don't copy:** reference `docs/…`, the ADRs, CONTRIBUTING and the PR template by path. Never paste their content (Cursor, Factory).
5. **One source of truth:** AGENTS.md is canonical; CLAUDE.md stays as `@AGENTS.md` (Windows-safe); nested files must not contradict the root. Before adding a line, check it against existing ADRs and the root file (conflicts are resolved arbitrarily or by tool-specific order).
6. **Review it like code:** put `AGENTS.md`, `**/AGENTS.md`, `CLAUDE.md`, `.claude/**` and `.github/copilot-instructions.md` in CODEOWNERS with "Require review from Code Owners". Changes go in their own `docs(agents)`-type PRs that state the mistake being prevented. Watch for hidden Unicode (Pillar).
7. **Verify loading after edits:** in Claude, run `/context`; in Codex, run `codex --ask-for-approval never "Summarize the current instructions."`. Run `/doctor prompt-audit` at each milestone to catch stale paths and conflicts.
8. **No secrets, hostnames or temporary task notes** in the file (Factory).

### Gaps
- No evidence was found specifically about student or bootcamp teams. All size and section recommendations above are extrapolations from OSS corpora, vendor docs and benchmarks.
- I could not retrieve Korean community posts (velog, tistory, company blogs) on writing AGENTS.md or CLAUDE.md. Search was unavailable, and velog's tag page renders client-side. The only Korean source is Anthropic's official Korean Claude Code docs ([code.claude.com/docs/ko/memory](https://code.claude.com/docs/ko/memory)).
- I did not research whether import-direction linters or secret scanners fit 믿집's CI. Those suggestions are inferences.

#### Web pages consulted (fetched 2026-10-29; publication dates noted where older)
- https://agents.md/
- https://github.com/agentsmd/agents.md
- https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation (2025-12-09)
- https://developers.openai.com/codex/guides/agents-md → redirected to https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://developers.openai.com/codex/learn/best-practices → redirected to https://learn.chatgpt.com/guides/best-practices
- https://developers.openai.com/codex/agent-approvals-security → redirected to https://learn.chatgpt.com/docs/agent-approvals-security
- https://developers.openai.com/codex/security → redirected to https://learn.chatgpt.com/docs/security (no relevant content)
- https://github.com/openai/codex (repo listing)
- https://openai.com/index/introducing-codex/ (403, not read)
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/ko/memory (Korean edition)
- https://code.claude.com/docs/en/best-practices
- https://code.claude.com/docs/en/hooks-guide
- https://www.anthropic.com/engineering/claude-code-best-practices (April 2025 post; now 308-redirects to the best-practices docs)
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (2025-09-29)
- https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- https://docs.github.com/en/copilot/reference/custom-instructions-support
- https://docs.github.com/en/copilot/tutorials/coding-agent/get-the-best-results
- https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/ (2025-08-28)
- https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ (2025-11-19)
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- https://cursor.com/docs/context/rules
- https://geminicli.com/docs/cli/gemini-md/
- https://docs.windsurf.com/windsurf/cascade/memories → redirected to https://docs.devin.ai/desktop/cascade/memories
- https://aider.chat/docs/usage/conventions.html
- https://jules.google/docs/
- https://docs.factory.ai/cli/configuration/agents-md → redirected to https://docs.factory.com/cli/configuration/agents-md
- https://ampcode.com/manual and https://ampcode.com/docs/customize/agents-md
- https://zed.dev/docs/ai/rules (404) and https://zed.dev/docs/ai/rules.html (404)
- https://www.humanlayer.dev/blog/writing-a-good-claude-md (2025-11-25)
- https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals (2026-01-27)
- https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents (2025-03-18)
- https://research.trychroma.com/context-rot → redirected to https://www.trychroma.com/research/context-rot (2025-07-14)
- https://arxiv.org/abs/2602.11988 and https://arxiv.org/html/2602.11988v3 (ETH, 2026-02 / v3 2026-09)
- https://arxiv.org/abs/2601.20404 (2026-01)
- https://arxiv.org/abs/2509.14744 (2025-09)
- https://arxiv.org/abs/2510.21413 and https://arxiv.org/html/2510.21413 (MSR 2026)
- https://arxiv.org/abs/2511.12884 and https://arxiv.org/html/2511.12884 (2025-11 / v2 2026-08)
- https://arxiv.org/abs/2507.11538 (2025-07)
- https://arxiv.org/abs/2307.03172 (2023, older)
- https://velog.io/tags/AGENTS.md (tag page; post list not rendered)
