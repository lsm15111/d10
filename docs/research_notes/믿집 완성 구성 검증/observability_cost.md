# 믿집 observability (monitoring · logging · alerting · error tracking) and total monthly cost — AWS Seoul (ap-northeast-2)

Research date: 2026-10-29. Every price below was read on 2026-10-29 unless marked otherwise. AWS unit prices for Seoul were taken directly from the official **AWS Price List API** files for `ap-northeast-2` (machine-readable, the same data the pricing pages render); each file's `publicationDate` is given where it was printed (e.g., CloudWatch 2026-10-07, RDS 2026-10-29, S3 2026-10-15, VPC 2026-10-16, SSM 2026-10-08, SNS 2026-09-15, ECR/Route 53/X-Ray 2026-09-11, EC2 pricing-page JSON 2026-10-28). Where an AWS marketing page shows a us-east-1 example price that differs from the Seoul price list, the Seoul price list wins and the conflict is noted.

Note on method: the shared web-search budget ran out part-way through (the tool reported "limit: 200 WebSearch calls per turn, shared by every agent"). After that, only direct fetches of known official URLs and the AWS Price List API were used. Some sources are search-result snippets only (marked "search snippet"); everything else was fetched.

Architecture assumed (from the brief, not re-verified here): 1× EC2 t4g.small running Docker Compose (Caddy, Next.js 16, FastAPI with 2 uvicorn workers, Redis, arq worker); RDS PostgreSQL 17 db.t4g.micro Single-AZ, 20 GB gp3; private S3 bucket (a few GB); SES; Route 53 + domain; ECR; SSM Parameter Store; GitHub Actions; OpenAI API.

---

## Q1. Logs — shipping method (awslogs vs CloudWatch agent vs Fluent Bit), retention, Seoul prices, structured JSON, keeping personal data out

### Takeaway
For one Docker Compose host, use the Docker `awslogs` driver per container (no extra agent process), with non-blocking mode and pre-created log groups that have explicit retention. Use structured JSON logs (structlog for FastAPI; Caddy already writes JSON) with a request ID. Keep personal data out at the source rather than relying on CloudWatch masking. In Seoul, log ingestion costs $0.76/GB (Standard) or $0.38/GB (Infrequent Access), storage $0.0314/GB-month, and the first 5 GB/month are free. At a few to ~10 GB/month the total log bill is $0–4.

