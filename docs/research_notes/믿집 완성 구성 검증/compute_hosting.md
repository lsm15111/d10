# Compute / hosting verification: single EC2 t4g.small + Docker Compose + Caddy (믿집, AWS Seoul, as of 2026-10-29)

Scope: the compute, container runtime, reverse proxy and single-host deployment parts of the proposed 믿집 architecture (one EC2 t4g.small in ap-northeast-2 running Caddy + Next.js 16 standalone + FastAPI (2 uvicorn workers) + Redis 8 + arq worker via Docker Compose; RDS/S3/SES/Route 53 managed; GitHub Actions → ECR → SSM Run Command deploys). RDS, S3, SES internals, the AI layer and app security are out of scope.

Method note: Seoul prices below were read directly from the AWS public price-list JSON files that power the AWS pricing pages (EC2/EBS files published 2026-10-28; ECS/Fargate 2026-10-19; VPC 2026-10-16; ELB 2026-09-11). Python wheel availability was read from the PyPI JSON API on 2026-10-29. The shared web-search budget ran out partway through, so later evidence comes from fetching known official pages directly. As a result there are fewer Korean community sources and HN/Reddit threads than planned (see Gaps).

---

## 1. Is one EC2 + Docker Compose the right platform in 2026 compared with ECS Express Mode/Fargate, Lightsail, Elastic Beanstalk, Fly.io/Render/Railway and App Runner?

### Takeaway
Yes. For a few hundred sign-ups, tens of concurrent users, a student team and RDS already fixed in Seoul, a single Seoul EC2 (or Lightsail) host running Compose is the cheapest option with low latency to RDS, and it is easy to operate. App Runner is closed to new customers, so it is not an option. ECS Express Mode is AWS's managed successor, but it costs roughly 3–4× more in Seoul because of the ALB, per-task Fargate billing and public IPv4. Fly.io, Render and Railway have no Korean region. What a single host gives up, compared with ECS, is built-in rolling deploys, health-based replacement and survival of host failure. Those gaps have to be covered with the additions in sections 5, 7 and 8.

