# Reference/Exemplar Applications and Architecture Documentation Methods for 믿집

> **How this was researched (2026-10-29):** The shared WebSearch budget was already used up when this task started, so no search-engine queries were run. Every source below was reached by fetching a known primary URL directly: official docs, engineering blogs, GitHub repo pages, raw repo files, and Korean tech-blog RSS feeds and sitemaps. Repo activity was checked today by scraping each GitHub repo page for `isArchived`/`stargazerCount` and reading the newest commit timestamp from `github.com/<repo>/commits.atom` (default branch). "Last commit" below means that timestamp, and star counts are as of 2026-10-29. The unauthenticated GitHub REST API rate limit ran out partway through, so those two methods were mixed. Facts dated before 2025 are labelled **(older)**.

## Q1. Which well-known reference apps are still worth learning from in 2025–2026, and which fit a modular monolith with a separate SPA/SSR frontend?

### Takeaway
Most famous "reference apps" are either specs with mostly stale implementations (RealWorld), single-stack demos (PetClinic), or microservice/Kubernetes showcases (eShop, Online Boutique, AWS Retail Store). None of these models 믿집's shape: one FastAPI modular monolith, a separate Next.js app, a Redis worker, and Docker Compose on one host. The closest maintained exemplars are real products. Polar (FastAPI + Next.js 16 + worker) is the best fit, followed by Dify (Python API + Next.js + Celery + Compose, layer rules enforced with import-linter) and Plane (Python API + separate web/admin apps + worker in one Compose file). Shopify, GitLab and Basecamp are best used for modular-monolith principles, not as code to copy.