### Cited Findings
**Shipping options**
- Docker `awslogs` options: `awslogs-region` (defaults to the instance's region on EC2), `awslogs-group` (required), `awslogs-stream` (defaults to container ID; don't share one stream across concurrently running containers), `awslogs-create-group` (default `false`; needs `logs:CreateLogGroup`), `awslogs-multiline-pattern`/`awslogs-datetime-format`, `tag`, `awslogs-force-flush-interval-seconds` (default 5 s), `awslogs-max-buffered-events` (default 4K). On EC2 the daemon can use the instance profile. Required IAM: `logs:CreateLogStream`, `logs:PutLogEvents`. Docker reads credentials when the container starts. With temporary credentials, restart the container after refreshing them. Multiline regex matching per message can hurt performance. — [Docker awslogs driver docs](https://docs.docker.com/engine/logging/drivers/awslogs/)
- Docker delivery modes: the default is "direct, blocking delivery" from container to driver. `mode: non-blocking` puts a per-container ring buffer in between. When the buffer is full, new messages are dropped. `max-buffer-size` defaults to 1m (1 MB) and applies only in non-blocking mode. The default `json-file` driver does **no rotation by default** and can exhaust disk. Docker recommends the `local` driver otherwise, because it rotates by default. — [Docker "Configure logging drivers"](https://docs.docker.com/engine/logging/configure/)
- AWS (ECS context): in blocking mode a stalled log flow can freeze the app's stdout/stderr writes and fail health checks. AWS recommends non-blocking when availability matters more than every log line. ECS switched its default to non-blocking on 2025-06-25. ECS's `max-buffer-size` default is 10m. — [ECS LogConfiguration API reference](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_LogConfiguration.html) (search snippet). Conflict on the buffer default: Docker Engine documents 1m, ECS documents 10m. Use Docker's value on plain EC2.
- Fluent Bit's core C plugin `cloudwatch_logs` has these options: `region`, `log_group_name`, `log_stream_prefix`, `auto_create_group` (default false), and `log_retention_days` (default 0; only allowed values such as 7/30/365). It needs `logs:CreateLogStream`, `logs:CreateLogGroup`, `logs:PutLogEvents` and `logs:PutRetentionPolicy`. It can also emit EMF metrics (cpu/mem only). The docs give no memory benchmarks. — [Fluent Bit CloudWatch output](https://docs.fluentbit.io/manual/pipeline/outputs/cloudwatch)
- The CloudWatch agent collects metrics, logs and traces from servers and containers and is usually deployed and configured via SSM Parameter Store. The instance role needs `CloudWatchAgentServerPolicy` and `AmazonSSMManagedInstanceCore`. — [CloudWatch solution: EC2 health](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Solution-EC2-Health.html)

**Log classes and retention**
- Standard vs Infrequent Access (IA): the two classes differ only in ingestion price; storage and Logs Insights prices are the same. **A log group's class can't be changed after creation.** IA does **not** support metric filters, subscription filters, Live Tail, Logs Anomaly Detection, field indexing, EMF, or GetLogEvents/FilterLogEvents (you must use Logs Insights). IA does support Logs Insights, S3 export, KMS and data-protection masking. — [CloudWatch Logs log classes](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html)

**Seoul prices (AWS Price List, AmazonCloudWatch ap-northeast-2, published 2026-10-07, read 2026-10-29)** — [Price List: CloudWatch Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/ap-northeast-2/index.json)
- Custom log ingestion, Standard class: **$0.76/GB**. Infrequent Access: **$0.38/GB**.
- Log storage: **$0.0314/GB-month**. IA "TimedStorage-IA" is $0.01884/GB-month (as listed).
- Logs Insights scan: **$0.0076/GB**. Live Tail: $0.01/min after 1,800 free minutes.
- Data protection (masking) scanning: **$0.12/GB** in Seoul.
- Monthly free usage (Global SKUs): 5 GB of log data ingestion, 5 GB archived storage, 5 GB Logs Insights scan, 5 GB data delivery, and 1,800 Live Tail minutes. — same price list. The pricing page describes this as "5 GB across ingestion, archive storage, and Logs Insights scans". — [CloudWatch pricing page](https://aws.amazon.com/cloudwatch/pricing/)
- The pricing page's container examples use $0.50/GB ingestion. That is the us-east-1 rate; Seoul is $0.76/GB per the price list. — [CloudWatch pricing page](https://aws.amazon.com/cloudwatch/pricing/)

**Structured logs and PII**
- structlog (current version 26.1.0) is described as "the production-ready logging solution for Python". It supports JSON, logfmt and console output, has a Context Variables chapter (for request-scoped binding) and a Standard Library Logging chapter (for forwarding into `logging`). — [structlog docs](https://www.structlog.org/en/stable/)
- Caddy's access log format defaults to `json` when stderr isn't a terminal. Request headers are logged, but `Cookie`, `Set-Cookie`, `Authorization` and `Proxy-Authorization` are redacted by default. `format filter` can `delete`/`hash`/`replace`/`regexp` fields, and `ip_mask` truncates client IPs (e.g., `request>remote_ip ip_mask 16 32`). File output rolls at 100 MiB, keeps 10 files and 90 days by default. — [Caddy `log` directive](https://caddyserver.com/docs/caddyfile/directives/log)
- arq logs successful job results by default (`log_results` defaults to true), so sensitive return values reach worker logs unless `log_results=False`. Results are kept in Redis for 3,600 s by default (`keep_result`). Job `args`/`kwargs` are stored (pickle by default) and visible via `Job.info()`/`queued_jobs()`. — [arq docs](https://arq-docs.helpmanual.io/)
- OWASP: don't log session identifiers (hash them if you need them for tracking), access tokens, passwords, DB connection strings, encryption keys, payment/bank data, sensitive PII (e.g., government identifiers, health data), or data the user did not consent to. Do record when/where/who/what (timestamp, interaction ID, app name and version, host, entry URL and method, source IP, user identity, event type, severity, security-relevant flag). — [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- CloudWatch Logs data-protection policies mask matching data at ingestion on all egress points (Insights, metric filters, subscriptions). Only principals with `logs:Unmask` can see the raw values. Logs ingested before the policy aren't masked. Managed identifiers cover credentials, financial, PII, PHI and device IDs (IP/MAC), and custom regex identifiers are supported. The `LogEventsWithFindings` metric is free. Masking works in both Standard and IA classes. — [CloudWatch Logs masking](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html). Seoul cost: $0.12/GB scanned — [Price List: CloudWatch Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/ap-northeast-2/index.json)
- OpenTelemetry FastAPI instrumentation can capture request/response headers as span attributes. `OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SANITIZE_FIELDS` (regex list) replaces matching values with `[REDACTED]`. `excluded_urls` (e.g., `health.*`) skips health endpoints. The header-capture env-var names are marked experimental. — [opentelemetry-instrumentation-fastapi](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html)

### Inferences
- **Recommended shipping: `awslogs` driver in `docker-compose.yml` (`x-logging` anchor)** with `awslogs-region: ap-northeast-2`, one group per service (`/mitjip/prod/caddy`, `/mitjip/prod/api`, `/mitjip/prod/web`, `/mitjip/prod/worker`; Redis optional), `awslogs-create-group: "false"` (create the groups in IaC or the CLI with retention set), `mode: non-blocking`, `max-buffer-size: 4m`, and `tag: "{{.Name}}"`. Reasons: zero extra processes on a 2 GiB box and the instance role supplies credentials. Fluent Bit is only worth it for fan-out to multiple sinks. The CloudWatch agent's log collection would duplicate what the driver does, so use the agent only for host metrics (Q2).
- Keep `/health/live` and `/health/ready` probes out of the access logs (Caddy `skip_log` or app filter) and out of traces (`excluded_urls`). Otherwise an uptime monitor every 1–3 minutes creates noise and cost.
- **Retention:** 14 days for Caddy access logs, 30 days for app, web and worker logs. If a separate admin/audit log is kept for 개인정보처리시스템 access (see Gaps), keep it ≥1 year in a separate log group, or in S3 via export (cheaper storage). Never leave the default "Never expire".
- **Log class:** stay on Standard. At ≤10 GB/month, IA would save at most ~$2–4/month but loses metric filters (needed for a "5xx count" alarm), Live Tail and `GetLogEvents`. Since the class can't be changed later, choose Standard at creation.
- **PII rules for 믿집** (quote data contains names, phone numbers, apartment 동/호, addresses, and photos/plans):
  - Log an internal `user_id` and `quote_id` (UUIDs) instead of names, phones or addresses.
  - Never log request/response bodies of quote, upload or auth endpoints.
  - Strip query strings in access logs, or ensure no PII ever goes in query strings.
  - Mask client IPs with Caddy `ip_mask` (e.g., /24) unless they're needed for abuse handling.
  - Set arq `log_results=False` and pass only IDs as job args.
  - Don't log S3 presigned URLs; they are bearer tokens.
  - Add a single CloudWatch masking policy (email and phone custom regex) as a safety net only. At ~5–10 GB/month it costs ~$0.6–1.2, so this is optional.

### Gaps
- Whether `docker logs` keeps working with the `awslogs` driver ("dual logging") wasn't confirmed: the fetched Docker page didn't cover it.
- The CloudWatch agent's own memory footprint on ARM, and a Fluent Bit vs agent benchmark, weren't found because the search budget ran out.
- Uvicorn's default access log format (client address and query string) couldn't be fetched (uvicorn.org DNS failure). Check whether `--no-access-log` plus Caddy access logs is sufficient.
- **Korean PIPA requirement (unverified in this session):** 「개인정보의 안전성 확보조치 기준」 제8조 is commonly cited as requiring 접속기록 for 개인정보처리시스템 access by 취급자 to be kept ≥1 year (≥2 years for ≥50,000 정보주체, 고유식별정보 or 민감정보), and checked at least monthly. law.go.kr returned only a JS shell, so this must be verified before it's written into the design.

---

## Q2. Metrics — what default EC2 metrics miss, CloudWatch agent cost, T4g CPU-credit alarms, RDS alarms, Database Insights / Performance Insights in 2026

### Takeaway
Default EC2 metrics are free but have no memory or disk-usage figures. The CloudWatch agent adds them as custom metrics at $0.30/metric-month in Seoul (first 10 free), so 3–6 metrics cost $0–$2. Both the t4g.small and db.t4g.micro run in **unlimited** credit mode by default, so CPU-credit exhaustion shows up as **extra charges**, not throttling. Alarm on `CPUSurplusCreditsCharged`/`CPUCreditBalance`, not just CPU%. Performance Insights reached end-of-life on 2026-07-31. Its replacement, **Database Insights Standard mode, is free with 7-day retention and is supported on RDS PostgreSQL db.t4g.micro**. Advanced mode (~$18/month here) isn't worth it.

### Cited Findings
**Custom metrics and the agent**
- All CloudWatch-agent metrics are billed as custom metrics, while vended `AWS/EC2` metrics are free. The disk metrics count multiplies by `device/fstype/path` dimensions. A default t2.micro example produces 22 agent metrics (4 CPU, 12 disk, 4 diskio, 1 mem, 1 swap). The agent calls `PutMetricData` once a minute, i.e. 43,200 calls per host per 30 days. — [CloudWatch solution: EC2 health](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Solution-EC2-Health.html)
- Seoul custom metrics: **$0.30/metric-month for the first 10,000**, then $0.10, $0.05, $0.02 per tier. Alarms: **$0.10 per standard-resolution alarm metric-month**, $0.30 high-resolution, $0.50 composite. Monthly free: 10 metrics, 10 alarms, 1M API requests, 100 canary runs. — [Price List: CloudWatch Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/ap-northeast-2/index.json)
- Dashboards: $3.00 per dashboard-month, and the first 3 are free (Global SKU). — [Price List: CloudWatch global](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/index.json). The pricing page adds that the 3 free dashboards are limited to 50 metrics each, and that GetMetricData/GetMetricWidgetImage calls are always billed. — [CloudWatch pricing page](https://aws.amazon.com/cloudwatch/pricing/)

**T4g credits**
- t4g.small earns **24 credits/hour**, accrues a maximum of **576**, has 2 vCPUs and a **20% baseline per vCPU**. t4g.micro earns 12/hour (max 288, 10% baseline). T4g credits persist 7 days after a stop. — [EC2 burstable credit table](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html)
- T4g (and T3/T3a/T8i) launch in **unlimited mode by default**. If average CPU over a rolling 24 h exceeds baseline, surplus credits are billed at a flat rate per vCPU-hour. They are also charged when the instance stops or switches to standard. Watch `CPUSurplusCreditBalance` and `CPUSurplusCreditsCharged`. — [Unlimited mode concepts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances-unlimited-mode-concepts.html)
- Seoul EC2 T4g surplus credits cost **$0.04 per vCPU-hour** (`APN2-CPUCredits:t4g`). — [Price List: EC2 Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-northeast-2/index.json). The T4g product page also says $0.04 per vCPU-hour for prolonged high CPU. — [EC2 T4g page](https://aws.amazon.com/ec2/instance-types/t4/)
- RDS T4g/T3 DB instances "run in Unlimited mode". The RDS PostgreSQL pricing page says CPU credits are "$0.075 per vCPU-Hour… the same for all T4g and T3 sizes in all regions". — [RDS for PostgreSQL pricing](https://aws.amazon.com/rds/postgresql/pricing/). **Contradicted by** the Seoul price list, which lists `APN2-CPUCredits:db.t4g` at **$0.09 per vCPU-hour** ("USD 0.09 per vCPU-Hour of T4g CPU Credits"). — [Price List: RDS Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/ap-northeast-2/index.json)

**AWS-recommended alarms**
- EC2: `CPUUtilization` > 80 (Average, 300 s, 3 of 3) and `StatusCheckFailed` ≥ 1 (Maximum, 300 s, 2 of 2). Also `StatusCheckFailed_AttachedEBS`. — [CloudWatch recommended alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html)
- RDS, all at 60 s periods (same page):
  - `CPUUtilization` > 90, 5 datapoints.
  - `DatabaseConnections` > 90–95% of max connections, 5 datapoints.
  - `EBSByteBalance%` and `EBSIOBalance%` < 10, 3 datapoints.
  - `FreeableMemory` should not stay below 25% of total memory, 15 datapoints.
  - `FreeStorageSpace` < ~10% of allocated storage, 5 datapoints.
  - `MaximumUsedTransactionIDs` > 1e9, 1 datapoint.
  - `Read/WriteLatency` > ~20 ms investigate, 5 datapoints.
  - `DBLoad` above the vCPU line, 15 datapoints.

  The fetched RDS section did not list a CPUCreditBalance alarm.
- RDS PostgreSQL default `max_connections` = `LEAST({DBInstanceClassMemory/9531392}, 5000)`. DBInstanceClassMemory is below nominal RAM because the OS and RDS processes reserve memory. — [RDS quotas: max connections](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html)

**Performance Insights → Database Insights**
- "AWS announced that the end-of-life date for Performance Insights was July 31, 2026, and has migrated Performance Insights users to Database Insights." Standard mode is the default: detailed database and per-query metric retention is **free up to 7 days**, with paid retention of 1–24 months. Advanced mode adds 1–24-month retention at no extra cost, plus per-query stats, lock analysis (PostgreSQL), slow-SQL analysis (needs log export), fleet views and on-demand analysis. — [CloudWatch Database Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Database-Insights.html); also [RDS Performance Insights overview](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.Overview.md) (search snippet: "console will redirect to CloudWatch Database Insights")
- Instance-class support: Database Insights **isn't supported** on db.t2/t3/t4g micro/small **for MariaDB and MySQL**. For **RDS for PostgreSQL** the restriction column is "N/A" (no restriction). Seoul is a supported region. — [RDS engine/instance support for Database Insights](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_DatabaseInsights.Engines.html)
- Seoul Database Insights prices: Advanced mode **$0.0125 per vCPU-hour** for RDS PostgreSQL provisioned. Standard-mode extended retention is $0.002405/vCPU-hour for the first month of retention and $0.000101/vCPU-hour per additional month. The DI API costs $0.00001/call after 1M free. — [Price List: CloudWatch Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/ap-northeast-2/index.json)
- A third-party write-up notes DI is billed per vCPU-hour (PI was per vCPU-month). — [DoiT blog](https://www.doit.com/blog/transitioning-from-rds-performance-insights-to-cloudwatch-database-insights) (search snippet)

### Inferences
- **CloudWatch agent config (metrics only):** collect `mem_used_percent`, `swap_used_percent`, and `disk_used_percent` restricted to `"resources": ["/"]`. Drop `inodes_free` and diskio. Don't append `ImageId`/`InstanceType` dimensions. That gives 3 custom metrics, or 4–5 if the Docker data root sits on a separate volume, which fits inside the 10 free metrics. Avoid the "EC2 Health solution" default config (22 metrics ≈ $3.6/month).
- **Alarm set (~12 alarms ≈ $0.20/month after the 10 free):**
  1. EC2 `StatusCheckFailed` ≥ 1 for 2×5 min → recover/notify.
  2. EC2 `CPUCreditBalance` < 100 (≈4 h of baseline headroom; max 576) for 3×5 min.
  3. EC2 `CPUSurplusCreditsCharged` > 0 (daily signal that unlimited mode is costing money).
  4. `mem_used_percent` > 90 for 5 min (2 GiB host running Next.js, 2 uvicorn workers, Redis and arq).
  5. `disk_used_percent` > 80.
  6. RDS `CPUCreditBalance` < ~50 (db.t4g.micro presumably mirrors t4g.micro's 12 credits/h and 288 max; RDS credit table not verified).
  7. RDS `FreeStorageSpace` < 2 GB (10% of 20 GB) — or enable storage autoscaling.
  8. RDS `FreeableMemory` < ~200 MB for 15 min (25% of 1 GiB).
  9. RDS `DatabaseConnections` > 80 (verify actual `max_connections` with `SHOW max_connections`; the formula gives ~100 or fewer on 1 GiB).
  10. RDS `MaximumUsedTransactionIDs` > 1e9.
  11. Log-metric-filter alarm for API 5xx count > N in 5 min.
  12. External uptime monitor (Q3).

  The AWS Budgets alerts are separate and free (Q6).
- Enable **Database Insights Standard** (free, 7 days) on the db.t4g.micro. Skip Advanced: 2 vCPU × 730 h × $0.0125 ≈ $18.25/month, about the same as the DB instance itself. Enable RDS log export of `postgresql` logs with `log_min_duration_statement` ≈ 500 ms only if slow queries become a problem (these logs count toward CloudWatch Logs ingestion).
- At the brief's scale (tens of concurrent users), the 20% baseline (0.4 vCPU sustained) should be ample. The main risks are Next.js builds on the box (build in GitHub Actions and push to ECR instead) and runaway workers. Memory, not CPU, is the likely first bottleneck on a 2 GiB host, so the `mem_used_percent` alarm matters most.

### Gaps
- The RDS burstable credit table (credits/hour, max balance for db.t4g.micro) wasn't fetched. The EC2 values were used as a proxy.
- Real measured RAM usage of this Compose stack on t4g.small wasn't researched.

---

## Q3. Uptime / synthetic checks and alert routing (SNS email, Slack, Discord, Kakao)

### Takeaway
Use a **free external uptime monitor** (Better Stack free: 10 monitors + 10 heartbeats + a status page, 3-minute checks, Slack/email; or UptimeRobot free: 50 monitors, 5-minute checks, 1 status page) against `/health/ready`. Add a **heartbeat** monitor (Healthchecks.io free, 20 checks, or Better Stack heartbeats) for the arq worker and nightly jobs. CloudWatch Synthetics costs ~$16/month per 5-minute canary in Seoul plus Lambda/S3/log extras, which is poor value here. Route alarms CloudWatch → SNS → email (first 1,000 emails/month free) and to Slack via Amazon Q Developer in chat applications (AWS Chatbot: no extra charge). Discord needs a tiny relay because the SNS envelope isn't a Discord payload. Kakao's message API is not designed for server alerts.

### Cited Findings
- **CloudWatch Synthetics, Seoul:** **$0.0019 per canary run**, first 100 runs/month free. — [Price List: CloudWatch Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/ap-northeast-2/index.json). The pricing-page example (us-east-1, $0.0012/run) shows canaries also incur Lambda (~$14.89 for 5 canaries every 5 min at 20 s/1 GB), CloudWatch Logs, S3 and metric costs. Five canaries every 5 min: $54.07 canary + $20.59 extras = $74.66/month. — [CloudWatch pricing page](https://aws.amazon.com/cloudwatch/pricing/)
- **Route 53 health checks (global price list, 2026-09-11):** "First 50 Health Checks of AWS endpoints are free of charge". After that, $0.50/month each for AWS endpoints and $0.75/month for non-AWS endpoints. Optional features (HTTPS, string matching, fast interval, latency) cost $1.00 each for AWS endpoints and $2.00 each for non-AWS. — [Price List: Route 53 global](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRoute53/current/index.json); the pricing page calls the 50 free checks a "special offer" for new and existing customers. — [Route 53 pricing](https://aws.amazon.com/route53/pricing/)
- **UptimeRobot (official pricing page):**
  - Free plan: 50 monitors, 5-minute interval, 1 basic status page, "Only 5 integrations" (unnamed). The page calls it "Good for personal and commercial projects."
  - Solo: $9/month annual ($10 monthly), 10 monitors.
  - Team: $35/month annual ($41 monthly), 100 monitors.

  — [UptimeRobot pricing](https://uptimerobot.com/pricing/). **Contradicted by** competitor/third-party pages saying the free plan was restricted to non-commercial use from Nov/Dec 2024. — [notifier.so UptimeRobot pricing 2026](https://notifier.so/guides/uptimerobot-pricing-2026/) (search snippet); [dev.to article](https://dev.to/velprove/uptimerobot-commercial-use-free-alternatives-for-business-sites-in-2026-5d75) (search snippet). These are competitor marketing sources, and the official page currently says commercial use is allowed.
- **Better Stack free:** "10 monitors, 10 heartbeats and a status page with 3-minute checks totally free". — [Better Stack Uptime](https://betterstack.com/uptime). The pricing page lists free alerts as Slack and e-mail (no phone/SMS) plus 3 GB of logs retained 3 days. The cheapest paid item is a Responder seat at $29/month (annual). — [Better Stack pricing](https://betterstack.com/pricing)
- **Healthchecks.io free "Hobbyist":** 20 jobs, 100 log entries per job. The page didn't state integrations or commercial-use terms. — [Healthchecks.io pricing](https://healthchecks.io/pricing/)
- **Uptime Kuma:** MIT-licensed, self-hosted (Docker image `louislam/uptime-kuma:2`). Monitor types include HTTP(s) keyword/JSON query, TCP, ping, DNS, Push and Docker container. Notifications include Telegram, Discord, Slack, email and 90+ others (KakaoTalk not mentioned). Supports multiple status pages. The repo lists no RAM requirement. — [Uptime Kuma GitHub](https://github.com/louislam/uptime-kuma)
- **SNS (Seoul):** first 1,000 email/email-JSON notifications/month free, then $2.00 per 100,000. First 100,000 HTTP/HTTPS deliveries free, then $0.06 per 100,000. First 1M API requests free. — [Price List: SNS Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonSNS/current/ap-northeast-2/index.json)
- **AWS Chatbot / Amazon Q Developer in chat applications:** "no additional charge"; you pay only for the underlying services (SNS, CloudWatch, etc.). The fetched pricing page didn't name the supported chat platforms. — [AWS Chatbot pricing](https://aws.amazon.com/chatbot/pricing/). Cost Anomaly Detection's page says SNS topics can route alerts to Slack, Microsoft Teams or Amazon Chime. — [Cost Anomaly Detection](https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/)
- **Discord** supports Slack-compatible webhooks (`POST /webhooks/{id}/{token}/slack`, without `channel`, `icon_emoji`, `mrkdwn`) and GitHub-compatible webhooks (`/github`). Message `content` is capped at 2,000 characters and 10 embeds. — [Discord webhook docs](https://docs.discord.com/developers/resources/webhook)
- **Kakao:** the KakaoTalk Message API (나에게/친구에게 보내기) is user-to-user and needs a logged-in Kakao user. Friend messaging needs business-app conversion and review (30/day before approval; 30,000/day per app after, with per-sender/recipient caps). Alimtalk (알림톡) is the service-to-user channel via a business KakaoTalk channel. The doc's conclusion: the Message API isn't a fit for server monitoring alerts. — [Kakao Developers: KakaoTalk message](http://developers.kakao.com/docs/ko/kakaotalk-message/common)

### Inferences
- **Recommended uptime setup ($0):**
  1. Better Stack (or UptimeRobot) HTTPS keyword monitor on `https://<domain>/health/ready` every 3–5 min, with `/health/live` as a second monitor so you can tell "Caddy up, DB/Redis down" from "host down".
  2. A heartbeat URL pinged by the arq worker every ~5 min (cron job), plus one after the nightly backup/cleanup job.
  3. The free public status page.

  An external monitor also covers the case where the whole EC2 host dies, which CloudWatch metric alarms see only indirectly.
- Optional: one **Route 53 health check** on the Elastic IP (AWS endpoint → basic check free under the 50-check offer; +$1/month for HTTPS, +$1 for string matching). It gives an AWS-native alarm, but Route 53 health-check metrics live in us-east-1 (unverified here), so the alarm and SNS topic must be created there. The external monitor is simpler.
- Skip CloudWatch Synthetics: a single canary costs ~$16.45/month at 5-minute intervals (8,760 runs × $0.0019 − 100 free) or ~$5.36 at 15 minutes, before Lambda/S3/log extras.
- **Alert routing:**
  - One SNS topic `mitjip-alerts` (Seoul), with email subscriptions for 2–3 team members.
  - Amazon Q Developer in chat applications → a Slack `#mitjip-alerts` channel, if the team uses Slack.
  - For Discord: a ~20-line Lambda (always-free tier) subscribed to SNS that reformats and POSTs to the Discord webhook, or point Better Stack/UptimeRobot/Healthchecks integrations straight at a Discord webhook.
  - Don't use Kakao for ops alerts (Alimtalk requires a business channel and an agency).
- Severity: P1 (site down, DB down, disk > 90%) → Discord/Slack + email immediately. P2 (credit balance low, memory > 90%, 5xx spike) → channel only. Cost/budget alerts → email to the budget owner.

### Gaps
- Which 5 integrations UptimeRobot Free includes (Slack/Discord/webhook?) wasn't confirmed.
- Whether Healthchecks.io's free tier is allowed for commercial use, and its integrations list, weren't confirmed.
- Better Stack free plan's commercial-use terms weren't stated on the fetched pages.
- The us-east-1 requirement for Route 53 health-check alarms wasn't verified in this session.

---

## Q4. Error tracking and tracing (Sentry, GlitchTip, OpenTelemetry → X-Ray / Application Signals) — is tracing worth it?

### Takeaway
Use **Sentry Developer (free)** for both FastAPI and Next.js error tracking: 1 user, 5k errors, 5M spans, 5 GB logs, 30-day lookback, **email-only alerts, no third-party integrations**. Set `send_default_pii=False`, add a `before_send` scrubber and sample traces at ~10–20%. Full distributed tracing (OTel → X-Ray/Application Signals) isn't worth the setup for a single-host monolith with tens of users. Sentry's spans give enough performance data. If tracing is added later, use OpenTelemetry: the X-Ray SDKs/daemon have been in maintenance mode since 2026-02-25.

### Cited Findings
- **Sentry Developer (free), official page:**
  - Limits: 1 user, 5k errors, 5M spans, 50 replays, 5 GB logs (extra $0.50/GB), 1 GB attachments, 1 cron monitor, 1 uptime monitor, 30-day lookback, 10 dashboards.
  - Restrictions: email-only alerts, "no API or third-party integrations", no Seer.

  **Team:** $29/month monthly or $26/month annual. Unlimited users, integrations, 50k errors, up to 90-day lookback, spend notifications and a max-spend threshold. — [Sentry pricing](https://sentry.io/pricing/)
- A third-party source claims Developer includes 50K errors + 10M spans after an August 2025 change. This **conflicts** with the official page (5k errors, 5M spans). — search snippet via [last9 Sentry pricing](https://last9.io/blog/sentry-pricing/) / [agentdeals](https://agentdeals.dev/vendor/sentry). The official page wins.
- **Sentry Python PII:**
  - `send_default_pii` controls default PII collection and is to be replaced by `data_collection` in SDK 3.0.
  - The default `event_scrubber` filters passwords, auth values, sessions, cookies and CSRF tokens. With `send_default_pii=False` it also filters IP addresses.
  - `before_send`, `before_send_transaction` and `before_send_span` hooks scrub locally. Places to check include stack locals, breadcrumbs (DB queries, query strings), user/HTTP context and transaction names.
  - Server-side scrubbing rules can also be set in the UI.

  — [Sentry Python sensitive data](https://docs.sentry.io/platforms/python/data-management/sensitive-data/)
- **GlitchTip hosted:** Free (Hobby & Trial) 1,000 events/month with 30-day retention; Small $15/month (100k events); Medium $50; Large $250. Self-hosting is offered. The page didn't state the license or requirements. — [GlitchTip pricing](https://glitchtip.com/pricing)
- **X-Ray:** "On February 25th, 2026, the AWS X-Ray SDKs/Daemon will enter maintenance mode" (security fixes only). AWS recommends OpenTelemetry SDKs or ADOT for instrumentation, and the CloudWatch agent (v1.300025.0+) or the OTel Collector for collection. — [X-Ray → OpenTelemetry migration](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-migration.html)
- **X-Ray Seoul prices:** 100,000 traces stored free per month, then **$0.000005/trace** ($5 per million). 1M traces accessed free, then $0.0000005. Insights $0.000001/trace. — [Price List: X-Ray Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSXRay/current/ap-northeast-2/index.json). X-Ray spans indexed: $0.00000075 each (Seoul). — [Price List: CloudWatch Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/ap-northeast-2/index.json)
- **Application Signals, Seoul:** **$1.50 per million signals** (first 100M), $0.75 (next 900M), $0.30 (beyond). Span ingestion $0.35/GB for the first 10 TB. — [Price List: CloudWatch Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/ap-northeast-2/index.json). Each inbound request and each outbound dependency call counts as a signal. Free usage lasts 3 months per account (100M signals, or 100 GB / 1M indexed spans with transaction visibility). Default X-Ray sampling is 5%. — [CloudWatch pricing page](https://aws.amazon.com/cloudwatch/pricing/)
- **Next.js OpenTelemetry** (docs updated 2026-10-22):
  - Next.js is "already instrumented". Enable it with `instrumentation.ts` + `@vercel/otel` `registerOTel({serviceName})`, or with manual `NodeSDK` (node runtime only).
  - Default spans include the root `[http.method] [next.route]`, `render route (app)`, `fetch`, and `executing api route`. More spans appear with `NEXT_OTEL_VERBOSE=1`. `NEXT_OTEL_FETCH_DISABLED=1` turns off fetch spans.
  - Self-hosted setups need an OTel Collector or a custom exporter.

  — [Next.js OpenTelemetry guide](https://nextjs.org/docs/app/guides/open-telemetry)
- **FastAPI OTel:** `FastAPIInstrumentor.instrument_app(app, excluded_urls="health.*")`, with header capture and sanitize env vars. — [opentelemetry-instrumentation-fastapi](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html)
- **Grafana Cloud Free** ("Always free", no card): 10k active metric series, 50 GB logs, 50 GB traces, 50 GB profiles (14-day retention each), 100k synthetic API test executions, 3 visualization users, 3 IRM (on-call) users. Paid plans start at $19/month + usage. — [Grafana Cloud pricing](https://grafana.com/pricing/)

### Inferences
- **Recommendation:** Sentry Developer, one project each for `mitjip-api` (sentry-sdk with the FastAPI integration) and `mitjip-web` (@sentry/nextjs).
  - `send_default_pii=False`.
  - `before_send` drops request bodies, cookies and query strings, and replaces user objects with `{id: internal_uuid}`.
  - `traces_sample_rate≈0.1–0.2` and `profiles_sample_rate=0`.
  - Tag events with `release=<git sha>` from GitHub Actions.

  5k errors/month is plenty for a few hundred users unless an error loop occurs, so set a rate limit and inbound filters. Limitation: only 1 seat and email-only alerts on the free plan. Share the login via a team alias address, or accept email alerts. If Slack/Discord routing is essential, Team at $26–29/month is the step up.
- Avoid self-hosting GlitchTip/Sentry on the t4g.small: extra web, worker and DB processes would compete for 2 GiB of RAM. GlitchTip hosted free (1,000 events/month) is a fallback if Sentry's single-seat limit is a blocker.
- **Tracing:** not worth a separate stack at this size. Everything runs on one box, so the only "distributed" hops are Next.js → FastAPI → Postgres/Redis/OpenAI, which Sentry performance spans already show. Application Signals would be cheap after its 3-month trial (e.g., ~300k requests × ~2–3 signals ≈ $1–1.5/month). The cost is operational: the CloudWatch agent as an OTLP receiver plus ADOT Python/Node auto-instrumentation and config on a memory-constrained host. Revisit only if latency debugging across services becomes a real problem.
- Grafana Cloud Free is a credible all-in-one alternative (logs, metrics, traces, synthetics, on-call for 3 users), but it adds a second observability vendor next to CloudWatch, which a student team must learn. Keep it as plan B.

### Gaps
- Sentry's Next.js-specific free-tier caveats (e.g., source-map upload limits) weren't researched.
- GlitchTip's self-host RAM needs weren't found.

---

## Q5. LLM observability (Langfuse cloud vs self-host, OpenAI dashboard/budgets/limits, prompt logging without personal data)

### Takeaway
Use **Langfuse Cloud Hobby (free: 50k units/month, 30-day data access, 2 users; US, EU or Japan region)** with SDK-side masking. Self-hosted Langfuse v3/v4 needs Postgres + ClickHouse + Redis + S3 and a recommended ≥4 cores/16 GiB VM, which is impossible on a t4g.small. On the OpenAI side, create separate **dev/prod projects**, each with a **spend alert and a hard monthly spend limit** (requests return 429 when hit). In-app, log per-call metadata (model, prompt version, tokens, latency, cost, request_id), not raw user text. API data is not used for training by default, and abuse-monitoring logs are kept up to 30 days.

### Cited Findings
- **Langfuse Cloud pricing (official):**
  - Hobby: free, no card, **50k units/month**, 30 days of data access, 2 users, community support.
  - Core: **$29/month**, 100k units, 90-day access, unlimited users.
  - Overage: $8 per 100k units (100k–1M), falling to $6 per 100k beyond 50M.
  - A unit is any tracing data point (trace, observation/span/generation/event, or score).
  - Data-retention deletion is only on Pro/Enterprise. Cloud is hosted on AWS with **US, EU or Japan** regions for Hobby/Core/Pro.
  - "Open source and you can self-host it for free."

  — [Langfuse pricing](https://langfuse.com/pricing.md)
- **Langfuse self-hosting:**
  - Components: Postgres (transactional), ClickHouse (traces/observations/scores), Redis/Valkey (cache and queue), S3/blob storage, plus Web and Worker containers. Some add-on features need a license key. Docker Compose is listed for "Local use and testing", as a "Single VM without high availability, scaling, or backups". — [Langfuse self-hosting](https://langfuse.com/self-hosting)
  - The Compose guide recommends "at least 4 cores and 16 GiB of memory" (e.g., t3.xlarge) and ~100 GiB of storage. — [Langfuse Docker Compose](https://langfuse.com/self-hosting/deployment/docker-compose)
  - The scaling page lists minimums of 2 CPU/4 GiB worker, 2 CPU/4 GiB Postgres, 1 CPU/1.5 GiB Redis, and 2 CPU/8 GiB ClickHouse. — [Langfuse scaling](https://langfuse.com/self-hosting/configuration/scaling.md) (search snippet)
- **Langfuse masking:** runs in the SDK before export, so redacted values never leave the app. Python offers `mask_otel_spans` (recommended) or the legacy `mask`. JS passes a `mask` function to `LangfuseSpanProcessor`. The docs give regex examples that replace emails and phone numbers with `[REDACTED EMAIL]`/`[REDACTED PHONE]`. — [Langfuse masking](https://langfuse.com/docs/observability/features/masking)
- **OpenAI data controls:**
  - API data is not used for training unless you opt in.
  - Abuse-monitoring logs are kept up to 30 days.
  - Zero Data Retention needs approval.
  - Responses API state is kept ≥30 days by default (`store`).
  - Data residency includes **South Korea (`kr.api.openai.com`) with regional storage but not regional processing**, as do Japan, India and Singapore. Non-US regions require approval for abuse-monitoring controls.

  — [OpenAI "Your data"](https://developers.openai.com/api/docs/guides/your-data)
- **OpenAI limits and budgets:**
  - Usage tiers: Free $100/month (allowed geographies), Build ($5 paid → $500/month), Launch ($100 → $5,000/month), Grow ($500 → $200,000/month).
  - Rate limits are set per organization **and per project**.
  - Spend limits can be set per org or per project. A **spend alert** notifies while traffic continues. A **hard spend limit** returns 429 to enforce a monthly cap.

  — [OpenAI rate limits](https://developers.openai.com/api/docs/guides/rate-limits)
- Production guidance: the limits page also lets you set an email notification threshold. Use separate projects to isolate staging from production, with custom rate/spend limits per project. The usage dashboard shows token usage per billing cycle and per API key. — [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)
- **OpenAI prices (official pricing page, read 2026-10-29), per 1M tokens, standard tier:**
  - gpt-5.4-nano $0.20 in / $0.02 cached / $1.25 out.
  - gpt-5.4-mini $0.75 / $0.075 / $4.50.
  - gpt-5-nano $0.05 / $0.005 / $0.40.
  - gpt-5-mini $0.25 / $0.025 / $2.00.
  - gpt-4.1-mini $0.40 / $0.10 / $1.60.
  - gpt-4o-mini $0.15 / $0.075 / $0.60.
  - The page also lists "gpt-6-luna" ($0.10 / $0.01 / $0.50) and "gpt-5.6-luna" ($0.20 / $0.02 / $1.20).
  - Batch/Flex rates are exactly half of standard for the listed small models.
  - Embeddings: text-embedding-3-small **$0.02**, text-embedding-3-large $0.13.

  — [OpenAI API pricing](https://developers.openai.com/api/docs/pricing). The model pages for gpt-5-mini/gpt-5-nano show the same rates. — [GPT-5 mini](https://developers.openai.com/api/docs/models/gpt-5-mini), [GPT-5 nano](https://developers.openai.com/api/docs/models/gpt-5-nano) (search snippets)

### Inferences
- **Langfuse units estimate:** one explanation = 1 trace + ~2–4 observations (retrieval/embedding, generation, optional score), i.e. ~3–5 units. At ~3,000 explanations/month that's ~9k–15k units, well inside Hobby's 50k. Choose the **Japan** (closest) or EU region. Hobby's 30-day data access suits a bootcamp project. The 2-user limit means the AI-owner and one reviewer get logins.
- **Prompt logging without PII:**
  - Send Langfuse the prompt *template ID/version* and structured, de-identified inputs: trade type (도배/목공), area m², item codes, price figures, region at 시/구 level only.
  - Never send names, phone numbers, 동/호, full addresses, or uploaded image/plan URLs.
  - Apply `mask_otel_spans` regexes for Korean phone (`01[016789]-?\d{3,4}-?\d{4}`), email, and 동/호 patterns as a backstop.
  - Do the same scrubbing in the text sent to OpenAI itself, since the OpenAI-side retention (30-day abuse logs) applies to whatever is sent.
- **OpenAI controls to set now:**
  1. Projects `mitjip-dev` and `mitjip-prod`, each with its own key in Parameter Store (SecureString).
  2. A prod-project hard spend limit (e.g., $20/month) and a spend alert at ~$10.
  3. A dev-project hard limit of ~$10.
  4. Per-project rate limits on the expensive model.
  5. App-side: cache explanations per quote version (don't regenerate on every page view), and use Batch (50% off) for non-interactive bulk re-explanations.
  6. The app must handle 429s gracefully (show the cached/rule-based explanation) because the hard limit is enforced as 429.
- Korea data residency (`kr.api.openai.com`) offers storage only, not processing, and needs approval. For a bootcamp project the default US endpoint is fine if the inputs are de-identified as above.

### Gaps
- OpenAI's help-center article on project budgets returned HTTP 403, so the exact notification-threshold options (percentages vs dollar amounts) weren't confirmed beyond the docs above.
- The "gpt-6-luna"/"gpt-5.6-luna" entries were read from the official pricing page but not cross-checked against model pages. Treat model choice as a team decision.

---

## Q6. Cost controls (AWS Budgets, Cost Anomaly Detection, Free Tier alerts, tagging, Free Plan credits and the 6-month limit)

### Takeaway
All the core AWS cost guards are free:
- Budgets monitoring/notifications (first 2 action-enabled budgets free).
- Free Tier usage alerts at 85% (automatic for standalone accounts).
- Cost Anomaly Detection.
- Cost-allocation tags, which must be activated (≤24 h to appear).

The post-15-July-2025 **Free plan** gives $100 (+ up to $100 more for 5 activities) and ends at **6 months or credit exhaustion**. At that point the account is **suspended**, data kept 90 days, then erased unless upgraded to the Paid plan. So a team relying on credits must upgrade before the demo or operations period.

### Cited Findings
- **AWS Budgets:** "You can monitor and receive notifications on your budgets free of charge". The first two action-enabled budgets per month are free, then $0.10/day each. Budget reports cost $0.01 per report delivered. — [AWS Budgets pricing](https://aws.amazon.com/aws-cost-management/aws-budgets/pricing/)
- **Cost Anomaly Detection:** alerts by email or SNS (and from there to Slack, Microsoft Teams or Chime). It starts working within 24 h of setup, with individual, daily or weekly alerts. The fetched page didn't list a price. — [AWS Cost Anomaly Detection](https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/)
- **Free Tier tracking:**
  - Free Tier usage alerts email at **85%** of each service's Free Tier limit. They are automatic for individual accounts; Organizations management accounts must opt in. A "zero spend budget" template tracks 100%.
  - Free-plan accounts can monitor plan expiry, credit balance and days remaining in the console or via API, with periodic email alerts.
  - **Free-plan accounts only have Always Free offerings active.**
  - CloudWatch, SNS, SES (certain usage types), X-Ray, Route 53 health checks and Data Transfer are listed as "Always Free" trackable services.

  — [Tracking Free Tier usage](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/tracking-free-tier-usage.html)
- **Free Tier overhaul (2025-07-15):**
  - Both plans get $100 at sign-up. Five activities earn $20 each: EC2, RDS, Lambda, Bedrock, and an AWS Budgets cost budget.
  - The Free plan expires at 6 months or when credits run out. Upgrading to Paid lets unused credits be used for up to 12 months from sign-up.
  - Accounts created before 2025-07-15 stay on the legacy Free Tier (12-month and short-term trials plus always-free).
  - Alerts are sent at 50/25/10% credits remaining and 15/7/2 days left.

  — [AWS News Blog, Free Tier update](https://aws.amazon.com/blogs/aws/aws-free-tier-update-new-customers-can-get-started-and-explore-aws-with-up-to-200-in-credits); also [What's New 2025-07](https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/) (search snippet), [Neowin](https://www.neowin.net/news/aws-free-tier-overhauled-new-users-get-200-in-credits-but-theres-a-catch/) (search snippet: "6-month free trial, compared to the previous 12-month")
- **Free Tier page:** the Free plan has "Access is limited to select services". The account closes 6 months after opening or when credits run out, and "You won't be charged unless you convert to a Paid plan." The Paid plan is also eligible for up to $200 in credits. — [AWS Free Tier](https://aws.amazon.com/free/)
- **Free Tier FAQ:**
  - After the Free plan ends, "your account and projects are then suspended… AWS keeps your data for 90 days". You can restore by upgrading; otherwise the account is erased.
  - The Free plan omits services that would use up credits immediately or require hardware purchases.
  - The FAQ mentions sign-ups "in October 2026" (use the Credits page) without describing the change.
  - It is **internally inconsistent** on credit expiry: 6 months in some answers, 12 months in others.

  — [AWS Free Tier FAQs](https://aws.amazon.com/free/free-tier-faqs/)
- **Tags:** user-defined and AWS-generated cost-allocation tags must each be **activated** in the Billing console. They can take up to 24 h to appear, and can then filter Cost Explorer and reports. Don't put sensitive information in tags. — [Cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html)
- RDS snapshot charges are attributed per snapshot ARN (not the DB instance) in Cost Explorer/CUR, so Budgets filters keyed on the instance ARN won't match them. Enable copy-tags-to-snapshot. — [RDS backups: backup storage](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)

### Inferences
- **Set up on day 1 (all $0):**
  1. Monthly cost budget, e.g. **$60**, with actual 80%/100% and forecast 100% alerts to the team email and the SNS topic. This also earns the $20 Budgets activity credit on a new account.
  2. A second budget, "zero-spend until 2026-12-31", or a usage budget on EC2 `BoxUsage:t4g.small` hours to catch the t4g trial ending.
  3. Cost Anomaly Detection: a service monitor with daily-summary email, threshold ~$5.
  4. Tag policy: `Project=mitjip`, `Env=prod|dev`, `Owner=<name>` on EC2, EBS, RDS, S3, ECR and log groups; activate them in Billing; enable RDS copy-tags-to-snapshot.
  5. OpenAI hard limit (Q5), since OpenAI spend isn't visible in AWS Budgets.
- **Account-plan risk:** if 믿집 runs on a new Free-plan account, it will be **suspended at 6 months** (or earlier if credits run out). At ~$35–50/month of AWS spend, $200 of credits lasts about 4–5 months. Upgrade to the Paid plan early: credits keep applying, and there's no suspension.
- If the team account predates 2025-07-15, its legacy 12-month offers (e.g., the 750 h public IPv4 allowance; RDS 750 h on a selection of Single-AZ instances per the RDS page) would have expired by Oct 2026. Expect only Always Free plus the t4g.small trial.

### Gaps
- Cost Anomaly Detection pricing wasn't stated on the fetched page (believed free, but unverified here).
- Which services a **Free-plan** account can use (e.g., whether RDS db.t4g.micro, SES production access and Route 53 domain registration are allowed) is not listed on the fetched pages.
- Whether the t4g.small free trial applies to Free-plan accounts or stacks with credits isn't stated. The re:Post announcement returned HTTP 403.

---

## Q7. Itemised monthly cost estimate — AWS Seoul, during and after the t4g.small free trial, plus OpenAI

### Takeaway
**During the t4g.small trial (through 2026-12-31): ≈ $30 low / $41 typical / $66 high per month** (AWS ≈ $30 / $36 / $53, plus OpenAI ≈ $1 / $5 / $13). **After the trial (from 2027-01-01): ≈ $46 / $56 / $81 per month** (adds $15.18 for EC2). The fixed floor is RDS ($18.25 instance + $2.62 storage), public IPv4 ($3.65), EBS ($2.74), and the instance itself after the trial. CloudWatch and OpenAI are the variable items. The observability add-ons recommended here (Sentry Developer, Langfuse Hobby, Better Stack/UptimeRobot free, Healthchecks.io free) add **$0**.

### Cited Findings (Seoul unit prices, read 2026-10-29)
**EC2 and network**
- **EC2 t4g.small Linux on-demand: $0.0208/h.** t4g.micro $0.0104/h, t4g.medium $0.0416/h, t3.small $0.026/h. — [EC2 Seoul pricing-page JSON (2026-10-28)](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20%28Seoul%29/Linux/index.json)
- **t4g.small free trial:** "free for up to 750 hours / month until Dec 31st 2026". Surplus CPU credit charges may still apply. — [EC2 T4g page](https://aws.amazon.com/ec2/instance-types/t4/)
- Classmethod's CUR check (2026-01-07, Tokyo): a January 2026 line item showed $0.00 for `APN1-BoxUsage:t4g.small`, though the description still read "…t4g free trial ending Dec 31 2025". EBS, public IPv4 and surplus credits are **not** covered. Their estimate: ~$6.15/month for 25 GB gp3 + public IPv4 with a free instance. The 750 h is shared across an Organization. — [Classmethod DevelopersIO](https://dev.classmethod.jp/en/articles/ec2-t4g-small-free-tier-2026/); a re:Post answer notes the console may not show the free-tier label. — [re:Post](https://repost.aws/questions/QULeuz1E2tQD-wO9lB41cDDg/free-tier-t4g-small-instance-in-2025) (search snippet)
- **Public IPv4: $0.005/h**, in-use or idle (`APN2-PublicIPv4:InUseAddress`). — [Price List: VPC Seoul (2026-10-16)](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonVPC/current/ap-northeast-2/index.json). The charge applies to all public IPv4 addresses since 2024-02-01, including on RDS. The legacy EC2 Free Tier covered 750 h/month for 12 months. — [AWS blog: public IPv4 charge](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)
- **EBS gp3: $0.0912/GB-month**, extra IOPS $0.0057/IOPS-month, extra throughput $46.6944 per GiBps-month. gp2 is $0.114. **Snapshots: $0.05/GB-month.** — [EBS pricing-page JSON (2026-10-28)](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ebs.json). Data Lifecycle Manager is "at no additional cost". — [Amazon DLM](https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html)

**RDS**
- **RDS PostgreSQL db.t4g.micro Single-AZ: $0.025/h**; db.t4g.small $0.051/h; db.t3.micro $0.028/h.
- **gp3 storage: $0.131/GB-month**; extra gp3 IOPS $0.023/IOPS-month; throughput $0.091/MiBps-month.
- **Backup storage beyond the free allowance: $0.095/GB-month.**
- T4g CPU credits: $0.09/vCPU-h.

  — [Price List: RDS Seoul (2026-10-29)](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/ap-northeast-2/index.json)
- Free RDS backup storage = 100% of total provisioned DB storage per Region, applied as a percentage discount across snapshots. Manual snapshots persist after instance deletion. — [RDS backups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)

**Storage, email, DNS, registry**
- **S3 Standard: $0.025/GB-month** (first 50 TB). PUT/COPY/POST/LIST $0.0045 per 1,000; GET $0.0035 per 10,000. — [Price List: S3 Seoul (2026-10-15)](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/ap-northeast-2/index.json)
- **SES:** outbound à la carte `APN2-Recipients` **$0.0001 per email ($0.10/1,000)**. — [Price List: SES Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonSES/current/ap-northeast-2/index.json). Attachments cost $0.12/GB. **New accounts (or account-regions with no metered SES since 2025-06-01) start on the Essentials plan from 2026-07-21 at $0.16/1,000**. You can switch to à la carte at any time; the first downgrade from a defaulted Essentials plan is immediate. New customers can apply Free Tier credits; the page doesn't mention the old 3,000/month allowance. — [SES pricing](https://aws.amazon.com/ses/pricing/)
- **Route 53:** hosted zone **$0.50/month** (first 25). Standard queries $0.40 per million (first 1B). Alias queries to supported AWS resources are free. Health checks as in Q3. — [Price List: Route 53 global](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRoute53/current/index.json); [Route 53 pricing](https://aws.amazon.com/route53/pricing/). Resolver/DNS Firewall SKUs are in the Seoul file (not needed). — [Price List: Route 53 Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRoute53/current/ap-northeast-2/index.json)
- **Domain:** Route 53's domain price PDF announces new prices effective **2026-07-01**. `.com` goes from **$15.00 to $16.00/year** for registration/renewal and transfer, `.xyz` from $18 to $19. Promotional credit can't pay domain fees. — [Route 53 domain pricing PDF](https://d32ze2gidvkk54.cloudfront.net/Amazon_Route_53_Domain_Registration_Pricing_20140731.pdf)
- `.kr` and `.co.kr` are **not** in Route 53's registrable TLD list. The Asia/Oceania geographic TLDs include .jp, .sg, .in and .io, but not .kr. Route 53 DNS can still host any TLD registered elsewhere. — [Route 53 registrable TLDs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/registrar-tld-list.html)
- **ECR private storage: $0.10/GB-month.** — [Price List: ECR Seoul (2026-09-11)](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECR/current/ap-northeast-2/index.json). Same-Region ECR→EC2 transfer is $0.00. The 500 MB/month private-storage free tier is "for one year". — [ECR pricing](https://aws.amazon.com/ecr/pricing/)
- **Parameter Store:** the Seoul price list contains only paid SKUs: Advanced parameters $0.05/parameter-month, and $0.05 per 10,000 API interactions for Advanced/higher-throughput. Standard parameters at standard throughput have no billable SKU. — [Price List: SSM Seoul (2026-10-08)](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSSystemsManager/current/ap-northeast-2/index.json)
- **Data transfer out to the internet:** **$0.126/GB** for the first 10 TB "beyond the global free tier". — [Price List: Data Transfer Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSDataTransfer/current/ap-northeast-2/index.json). The free tier is 100 GB/month to the internet from AWS Regions (since 2021-12-01; excludes GovCloud/China). — [AWS blog: 100 GB free DTO](https://aws.amazon.com/blogs/aws/aws-free-tier-data-transfer-expansion-100-gb-from-regions-and-1-tb-from-amazon-cloudfront-per-month/)
- **CloudWatch and SNS:** prices as in Q1–Q3 — [Price List: CloudWatch Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/ap-northeast-2/index.json), [Price List: SNS Seoul](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonSNS/current/ap-northeast-2/index.json). (The price-list region index was used to locate the Seoul files. — [CloudWatch region index](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/region_index.json))
- **OpenAI:** rates as in Q5 — [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)

### Inferences — itemised estimate (730 h/month; my arithmetic from the unit prices above)

| Item | Assumption | Low | Typical | High |
|---|---|---:|---:|---:|
| EC2 t4g.small | on-demand after trial; **$0 until 2026-12-31** | 15.18 | 15.18 | 15.18 |
| Public IPv4 | 1 address × 730 h | 3.65 | 3.65 | 3.65 |
| EBS gp3 30 GB | 3,000 IOPS/125 MB/s baseline, no extras | 2.74 | 2.74 | 2.74 |
| EBS snapshots (DLM daily, keep 7) | billed 5 / 10 / 20 GB incremental | 0.25 | 0.50 | 1.00 |
| RDS db.t4g.micro Single-AZ | 730 h | 18.25 | 18.25 | 18.25 |
| RDS gp3 20 GB | | 2.62 | 2.62 | 2.62 |
| RDS backup beyond free 20 GB | 0 / 0 / 10 GB of manual snapshots | 0.00 | 0.00 | 0.95 |
| RDS CPU credit surplus | normally 0 at this load | 0 | 0 | (spiky) |
| S3 | 1 / 5 / 20 GB + requests | 0.04 | 0.28 | 1.00 |
| SES (à la carte) | 500 / 2,000 / 5,000 mails | 0.05 | 0.20 | 0.50 |
| CloudWatch Logs ingestion | 2 / 8 / 20 GB (5 GB free) at $0.76 | 0.00 | 2.28 | 11.40 |
| CloudWatch Logs storage | 30-day retention | 0.00 | 0.25 | 0.63 |
| CloudWatch custom metrics | ≤10 free / 15 / 25 | 0.00 | 1.50 | 4.50 |
| CloudWatch alarms | ≤10 free / 15 / 20 | 0.00 | 0.50 | 1.00 |
| CloudWatch dashboards | ≤3 free | 0 | 0 | 0 |
| Route 53 hosted zone + queries | | 0.52 | 0.55 | 0.90 |
| Route 53 health check (optional) | none / HTTPS / HTTPS+string | 0.00 | 1.00 | 2.00 |
| Domain .com | $16/yr on Route 53 | 1.33 | 1.33 | 1.33 |
| ECR | 0.5 / 2 / 5 GB (lifecycle policy keeps last N images) | 0.05 | 0.20 | 0.50 |
| Data transfer out | < 100 GB/month free | 0 | 0 | 0 |
| Parameter Store (Standard) / SNS email / Budgets / Anomaly Detection / DLM | free tiers | 0 | 0 | 0 |
| OpenAI | 3,000 explanations × (2,000 in + 600 out) tokens = 6M in / 1.8M out; gpt-5-nano / gpt-5-mini / gpt-5.4-mini; embeddings ~$0.04 | 1.02 | 5.10 | 12.60 |
| **Total, after trial (2027-01+)** | | **≈ 45.7** | **≈ 56.1** | **≈ 80.8** |
| **Total, during trial (EC2 $0)** | | **≈ 30.5** | **≈ 41.0** | **≈ 65.6** |
| AWS only, during trial | | ≈ 29.5 | ≈ 35.9 | ≈ 53.0 |
| AWS only, after trial | | ≈ 44.7 | ≈ 51.0 | ≈ 68.2 |

Notes on the estimate (inferences):
- Other OpenAI model choices for the same 6M/1.8M tokens: gpt-5.4-nano ≈ $3.45, gpt-4.1-mini ≈ $5.28. Batch halves any of these for non-interactive work.
- Optional paid add-ons, if chosen:
  - Sentry Team: $26–29/month.
  - Langfuse Core: $29/month.
  - Database Insights Advanced: ≈ $18.25/month (2 vCPU × 730 × $0.0125).
  - Standard-mode DI retention beyond 7 days: ≈ $3.5/month for the first month of retention.
  - One CloudWatch Synthetics canary: ≈ $16.45/month at 5-minute intervals or $5.36 at 15-minute, plus Lambda/S3/logs.
  - Upgrading RDS to db.t4g.small: +$18.98/month ($37.23 vs $18.25).
  - Upgrading EC2 to t4g.medium if memory is short: $30.37/month vs $15.18.
- **Biggest controllable levers:**
  - Logs volume: drop health-check access logs and debug logs, and keep retention short. Each 1 GB over the free 5 GB costs $0.76.
  - The agent metric count: keep it ≤10 (the EC2 Health default config of 22 metrics alone would cost ~$3.6).
  - Not adding Synthetics or DI Advanced.
  - Explanation caching and the OpenAI hard limit.
- Making RDS publicly accessible would add another $3.65/month for its public IPv4. Keep it private (EC2 → RDS in the same VPC).
- New Free-plan credits ($100–200) can cover roughly 3–5 months of the typical AWS bill. Don't count on them beyond the 6-month plan window (see Q6).
- Switch SES to à la carte if the account was defaulted to Essentials ($0.16 vs $0.10 per 1,000). Immaterial at this volume (cents), but worth knowing.

### Gaps
- `.kr`/`.co.kr` registration prices from Korean registrars (e.g., 가비아) weren't researched; the search budget was exhausted.
- KRW conversion and Korean VAT treatment of AWS invoices weren't researched.
- Actual OpenAI token volumes per explanation are assumptions. Replace them with measured numbers from the OpenAI usage dashboard and Langfuse after a week of use.
- Seoul prices for Lambda (if a Discord relay Lambda is used) weren't pulled; within the Always Free allowance the cost is presumably $0.
- No 2025–2026 Korean blog with a real small-AWS cost breakdown was found before the search budget ran out. The only real-bill evidence is Classmethod's Tokyo CUR article.

---

## Q8. Operational artefacts to add (runbook, status page, on-call/alert rules, backup-restore drill, dashboards)

### Takeaway
A student team can be operationally credible with six small artefacts:
1. A one-page **alert rules table** (alarm → threshold → severity → who → first action).
2. A **runbook** covering ~8 failure scenarios.
3. A free **public status page** from the uptime tool.
4. A lightweight **on-call rota** (business hours, weekly).
5. A dated **RDS PITR + EBS snapshot restore drill**.
6. One **CloudWatch dashboard** (free tier) plus the Sentry and Langfuse views.

All can be built from features already covered above at $0.

### Cited Findings
- RDS automated backups: point-in-time recovery to any point in the retention period, PITR works across all storage volumes, and the first snapshot is full with later ones incremental. If "Retain automated backups" isn't selected at deletion, the automated backups are deleted with the instance. Manual and final snapshots are independent. — [RDS backups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)
- Data Lifecycle Manager automates EBS snapshot and AMI creation, retention and deletion "at no additional cost". It can't manage snapshots created by other means. — [Amazon DLM](https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html)
- CloudWatch gives 3 free dashboards of up to 50 metrics each; extra dashboards cost $3/month. — [CloudWatch pricing page](https://aws.amazon.com/cloudwatch/pricing/), [Price List: CloudWatch global](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/index.json)
- AWS's EC2 Health solution ships a prebuilt dashboard template (CPU, disk, memory, network). Previewing in the console before saving avoids charges. — [CloudWatch solution: EC2 health](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Solution-EC2-Health.html)
- Free status pages: UptimeRobot Free includes 1 basic status page — [UptimeRobot pricing](https://uptimerobot.com/pricing/). Better Stack Free includes a status page — [Better Stack Uptime](https://betterstack.com/uptime). Uptime Kuma supports multiple status pages on custom domains (self-hosted) — [Uptime Kuma](https://github.com/louislam/uptime-kuma).
- Grafana Cloud Free includes IRM/on-call scheduling for 3 active users if a real on-call tool is wanted. — [Grafana Cloud pricing](https://grafana.com/pricing/)
- The arq `--check` CLI exits 0/1 based on the worker health key in Redis. The key is written every `health_check_interval` (default 3,600 s), so it can back a cron heartbeat or a `/health/ready` sub-check. — [arq docs](https://arq-docs.helpmanual.io/)
- OpenAI hard spend limits return 429 when reached, so the app needs a degraded mode. — [OpenAI rate limits](https://developers.openai.com/api/docs/guides/rate-limits)

### Inferences
- **Alert rules table** (`docs/ops/alerts.md`): one row per alarm from Q2 and Q3, giving the CloudWatch name, threshold, evaluation, severity (P1/P2/P3), channel (Discord/Slack + email / channel only / email), owner, and runbook link. Review it whenever an alarm fires falsely twice.
- **Runbook** (`docs/ops/runbook.md`), with diagnosis commands via SSM Session Manager (no SSH keys):
  1. Site down: check Caddy, then `docker compose ps`, then the host.
  2. `/health/ready` failing on DB: RDS status, connections, credits.
  3. `/health/ready` failing on Redis.
  4. Memory pressure or OOM kills: `docker stats`; restart order; consider t4g.medium.
  5. Disk > 80%: `docker system prune`, check the log driver, EBS resize.
  6. CPU credits exhausted or surplus charges.
  7. OpenAI 429/outage: confirm the fallback to cached explanations; check the hard limit.
  8. SES bounce/complaint spike.
  9. Bad deploy rollback: redeploy the previous ECR image tag from GitHub Actions.
  10. Secret leak: rotate in Parameter Store and redeploy.
  11. Restore from backup (link the drill doc).
- **Backup-restore drill** (once before the demo, then monthly): RDS PITR to a new instance `mitjip-restore-test`, connect, run row-count/checksum queries on key tables, record RTO/RPO, delete the instance. Also restore the latest DLM EBS snapshot to a volume, mount it on a temp instance, and confirm `.env`/compose files. A 1-hour db.t4g.micro test costs ~$0.03. Keep the dated record in `docs/ops/restore-drills.md`.
- **On-call:** weekly rotation among 3–4 students, 09:00–23:00 KST best-effort, with a named backup. P1 acknowledged within 30 min during on-call hours. Write a 5-line postmortem (what, impact, cause, fix, follow-up) for every P1.
- **Dashboard** (`mitjip-prod`, 1 of the 3 free), with widgets:
  - EC2: CPUUtilization, CPUCreditBalance, CPUSurplusCreditBalance, mem_used_percent, disk_used_percent.
  - RDS: CPU, CPUCreditBalance, DatabaseConnections, FreeableMemory, FreeStorageSpace, Read/WriteLatency.
  - Logs: 5xx count (metric filter), plus a Logs Insights widget of top error messages.
  - SES: Bounce/Complaint rate.
  - Cost: EstimatedCharges (us-east-1 billing metric).

  Add links to Sentry, Langfuse, Better Stack and the OpenAI usage page.
- **Also add:**
  - A logging and PII policy page (Q1 rules).
  - A cost review checklist: weekly, 5 minutes, covering Cost Explorer by tag, the OpenAI usage page, and the remaining Free Tier credits.
  - An "end-of-trial" calendar reminder for 2026-12-15: decide whether to keep t4g.small (+$15.18/month from 2027-01-01) or move to a smaller or Savings-Plan option.

### Gaps
- No Korean-language sources on student or startup incident-response practice were consulted (search budget exhausted).

---

## Source register (every URL consulted; all read/fetched 2026-10-29)

### Takeaway
89 distinct URLs were consulted: 17 AWS Price List / pricing-JSON files (official machine-readable Seoul prices) and 72 web pages or docs. Pages marked "(snippet)" were only seen as search-result summaries. Four fetches failed (help.openai.com 403, re:Post t4g announcement 403, law.go.kr JS shell, uvicorn.org DNS failure).

### Cited Findings
**AWS Price List API / pricing JSON (official, Seoul unless noted)**
1. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/region_index.json
2. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/ap-northeast-2/index.json
3. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/index.json (global)
4. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-northeast-2/index.json
5. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/ap-northeast-2/index.json
6. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/ap-northeast-2/index.json
7. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonSES/current/ap-northeast-2/index.json
8. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECR/current/ap-northeast-2/index.json
9. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRoute53/current/index.json (global)
10. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRoute53/current/ap-northeast-2/index.json
11. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSXRay/current/ap-northeast-2/index.json
12. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonVPC/current/ap-northeast-2/index.json
13. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSSystemsManager/current/ap-northeast-2/index.json
14. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSDataTransfer/current/ap-northeast-2/index.json
15. https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonSNS/current/ap-northeast-2/index.json
16. https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20%28Seoul%29/Linux/index.json
17. https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ebs.json

**AWS pages and docs**
18. https://aws.amazon.com/ec2/instance-types/t4/
19. https://dev.classmethod.jp/en/articles/ec2-t4g-small-free-tier-2026/
20. https://repost.aws/questions/QULeuz1E2tQD-wO9lB41cDDg/free-tier-t4g-small-instance-in-2025 (snippet)
21. https://repost.aws/articles/ARbeHG--bbT6mXw38WgSz01w/announcing-amazon-ec2-t4g-free-trial-extension (fetch failed, 403)
22. https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/ (snippet)
23. https://aws.amazon.com/blogs/aws/aws-free-tier-update-new-customers-can-get-started-and-explore-aws-with-up-to-200-in-credits
24. https://aws.amazon.com/free/
25. https://aws.amazon.com/free/free-tier-faqs/
26. https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/tracking-free-tier-usage.html
27. https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html
28. https://aws.amazon.com/aws-cost-management/aws-budgets/pricing/
29. https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/
30. https://aws.amazon.com/chatbot/pricing/
31. https://aws.amazon.com/cloudwatch/pricing/
32. https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Solution-EC2-Health.html
33. https://repost.aws/knowledge-center/cloudwatch-memory-metrics-ec2 (snippet)
34. https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html
35. https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html
36. https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html
37. https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Database-Insights.html
38. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_DatabaseInsights.Engines.html
39. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.Overview.md (snippet)
40. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html
41. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html
42. https://aws.amazon.com/rds/postgresql/pricing/
43. https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances-unlimited-mode-concepts.html
44. https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html
45. https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html
46. https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/
47. https://aws.amazon.com/blogs/aws/aws-free-tier-data-transfer-expansion-100-gb-from-regions-and-1-tb-from-amazon-cloudfront-per-month/
48. https://aws.amazon.com/ses/pricing/
49. https://aws.amazon.com/ecr/pricing/
50. https://aws.amazon.com/route53/pricing/
51. https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/registrar-tld-list.html
52. https://d32ze2gidvkk54.cloudfront.net/Amazon_Route_53_Domain_Registration_Pricing_20140731.pdf
53. https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-migration.html
54. https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_LogConfiguration.html (snippet)
55. https://www.doit.com/blog/transitioning-from-rds-performance-insights-to-cloudwatch-database-insights (snippet)
56. https://www.neowin.net/news/aws-free-tier-overhauled-new-users-get-200-in-credits-but-theres-a-catch/ (snippet)

**Logging and instrumentation**
57. https://docs.docker.com/engine/logging/drivers/awslogs/
58. https://docs.docker.com/engine/logging/configure/
59. https://docs.fluentbit.io/manual/pipeline/outputs/cloudwatch
60. https://www.structlog.org/en/stable/
61. https://caddyserver.com/docs/caddyfile/directives/log
62. https://arq-docs.helpmanual.io/
63. https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
64. https://nextjs.org/docs/app/guides/open-telemetry
65. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
66. https://www.uvicorn.org/settings/ (fetch failed, DNS)

**Error tracking, uptime, observability SaaS**
67. https://sentry.io/pricing/
68. https://docs.sentry.io/platforms/python/data-management/sensitive-data/
69. https://last9.io/blog/sentry-pricing/ (snippet)
70. https://agentdeals.dev/vendor/sentry (snippet)
71. https://glitchtip.com/pricing
72. https://uptimerobot.com/pricing/
73. https://notifier.so/guides/uptimerobot-pricing-2026/ (snippet)
74. https://dev.to/velprove/uptimerobot-commercial-use-free-alternatives-for-business-sites-in-2026-5d75 (snippet)
75. https://betterstack.com/pricing
76. https://betterstack.com/uptime
77. https://healthchecks.io/pricing/
78. https://github.com/louislam/uptime-kuma
79. https://grafana.com/pricing/
80. https://docs.discord.com/developers/resources/webhook
81. http://developers.kakao.com/docs/ko/kakaotalk-message/common

**LLM observability and OpenAI**
82. https://langfuse.com/pricing.md
83. https://langfuse.com/self-hosting
84. https://langfuse.com/self-hosting/deployment/docker-compose
85. https://langfuse.com/self-hosting/configuration/scaling.md (snippet)
86. https://langfuse.com/docs/observability/features/masking
87. https://developers.openai.com/api/docs/pricing
88. https://developers.openai.com/api/docs/models/gpt-5-mini (snippet); https://developers.openai.com/api/docs/models/gpt-5-nano (snippet)
89. https://developers.openai.com/api/docs/guides/your-data; https://developers.openai.com/api/docs/guides/rate-limits; https://developers.openai.com/api/docs/guides/production-best-practices
(also attempted: https://help.openai.com/en/articles/9186755-managing-your-work-in-the-api-platform-with-projects — 403; https://www.law.go.kr/행정규칙/개인정보의안전성확보조치기준 — content not rendered)

### Inferences
- The AWS Price List files are the most reliable Seoul source. Marketing pages frequently show us-east-1 example rates that understate Seoul: logs $0.50 vs $0.76/GB, canary $0.0012 vs $0.0019/run, and the RDS credit price $0.075 vs $0.09.

### Gaps
- The search budget ran out before Korean-language cost blogs, `.kr` registrar pricing and the PIPA 접속기록 rule could be sourced. These are the main items to verify manually.