### Cited Findings
- **App Runner:** AWS docs say App Runner "is no longer open to new customers". Existing customers can keep using it, and AWS recommends Amazon ECS Express Mode for everyone else — [AWS App Runner docs](https://docs.aws.amazon.com/apprunner/latest/dg/what-is-apprunner.html). The maintenance-mode announcement came 2026-03-31, the cut-off for new customers was 2026-04-30, and no new features are planned — [Encore analysis](https://encore.dev/articles/end-of-app-runner). Encore reads "no new customers" as the usual start of a gradual sunset; that is Encore's opinion, not an AWS statement — [Encore](https://encore.dev/articles/end-of-app-runner).
- **ECS Express Mode basics:** Express Mode needs only a container image, a task execution role and an infrastructure role. It provisions a Fargate service, an ALB with TLS, auto-scaling, monitoring and networking. It is aimed at stateless HTTP web apps and APIs — [AWS ECS docs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-overview.md).
- **ECS Express Mode cost and ALB sharing:** "There is no additional charge" for Express Mode; you pay for Fargate, the ALB, CloudWatch and data transfer — [AWS ECS docs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-overview.md). The ALB is shared across up to 25 services via host-header rules. Express Mode launched 21 Nov 2025 in all regions — [AWS News Blog](https://aws.amazon.com/blogs/aws/build-production-ready-applications-without-infrastructure-complexity-using-amazon-ecs-express-mode); [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/11/announcing-amazon-ecs-express-mode/). A third-party test found that ALB sharing depends on the networking configuration — [Classmethod](https://dev.classmethod.jp/articles/ecs-express-mode-alb-creation-timing/).
- **ECS Express Mode and background workers:** The launch post covers HTTP services with a container port and health-check path. It does not cover non-HTTP background workers such as an arq worker — [AWS News Blog](https://aws.amazon.com/blogs/aws/build-production-ready-applications-without-infrastructure-complexity-using-amazon-ecs-express-mode).
- **Seoul Fargate and ALB prices:**
  - Fargate ARM: $0.03725 per vCPU-hour and $0.00409 per GB-hour. Fargate x86: $0.04656 per vCPU-hour and $0.00511 per GB-hour — [AWS price list, ECS/Fargate](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ecs/USD/current/ecs.json).
  - ALB: $0.0225 per hour plus $0.008 per LCU-hour — [AWS price list, ELB](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/elb/USD/current/elb.json).
  - In-use public IPv4: $0.005 per hour — [AWS price list, VPC](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/vpc/USD/current/vpc.json).
- **Seoul EC2 on-demand prices (Linux):**
  - t4g.small (2 vCPU, 2 GiB): $0.0208/h, about $15.18 per 730 h.
  - t4g.medium (4 GiB): $0.0416/h, about $30.37.
  - t4g.micro (1 GiB): $0.0104/h, about $7.59.
  - t3.small: $0.026/h, about $18.98.
  - t3a.small: $0.0234/h, about $17.08.
  - m7g.medium (1 vCPU, 4 GiB, non-burstable): $0.0502/h, about $36.65.
  - Source: [AWS price list, EC2 Seoul Linux](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Seoul)/Linux/index.json).
- **Lightsail (Linux, public IPv4 included):** $12/mo for 2 GB RAM, 2 vCPU, 60 GB SSD and 3 TB transfer. $24/mo for 4 GB RAM, 80 GB SSD and 4 TB transfer. IPv6-only bundles are $10 (2 GB) and $20 (4 GB). The regions with half transfer allowance are Mumbai, Sydney, Jakarta, Malaysia, Hong Kong and São Paulo; Seoul is not on that list. Lightsail containers start at $10 (Micro: 0.25 vCPU, 1 GB). The Lightsail load balancer is $18/mo — [AWS Lightsail pricing](https://aws.amazon.com/lightsail/pricing/).
- **Lightsail pricing dispute:** Third-party 2026 guides agree on $12 for 2 GB but disagree on IPv6-only and IPv4-premium figures — [Cloudburn](https://cloudburn.io/blog/amazon-lightsail-pricing); [Kuberns](https://kuberns.com/blogs/aws-lightsail-pricing-your-comprehensive-guide/); [Toolradar](https://toolradar.com/tools/amazon-lightsail). An undated AWS re:Post answer says IPv4 is being folded into bundle prices — [AWS re:Post](https://repost.aws/questions/QUT9M2DAKiQTSkOXZnaYYR0g/does-lightsail-charge-extra-ip-fees).
- **Elastic Beanstalk:** Beanstalk still offers Docker platform branches, including an ECS-managed Docker branch — [AWS Elastic Beanstalk docs](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker.html).
- **Fly.io:** Fly.io has no Seoul region; its Asia-Pacific regions are nrt (Tokyo), sin (Singapore) and syd (Sydney) — [Fly.io regions](https://docs.fly.io/reference/regions). Prices per 30 days in iad: shared-cpu-1x/1 GB $6.70, shared-cpu-2x/2 GB $13.39. The Singapore example costs about 1.27× iad. There is no free allowance for new orgs, Managed Postgres starts at $38/mo, and a dedicated IPv4 is $2/mo — [Fly.io pricing](https://docs.fly.io/about/pricing).
- **Render:** Render's regions are Oregon, Ohio, Virginia, Frankfurt and Singapore, with none in Korea or Japan — [Render regions](https://render.com/docs/regions).
- **Railway:** Railway's only Asian region is Singapore — [Railway regions](https://docs.railway.com/reference/deployment-regions).
- **App Runner alternatives:** Encore lists ECS Express Mode, Encore, and Render/Fly.io/Railway as the post-App Runner alternatives. Moving to the latter three means moving off AWS — [Encore](https://encore.dev/articles/end-of-app-runner).
- **Kamal:** Kamal (v2.12.0) is a single-VM, Compose-like alternative. It deploys containers to bare servers or cheap VMs with zero-downtime deploys and rolling restarts. It needs SSH-key access to the servers — [Kamal](https://kamal-deploy.org/). A Korean GeekNews post links Kamal Proxy as an alternative to docker-rollout for zero-downtime deploys — [GeekNews](https://news.hada.io/topic?id=8445).

### Inferences
- **Monthly cost after the trial (Seoul, 730 h):**
  - EC2 t4g.small: $15.18 + public IPv4 $3.65 + 30 GB gp3 $2.74 + roughly 10 GB of incremental snapshots $0.50 ≈ **$22/mo**.
  - EC2 t4g.medium: ≈ **$37/mo**.
  - Lightsail 2 GB: **$12**. Lightsail 4 GB: **$24**.
- **ECS Express Mode estimate (Seoul):**
  - Assumed task sizes, which Express Mode does not prescribe in the fetched docs: Next.js 0.5 vCPU/1 GB, FastAPI 0.5 vCPU/1 GB, arq 0.25 vCPU/0.5 GB, Redis 0.25 vCPU/0.5 GB.
  - Monthly cost by part:

    | Part | Monthly cost |
    |---|---|
    | Fargate ARM tasks: 16.58 + 16.58 + 8.29 + 8.29 | ≈ $49.7 |
    | ALB base hours | $16.4 |
    | At least 1 LCU | about $5.8 |
    | ALB public IPv4 in 2 AZs | $7.3 |
    | Task public IPs (instead of a NAT gateway) | $14.6 |
    | **Total** | **≈ $90–95/mo** |

  - That is roughly 4× the EC2 t4g.small option and roughly 2.5× t4g.medium.
- **Off-AWS platforms:** Fly.io, Render and Railway would put the app servers in Tokyo or Singapore while RDS sits in Seoul. Every SSR request and API call would then pay cross-region round trips and data-transfer charges. They are a poor fit once "RDS in Seoul" is fixed.
- **Lightsail as a cheaper variant:** A Lightsail 4 GB box at $24 costs less than t4g.medium at about $37 all-in and solves the RAM concern in section 2. Lightsail sits outside the normal VPC, though. Before switching, the team would need to verify RDS connectivity (VPC peering), IAM role support and SSM integration; none of these were checked here.
- **Overall:** EC2 + Compose remains the best fit for "simple, cheap, Seoul, already on AWS". ECS Express Mode is the natural upgrade path if the team later wants managed rolling deploys and autoscaling. Keeping images 12-factor (config from env/SSM, no state in containers) keeps that migration cheap.

### Gaps
- No 2025–2026 HN, Reddit or Korean velog/tistory threads were collected because the search budget was exhausted. Practitioner sentiment here rests on the 2026 proxy-comparison post (section 6) and the Kamal/docker-rollout sources.
- ECS Express Mode default task CPU/memory, minimum task count and support for non-HTTP worker services were not found in the fetched pages.
- Not verified: whether Elastic Beanstalk's AL2023 Docker platform supports Compose files with single-instance (no-ALB) environments on Graviton. Lightsail's support for IAM instance roles, SSM and RDS peering was also not verified.

---

## 2. Is t4g.small (2 GiB) enough for Caddy + Next.js 16 standalone + FastAPI (2 uvicorn workers, Pillow) + arq worker + Redis? (memory, swap, EBS, CPU credits)

### Takeaway
It is borderline. The steady-state sum fits, but there is little headroom. A 20 MB photo decode, two overlapping Next.js or FastAPI copies during a zero-downtime deploy, or a Redis fork can push it into the OOM killer, and Docker does not protect container processes from OOM. Two options:
- Stay on t4g.small with hard per-container memory limits, a 2 GB swap file, serialized image processing and stop-then-start deploys.
- Or plan for t4g.medium (4 GiB, about +$15/mo after the trial, $0.0416/h in Seoul).

CPU credits are unlikely to matter at this load, but add a billing alarm.

### Cited Findings
- **t4g specs:** t4g.small has 2 vCPU and 2 GiB, a 20% baseline per vCPU and earns 24 CPU credits per hour. t4g.medium has 4 GiB with the same baseline and credits. t4g.micro has 1 GiB, a 10% baseline and earns 12 credits per hour — [AWS EC2 T4g page](https://aws.amazon.com/ec2/instance-types/t4/).
- **Unlimited mode and surplus charges:** T4g launches in Unlimited mode by default. If average CPU over a rolling 24 h stays above baseline, surplus credits are billed at a flat per-vCPU-hour rate. They are also charged when the instance is stopped or switched to standard mode. Track this with the CloudWatch metrics `CPUSurplusCreditBalance` and `CPUSurplusCreditsCharged` — [AWS EC2 docs: unlimited mode](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances-unlimited-mode-concepts.html).
- **Surplus credit rate:** $0.04 per vCPU-hour — [AWS EC2 T4g page](https://aws.amazon.com/ec2/instance-types/t4/) (region not stated); the same figure appears in a 2023 Vantage analysis — [Vantage, Nov 2023](https://vantage.sh/blog/m7i-flex-vs-t-series-cost).
- **Breakeven vs fixed-performance instances:** A t3.large breaks even with an m5.large at 42.5% average CPU (us-east-1 example) — [AWS EC2 docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances-unlimited-mode-concepts.html). Vantage puts the T4g vs M7i-Flex breakeven at 66% average CPU. That analysis is from 2023 — [Vantage](https://vantage.sh/blog/m7i-flex-vs-t-series-cost).
- **Next.js runtime memory:**
  - Next.js preloads each page's JavaScript modules into memory when the server starts and never unloads them; `experimental.preloadEntriesOnStart: false` defers this. Build memory is the more common problem (webpack memory options, TypeScript checking) — [Next.js memory guide, updated 2026-04-28](https://nextjs.org/docs/app/guides/memory-usage).
  - The default Next.js cache stores generated assets in memory (default 50 MB) and on disk — [Next.js self-hosting guide, updated 2026-10-15](https://nextjs.org/docs/app/guides/self-hosting).
  - The only measured runtime figure found is one app's anecdote: about 300 MB dropping to about 200 MB after switching to standalone — [ibl.ai](https://ibl.ai/developer/os/standalone-deployment).
  - A Railway user reports RAM staying high after deploy — [Railway Station](https://station.railway.com/questions/memory-usage-and-disk-space-15c5e366).
- **sharp (used by `next/image`):** On glibc Linux, Next.js image optimization may need allocator configuration to avoid excessive memory — [Next.js self-hosting](https://nextjs.org/docs/app/guides/self-hosting). sharp says the glibc allocator "is unsuitable for long-running, multi-threaded processes" and recommends jemalloc. musl/Alpine is unaffected — [sharp install docs](https://sharp.pixelplumbing.com/install).
- **Node heap sizing:** Node docs say the default V8 heap limit is "based on your system's available memory". Set `--max-old-space-size` below the container limit and watch RSS — [Node.js memory guide](https://nodejs.org/en/learn/diagnostics/memory/understanding-and-tuning-memory).
- **FastAPI/uvicorn memory:**
  - 2023 GitHub report: about 125 MB per worker on Pydantic v1, about 1.2 GB for 2 workers on Pydantic 2.0.2, and about 440 MB for 2 workers on 2.0.3 — [pydantic#6620 (2023)](https://github.com/pydantic/pydantic/issues/6620).
  - The FastAPI docs say that with multiple processes per container "you will have to make sure that the number of processes started doesn't consume more memory than what is available" — [FastAPI Docker docs](https://fastapi.tiangolo.com/deployment/docker/).
- **arq worker defaults:** `max_jobs=10` concurrent jobs, `job_timeout=300 s`, `max_tries=5`, `job_completion_wait=0`. The current version is v0.28.0 (2026-04-16) — [arq docs](https://arq-docs.helpmanual.io/).
- **Redis memory and kernel settings:**
  - Set `vm.overcommit_memory = 1` and disable Transparent Huge Pages.
  - Set an explicit `maxmemory`.
  - Saving an RDB or rewriting the AOF can use up to 2× normal memory under writes.
  - Enable swap equal to RAM so an OOM shows up as latency instead of a kill.
  - Source: [Redis admin docs](https://redis.io/docs/latest/operate/oss_and_stack/management/admin/).
- **Docker OOM behavior:** "Any process is subject to killing, including Docker". Docker lowers the daemon's OOM priority, but "The OOM priority on containers isn't adjusted" — [Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/).
- **Compose memory limits:** `mem_limit` and `memswap_limit` are per-service settings. Setting `memswap_limit` equal to `memory` disables swap for that container; leaving it unset allows swap equal to `memory` when the host has swap — [Compose services reference](https://docs.docker.com/reference/compose-file/services/).
- **Compose resource limits in practice:** A 2026 production write-up warns that `deploy.resources` was historically Swarm-oriented and that limits must be verified on plain `docker compose` — [EastonDev, 2026-04](https://eastondev.com/blog/en/posts/dev/20260424-docker-compose-production/). The Compose deploy spec itself only says "the platform must prevent the container from allocating more resources" — [Compose deploy spec](https://docs.docker.com/reference/compose-file/deploy/).
- **Swap guidance:**
  - AWS's swap-file Knowledge Center article covers creating a swap file with dd/mkswap/fstab. It says swap is "not a replacement for more RAM" and that AWS's best practice is swap on instance store, which T4g does not have. A commenter reported `swapon failed: Invalid argument` on AL2 and AL2023 in April 2025 — [AWS re:Post Knowledge Center](https://repost.aws/knowledge-center/ec2-memory-swap-file).
  - A November 2024 Japanese walkthrough covers creating a 1 GB swap file on AL2023 — [Classmethod (2024)](https://dev.classmethod.jp/articles/how-to-create-swap-memory-in-linux-on-ec2-jp/).
- **Seoul EBS prices:** gp3 $0.0912/GB-month (gp2 $0.114), extra gp3 IOPS $0.0057/IOPS-month, extra throughput $46.69/GiBps-month, snapshots $0.05/GB-month — [AWS price list, EBS](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ebs.json). gp3 includes a 3,000 IOPS / 125 MB/s baseline (us-east-1 sources) — [Wring EBS guide](https://wring.co/blog/aws-ebs-pricing-guide).
- **Pillow decompression bombs:** Pillow warns when an image exceeds `Image.MAX_IMAGE_PIXELS` and raises `DecompressionBombError` above 2× that limit. `Image.draft()` can load a JPEG at reduced size or mode — [Pillow Image docs](https://pillow.readthedocs.io/en/stable/reference/Image.html).

### Inferences
- **Approximate memory budget on 2 GiB (~1.9 GiB usable).** Ranges are my estimates; the figures that have sources are cited in the findings above.

  | Component | Estimate |
  |---|---|
  | AL2023 + dockerd/containerd + SSM agent + CloudWatch agent | ~300–400 MB |
  | Caddy | ~30–60 MB |
  | Next.js standalone | ~150–300 MB |
  | FastAPI with 2 workers | ~250–450 MB |
  | arq worker (same image, imports the app) | ~150–250 MB |
  | Redis with tiny datasets | ~10–30 MB |
  | **Steady state** | **≈ 0.9–1.5 GB** |

- **Spikes on top of the steady state:**
  - Decoding a 20 MB phone JPEG of about 12–48 MP needs roughly 36–144 MB of raw RGB, plus copies for transpose/re-encode.
  - A HEIC decode via pillow-heif is similar.
  - Two concurrent uploads can add 300–600 MB.
  - A blue/green deploy temporarily doubles Next.js and FastAPI, adding about 400–750 MB.
  - Conclusion: t4g.small is workable only if spikes are controlled.
- **Recommendations if staying on t4g.small:**
  1. Set `mem_limit` per service, for example Caddy 128m, Next.js 512m, FastAPI 640m, arq 384m, Redis 128m. That way one runaway container is OOM-killed and restarted instead of the kernel killing a random process.
  2. Set `NODE_OPTIONS=--max-old-space-size≈384` for Next.js.
  3. Add a 2 GB swap file on the gp3 root volume as a safety net, with low `vm.swappiness` (about 10).
  4. Strip EXIF/GPS without a full decode where possible. Otherwise cap concurrent Pillow work with a semaphore, or move it to the arq worker with `max_jobs` at 1–2. Lower `MAX_IMAGE_PIXELS` to match the real photo size.
  5. Run Next.js image optimization with jemalloc or `unoptimized`, or use an Alpine base image.
  6. Use stop-then-start deploys (section 5) rather than double-running containers.
- **When to move to t4g.medium:** If measured `docker stats` peaks exceed about 1.6 GB, move to t4g.medium. The extra $15.19/mo is cheaper than debugging OOMs in a demo. On-demand pricing applies after 2026-12-31 either way, since the free trial covers only t4g.small.
- **CPU credits:** The workload is mostly I/O-bound (LLM and HTTP calls, DB). The 20%-per-vCPU baseline (0.4 vCPU sustained) should cover it. Worst case, both vCPUs pegged for a full month: surplus is 1.6 vCPU-h per hour × $0.04 ≈ $0.064/h ≈ $47/mo. Add a CloudWatch alarm on `CPUSurplusCreditsCharged > 0` or a monthly AWS Budget. Alternatively, set credit specification to `standard`, which throttles instead of billing; this is acceptable for a demo but hurts SSR latency during bursts.
- **EBS:** A 30 GB gp3 root at default 3,000 IOPS / 125 MB/s is enough: OS, Docker images (keep 2–3 tags), swap, `.next/cache`, Caddy `/data` and logs. It costs about $2.74/mo in Seoul. Prune old images after each deploy so the disk does not fill up.

### Gaps
- No credible 2025–2026 measured RSS figures were found for a Next.js 16 standalone server, a Python 3.12 FastAPI worker or an arq worker. The numbers above are anecdotes or estimates, and the team should measure with `docker stats` under a short load test.
- The Pillow `MAX_IMAGE_PIXELS` default value was not shown in the fetched part of the Pillow docs; it is commonly about 89.5 MP, but this was not verified here.
- The T4g surplus-credit rate for Seoul specifically was not confirmed; the $0.04 figure comes from the global T4g page.

---

## 3. t4g.small free-trial terms (to 2026-12-31?) and post-trial Seoul pricing; public IPv4 / Elastic IP charges

### Takeaway
The t4g.small free trial is confirmed through 2026-12-31 and covers Seoul. It gives 750 h/month aggregated across regions, one trial per payer account, and covers instance hours only. EBS, public IPv4 and surplus CPU credits are billed. From 2027-01-01, t4g.small costs $0.0208/h (about $15.18/mo) in Seoul. Budget about $3.65/mo for one public IPv4 or Elastic IP, and about $2–3/mo for gp3.

### Cited Findings
- **Trial terms:**
  - The trial gives 750 free hours per month for t4g.small "until December 31, 2026".
  - Hours are "calculated in aggregate across all Regions".
  - From 2027-01-01, usage moves to On-Demand rates, or to any Reserved Instance or Savings Plan the customer holds.
  - "Customers must pay for surplus CPU credits".
  - Organizations get one trial per payer account.
  - Asia Pacific (Seoul) is one of the 18 eligible regions.
  - Source: [AWS EC2 FAQ](https://aws.amazon.com/ec2/faqs/).
- **T4g page:** The T4g page repeats "750 hours / month until Dec 31st 2026" and that surplus usage costs $0.04/vCPU-hour — [AWS T4g page](https://aws.amazon.com/ec2/instance-types/t4/).
- **Billing verification (Tokyo):** Classmethod checked CUR billing data and confirmed $0 instance cost in January 2026, even though the line-item text still said "ending Dec 31 2025". EBS gp3 25 GB was about $2.40/mo and public IPv4 about $3.75/mo, about 60% of the remaining bill. Their estimated total was about $6.15/mo during the trial and about $18.75/mo after (Tokyo prices). The 750 h is shared across an AWS Organization — [Classmethod, Jan 2026](https://dev.classmethod.jp/en/articles/ec2-t4g-small-free-tier-2026/).
- **Region-specific campaigns:** An AWS China page lists a different end date (2026-07-31) for the China regions — [AWS China](https://amazonaws.cn/en/new/2025/announcing-amazon-ec2-t4g-free-trial).
- **Post-trial Seoul prices:**
  - t4g.small: $0.0208/h.
  - Spot and 1-year Reserved prices for t4g.small appear on a third-party tracker, but the page does not state the region — [Vantage instances](https://instances.vantage.sh/aws/ec2/t4g.small).
  - Seoul on-demand: [AWS price list, EC2 Seoul](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Seoul)/Linux/index.json).
- **Public IPv4 charge:** $0.005 per IP-hour for all public IPv4 addresses, in use or idle, including Elastic IPs and Amazon-provided addresses, effective 2024-02-01 — [AWS News Blog](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights). Seoul's price list shows the same $0.005/h for in-use and idle public IPv4 — [AWS price list, VPC](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/vpc/USD/current/vpc.json).
- **Public IPv4 under the legacy free tier:** The legacy free tier included 750 h/month of public IPv4 for the first 12 months (2024 announcement) — [AWS What's New, Feb 2024](https://aws.amazon.com/about-aws/whats-new/2024/02/aws-free-tier-750-hours-free-public-ipv4-addresses/).
- **New-account Free Tier model:** New accounts get a Free plan (up to $200 in credits: $100 on sign-up plus up to $100 earned) or a Paid plan. A Free-plan account "closes on its own 6 months after you open it" or when credits run out, unless converted to Paid — [AWS Free Tier](https://aws.amazon.com/free/).

### Inferences
- **Monthly cost timeline (Seoul):**

  | Period | Instance | Other charges | Total |
  |---|---|---|---|
  | Now to 2026-12-31 | $0 | IPv4 $3.65 + 30 GB gp3 $2.74 + small snapshots | ≈ **$7/mo** |
  | From 2027-01 (t4g.small) | $15.18 | same | ≈ **$22/mo** |
  | From 2027-01 (t4g.medium) | $30.37 | same | ≈ **$37/mo** |

  A 1-year Savings Plan or Reserved Instance would cut the instance line by roughly a third, but it is probably not worth it for a bootcamp project.
- **Elastic IP:** One EIP attached costs the same $0.005/h as an auto-assigned public IPv4. Use the EIP: the public IP then survives stop/start and retirement (section 7), and the Route 53 A record stays valid.
- **Account type:** If the team's account was created on the 2025+ Free plan, it auto-closes after 6 months. Confirm the account is on the Paid plan, or that someone's payer account is, before relying on it for a launch. Also check whether a Free-plan account gets the t4g trial; the FAQ does not say.

### Gaps
- The FAQ does not say whether accounts on the new 2025 "Free plan" (credits model) are eligible for the t4g.small trial, or whether trial hours draw down credits.
- No official Seoul figure was found for 1-year Reserved or Savings Plan rates for t4g.small.

---

## 4. arm64 (Graviton) container images: compatibility for Pillow, pillow-heif, argon2-cffi, asyncpg, and Node/Next.js

### Takeaway
There are no blockers. As of October 2026 every compiled dependency in the stack ships manylinux aarch64 wheels for CPython 3.12, and sharp ships linux-arm64 prebuilt binaries. The real risk is build speed: QEMU-emulated arm64 builds on x86 runners are slow. Build natively on GitHub's `ubuntu-24.04-arm` runners, or a multi-arch buildx with an arm64 runner.

### Cited Findings
- **PyPI aarch64 wheels (checked 2026-10-29 via the PyPI JSON API):**

  | Package | Version | aarch64 wheel |
  |---|---|---|
  | Pillow | 13.0.0, 2026-10-16 | `cp312-manylinux_2_27/2_28_aarch64` and musllinux — [PyPI Pillow](https://pypi.org/project/pillow/) |
  | pillow-heif | 1.8.1, 2026-10-11 | `cp312-manylinux_2_26/2_28_aarch64` — [PyPI pillow-heif](https://pypi.org/project/pillow-heif/) |
  | argon2-cffi-bindings | 26.1.0 | `cp310-abi3-manylinux_2_26/2_28_aarch64` — [PyPI argon2-cffi-bindings](https://pypi.org/project/argon2-cffi-bindings/) |
  | argon2-cffi | 25.1.0 | pure Python, `py3-none-any` — [PyPI argon2-cffi](https://pypi.org/project/argon2-cffi/) |
  | asyncpg | 0.32.0, 2026-10-06 | `cp312-manylinux_2_28_aarch64` — [PyPI asyncpg](https://pypi.org/project/asyncpg/) |
  | uvloop | 0.23.0 | aarch64 wheel — [PyPI uvloop](https://pypi.org/project/uvloop/) |
  | httptools | 0.9.0 | aarch64 wheel — [PyPI httptools](https://pypi.org/project/httptools/) |
  | pydantic-core | 2.50.1 | aarch64 wheel — [PyPI pydantic-core](https://pypi.org/project/pydantic-core/) |
  | psycopg-binary | 3.3.6 | aarch64 wheel — [PyPI psycopg-binary](https://pypi.org/project/psycopg-binary/) |
  | cryptography | 50.0.2 | abi3 aarch64 wheel — [PyPI cryptography](https://pypi.org/project/cryptography/) |
  | orjson | 3.13.0 | aarch64 wheel — [PyPI orjson](https://pypi.org/project/orjson/) |
  | arq | 0.28.0 | pure Python — [PyPI arq](https://pypi.org/project/arq/) |
  | redis-py | 8.1.0 | pure Python — [PyPI redis](https://pypi.org/project/redis/) |

- **AWS Graviton Python guide:**
  - pip ≥ 20.3 is needed for `manylinux_x_y` tags.
  - When no wheel exists, pip builds from source, which "can take up to 20 minutes".
  - `manylinux_2_28` wheels will not install on Amazon Linux 2 (glibc 2.26).
  - Use at least Python 3.11.
  - AWS runs a nightly arm64 wheel tester covering 200+ packages.
  - Source: [AWS Graviton getting-started, Python](https://github.com/aws/aws-graviton-getting-started/blob/main/python.md).
- **sharp:** sharp prebuilt binaries cover "Linux ARM64 (glibc >= 2.28, musl >= 1.2.5)" — [sharp install docs](https://sharp.pixelplumbing.com/install).
- **Next.js standalone image contents:** standalone output does not copy `public/` or `.next/static`; copy them manually, or let a CDN serve them. Native assets such as `node_modules/sharp` may need `outputFileTracingIncludes` — [Next.js output docs](https://nextjs.org/docs/app/api-reference/config/next-config-js/output).
- **Caddy image:** The official Caddy image is multi-arch, including arm64v8. The current tags are `2.11.7`, `2.11`, `2` and `latest` — [Docker Hub Caddy](https://hub.docker.com/_/caddy).
- **GitHub-hosted arm64 runners:** Labels are `ubuntu-24.04-arm`, `ubuntu-22.04-arm` and `ubuntu-26.04-arm`. They are free and unlimited for public repos (4 vCPU / 16 GB). For private repos they are 2 vCPU / 8 GB and use the account's included minutes, then per-minute rates — [GitHub Docs](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).

### Inferences
- **Base image:** Use `python:3.12-slim` (Debian, glibc ≥ 2.36), which satisfies every `manylinux_2_28` wheel. Avoid Alpine for the Python image: musllinux wheels exist, but slim/glibc is the well-trodden path. For Next.js, either Alpine (avoids the sharp/glibc fragmentation issue) or slim plus jemalloc works.
- **Builds:** Build on `ubuntu-24.04-arm` and push arm64-only images to ECR. QEMU multi-arch builds of Next.js are often several times slower and can time out. Pin `--platform=linux/arm64` in the Dockerfile and compose file, so a developer's x86 laptop does not accidentally push amd64.
- **Local development on x86 Windows laptops:** Run the amd64 variant locally (build both arches, or build locally per-arch). Do not run arm64 images under emulation day to day.

### Gaps
- Node's official `node:*` images and Redis 8 images on arm64 were not checked directly in this session; they are widely multi-arch, but this was not verified here.
- Per-minute pricing for private-repo arm64 runners was not captured.

---

## 5. Zero- or low-downtime deploys on a single host with Compose, and Compose production practices

### Takeaway
Plain `docker compose pull && docker compose up -d` stops each changed container before its replacement starts, so each changed service is down for a few seconds. On a single small host, the pragmatic choice is to accept a few seconds of blip and mask it:
- Caddy `lb_try_duration` holds requests while upstreams restart.
- Healthchecks plus `docker compose up -d --wait` make the deploy script fail loudly.
- Graceful shutdown with a longer `stop_grace_period` lets in-flight work finish.

Real zero downtime, using docker-rollout scaling to two copies or Kamal, is possible. It doubles memory during the deploy, though (section 2), and docker-rollout documents only Traefik/nginx-proxy, not Caddy.

### Cited Findings
- **docker-rollout:**
  - It is a drop-in for `docker compose up -d <service>`: it scales the service to 2×, waits for the new container's healthcheck (`--timeout` default 60 s), waits `--wait-after-healthy` (default 3 s), then removes the old container.
  - It requires a proxy "like Traefik or nginx-proxy". The service must not define `container_name` or `ports`.
  - Without draining, in-flight requests may be lost. The recommended drain is a `--pre-stop-hook` that touches a file to fail the healthcheck, then sleeps longer than interval×retries plus request time; the docs' example is 35 s.
  - Source: [docker-rollout README](https://github.com/Wowu/docker-rollout).
  - The Korean GeekNews summary notes it supports only single-instance services — [GeekNews](https://news.hada.io/topic?id=8445).
  - Hands-on reviews flag the same caveats — [VirtualizationHowTo, 2025-06](https://www.virtualizationhowto.com/2025/06/docker-rollout-zero-downtime-deployments-for-docker-compose-made-simple/); [LinuxTLDR](https://linuxtldr.com/installing-docker-rollout/); [supun.io](https://supun.io/zero-downtime-deployments-docker-compose).
- **Caddy retries during restarts:**
  - `lb_try_duration` (default 0, meaning off; the docs suggest starting around 5 s) makes Caddy keep retrying upstreams for that long, so retries can "hold requests until a healthy upstream can be selected" during redeploys.
  - `lb_try_interval` defaults to 250 ms.
  - By default only GET requests are retried, but connection failures are always retried. `lb_retry_match` was added in 2.11.3.
  - Active health checks (`health_uri`, interval 30 s) do not run for dynamic upstreams.
  - Passive checks (`fail_duration`) are off by default.
  - Default `dial_timeout` is 3 s.
  - Source: [Caddy reverse_proxy docs](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy); [Caddy releases](https://github.com/caddyserver/caddy/releases).
- **`docker compose up` flags:** `--wait` means "Wait for services to be running|healthy. Implies detached mode." `--wait-timeout` caps the wait. `--pull always|missing|never`, `--remove-orphans` and `--force-recreate` are also available — [docker compose up reference](https://docs.docker.com/reference/cli/docker/compose/up/).
- **Compose service attributes:**
  - `healthcheck` supports `interval`, `timeout`, `retries`, `start_period` and `start_interval`.
  - `depends_on` with `condition: service_healthy` waits for the dependency's healthcheck, and `restart: true` restarts the dependent service when the dependency is updated (Compose 2.17+).
  - `restart` options are `no` (the default), `always`, `on-failure` and `unless-stopped`.
  - `stop_grace_period` defaults to 10 s before SIGKILL.
  - `init: true` forwards signals and reaps zombies.
  - `read_only` and `pids_limit` are also available.
  - Source: [Compose services reference](https://docs.docker.com/reference/compose-file/services/).
- **Docker logging:** The default `json-file` driver does no log rotation. Docker recommends the `local` driver, which rotates by default. `daemon.json` `log-opts` (`max-size`, `max-file`) apply only to newly created containers — [Docker logging docs](https://docs.docker.com/engine/logging/configure/).
- **Next.js graceful shutdown:** Next.js finishes in-flight requests and pending `after()` callbacks on SIGINT/SIGTERM; a 10–30 s drain is recommended — [Next.js self-hosting](https://nextjs.org/docs/app/guides/self-hosting).
- **Next.js rolling deploys:** Rolling or overlapping deploys can cause version skew: missing assets, Server Function mismatches and navigation failures. Setting `deploymentId` makes Next.js do a hard reload on mismatch. All instances need the same `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` — [Next.js self-hosting](https://nextjs.org/docs/app/guides/self-hosting).
- **FastAPI graceful shutdown:** Use the exec-form `CMD` so FastAPI/uvicorn shuts down gracefully and runs lifespan events. For a single server with Docker Compose, running one container with `--workers` is acceptable. Add `--proxy-headers` behind a TLS-terminating proxy — [FastAPI Docker docs](https://fastapi.tiangolo.com/deployment/docker/).
- **arq shutdown:** arq handles signals by default (`handle_signals=True`), but `job_completion_wait` defaults to 0, so in-flight jobs are cancelled almost immediately on shutdown. `max_tries=5` retries — [arq docs](https://arq-docs.helpmanual.io/).
- **Kamal:** Kamal offers zero-downtime deploys and rolling restarts to plain VMs, but it is SSH-based — [Kamal](https://kamal-deploy.org/).
- **Compose in production (2026 write-up):** Healthchecks, restart policies and resource limits are what make Compose hold up in production — [EastonDev 2026](https://eastondev.com/blog/en/posts/dev/20260424-docker-compose-production/).

### Inferences
- **Recommended deploy for 믿집 (SSM Run Command script):**
  1. `aws ecr get-login-password | docker login`
  2. Write the new immutable image tags (git SHA, never `latest`) into `.env`.
  3. `docker compose pull`
  4. `docker compose up -d --wait --wait-timeout 120 --remove-orphans`
  5. On non-zero exit, restore the previous tags and run `up -d --wait` again (automatic rollback).
  6. `docker image prune -f --filter "until=168h"`
  7. A smoke `curl` to `/api/healthz` and `/` through Caddy.
- **Caddy settings for this deploy style:** `lb_try_duration 10s` plus `lb_try_interval 250ms` on both upstreams. Expected user impact is a few seconds of slower responses rather than 502s for GETs. A POST that hits during the gap is retried only if the TCP connect failed; the frontend should retry idempotent writes or show a toast.
- **Graceful shutdown settings:** `stop_grace_period: 30s` for Next.js and FastAPI. For arq, use `stop_grace_period: 120s` and set `job_completion_wait` to about 60–110 s, so LLM jobs finish or are safely retried. Because the Postgres jobs table is the ledger, a cancelled job can be re-enqueued by a startup sweeper.
- **Compose hygiene checklist:**
  - `restart: unless-stopped` on all services.
  - Healthchecks on api (`/api/healthz`), web, redis (`redis-cli ping`) and caddy.
  - `depends_on: condition: service_healthy`.
  - `init: true`.
  - `logging: driver: local` (or `json-file` with `max-size: 10m`, `max-file: 3`), set in `daemon.json` before the first containers are created.
  - `mem_limit` per service.
  - Do not publish Redis, api or web ports on the host; only Caddy's 80/443 (plus 443/udp for HTTP/3).
  - Immutable image tags.
  - A `docker compose config` lint in CI.
- **True zero downtime is optional:** Use docker-rollout for `web` and `api` only if the demo really needs it, and only on t4g.medium (memory). With Caddy, either use upstream service-name DNS (Docker's embedded DNS returns both containers' IPs while scaled), or a `dynamic a` upstream with a short `refresh`. Test this; it is not documented by docker-rollout. Set Next.js `deploymentId` if old and new copies overlap.

### Gaps
- No Caddy-specific documentation or forum thread was retrieved showing docker-rollout and Caddy upstream DNS behavior with scaled Compose services.
- Exact downtime numbers for `compose up` recreate on t4g.small were not found; measure them in staging.

---

## 6. Caddy vs Nginx vs Traefik in production in 2026 (Caddy 2.11 changes, certificate storage, rate limiting, security headers)

### Takeaway
Caddy is the right proxy for a small single host in 2026. It gives automatic HTTPS (Let's Encrypt with ZeroSSL fallback), HTTP/3 and a two-line config. Traefik's advantage, Docker-label discovery, matters little with a fixed set of services, and Nginx needs certbot. Update the plan from "Caddy 2.10" to 2.11.7, the current stable release (2026-10-03). 2.11.x fixed multiple CVEs and 2.11.6 changed defaults. Persist `/data`. Rate limiting needs a third-party plugin, so keep app-level limits in FastAPI/Redis as planned.

### Cited Findings
- **2026 comparison (May 2026):**
  - Caddy 2.11: automatic HTTPS by default, ECH key rotation, HTTP/3, about 30k+ req/s on commodity hardware.
  - Nginx 1.30/1.31: highest throughput and lowest memory, but no built-in ACME.
  - Traefik 3.7.1: Docker/K8s provider model, about 30% slower than Nginx and more memory.
  - Recommendation: "Small single-host setups or homelabs: Caddy". Outside Docker/K8s dynamism, Traefik "misses its main advantages".
  - The community ingress-nginx project reached end-of-life in March 2026 (Kubernetes-only relevance).
  - Source: [Falcão, 2026-05-20](https://falcao.org/posts/caddy-nginx-traefik-2026/).
  - Similar 2026 framings: [Dokploy blog](https://dokploy.com/blog/caddy-vs-traefik-vs-nginx); [WZ-IT](https://wz-it.com/en/blog/caddy-traefik-nginx-reverse-proxy-comparison/); [Gupta, Top 5 reverse proxies 2026](https://guptadeepak.com/tools/top-5-reverse-proxies-2026/).
- **Caddy release history:**

  | Version | Date | Changes |
  |---|---|---|
  | v2.10.1 | 22 Aug 2025 | Requires Go 1.25 |
  | v2.10.2 | 23 Aug 2025 | Hotfix |
  | v2.11.1 | 23 Feb 2026 | First 2.11 release: ECH key rotation, time-based log rolling, six CVE fixes (including TLS client-auth failing open and admin cross-origin) |
  | v2.11.2 | Mar 2026 | `forward_auth` and `vars_regexp` security fixes; passive health checks for dynamic upstreams |
  | v2.11.3 | May 2026 | FastCGI and admin API fixes; `lb_retry_match` |
  | v2.11.4 | Jun 2026 | Path-matcher and template fixes; zstd/br preferred over gzip |
  | v2.11.6 | 1 Oct 2026 | Go 1.26 minimum, CVE-2026-52844 and others; breaking changes: request headers capped at 16 KiB, new 1-minute idle read/write timeouts, header fields containing dots dropped, stricter config validation |
  | v2.11.7 | 3 Oct 2026 | Fixes 2.11.6 regressions (an HTTP/2 proxy crash and streams cut after a minute); upgrade advised |

  Source: [Caddy GitHub releases](https://github.com/caddyserver/caddy/releases).
- **Caddy server defaults:**
  - `read_header` 1m. `read_body` and `write` have no timeout. `read_body_idle` and `write_idle` are 1m. `idle` is 5 min.
  - `max_header_size` is 16 KiB (431 response above it).
  - "By default, no proxies are trusted" (`trusted_proxies`).
  - `client_ip_headers` defaults to X-Forwarded-For.
  - Source: [Caddy global options](https://caddyserver.com/docs/caddyfile/options).
- **Certificate storage and issuance:**
  - Caddy stores certificates and keys in the data directory, which must be writable and persistent.
  - Defaults are Let's Encrypt, then ZeroSSL.
  - Ports 80/443 must be reachable.
  - On failure Caddy backs off exponentially, up to 1 day between tries, for 30 days.
  - Source: [Caddy Automatic HTTPS](https://caddyserver.com/docs/automatic-https).
  - The Docker image exposes `/data` and `/config`; "it's very important to persist the data directory" — [Docker Hub Caddy](https://hub.docker.com/_/caddy).
- **Let's Encrypt limits:**
  - 50 new certificates per registered domain per 7 days.
  - 5 per exact identifier set per 7 days, refilling 1 per 34 h, with no overrides.
  - 5 authorization failures per identifier per hour.
  - ARI-coordinated renewals are exempt from all limits.
  - Source: [Let's Encrypt rate limits](https://letsencrypt.org/docs/rate-limits/).
- **Rate limiting:** `caddy-ratelimit` is a non-official plugin that needs a custom build (`xcaddy` or the `:builder` image). It uses a sliding window, keys such as `{remote_host}`, and has an optional distributed mode — [mholt/caddy-ratelimit](https://github.com/mholt/caddy-ratelimit); [Docker Hub Caddy builder](https://hub.docker.com/_/caddy).
- **Body size limit:** `request_body max_size` caps body size (413 when exceeded). Timeouts moved to the `timeouts` directive — [Caddy request_body](https://caddyserver.com/docs/caddyfile/directives/request_body).
- **Request and response buffering:**
  - Request buffering (`request_buffers`) is off by default and "very inefficient" when enabled.
  - `flush_interval` defaults to no periodic flushing. Flushing is forced for `text/event-stream`, and `-1` disables response buffering.
  - Source: [Caddy reverse_proxy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy).
- **Next.js streaming:** Next.js recommends a reverse proxy in front, to handle malformed requests, slow-connection attacks, payload limits and rate limiting. Streaming needs the proxy not to buffer; the nginx example is `X-Accel-Buffering: no` — [Next.js self-hosting](https://nextjs.org/docs/app/guides/self-hosting).

### Inferences
- **Version pin:** Pin `caddy:2.11.7` (or the digest), not "2.10". 2.10.x predates more than ten CVE fixes. Watch for 2.11.6-style breaking defaults on each upgrade; the 16 KiB header cap matters if session cookies grow.
- **Minimal Caddyfile pattern:**
  - Site `mitjip.example` with `encode zstd gzip`.
  - `handle /api/*` → `request_body { max_size 25MB }` then `reverse_proxy api:8000 { lb_try_duration 10s }`.
  - `handle` → `reverse_proxy web:3000 { lb_try_duration 10s; flush_interval -1 }`, to be safe for RSC/streaming.
  - Security headers via the `header` directive: HSTS, `X-Content-Type-Options nosniff`, `Referrer-Policy`, a frame-ancestors CSP, and `-Server`.
  - Set uvicorn `--proxy-headers --forwarded-allow-ips` to the Caddy container's network, so FastAPI sees real client IPs for rate limiting.
- **Certificate volume:** Mount a named volume for `/data` and include it in EBS snapshots. Rebuilding the box repeatedly without `/data` can hit the 5-per-7-days duplicate-certificate limit. Use the LE staging CA (`acme_ca`) while experimenting.
- **Rate limiting placement:** Keep rate limiting in FastAPI+Redis (already planned), which avoids maintaining a custom Caddy build. Add a coarse Caddy or CloudFront/WAF limit only if abuse shows up.

### Gaps
- The Caddy `header` directive docs were not fetched, so security-header syntax is from general knowledge.
- No 2026 benchmark of Caddy memory footprint was found.
- No primary source was found on Caddy's default behavior for streaming responses with unknown Content-Length over HTTP/1.1 upstreams. Test Next.js streaming through Caddy.

---

## 7. EC2 resilience for a single instance (auto-recovery, EBS snapshots/DLM, AMI backups, retirement)

### Takeaway
A single EBS-backed instance recovers on its own from AWS host failures. Simplified automatic recovery is on by default and keeps the instance ID, IPs and EBS volumes. Instance-level failures, hardware retirement, a bad deploy and AZ outages still need action from the team. Add the following and the setup reaches a "minutes to an hour" recovery time at about $1/mo:
- An Elastic IP.
- A DLM default policy for daily EBS-backed AMIs or snapshots, retained 7 days.
- CloudWatch alarms for system and instance status checks.
- A scripted rebuild path (user-data/IaC plus the compose file in S3 or SSM).

### Cited Findings
- **Automatic recovery mechanics:**
  - Two mechanisms exist: simplified automatic recovery (on by default for supported instances, no cost, Health Dashboard notifications) and CloudWatch action-based recovery (manual setup, SNS notifications, faster recovery attempts, may incur CloudWatch charges).
  - Recovery triggers only on a failed **system** status check, not on an instance status check.
  - A recovered instance keeps its instance ID, public, private and Elastic IPs, metadata, EBS volumes and AZ. It loses RAM contents, and uptime resets.
  - If recovery fails, you must stop/start manually, and "a restarted instance receives a new public IPv4 address unless it has an Elastic IP address".
  - AWS recommends ELB plus Auto Scaling for system-level resilience.
  - Source: [AWS EC2 docs: automatic instance recovery](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-recover.html).
  - Recovery does not run during Health Dashboard events, can fail without spare capacity, and has a daily attempt limit; it can be disabled with `modify-instance-maintenance-options` — [AWS docs: simplified automatic recovery](https://docs.amazonaws.cn/en_us/AWSEC2/latest/UserGuide/instance-configuration-recovery.html); [AWS re:Post](https://repost.aws/knowledge-center/ec2-automatic-recovery-status-check).
  - A 2026 tutorial recommends adding a CloudWatch alarm on top of the default — [OneUptime, 2026-02](https://oneuptime.com/blog/post/2026-02-12-set-up-ec2-auto-recovery-for-instance-health/view).
- **Instance retirement:**
  - Retirement is scheduled when the host has an irreparable hardware failure. An EBS-backed instance "is stopped, and you can start it again at any time", and starting it migrates it to new hardware.
  - Email goes to the account's primary and operations contacts. The instance "might already be unreachable", so act early.
  - Before retirement, create an EBS-backed AMI.
  - Source: [AWS EC2 docs: instance retirement](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-retirement.html).
  - A stop can hang on degraded hardware (force stop it), and a start can hit capacity errors — [AWS re:Post](https://repost.aws/knowledge-center/ec2-instance-retirement).
- **DLM default policies:**
  - The EBS-snapshot default policy (VOLUME) and EBS-backed-AMI default policy (INSTANCE) create every 1–7 days (default daily) and retain for 2–14 days (default 7).
  - They target only resources at least 24 h old and skip resources with a recent backup.
  - Each resource gets a random 4-hour window. Policies can copy to up to 3 other regions.
  - "Extend deletion" controls whether the last backup is deleted.
  - Source: [AWS EBS docs: DLM default policies](https://docs.aws.amazon.com/ebs/latest/userguide/default-policies.html); [DLM API](https://docs.aws.amazon.com/dlm/latest/APIReference/API_CreateLifecyclePolicy.html).
- **Snapshot price:** Seoul snapshot storage is $0.05/GB-month — [AWS price list, EBS](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ebs.json).

### Inferences
- **Recommended resilience set (≈ $1–2/mo):**
  1. Attach an Elastic IP.
  2. Enable a DLM default **AMI** policy (daily, retain 7 days). It captures the root volume, including the Caddy `/data` certs, `.env`, Redis AOF if enabled, and the Docker image cache, so a rebuild is "launch from AMI, re-associate EIP".
  3. Add CloudWatch alarms: `StatusCheckFailed_System` → recover action plus SNS email, `StatusCheckFailed_Instance` (3 × 1 min) → reboot action, and `CPUSurplusCreditsCharged`.
  4. Keep the instance stateless enough to rebuild from scratch: compose file and Caddyfile in git, secrets in SSM Parameter Store, images in ECR, data in RDS/S3. Then a user-data script or a `aws ssm send-command` runbook can recreate the host in about 10–15 minutes even if the AMI is lost.
  5. Confirm the AWS account's primary and operations contact emails are monitored, so retirement notices are seen.
- **Redis contents:** Redis data is lost on recovery or reboot because RAM is lost. That is acceptable because the Postgres jobs table is the ledger. On worker start, re-enqueue `pending`/`running` jobs older than N minutes. Rate-limit counters resetting is harmless.
- **What this design cannot survive:** It does not survive an AZ outage or a bad deploy that corrupts the host. That is acceptable for this scale; the image-tag rollback in section 5 covers bad deploys.

### Gaps
- The "Requirements for simplified automatic recovery" page was not fetched, so T4g support is not confirmed from that page (T4g is EBS-only with default tenancy, so it is very likely supported).
- No data was found on how often T-family hosts are retired or fail system checks in Seoul.

---

## 8. What else to add at the compute layer (CloudFront, IPv6-only, Elastic IP, swap, patching, time sync, log limits, monitoring)

### Takeaway
High-value, near-zero-cost additions:
- An Elastic IP.
- A swap file.
- Docker log rotation set before first deploy.
- `mem_limit`s.
- SSM Patch Manager. AL2023 does not apply security updates by itself.
- A DLM backup policy.
- CloudWatch agent memory/disk metrics and alarms.

Two "optional, evaluate" items:
- **CloudFront Free flat-rate plan in front.** It costs $0 and includes WAF, DDoS protection and edge caching of Next.js static assets. It adds proxy-header and origin-lockdown work.
- **IPv6-only.** Not recommended: IPv4-only destinations would require a paid NAT gateway, which costs far more than one $3.65/mo IPv4.

### Cited Findings
- **CloudFront flat-rate plans (announced Nov 2025):**
  - Free: $0, 1M requests and 100 GB per month, 5 WAF rules, always-on DDoS, Route 53 DNS, TLS certificate, 5 GB S3 credits.
  - Pro: $15, 10M requests, 50 TB, 25 WAF rules, logging.
  - No overage charges.
  - Private (VPC) origins only from the Business plan.
  - Origins can be "any publicly accessible URL".
  - Source: [AWS CloudFront pricing](https://aws.amazon.com/cloudfront/pricing/); [AWS What's New, Nov 2025](https://aws.amazon.com/about-aws/whats-new/2025/11/aws-flat-rate-pricing-plans).
  - A DEV post claims a limit of three Free-plan distributions per account; this is unverified — [DEV Community](https://dev.to/aws-builders/new-pricing-model-for-cloudfront-213k).
- **CloudFront VPC origins:**
  - VPC origins support EC2 instances in private subnets, including in Seoul.
  - The origin security group should allow the `com.amazonaws.global.cloudfront.origin-facing` managed prefix list.
  - Private IPs used have "no additional cost".
  - VPC origins do not support gRPC or Lambda@Edge origin triggers.
  - Source: [AWS CloudFront docs: VPC origins](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html).
- **IPv6-only:** IPv6-only workloads reaching IPv4-only internet services need DNS64 on the subnet plus a NAT gateway, which provides NAT64 — [AWS VPC docs: DNS64/NAT64](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-nat64-dns64.html). Lightsail's IPv6-only 2 GB bundle is $10 versus $12 with IPv4 — [Lightsail pricing](https://aws.amazon.com/lightsail/pricing/).
- **Patching on AL2023:**
  - "By default, your AL2023 instance doesn't automatically receive additional critical and important security updates". Repositories are locked to the AMI's release version.
  - Use `dnf check-release-update` / `dnf upgrade --releasever=…`, or SSM Patch Manager.
  - Source: [AL2023 deterministic upgrades](https://docs.aws.amazon.com/linux/al2023/ug/deterministic-upgrades.html).
  - Patch Manager supports scan or scan-and-install on a schedule via Quick Setup patch policies. By default it focuses on security updates. "AWS doesn't test patches before making them available" — [AWS Patch Manager docs](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager.html).
- **SSM Agent:** SSM Agent comes preinstalled on AL2023 and Ubuntu 22.04/24.04 AMIs, but the preinstalled version may not be the latest — [AWS SSM docs](https://docs.aws.amazon.com/systems-manager/latest/userguide/ami-preinstalled-agent.html).
- **Time sync:** AWS recommends the local Amazon Time Sync Service on instances. A wrong clock breaks AWS SDK request signing — [AWS EC2 docs: time sync](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html).
- **Docker log rotation:** Docker does no log rotation by default and recommends the `local` driver. Daemon logging settings apply only to new containers — [Docker logging docs](https://docs.docker.com/engine/logging/configure/).
- **Swap and kernel settings for Redis:** Redis recommends swap equal to RAM, `vm.overcommit_memory=1` and THP disabled — [Redis admin docs](https://redis.io/docs/latest/operate/oss_and_stack/management/admin/).
- **ECR:** Storage is $0.10/GB-month, with 500 MB/month free for one year for new customers. Same-region pulls to EC2 are free — [AWS ECR pricing](https://aws.amazon.com/ecr/pricing/).
- **Next.js cache in containers:** The Next.js server cache (ISR and optimized images) is on local disk per instance. It "works automatically for a single self-hosted `next start` instance with persistent local disk" — [Next.js self-hosting](https://nextjs.org/docs/app/guides/self-hosting).

### Inferences
- **Add now (cost ≈ $0–4/mo):**
  - **Elastic IP:** keeps the Route 53 A record valid across stop/start and retirement.
  - **2 GB swap file and kernel settings:** `vm.swappiness=10`, `vm.overcommit_memory=1`, THP=never, applied through user-data.
  - **Docker settings:** `/etc/docker/daemon.json` with `log-driver: local` (or json-file with 10m×3) before the first `compose up`.
  - **`mem_limit` per service** (section 2).
  - **Named volumes** for Caddy `/data` and Next.js `.next/cache`. Container filesystems are replaced on every deploy, so without a volume the ISR/image cache is lost each deploy.
  - **SSM Patch Manager patch policy:** weekly scan-and-install of Security updates with `RebootIfNeeded` in a low-traffic window. Or a monthly `dnf upgrade --releasever=latest` via SSM Run Command, followed by a `compose up --wait` health check.
  - **ECR lifecycle policy:** keep the last 10 images per repository.
  - **Security group:** only 80/443 (TCP and UDP for HTTP/3) inbound, no 22 (SSM Session Manager replaces SSH); IMDSv2 required.
  - **CloudWatch agent:** memory, disk and swap metrics plus alarms (memory > 85%, disk > 80%, status checks, surplus credits), and an AWS Budget alert.
- **Evaluate:**
  - **CloudFront Free plan:** Caches Next.js `/_next/static/*` (immutable) at the edge and adds WAF and DDoS protection for $0.
  - Downside 1: Caddy must trust CloudFront's forwarded IP headers. Configure `trusted_proxies` with CloudFront ranges, read `CloudFront-Viewer-Address` or X-Forwarded-For, and pass the real client IP on to FastAPI rate limits.
  - Downside 2: The origin should be locked to the CloudFront prefix list. Without that, attackers bypass the edge.
  - Downside 3: 20 MB uploads pass through CloudFront. This was not verified against CloudFront body-size limits (see Gaps).
  - Since tens of concurrent users and 1M requests/month are within the Free plan, it is a reasonable "phase 2" item rather than a launch blocker.
- **Skip:**
  - IPv6-only: GitHub, the Korean public-data APIs and possibly other dependencies may be IPv4-only, which would force NAT64 through a NAT gateway.
  - VPC-origin/private-subnet EC2: outbound calls to OpenAI and the public APIs would then need a NAT gateway, and VPC origins on flat-rate need the Business plan.
- **Time sync:** AL2023 and Ubuntu AMIs already ship chrony pointed at the Amazon Time Sync Service (general knowledge, not re-verified). Just verify with `chronyc tracking` rather than adding anything.

### Gaps
- NAT gateway hourly price for Seoul was not extracted, because it is not in the VPC price file that was parsed.
- CloudFront's maximum request body size for POST/PUT was not verified.
- Not verified: IPv6 reachability of data.go.kr, OpenAI, GitHub and ECR endpoints.
- Default EC2 metrics lacking memory/disk (so the CloudWatch agent is needed) is general knowledge, not re-verified in this session.
- Ubuntu's default unattended-upgrades behavior was not re-verified in this session.
- Korean-language practitioner posts (velog, tistory, company tech blogs) on single-EC2 Compose operations could not be collected after the search budget ran out; only GeekNews and AWS Korea pages surfaced.

### All sources consulted (URL list)
- https://docs.aws.amazon.com/apprunner/latest/dg/what-is-apprunner.html
- https://encore.dev/articles/end-of-app-runner
- https://en.wikipedia.org/wiki/AWS_App_Runner (search result only)
- https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-overview.md
- https://aws.amazon.com/blogs/aws/build-production-ready-applications-without-infrastructure-complexity-using-amazon-ecs-express-mode
- https://aws.amazon.com/ko/blogs/aws/build-production-ready-applications-without-infrastructure-complexity-using-amazon-ecs-express-mode/ (Korean-locale copy; search result)
- https://aws.amazon.com/about-aws/whats-new/2025/11/announcing-amazon-ecs-express-mode/
- https://dev.classmethod.jp/articles/ecs-express-mode-alb-creation-timing/
- https://www.factualminds.com/blog/amazon-ecs-express-mode/ (search result; its "ECS Gateway" claims unverified, not relied on)
- https://aws.amazon.com/ec2/instance-types/t4/
- https://aws.amazon.com/ec2/faqs/
- https://dev.classmethod.jp/en/articles/ec2-t4g-small-free-tier-2026/
- https://amazonaws.cn/en/new/2025/announcing-amazon-ec2-t4g-free-trial
- https://repost.aws/articles/ARbeHG--bbT6mXw38WgSz01w/announcing-amazon-ec2-t4g-free-trial-extension (search result)
- https://aws.amazon.com/free/
- https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Seoul)/Linux/index.json
- https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ebs.json
- https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ecs/USD/current/ecs.json
- https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/elb/USD/current/elb.json
- https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/vpc/USD/current/vpc.json
- https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/lightsail/USD/current/lightsail.json (downloaded; rate codes not human-readable, not used)
- https://instances.vantage.sh/aws/ec2/t4g.small
- https://instances.vantage.sh/aws/ec2/t4g.medium
- https://www.devzero.io/instances/aws/regions/ap-northeast-2 (search result)
- https://aws-pricing.com/ap-northeast-2.html (search result)
- https://wring.co/blog/aws-ebs-pricing-guide
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances-unlimited-mode-concepts.html
- https://vantage.sh/blog/m7i-flex-vs-t-series-cost
- https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights
- https://aws.amazon.com/about-aws/whats-new/2024/02/aws-free-tier-750-hours-free-public-ipv4-addresses/
- https://www.techradar.com/pro/aws-could-quietly-become-an-internet-domain-kingmaker-as-it-starts-charging-for-ipv4-addresses (search result)
- https://aws.amazon.com/lightsail/pricing/
- https://cloudburn.io/blog/amazon-lightsail-pricing
- https://kuberns.com/blogs/aws-lightsail-pricing-your-comprehensive-guide/
- https://toolradar.com/tools/amazon-lightsail
- https://repost.aws/questions/QUT9M2DAKiQTSkOXZnaYYR0g/does-lightsail-charge-extra-ip-fees
- https://docs.aws.amazon.com/ko_kr/lightsail/latest/userguide/understanding-public-ip-and-private-ip-addresses-in-amazon-lightsail.html (Korean AWS doc; search result)
- https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker.html
- https://docs.fly.io/reference/regions
- https://docs.fly.io/about/pricing
- https://render.com/docs/regions
- https://docs.railway.com/reference/deployment-regions
- https://costbench.com/compare/railway-vs-render/ (search result)
- https://kamal-deploy.org/
- https://news.hada.io/topic?id=8445
- https://github.com/Wowu/docker-rollout
- https://www.virtualizationhowto.com/2025/06/docker-rollout-zero-downtime-deployments-for-docker-compose-made-simple/
- https://linuxtldr.com/installing-docker-rollout/
- https://supun.io/zero-downtime-deployments-docker-compose
- https://docs.docker.com/reference/cli/docker/compose/up/
- https://docs.docker.com/reference/compose-file/services/
- https://docs.docker.com/reference/compose-file/deploy/
- https://docs.docker.com/engine/logging/configure/
- https://docs.docker.com/engine/containers/resource_constraints/
- https://eastondev.com/blog/en/posts/dev/20260424-docker-compose-production/
- https://stackharbor.com/en/knowledge-base/docker-compose-depends-on-healthcheck/ (search result)
- https://nextjs.org/docs/app/guides/self-hosting
- https://nextjs.org/docs/app/api-reference/config/next-config-js/output
- https://nextjs.org/docs/app/guides/memory-usage
- https://ibl.ai/developer/os/standalone-deployment
- https://station.railway.com/questions/memory-usage-and-disk-space-15c5e366
- https://nodejs.org/en/learn/diagnostics/memory/understanding-and-tuning-memory
- https://sharp.pixelplumbing.com/install
- https://fastapi.tiangolo.com/deployment/docker/
- https://fastapi.tiangolo.com/hi/deployment/server-workers/ (search result)
- https://github.com/pydantic/pydantic/issues/6620
- https://arq-docs.helpmanual.io/
- https://redis.io/docs/latest/operate/oss_and_stack/management/admin/
- https://pillow.readthedocs.io/en/stable/reference/Image.html
- https://pypi.org/pypi/pillow/json
- https://pypi.org/pypi/pillow-heif/json
- https://pypi.org/pypi/argon2-cffi/json
- https://pypi.org/pypi/argon2-cffi-bindings/json
- https://pypi.org/pypi/asyncpg/json
- https://pypi.org/pypi/uvloop/json
- https://pypi.org/pypi/httptools/json
- https://pypi.org/pypi/pydantic-core/json
- https://pypi.org/pypi/psycopg-binary/json
- https://pypi.org/pypi/cryptography/json
- https://pypi.org/pypi/orjson/json
- https://pypi.org/pypi/arq/json
- https://pypi.org/pypi/redis/json
- https://github.com/aws/aws-graviton-getting-started/blob/main/python.md
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
- https://caddyserver.com/docs/caddyfile/directives/request_body
- https://caddyserver.com/docs/caddyfile/options
- https://caddyserver.com/docs/automatic-https
- https://github.com/caddyserver/caddy/releases
- https://hub.docker.com/_/caddy
- https://github.com/mholt/caddy-ratelimit
- https://letsencrypt.org/docs/rate-limits/
- https://www.linux.org/threads/linuxiac-caddy-2-11-1-web-server-released-with-automatic-ech-key-rotation.63099/ (search result)
- https://falcao.org/posts/caddy-nginx-traefik-2026/
- https://dokploy.com/blog/caddy-vs-traefik-vs-nginx
- https://wz-it.com/en/blog/caddy-traefik-nginx-reverse-proxy-comparison/
- https://guptadeepak.com/tools/top-5-reverse-proxies-2026/
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-recover.html
- https://docs.amazonaws.cn/en_us/AWSEC2/latest/UserGuide/instance-configuration-recovery.html
- https://repost.aws/knowledge-center/ec2-automatic-recovery-status-check
- https://oneuptime.com/blog/post/2026-02-12-set-up-ec2-auto-recovery-for-instance-health/view
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-retirement.html
- https://repost.aws/knowledge-center/ec2-instance-retirement
- https://docs.aws.amazon.com/ebs/latest/userguide/default-policies.html
- https://docs.aws.amazon.com/dlm/latest/APIReference/API_CreateLifecyclePolicy.html
- https://repost.aws/knowledge-center/ec2-memory-swap-file
- https://dev.classmethod.jp/articles/how-to-create-swap-memory-in-linux-on-ec2-jp/
- https://aws.amazon.com/cloudfront/pricing/
- https://aws.amazon.com/about-aws/whats-new/2025/11/aws-flat-rate-pricing-plans
- https://dev.to/aws-builders/new-pricing-model-for-cloudfront-213k
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html
- https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-nat64-dns64.html
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html
- https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager.html
- https://docs.aws.amazon.com/linux/al2023/ug/deterministic-upgrades.html
- https://docs.aws.amazon.com/systems-manager/latest/userguide/ami-preinstalled-agent.html
- https://aws.amazon.com/ecr/pricing/
