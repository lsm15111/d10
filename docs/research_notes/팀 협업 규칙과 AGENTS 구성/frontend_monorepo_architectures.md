# Next.js App Router frontend architectures & full-stack monorepo layouts (JS frontend + Python backend) — survey for 믿집

> Research date: 2026-10-29. Scope: popular/praised Next.js App Router repos & templates, folder conventions, Next.js ↔ separate backend patterns, polyglot monorepo layouts & CI, testing/quality/docs conventions, ranked recommendations and a workspace-tool verdict.
>
> Method & caveats (read first):
> - Repository stars, archive flags and latest-commit dates were scraped on 2026-10-29 from each repo's github.com page (`stargazerCount`, `isArchived`) and its `commits/<branch>.atom` feed. The GitHub REST API was rate-limited by parallel agents, so this method replaced it.
> - Framework versions come from each repo's raw `package.json`, fetched the same day.
> - The shared WebSearch quota (200 per turn) ran out early. Most evidence therefore comes from WebFetch/curl of known URLs: official docs, raw GitHub files, npm registry JSON. Korean-blog coverage is thinner than intended (see Gaps).
> - Four parallel sub-researchers covered API/BFF patterns, monorepo/CI tooling, folder conventions and testing. Their findings were spot-checked: RFC 10017, the Next.js AI-agents doc, the vercel/commerce archive notice, the Next 16 blog, the Turborepo Python page and the oxlint type-aware post were all re-verified.
> - Facts older than 2025 are labelled "(older: YYYY)".
> - 믿집's own state was read (not modified) from `mitjip/frontend` and `mitjip/.github/workflows/ci.yml` to make the comparison concrete.

## Q1. Which Next.js App Router repos/templates are most popular or praised in 2025–2026, how are they structured, and how do they fetch data?

### Takeaway
The App Router reference repos that are still active and on Next 16 are mostly product codebases, not templates:
- **Polar, Onyx and Dify.** Each pairs Next 16 with a Python backend.
- **Formbricks, cal.com (now `calcom/cal.diy`), Langfuse and Umami.**
- **Vercel's newer `vercel/shop`.**
- **Two starters: Kiranism dashboard and ixartz boilerplate.**

Several famous names are now poor App Router references:
- **Archived or deprecated:** vercel/commerce and shadcn/taxonomy.
- **Stale:** create-t3-app, next-forge, bulletproof-react's Next app, nextjs/saas-starter.
- **Moved off Next.js:** Documenso, Plane web, Infisical, Twenty, Supabase Studio. Supabase Studio is mid-migration to TanStack Start.

### Cited Findings