### Cited Findings
**Classic reference apps (activity checked 2026-10-29)**
- RealWorld ("Conduit", a Medium clone) has moved from `gothinkster/realworld` to `realworld-apps/realworld`. It has 84,333 stars and its last commit was 2026-08-26. It markets itself as "The mother of all demo apps" and lists 100+ implementations on CodebaseShow. Only two backends are marked as passing the full API test suite: Nitro + Prisma + Zod, and Django Ninja — [realworld-apps/realworld](https://github.com/realworld-apps/realworld)
- The RealWorld spec is maintained as `specs/api/openapi.yml`, a Hurl test suite, and a Bruno collection generated from Hurl ("The Hurl files are the source of truth") and kept in sync by CI. There is also a shared `specs/e2e` suite for frontends — [RealWorld specs/api README](https://raw.githubusercontent.com/realworld-apps/realworld/main/specs/api/README.md); [repo tree](https://github.com/realworld-apps/realworld/tree/main/specs)
- Individual RealWorld implementations go stale. `nsidnev/fastapi-realworld-example-app` (3,100 stars) is **archived** with its last commit on 2022-08-21. `reck1ess/next-realworld-example-app` (824 stars) last changed on 2020-08-06 **(older)** — [nsidnev/fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app); [reck1ess/next-realworld-example-app](https://github.com/reck1ess/next-realworld-example-app)
- Spring PetClinic has 9,614 stars and was last pushed 2026-09-29. It is a Spring Boot + Thymeleaf sample that needs Java 17+. Its architecture slides are flagged as referring to "a legacy, pre–Spring Boot version" — [spring-projects/spring-petclinic](https://github.com/spring-projects/spring-petclinic). There are 18 maintained forks covering Angular, React, Kotlin, GraphQL, a microservices version and Spring AI variants — [spring-petclinic.github.io](https://spring-petclinic.github.io/). The microservices fork has 2,232 stars and was last changed 2026-10-23 — [spring-petclinic-microservices](https://github.com/spring-petclinic/spring-petclinic-microservices)
- dotnet/eShop has 10,983 stars and is active. It is a "services-based architecture" built on .NET Aspire and targets .NET 10. Its Azure deployment uses containerized Postgres, Redis and RabbitMQ "for evaluation, not production" — [dotnet/eShop](https://github.com/dotnet/eShop). Its predecessor eShopOnContainers (24,291 stars) was **archived on 2023-11-17** — [dotnet-architecture/eShopOnContainers](https://github.com/dotnet-architecture/eShopOnContainers)
- Google's Online Boutique (`microservices-demo`) has 21,096 stars and its last commit was 2026-10-27. It has 11 gRPC microservices in Go, C#, Node.js, Python and Java and targets GKE, Istio and Cloud Service Mesh. Its README says 10 services in one place and 11 in another — [GoogleCloudPlatform/microservices-demo](https://github.com/GoogleCloudPlatform/microservices-demo)
- AWS samples: the Retail Store Sample App (612 stars, last commit 2026-09-25) has a Java UI and Go/Java/Node services, runs locally with Docker Compose, deploys to EKS/ECS/App Runner, and states it is "intended for educational purposes only and not for production use" — [aws-containers/retail-store-sample-app](https://github.com/aws-containers/retail-store-sample-app). The older `aws-modern-application-workshop` is **archived** (last commit 2019) — [aws-samples/aws-modern-application-workshop](https://github.com/aws-samples/aws-modern-application-workshop)
- `vercel/commerce` (14,311 stars) shows as **archived** on GitHub today — [vercel/commerce](https://github.com/vercel/commerce). `nextjs/saas-starter` (16,234 stars) last changed on 2025-12-11 — [nextjs/saas-starter](https://github.com/nextjs/saas-starter)

**FastAPI / Python + JS full-stack exemplars**
- `fastapi/full-stack-fastapi-template` has 46,103 stars and its last commit was 2026-10-26. Its stack is FastAPI + SQLModel + Postgres, a React/Vite/shadcn frontend, JWT auth, Mailpit, Pytest and Playwright, Docker Compose with Traefik, GitHub Actions, and an auto-generated frontend client. Its docs are split into `backend/README.md`, `frontend/README.md`, `development.md`, `deployment-docker-compose.md` and `release-notes.md` — [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)
- The template's backend is flat, not modular: `app/models.py`, `app/crud.py`, `app/api/`, `alembic/`, `email-templates/` — [backend/README.md](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/backend/README.md); [backend/app tree](https://github.com/fastapi/full-stack-fastapi-template/tree/master/backend/app). It uses `compose.yml` + `compose.override.yml` (local overrides such as source mounts) and `docker compose watch` — [development.md](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/development.md)
- `zhanymkanov/fastapi-best-practices` (18,263 stars, last commit 2026-08-27) recommends organizing code by domain under `src/` (`router.py`, `schemas.py`, `models.py`, `service.py`, `dependencies.py`, `exceptions.py`). It says to import other packages' services "with an explicit module name", to name Alembic migrations date + slug, and to give tables singular snake_case names — [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
- **Polar** (10,436 stars, Apache-2.0, last commit 2026-10-29) is a monorepo with a Python/FastAPI backend and a Next.js frontend. Its web app depends on `next ^16.3.6`, the same major version as 믿집 — [polarsource/polar](https://github.com/polarsource/polar); [clients/apps/web/package.json](https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/package.json). Its root AGENTS.md shows this layout per module: `polar/{module}/endpoints.py, service.py (singleton), repository.py, schemas.py, tasks.py (Dramatiq)`. Models are global, the backoffice is HTMX + DaisyUI, and "The TypeScript API client is generated from the backend's OpenAPI schema" — [Polar AGENTS.md](https://raw.githubusercontent.com/polarsource/polar/main/AGENTS.md)
- Polar's server guide says "ALL database queries MUST be in repository files". It also enforces in review: relationships set `lazy="raise"`, business errors are status-coded `PolarError` (409/404, with 422 reserved for payload validation), endpoints return ORM models, and destructive operations are marked in OpenAPI `x-tool-annotations` with a test that fails until every write is classified — [polar server/AGENTS.md](https://raw.githubusercontent.com/polarsource/polar/main/server/AGENTS.md)
- **Dify** (159,894 stars, last commit 2026-10-29) has a Flask + Celery backend (`api/`), a Next.js frontend (`web/`), and a Docker Compose stack with api, worker, worker_beat, web, Postgres, Redis, nginx and a vector DB — [langgenius/dify](https://github.com/langgenius/dify); [api/pyproject.toml](https://raw.githubusercontent.com/langgenius/dify/main/api/pyproject.toml); [web/package.json](https://raw.githubusercontent.com/langgenius/dify/main/web/package.json); [docker-compose.yaml](https://raw.githubusercontent.com/langgenius/dify/main/docker/docker-compose.yaml)
- Dify's `docs/BACKEND_ARCHITECTURE.md` defines Transport → Application → Domain → Infrastructure layers and a composition root, and says "Import-boundary contracts encode these directions and run in lint" — [BACKEND_ARCHITECTURE.md](https://raw.githubusercontent.com/langgenius/dify/main/docs/BACKEND_ARCHITECTURE.md). Its `api/.importlinter` has 1 `layers` contract (`controllers → services → core → libs`) and 74 `forbidden` contracts. The legacy exceptions are listed exactly, and the setting `unmatched_ignore_imports_alerting = error` makes that list shrink whenever an exception is fixed — [api/.importlinter](https://raw.githubusercontent.com/langgenius/dify/main/api/.importlinter)
- Dify's root AGENTS.md tells agents to "Follow the nearest scoped AGENTS.md" and to read the four backend architecture docs before backend work — [Dify AGENTS.md](https://raw.githubusercontent.com/langgenius/dify/main/AGENTS.md); [api/AGENTS.md](https://raw.githubusercontent.com/langgenius/dify/main/api/AGENTS.md)
- **Plane** (61,660 stars, AGPL-3.0, last commit 2026-10-29) is a pnpm/Turbo monorepo. Its README "Built with" lists React Router, Django and Node.js, and `apps/web` depends on `react-router`, not Next.js — [makeplane/plane](https://github.com/makeplane/plane); [apps/web/package.json](https://raw.githubusercontent.com/makeplane/plane/preview/apps/web/package.json). Its community Compose file defines `web, space, admin, live, api, worker, beat-worker, migrator, plane-db, plane-redis, plane-mq, plane-minio, proxy` — [docker-compose.yml](https://raw.githubusercontent.com/makeplane/plane/preview/deployments/cli/community/docker-compose.yml)
- Mealie (13,718 stars, active) is a self-hosted app with a REST API backend and a reactive frontend — [mealie-recipes/mealie](https://github.com/mealie-recipes/mealie). Netflix Dispatch (FastAPI) is **archived** (last commit 2025-09-03) — [Netflix/dispatch](https://github.com/Netflix/dispatch)
- Open WebUI (157,131 stars) and Langfuse (36,697 stars) are active. Langfuse's self-host architecture is Web + Worker + Postgres + ClickHouse + Redis/Valkey (cache and queue) + S3. It lists Docker Compose for "Local use and testing" only — [open-webui/open-webui](https://github.com/open-webui/open-webui); [langfuse/langfuse](https://github.com/langfuse/langfuse); [Langfuse self-hosting](https://langfuse.com/self-hosting)
- Smaller "clean architecture FastAPI" examples are active but niche: `iktakahiro/dddpy` (730 stars), `ivan-borovets/fastapi-clean-example` (597 stars), `Kludex/fastapi-tips` (3,634 stars) — [dddpy](https://github.com/iktakahiro/dddpy); [fastapi-clean-example](https://github.com/ivan-borovets/fastapi-clean-example); [fastapi-tips](https://github.com/Kludex/fastapi-tips)

**Modular monolith / majestic monolith sources**
- In "Deconstructing the Monolith" and its Sept 2020 follow-up **(older)**, Shopify describes a 2.8M-line Ruby core with 37 components and 400 Architecture Guild members. Wedge, which took over an hour, was replaced by Packwerk, which takes minutes. Lessons: large refactors are "mainly a people problem", fewer hard rules worked better than many, and functional cohesion beats grouping by DB table — [Shopify Engineering](https://shopify.engineering/shopify-monolith)
- Packwerk (Sept 2020, **older**) uses `package.yml` per package, "deprecated_references" todo lists, and `packwerk check` in CI. Its lesson: boundaries without enforcement are "a social contract that can be easily broken" — [Enforcing modularity with Packwerk](https://shopify.engineering/enforcing-modularity-rails-apps-packwerk)
- The Packwerk retrospective (Feb 2024, **older**) reports that privacy checks failed and were removed in v3.0, while dependency checks held the base layer. Its lesson: verify boundaries by running code in isolation, not only by counting violations — [A Packwerk Retrospective](https://shopify.engineering/a-packwerk-retrospective). The repo has 1,928 stars and its last commit was 2026-08-26 — [Shopify/packwerk](https://github.com/Shopify/packwerk)
- GitLab's modular monolith design document was created 2023-05-22 and is still marked "proposed". It cites 2.2M+ lines of Ruby and has a newer "agentic imperative" framing: modular boundaries make code "legible to AI agents" — [GitLab handbook](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/modular_monolith/). Enforcement uses `config/bounded_contexts.yml` plus a `Gitlab/BoundedContexts` RuboCop cop — [GitLab software design guide](https://docs.gitlab.com/development/software_design/); mirror at [gitlabhq/gitlabhq](https://github.com/gitlabhq/gitlabhq)
- DHH's "The Majestic Monolith" (2016, **older**) argues that a small team of 12 programmers serving six platforms should keep one integrated monolith rather than "cargo cult" microservices — [Signal v. Noise](https://signalvnoise.com/svn3/the-majestic-monolith/). Basecamp's source-available Campfire ships web app, jobs, caching, file serving and SSL in one Docker image for single-machine deploys — [basecamp/once-campfire](https://github.com/basecamp/once-campfire); Kamal for deploying anywhere — [basecamp/kamal](https://github.com/basecamp/kamal)
- Fowler's "MonolithFirst" (2015, **older**) says most successful microservice stories started as a monolith — [martinfowler.com](https://martinfowler.com/bliki/MonolithFirst.html). Grzybek's primer (2019, **older**) lists the module traits as independence, business orientation, contract, and encapsulation — [kamilgrzybek.com](https://www.kamilgrzybek.com/blog/posts/modular-monolith-primer)
- `kgrzybek/modular-monolith-with-ddd` (14,102 stars) has an ADL, C4 diagrams in C4-PlantUML, event-bus-only module integration with outbox/inbox, and NetArchTest architecture tests in CI. Its **last commit was 2024-04-20** and it is .NET — [kgrzybek/modular-monolith-with-ddd](https://github.com/kgrzybek/modular-monolith-with-ddd)
- Spring Modulith 2.1.1 builds a module model from code and uses it both to verify structure and to generate PlantUML C4 component diagrams and "Application Module Canvas" docs from a test — [Spring Modulith docs](https://docs.spring.io/spring-modulith/reference/documentation.html)
- Rails/SPA monoliths: Discourse is a Rails JSON API with an Ember.js frontend on Postgres and Redis (48,029 stars). Mastodon is Rails + Sidekiq + a Node.js streaming API + React/Redux (50,456 stars) — [Discourse README](https://raw.githubusercontent.com/discourse/discourse/main/README.md); [Mastodon README](https://raw.githubusercontent.com/mastodon/mastodon/main/README.md); [discourse/discourse](https://github.com/discourse/discourse); [mastodon/mastodon](https://github.com/mastodon/mastodon)
- Korean, 2026: Daangn's community system (about 20,000 RPS) calls itself a "모듈형 모놀리스(Modular Monolith)". It is one codebase and one release, split into four run units (api, worker, batch, console). It checks module dependency directions with architecture tests, and its API contract moved from documents to OpenAPI reviewed by PR, with code generation, because the documents could not be trusted to be current — [당근 테크블로그, 2026-07-14](https://medium.com/daangn/%EC%B2%9C%EB%A7%8C-mau%EB%A5%BC-%EC%A7%80%ED%83%B1%ED%95%98%EB%8A%94-%EC%BB%A4%EB%AE%A4%EB%8B%88%ED%8B%B0-%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84-%EC%86%8C%EA%B0%9C%ED%95%B4%EC%9A%94-090fb4021e20)

### Inferences
- 믿집 already has the "Daangn/Polar shape": one API codebase, a separate worker process, and a generated or contracted frontend boundary. The most useful things to borrow are enforcement and documentation patterns, not new folder layouts.
- RealWorld is still useful for exactly one thing: a spec plus executable API tests (Hurl/Bruno) as the "contract that keeps implementations honest". Its individual implementations should not be copied, since many are archived or stale.
- eShop, Online Boutique and the AWS Retail Store teach microservices and Kubernetes topics that 믿집 explicitly does not need on one EC2 instance. At most they are diagram-style references.
- Polar is the single closest match: FastAPI + Next.js 16, per-module router/service/repository, a worker, a generated TS client, an ADR log, and agent docs. Dify is the best example of turning a layer table like 믿집's AGENTS.md "층 규칙" into an executable import-linter contract.

### Gaps
- I could not fetch Shopify's original 2019 "Deconstructing the Monolith" post. The URL served the 2020 follow-up.
- I did not measure how each repo's docs are actually used, for example doc page views.
- I did not open the CodebaseShow listing to count how many RealWorld implementations are archived.

## Q2. How do marketplace, booking and quote open-source apps model requests, offers and status machines, admin back-offices, and audit logs?

### Takeaway
Strong products share three patterns:
1. They declare the status machine explicitly: who (actor) may move which state to which, and what side effects run.
2. They keep a separate append-only event/audit table per aggregate, recording actor, source, action, a JSON payload and a timestamp.
3. They run the admin back-office as either a separate app or a server-rendered internal UI, with operator actions logged.

Sharetribe's `default-negotiation` process is almost a direct template for 믿집's quote flow. Cal.diy's `BookingAudit` and Saleor's `OrderEvent` are good templates for the history table.

### Cited Findings
**Status machines**
- Sharetribe's transaction process is built from transitions, each with `:from`, `:to`, an actor (customer, provider, operator, or time/"system"), actions and notifications, and written in `process.edn`. You change a process by creating new versions: "Deleting transaction processes and transaction process versions is not possible." The Console visualises each version — [Sharetribe transaction process](https://www.sharetribe.com/docs/concepts/transaction-process/)
- Sharetribe's `default-negotiation` process includes the reverse-marketplace path `request-quote (customer) → quote-requested → make-offer-from-request (provider) → offer-pending → counter-offers / update-offer → request-payment-to-accept-offer → pending-payment → confirm-payment → offer-accepted → deliver → delivered → (request-changes ↔ deliver-changes) → accept-deliverable / auto-accept → completed → reviews`.
  - Operator-only transitions include `operator-reject-request`, `operator-cancel` and `operator-accept-deliverable`.
  - Time-based transitions include `expire-payment`, `auto-cancel` and `expire-review-period`.
  - Notifications are declared per transition, for example `new-quote-request` on `request-quote` goes to the provider.
  - Source: [sharetribe/web-template ext/transaction-processes/default-negotiation/process.edn](https://raw.githubusercontent.com/sharetribe/web-template/main/ext/transaction-processes/default-negotiation/process.edn); template repo (69 stars, last commit 2026-10-28) [sharetribe/web-template](https://github.com/sharetribe/web-template); more processes in [sharetribe/example-processes](https://github.com/sharetribe/example-processes)
- `sharetribe/sharetribe` describes itself as "Sharetribe Go … old source-available marketplace software" (2,448 stars), so the current product's backend is hosted, not open source — [sharetribe/sharetribe](https://github.com/sharetribe/sharetribe)
- Saleor documents order states from the `OrderStatus` enum: DRAFT, UNCONFIRMED, UNFULFILLED, PARTIALLY_FULFILLED, FULFILLED, PARTIALLY_RETURNED, RETURNED, EXPIRED, CANCELED. Each state lists its allowed transitions, the mutation that triggers it (`orderConfirm`, `orderCancel`…) and its stock effects, all shown as state diagrams — [Saleor order status docs](https://docs.saleor.io/developer/checkout/order-status); [saleor/saleor](https://github.com/saleor/saleor) (23,487 stars, active)
- Cal.diy's `BookingStatus` enum is `CANCELLED, ACCEPTED, REJECTED, PENDING, AWAITING_HOST` — [cal.diy schema.prisma](https://raw.githubusercontent.com/calcom/cal.diy/main/packages/prisma/schema.prisma)
- Repo status note: `github.com/calcom/cal.com` now **redirects to `calcom/cal.diy`** (49,504 stars, last commit 2026-10-28). Cal.diy describes itself as an MIT-licensed community fork with enterprise features removed and self-hosting "strictly recommended for personal, non-production use" — [calcom/cal.diy](https://github.com/calcom/cal.diy)
- Gmarket's travel platform (2024, **older**) defined each system's states and matched equivalent stages across systems before implementing a state machine. A reconciliation batch re-syncs states after transient failures — [지마켓 기술블로그, 2024-07-23](https://dev.gmarket.com/115)

**Module boundaries for cross-domain flows**
- Medusa's rule is that "Modules can't access resources, such as services or data models, from other modules". Cross-module data is joined via Module Links plus Query. Cross-module logic goes in workflows, whose steps define rollback/compensation and whose executions are tracked — [Medusa module isolation](https://docs.medusajs.com/learn/fundamentals/modules/isolation); [Medusa workflows](https://docs.medusajs.com/learn/fundamentals/workflows); [Medusa modules](https://docs.medusajs.com/learn/fundamentals/modules); [medusajs/medusa](https://github.com/medusajs/medusa) (36,994 stars, active)

**Audit and event history tables**
- Saleor `OrderEvent` has `date`, `type` (from about 87 `OrderEvents` constants such as CONFIRMED, PLACED, CANCELED, PAYMENT_CAPTURED, EMAIL_SENT, FULFILLMENT_*), a FK to `order`, a `parameters` JSON field, a nullable `user`, and a nullable `app` — [saleor/order/models.py](https://raw.githubusercontent.com/saleor/saleor/main/saleor/order/models.py); [saleor/order/__init__.py](https://raw.githubusercontent.com/saleor/saleor/main/saleor/order/__init__.py)
- Cal.diy `BookingAudit` has `actorId`, `type` (record created/updated/deleted), `action` (CREATED, ACCEPTED, REJECTED, RESCHEDULED, REASSIGNMENT…), a business `timestamp` separate from `createdAt`, `source` (API_V1/API_V2/WEBAPP/WEBHOOK/SYSTEM/MAGIC_LINK), `operationId` for correlating bulk ops, `data` JSON and `context` JSON (ip, userAgent, impersonation).
  - `bookingUid` and the actor references are stored **without FK constraints** on purpose, so the history survives deletion.
  - A separate `AuditActor` table types actors as USER/GUEST/ATTENDEE/SYSTEM/APP.
  - Source: [cal.diy schema.prisma](https://raw.githubusercontent.com/calcom/cal.diy/main/packages/prisma/schema.prisma)
- Mastodon `admin_action_logs` has `account_id` (the staff member), `action`, polymorphic `target_type`/`target_id`, `human_identifier`, `permalink`, `recorded_changes` jsonb and timestamps — [mastodon app/models/admin/action_log.rb](https://raw.githubusercontent.com/mastodon/mastodon/main/app/models/admin/action_log.rb); [db/schema.rb](https://raw.githubusercontent.com/mastodon/mastodon/main/db/schema.rb)
- Discourse `UserHistory` is a "staff action log" keyed by an `actions` enum, with a `staff_actions` subset such as `delete_user` and `create_bot` — [discourse app/models/user_history.rb](https://raw.githubusercontent.com/discourse/discourse/main/app/models/user_history.rb)
- The audit-logging pattern is to keep a DB record of user activity. Its drawback is that auditing code mixes into business logic, and event sourcing is "a reliable way to implement auditing" — [microservices.io audit logging](https://microservices.io/patterns/observability/audit-logging.html)
- Fowler's Event Sourcing (2005, **older**) gives audit, temporal query and replay. Its costs are an unnatural style, retrofit difficulty, side effects on replay and the need for snapshots — [martinfowler.com](https://martinfowler.com/eaaDev/EventSourcing.html)
- PostgreSQL's generic audit trigger writes `audit.logged_actions` with old/changed row data (hstore), txid, client info and the statement. The app should only have SELECT rights on it, and it does not log SELECT/DDL. It is a safety net, not a business history — [PostgreSQL wiki audit trigger](https://wiki.postgresql.org/wiki/Audit_trigger_91plus)
- Transactional outbox: write the message to an outbox table in the same DB transaction and let a relay publish it. Messages are sent "if and only if" the commit succeeds. Consumers must be idempotent — [microservices.io outbox](https://microservices.io/patterns/data/transactional-outbox.html). arq v0.28.0 (2026-04-16) runs jobs pessimistically, so jobs can run more than once, and its docs advise idempotent jobs — [arq docs](https://arq-docs.helpmanual.io/); [python-arq/arq](https://github.com/python-arq/arq) (3,018 stars)

**Admin back-office patterns**
- Polar's internal backoffice lives in the backend and is server-rendered with HTMX + DaisyUI + tagflow, using its own `BackofficeRouter` — [polar backoffice AGENTS.md](https://raw.githubusercontent.com/polarsource/polar/main/server/polar/backoffice/AGENTS.md)
- Plane ships a separate `admin` app container next to `web` — [Plane compose](https://raw.githubusercontent.com/makeplane/plane/preview/deployments/cli/community/docker-compose.yml). Saleor ships its dashboard as a separate GraphQL SPA — [saleor/saleor-dashboard](https://github.com/saleor/saleor-dashboard) (1,046 stars)
- Admin frameworks (all active): react-admin (26,978 stars), Refine (35,961 stars), and, for FastAPI/SQLAlchemy, SQLAdmin (2,849 stars) and starlette-admin (1,069 stars) — [react-admin](https://github.com/marmelab/react-admin); [refine](https://github.com/refinedev/refine); [sqladmin](https://github.com/aminalaee/sqladmin); [starlette-admin](https://github.com/jowilf/starlette-admin)
- Twenty (CRM, 60,060 stars) uses NestJS + BullMQ + Postgres + Redis + React and is "mostly" AGPLv3, with some files under a commercial license — [twentyhq/twenty](https://github.com/twentyhq/twenty); [LICENSE](https://raw.githubusercontent.com/twentyhq/twenty/main/LICENSE)

### Inferences
- 믿집's per-trade (공정) state line, "고르는 중 → 가견적 기다림 → 비교 중 → 실측 기다림 → 실측 견적 도착 → 확정 → 일정 등록됨 (+다시 고르기)", maps almost one-to-one onto Sharetribe's `request-quote → offer-pending → … → accepted` path.
  - Sharetribe's explicit **actor column** (customer/provider/operator/time) is exactly the rule 믿집 already states in prose: "확정·다시 고르기·실측 요청은 고객만, 견적서·공사기간은 업체만".
  - Adding an "operator" (admin) column and "time" transitions, such as expiry, would make those rules checkable.
- A history table modeled on cal.diy/Saleor is low-cost and fits the existing `jobs` pattern. Suggested shape: `quote_event(id, project_id, trade_id, vendor_id?, from_status, to_status, action, actor_type, actor_id, source, payload jsonb, occurred_at)`. Also: write it in the same transaction as the status change, and avoid hard FKs to rows that may be deleted.
- Of these back-office options, the cheapest path for a student team is the existing Next.js admin pages plus an admin action log table, modeled on Mastodon's `admin_action_logs`. A second admin framework would add more stack to learn.

### Gaps
- I did not verify cal.com's own announcement explaining the cal.com → cal.diy rename. With search unavailable, only the redirect and cal.diy README were checked.
- The Medusa docs page included a block addressed to AI agents asking for feedback submission. It was ignored as page data, not an instruction.
- I did not fetch Medusa's order-change/versioning model or Twenty's audit/timeline model.

## Q3. Which architecture documentation methods are light enough for students and stay up to date, and should diagrams be generated or hand-drawn?

### Takeaway
The lightest set that experts converge on is:
- a short ARCHITECTURE.md (bird's-eye view, code map, invariants), revisited a few times a year;
- C4 System Context + Container diagrams only ("sufficient for most software development teams");
- short ADRs in the repo;
- diagrams as code that render where people already read, which means Mermaid on GitHub.

arc42 is useful as a checklist or one-page canvas, not as a 12-section document to fill. On generated vs. hand-drawn: generate from a single model or from code when possible. Hand-authored diagrams-as-code drift through duplication, and a small custom SVG generator, as 믿집 has, is an accepted approach.

### Cited Findings
**ARCHITECTURE.md**
- matklad (2021, **older**, still the reference): projects of 10k–200k lines should add ARCHITECTURE.md. Newcomers need about 2x longer to write a patch but about 10x longer to find where to change.
  - "Keep it short", and include only things unlikely to change.
  - Don't try to keep it synchronized with the code: "revisit it a couple of times a year".
  - Structure: bird's-eye view, then a codemap ("a map of a country, not an atlas"), then invariants (especially absences such as "the model layer does not depend on views"), boundaries, and cross-cutting concerns.
  - Name files and types, but don't link to them, because links go stale.
  - Source: [matklad ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
- rust-analyzer's architecture doc is the canonical example. Its sections are Bird's Eye View, Entry Points, Code Map (per crate, with "Architecture Invariant" and "API Boundary" callouts) and Cross-Cutting Concerns (testing, error handling, observability). It is active (16,957 stars) — [rust-analyzer architecture](https://rust-analyzer.github.io/book/contributing/architecture.html); [rust-lang/rust-analyzer](https://github.com/rust-lang/rust-analyzer)
- Zulip's architecture overview is mostly prose with one simple diagram. It names concrete files and directories and explains the rationale, for example why Tornado must not block. Repo: 26,135 stars — [Zulip architecture overview](https://zulip.readthedocs.io/en/latest/overview/architecture-overview.html); [zulip/zulip](https://github.com/zulip/zulip)

**C4 model and tools**
- C4 has four levels (Context, Container, Component, Code) and three supporting diagrams (system landscape, dynamic, deployment). It is notation- and tool-independent, licensed CC BY 4.0 — [c4model.com](https://c4model.com/). "the system context and container diagrams are sufficient for most software development teams" — [c4model.com/diagrams](https://c4model.com/diagrams)
- C4 treats a server-side app plus a significant JS client as **two containers**, because they are "two separate process spaces". It counts managed S3 and RDS as containers when you own the buckets or schemas — [c4model.com/abstractions/container](https://c4model.com/abstractions/container)
- C4 covers static structure only. For state machines, business processes and data models it says to "supplement with other notations" — [c4model FAQ](https://c4model.com/faq)
- C4 recommends "Modelling" tools over "Diagramming", because a model can be validated, queried and renamed while boxes-and-lines cannot — [c4model.com/tooling](https://c4model.com/tooling)
- Simon Brown's InfoQ article (2018, **older**) says to give every diagram a title stating its type and scope, to give every element a name, type, technology and description, and to always include a legend — [InfoQ](https://www.infoq.com/articles/C4-architecture-model/)
- Simon Brown's "Diagrams as code 2.0" (2021, **older**) argues that tools like PlantUML and Mermaid keep each diagram in its own file. Shared definitions get duplicated and "have to be kept in sync by hand", which often doesn't happen. His fix is one model with many generated views, keeping authoring separate from rendering — [dev.to](https://dev.to/simonbrown/diagrams-as-code-2-0-82k)
- Structurizr is the C4 "models as code" reference tool. Its docs list unified `local`/`server`/`export`/`playground` commands (binaries v2026.09.19) and exports to PlantUML, C4-PlantUML, Mermaid and others — [docs.structurizr.com](https://docs.structurizr.com/); [structurizr/structurizr](https://github.com/structurizr/structurizr) (507 stars, last commit 2026-10-29)
- Structurizr status change in 2026: the older `structurizr/lite`, `structurizr/cli` and `structurizr/onpremises` repos are now **archived** (last commits Feb–Mar 2026), and `structurizr/dsl` returns 404 — [structurizr/lite](https://github.com/structurizr/lite); [structurizr/cli](https://github.com/structurizr/cli); [structurizr/onpremises](https://github.com/structurizr/onpremises)
- C4-PlantUML (7,447 stars, last commit 2026-08-26) provides Person/System/Container/Component/Rel/boundary macros plus dynamic and deployment diagrams. It needs PlantUML (Java), and clickable links only work in SVG — [plantuml-stdlib/C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML). PlantUML (13,386 stars) supports sequence, state, component, deployment, ER/IE and more. Its default layout engine is Graphviz, which must be installed, or Smetana, which is built in — [plantuml.com](https://plantuml.com/); [plantuml/plantuml](https://github.com/plantuml/plantuml)
- Mermaid has 90,920 stars and its last commit was 2026-10-28 — [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid). Its C4 syntax is still **experimental**: fixed styles, no `Lay_*` layout macros, positions depend on statement order — [Mermaid C4](https://mermaid.js.org/syntax/c4.html)
- GitHub renders Mermaid natively in Markdown. Support was announced 2022-02-14 **(older)** — [GitHub Docs: creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams); [GitHub blog](https://github.blog/developer-skills/github/include-diagrams-markdown-files-mermaid/)
- ThoughtWorks Radar: Mermaid is **Adopt** (Sep 2023), noting that GitHub and GitLab render it natively — [TW Radar Mermaid](https://www.thoughtworks.com/radar/tools/mermaid). D2 is **Trial** (Apr 2025) — [TW Radar D2](https://www.thoughtworks.com/radar/tools/d2). Diagrams as code is **Trial** (Oct 2020, **older**), noting that "writing a small SVG generator yourself is fairly simple" — [TW Radar diagrams as code](https://www.thoughtworks.com/radar/techniques/diagrams-as-code). The current Vol. 34 (Apr 2026) techniques page has no C4 or Structurizr blip — [TW Radar Vol 34 techniques](https://www.thoughtworks.com/radar/techniques/c4-model); [TW Radar tools](https://www.thoughtworks.com/radar/tools/structurizr)
- D2 (moved to `d2lang/d2`, 25,753 stars, last commit 2026-10-11) is a declarative diagram language with a CLI watch mode, fiscally sponsored by Hack Club — [d2lang.com tour](https://d2lang.com/tour/intro); [d2lang/d2](https://github.com/d2lang/d2)
- Python `diagrams` (42,763 stars, last commit 2026-10-15) needs Python 3.9+ and Graphviz. It has AWS/on-prem/C4 node sets and "does not control any actual cloud resources" — [mingrammer/diagrams](https://github.com/mingrammer/diagrams); [diagrams.mingrammer.com](https://diagrams.mingrammer.com/)
- Real repos embed Mermaid in their architecture pages:
  - GitLab: a component `graph`, a grouped component diagram with clickable nodes, and `sequenceDiagram` request flows — [GitLab architecture](https://docs.gitlab.com/development/architecture/)
  - Sentry: Mermaid component and event-pipeline flowcharts labelled "extremely simplified" — [Sentry architecture overview](https://develop.sentry.dev/application-architecture/overview/); [getsentry/sentry](https://github.com/getsentry/sentry) (45,678 stars)
- Korean, 2026: Yeogi (여기어때) found that Mermaid auto-layout of a 20-table ERD sprawls, cannot be adjusted by hand, and mangles types such as `BIGINT UNSIGNED`. Asking AI to draw diagrams gave different results on each run, so they gave the AI a deterministic ERD tool via MCP instead — [여기어때 기술블로그, 2026-10-10](https://techblog.gccompany.co.kr/%EC%8B%9C%ED%82%AC-%EB%95%8C%EB%A7%88%EB%8B%A4-%EB%8B%A4%EB%A5%B8-%EA%B2%B0%EA%B3%BC%EB%A5%BC-%EB%82%B4%EB%8A%94-ai%EC%97%90%EA%B2%8C-%EB%8F%84%EA%B5%AC%EB%A5%BC-%EC%A5%90%EC%97%AC-%EC%A3%BC%EC%97%88%EC%8A%B5%EB%8B%88%EB%8B%A4-ai%EA%B0%80-%EC%93%B0%EB%8A%94-erd-%EB%8F%84%EA%B5%AC-%EC%A0%9C%EC%9E%91%EA%B8%B0-f97eefa26354)

**arc42**
- arc42 has 12 sections: goals, constraints, context, solution strategy, building blocks, runtime, deployment, crosscutting concepts, decisions, quality, risks/tech debt, glossary. It is CC BY-SA 4.0 and offers a one-page "arc42 canvas" for when you "need something lighter than twelve sections" — [arc42 overview](https://arc42.org/overview); [arc42 canvas](https://canvas.arc42.org/); [arc42/arc42-template](https://github.com/arc42/arc42-template) (1,314 stars, last commit 2026-10-19)
- The C4 FAQ maps C4 to arc42: Context ↔ Context & Scope, Container ↔ Building Block level 1, and so on — [c4model FAQ](https://c4model.com/faq)

**ADRs**
- Nygard (2011, **older**): Title, Context, Decision, Status, Consequences. Keep each to one or two pages, number sequentially and never reuse numbers, keep them in the repo, and mark replaced ones "superseded" instead of deleting them — [Cognitect blog](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- MADR 4.0.0 (2024-09-17) offers full, minimal and bare variants, `NNNN-title-with-dashes.md` in `docs/decisions/`, and an optional "Confirmation" section on how compliance is checked, for example by a test — [MADR](https://adr.github.io/madr/); [adr/madr](https://github.com/adr/madr) (2,597 stars, last commit 2026-08-28). The ADR community hub is [adr.github.io](https://adr.github.io/) and the examples collection is [architecture-decision-record](https://github.com/architecture-decision-record/architecture-decision-record) (17,347 stars)
- Tooling status: `npryce/adr-tools` (5,748 stars) last changed 2020-03-30 and `thomvaill/log4brains` on 2024-12-17, so both are stale **(older)** — [adr-tools](https://github.com/npryce/adr-tools); [log4brains](https://github.com/thomvaill/log4brains)
- ThoughtWorks Radar lists lightweight ADRs as **Adopt** (May 2018, **older**). They should live in source control, not a wiki — [TW Radar](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- Fowler's bliki (2026-03-24) advises about one page in inverted-pyramid style, kept in `doc/adr`. Records "should never be reopened or edited", only superseded — [martinfowler.com ADR](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)
- Microsoft (2026-04) treats the log as append-only and asks each record to state its confidence level — [Microsoft Learn](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- AWS treats ADRs as immutable once accepted and suggests reviews open with 10–15 minutes of silent reading — [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- The UK GDS/DSIT ADR framework (2025-11-04) adds "Stakeholders consulted" and assigns decision levels — [GOV.UK](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework)
- **These sources disagree on editing accepted ADRs.** Polar fixes accepted ADRs in place when the text was wrong or incomplete, and supersedes them only when the decision itself changed. It argues git history keeps every version anyway — [Polar ADR index](https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/decisions/index.mdx). Fowler, Microsoft and AWS (above) say never edit
- Polar's ADR practice in detail:
  - One global sequence for the monorepo, with an **Area** field (Backend/Frontend/Infra/Cross-cutting).
  - Statuses are Accepted or Superseded only; proposals live in open PRs.
  - The goal is that a newcomer can read the whole log "in under an hour".
  - It has 14 ADRs, for example ADR-0003 "One request or task is one transaction" and ADR-0012 "Minimize data in AI API calls".
  - Agents must treat Accepted ADRs as binding and cite violations by id.
  - Its template is Status/Area/Date, Context (2–4 sentences), Decision (1–2 sentences), Consequences, Alternatives, References.
  - Source: [Polar ADR index](https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/decisions/index.mdx); [Polar ADR template](https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/decisions/template.mdx)
- Polar separates design docs (forward-looking, pages long, stale after shipping, with a mandatory "Security considerations" section) from ADRs (one page, kept current) — [Polar design-doc template](https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/design-documents/template.mdx)
- Korean, 2026: Inflearn's backend team records ADRs and links them from CLAUDE.md/AGENTS.md so coding agents get the decision context — [인프랩 기술블로그, 2026-06-30](https://tech.inflab.com/20260621-study-agent/학습에이전트%20-%20Building%20the%20Brain/)

**Agent-facing docs (AGENTS.md)**
- AGENTS.md is "a README for agents", now stewarded by the Agentic AI Foundation under the Linux Foundation. It claims use in 60k+ projects, has no required fields, and in monorepos the nearest file wins — [agents.md](https://agents.md/); [agentsmd/agents.md](https://github.com/agentsmd/agents.md) (25,205 stars)
- Cal.diy's AGENTS.md has "Always do / Ask first / Never do" boundaries, PR limits (<500 changed lines, <10 code files), "Never put business logic in repositories", and an `agents/` rules directory with an index — [cal.diy AGENTS.md](https://raw.githubusercontent.com/calcom/cal.diy/main/AGENTS.md); [agents/README.md](https://raw.githubusercontent.com/calcom/cal.diy/main/agents/README.md)
- Plane's and Twenty's agent files are short: commands, style and gotchas — [Plane AGENTS.md](https://raw.githubusercontent.com/makeplane/plane/preview/AGENTS.md); [Twenty CLAUDE.md](https://raw.githubusercontent.com/twentyhq/twenty/main/CLAUDE.md)

### Inferences
- 믿집 already has most pieces (AGENTS.md, docs/design, generated SVGs, docs/adr). What it lacks is a **single short, stable ARCHITECTURE.md** that the design docs and diagrams hang from, plus a one-line "status/area" header and an index for ADRs.
- The Python SVG generators (`docs/architecture/src/*.py` + `svgkit.py`) fit the Radar's "small SVG generator" note and the 여기어때 finding that layout control matters.
  - Their weakness is the same one Simon Brown names: each script hand-repeats element names. Prevent drift with a shared element list in `svgkit.py`, or a CI step that regenerates and fails on diff.
  - For small or volatile diagrams (state, sequence, ERD fragments) inside Markdown, Mermaid is cheaper because GitHub renders it in PR diffs.
- Structurizr is technically the "correct" C4 tool, but its 2026 repo consolidation and Java/Docker requirement make it poor value for a one-month student project.

### Gaps
- arc42's FAQ site (`faq.arc42.org`, `docs.arc42.org/faq/`) could not be retrieved, so arc42's official "lean" guidance is not quoted.
- The C4 tooling page did not render its tool list in text.
- I found no Korean 2023–2026 blog post specifically on the C4 model. This may be because search was unavailable rather than because none exist.

## Q4. How should state machines, workflow sequences and event/state history be documented?

### Takeaway
Use three artifacts per workflow:
1. A **state diagram** (Mermaid `stateDiagram-v2`, rendered on GitHub).
2. A **transition table** that is the real spec, with columns from → to, event, allowed actor, guards, side effects/notifications, and the history row written.
3. One or two **sequence diagrams** for the cross-process path (web → API → DB → `jobs` → arq worker → SES/LLM).

Where possible, generate the diagram from the code's single source of truth (python-statemachine can emit Mermaid). Back the documentation with an event/history table so the documented transitions are observable in data.

### Cited Findings
- Mermaid `stateDiagram-v2` supports `[*]` start/end, labelled transitions, composite states, `<<choice>>`, `<<fork>>`/`<<join>>`, notes, concurrency (`--`) and `direction` — [Mermaid state diagrams](https://mermaid.js.org/syntax/stateDiagram.html)
- Mermaid `sequenceDiagram` supports `actor`/participant aliases, sync and async arrows (`->>`, `-)`), activations, `alt`/`opt`/`loop`/`par`/`critical`/`break`, notes, `autonumber`, and `box` grouping (no hex colors) — [Mermaid sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html)
- GitLab documents request flows (`git fetch` over HTTP/SSH) as Mermaid `sequenceDiagram` blocks in its architecture page — [GitLab architecture](https://docs.gitlab.com/development/architecture/)
- python-statemachine 3.2.2 declares states and transitions in code, with guards (`cond=`/`unless=`) and async callbacks. It can export `f"{sm:mermaid}"` and a Markdown table `f"{sm:md}"`, or PNG via Graphviz — [python-statemachine docs](https://python-statemachine.readthedocs.io/en/latest/). The repo is now at `fgmacedo/python-statemachine` (1,327 stars, last commit 2026-10-16); `python-statemachine/python-statemachine` returns 404 — [fgmacedo/python-statemachine](https://github.com/fgmacedo/python-statemachine)
- `pytransitions/transitions` (6,600 stars, last commit 2025-09-09) has `GraphMachine` diagram extensions, including an async variant — [pytransitions README](https://raw.githubusercontent.com/pytransitions/transitions/master/README.md); [pytransitions/transitions](https://github.com/pytransitions/transitions). XState (30,374 stars, active) is the TypeScript statechart option — [statelyai/xstate](https://github.com/statelyai/xstate)
- Sharetribe models every transition with actor, actions and notifications in one file and visualises each version in the Console — [Sharetribe docs](https://www.sharetribe.com/docs/concepts/transaction-process/); [default-negotiation process.edn](https://raw.githubusercontent.com/sharetribe/web-template/main/ext/transaction-processes/default-negotiation/process.edn)
- Saleor's state docs pair each state with the mutation or setting that moves it and the stock side effect — [Saleor order status](https://docs.saleor.io/developer/checkout/order-status)
- History tables in production apps: Saleor `OrderEvent` (type + parameters JSON + user/app), cal.diy `BookingAudit` (actor/source/action/operationId/data/context, no FKs), Mastodon `admin_action_logs` (actor, action, polymorphic target, recorded_changes) — [Saleor models.py](https://raw.githubusercontent.com/saleor/saleor/main/saleor/order/models.py); [cal.diy schema](https://raw.githubusercontent.com/calcom/cal.diy/main/packages/prisma/schema.prisma); [Mastodon action_log.rb](https://raw.githubusercontent.com/mastodon/mastodon/main/app/models/admin/action_log.rb)
- For side effects after a state change, the transactional outbox avoids lost or phantom messages but requires idempotent consumers — [microservices.io outbox](https://microservices.io/patterns/data/transactional-outbox.html); arq jobs may run more than once — [arq docs](https://arq-docs.helpmanual.io/)
- Korean, 2026: during a dual-write migration, SOCAR documented the **current state, target state and rollback method** for each phase so others could take over or roll back. They also produced ERDs for 10 systems and shared them — [쏘카 기술블로그, 2026-02-14](https://tech.socar.kr/dev/2026/02/14/legacy-code-and-docs-improvement)
- Korean, 2024 (**older**): Gmarket's per-system state definitions, cross-system stage mapping and state diagram came before the state-machine implementation — [지마켓 기술블로그](https://dev.gmarket.com/115)

### Inferences
- 믿집's `quote-flow-v3.2.md` §4 currently draws the per-trade state machine as ASCII art in a code block. Converting it to `stateDiagram-v2` keeps it diffable and renders it on GitHub. Adding a transition table with columns `현재 상태 | 이벤트(API) | 누가(고객/업체/관리자/시간) | 다음 상태 | 남기는 이력 | 알림/작업(jobs)` would turn the prose rules in AGENTS.md §3 into a reviewable spec.
- If status changes are centralised in one function per feature, for example `quote.service.transition(...)`, the same table can drive both validation and tests (one parametrized test per row). That gives the "living" property without adopting a state-machine library. A library such as python-statemachine is optional and worthwhile only if the Mermaid export is wanted.
- One sequence diagram covers the four representative flows already in `code-flow.svg`: "가견적 요청 → 업체 제출 → 실측 요청 → 실측 견적 → 확정", including the `jobs` row, commit, arq enqueue and SES email.

### Gaps
- I found no empirical study comparing state tables with diagrams for comprehension.
- I did not fetch Sharetribe's Console visualiser screenshots or Medusa's workflow-execution UI.

## Q5. What evidence is there on which documentation actually gets read and maintained (Diátaxis, docs-as-code, living documentation)?

### Takeaway
The evidence points the same way: docs that live in the repo, change in the same PR as the code, have owners, and are short get read and stay correct. Large wikis and big upfront specs rot. Quantitatively, DORA links documentation quality to large amplification of every technical practice, and surveys show stale docs are near-universal (93%). Newer Korean and industry practice (2026) treats repo docs as the shared context for both humans and coding agents, and increasingly generates or validates docs from code.

### Cited Findings
- DORA (2022 research, **older**, reaffirming 2021) found "a clear link between documentation quality and organizational performance". Teams with above-average docs saw much higher performance lift from every practice, for example trunk-based development +1525% vs +36% and CI +750% vs +34% — [DORA documentation quality](https://dora.dev/capabilities/documentation-quality/)
- GitHub's Open Source Survey 2017 (**older**): 93% observed incomplete or outdated documentation, "a pervasive problem", and 60% of contributors rarely or never contribute to docs — [opensourcesurvey.org/2017](https://opensourcesurvey.org/2017/)
- Stack Overflow 2025: technical documentation is the most-used learning resource (67.8%), ahead of Stack Overflow (51.4%) and AI tools (44%) — [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/developers)
- *Software Engineering at Google*, ch. 10 (**older**) tells the story of a wiki with no owners where about 90% of documents had no views or updates in recent months when it was deprecated. Moving docs into source control with owners, review, bugs and freshness dates worked better. Every document should have a single purpose (reference, design doc, tutorial, conceptual, landing page) — [SWE at Google ch.10](https://abseil.io/resources/swe-book/html/ch10.html)
- Google's documentation guide says to keep minimum viable documentation, update docs in the same change as the code, delete dead docs, and treat docs "like a bonsai tree" that is alive but frequently trimmed — [Google docguide best practices](https://google.github.io/styleguide/docguide/best_practices.html)
- Docs-as-code means issue trackers, git, plain-text markup, code review and automated tests for docs. Teams can block merges that lack docs — [Write the Docs](https://www.writethedocs.org/guide/docs-as-code/). Spotify's TechDocs (docs-like-code in Backstage) reports 5,000+ documentation sites and about 10,000 daily hits — [Backstage TechDocs](https://backstage.io/docs/features/techdocs/)
- Diátaxis has four types (tutorials, how-to guides, reference, explanation) on two axes: action vs cognition, and acquisition vs application. Adopters named on its site include Vonage, Gatsby and Cloudflare developer docs — [diataxis.fr](https://diataxis.fr/); [Diátaxis compass](https://diataxis.fr/compass/)
- Korean, 2026: Toss's data team reorganised repo docs using Diátaxis and OKF so agents (and people) find the right doc. They cite OpenAI's "harness engineering" post and an Anthropic case where structured context raised analysis accuracy from 21% to over 95% (secondhand) — [토스 테크, 2026-10-16](https://toss.tech/article/dw-airflow-migration)
- Korean, 2026: LY Corp's "LLM Wiki" keeps a code-derived SSOT.
  - A raw layer is reverse-extracted from code and config; a knowledge layer is built per domain.
  - On every merged PR, GitHub Actions extracts spec changes into a PR that a human reviews.
  - A periodic lint checks link integrity, identifier fidelity and freshness.
  - ADRs are attached to PRs only for intent that code cannot show. No quantitative results are reported.
  - Source: [LY Corp 기술블로그, 2026-08-28](https://techblog.lycorp.co.jp/ko/llm-wiki-code-driven-knowledge-ssot)
- Korean, 2026: Daangn's merged FE+BE team said the architecture diagrams and DB-schema docs kept in each service repo served as onboarding material "before" they became AI context. Technical changes still go through tech-spec review — [당근 테크블로그, 2026-07-23](https://medium.com/daangn/%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%EC%99%80-%EB%B0%B1%EC%97%94%EB%93%9C%EB%A5%BC-%ED%95%9C-%ED%8C%80%EC%9C%BC%EB%A1%9C-%ED%95%A9%EC%B9%98%EB%A9%B4-%EC%96%B4%EB%96%A4-%EC%9D%BC%EC%9D%B4-%EC%9D%BC%EC%96%B4%EB%82%A0%EA%B9%8C-f8b32edb2eb1)
- Korean, 2024 (**older**): Banksalad's "테크스펙은 문서가 아니다" treats a tech spec as a discussion forum.
  - Draft in 1–2 days and close the discussion within a week.
  - Specs are not updated afterwards; a changed decision gets a new spec.
  - Durable facts move into IDL comments, tests and README.
  - Source: [뱅크샐러드 기술블로그, 2024-11-11](https://blog.banksalad.com/tech/techspec-is-not-doc/)
- ThoughtWorks Radar Vol. 34 (Apr 2026, **Assess**) on "Architecture drift reduction with LLMs": coding agents accelerate drift. The suggested remedy pairs deterministic checks (ArchUnit, Spring Modulith, Spectral) with LLM evaluation and small, verified fixes — [TW Radar](https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms)
- Enforcement as living documentation:
  - Import Linter supports layers, independence, forbidden, protected and acyclic-siblings contracts, configured in `.importlinter`, run with `lint-imports` — [Import Linter docs](https://import-linter.readthedocs.io/en/stable/); [seddonym/import-linter](https://github.com/seddonym/import-linter) (1,240 stars, last commit 2026-10-29)
  - bulletproof-react forbids cross-feature imports with ESLint `import/no-restricted-paths` zones — [bulletproof-react project-structure.md](https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/project-structure.md); [alan2207/bulletproof-react](https://github.com/alan2207/bulletproof-react) (36,019 stars)
  - CODEOWNERS auto-requests owner review and can be made required by branch protection — [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- Next.js (docs updated 2026-07-21) is "unopinionated" about project organisation. It offers private `_folders`, `(route groups)` and three layout strategies, and recommends choosing one strategy and being consistent — [Next.js project structure](https://nextjs.org/docs/app/getting-started/project-structure)

### Inferences
- For a student team, the decisive factor is **where the doc lives and when it is touched**, not which framework is used. Docs in the repo, reviewed in the same PR, short, with an owner and a date header, give the best chance of being read and maintained. Diátaxis is useful as a sorting lens:
  - README quick start = tutorial
  - `development.md`/runbook = how-to
  - OpenAPI + transition tables = reference
  - ARCHITECTURE.md + ADRs = explanation
- 믿집 should separate durable docs from ephemeral ones, following Polar and Banksalad. Design docs such as `quote-flow-v3.2.md` may go stale after shipping, as long as their decisions are distilled into ADRs, and their stable facts are distilled into ARCHITECTURE.md, the transition tables and tests.
- The executable check of the AGENTS.md layer table is the highest-leverage "living doc". In the Dify style, write the 층 규칙 as an import-linter `layers` contract plus `independence` contracts (`account | project | vendor`), run in CI. It is also exactly what the 2026 Radar entry recommends against agent-induced drift.

### Gaps
- No peer-reviewed study was fetched on ADR adoption outcomes (for example, the ICSE papers on documentation issues). The search budget was gone and the URLs were unknown.
- I could not retrieve OpenAI's "harness engineering" post (HTTP 403); it is cited only secondhand via Toss.
- I could not retrieve Martraire's *Living Documentation* book page (HTTP 403).
- Musinsa's 2026 post on domain-knowledge sharing returned 403.

## Q6. Ranked recommendation: (a) which exemplar repos to learn from and what to borrow, and (b) the minimal architecture documentation set for 믿집

### Takeaway
(a) Learn from Polar first: it is the closest stack, with module layout, generated client, ADRs and agent docs. Then Dify for executable layer rules and the backend architecture doc, Sharetribe's negotiation process for the quote state machine, cal.diy and Saleor for history tables and agent boundaries, and full-stack-fastapi-template for Compose and dev docs. Use rust-analyzer/matklad, GitLab/Sentry and Plane/Medusa as format and pattern references.

(b) Keep the doc set to seven items:
1. README
2. AGENTS.md (root plus backend/frontend)
3. a new short ARCHITECTURE.md
4. two C4-level diagrams plus a deployment view
5. ADRs with an index
6. one workflow doc per state machine (Mermaid state + transition table + sequence)
7. an import-linter contract that executes the layer rules

### Cited Findings
**(a) Ranked exemplars (checked 2026-10-29)**

1. **polarsource/polar.** FastAPI + Next.js 16 + worker, Apache-2.0, active. Borrow:
   - the per-module `endpoints/service/repository/schemas/tasks` contract and the "all queries in repository" rule;
   - status-coded business errors;
   - ADR-0003 "one request or task is one transaction";
   - generating the TS client from OpenAPI;
   - the ADR index (Area field, design doc vs ADR table, "readable in under an hour") and the design-doc template's mandatory security section;
   - a root AGENTS.md that links to per-area AGENTS.md.
   - Caveat: Dramatiq, not arq, and a much larger codebase.
   - Sources: [polar](https://github.com/polarsource/polar); [AGENTS.md](https://raw.githubusercontent.com/polarsource/polar/main/AGENTS.md); [server/AGENTS.md](https://raw.githubusercontent.com/polarsource/polar/main/server/AGENTS.md); [ADR index](https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/decisions/index.mdx)
2. **langgenius/dify.** Flask/Celery API + Next.js + Compose. Borrow:
   - `docs/BACKEND_ARCHITECTURE.md` (layers, review checks);
   - the `.importlinter` layers contract with an exact legacy-exception baseline that is set to shrink;
   - "nearest scoped AGENTS.md".
   - Caveat: Flask, and huge.
   - Sources: [BACKEND_ARCHITECTURE.md](https://raw.githubusercontent.com/langgenius/dify/main/docs/BACKEND_ARCHITECTURE.md); [.importlinter](https://raw.githubusercontent.com/langgenius/dify/main/api/.importlinter)
3. **sharetribe/web-template, `default-negotiation`.** Borrow: the state and transition naming, the actor column including operator and time, and per-transition notifications. This is the closest public model of "quote requested → offer → accept → deliver → review". Caveat: the backend is a hosted SaaS. Source: [process.edn](https://raw.githubusercontent.com/sharetribe/web-template/main/ext/transaction-processes/default-negotiation/process.edn)
4. **calcom/cal.diy** (redirected from cal.com). Borrow:
   - the `BookingAudit` + `AuditActor` design (actor type, source, action, operationId, JSON data/context, no-FK retention);
   - AGENTS.md "Always / Ask first / Never" plus PR size limits.
   - Caveat: Next.js/tRPC/Prisma, and the repo positions itself for non-production self-hosting.
   - Sources: [schema.prisma](https://raw.githubusercontent.com/calcom/cal.diy/main/packages/prisma/schema.prisma); [AGENTS.md](https://raw.githubusercontent.com/calcom/cal.diy/main/AGENTS.md)
5. **saleor/saleor.** Borrow: per-state documentation with triggering mutations and side effects, and the `OrderEvent` table (type enum + parameters JSON + user/app). Sources: [order status docs](https://docs.saleor.io/developer/checkout/order-status); [models.py](https://raw.githubusercontent.com/saleor/saleor/main/saleor/order/models.py)
6. **fastapi/full-stack-fastapi-template.** Borrow: the `compose.yml` + `compose.override.yml` split, `development.md` / `deployment-docker-compose.md` doc split, Mailpit for local email, Playwright e2e and the generated client. Don't copy its flat `models.py`/`crud.py` layout. Source: [repo](https://github.com/fastapi/full-stack-fastapi-template)
7. **rust-analyzer architecture.md (matklad's format).** Borrow the ARCHITECTURE.md skeleton: bird's-eye view, entry points, code map, "Architecture Invariant" callouts, cross-cutting concerns. Sources: [architecture.md](https://rust-analyzer.github.io/book/contributing/architecture.html); [matklad](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
8. **GitLab / Sentry architecture pages.** Borrow Mermaid component and sequence diagrams embedded in Markdown with a component table. Sources: [GitLab](https://docs.gitlab.com/development/architecture/); [Sentry](https://develop.sentry.dev/application-architecture/overview/)
9. **makeplane/plane.** Borrow the Compose service split (`api`, `worker`, `beat-worker`, `migrator`, separate `admin` app) and short AGENTS.md. Caveat: AGPL, and the frontend is React Router, not Next.js. Source: [compose](https://raw.githubusercontent.com/makeplane/plane/preview/deployments/cli/community/docker-compose.yml)
10. **medusajs/medusa.** Borrow the rule "modules can't access other modules' services or data models" and the idea that cross-module flows live in orchestrating workflows with compensation. Caveat: TypeScript. Source: [isolation](https://docs.medusajs.com/learn/fundamentals/modules/isolation)

Not recommended as primary exemplars for this team:
- RealWorld implementations (stale or archived; use only the spec-plus-Hurl idea)
- PetClinic (Java)
- eShop, Online Boutique and the AWS Retail Store (microservices/K8s)
- eShopOnContainers, Netflix Dispatch, vercel/commerce and aws-modern-application-workshop (archived)
- kgrzybek/modular-monolith-with-ddd (excellent docs, but .NET with no commits since 2024-04)
- Sources: see Q1 citations.

**(b) Minimal documentation set — supporting evidence**
- ARCHITECTURE.md should be short, stable and revisited a couple of times a year — [matklad](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
- Context + Container diagrams "are sufficient for most software development teams", and the Next.js web and the API count as separate containers — [c4model.com/diagrams](https://c4model.com/diagrams); [container](https://c4model.com/abstractions/container)
- ADRs: use a one-page template with the ADRs in the repo — [Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions); [MADR](https://adr.github.io/madr/); [Polar template](https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/decisions/template.mdx)
- Mermaid renders natively on GitHub and is Radar "Adopt" — [GitHub Docs](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams); [TW Radar](https://www.thoughtworks.com/radar/tools/mermaid)
- Change docs in the same change as the code — [Google docguide](https://google.github.io/styleguide/docguide/best_practices.html)
- Enforce boundaries in lint/CI — [Dify .importlinter](https://raw.githubusercontent.com/langgenius/dify/main/api/.importlinter); [Packwerk](https://shopify.engineering/enforcing-modularity-rails-apps-packwerk); [당근 아키텍처 테스트](https://medium.com/daangn/%EC%B2%9C%EB%A7%8C-mau%EB%A5%BC-%EC%A7%80%ED%83%B1%ED%95%98%EB%8A%94-%EC%BB%A4%EB%AE%A4%EB%8B%88%ED%8B%B0-%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84-%EC%86%8C%EA%B0%9C%ED%95%B4%EC%9A%94-090fb4021e20)

#### Full source index (every URL consulted, grouped)

**Repositories, GitHub pages or raw files (activity checked 2026-10-29):**
- https://github.com/realworld-apps/realworld
- https://github.com/realworld-apps/realworld/tree/main/specs
- https://raw.githubusercontent.com/realworld-apps/realworld/main/specs/api/README.md
- https://github.com/nsidnev/fastapi-realworld-example-app
- https://github.com/reck1ess/next-realworld-example-app
- https://github.com/spring-projects/spring-petclinic
- https://github.com/spring-petclinic/spring-petclinic-microservices
- https://github.com/dotnet/eShop
- https://github.com/dotnet-architecture/eShopOnContainers
- https://github.com/GoogleCloudPlatform/microservices-demo
- https://github.com/aws-containers/retail-store-sample-app
- https://github.com/aws-samples/aws-modern-application-workshop
- https://github.com/vercel/commerce
- https://github.com/nextjs/saas-starter
- https://github.com/fastapi/full-stack-fastapi-template
- https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/backend/README.md
- https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/development.md
- https://github.com/fastapi/full-stack-fastapi-template/tree/master/backend/app
- https://github.com/zhanymkanov/fastapi-best-practices
- https://github.com/Kludex/fastapi-tips
- https://github.com/iktakahiro/dddpy
- https://github.com/ivan-borovets/fastapi-clean-example
- https://github.com/Netflix/dispatch
- https://github.com/mealie-recipes/mealie
- https://github.com/polarsource/polar
- https://raw.githubusercontent.com/polarsource/polar/main/AGENTS.md
- https://raw.githubusercontent.com/polarsource/polar/main/server/AGENTS.md
- https://raw.githubusercontent.com/polarsource/polar/main/server/polar/backoffice/AGENTS.md
- https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/decisions/index.mdx
- https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/decisions/template.mdx
- https://raw.githubusercontent.com/polarsource/polar/main/handbook/engineering/design-documents/template.mdx
- https://raw.githubusercontent.com/polarsource/polar/main/clients/apps/web/package.json
- https://github.com/langgenius/dify
- https://raw.githubusercontent.com/langgenius/dify/main/AGENTS.md
- https://raw.githubusercontent.com/langgenius/dify/main/api/AGENTS.md
- https://raw.githubusercontent.com/langgenius/dify/main/docs/BACKEND_ARCHITECTURE.md
- https://raw.githubusercontent.com/langgenius/dify/main/api/.importlinter
- https://raw.githubusercontent.com/langgenius/dify/main/docker/docker-compose.yaml
- https://raw.githubusercontent.com/langgenius/dify/main/api/pyproject.toml
- https://raw.githubusercontent.com/langgenius/dify/main/web/package.json
- https://github.com/makeplane/plane
- https://raw.githubusercontent.com/makeplane/plane/preview/AGENTS.md
- https://raw.githubusercontent.com/makeplane/plane/preview/deployments/cli/community/docker-compose.yml
- https://raw.githubusercontent.com/makeplane/plane/preview/apps/web/package.json
- https://github.com/twentyhq/twenty
- https://raw.githubusercontent.com/twentyhq/twenty/main/CLAUDE.md
- https://raw.githubusercontent.com/twentyhq/twenty/main/LICENSE
- https://github.com/calcom/cal.diy (redirect target of https://github.com/calcom/cal.com)
- https://raw.githubusercontent.com/calcom/cal.diy/main/AGENTS.md
- https://raw.githubusercontent.com/calcom/cal.diy/main/agents/README.md
- https://raw.githubusercontent.com/calcom/cal.diy/main/packages/prisma/schema.prisma
- https://github.com/medusajs/medusa
- https://github.com/saleor/saleor
- https://raw.githubusercontent.com/saleor/saleor/main/saleor/order/models.py
- https://raw.githubusercontent.com/saleor/saleor/main/saleor/order/__init__.py
- https://github.com/saleor/saleor-dashboard
- https://github.com/sharetribe/web-template
- https://github.com/sharetribe/web-template/tree/main/ext/transaction-processes
- https://raw.githubusercontent.com/sharetribe/web-template/main/ext/transaction-processes/default-negotiation/process.edn
- https://raw.githubusercontent.com/sharetribe/web-template/main/ext/transaction-processes/default-booking/process.edn
- https://github.com/sharetribe/example-processes
- https://github.com/sharetribe/sharetribe
- https://github.com/mastodon/mastodon
- https://raw.githubusercontent.com/mastodon/mastodon/main/README.md
- https://raw.githubusercontent.com/mastodon/mastodon/main/app/models/admin/action_log.rb
- https://raw.githubusercontent.com/mastodon/mastodon/main/db/schema.rb
- https://github.com/discourse/discourse
- https://raw.githubusercontent.com/discourse/discourse/main/README.md
- https://raw.githubusercontent.com/discourse/discourse/main/app/models/user_history.rb
- https://github.com/gitlabhq/gitlabhq
- https://github.com/Shopify/packwerk
- https://github.com/kgrzybek/modular-monolith-with-ddd
- https://github.com/basecamp/once-campfire
- https://raw.githubusercontent.com/basecamp/once-campfire/main/README.md
- https://github.com/basecamp/kamal
- https://github.com/docker/awesome-compose
- https://github.com/rust-lang/rust-analyzer
- https://raw.githubusercontent.com/rust-lang/rust-analyzer/master/docs/book/src/contributing/architecture.md
- https://github.com/zulip/zulip
- https://github.com/getsentry/sentry
- https://github.com/PostHog/posthog
- https://github.com/langfuse/langfuse
- https://github.com/open-webui/open-webui
- https://github.com/documenso/documenso
- https://github.com/mermaid-js/mermaid
- https://github.com/d2lang/d2 (redirect from terrastruct/d2)
- https://github.com/plantuml/plantuml
- https://github.com/plantuml-stdlib/C4-PlantUML
- https://github.com/mingrammer/diagrams
- https://github.com/structurizr/structurizr
- https://raw.githubusercontent.com/structurizr/structurizr/main/README.md
- https://github.com/structurizr/lite
- https://github.com/structurizr/cli
- https://github.com/structurizr/onpremises
- https://github.com/structurizr/dsl (404)
- https://github.com/arc42/arc42-template
- https://github.com/adr/madr
- https://github.com/architecture-decision-record/architecture-decision-record (redirect from joelparkerhenderson/…)
- https://github.com/npryce/adr-tools
- https://github.com/thomvaill/log4brains
- https://github.com/agentsmd/agents.md
- https://github.com/seddonym/import-linter
- https://github.com/fgmacedo/python-statemachine
- https://github.com/python-statemachine/python-statemachine (404)
- https://github.com/pytransitions/transitions
- https://raw.githubusercontent.com/pytransitions/transitions/master/README.md
- https://github.com/statelyai/xstate
- https://github.com/python-arq/arq
- https://github.com/alan2207/bulletproof-react
- https://raw.githubusercontent.com/alan2207/bulletproof-react/master/docs/project-structure.md
- https://github.com/marmelab/react-admin
- https://github.com/refinedev/refine
- https://github.com/aminalaee/sqladmin
- https://github.com/jowilf/starlette-admin

**Docs, blogs and standards:**
- https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html
- https://rust-analyzer.github.io/book/contributing/architecture.html
- https://zulip.readthedocs.io/en/latest/overview/architecture-overview.html
- https://docs.joinmastodon.org/dev/overview/
- https://develop.sentry.dev/application-architecture/overview/
- https://docs.gitlab.com/development/architecture/
- https://docs.gitlab.com/development/software_design/
- https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/modular_monolith/
- https://shopify.engineering/shopify-monolith
- https://shopify.engineering/enforcing-modularity-rails-apps-packwerk
- https://shopify.engineering/a-packwerk-retrospective
- https://signalvnoise.com/svn3/the-majestic-monolith/
- https://martinfowler.com/bliki/MonolithFirst.html
- https://www.kamilgrzybek.com/blog/posts/modular-monolith-primer
- https://docs.spring.io/spring-modulith/reference/documentation.html
- https://spring-petclinic.github.io/
- https://docs.realworld.show/
- https://langfuse.com/self-hosting
- https://nextjs.org/docs/app/getting-started/project-structure
- https://www.sharetribe.com/docs/concepts/transaction-process/
- https://docs.medusajs.com/learn/fundamentals/workflows
- https://docs.medusajs.com/learn/fundamentals/modules
- https://docs.medusajs.com/learn/fundamentals/modules/isolation
- https://docs.saleor.io/developer/checkout/order-status
- https://microservices.io/patterns/observability/audit-logging.html
- https://microservices.io/patterns/data/transactional-outbox.html
- https://martinfowler.com/eaaDev/EventSourcing.html
- https://wiki.postgresql.org/wiki/Audit_trigger_91plus
- https://arq-docs.helpmanual.io/
- https://python-statemachine.readthedocs.io/en/latest/
- https://import-linter.readthedocs.io/en/stable/ (and the 404 at …/contract_types.html)
- https://c4model.com/
- https://c4model.com/diagrams
- https://c4model.com/faq
- https://c4model.com/tooling
- https://c4model.com/abstractions/container
- https://www.infoq.com/articles/C4-architecture-model/
- https://dev.to/simonbrown/diagrams-as-code-2-0-82k
- https://docs.structurizr.com/
- https://arc42.org/overview
- https://canvas.arc42.org/
- https://faq.arc42.org/ (empty) and https://docs.arc42.org/faq/ (404)
- https://mermaid.js.org/syntax/stateDiagram.html
- https://mermaid.js.org/syntax/sequenceDiagram.html
- https://mermaid.js.org/syntax/c4.html
- https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams
- https://github.blog/developer-skills/github/include-diagrams-markdown-files-mermaid/
- https://d2lang.com/tour/intro
- https://diagrams.mingrammer.com/
- https://plantuml.com/
- https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
- https://www.thoughtworks.com/radar/techniques/diagrams-as-code
- https://www.thoughtworks.com/radar/techniques/c4-model (served Vol 34 techniques page)
- https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms
- https://www.thoughtworks.com/radar/tools/mermaid
- https://www.thoughtworks.com/radar/tools/d2
- https://www.thoughtworks.com/radar/tools/structurizr (served Vol 34 tools page)
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- https://adr.github.io/
- https://adr.github.io/madr/
- https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
- https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
- https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
- https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework
- https://agents.md/
- https://diataxis.fr/
- https://diataxis.fr/compass/
- https://google.github.io/styleguide/docguide/best_practices.html
- https://abseil.io/resources/swe-book/html/ch10.html
- https://www.writethedocs.org/guide/docs-as-code/
- https://backstage.io/docs/features/techdocs/
- https://dora.dev/capabilities/documentation-quality/
- https://opensourcesurvey.org/2017/
- https://survey.stackoverflow.co/2025/developers
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners

**Korean sources (blogs reached via RSS or sitemap, then the article):**
- https://medium.com/daangn/%EC%B2%9C%EB%A7%8C-mau%EB%A5%BC-%EC%A7%80%ED%83%B1%ED%95%98%EB%8A%94-%EC%BB%A4%EB%AE%A4%EB%8B%88%ED%8B%B0-%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84-%EC%86%8C%EA%B0%9C%ED%95%B4%EC%9A%94-090fb4021e20
- https://medium.com/daangn/%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%EC%99%80-%EB%B0%B1%EC%97%94%EB%93%9C%EB%A5%BC-%ED%95%9C-%ED%8C%80%EC%9C%BC%EB%A1%9C-%ED%95%A9%EC%B9%98%EB%A9%B4-%EC%96%B4%EB%96%A4-%EC%9D%BC%EC%9D%B4-%EC%9D%BC%EC%96%B4%EB%82%A0%EA%B9%8C-f8b32edb2eb1
- https://toss.tech/article/dw-airflow-migration
- https://techblog.lycorp.co.jp/ko/llm-wiki-code-driven-knowledge-ssot
- https://tech.socar.kr/dev/2026/02/14/legacy-code-and-docs-improvement
- https://blog.banksalad.com/tech/techspec-is-not-doc/
- https://tech.inflab.com/20260621-study-agent/ (학습에이전트 - Building the Brain)
- https://techblog.gccompany.co.kr/ (AI가 쓰는 ERD 도구 제작기, full URL in Q3)
- https://dev.gmarket.com/115
- Feeds and sitemaps scanned, listing only: https://toss.tech/rss.xml, https://medium.com/feed/daangn, https://tech.kakao.com/feed/, https://techblog.lycorp.co.jp/ko/feed/index.xml, https://blog.banksalad.com/rss.xml, https://tech.inflab.com/rss.xml, https://techblog.gccompany.co.kr/feed, https://dev.gmarket.com/rss, https://oliveyoung.tech/rss.xml, https://techblog.woowahan.com/feed/, https://tech.socar.kr/feed.xml, https://medium.com/feed/musinsa-tech

**Attempted but not retrieved (403/404):**
- https://openai.com/index/harness-engineering/
- https://www.oreilly.com/library/view/living-documentation-continuous/9780134689418/
- the musinsa techblog article

### Inferences
**Proposed minimal doc set for 믿집.** Each item is small, lives in the repo, and is touched in the same PR as the code it describes.

1. **README.md**: what it is, how to run it, links. Already exists.
2. **AGENTS.md**: root rules. Already exists. Polar and Dify suggest two refinements:
   - add short `backend/AGENTS.md` and `frontend/AGENTS.md` ("nearest file wins"), so the root stays a table of contents;
   - add a line saying Accepted ADRs are binding and listing where ARCHITECTURE.md and the transition tables live.
3. **docs/ARCHITECTURE.md**, new, 1–2 pages in matklad format:
   - bird's-eye view;
   - code map (one line per package: `account | project | vendor`, `schedule → visit → quote`, `files | refprice | jobs`, `agent → calc`, `shared/db/queue/config`);
   - invariants written as absences (for example "the frontend never touches the DB, the LLM or money math", "`calc` knows no DB/HTTP/clock", "router never imports router");
   - cross-cutting concerns: error shape, sessions/permissions, jobs + commit-then-enqueue, money/date rules.
   - Existing `docs/design/app-structure.md` and `target-architecture.md` can be the source material.
4. **Diagrams, three views only:**
   - C4 System Context and Container: web (Next.js) and API as separate containers, plus worker, Postgres, Redis, S3, SES and OpenAI;
   - one Deployment view: EC2 + Compose + Caddy + RDS.
   - Keep the existing Python SVG generators for these, since layout control matters. Add a CI step that regenerates and fails on diff, and/or one shared element list to stop name drift.
   - Each diagram needs a title stating type and scope, plus a legend.
5. **docs/adr/** (exists: 0001–0003):
   - add `docs/adr/README.md` as an index (number · title · Area · Status · date);
   - adopt a one-page header (Status / Area / Date) with Context (2–4 sentences), Decision (1–2 sentences), Consequences and Alternatives;
   - decide and write down one edit policy: supersede-only (Nygard/Fowler/AWS) or Polar's "fix errors in place, supersede on change of mind".
6. **One workflow doc per state machine**, starting with the quote flow: a Mermaid `stateDiagram-v2`, the **transition table** (from · event/API · actor customer/vendor/admin/time · to · history row · job/notification), and one Mermaid `sequenceDiagram` (web → API → service → DB + `jobs` → commit → arq → SES/LLM). Pair it with a `*_event` history table spec (cal.diy/Saleor shape) and one parametrized test per table row.
7. **Executable architecture**:
   - an import-linter `.importlinter` with one `layers` contract mirroring AGENTS.md §2, plus `independence` contracts for the `|` groups, run in the existing `ci.yml`;
   - the one documented exception (`auth.service → vendor.repository`) listed as an exact `ignore_imports` entry, in the Dify style;
   - optionally, ESLint `import/no-restricted-paths` for frontend features, plus CODEOWNERS for `docs/` and `backend/app/*/`.

**Explicitly optional or skippable for this team:**
- full arc42: use the arc42 canvas only for a presentation slide;
- Structurizr: its repos were consolidated in 2026 and it needs Java/Docker;
- C4 component and code diagrams;
- Diátaxis restructuring: use it only as a lens for README, how-to, reference and explanation;
- event sourcing: a simple history table is enough.

These choices fit the constraints from the earlier sections: one month, a small team, docs read by both people and coding agents, and the 2026 Radar warning that agents speed up architecture drift unless there are deterministic checks.

### Gaps
- Star counts and "last commit" come from GitHub HTML and Atom feeds scraped on 2026-10-29, not the authenticated API. Default branches were assumed (`main`/`master`/`preview`).
- I did not inspect 믿집's existing ADR bodies or `ci.yml` in detail, so the exact import-linter contract text, and whether the current package names match AGENTS.md exactly, still need verification.
- I found no source quantifying how many student or bootcamp teams maintain ADRs or ARCHITECTURE.md, so the claim that this set is light enough for students rests on expert guidance, not measured outcomes.