**Current Next.js release:** `next@latest` is **16.4.3**. — [npm registry](https://registry.npmjs.org/next/latest)

**Activity and structure snapshot**

Stars and latest commit as of 2026-10-29. Next version is from each repo's package.json.

| Repo | ★ | Last commit | Next | App-Router structure highlights |
|---|---|---|---|---|
| [vercel/commerce](https://github.com/vercel/commerce) | 14,311 | 2026-10-19 | – | **Archived** (2026-10-20). README: "This repository is archived and the template is deprecated. Development has moved to vercel/shop" ([README](https://raw.githubusercontent.com/vercel/commerce/main/README.md)). Flat `app/` (`[page]`, `product/[handle]`, `search`, `api/revalidate`), `components/{cart,grid,layout,product}`, `lib/shopify` |
| [vercel/shop](https://github.com/vercel/shop) | GAP | – | 16.4.3 ([pkg](https://raw.githubusercontent.com/vercel/shop/main/package.json)) | Single app with `app/`, `components/`, `lib/`, `agent/`, `proxy.ts`, `instrumentation.ts`, `AGENTS.md` |
| [shadcn-ui/taxonomy](https://github.com/shadcn-ui/taxonomy) | 19,285 | 2026-04-20 | – | README calls it "officially archived", "an experiment", "not recommended for production", yet GitHub's `isArchived` is false. Route groups `(auth) (dashboard) (docs) (editor) (marketing)`; still has `pages/api/auth` + `middleware.ts` |
| [calcom/cal.com → calcom/cal.diy](https://github.com/calcom/cal.diy) | 49,504 | 2026-10-28 | 16.4.3 ([pkg](https://raw.githubusercontent.com/calcom/cal.com/main/apps/web/package.json)) | `github.com/calcom/cal.com` now 301-redirects to `calcom/cal.diy`. Cal.diy is a "fork of Cal.com with all enterprise/commercial code removed", 100% MIT ([README](https://raw.githubusercontent.com/calcom/cal.diy/main/README.md)). `apps/web/{app,modules,pages,proxy.ts,playwright}` plus `packages/{features,trpc,ui,prisma,…}` |
| [dubinc/dub](https://github.com/dubinc/dub) | 24,993 | 2026-10-26 | 15.5.8 ([pkg](https://raw.githubusercontent.com/dubinc/dub/main/apps/web/package.json)) | `apps/web/{app,ui,lib,playwright,tests}`; still uses `middleware.ts` and `next lint` |
| [formbricks/formbricks](https://github.com/formbricks/formbricks) | 13,186 | 2026-10-29 | 16.4.1 ([pkg](https://raw.githubusercontent.com/formbricks/formbricks/main/apps/web/package.json)) | `apps/web/{app,modules,lib}`; ~29 `modules/*` feature folders |
| [polarsource/polar](https://github.com/polarsource/polar) | 10,436 | 2026-10-29 | ^16.3.6 ([pkg](https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/package.json)) | `clients/apps/web/src/{app,components,hooks,providers,utils,proxy.ts}`; `app/(checkout) (embed) (main) api/ actions.ts` |
| [onyx-dot-app/onyx](https://github.com/onyx-dot-app/onyx) | 33,070 | 2026-10-29 | 16.4.1 ([pkg](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/package.json)) | `web/src/{app,components,ee,hooks,lib,providers,refresh-components,sections,views,proxy.ts}` |
| [langgenius/dify](https://github.com/langgenius/dify) | 159,894 | 2026-10-29 | 16.4.2 (catalog, [pnpm-workspace.yaml](https://raw.githubusercontent.com/langgenius/dify/main/pnpm-workspace.yaml)) | `web/{app,features,service,context,models,i18n,…}`; `app/(commonLayout) (shareLayout) (education) …`; `web/proxy.ts` |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | 36,697 | 2026-10-29 | 16.4.2 ([pkg](https://raw.githubusercontent.com/langfuse/langfuse/main/web/package.json)) | `web/src` has both `app/` and `pages/`, plus `features/` and `server/` |
| [umami-software/umami](https://github.com/umami-software/umami) | 39,776 | 2026-10-23 | 16.4.2 ([pkg](https://raw.githubusercontent.com/umami-software/umami/master/package.json)) | `src/{app,components,lib,queries,permissions,store,openapi}` |
| [Kiranism/next-shadcn-dashboard-starter](https://github.com/Kiranism/next-shadcn-dashboard-starter) | 7,193 | 2026-10-20 | 16.4.2 ([pkg](https://raw.githubusercontent.com/Kiranism/next-shadcn-dashboard-starter/main/package.json)) | `src/{app,components,features,lib,hooks,config}`; `src/features/{products,users,kanban,chat,auth,…}` |
| [ixartz/Next-js-Boilerplate](https://github.com/ixartz/Next-js-Boilerplate) | 13,091 | 2026-10-08 | 16.4.0 ([pkg](https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/package.json)) | `src/app/[locale]/(auth)`, `(marketing)`; `src/{components,libs,models,templates,validations}`; ships `oxlint.config.ts`, `oxfmt.config.ts`, `lefthook.yml` |
| [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | 126,880 | 2026-10-27 | 16.4.2 ([pkg](https://raw.githubusercontent.com/shadcn-ui/ui/main/apps/v4/package.json)) | `apps/v4` docs site; pnpm + turbo |
| [vercel/chatbot (ex ai-chatbot)](https://github.com/vercel/chatbot) | 21,016 | 2026-07-08 | 16.2.10 ([pkg](https://raw.githubusercontent.com/vercel/chatbot/main/package.json)) | `github.com/vercel/ai-chatbot` 301-redirects to `vercel/chatbot`. `app/ artifacts/ components/ hooks/ lib/ tests/ proxy.ts`; Biome; Playwright |
| [vercel/next-app-router-playground](https://github.com/vercel/next-app-router-playground) | 3,006 | 2026-09-09 | – | `app/` with private `_hooks`, `_internal`, `_patterns`; root `ui/`, `lib/` |
| [vercel/next-forge](https://github.com/vercel/next-forge) | 7,677 | **2026-05-28** | 16.1.6 ([pkg](https://raw.githubusercontent.com/vercel/next-forge/main/apps/app/package.json)) | Turborepo + bun; apps `api app docs email storybook studio web`; 20 packages |
| [t3-oss/create-t3-app](https://github.com/t3-oss/create-t3-app) | 29,195 | **2025-12-13** | – | Template: `src/app/_components`, `src/server/{auth,db,api/routers}`, `src/trpc/{server.ts,react.tsx}` ([docs](https://create.t3.gg/en/folder-structure-app), [tree](https://github.com/t3-oss/create-t3-app/tree/main/cli/template/base/src)) |
| [alan2207/bulletproof-react](https://github.com/alan2207/bulletproof-react) | 36,019 | 2026-05-14 | **^14.2.5** ([pkg](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/apps/nextjs-app/package.json)) | `apps/nextjs-app/src/{app,components,config,features,hooks,lib,testing,types,utils}` |
| [nextjs/saas-starter](https://github.com/nextjs/saas-starter) | 16,234 | **2025-12-11** | 15.6.0-canary.59 ([pkg](https://raw.githubusercontent.com/nextjs/saas-starter/main/package.json)) | `app/(login)/actions.ts`, `lib/{auth,db,payments}`, `middleware.ts` |
| [midday-ai/midday](https://github.com/midday-ai/midday) | 15,102 | 2026-06-13 | 16.2.1 ([pkg](https://raw.githubusercontent.com/midday-ai/midday/main/apps/dashboard/package.json)) | bun + turbo; apps `api dashboard desktop website worker`; 30+ packages |
| [openstatusHQ/openstatus](https://github.com/openstatusHQ/openstatus) | 9,241 | 2026-10-28 | catalog | 10 apps, 25 packages; `docs/adr/`, `AGENTS.md`, `DESIGN.md` |
| [unkeyed/unkey](https://github.com/unkeyed/unkey) | 5,481 | 2026-10-29 | 16.4.3 ([pkg](https://raw.githubusercontent.com/unkeyed/unkey/main/web/apps/dashboard/package.json)) | Go at the repo root; `web/` is a self-contained pnpm + turbo workspace (`web/apps/dashboard`) |
| [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) | 83,577 | 2026-10-29 | ~16.3.8 + vite 8 ([pkg](https://raw.githubusercontent.com/lobehub/lobe-chat/main/package.json)) | Has a `dev:spa: vite` script and `src/spa/`, so it runs a hybrid Next/Vite SPA |
| [mfts/papermark](https://github.com/mfts/papermark) | 9,279 | 2026-08-28 | ^14.2.35 ([pkg](https://raw.githubusercontent.com/mfts/papermark/main/package.json)) | Mixed `app/` + `pages/` |

**Repos that look like Next.js references but are not (any more)**

- **[Documenso](https://github.com/documenso/documenso)** (15,600★).
  - `apps/` is now `docs/ openpage-api/ remix/`.
  - `apps/remix` uses `react-router ^7.12.0`, `@react-router/*`, Hono and Vite — [pkg](https://raw.githubusercontent.com/documenso/documenso/main/apps/remix/package.json).
  - Its AGENTS.md says `npm run dev` starts "the React Router app (`apps/remix`)" — [AGENTS.md](https://raw.githubusercontent.com/documenso/documenso/main/AGENTS.md).
- **[Plane](https://github.com/makeplane/plane)** (61,660★). `apps/web` depends on `react-router`, `@react-router/dev` and `vite`, and has `react-router.config.ts`. No `next`. — [pkg](https://raw.githubusercontent.com/makeplane/plane/preview/apps/web/package.json)
- **[Infisical](https://github.com/Infisical/infisical)** (30,127★). `frontend/` is Vite 8 + `@tanstack/react-router` + React 19.3. — [pkg](https://raw.githubusercontent.com/Infisical/infisical/main/frontend/package.json)
- **[Twenty](https://github.com/twentyhq/twenty)** (60,060★). An Nx + yarn monorepo; `twenty-front` is a Vite app. — [pkg](https://raw.githubusercontent.com/twentyhq/twenty/main/packages/twenty-front/package.json)
- **[Supabase Studio](https://github.com/supabase/supabase)** (114,287★).
  - `apps/studio` depends on both `next` and `@tanstack/react-start` — [pkg](https://raw.githubusercontent.com/supabase/supabase/master/apps/studio/package.json).
  - Its `TANSTACK_MIGRATION.md` says "Next.js and TanStack Start run side-by-side… The Vite/TanStack build is what we run today; the Next build… stays alive as a fallback" — [doc](https://raw.githubusercontent.com/supabase/supabase/master/apps/studio/TANSTACK_MIGRATION.md).
- **[PostHog](https://github.com/PostHog/posthog)** (40,509★). `frontend/` is Vite + kea (`vite.config.mts`), not Next. — [tree](https://github.com/PostHog/posthog)

**Data-fetching and mutation patterns in the active Next 16 repos**

- **Polar (FastAPI backend)**
  - `@polar-sh/client` is generated with `openapi-typescript ^7.13.0` and `openapi-fetch` — [pkg](https://raw.githubusercontent.com/polarsource/polar/main/clients/packages/client/package.json).
  - Server side, `getServerSideAPI = cache(...)` forwards `Cookie` (all cookies), `X-Forwarded-For` and version headers to `POLAR_API_URL` — [serverside.ts](https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/src/utils/client/serverside.ts).
  - The browser calls `NEXT_PUBLIC_API_URL` cross-origin with `credentials:'include'`. There are no `/api` rewrites — [next.config.mjs](https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/next.config.mjs), [client index.ts](https://raw.githubusercontent.com/polarsource/polar/main/clients/packages/client/src/index.ts).
- **Onyx (FastAPI)**
  - `fetchSS` builds `${INTERNAL_URL}${path}`, turns `cookies()` into a `cookie` header, and uses `cache:"no-store"` — [utilsSS.ts](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/src/lib/utilsSS.ts).
  - The browser calls same-origin `/api/*`. In production, nginx strips `/api` and proxies to the API server — [nginx template](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/deployment/data/nginx/app.conf.template).
- **Dify (Flask)**
  - New `web/service/console/{browser.ts,server.ts}`. `server.ts` imports `'server-only'`, memoises request identity with `cache()`, forwards the raw cookie header plus a CSRF header, and prefers `SERVER_CONSOLE_API_PREFIX` — [server.ts](https://raw.githubusercontent.com/langgenius/dify/main/web/service/console/server.ts).
  - Built on oRPC contracts. Their `web/AGENTS.md` says: "Do not add handwritten REST helpers or DTO mirrors" — [AGENTS.md](https://raw.githubusercontent.com/langgenius/dify/main/web/AGENTS.md).
- **Formbricks**
  - Route files are thin re-exports of `modules/*/page.tsx`. `actions.ts` uses `"use server"` + `authenticatedActionClient.inputSchema(zod)` — [actions.ts](https://raw.githubusercontent.com/formbricks/formbricks/main/apps/web/modules/survey/list/actions.ts).
  - Their AGENTS.md calls Server Actions legacy; new backend work goes to `/api/v3` routes with TanStack Query — [AGENTS.md](https://raw.githubusercontent.com/formbricks/formbricks/main/AGENTS.md).
- **dub**
  - `lib/actions/*.ts`: one file per Server Action, plus `safe-action.ts`. Alongside it: `lib/swr`, `lib/zod/schemas`, `lib/api` — [lib/actions](https://github.com/dubinc/dub/tree/main/apps/web/lib/actions).
- **cal.com / cal.diy**
  - tRPC: `apps/web/app/_trpc`, `packages/trpc`.
  - Rule: `packages/features` holds framework-agnostic repositories and services and must not import `@calcom/trpc` — [architecture-features-modules.md](https://raw.githubusercontent.com/calcom/cal.com/main/agents/rules/architecture-features-modules.md).
- **nextjs/saas-starter**
  - Server Actions colocated in `app/(login)/actions.ts`, wrapped in `validatedAction` / `validatedActionWithUser` (zod) — [actions.ts](https://raw.githubusercontent.com/nextjs/saas-starter/main/app/(login)/actions.ts).
- **Kiranism starter**
  - Each feature's data layer is `types.ts`, `service.ts` ("the only file to change when swapping the backend") and `queries.ts` (React Query options and key factories).
  - Data is prefetched on the server, passed through `HydrationBoundary`, and read on the client with a suspense query.
  - Route handlers in `src/app/api` serve as a BFF proxy.
  - [AGENTS.md](https://raw.githubusercontent.com/Kiranism/next-shadcn-dashboard-starter/main/AGENTS.md)
- **vercel/shop AGENTS.md**
  - `lib/<domain>/` is split by runtime: `index.ts` (universal), `server.ts`, `request.ts` (proxy/route handlers), `client.ts`, `action.ts` (Server Actions), `types.ts`. No barrels.
  - Server Actions are treated as public endpoints and validated with zod.
  - [AGENTS.md](https://raw.githubusercontent.com/vercel/shop/main/AGENTS.md)

### Inferences
- **The best structural analogues for 믿집 are polyglot product repos on Next 16:** Polar, Onyx and Dify. Classic templates are stale, archived, Server-Actions/tRPC-centric (t3, saas-starter, next-forge), or assume a JS-only backend.
- **Popularity ≠ App Router reference quality.** Five of the largest repos people cite (Plane, Twenty, Infisical, Documenso, Supabase Studio) don't run on the App Router. Their folder layouts reflect Vite or React Router SPAs, so copying them would import non-Next conventions.
- **The 2025–2026 trend is toward explicit runtime-split files and away from implicit Server Actions.** Examples: `server.ts`/`client.ts` (Dify, vercel/shop, 믿집 already) and Formbricks moving Server Actions to legacy.

### Gaps
- vercel/shop's star count and last-commit date were not scraped.
- The reason cal.com's public repo became "cal.diy" was not found; web search quota was exhausted. Don't assert that Cal.com went closed-source.
- I found no primary blog posts explaining why Plane, Documenso and Supabase Studio left Next.js (search unavailable). The evidence is the package.json files and Supabase's migration doc only.

## Q2. Folder conventions: route groups, colocation, `features/` vs `components/` vs `lib/`, FSD with App Router, server/client boundary, where API clients and generated types live

### Takeaway
The evidence converges on one shape:
- `app/` stays routing-first. Route groups are used only for layouts or auth segments, and `_private` folders hold route-local pieces.
- Domain-grouped folders sit outside `app/`. They are named `components/<area>` (dub `ui/<area>`), `features/<x>` (bulletproof, Kiranism) or `modules/<x>` (Formbricks, cal).
- Code flows one way: app → area → shared, and areas never import each other.
- No barrel files.
- Runtime-split modules: `server.ts` with `server-only`, `client.ts`, and `'use client'` only at boundary leaves.
- Generated API types live in one place, are never hand-edited, and are never mirrored by hand-written DTOs.

Full FSD is documented for Next but awkward: it needs a re-export layer, its English and Korean docs disagree, and its linter is still beta. Borrow its rules, not its six layers.

### Cited Findings

**Next.js official guidance (docs last updated 2026-07-21)**
- "Next.js is **unopinionated** about how you organize and colocate your project files". It offers three strategies:
  - store project files outside `app`;
  - store them in top-level folders inside `app`;
  - split them by feature/route.
  - "choose a strategy that works for you and your team and be consistent". — [Project structure](https://nextjs.org/docs/app/getting-started/project-structure)
- Route groups `(folder)` are for "organizing routes by site section, intent, or team", for nested and multiple root layouts, and for scoping `loading.tsx`. Private folders `_folder` opt out of routing. They are "not required for colocation" but useful for "separating UI logic from routing logic" and "avoiding potential naming conflicts with future Next.js file conventions". — [Project structure](https://nextjs.org/docs/app/getting-started/project-structure)
- The Next 16 top-level file convention is **`proxy.ts`** ("Next.js request proxy"), replacing `middleware.ts`. — [Project structure](https://nextjs.org/docs/app/getting-started/project-structure); [Next 16 blog](https://nextjs.org/blog/next-16)
- `'use client'` is needed only on files whose components are rendered directly from Server Components. It marks the boundary, and props must be serializable (docs updated 2026-10-05). — [use client](https://nextjs.org/docs/app/api-reference/directives/use-client)
- `import 'server-only'` causes "a build error if the module is imported in the client environment". The docs also say "only the Data Access Layer should access `process.env`". — [Data security](https://nextjs.org/docs/app/guides/data-security)

**Feature-Sliced Design**
- FSD is at **v2.1**; v1.0/v0.1 are archived.
  - Layers: app → (processes, deprecated) → pages → widgets → features → entities → shared.
  - A module may only import strictly lower layers, and slices on the same layer can't import each other.
  - [FSD overview](https://feature-sliced.design/docs/get-started/overview)
- **FSD with the Next App Router, English page:**
  - Rename the FSD layers to `_app`/`_pages`. Keep Next's `app/` at the root and the FSD layers in `src/`.
  - Route files only re-export, e.g. `export { ExamplePage as default, metadata } from '@/_pages/example'`.
  - Server-only exports go in `index.server.ts`.
  - [with-nextjs (EN)](https://feature-sliced.design/docs/guides/tech/with-nextjs)
- **Conflict:** the Korean translation is out of date. It keeps `src/app`/`src/pages`, requires an empty root `pages/`, and doesn't mention `_pages`. — [with-nextjs (KR)](https://feature-sliced.design/kr/docs/guides/tech/with-nextjs)
- **v2.1 "pages-first":** keep most UI and logic in the page; move it down a layer only when several pages need it. Merge slices used only once. — [Migration from v2.0](https://feature-sliced.design/docs/guides/migration/from-v2-0)
- FSD's own anti-pattern guide suggests possibly having no `entities` layer in thin, backend-heavy clients, and putting CRUD in `shared/api`. — [Excessive entities](https://feature-sliced.design/docs/guides/issues/excessive-entities)
- **Public API vs barrels:** FSD wants an `index.ts` per slice. It also warns that barrels in `shared/ui`/`shared/lib` hurt tree-shaking and cause circular imports. — [Public API](https://feature-sliced.design/docs/reference/public-api). This conflicts with the "no barrels" rules below.
- **Steiger (FSD linter):** self-described beta, 453★, 21 rules (`fsd/forbidden-imports`, `fsd/insignificant-slice`, …); npm 0.8.1. — [steiger](https://github.com/feature-sliced/steiger), [npm](https://registry.npmjs.org/steiger/latest). The FSD docs repo has 2,405★ and was last committed 2026-10-26 — [documentation](https://github.com/feature-sliced/documentation).
- **Korean criticism:** teo.v argues there is no single right structure; move page-centred → domain-centred → feature-centred as the project matures. Commenters report that FSD boilerplate eats time. (older: 2024-09) — [velog @teo](https://velog.io/@teo/separation-of-concerns-of-frontend)

**Bulletproof React** (36,019★)
- Calls itself "an opinionated guide", not a template. — [repo](https://github.com/alan2207/bulletproof-react)
- `src/` = `app, assets, components, config, features, hooks, lib, stores, testing, types, utils`. Each feature has optional `api, components, hooks, stores, types, utils`.
- Rules:
  - Features never import each other; compose them at the app layer.
  - Code flows shared → features → app.
  - It "used to recommend barrel files" and now says import files directly, because barrels break Vite tree-shaking.
  - [project-structure.md](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/project-structure.md)
- **API layer:** one pre-configured client (`lib/api-client.ts`). Each request is its own file with types, fetcher and hook in `features/<x>/api/`. — [api-layer.md](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/api-layer.md)
- **State:** five categories; "localize the state as closely as possible". — [state-management.md](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/state-management.md)
- **Enforcement:** ESLint `import/no-restricted-paths` with one zone per feature; shared folders can't import features or app; plus `import/no-cycle` and kebab-case files via `check-file`. — [.eslintrc.cjs](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/apps/nextjs-app/.eslintrc.cjs)
- **Its Next App Router app is a hybrid** of `src/features/discussions/{api,components}` and route-local `src/app/app/_components/` and `src/app/app/discussions/{_components,__tests__}`. — [src/app/app](https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app/src/app/app), [discussions](https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app/src/app/app/discussions)

**Colocation in practice**
- **dub:** `apps/web/ui/` is grouped by product area (account, analytics, auth, customers, domains, links, modals, layout, shared, workspaces…), which is the same idea as 믿집's `components/<area>`. `app/app.dub.co/` uses route groups `(auth) (dashboard) (onboarding) …`. — [ui](https://github.com/dubinc/dub/tree/main/apps/web/ui), [app.dub.co](https://github.com/dubinc/dub/tree/main/apps/web/app/app.dub.co)
- **Formbricks:** `modules/survey/list/` holds `page.tsx, loading.tsx, actions.ts, actions.test.ts, components/, hooks/, lib/, types/`. The route file is a 2-line re-export. — [modules/survey/list](https://github.com/formbricks/formbricks/tree/main/apps/web/modules/survey/list), [route page.tsx](https://raw.githubusercontent.com/formbricks/formbricks/main/apps/web/app/(app)/workspaces/%5BworkspaceId%5D/surveys/page.tsx)
- **cal.com rules:**
  - vertical slices (`services/ repositories/ components/ tests/`);
  - features talk only through public entry points;
  - "import from the source file, not a barrel";
  - auth checks go in `page.tsx`, not `layout.tsx`.
  - [vertical-slices](https://raw.githubusercontent.com/calcom/cal.com/main/agents/rules/architecture-vertical-slices.md), [feature-boundaries](https://raw.githubusercontent.com/calcom/cal.com/main/agents/rules/architecture-feature-boundaries.md), [avoid-barrel-imports](https://raw.githubusercontent.com/calcom/cal.com/main/agents/rules/quality-avoid-barrel-imports.md), [agents/rules](https://github.com/calcom/cal.com/tree/main/agents/rules)
- **next-forge:**
  - apps don't depend on other apps;
  - "Each package should be self-contained";
  - each app has its own `env.ts`;
  - `apps/app/app/(authenticated)/components/` is colocated inside the route group.
  - [structure](https://www.next-forge.com/docs/structure), [apps/app](https://www.next-forge.com/docs/apps/app), [(authenticated)](https://github.com/vercel/next-forge/tree/main/apps/app/app/(authenticated))
- **create-t3-app:** route-local `src/app/_components/post.tsx`; server-only code in `src/server/`; tRPC split into `src/trpc/server.ts` (for RSC) and `react.tsx` (client). — [folder structure](https://create.t3.gg/en/folder-structure-app)
- **ixartz:** `src/app/[locale]/(auth)/(center)`, `(auth)/dashboard`, `(marketing)`. — [tree](https://github.com/ixartz/Next-js-Boilerplate/tree/main/src/app/%5Blocale%5D/(auth))
- **vercel/shop:**
  - `components/ui/` takes primitive props only; domain wrappers go in `components/<domain>/`.
  - `'use client'` goes as low as possible. A sub-component that needs a different directive moves to a sibling `-client.tsx`/`-server.tsx`.
  - kebab-case file names; default exports for pages, named exports for components.
  - [AGENTS.md](https://raw.githubusercontent.com/vercel/shop/main/AGENTS.md)

**Thought leaders and Korean guidance**
- **Kent C. Dodds:** "Place code as close to where it's relevant as possible"; "things that change together should be located as close as reasonable". (older: 2019) — [Colocation](https://kentcdodds.com/blog/colocation)
- **Robin Wieruch (updated 2026-05-05):**
  - Staged evolution, ending with `features/<name>` that don't cross-import, then promote to shared on second use. kebab-case; no barrels.
  - For Next.js he advises keeping feature code outside `app/` and avoiding private folders for it.
  - **Conflict:** t3, bulletproof and the Vercel playground all use `_components`.
  - [React folder structure](https://www.robinwieruch.de/react-folder-structure/)
  - Earlier post: RSC reads, Server Actions write, fetch in parallel in the page. (older: 2024-11) — [Feature-based React architecture](https://www.robinwieruch.de/react-feature-architecture/)
- **Dan Abramov:** `'use client'`/`'use server'` are module-level "doors" between environments (2025-04-25) — [What does "use client" do?](https://overreacted.io/what-does-use-client-do/). Pair a data-loading server part with an interactive client part, and pass server content as children (2025-04-22) — [Impossible Components](https://overreacted.io/impossible-components/).
- **Josh Comeau (updated 2025-05-09):** a client boundary spreads to everything it imports; "if a component can be a Server Component, it should be". — [Making sense of RSC](https://www.joshwcomeau.com/react/server-components/)
- **토스 Frontend Fundamentals, "함께 수정되는 파일을 같은 디렉토리에 두기":**
  - Grouping by type (`components/hooks/utils`) hides dependencies and leaves dead code.
  - Grouping by domain (`src/domains/<Domain>/{components,hooks,utils}` plus shared top-level folders) makes wrong cross-domain imports obvious, and lets you delete a feature by deleting its folder.
  - [code-directory](https://frontend-fundamentals.com/code-quality/code/examples/code-directory.html)
- **Toss's four criteria:** 가독성 (readability), 예측 가능성 (predictability), 응집도 (cohesion), 결합도 (coupling). "가독성과 응집도는 서로 상충할 수 있어요" (readability and cohesion can conflict). — [code quality](https://frontend-fundamentals.com/code-quality/code/)
- **Toss, "중복 코드 허용하기":** allow duplication when pages are likely to diverge. — [use-bottom-sheet](https://frontend-fundamentals.com/code-quality/code/examples/use-bottom-sheet.html). Repo: 2,003★, last commit 2026-03-08 — [toss/frontend-fundamentals](https://github.com/toss/frontend-fundamentals)

**Where API clients and generated types live**
- **Polar:** a separate package, `clients/packages/client/src/v1.ts` (committed). — [pkg](https://raw.githubusercontent.com/polarsource/polar/main/clients/packages/client/package.json)
- **full-stack-fastapi-template:** `frontend/src/client/{sdk.gen.ts,types.gen.ts,client.gen.ts}` (committed). — [tree](https://github.com/fastapi/full-stack-fastapi-template/tree/master/frontend/src/client)
- **PostHog:** orval output in `frontend/src/generated/core/{api.ts,api.schemas.ts,api.zod.ts}`. — [generated/core](https://github.com/PostHog/posthog/tree/master/frontend/src/generated/core)
- **vintasoftware:** `nextjs-frontend/app/openapi-client` (inside `app/`). — [tree](https://github.com/vintasoftware/nextjs-fastapi-template/tree/main/nextjs-frontend/app)
- **Dify:** the `@dify/contracts` package. — [server.ts](https://raw.githubusercontent.com/langgenius/dify/main/web/service/console/server.ts)

**믿집 today (read-only observation)**
- **`frontend/app/`:** `account admin login my projects samples signup start status vendor vendors`, with **no route groups**.
- **`components/`:** `admin auth my project site start ui vendors`.
- **`lib/`:** `api.ts, backend/{client.ts,server.ts,schema.d.ts}, format.ts, labels.ts, mock/, session.ts, trade-status.ts, types.ts`.
- 21 files contain `'use client'`.
- `frontend/lib/backend/server.ts` uses `cookies()` from `next/headers`, but **no file under `frontend/lib` imports `server-only`**.
- Sources: `mitjip/frontend/app`, `mitjip/frontend/components`, `mitjip/frontend/lib/backend/server.ts`. These are local files.

### Inferences
- 믿집's `components/<area>` already matches dub's `ui/<area>` and Toss's domain grouping. A big-bang move to `features/` or FSD in a 2-month project isn't justified by the evidence.
- What's missing is the *rules*: import direction, no cross-area imports, no barrels, and `server-only` on `lib/backend/server.ts`. A lint guard would help too, since bulletproof enforces with lint zones and cal with rules.
- Route groups (e.g., `(public)`, `(app)`, `(admin)`) are worth adding only if they remove duplicated layout or auth code. Next's docs frame them as layout tools, not decoration.
- Adopt a graduation rule: move a component to `components/<area>` (or `features/<area>`) only when a second route uses it. Until then keep it in the route's `_components/`. This reconciles Kent C. Dodds, FSD pages-first, and bulletproof's hybrid Next app.

### Gaps
- I could not confirm whether oxlint implements `import/no-restricted-paths`, the bulletproof zone rule. The oxlint plugin list includes `import`, but rule-level parity wasn't checked. ESLint core's `no-restricted-imports` pattern rule may be the fallback (unverified).
- I found no Korean company blog posts (당근, 카카오엔터, 우아한형제들) specifically on App Router folder structure:
  - web search was exhausted;
  - the 카카오엔터 FE blog moved to [tech.kakaoent.com](https://tech.kakaoent.com/) and the post bodies would not load.

## Q3. Patterns for Next.js talking to a separate backend (FastAPI/Django/Go): BFF, OpenAPI type generation, auth-cookie forwarding, avoiding Server Actions

### Takeaway
믿집's design is the "External HTTP APIs" model that Next.js recommends when "separate backend teams use other languages". The design is: RSC reads forward cookies to FastAPI; browser writes go same-origin to `/api`, proxied to FastAPI; there are no Server Actions; openapi-typescript generates the types. Dify (`server.ts` + `server-only` + `cache()`), Onyx (`fetchSS` + same-origin `/api` behind nginx) and Polar (`cache(getServerSideAPI)` + openapi-typescript/openapi-fetch + a CI drift check) independently converged on the same shape.

The main hardening items:
- `server-only` on `server.ts`;
- a documented rule that Set-Cookie from FastAPI cannot propagate through Server Component renders;
- explicit CSRF defence, since there are no Server Actions to provide it.

### Cited Findings

**Official Next.js guidance**
- The data-security guide names three approaches: HTTP APIs "for existing large applications and organizations", a Data Access Layer "for new projects", and component-level access for prototypes. It says: "choosing one data fetching approach and avoiding mixing them".
  - The HTTP API approach "works well when… Separate backend teams use other languages or manage APIs independently".
  - It follows a **Zero Trust** model, and its example forwards `Cookie: AUTH_TOKEN=…` from `cookies()`.
  - [Data security](https://nextjs.org/docs/app/guides/data-security) (updated 2026-10-06)
- **BFF guide:**
  - "Next.js backend capabilities are not a full backend replacement".
  - "Fetch data in Server Components directly from its source, not via Route Handlers". Route Handlers fail at build for prerendered pages and add a round trip.
  - "Server Actions are queued. Using them for data fetching introduces sequential execution."
  - Route Handlers can proxy (`app/api/[...slug]/route.ts`), as can `proxy.ts` rewrites or `next.config` `rewrites`.
  - "Do not rely on proxy alone for authentication and authorization."
  - [BFF guide](https://nextjs.org/docs/app/guides/backend-for-frontend) (updated 2026-06-25)
- **Next 16 (2025-10-21):** "`proxy.ts` replaces `middleware.ts`… runs on the Node.js runtime"; synchronous `cookies()`/`headers()` are removed; `updateTag()`/`refresh()` are Server-Actions-only. — [Next 16 blog](https://nextjs.org/blog/next-16)
- **Proxy reference (updated 2026-09-04):** Proxy is "recommended to be used as a last resort". Pass headers upstream via `NextResponse.next({request:{headers}})`. Codemod `npx @next/codemod@canary middleware-to-proxy .` — [proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)
- **Authentication guide (updated 2026-09-16):**
  - cookies should be HttpOnly, Secure, `sameSite:'lax'`, `path:'/'`;
  - Proxy should do only optimistic checks ("avoid database checks");
  - the DAL uses `import 'server-only'` + `cache(verifySession)`;
  - Route Handlers get "the same security considerations as public-facing API endpoints".
  - [Authentication](https://nextjs.org/docs/app/guides/authentication)
- **cookies() (updated 2026-06-09):** "Setting cookies is not supported during Server Component rendering"; "HTTP does not allow setting cookies after streaming starts". A `Set-Cookie` that FastAPI returns to an RSC fetch therefore never reaches the browser. — [cookies](https://nextjs.org/docs/app/api-reference/functions/cookies)
- **Cache Components:** plain `'use cache'` "can't call `cookies()`"; per-user reads use `'use cache: private'`; keep tokens out of cache-key arguments. — [Auth with Cache Components](https://nextjs.org/docs/app/guides/authentication-with-cache-components)
- **Rewrites (updated 2026-09-28):** "Rewrites act as a URL proxy" to external URLs. The docs give no timeout or streaming options. — [rewrites](https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites)
- **CSRF (older: 2023):** Server Actions get CSRF protection (POST-only + Origin/Host check); with Route Handlers "CSRF protection has to be done manually". — [Security of RSC & Actions](https://nextjs.org/blog/security-nextjs-server-components-actions); [Vercel CSRF guide](https://vercel.com/guides/understanding-csrf-attacks) (older: 2023)
- **RFC 10017, "OAuth 2.0 for Browser-Based Applications" (August 2026; title and date verified).**
  - BFF session cookies MUST be Secure + HttpOnly, SHOULD be SameSite=Strict, Path `/`, no Domain, `__Host-` prefix.
  - The BFF "MUST implement a proper CSRF defense": a custom header forcing a preflight, or double-submit.
  - Proxying BFFs MUST allowlist destinations.
  - [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017.html), [draft history](https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/)

**OpenAPI → TypeScript tooling (2026 status)**
- **openapi-typescript 7.13.0 / openapi-fetch 0.17.0 / openapi-react-query 0.5.4**, all released ~2026-02-11 with no release since.
  - Issues are restricted to collaborators. Repo 8,422★, last commit 2026-09-25.
  - [npm openapi-typescript](https://registry.npmjs.org/openapi-typescript/latest), [npm openapi-fetch](https://registry.npmjs.org/openapi-fetch/latest), [npm openapi-react-query](https://registry.npmjs.org/openapi-react-query/latest), [repo](https://github.com/openapi-ts/openapi-typescript), [releases](https://github.com/openapi-ts/openapi-typescript/releases)
- **openapi-fetch:** "6 kb", types-only. The docs recommend `noUncheckedIndexedAccess` + `tsc --noEmit` in CI — [openapi-fetch](https://openapi-ts.dev/openapi-fetch/). The CLI has `--check` ("Check that the generated types are up-to-date") — [CLI](https://openapi-ts.dev/cli). Module-level token state "should be avoided for server applications" — [middleware-auth](https://openapi-ts.dev/openapi-fetch/middleware-auth). Next.js example (no cookie-forwarding guidance) — [examples](https://openapi-ts.dev/openapi-fetch/examples). React Query wrapper — [openapi-react-query](https://openapi-ts.dev/openapi-react-query/).
- **@hey-api/openapi-ts 0.99.0** (~2026-06-24): "initial development", "pin an exact version". The output folder "is emptied on every run". Its Next.js client uses `runtimeConfigPath`. Repo 5,533★.
  - [npm](https://registry.npmjs.org/@hey-api/openapi-ts/latest), [get-started](https://heyapi.dev/openapi-ts/get-started), [output](https://heyapi.dev/openapi-ts/configuration/output), [Next.js client](https://heyapi.dev/openapi-ts/clients/next-js), [fetch client](https://heyapi.dev/openapi-ts/clients/fetch), [repo](https://github.com/hey-api/openapi-ts)
- **orval 8.45.0** (~2026-10-25): React Query/SWR/Zod/MSW/native fetch; 6,566★; last commit 2026-10-29. — [npm](https://registry.npmjs.org/orval/latest), [repo](https://github.com/orval-labs/orval)
- **kubb `@kubb/core` 5.15.1** (~2026-10-28), plugin-based. — [npm](https://registry.npmjs.org/@kubb/core/latest), [repo](https://github.com/kubb-labs/kubb)
- **openapi-typescript-codegen is unmaintained:** "migrate your projects to use @hey-api/openapi-ts" (older: 2024). — [repo](https://github.com/ferdikoomen/openapi-typescript-codegen)

**Schema-drift checks in real repos**
- **Polar** `openapi-generate-check.yml`:
  - runs on PRs touching `server/polar/**` or the client;
  - regenerates the client;
  - runs `git status --porcelain`;
  - posts the diff as a PR comment and fails with "Generated OpenAPI files are out of date".
  - [workflow](https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/openapi-generate-check.yml)
- **full-stack-fastapi-template:** a pre-commit hook `generate-frontend-sdk` runs `scripts/generate-client.sh` when backend files change. CI runs `prek` and auto-commits fixes. The generated client is committed; `openapi.json` is gitignored.
  - [.pre-commit-config.yaml](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/.pre-commit-config.yaml), [pre-commit.yml](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/.github/workflows/pre-commit.yml), [generate-client.sh](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/scripts/generate-client.sh), [frontend/.gitignore](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/frontend/.gitignore)
- **vintasoftware:** a dev-time chokidar watcher regenerates the client, and there is **no** CI drift check. — [watcher.js](https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/watcher.js), [ci.yml](https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/.github/workflows/ci.yml)
- **Umami** CI runs an OpenAPI generate/check step. — [ci.yml](https://raw.githubusercontent.com/umami-software/umami/master/.github/workflows/ci.yml)
- **믿집 already does this.** `ci.yml`:
  1. The backend job starts uvicorn and saves `openapi.json` as an artifact.
  2. The frontend job runs `openapi-typescript ../openapi.json -o lib/backend/schema.d.ts && git diff --exit-code -- lib/backend/schema.d.ts`.
  3. Then it runs typecheck, lint and build.

  (local file `mitjip/.github/workflows/ci.yml`)

**Proxy topology options seen in real repos**
- **Same-origin `/api` via a reverse proxy in production, plus Next `rewrites` in dev:**
  - Onyx uses nginx; see the [nginx template](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/deployment/data/nginx/app.conf.template), [next.config.js](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/next.config.js).
  - Dify routes `/console/api`, `/api`, `/v1` to the API and `/` to web; see the [nginx](https://raw.githubusercontent.com/langgenius/dify/main/docker/nginx/conf.d/default.conf.template).
  - 믿집 does the same: `next.config.ts` rewrites `/api/:path*` to `API_INTERNAL_URL`, and Caddy handles `/api` in production (local file `mitjip/frontend/next.config.ts`).
- **Catch-all Route Handler proxy, Onyx, dev-only.** `web/src/app/api/[...path]/route.ts` returns 404 unless `NODE_ENV=development`. It:
  - re-appends each `Set-Cookie` via `getSetCookie()`;
  - uses `duplex:"half"` and `redirect:"manual"`;
  - sets `X-Accel-Buffering:no` for streams.
  - [route.ts](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/src/app/api/%5B...path%5D/route.ts)
- **Browser calls the backend cross-origin:** Polar. — [next.config.mjs](https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/next.config.mjs)
- **Dev-only rewrites plus static export in production:** Khoj (`/api`, `/auth`, `/static` → `localhost:42110`) and LiteLLM (rewrites keyed on the `Accept` header). — [khoj next.config.mjs](https://raw.githubusercontent.com/khoj-ai/khoj/master/src/interface/web/next.config.mjs), [litellm next.config.mjs](https://raw.githubusercontent.com/BerriAI/litellm/main/ui/litellm-dashboard/next.config.mjs)
- **Vercel Python functions:** digitros/nextjs-fastapi rewrites `/api/py/:path*` to `127.0.0.1:8000` in dev (608★, last commit 2024-09-20). — [next.config.js](https://raw.githubusercontent.com/digitros/nextjs-fastapi/main/next.config.js)

**Auth and CSRF details in real repos**
- **Dify:** ky with `credentials:'include'`, plus `X-CSRF-Token` from the `csrf_token`/`__Host-csrf_token` cookie (double-submit) — [fetch.ts](https://raw.githubusercontent.com/langgenius/dify/main/web/service/fetch.ts). Cookie-based `POST /refresh-token` with an in-tab lock and a cross-tab flag — [refresh-token.ts](https://raw.githubusercontent.com/langgenius/dify/main/web/service/refresh-token.ts). `dev-proxy.config.ts` maps the CSRF cookie to a header — [dev-proxy](https://raw.githubusercontent.com/langgenius/dify/main/web/dev-proxy.config.ts).
- **Polar** `unwrap()` throws typed `UnauthorizedResponseError`/`NotFoundResponseError`/`TooManyRequestsResponseError`; there is an `isValidationError` guard for FastAPI `{loc,msg,type}`. — [client index.ts](https://raw.githubusercontent.com/polarsource/polar/main/clients/packages/client/src/index.ts)
- **Anti-patterns:**
  - **full-stack-fastapi-template** keeps the JWT in `localStorage` and redirects on 401/403 via `window.location`. It is also a Vite SPA, not Next, and uses `@hey-api/openapi-ts` 0.97.3 with the axios client. — [main.tsx](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/frontend/src/main.tsx), [openapi-ts.config.ts](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/frontend/openapi-ts.config.ts), [frontend package.json](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/frontend/package.json)
  - **vintasoftware/nextjs-fastapi-template** (329★, last commit 2025-12-17, Next 16.0.8):
    - login is a Server Action that calls `cookies().set("accessToken", token)` with **no httpOnly/secure/sameSite flags**;
    - its `proxy.ts` calls the backend `usersCurrentUser`, which contradicts the docs' "optimistic checks" advice;
    - the README says "OpenAPI-fetch" but the code uses hey-api (conflict).
    - [login-action.ts](https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/components/actions/login-action.ts), [items-action.ts](https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/components/actions/items-action.ts), [proxy.ts](https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/proxy.ts), [package.json](https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/package.json), [README](https://github.com/vintasoftware/nextjs-fastapi-template), [Vinta blog (2026-02-19)](https://www.vintasoftware.com/blog/next-js-fastapi-template)
  - **unfoldadmin/turbo** (Django + Next ^16.0.10, 413★) still uses deprecated `openapi-typescript-codegen ^0.29.0`, plus next-auth Bearer tokens and Server Actions in `apps/web/actions/`. — [repo](https://github.com/unfoldadmin/turbo), [frontend package.json](https://raw.githubusercontent.com/unfoldadmin/turbo/main/frontend/package.json), [lib/api.ts](https://raw.githubusercontent.com/unfoldadmin/turbo/main/frontend/apps/web/lib/api.ts)
- **PostHog:** the orval `apiMutator` routes generated calls through the hand-written `lib/api` — [api-orval-mutator.ts](https://raw.githubusercontent.com/PostHog/posthog/master/frontend/src/lib/api-orval-mutator.ts). File header: "Auto-generated from the Django backend OpenAPI schema" — [api.ts](https://raw.githubusercontent.com/PostHog/posthog/master/frontend/src/generated/core/api.ts).
- **Agenta:** uses a Fern-generated client, with "zod validation at the boundary" as an independent drift check, because "Fern types under-declare backend `extra="allow"` fields". — [web/AGENTS.md](https://raw.githubusercontent.com/Agenta-AI/agenta/main/web/AGENTS.md)

### Inferences
- **Keep the 믿집 design.** It is the documented Next.js pattern for non-JS backends, and three large polyglot repos converged on it. Avoiding Server Actions is defensible:
  - the docs frame them as mutation-only and queued;
  - Formbricks now calls them legacy;
  - with a FastAPI owner of auth, they would duplicate authorization.

  The trade-off: 믿집 gives up their built-in Origin check and must add its own CSRF defence. Options are a required custom header (e.g., `X-Requested-With`) checked by FastAPI, double-submit like Dify, and an Origin check. `__Host-` and SameSite cookies are already partly in place (`__Host-mj_sid` in production per `server.ts` comments).
- **Write the Set-Cookie rule into AGENTS.md:**
  - login, logout and refresh happen only via browser → `/api`;
  - Server Components treat 401 as "redirect to login", not "refresh".

  This follows from the `cookies()` docs.
- **Add `import 'server-only'` to `lib/backend/server.ts`.** Dify does; Polar doesn't. It costs nothing and turns a leak into a build error.
- **openapi-typescript quality is fine.** The maintenance slowdown (no release since Feb 2026) is a watch item, not a reason to switch. Pin the version. Fallback is orval (most active) if Zod/MSW generation is wanted later. hey-api is pre-1.0 and must be pinned exactly.

### Gaps
- No independent 2025–26 engineering-blog posts on "Next.js as BFF for FastAPI/Django/Go" were found (search exhausted). The strongest sources are official docs, RFC 10017 and repo code.
- No official statement says "avoid Server Actions with a separate backend". This is an inference from the docs' framing.
- Streaming/SSE and timeout behaviour of `next.config` rewrites is undocumented. 믿집's chatbot streaming via rewrites in dev should be tested; Caddy handles production.
- 믿집's `next.config.ts` uses `experimental.proxyClientMaxBodySize: "25mb"` for rewrite bodies. I did not find its docs page in this pass.

## Q4. Monorepo layout for a JS frontend + Python backend: plain folders vs pnpm workspaces / Turborepo / Nx / moon / Pants; CI split by path; what popular polyglot repos do

### Takeaway
None of the 11 large polyglot repos inspected runs Python through Turborepo or Nx. uv is now near-universal for the Python side. A JS task runner (Turborepo) appears only where there are many JS packages: Plane, Polar, PostHog. Even then Plane explicitly excludes its Django app from the pnpm workspace, and Polar and Unkey nest a self-contained JS workspace (`clients/`, `web/`) inside a polyglot repo. CI is split by path filters plus one aggregator check, not by a build tool.

For 믿집 (one JS package and one Python package, already on uv), keep the plain-folder monorepo. Do not adopt Turborepo/Nx/pnpm workspaces now.

### Cited Findings

**What the tools are (official docs)**
- **Turborepo**
  - It is built on package-manager workspaces: root `package.json`, `pnpm-workspace.yaml`, root `turbo.json`, a single lockfile. Nested packages are an error. — [Structuring a repository](https://turborepo.dev/docs/crafting-your-repository/structuring-a-repository)
  - Non-JS code is wrapped in a `package.json`. Turbo "does not read `.csproj` references". — [Multi-language](https://turborepo.dev/docs/guides/multi-language)
  - Native Python/uv: "uv support is experimental and can change at any time" (verified). It needs `futureFlags.experimentalPythonWorkspaces`. — [Python guide](https://turborepo.dev/docs/guides/tools/python)
  - `--affected` equals `--filter=...[main...HEAD]`; a shallow clone makes everything count as affected. — [run reference](https://turborepo.dev/docs/reference/run)
  - `turbo prune --docker` exists because "unrelated changes can make Docker do unnecessary work". — [prune](https://turborepo.dev/docs/reference/prune), [Docker guide](https://turborepo.dev/docs/guides/tools/docker)
  - It "can be incrementally adopted", but `dev` "doesn't provide much value in a single-package workspace". — [Add to existing repo](https://turborepo.dev/docs/getting-started/add-to-existing-repository)
  - Vercel Remote Cache is free on all plans. — [Remote caching](https://turborepo.dev/docs/core-concepts/remote-caching)
  - The docs home calls Turbo "the build system for coding agents". — [docs](https://turborepo.dev/docs)
  - Repo: 31,272★, last commit 2026-10-29 — [vercel/turborepo](https://github.com/vercel/turborepo).
- **Nx**
  - "works with any language or toolchain". Python is via the community plugin `@nxlv/python` (uv/Poetry). — [multi-language](https://nx.dev/docs/features/multi-language-support), [@nxlv/python README](https://cdn.jsdelivr.net/npm/@nxlv/python@23.0.0/README.md)
  - Inferred tasks since Nx 18. — [inferred tasks](https://nx.dev/docs/concepts/inferred-tasks)
  - `nx affected` needs `fetch-depth: 0` and `nrwl/nx-set-shas`. — [affected](https://nx.dev/docs/features/ci-features/affected)
  - The Nx Cloud Hobby tier is free. — [pricing](https://nx.dev/pricing)
  - Repo: 29,435★ — [nrwl/nx](https://github.com/nrwl/nx).
- **moon:** the v2 RC (2026-01-26) says "the Python toolchain will be marked as unstable for a little while longer". — [moon v2 RC](https://moonrepo.dev/blog/moon-v2-rc). Repo: 4,171★ — [moonrepo/moon](https://github.com/moonrepo/moon).
- **Pants:** "Javascript support is beta stage". — [Pants JS overview](https://www.pantsbuild.org/dev/docs/javascript/overview). Repo: 3,854★ — [pantsbuild/pants](https://github.com/pantsbuild/pants).
- **pnpm workspaces:** `pnpm-workspace.yaml`, `workspace:*`, one root lockfile — [workspaces](https://pnpm.io/workspaces). Catalogs share version ranges — [catalogs](https://pnpm.io/catalogs).
- **uv workspaces:** one shared `uv.lock`, for "multiple interconnected packages", and "not suited" to members with conflicting requirements. — [uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- **monorepo.tools** is vendor-authored ("© 2026 Nx and Contributors"). — [monorepo.tools](https://monorepo.tools/)
- **Next.js standalone in a monorepo:** tracing defaults to the app folder, and files outside it need `outputFileTracingRoot`. — [output](https://nextjs.org/docs/app/api-reference/config/next-config-js/output)

**What real polyglot repos do**

| Repo | JS root setup | Task runner | Python | CI split |
|---|---|---|---|---|
| [makeplane/plane](https://github.com/makeplane/plane) 61.7k★ | Root pnpm workspace + `turbo.json` ([pkg](https://raw.githubusercontent.com/makeplane/plane/preview/package.json), [ws](https://raw.githubusercontent.com/makeplane/plane/preview/pnpm-workspace.yaml), [turbo](https://raw.githubusercontent.com/makeplane/plane/preview/turbo.json)) | Turbo for JS only; `"!apps/api"` excluded | Django `apps/api` with uv ([tree](https://github.com/makeplane/plane/tree/preview/apps/api)) | [api workflow](https://raw.githubusercontent.com/makeplane/plane/preview/.github/workflows/pull-request-build-lint-api.yml) has `paths: apps/api/**`; [web workflow](https://raw.githubusercontent.com/makeplane/plane/preview/.github/workflows/pull-request-build-lint-web-apps.yml) runs `turbo --affected` |
| [polarsource/polar](https://github.com/polarsource/polar) 10.4k★ | Root `package.json` only `{private, packageManager}` ([pkg](https://raw.githubusercontent.com/polarsource/polar/main/package.json)); real pnpm + turbo workspace in `clients/` ([tree](https://github.com/polarsource/polar/tree/main/clients)) | Turbo inside `clients/` | `server/` uv | [test_server.yaml](https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/test_server.yaml) / [test_client.yaml](https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/test_client.yaml): `dorny/paths-filter` + a status job that passes on success or skip |
| [PostHog/posthog](https://github.com/PostHog/posthog) 40.5k★ | Root pnpm workspace ([pkg](https://raw.githubusercontent.com/PostHog/posthog/master/package.json), [ws](https://raw.githubusercontent.com/PostHog/posthog/master/pnpm-workspace.yaml)) | Turbo only as `--affected --dry-run` ([ci-turbo](https://raw.githubusercontent.com/PostHog/posthog/master/.github/workflows/ci-turbo.yml)) | uv | 100+ `ci-*.yml`; vendored paths-filter ([ci-paths-filter](https://raw.githubusercontent.com/PostHog/posthog/master/.github/workflows/ci-paths-filter.yml), [ci-python](https://raw.githubusercontent.com/PostHog/posthog/master/.github/workflows/ci-python.yml)) |
| [langgenius/dify](https://github.com/langgenius/dify) ~160k★ | Root pnpm workspace, strict catalog ([pkg](https://raw.githubusercontent.com/langgenius/dify/main/package.json), [ws](https://raw.githubusercontent.com/langgenius/dify/main/pnpm-workspace.yaml)) | None (vite-plus `vp run`) | `api/` uv ([tree](https://github.com/langgenius/dify/tree/main/api)) | [main-ci.yml](https://raw.githubusercontent.com/langgenius/dify/main/.github/workflows/main-ci.yml): `dorny/paths-filter@v4.0.3` → reusable workflows + finalizers |
| [onyx-dot-app/onyx](https://github.com/onyx-dot-app/onyx) 33.1k★ | Root bun workspaces for widget/desktop; `web/` has its own lockfile ([pkg](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/package.json)) | None; `Makefile` | Root `pyproject.toml` + uv workspace ([pyproject](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/pyproject.toml)) | ~52 `pr-*.yml` ([workflows](https://github.com/onyx-dot-app/onyx/tree/main/.github/workflows), [pr-jest-tests](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.github/workflows/pr-jest-tests.yml)) |
| [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) 46.1k★ | Root bun workspaces `["frontend","packages/*"]` ([pkg](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/package.json)) | None | Root uv workspace `members=["backend"]` ([pyproject](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/pyproject.toml)) | [test-backend.yml](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/.github/workflows/test-backend.yml) (coverage ≥90%); [playwright.yml](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/.github/workflows/playwright.yml): paths-filter + `re-actors/alls-green` |
| [getsentry/sentry](https://github.com/getsentry/sentry) 45.7k★ | Root pnpm workspace ([pkg](https://raw.githubusercontent.com/getsentry/sentry/master/package.json), [ws](https://raw.githubusercontent.com/getsentry/sentry/master/pnpm-workspace.yaml)) | None | Root Python | [frontend.yml](https://raw.githubusercontent.com/getsentry/sentry/master/.github/workflows/frontend.yml): paths-filter + one required check ([workflows](https://github.com/getsentry/sentry/tree/master/.github/workflows)) |
| [apache/superset](https://github.com/apache/superset) 75.4k★ | JS in `superset-frontend/` | None | Root Python + `Makefile` | [superset-frontend.yml](https://raw.githubusercontent.com/apache/superset/master/.github/workflows/superset-frontend.yml) gated by a local change-detector ([workflows](https://github.com/apache/superset/tree/master/.github/workflows)) |
| [open-webui/open-webui](https://github.com/open-webui/open-webui) 157k★ | Root SvelteKit `package.json` | None; `Makefile` | `backend/` + root uv | Simplest split: [backend.yaml](https://raw.githubusercontent.com/open-webui/open-webui/main/.github/workflows/backend.yaml) `paths:`, [frontend.yaml](https://raw.githubusercontent.com/open-webui/open-webui/main/.github/workflows/frontend.yaml) `paths-ignore:` ([workflows](https://github.com/open-webui/open-webui/tree/main/.github/workflows)) |
| [langflow-ai/langflow](https://github.com/langflow-ai/langflow) 156k★ | Minimal root `package.json` ([pkg](https://raw.githubusercontent.com/langflow-ai/langflow/main/package.json)) | None; Makefiles | Large uv workspace ([pyproject](https://raw.githubusercontent.com/langflow-ai/langflow/main/pyproject.toml)) | [ci.yml](https://raw.githubusercontent.com/langflow-ai/langflow/main/.github/workflows/ci.yml): paths-filter → reusable workflows + "CI Success" aggregator ([workflows](https://github.com/langflow-ai/langflow/tree/main/.github/workflows)) |
| [unkeyed/unkey](https://github.com/unkeyed/unkey) 5.5k★ (Go backend) | `web/` is a self-contained pnpm + turbo workspace; Go at root | Turbo inside `web/` | (Go) | GAP |
| [mlflow/mlflow](https://github.com/mlflow/mlflow) 28.6k★ | No root `package.json` | None | Root uv | GAP |

**CI mechanics**
- **Workflow-level `paths`/`paths-ignore`:**
  - "If at least one path matches… the workflow runs".
  - You can't use both filters for the same event.
  - The changed-file limit is 3,000.
  - [Workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)
- **Required-check pitfall:** a workflow skipped by a path filter leaves required checks "Pending" and blocks merging. A *job* skipped via `if:` reports Success. — [Troubleshooting required checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks)
- **`dorny/paths-filter`** (v4, 3,381★, last commit 2026-09-27) filters at job/step level; outputs are strings, so compare with `== 'true'`. — [dorny/paths-filter](https://github.com/dorny/paths-filter)
- **`re-actors/alls-green`** gives one required check over `needs`, with `allowed-skips`. — [alls-green](https://github.com/re-actors/alls-green)
- **믿집 CI today:**
  - one `ci.yml` and no path filters;
  - `frontend` has `needs: backend`, because the frontend drift check consumes the backend's `openapi.json` artifact;
  - backend runs ruff and pytest against Postgres 17 and Redis 8 service containers, with `uv sync --locked`.
  - (local file `mitjip/.github/workflows/ci.yml`)

**Korean and industry experience reports**
- **Toss:** a 200+ service monorepo (50–60 contributors, 60+ PRs a day) needed custom infrastructure:
  - CircleCI dynamic per-service pipelines;
  - pre-cloned base images (checkout went from ~36 min to ~22 s);
  - Yarn-PnP standalone bundling (images went from ~4 GB to ~200 MB).

  (older: 2024-06) — [toss.tech monorepo-pipeline](https://toss.tech/article/monorepo-pipeline). Yarn Berry workspaces (older: 2021) — [toss.tech yarn berry](https://toss.tech/article/node-modules-and-yarn-berry).
- **우아한형제들:** a Yarn Berry workspace frontend monorepo. Benefits: shared UI and types. Costs: per-project dependency declarations, ESLint/tsconfig overrides, editor SDKs, "a lot of trial and error" migrating CI/CD. (older: 2022) — [techblog.woowahan.com/7976](https://techblog.woowahan.com/7976/)
- **LINE:** adopting Turborepo for 6 JS packages took only `package.json` and `turbo.json` edits; a cached re-run took ~7 min → 0.64 s. (older: 2022) — [LINE Engineering](https://engineering.linecorp.com/ko/blog/monorepo-with-turborepo)

### Inferences
- **Turborepo/Nx would have nothing to orchestrate in 믿집.** A task graph and cache pay off with several interdependent JS packages (LINE: 6; Plane: 6 apps + 14 packages). 믿집 has one Next app and one FastAPI app, and their dependency is already modelled explicitly: OpenAPI artifact → drift check.
- **Turbo's Python support is experimental; Nx's Python plugin is community-maintained.** Both would add config the team must learn, with no caching win on a ~2-month timeline.
- **Moving to a root pnpm workspace has real migration costs.** It would mean moving the lockfile and changing Docker build contexts and `outputFileTracingRoot` for `output: "standalone"`. That is pure cost now.
- **Path-filtered CI is optional for 믿집.** The frontend job depends on the backend's schema artifact, so filtering out backend on frontend-only PRs breaks the drift check unless the schema is committed. A committed `openapi.json` would enable it, as vintasoftware does.

  If CI time becomes painful, the simplest valid split is: a `changes` job with dorny/paths-filter, then backend and frontend gated jobs, then one `ci-ok` aggregator as the sole required check. Sentry, Langflow, Polar, Dify and the FastAPI template all use this pattern.
- **A root task entrypoint (Makefile/justfile) is what Onyx, Open WebUI, Langflow, Superset and Dify use instead of a monorepo tool.** On Windows, `make` isn't native, so a documented `pnpm -C frontend …` / `uv --directory backend run …` / `docker compose …` command table in AGENTS.md may be simpler.

### Gaps
- No Korean posts from 당근/카카오/네이버 D2 on monorepo adoption could be retrieved. The D2 fetch was blocked; the others were never found because search ran out.
- Matt Klein's "Monorepos: Please don't!" (Medium) returned 403. I found no reputable "small team doesn't need a monorepo tool" essay to cite. The verdict rests on the tool docs and repo practice.
- The CI for MLflow and Unkey was not inspected.

## Q5. Testing and quality conventions in those repos (Playwright/Vitest, lint configs, Storybook) and how they document architecture

### Takeaway
The 2026 default for Next.js repos is Vitest for unit tests and Playwright for E2E: Vitest in 13 of 20 repos, Playwright in 13, Cypress in none. E2E runs against `next build && next start`, with the backend in compose or service containers.

Linting is split three ways: ESLint 8, oxlint 6 and Biome 5. Oxlint plus oxfmt is common among Next + Python repos (Polar, Onyx, Plane, Dify, ixartz).

Next 16 removed `next lint`, and `next build` no longer lints, so lint must be its own CI step. 믿집 already does this.

Architecture is increasingly documented in AGENTS.md: root index plus nested per-area files (Polar, Dify, cal). Standalone ARCHITECTURE.md is rarer but exists (Documenso, LiteLLM). Next.js 16.3+ itself manages an AGENTS.md block.

### Cited Findings

**Official guidance**
- **Next.js testing:**
  - For async Server Components, "we recommend using End-to-End Testing over Unit Testing". — [Testing](https://nextjs.org/docs/app/guides/testing)
  - "Vitest currently does not support" async Server Components. Setup: `vitest @vitejs/plugin-react jsdom @testing-library/react vite-tsconfig-paths`. — [Vitest guide](https://nextjs.org/docs/app/guides/testing/vitest)
  - Playwright: test against production builds; `webServer` is supported. — [Playwright guide](https://nextjs.org/docs/app/guides/testing/playwright)
- **Next 16 lint changes:**
  - `next lint` removed: "Use Biome or ESLint directly; `next build` no longer runs linting". Codemod `next-lint-to-eslint-cli`. — [Next 16 blog](https://nextjs.org/blog/next-16) (verified)
  - "Scripts and CI no longer invoke `next lint`; linting runs separately". — [v16 upgrade guide](https://nextjs.org/docs/app/guides/upgrading/version-16)
  - `create-next-app` offers ESLint/Biome/None, with no oxlint option. — [create-next-app](https://nextjs.org/docs/app/api-reference/cli/create-next-app), [ESLint config](https://nextjs.org/docs/app/api-reference/config/eslint)
- **Oxlint timeline:**
  - stable v1.0 on 2025-06-10 — [blog post](https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2025-06-10-oxlint-stable.md);
  - **type-aware linting stable 2026-07-22** (tsgolint v7 tracking TypeScript 7.0.2, 59 of 61 typescript-eslint type-aware rules; verified) — [blog post](https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2026-07-22-type-aware-linting-stable.md);
  - JS plugins alpha 2026-03-11, with known out-of-memory problems on Windows — [blog post](https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2026-03-11-oxlint-js-plugins-alpha.md);
  - oxfmt beta 2026-02-24 (100% Prettier JS/TS conformance, Tailwind class sorting) — [blog post](https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2026-02-24-oxfmt-beta.md);
  - React Compiler rules 2026-08-18 — [blog post](https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2026-08-18-react-compiler-support.md);
  - blog index — [oxc-project.github.io blog dir](https://github.com/oxc-project/oxc-project.github.io/tree/main/src/blog), [oxc.rs blog](https://oxc.rs/blog/).
- **Oxlint today:** npm 1.90.0 — [npm](https://registry.npmjs.org/oxlint/latest); repo [oxc-project/oxc](https://github.com/oxc-project/oxc) 23,262★.
  - 872 rules; `@oxlint/migrate` — [linter docs](https://oxc.rs/docs/guide/usage/linter.html).
  - Default plugins are `eslint, typescript, unicorn, oxc`. `react`, `nextjs`, `jsx-a11y`, `import` and `vitest` are opt-in, and **setting `plugins` overwrites the defaults**. — [plugins](https://oxc.rs/docs/guide/usage/linter/plugins.html)
- **Biome:** v2 on 2025-06-17 (type-aware without tsc) — [Biome v2](https://biomejs.dev/blog/biome-v2/); v2.6 on 2026-10-15 (JS plugins preview) — [Biome v2.6](https://biomejs.dev/blog/biome-v2-6/), [blog](https://biomejs.dev/blog/).

**What repos use**

| Repo | Unit | E2E | Storybook | Lint/format | Hooks | Source |
|---|---|---|---|---|---|---|
| cal.com | Vitest 4.1.8 | Playwright 1.57; label-gated `ready-for-e2e`, 8 shards | – | Biome 2.3.10 | husky + lint-staged | [pkg](https://raw.githubusercontent.com/calcom/cal.com/main/package.json), [e2e.yml](https://raw.githubusercontent.com/calcom/cal.com/main/.github/workflows/e2e.yml), [pr.yml](https://raw.githubusercontent.com/calcom/cal.com/main/.github/workflows/pr.yml), [workflows](https://github.com/calcom/cal.com/tree/main/.github/workflows) |
| dub | Vitest 4.0.8 | Playwright ^1.52 | – | ESLint 8 + Prettier (`next lint`) | – | [pkg](https://raw.githubusercontent.com/dubinc/dub/main/apps/web/package.json), [root pkg](https://raw.githubusercontent.com/dubinc/dub/main/package.json) |
| formbricks | Vitest | Playwright + axe | yes (Chromatic) | ESLint 9 + Prettier | husky + lint-staged | [pkg](https://raw.githubusercontent.com/formbricks/formbricks/main/package.json), [e2e.yml](https://raw.githubusercontent.com/formbricks/formbricks/main/.github/workflows/e2e.yml), [workflows](https://github.com/formbricks/formbricks/tree/main/.github/workflows) |
| documenso | GAP | Playwright 1.64 | – | Biome 2.4.8 | husky + commitlint | [pkg](https://raw.githubusercontent.com/documenso/documenso/main/package.json), [e2e-tests.yml](https://raw.githubusercontent.com/documenso/documenso/main/.github/workflows/e2e-tests.yml), [workflows](https://github.com/documenso/documenso/tree/main/.github/workflows) |
| next-forge | Vitest ^4.0.18 | – | app | Biome + Ultracite | – | [pkg](https://raw.githubusercontent.com/vercel/next-forge/main/package.json) |
| create-t3-app (CLI) | – | – | – | ESLint 9 + Prettier | – | [pkg](https://raw.githubusercontent.com/t3-oss/create-t3-app/main/package.json) |
| bulletproof nextjs-app | Vitest ^2.1 + RTL | Playwright ^1.49 | SB 8 | ESLint 8 + Prettier | husky | [pkg](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/apps/nextjs-app/package.json), [mock-server.ts](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/apps/nextjs-app/mock-server.ts) |
| nextjs/saas-starter | – | – | – | – | – | [pkg](https://raw.githubusercontent.com/nextjs/saas-starter/main/package.json) |
| ixartz boilerplate | Vitest 4.1 browser mode | Playwright 1.62 (switches to `start` on CI) | SB 10 | **oxlint 1.78 + oxfmt + tsgolint** | lefthook | [pkg](https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/package.json), [CI.yml](https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/.github/workflows/CI.yml), [lefthook.yml](https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/lefthook.yml), [playwright.config.ts](https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/playwright.config.ts), [workflows](https://github.com/ixartz/Next-js-Boilerplate/tree/main/.github/workflows) |
| polar clients | Vitest + MSW ^2.15 | Vitest/Playwright 1.63 after deploy | – | **oxlint ^1.85 + tsgolint + oxfmt** | – | [clients pkg](https://raw.githubusercontent.com/polarsource/polar/main/clients/package.json), [web pkg](https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/package.json), [test_e2e.yaml](https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/test_e2e.yaml) |
| supabase studio | Vitest + RTL + MSW | GAP | – | ESLint | GAP | [pkg](https://raw.githubusercontent.com/supabase/supabase/master/apps/studio/package.json) |
| langfuse web | Vitest ^4.1 | Playwright ^1.57 | yes | ESLint `--max-warnings 0` + Prettier | GAP | [pkg](https://raw.githubusercontent.com/langfuse/langfuse/main/web/package.json), [pipeline.yml](https://raw.githubusercontent.com/langfuse/langfuse/main/.github/workflows/pipeline.yml) |
| midday | `bun test` | – | – | Biome 2.4.10 | – | [pkg](https://raw.githubusercontent.com/midday-ai/midday/main/apps/dashboard/package.json), [root pkg](https://raw.githubusercontent.com/midday-ai/midday/main/package.json) |
| shadcn/ui | Vitest ^3.2 | – | – | ESLint 9 + Prettier | commitlint | [pkg](https://raw.githubusercontent.com/shadcn-ui/ui/main/package.json) |
| lobe-chat | Vitest 5.0 | Playwright | – | ESLint 10 + Prettier + stylelint | lint-staged | [pkg](https://raw.githubusercontent.com/lobehub/lobe-chat/main/package.json) |
| onyx web | Jest 30 + RTL | Playwright (`docker compose up --wait`, mock-LLM service) | – | **oxlint ^1.66 + oxfmt** | prek (pre-commit) incl. ruff | [pkg](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/package.json), [pr-playwright-tests.yml](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.github/workflows/pr-playwright-tests.yml), [pr-quality-checks.yml](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.github/workflows/pr-quality-checks.yml), [.pre-commit-config.yaml](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.pre-commit-config.yaml) |
| twenty (Vite, not Next) | Jest 29 | Playwright | SB 10 + msw addon | oxlint + tsgolint + Prettier | – | [front pkg](https://raw.githubusercontent.com/twentyhq/twenty/main/packages/twenty-front/package.json), [root pkg](https://raw.githubusercontent.com/twentyhq/twenty/main/package.json) |
| dify web | Vitest via `vp test` | Playwright + Cucumber vs. real API | SB 10 | **oxlint + ESLint** hybrid | GAP | [web pkg](https://raw.githubusercontent.com/langgenius/dify/main/web/package.json), [web-e2e.yml](https://raw.githubusercontent.com/langgenius/dify/main/.github/workflows/web-e2e.yml), [web-tests.yml](https://raw.githubusercontent.com/langgenius/dify/main/.github/workflows/web-tests.yml), [workflows](https://github.com/langgenius/dify/tree/main/.github/workflows) |
| umami | Vitest ^4.1 + MSW | Playwright ^1.63 (not in CI) | – | Biome ^2.5 | – | [pkg](https://raw.githubusercontent.com/umami-software/umami/master/package.json), [ci.yml](https://raw.githubusercontent.com/umami-software/umami/master/.github/workflows/ci.yml), [workflows](https://github.com/umami-software/umami/tree/master/.github/workflows) |
| plane | – | – | – | **oxlint + oxfmt** | husky + lint-staged | [pkg](https://raw.githubusercontent.com/makeplane/plane/preview/package.json) |

**MSW, Next test mode and Playwright mocking**
- **MSW + App Router.** msw#1644 was closed 2024-10-23 with "No action is needed on MSW side"; the remaining HMR blocker sits in Next.js. (older: 2024) — [msw#1644](https://github.com/mswjs/msw/issues/1644)
- The official example PR mswjs/examples#101 is still a Draft and breaks under Turbopack — [PR #101](https://github.com/mswjs/examples/pull/101). There is no `with-next` example — [examples](https://github.com/mswjs/examples/tree/main/examples). Repos therefore use MSW inside Vitest, not in-app.
- **Next `experimental.testProxy` + `next/experimental/testmode/playwright`** can mock the server's external `fetch` (the RSC → FastAPI calls). It exists only as a README. — [testmode README](https://raw.githubusercontent.com/vercel/next.js/canary/packages/next/src/experimental/testmode/playwright/README.md)
- **Playwright** `page.route()` mocks browser requests only — [mock](https://playwright.dev/docs/mock). `webServer` accepts an array, so one config can start frontend and backend — [webServer](https://playwright.dev/docs/test-webserver).

**Adoption data** (npm weekly downloads, 2026-10-21 → 10-27)
- vitest 141.7M vs jest 50.8M
- @playwright/test 86.4M vs cypress 6.5M
- eslint 169.2M, prettier 149.5M
- oxlint 33.2M, oxfmt 21.2M, @biomejs/biome 20.7M
- storybook 28.7M, msw 26.2M

Sources: [npm API batch](https://api.npmjs.org/downloads/point/last-week/vitest,jest,cypress,msw,oxlint,eslint,prettier,playwright,oxfmt,storybook), [@playwright/test](https://api.npmjs.org/downloads/point/last-week/@playwright/test), [@biomejs/biome](https://api.npmjs.org/downloads/point/last-week/@biomejs/biome).

**State of JS and Vitest**
- State of JS 2024 "used at work": Jest 7,262; Vitest 3,986; Playwright 3,674; Cypress 3,603. (older: 2024) — [SoJS 2024 testing](https://2024.stateofjs.com/en-US/libraries/testing/)
- 2025 is qualitative only: "Vitest could overtake Jest". — [SoJS 2025 testing](https://2025.stateofjs.com/en-US/libraries/testing/)
- Vitest 4 (2025-10-22) made Browser Mode stable; the latest is 5.0.5. — [Vitest 4](https://vitest.dev/blog/vitest-4), [npm](https://registry.npmjs.org/vitest/latest)

**Architecture documentation conventions**
- **matklad's ARCHITECTURE.md:** a bird's-eye view, a codemap of coarse modules, invariants ("especially absences"), layer boundaries, cross-cutting concerns. Keep it short; name files but don't link them; "Don't try to keep it synchronized with code". (older: 2021) — [ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
- **Standalone ARCHITECTURE.md exists in:**
  - **Documenso:** 1,142 words. Sections: Monorepo Structure, Tech Stack, API Architecture (V1 deprecated / V2 / internal tRPC), Background Jobs, Swappable Providers, Request Flow, Key Directories. — [ARCHITECTURE.md](https://raw.githubusercontent.com/documenso/documenso/main/ARCHITECTURE.md)
  - **LiteLLM:** request flow, data access layer, "Adding/Modifying Providers" checklist. — [ARCHITECTURE.md](https://raw.githubusercontent.com/BerriAI/litellm/main/ARCHITECTURE.md)
  - **ADR folders:** openstatus `docs/adr/`, LiteLLM `docs/adrs/`, Formbricks `docs/adr/` + `GLOSSARY.md`. — [openstatus tree](https://github.com/openstatusHQ/openstatus), [litellm tree](https://github.com/BerriAI/litellm), [formbricks AGENTS.md](https://raw.githubusercontent.com/formbricks/formbricks/main/AGENTS.md)
- **AGENTS.md:** a "README for agents", stewarded by the Agentic AI Foundation (Linux Foundation), used in 60k+ repos. The nearest AGENTS.md wins, and the user prompt overrides it. — [agents.md](https://agents.md/)
- **Next.js AI-agents guide (updated 2026-10-15; verified):**
  - since 16.2, version-matched docs ship in `node_modules/next/dist/docs/`;
  - from 16.3, `create-next-app`/`next dev` maintain an AGENTS.md block between `<!-- BEGIN:nextjs-agent-rules -->` markers ("commit it"; can be disabled via `agentRules`);
  - the dev server exposes MCP at `/_next/mcp`.
  - [AI agents](https://nextjs.org/docs/app/guides/ai-agents)
- **Nested and indexed agent docs in real repos:**
  - **Polar:** the root AGENTS.md is an index (architecture tree, binding ADRs) pointing to `server/AGENTS.md` and `clients/AGENTS.md`. Frontend rules include a 250-line file limit and no manual memoisation under React Compiler. — [root](https://raw.githubusercontent.com/polarsource/polar/main/AGENTS.md), [clients](https://raw.githubusercontent.com/polarsource/polar/main/clients/AGENTS.md)
  - **cal.com:** a short AGENTS.md plus ~40 single-rule files in `agents/rules/`. — [AGENTS.md](https://raw.githubusercontent.com/calcom/cal.com/main/AGENTS.md), [agents/README](https://raw.githubusercontent.com/calcom/cal.com/main/agents/README.md)
  - **Twenty:** `AGENTS.md` is a symlink to `CLAUDE.md` (~1,000 words). — [CLAUDE.md](https://raw.githubusercontent.com/twentyhq/twenty/main/CLAUDE.md), [AGENTS.md](https://raw.githubusercontent.com/twentyhq/twenty/main/AGENTS.md)
  - **Kiranism:** AGENTS.md plus a CLAUDE.md that links to it. — [CLAUDE.md](https://raw.githubusercontent.com/Kiranism/next-shadcn-dashboard-starter/main/CLAUDE.md)
  - **Agenta:** `web/AGENTS.md`: "Do not hand-edit generated files". — [AGENTS.md](https://raw.githubusercontent.com/Agenta-AI/agenta/main/web/AGENTS.md)
- **믿집 today:**
  - root `AGENTS.md`: 140 lines, with sections 제품 흐름 / 구조와 코드 흐름 / 돈·날짜·상태 / 에이전트 / 코드 작성 / Git·PR / 검증;
  - `CLAUDE.md`: 1 line;
  - no Next.js-managed `nextjs-agent-rules` block;
  - `frontend/node_modules/next/dist/docs/` exists (Next 16.3.8);
  - no frontend test runner in `package.json`. Scripts are `lint: oxlint app components lib`, `typecheck: tsc --noEmit`, `gen:api`.
  - (local files `mitjip/AGENTS.md`, `mitjip/frontend/package.json`)

### Inferences
- **A minimal, credible stack for 믿집:**
  1. keep oxlint, but list plugins explicitly (`eslint, typescript, unicorn, oxc, react, nextjs, jsx-a11y, import`), because setting `plugins` overrides the defaults;
  2. optionally oxfmt `--check`;
  3. keep `tsc --noEmit` and the drift check;
  4. add Vitest + RTL only for pure logic: quote/price/date calculation, label/status mapping in `lib/format.ts`, `lib/trade-status.ts`, and the draft/basket stores in `components/start/draft.ts` and `components/vendors/basket.ts`;
  5. add 2–3 Playwright smoke flows against `next build && next start`, with FastAPI and Postgres from the existing compose. Mock only the paid LLM; the CI rule is "유료 호출 0회".

  Skip Storybook, Chromatic and coverage gates.
- **Avoid oxlint JS plugins on Windows**, because of the known out-of-memory issue.
- **Documentation:** keep `AGENTS.md` as the binding rule file, and consider a nested `frontend/AGENTS.md` for frontend-only rules (the Polar/Dify pattern). Keep architecture prose in `docs/design/*.md` (`app-structure.md`, `target-architecture.md` already exist). If the team upgrades its Next usage, decide whether to accept the Next-managed AGENTS.md block or disable it via `agentRules`.

### Gaps
- Documenso unit runner, Supabase Studio E2E, and Langfuse and Dify hooks were not confirmed.
- I couldn't extract State of JS 2025 numbers (interactive charts).
- I couldn't verify whether oxlint's `import` plugin covers bulletproof-style path-zone restrictions.

## Q6. Ranked recommendation list (repo/template → what to borrow → what not to copy) and verdict on adopting a workspace tool

### Takeaway
**Verdict: keep the plain-folder monorepo; do not adopt pnpm workspaces, Turborepo, Nx, moon or Pants now.** 믿집 has one JS app and one Python app, and its cross-stack dependency (OpenAPI → `schema.d.ts`) is already enforced by CI.

Reconsider pnpm workspaces only when a second JS package appears, such as a shared UI/tokens package, a generated client package, or a second app. Use Polar's `clients/` or Unkey's `web/` nested-workspace pattern then. Reconsider Turborepo only at ≥3 interdependent JS packages or with frontend CI over ~10 minutes.

For frontend structure, borrow rules from Dify, Polar, Onyx and vercel/shop, and folder shapes from dub, bulletproof and Kiranism. Do not copy full FSD or the stale and archived templates.

### Cited Findings

**Ranked list.** Each claim is sourced in Q1–Q5; key URLs are repeated.

1. **langgenius/dify `web/`** (Next 16.4.2 + Flask) — [web/service/console/server.ts](https://raw.githubusercontent.com/langgenius/dify/main/web/service/console/server.ts), [web/AGENTS.md](https://raw.githubusercontent.com/langgenius/dify/main/web/AGENTS.md)
   - Borrow:
     - the `server.ts` (`'server-only'` + `cache()` + cookie/CSRF forwarding + internal-URL env) / `browser.ts` split;
     - the "no handwritten REST helpers or DTO mirrors" rule;
     - double-submit CSRF;
     - nginx same-origin routing;
     - paths-filter + reusable workflows.
   - Don't copy: oRPC contracts and vite-plus toolchain, a root pnpm workspace with many packages, the 20+ top-level `web/` folders.
2. **polarsource/polar** (Next ^16.3.6 + FastAPI) — [serverside.ts](https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/src/utils/client/serverside.ts), [client index.ts](https://raw.githubusercontent.com/polarsource/polar/main/clients/packages/client/src/index.ts), [openapi-generate-check.yml](https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/openapi-generate-check.yml)
   - Borrow:
     - the same generator pair (openapi-typescript + openapi-fetch);
     - `unwrap()` with typed 401/404/429 errors and an `isValidationError` guard for FastAPI 422s;
     - the drift-check workflow, which 믿집 already has in simpler form;
     - nested AGENTS.md;
     - an oxlint + oxfmt + tsgolint config package.
   - Don't copy:
     - cross-origin browser calls; 믿집's same-origin `/api` is simpler for cookies and CSRF;
     - the 10-package `clients/` turbo workspace;
     - the missing `server-only`.
3. **onyx-dot-app/onyx `web/`** (Next 16.4.1 + FastAPI) — [utilsSS.ts](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/src/lib/utilsSS.ts), [api/[...path]/route.ts](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/src/app/api/%5B...path%5D/route.ts), [pr-playwright-tests.yml](https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.github/workflows/pr-playwright-tests.yml)
   - Borrow:
     - the `fetchSS` shape;
     - same-origin `/api` via a reverse proxy, as 믿집 does with Caddy;
     - if a catch-all proxy route is ever needed, its `getSetCookie()` re-append, `duplex:'half'` and `redirect:'manual'`;
     - Playwright against `docker compose up --wait` with a mock-LLM service;
     - prek/pre-commit spanning ruff and oxlint.
   - Don't copy: bun, Jest, ~52 workflow files.
4. **vercel/shop `AGENTS.md`** (Next 16.4.3; successor of the archived vercel/commerce) — [AGENTS.md](https://raw.githubusercontent.com/vercel/shop/main/AGENTS.md)
   - Borrow:
     - file naming by runtime (`server.ts`, `client.ts`, `action.ts`, `types.ts`);
     - the `'use client'`-at-leaves rule with sibling `-client.tsx`;
     - `components/ui` with primitive props only;
     - no barrels, kebab-case.
   - Don't copy: Server-Action-centric mutations, Shopify-specific `lib/`.
5. **dubinc/dub `apps/web`** — [ui/](https://github.com/dubinc/dub/tree/main/apps/web/ui)
   - Borrow: confirmation that `ui/<product-area>` (믿집's `components/<area>`) works at scale; route groups for auth/onboarding/dashboard.
   - Don't copy: Next 15.5 + `middleware.ts` + `next lint`, the multi-domain `app.dub.co/` tree, `lib/actions` Server Actions.
6. **alan2207/bulletproof-react** (docs, not its Next 14 app) — [project-structure.md](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/project-structure.md), [.eslintrc.cjs](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/apps/nextjs-app/.eslintrc.cjs)
   - Borrow:
     - one-way imports (shared → area → app) and no cross-feature imports;
     - lint zones;
     - "import files directly, no barrels";
     - the hybrid `features/` + route `_components/` layout.
   - Don't copy: the stale Next ^14.2.5 app, React Query + MSW mock-server everywhere, ESLint 8.
7. **Kiranism/next-shadcn-dashboard-starter** (Next 16.4.2) — [AGENTS.md](https://raw.githubusercontent.com/Kiranism/next-shadcn-dashboard-starter/main/AGENTS.md)
   - Borrow: the `features/<x>/{api,components,schemas,constants}` shape, if and when an area outgrows `components/<area>`; AGENTS.md + CLAUDE.md pointer.
   - Don't copy: React Query hydrate for every read (믿집 reads in RSC), bun, BFF route handlers for everything.
8. **fastapi/full-stack-fastapi-template** — [repo](https://github.com/fastapi/full-stack-fastapi-template)
   - Borrow (backend and CI side):
     - the uv workflow;
     - the pre-commit `generate-frontend-sdk` hook idea;
     - Playwright workflow with paths-filter + `alls-green`;
     - backend coverage gate.
   - Don't copy: the Vite SPA frontend, `localStorage` JWT, hey-api axios client.
9. **makeplane/plane** — [pnpm-workspace.yaml](https://raw.githubusercontent.com/makeplane/plane/preview/pnpm-workspace.yaml), [api workflow](https://raw.githubusercontent.com/makeplane/plane/preview/.github/workflows/pull-request-build-lint-api.yml)
   - Borrow: polyglot CI split (path-filtered API workflow), oxlint + oxfmt adoption, excluding Python from any future JS workspace.
   - Don't copy: React Router web app conventions, turbo with 6 apps and 14 packages.
10. **ixartz/Next-js-Boilerplate** (Next 16.4.0) — [CI.yml](https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/.github/workflows/CI.yml), [playwright.config.ts](https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/playwright.config.ts)
    - Borrow: oxlint + oxfmt + tsgolint configs, lefthook, Playwright config that uses `start` on CI, `(auth)`/`(marketing)` route groups.
    - Don't copy: its everything-included stack (i18n, Sentry, Checkly, Storybook, Clerk, knip).
11. **formbricks / cal.com (cal.diy)** — [formbricks AGENTS.md](https://raw.githubusercontent.com/formbricks/formbricks/main/AGENTS.md), [cal agents/rules](https://github.com/calcom/cal.com/tree/main/agents/rules)
    - Borrow:
      - thin route files that re-export `modules/*`, if `app/` gets crowded;
      - the cal rules "auth in page.tsx not layout.tsx" and "no barrel imports";
      - Formbricks' "no direct `process.env` in app code".
    - Don't copy: their scale (29 modules, ~40 rule files, 5,000-word AGENTS.md), tRPC, Server Actions.
12. **create-t3-app / nextjs/saas-starter / next-forge** — [t3 folder structure](https://create.t3.gg/en/folder-structure-app), [saas-starter](https://github.com/nextjs/saas-starter), [next-forge structure](https://www.next-forge.com/docs/structure)
    - Borrow: `_components` colocation (t3); next-forge's "packages self-contained / apps don't depend on apps" rule, as a future guideline.
    - Don't copy: tRPC or Server Actions as the data layer (FastAPI owns it), Turborepo for a single app. All three are stale (last commits 2025-12 to 2026-05).

**Do not use as references**
- **vercel/commerce:** archived 2026-10-20 — [README](https://raw.githubusercontent.com/vercel/commerce/main/README.md)
- **shadcn/taxonomy:** "officially archived… experiment" — [repo](https://github.com/shadcn-ui/taxonomy)
- **Not on the App Router:** Documenso, Plane web, Infisical, Twenty, Supabase Studio (Q1)
- **vintasoftware/nextjs-fastapi-template:** unflagged auth cookie, backend call in `proxy.ts` — [login-action.ts](https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/components/actions/login-action.ts)
- **digitros/nextjs-fastapi:** last commit 2024-09 — [repo](https://github.com/digitros/nextjs-fastapi)

**Workspace-tool evidence summary**
- **Turbo with Python is experimental** — [Turbo Python](https://turborepo.dev/docs/guides/tools/python). **Nx Python is community-maintained** — [Nx multi-language](https://nx.dev/docs/features/multi-language-support).
- **No inspected polyglot repo routes Python through a JS task runner.** Plane excludes `apps/api` from its pnpm workspace — [pnpm-workspace.yaml](https://raw.githubusercontent.com/makeplane/plane/preview/pnpm-workspace.yaml).
- **Large repos run pnpm workspaces without Turbo:** Sentry and Dify — [Sentry ws](https://raw.githubusercontent.com/getsentry/sentry/master/pnpm-workspace.yaml), [Dify ws](https://raw.githubusercontent.com/langgenius/dify/main/pnpm-workspace.yaml).
- **Self-contained JS roots inside polyglot repos:** Polar `clients/`, Unkey `web/`, Open WebUI, Superset `superset-frontend/` (Q4 table).

### Inferences
- **Recommended 믿집 frontend rules**, written as AGENTS.md / `docs/design/app-structure.md` items:
  1. `app/` holds routing, layouts and page composition only. Route-local pieces go in `app/<route>/_components/`. Promote to `components/<area>/` on second use.
  2. Areas (`start`, `project`, `vendors`, `my`, `admin`, `auth`, `site`) never import each other. Shared primitives go in `components/ui/`.
  3. The import direction is app → components/<area> → components/ui and lib. `lib/` never imports `components/` or `app/`.
  4. No barrel `index.ts` files. Use `@/` imports from the defining file.
  5. `lib/backend/server.ts` starts with `import 'server-only'` and is the only module that reads `API_INTERNAL_URL` and calls `cookies()`. `client.ts` stays browser-safe.
  6. `'use client'` only at interaction leaves. When a component needs a different directive than its parent, give it a sibling `*-client.tsx`.
  7. `schema.d.ts` is generated-only, never hand-edited, with no DTO mirrors. Use `components["schemas"][…]` aliases (`Schemas` is already exported in `server.ts`).
  8. No Server Actions. Writes go browser → `/api` → FastAPI. Login, logout and refresh never go through RSC.
  9. Design tokens live only in `globals.css` (`mj-*`); no raw hex or px in components.
  10. Add route groups only when they remove duplicated layouts or auth, e.g. `(site)` for the public header pages vs `admin/`.
- **A future `features/` migration needs a trigger:** an area gains non-UI code (hooks, request wrappers, zod schemas, stores). When that happens, rename `components/<area>` → `features/<area>/{components,hooks,api,types}`. `components/start/draft.ts` and `components/vendors/basket.ts` are early signs.
- **CI changes, ranked by value for a student team:**
  - (a) explicit oxlint plugin list;
  - (b) a Vitest job for pure logic;
  - (c) one Playwright smoke job gated to `main` or a label;
  - (d) only if needed, a paths-filter + `ci-ok` aggregator. This requires committing `openapi.json`, so the frontend drift check can run without the backend job.

### Gaps
- Team-size and CI-duration thresholds for adopting Turborepo (≥3 packages, >10 min) are a judgment from the LINE/Turbo docs evidence, not a published rule.
- No 2025–2026 Korean company post comparing plain monorepo vs workspace tools for small teams was retrieved (search exhausted).
- vercel/shop's activity metrics and any official Vercel endorsement of its AGENTS.md conventions as "recommended structure" were not verified.

### Appendix — every URL consulted

(Generated below: unique URLs cited above, plus URLs consulted but not cited because they were 404, blocked or irrelevant.)

Totals: **534 unique URLs** (344 cited inline above), spanning **64 distinct GitHub repositories**. Annotations mark pages that failed or were only seen as search snippets. Commit-feed (`.atom`) and tree URLs were fetched by script (2026-10-29) for last-commit dates and folder listings.


**GitHub repositories (root pages; stars/archive flag scraped 2026-10-29) (60)**

- <https://github.com/vercel/commerce>
- <https://github.com/vercel/shop>
- <https://github.com/shadcn-ui/taxonomy>
- <https://github.com/calcom/cal.diy>
- <https://github.com/dubinc/dub>
- <https://github.com/formbricks/formbricks>
- <https://github.com/polarsource/polar>
- <https://github.com/onyx-dot-app/onyx>
- <https://github.com/langgenius/dify>
- <https://github.com/langfuse/langfuse>
- <https://github.com/umami-software/umami>
- <https://github.com/Kiranism/next-shadcn-dashboard-starter>
- <https://github.com/ixartz/Next-js-Boilerplate>
- <https://github.com/shadcn-ui/ui>
- <https://github.com/vercel/chatbot>
- <https://github.com/vercel/next-app-router-playground>
- <https://github.com/vercel/next-forge>
- <https://github.com/t3-oss/create-t3-app>
- <https://github.com/alan2207/bulletproof-react>
- <https://github.com/nextjs/saas-starter>
- <https://github.com/midday-ai/midday>
- <https://github.com/openstatusHQ/openstatus>
- <https://github.com/unkeyed/unkey>
- <https://github.com/lobehub/lobe-chat>
- <https://github.com/mfts/papermark>
- <https://github.com/documenso/documenso>
- <https://github.com/makeplane/plane>
- <https://github.com/Infisical/infisical>
- <https://github.com/twentyhq/twenty>
- <https://github.com/supabase/supabase>
- <https://github.com/PostHog/posthog>
- <https://github.com/feature-sliced/steiger>
- <https://github.com/feature-sliced/documentation>
- <https://github.com/toss/frontend-fundamentals>
- <https://github.com/openapi-ts/openapi-typescript>
- <https://github.com/hey-api/openapi-ts>
- <https://github.com/orval-labs/orval>
- <https://github.com/kubb-labs/kubb>
- <https://github.com/ferdikoomen/openapi-typescript-codegen>
- <https://github.com/vintasoftware/nextjs-fastapi-template>
- <https://github.com/unfoldadmin/turbo>
- <https://github.com/vercel/turborepo>
- <https://github.com/nrwl/nx>
- <https://github.com/moonrepo/moon>
- <https://github.com/pantsbuild/pants>
- <https://github.com/fastapi/full-stack-fastapi-template>
- <https://github.com/getsentry/sentry>
- <https://github.com/apache/superset>
- <https://github.com/open-webui/open-webui>
- <https://github.com/langflow-ai/langflow>
- <https://github.com/mlflow/mlflow>
- <https://github.com/dorny/paths-filter>
- <https://github.com/re-actors/alls-green>
- <https://github.com/oxc-project/oxc>
- <https://github.com/BerriAI/litellm>
- <https://github.com/digitros/nextjs-fastapi>
- <https://github.com/calcom/cal.com>
- <https://github.com/khoj-ai/khoj>
- <https://github.com/Agenta-AI/agenta>
- <https://github.com/vercel/ai-chatbot>

**GitHub files, tree pages and commit feeds (356)**

- <https://raw.githubusercontent.com/vercel/commerce/main/README.md>
- <https://raw.githubusercontent.com/vercel/shop/main/package.json>
- <https://raw.githubusercontent.com/calcom/cal.com/main/apps/web/package.json>
- <https://raw.githubusercontent.com/calcom/cal.diy/main/README.md>
- <https://raw.githubusercontent.com/dubinc/dub/main/apps/web/package.json>
- <https://raw.githubusercontent.com/formbricks/formbricks/main/apps/web/package.json>
- <https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/package.json>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/package.json>
- <https://raw.githubusercontent.com/langgenius/dify/main/pnpm-workspace.yaml>
- <https://raw.githubusercontent.com/langfuse/langfuse/main/web/package.json>
- <https://raw.githubusercontent.com/umami-software/umami/master/package.json>
- <https://raw.githubusercontent.com/Kiranism/next-shadcn-dashboard-starter/main/package.json>
- <https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/package.json>
- <https://raw.githubusercontent.com/shadcn-ui/ui/main/apps/v4/package.json>
- <https://raw.githubusercontent.com/vercel/chatbot/main/package.json>
- <https://raw.githubusercontent.com/vercel/next-forge/main/apps/app/package.json>
- <https://github.com/t3-oss/create-t3-app/tree/main/cli/template/base/src>
- <https://raw.githubusercontent.com/alan2207/bulletproof-react/master/apps/nextjs-app/package.json>
- <https://raw.githubusercontent.com/nextjs/saas-starter/main/package.json>
- <https://raw.githubusercontent.com/midday-ai/midday/main/apps/dashboard/package.json>
- <https://raw.githubusercontent.com/unkeyed/unkey/main/web/apps/dashboard/package.json>
- <https://raw.githubusercontent.com/lobehub/lobe-chat/main/package.json>
- <https://raw.githubusercontent.com/mfts/papermark/main/package.json>
- <https://raw.githubusercontent.com/documenso/documenso/main/apps/remix/package.json>
- <https://raw.githubusercontent.com/documenso/documenso/main/AGENTS.md>
- <https://raw.githubusercontent.com/makeplane/plane/preview/apps/web/package.json>
- <https://raw.githubusercontent.com/Infisical/infisical/main/frontend/package.json>
- <https://raw.githubusercontent.com/twentyhq/twenty/main/packages/twenty-front/package.json>
- <https://raw.githubusercontent.com/supabase/supabase/master/apps/studio/package.json>
- <https://raw.githubusercontent.com/supabase/supabase/master/apps/studio/TANSTACK_MIGRATION.md>
- <https://raw.githubusercontent.com/polarsource/polar/main/clients/packages/client/package.json>
- <https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/src/utils/client/serverside.ts>
- <https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/next.config.mjs>
- <https://raw.githubusercontent.com/polarsource/polar/main/clients/packages/client/src/index.ts>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/src/lib/utilsSS.ts>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/deployment/data/nginx/app.conf.template>
- <https://raw.githubusercontent.com/langgenius/dify/main/web/service/console/server.ts>
- <https://raw.githubusercontent.com/langgenius/dify/main/web/AGENTS.md>
- <https://raw.githubusercontent.com/formbricks/formbricks/main/apps/web/modules/survey/list/actions.ts>
- <https://raw.githubusercontent.com/formbricks/formbricks/main/AGENTS.md>
- <https://github.com/dubinc/dub/tree/main/apps/web/lib/actions>
- <https://raw.githubusercontent.com/calcom/cal.com/main/agents/rules/architecture-features-modules.md>
- <https://raw.githubusercontent.com/nextjs/saas-starter/main/app/(login)/actions.ts>
- <https://raw.githubusercontent.com/Kiranism/next-shadcn-dashboard-starter/main/AGENTS.md>
- <https://raw.githubusercontent.com/vercel/shop/main/AGENTS.md>
- <https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/project-structure.md>
- <https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/api-layer.md>
- <https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/state-management.md>
- <https://raw.githubusercontent.com/alan2207/bulletproof-react/master/apps/nextjs-app/.eslintrc.cjs>
- <https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app/src/app/app>
- <https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app/src/app/app/discussions>
- <https://github.com/dubinc/dub/tree/main/apps/web/ui>
- <https://github.com/dubinc/dub/tree/main/apps/web/app/app.dub.co>
- <https://github.com/formbricks/formbricks/tree/main/apps/web/modules/survey/list>
- <https://raw.githubusercontent.com/formbricks/formbricks/main/apps/web/app/(app)/workspaces/%5BworkspaceId%5D/surveys/page.tsx>
- <https://raw.githubusercontent.com/calcom/cal.com/main/agents/rules/architecture-vertical-slices.md>
- <https://raw.githubusercontent.com/calcom/cal.com/main/agents/rules/architecture-feature-boundaries.md>
- <https://raw.githubusercontent.com/calcom/cal.com/main/agents/rules/quality-avoid-barrel-imports.md>
- <https://github.com/calcom/cal.com/tree/main/agents/rules>
- <https://github.com/vercel/next-forge/tree/main/apps/app/app/(authenticated)>
- <https://github.com/ixartz/Next-js-Boilerplate/tree/main/src/app/%5Blocale%5D/(auth)>
- <https://github.com/fastapi/full-stack-fastapi-template/tree/master/frontend/src/client>
- <https://github.com/PostHog/posthog/tree/master/frontend/src/generated/core>
- <https://github.com/vintasoftware/nextjs-fastapi-template/tree/main/nextjs-frontend/app>
- <https://github.com/openapi-ts/openapi-typescript/releases>
- <https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/openapi-generate-check.yml>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/.pre-commit-config.yaml>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/.github/workflows/pre-commit.yml>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/scripts/generate-client.sh>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/frontend/.gitignore>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/watcher.js>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/.github/workflows/ci.yml>
- <https://raw.githubusercontent.com/umami-software/umami/master/.github/workflows/ci.yml>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/next.config.js>
- <https://raw.githubusercontent.com/langgenius/dify/main/docker/nginx/conf.d/default.conf.template>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/web/src/app/api/%5B...path%5D/route.ts>
- <https://raw.githubusercontent.com/khoj-ai/khoj/master/src/interface/web/next.config.mjs>
- <https://raw.githubusercontent.com/BerriAI/litellm/main/ui/litellm-dashboard/next.config.mjs>
- <https://raw.githubusercontent.com/digitros/nextjs-fastapi/main/next.config.js>
- <https://raw.githubusercontent.com/langgenius/dify/main/web/service/fetch.ts>
- <https://raw.githubusercontent.com/langgenius/dify/main/web/service/refresh-token.ts>
- <https://raw.githubusercontent.com/langgenius/dify/main/web/dev-proxy.config.ts>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/frontend/src/main.tsx>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/frontend/openapi-ts.config.ts>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/frontend/package.json>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/components/actions/login-action.ts>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/components/actions/items-action.ts>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/proxy.ts>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/package.json>
- <https://raw.githubusercontent.com/unfoldadmin/turbo/main/frontend/package.json>
- <https://raw.githubusercontent.com/unfoldadmin/turbo/main/frontend/apps/web/lib/api.ts>
- <https://raw.githubusercontent.com/PostHog/posthog/master/frontend/src/lib/api-orval-mutator.ts>
- <https://raw.githubusercontent.com/PostHog/posthog/master/frontend/src/generated/core/api.ts>
- <https://raw.githubusercontent.com/Agenta-AI/agenta/main/web/AGENTS.md>
- <https://raw.githubusercontent.com/makeplane/plane/preview/package.json>
- <https://raw.githubusercontent.com/makeplane/plane/preview/pnpm-workspace.yaml>
- <https://raw.githubusercontent.com/makeplane/plane/preview/turbo.json>
- <https://github.com/makeplane/plane/tree/preview/apps/api>
- <https://raw.githubusercontent.com/makeplane/plane/preview/.github/workflows/pull-request-build-lint-api.yml>
- <https://raw.githubusercontent.com/makeplane/plane/preview/.github/workflows/pull-request-build-lint-web-apps.yml>
- <https://raw.githubusercontent.com/polarsource/polar/main/package.json>
- <https://github.com/polarsource/polar/tree/main/clients>
- <https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/test_server.yaml>
- <https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/test_client.yaml>
- <https://raw.githubusercontent.com/PostHog/posthog/master/package.json>
- <https://raw.githubusercontent.com/PostHog/posthog/master/pnpm-workspace.yaml>
- <https://raw.githubusercontent.com/PostHog/posthog/master/.github/workflows/ci-turbo.yml>
- <https://raw.githubusercontent.com/PostHog/posthog/master/.github/workflows/ci-paths-filter.yml>
- <https://raw.githubusercontent.com/PostHog/posthog/master/.github/workflows/ci-python.yml>
- <https://raw.githubusercontent.com/langgenius/dify/main/package.json>
- <https://github.com/langgenius/dify/tree/main/api>
- <https://raw.githubusercontent.com/langgenius/dify/main/.github/workflows/main-ci.yml>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/package.json>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/pyproject.toml>
- <https://github.com/onyx-dot-app/onyx/tree/main/.github/workflows>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.github/workflows/pr-jest-tests.yml>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/package.json>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/pyproject.toml>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/.github/workflows/test-backend.yml>
- <https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/.github/workflows/playwright.yml>
- <https://raw.githubusercontent.com/getsentry/sentry/master/package.json>
- <https://raw.githubusercontent.com/getsentry/sentry/master/pnpm-workspace.yaml>
- <https://raw.githubusercontent.com/getsentry/sentry/master/.github/workflows/frontend.yml>
- <https://github.com/getsentry/sentry/tree/master/.github/workflows>
- <https://raw.githubusercontent.com/apache/superset/master/.github/workflows/superset-frontend.yml>
- <https://github.com/apache/superset/tree/master/.github/workflows>
- <https://raw.githubusercontent.com/open-webui/open-webui/main/.github/workflows/backend.yaml>
- <https://raw.githubusercontent.com/open-webui/open-webui/main/.github/workflows/frontend.yaml>
- <https://github.com/open-webui/open-webui/tree/main/.github/workflows>
- <https://raw.githubusercontent.com/langflow-ai/langflow/main/package.json>
- <https://raw.githubusercontent.com/langflow-ai/langflow/main/pyproject.toml>
- <https://raw.githubusercontent.com/langflow-ai/langflow/main/.github/workflows/ci.yml>
- <https://github.com/langflow-ai/langflow/tree/main/.github/workflows>
- <https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions>
- <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks>
- <https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2025-06-10-oxlint-stable.md>
- <https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2026-07-22-type-aware-linting-stable.md>
- <https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2026-03-11-oxlint-js-plugins-alpha.md>
- <https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2026-02-24-oxfmt-beta.md>
- <https://raw.githubusercontent.com/oxc-project/oxc-project.github.io/main/src/blog/2026-08-18-react-compiler-support.md>
- <https://github.com/oxc-project/oxc-project.github.io/tree/main/src/blog>
- <https://raw.githubusercontent.com/calcom/cal.com/main/package.json>
- <https://raw.githubusercontent.com/calcom/cal.com/main/.github/workflows/e2e.yml>
- <https://raw.githubusercontent.com/calcom/cal.com/main/.github/workflows/pr.yml>
- <https://github.com/calcom/cal.com/tree/main/.github/workflows>
- <https://raw.githubusercontent.com/dubinc/dub/main/package.json>
- <https://raw.githubusercontent.com/formbricks/formbricks/main/package.json>
- <https://raw.githubusercontent.com/formbricks/formbricks/main/.github/workflows/e2e.yml>
- <https://github.com/formbricks/formbricks/tree/main/.github/workflows>
- <https://raw.githubusercontent.com/documenso/documenso/main/package.json>
- <https://raw.githubusercontent.com/documenso/documenso/main/.github/workflows/e2e-tests.yml>
- <https://github.com/documenso/documenso/tree/main/.github/workflows>
- <https://raw.githubusercontent.com/vercel/next-forge/main/package.json>
- <https://raw.githubusercontent.com/t3-oss/create-t3-app/main/package.json>
- <https://raw.githubusercontent.com/alan2207/bulletproof-react/master/apps/nextjs-app/mock-server.ts>
- <https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/.github/workflows/CI.yml>
- <https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/lefthook.yml>
- <https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/playwright.config.ts>
- <https://github.com/ixartz/Next-js-Boilerplate/tree/main/.github/workflows>
- <https://raw.githubusercontent.com/polarsource/polar/main/clients/package.json>
- <https://raw.githubusercontent.com/polarsource/polar/main/.github/workflows/test_e2e.yaml>
- <https://raw.githubusercontent.com/langfuse/langfuse/main/.github/workflows/pipeline.yml>
- <https://raw.githubusercontent.com/midday-ai/midday/main/package.json>
- <https://raw.githubusercontent.com/shadcn-ui/ui/main/package.json>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.github/workflows/pr-playwright-tests.yml>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.github/workflows/pr-quality-checks.yml>
- <https://raw.githubusercontent.com/onyx-dot-app/onyx/main/.pre-commit-config.yaml>
- <https://raw.githubusercontent.com/twentyhq/twenty/main/package.json>
- <https://raw.githubusercontent.com/langgenius/dify/main/web/package.json>
- <https://raw.githubusercontent.com/langgenius/dify/main/.github/workflows/web-e2e.yml>
- <https://raw.githubusercontent.com/langgenius/dify/main/.github/workflows/web-tests.yml>
- <https://github.com/langgenius/dify/tree/main/.github/workflows>
- <https://github.com/umami-software/umami/tree/master/.github/workflows>
- <https://github.com/mswjs/msw/issues/1644>
- <https://github.com/mswjs/examples/pull/101>
- <https://github.com/mswjs/examples/tree/main/examples>
- <https://raw.githubusercontent.com/vercel/next.js/canary/packages/next/src/experimental/testmode/playwright/README.md>
- <https://raw.githubusercontent.com/documenso/documenso/main/ARCHITECTURE.md>
- <https://raw.githubusercontent.com/BerriAI/litellm/main/ARCHITECTURE.md>
- <https://raw.githubusercontent.com/polarsource/polar/main/AGENTS.md>
- <https://raw.githubusercontent.com/polarsource/polar/main/clients/AGENTS.md>
- <https://raw.githubusercontent.com/calcom/cal.com/main/AGENTS.md>
- <https://raw.githubusercontent.com/calcom/cal.com/main/agents/README.md>
- <https://raw.githubusercontent.com/twentyhq/twenty/main/CLAUDE.md>
- <https://raw.githubusercontent.com/twentyhq/twenty/main/AGENTS.md>
- <https://raw.githubusercontent.com/Kiranism/next-shadcn-dashboard-starter/main/CLAUDE.md>
- <https://github.com/fastapi/full-stack-fastapi-template/tree/master/.github/workflows>
- <https://github.com/vintasoftware/nextjs-fastapi-template/tree/main/nextjs-frontend>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/openapi-ts.config.ts>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/app/clientService.ts>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/lib/clientConfig.ts>
- <https://github.com/vintasoftware/nextjs-fastapi-template/tree/main/nextjs-frontend/components/actions>
- <https://github.com/vintasoftware/nextjs-fastapi-template/tree/main/.github/workflows>
- <https://raw.githubusercontent.com/vintasoftware/nextjs-fastapi-template/main/nextjs-frontend/.gitignore>
- <https://github.com/polarsource/polar/tree/main/clients/packages>
- <https://github.com/polarsource/polar/tree/main/clients/packages/client/src>
- <https://github.com/polarsource/polar/tree/main/clients/apps/web/src/utils/client>
- <https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/src/utils/client/index.ts>
- <https://github.com/polarsource/polar/tree/main/.github/workflows>
- <https://raw.githubusercontent.com/polarsource/polar/main/README.md>
- <https://github.com/onyx-dot-app/onyx/tree/main/web/src/app/api>
- <https://github.com/onyx-dot-app/onyx/tree/main/web>
- <https://github.com/langgenius/dify/tree/main/web/service>
- <https://raw.githubusercontent.com/langgenius/dify/main/web/config/index.ts>
- <https://github.com/langgenius/dify/tree/main/web>
- <https://github.com/langgenius/dify/tree/main/web/service/console>
- <https://raw.githubusercontent.com/langgenius/dify/main/web/service/console/README.md>
- <https://raw.githubusercontent.com/unfoldadmin/turbo/main/frontend/apps/web/package.json>
- <https://raw.githubusercontent.com/unfoldadmin/turbo/main/frontend/packages/types/package.json>
- <https://github.com/khoj-ai/khoj/tree/master/src/interface/web>
- <https://github.com/Agenta-AI/agenta/tree/main/web>
- <https://raw.githubusercontent.com/Agenta-AI/agenta/main/web/oss/package.json>
- <https://github.com/PostHog/posthog/tree/master/frontend/src/generated>
- <https://raw.githubusercontent.com/PostHog/posthog/master/frontend/src/lib/api.ts>
- <https://github.com/makeplane/plane/tree/preview/apps>
- <https://github.com/makeplane/plane/tree/preview/.github/workflows>
- <https://raw.githubusercontent.com/makeplane/plane/preview/AGENTS.md>
- <https://github.com/PostHog/posthog/tree/master/.github/workflows>
- <https://raw.githubusercontent.com/vercel/shop/main/README.md>
- <https://github.com/vercel/next-forge/tree/main/apps/app/app>
- <https://github.com/Kiranism/next-shadcn-dashboard-starter/tree/main/src/features/products>
- <https://github.com/ixartz/Next-js-Boilerplate/tree/main/src/app/%5Blocale%5D>
- <https://raw.githubusercontent.com/ixartz/Next-js-Boilerplate/main/README.md>
- <https://github.com/nextjs/saas-starter/tree/main/app/(login)>
- <https://github.com/nextjs/saas-starter/tree/main/lib>
- <https://github.com/vercel/next-app-router-playground/tree/main/app>
- <https://github.com/dubinc/dub/tree/main/apps/web>
- <https://github.com/dubinc/dub/tree/main/apps/web/app>
- <https://github.com/dubinc/dub/tree/main/apps/web/app/app.dub.co/(dashboard)>
- <https://github.com/dubinc/dub/tree/main/apps/web/app/app.dub.co/(dashboard)/%5Bslug%5D/settings> — 404
- <https://github.com/dubinc/dub/tree/main/apps/web/lib>
- <https://raw.githubusercontent.com/dubinc/dub/main/AGENTS.md> — 404
- <https://github.com/formbricks/formbricks/tree/main/apps/web/modules>
- <https://github.com/formbricks/formbricks/tree/main/apps/web/modules/survey>
- <https://github.com/formbricks/formbricks/tree/main/apps/web/app/(app)>
- <https://raw.githubusercontent.com/formbricks/formbricks/main/apps/web/app/(app)/environments/%5BenvironmentId%5D/surveys/page.tsx> — 404
- <https://github.com/calcom/cal.com/tree/main/apps/web/modules>
- <https://github.com/calcom/cal.com/tree/main/apps/web/app>
- <https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app/src>
- <https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app/src/app>
- <https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app/src/app/app/_components>
- <https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app/src/features/discussions>
- <https://raw.githubusercontent.com/alan2207/bulletproof-react/master/apps/nextjs-app/vitest.config.mts> — 404
- <https://raw.githubusercontent.com/t3-oss/create-t3-app/main/cli/src/installers/dependencyVersionMap.ts>
- <https://api.github.com/rate_limit> — GitHub REST API rate-limited (shared IP); replaced by HTML + atom-feed scraping
- <https://github.com/vercel/commerce/commits/main.atom>
- <https://github.com/vercel/commerce/tree/main/app>
- <https://github.com/vercel/commerce/tree/main/components>
- <https://github.com/vercel/commerce/tree/main/lib>
- <https://github.com/shadcn-ui/taxonomy/commits/main.atom>
- <https://github.com/shadcn-ui/taxonomy/tree/main/app>
- <https://github.com/calcom/cal.com/commits/main.atom>
- <https://github.com/calcom/cal.com/tree/main/apps>
- <https://github.com/calcom/cal.com/tree/main/apps/web>
- <https://github.com/calcom/cal.com/tree/main/packages>
- <https://github.com/dubinc/dub/commits/main.atom>
- <https://github.com/dubinc/dub/tree/main/apps>
- <https://github.com/dubinc/dub/tree/main/packages>
- <https://github.com/documenso/documenso/commits/main.atom>
- <https://github.com/documenso/documenso/tree/main/apps>
- <https://github.com/documenso/documenso/tree/main/packages>
- <https://github.com/formbricks/formbricks/commits/main.atom>
- <https://github.com/formbricks/formbricks/tree/main/apps>
- <https://github.com/formbricks/formbricks/tree/main/apps/web>
- <https://github.com/formbricks/formbricks/tree/main/packages>
- <https://github.com/twentyhq/twenty/commits/main.atom>
- <https://github.com/twentyhq/twenty/tree/main/packages>
- <https://github.com/makeplane/plane/commits/preview.atom>
- <https://github.com/makeplane/plane/tree/preview/packages>
- <https://github.com/makeplane/plane/tree/preview/apps/web>
- <https://github.com/Infisical/infisical/commits/main.atom>
- <https://github.com/Infisical/infisical/tree/main/frontend>
- <https://github.com/Infisical/infisical/tree/main/frontend/src>
- <https://github.com/supabase/supabase/commits/master.atom>
- <https://github.com/supabase/supabase/tree/master/apps>
- <https://github.com/supabase/supabase/tree/master/apps/studio>
- <https://github.com/vercel/next-forge/commits/main.atom>
- <https://github.com/vercel/next-forge/tree/main/apps>
- <https://github.com/vercel/next-forge/tree/main/packages>
- <https://github.com/t3-oss/create-t3-app/commits/main.atom>
- <https://github.com/t3-oss/create-t3-app/tree/main/cli/template>
- <https://github.com/alan2207/bulletproof-react/commits/master.atom>
- <https://github.com/alan2207/bulletproof-react/tree/master/apps>
- <https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app>
- <https://github.com/alan2207/bulletproof-react/tree/master/apps/nextjs-app/src/features>
- <https://github.com/fastapi/full-stack-fastapi-template/commits/master.atom>
- <https://github.com/fastapi/full-stack-fastapi-template/tree/master/frontend>
- <https://github.com/fastapi/full-stack-fastapi-template/tree/master/frontend/src>
- <https://github.com/vintasoftware/nextjs-fastapi-template/commits/main.atom>
- <https://github.com/vintasoftware/nextjs-fastapi-template/tree/main/fastapi_backend>
- <https://github.com/digitros/nextjs-fastapi/commits/main.atom>
- <https://github.com/digitros/nextjs-fastapi/tree/main/api>
- <https://github.com/polarsource/polar/commits/main.atom>
- <https://github.com/polarsource/polar/tree/main/clients/apps>
- <https://github.com/polarsource/polar/tree/main/clients/apps/web>
- <https://github.com/polarsource/polar/tree/main/clients/apps/web/src>
- <https://github.com/polarsource/polar/tree/main/clients/apps/web/src/app>
- <https://github.com/onyx-dot-app/onyx/commits/main.atom>
- <https://github.com/onyx-dot-app/onyx/tree/main/web/src>
- <https://github.com/onyx-dot-app/onyx/tree/main/web/src/app>
- <https://github.com/langgenius/dify/commits/main.atom>
- <https://github.com/langgenius/dify/tree/main/web/app>
- <https://github.com/PostHog/posthog/commits/master.atom>
- <https://github.com/PostHog/posthog/tree/master/frontend>
- <https://github.com/PostHog/posthog/tree/master/frontend/src>
- <https://github.com/getsentry/sentry/commits/master.atom>
- <https://github.com/getsentry/sentry/tree/master/static>
- <https://github.com/apache/superset/commits/master.atom>
- <https://github.com/apache/superset/tree/master/superset-frontend>
- <https://github.com/khoj-ai/khoj/commits/master.atom>
- <https://github.com/khoj-ai/khoj/tree/master/src>
- <https://github.com/khoj-ai/khoj/tree/master/src/interface>
- <https://github.com/Agenta-AI/agenta/commits/main.atom>
- <https://github.com/BerriAI/litellm/commits/main.atom>
- <https://github.com/BerriAI/litellm/tree/main/ui>
- <https://github.com/langfuse/langfuse/commits/main.atom>
- <https://github.com/langfuse/langfuse/tree/main/web>
- <https://github.com/langfuse/langfuse/tree/main/web/src>
- <https://github.com/midday-ai/midday/commits/main.atom>
- <https://github.com/midday-ai/midday/tree/main/apps>
- <https://github.com/midday-ai/midday/tree/main/packages>
- <https://github.com/umami-software/umami/commits/master.atom>
- <https://github.com/umami-software/umami/tree/master/src>
- <https://github.com/openstatusHQ/openstatus/commits/main.atom>
- <https://github.com/openstatusHQ/openstatus/tree/main/apps>
- <https://github.com/openstatusHQ/openstatus/tree/main/packages>
- <https://github.com/unkeyed/unkey/commits/main.atom>
- <https://github.com/unkeyed/unkey/tree/main/web>
- <https://github.com/unkeyed/unkey/tree/main/web/apps>
- <https://github.com/lobehub/lobe-chat/commits/canary.atom>
- <https://github.com/lobehub/lobe-chat/tree/canary/src>
- <https://github.com/vercel/ai-chatbot/commits/main.atom>
- <https://github.com/nextjs/saas-starter/commits/main.atom>
- <https://github.com/ixartz/Next-js-Boilerplate/commits/main.atom>
- <https://github.com/ixartz/Next-js-Boilerplate/tree/main/src>
- <https://github.com/Kiranism/next-shadcn-dashboard-starter/commits/main.atom>
- <https://github.com/Kiranism/next-shadcn-dashboard-starter/tree/main/src>
- <https://github.com/Kiranism/next-shadcn-dashboard-starter/tree/main/src/features>
- <https://github.com/shadcn-ui/ui/commits/main.atom>
- <https://github.com/shadcn-ui/ui/tree/main/apps>
- <https://github.com/vercel/next-app-router-playground/commits/main.atom>
- <https://github.com/mfts/papermark/commits/main.atom>
- <https://github.com/hey-api/openapi-ts/commits/main.atom>
- <https://github.com/openapi-ts/openapi-typescript/commits/main.atom>
- <https://github.com/openapi-ts/openapi-typescript/tree/main/packages>
- <https://github.com/orval-labs/orval/commits/master.atom>
- <https://github.com/feature-sliced/documentation/commits/main.atom>
- <https://github.com/vercel/turborepo/commits/main.atom>
- <https://github.com/nrwl/nx/commits/master.atom>
- <https://github.com/moonrepo/moon/commits/master.atom>
- <https://github.com/pantsbuild/pants/commits/main.atom>
- <https://github.com/dorny/paths-filter/commits/master.atom>
- <https://github.com/open-webui/open-webui/commits/main.atom>
- <https://github.com/mlflow/mlflow/commits/master.atom>
- <https://github.com/toss/frontend-fundamentals/commits/main.atom>
- <https://github.com/oxc-project/oxc/commits/main.atom>

**Official docs, specs and project sites (78)**

- <https://create.t3.gg/en/folder-structure-app>
- <https://nextjs.org/docs/app/getting-started/project-structure>
- <https://nextjs.org/blog/next-16>
- <https://nextjs.org/docs/app/api-reference/directives/use-client>
- <https://nextjs.org/docs/app/guides/data-security>
- <https://feature-sliced.design/docs/get-started/overview>
- <https://feature-sliced.design/docs/guides/tech/with-nextjs>
- <https://feature-sliced.design/kr/docs/guides/tech/with-nextjs>
- <https://feature-sliced.design/docs/guides/migration/from-v2-0>
- <https://feature-sliced.design/docs/guides/issues/excessive-entities>
- <https://feature-sliced.design/docs/reference/public-api>
- <https://www.next-forge.com/docs/structure>
- <https://www.next-forge.com/docs/apps/app>
- <https://frontend-fundamentals.com/code-quality/code/examples/code-directory.html>
- <https://frontend-fundamentals.com/code-quality/code/>
- <https://frontend-fundamentals.com/code-quality/code/examples/use-bottom-sheet.html>
- <https://nextjs.org/docs/app/guides/backend-for-frontend>
- <https://nextjs.org/docs/app/api-reference/file-conventions/proxy>
- <https://nextjs.org/docs/app/guides/authentication>
- <https://nextjs.org/docs/app/api-reference/functions/cookies>
- <https://nextjs.org/docs/app/guides/authentication-with-cache-components>
- <https://nextjs.org/docs/app/api-reference/config/next-config-js/rewrites>
- <https://nextjs.org/blog/security-nextjs-server-components-actions>
- <https://www.rfc-editor.org/rfc/rfc10017.html>
- <https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/>
- <https://openapi-ts.dev/openapi-fetch/>
- <https://openapi-ts.dev/cli>
- <https://openapi-ts.dev/openapi-fetch/middleware-auth>
- <https://openapi-ts.dev/openapi-fetch/examples>
- <https://openapi-ts.dev/openapi-react-query/>
- <https://heyapi.dev/openapi-ts/get-started>
- <https://heyapi.dev/openapi-ts/configuration/output>
- <https://heyapi.dev/openapi-ts/clients/next-js>
- <https://heyapi.dev/openapi-ts/clients/fetch>
- <https://turborepo.dev/docs/crafting-your-repository/structuring-a-repository>
- <https://turborepo.dev/docs/guides/multi-language>
- <https://turborepo.dev/docs/guides/tools/python>
- <https://turborepo.dev/docs/reference/run>
- <https://turborepo.dev/docs/reference/prune>
- <https://turborepo.dev/docs/guides/tools/docker>
- <https://turborepo.dev/docs/getting-started/add-to-existing-repository>
- <https://turborepo.dev/docs/core-concepts/remote-caching>
- <https://turborepo.dev/docs>
- <https://nx.dev/docs/features/multi-language-support>
- <https://nx.dev/docs/concepts/inferred-tasks>
- <https://nx.dev/docs/features/ci-features/affected>
- <https://nx.dev/pricing>
- <https://moonrepo.dev/blog/moon-v2-rc>
- <https://www.pantsbuild.org/dev/docs/javascript/overview>
- <https://pnpm.io/workspaces>
- <https://pnpm.io/catalogs>
- <https://docs.astral.sh/uv/concepts/projects/workspaces/>
- <https://monorepo.tools/>
- <https://nextjs.org/docs/app/api-reference/config/next-config-js/output>
- <https://nextjs.org/docs/app/guides/testing>
- <https://nextjs.org/docs/app/guides/testing/vitest>
- <https://nextjs.org/docs/app/guides/testing/playwright>
- <https://nextjs.org/docs/app/guides/upgrading/version-16>
- <https://nextjs.org/docs/app/api-reference/cli/create-next-app>
- <https://nextjs.org/docs/app/api-reference/config/eslint>
- <https://oxc.rs/blog/>
- <https://oxc.rs/docs/guide/usage/linter.html>
- <https://oxc.rs/docs/guide/usage/linter/plugins.html>
- <https://biomejs.dev/blog/biome-v2/>
- <https://biomejs.dev/blog/biome-v2-6/>
- <https://biomejs.dev/blog/>
- <https://playwright.dev/docs/mock>
- <https://playwright.dev/docs/test-webserver>
- <https://2024.stateofjs.com/en-US/libraries/testing/>
- <https://2025.stateofjs.com/en-US/libraries/testing/>
- <https://vitest.dev/blog/vitest-4>
- <https://agents.md/>
- <https://nextjs.org/docs/app/guides/ai-agents>
- <https://orval.dev/overview> — 404
- <https://kubb.dev/> — no content
- <https://moonrepo.dev/docs/guides/python> — 404
- <https://nx.dev/docs/concepts/decisions/why-monorepos> — 404
- <https://mswjs.io/docs/integrations/react-native> — fetched by mistake, irrelevant

**Package registries / download stats (17)**

- <https://registry.npmjs.org/next/latest>
- <https://registry.npmjs.org/steiger/latest>
- <https://registry.npmjs.org/openapi-typescript/latest>
- <https://registry.npmjs.org/openapi-fetch/latest>
- <https://registry.npmjs.org/openapi-react-query/latest>
- <https://registry.npmjs.org/@hey-api/openapi-ts/latest>
- <https://registry.npmjs.org/orval/latest>
- <https://registry.npmjs.org/@kubb/core/latest>
- <https://cdn.jsdelivr.net/npm/@nxlv/python@23.0.0/README.md>
- <https://registry.npmjs.org/oxlint/latest>
- <https://api.npmjs.org/downloads/point/last-week/vitest,jest,cypress,msw,oxlint,eslint,prettier,playwright,oxfmt,storybook>
- <https://api.npmjs.org/downloads/point/last-week/@playwright/test>
- <https://api.npmjs.org/downloads/point/last-week/@biomejs/biome>
- <https://registry.npmjs.org/vitest/latest>
- <https://www.npmjs.com/package/@nxlv/python> — search-result snippet only
- <https://newreleases.io/project/yarn/nx/release/22.0.0> — search-result snippet only (secondary)
- <https://api.npmjs.org/downloads/point/last-week/vitest,jest,@playwright/test,cypress,msw,oxlint,@biomejs/biome> — HTTP 400

**Blogs, articles and other pages (incl. Korean) (23)**

- <https://velog.io/@teo/separation-of-concerns-of-frontend>
- <https://kentcdodds.com/blog/colocation>
- <https://www.robinwieruch.de/react-folder-structure/>
- <https://www.robinwieruch.de/react-feature-architecture/>
- <https://overreacted.io/what-does-use-client-do/>
- <https://overreacted.io/impossible-components/>
- <https://www.joshwcomeau.com/react/server-components/>
- <https://tech.kakaoent.com/>
- <https://vercel.com/guides/understanding-csrf-attacks>
- <https://www.vintasoftware.com/blog/next-js-fastapi-template>
- <https://toss.tech/article/monorepo-pipeline>
- <https://toss.tech/article/node-modules-and-yarn-berry>
- <https://techblog.woowahan.com/7976/>
- <https://engineering.linecorp.com/ko/blog/monorepo-with-turborepo>
- <https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html>
- <https://d2.naver.com/helloworld/0923884> — fetch blocked
- <https://medium.com/@mattklein123/monorepos-please-dont-e9a279be011b> — HTTP 403
- <https://fe-developers.kakaoent.com/> — 301 to tech.kakaoent.com
- <https://tech.kakaoent.com/front-end/> — 404
- <https://tech.kakaoent.com/front-end/2024/240116-common-component/> — body not loaded
- <https://www.robinwieruch.de/next-folder-structure/> — 404
- <https://www.robinwieruch.de/next-project-structure/> — 404
- <https://velog.io/tags/FSD> — HTTP 500
