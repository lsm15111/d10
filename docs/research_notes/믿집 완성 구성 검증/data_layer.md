# 믿집 data layer: RDS PostgreSQL 17, Redis on the app host, arq job queue (checked 2026-10-29)

Scope: RDS for PostgreSQL (instance sizing, backups, parameters, security, versions, pgvector, Korean search), Redis/Valkey on the EC2 host, the job queue (arq and alternatives), sessions and pooling, and what else the data layer needs. Region: ap-northeast-2 (Seoul). Seoul prices come from third-party aggregators because the AWS pricing page did not render Seoul tables for the fetch tool. Treat them as approximate and confirm in the AWS Pricing Calculator.

Note on research limits: the shared web-search budget ran out partway through. Later facts came from fetching known primary pages directly. Some items are therefore listed under Gaps rather than verified. These include Seoul gp3 and backup storage prices, Celery/Dramatiq status, a Korean-language RDS operations blog, and arq-specific bug reports.

---

## 1. RDS PostgreSQL db.t4g.micro (1 GiB) vs db.t4g.small (2 GiB): memory, max_connections, CPU credits, storage, Seoul prices, free tier/credits

### Takeaway
db.t4g.micro can handle tens of concurrent users and about 30 pooled connections. It is tight on memory: about 250 MB of shared_buffers, no headroom for IAM auth, and a small margin for HNSW builds and monitoring. Its sustained CPU baseline is only 10% per vCPU, and its EBS baseline is 500 IOPS. In Seoul it costs about $18/month on-demand, against about $37/month for db.t4g.small. A sensible plan is micro for dev/staging and the early demo, with an alarm-driven move to db.t4g.small (or starting there if the budget allows) once FreeableMemory or CPUCreditBalance shows pressure. Both classes always run in Unlimited CPU-credit mode on RDS, so sustained bursting adds $0.075 per vCPU-hour instead of throttling.

### Cited Findings
- Default RDS PostgreSQL `max_connections` = `LEAST({DBInstanceClassMemory/9531392}, 5000)`. `DBInstanceClassMemory` already subtracts memory reserved for the OS and RDS processes, so the real value is lower than raw GiB ÷ 9.53 MB. The allowed range is 6–262143. AWS warns that a value set too high can push the instance into `incompatible-parameters` status — [RDS quotas: Maximum number of database connections](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html)
- AWS recommends RDS Proxy when apps "frequently open and close connections, or keep a large number of long-lived connections open" — [RDS quotas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html)
- `shared_buffers` default = `{DBInstanceClassMemory/32768}`. AWS labels the unit "bytes". A practitioner guide reads it as 8 kB pages, which works out to about 25% of instance memory. The units conflict between sources, and the 25% reading is the standard interpretation. Default `work_mem` = 4 MB, `maintenance_work_mem` = 64 MB, `temp_buffers` = 8 MB. Total work memory can be "multiples of the work_mem setting" across sessions — [RDS for PostgreSQL memory](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Tuning.concepts.memory.html); [StackHarbor parameter-group tuning](https://stackharbor.com/en/knowledge-base/awsrds-parameter-group-tuning/)
- "Amazon RDS db.t4g instances are configured for Unlimited mode. This means that they can burst beyond the baseline over a 24-hour window for an additional charge" — [RDS DB instance class types (burstable)](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.Types.html)
- T4g/T3 CPU credits cost $0.075 per vCPU-hour, the same in all regions — [RDS for PostgreSQL pricing](https://aws.amazon.com/rds/postgresql/pricing/)
- Credit math for the underlying T4g sizes: t4g.micro has 2 vCPU, earns 12 credits/hour, accrues at most 288, and has a 10% baseline per vCPU. t4g.small has 2 vCPU, earns 24 credits/hour, accrues at most 576, and has a 20% baseline per vCPU. Unlimited mode bills when the 24-hour average exceeds baseline — [EC2 burstable credit concepts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html)
- db.t4g.micro specs: 2 vCPU and 1 GiB on Graviton2, network up to 5 Gbps. EBS baseline is 87 Mbps / 10.875 MB/s / 500 IOPS, burstable to 2,085 Mbps / 11,800 IOPS. PostgreSQL 12–18 is supported. The headline (us-east-1) price is $0.016/h on-demand and $0.012/h on a 1-year RI — [Vantage instances: db.t4g.micro](https://instances.vantage.sh/aws/rds/db.t4g.micro)
- Seoul (ap-northeast-2) PostgreSQL db.t4g.micro: $18/month on-demand (≈$0.025/h at 730 h), $14/month effective on a 1-year RI, $9/month on a 3-year RI. These are compute only; storage, IOPS and backup are extra. The page states no update date — [Bytebase dbcost: db.t4g.micro](https://www.bytebase.com/dbcost/rds/instance/db.t4g.micro.md)
- Seoul PostgreSQL db.t4g.small: $37/month on-demand (≈$0.051/h), $27/month on a 1-year RI, $18/month on a 3-year RI. Specs are 2 vCPU, 2 GiB, Graviton2 — [Bytebase dbcost: db.t4g.small](https://www.bytebase.com/dbcost/rds/instance/db.t4g.small.md)
- Spare Cores lists Seoul db.t4g.micro at $0.051/h for a multi-AZ (standby) deployment. That is about twice the single-AZ rate and consistent with the Bytebase figure — [Spare Cores: db.t4g.micro](https://sparecores.com/database/aws/db.t4g.micro)
- A third-party catalogue also states that db.t4g is configured for Unlimited mode — [Aiven: db.t4g.micro](https://aiven.io/tools/instances/db.t4g.micro)
- gp3 on RDS PostgreSQL ranges from 20 GiB to 65,536 GiB. Volumes of 20–399 GiB get a baseline of 3,000 IOPS and 125 MiB/s with no extra provisioning possible. At 400 GiB or more, the volume is striped across 4 volumes at 12,000 IOPS and 500 MiB/s. "DB instances that use General Purpose storage can experience much longer latency" after certain operations. db.t4g.micro maxes out at 6 TiB of PostgreSQL storage, and db.t4g.small at 16 TiB. Magnetic storage is deprecated, and from 2026-07-01 snapshots can no longer be restored to it — [RDS DB instance storage](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html)
- The instance's own EBS limit caps storage performance ("the maximum IOPS rate is enforced at the DB instance level") — [RDS DB instance storage](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html)
- The only gp3 price found is a US reference: $0.115/GB-month for RDS gp3 Single-AZ in us-east-1 (June 2026). No Seoul figure was found — [usage.ai RDS storage cost](https://www.usage.ai/blogs/aws/reserved-instances/rds/storage-cost/)
- Free tier for new accounts: accounts opened on or after 2025-07-15 get $100 in credits at sign-up plus up to $100 more from onboarding tasks, one of which uses RDS. Customers pick the Free Plan or the Paid Plan at sign-up — [AWS What's New, Mar 2026 (Aurora PostgreSQL on Free Tier)](https://aws.amazon.com/about-aws/whats-new/2026/03/amazon-aurora-postgresql-aws-free-tier); [AWS ElastiCache pricing page, Free Tier note](https://aws.amazon.com/elasticache/pricing/)
- Per third-party summaries, the Free Plan lasts six months or until the $200 is spent, whichever comes first, and credits expire 12 months after account opening. RDS and EC2 usage draws down the credit balance; there is no separate free-hours allowance. The legacy 750 h/month of a micro RDS instance applies only to accounts opened before 2025-07-15 — [InfraTally: AWS Free Tier 2026](https://infratally.com/articles/aws-free-tier-2026/); [Tech Insider: What changed in the AWS Free Tier for 2026](https://tech-insider.org/what-changed-in-the-aws-free-tier-for-2026/)

### Inferences
- Connection budget: FastAPI runs 2 uvicorn workers × (pool_size 5 + max_overflow 5) = 20 at peak. One arq worker process × 10 = 10. Alembic adds 1, and psql/admin plus pg_cron add 2–4. Peak is about 31–35. Even the raw formula ceiling for 1 GiB (1,073,741,824 / 9,531,392 ≈ 112, lower in practice) leaves room, so RDS Proxy and PgBouncer are unnecessary at this scale.
- Memory, not connections, is the binding constraint on micro. About 25% of roughly 0.8–0.9 GiB usable goes to shared_buffers. Each of 30+ backends adds a few MB, plus work_mem per sort or hash node. HNSW builds use maintenance_work_mem (64 MB default). That is workable but leaves little slack. On db.t4g.small the same workload has about 2× headroom.
- CPU: 10% × 2 vCPU equals about 0.2 vCPU sustained on micro, and the 288-credit bank covers bursts of about 2.4 vCPU-hours. A deterministic calc engine and CRUD for tens of users should stay under that. Migrations, index builds, and pgvector rebuilds will burst. Unlimited mode bills rather than throttles, so set alarms on `CPUSurplusCreditBalance` and `CPUCreditBalance`.
- On micro, the 500 IOPS instance EBS baseline rather than gp3's 3,000 IOPS sets sustained I/O, though bursts reach 11,800 IOPS. This matters for restores, which lazy-load from S3, and for vacuum and bulk loads.
- Rough monthly data-tier cost in Seoul, single-AZ, 20 GiB gp3 assuming a Seoul rate near the $0.115–0.13 US reference: micro ≈ $18 + about $2.5 storage ≈ $20–21. Small ≈ $37 + $2.5 ≈ $40. Multi-AZ roughly doubles both. A 1-year RI saves about 22–27%, but a bootcamp project rarely runs 12 months, so on-demand is the right default.
- The $100–200 credit covers the RDS bill for the project's life. A Free Plan account has a six-month cap, so check the plan type before the demo date.

### Gaps
- Exact AWS-published Seoul hourly rates for db.t4g.micro and db.t4g.small (Single-AZ and Multi-AZ). The AWS pricing tables did not render, and the Bytebase page has no date.
- Seoul gp3 GB-month price, and the actual `max_connections` value shown on a db.t4g.micro or small (only the formula is documented).
- The db.t4g.small EBS baseline IOPS and throughput (not fetched).

---

## 2. Automated backups, PITR, backup storage cost, snapshot export to S3, restore drills, when Multi-AZ is worth it

### Takeaway
Set backup retention explicitly to 7–14 days. The API/CLI default is only 1 day, and changing to or from 0 causes an outage. Backup storage up to 100% of provisioned storage is free, so a 20 GiB instance with about 7–14 days of a small dataset costs about $0 in backups. PITR has about 5-minute granularity and always restores into a new instance with the default parameter group unless you pass one. A restore drill must re-attach the custom parameter group and security group. Snapshot export to S3 produces Parquet for analytics, not a restorable backup. Multi-AZ is roughly 2× the instance cost and only lifts the SLA from 99.5% to 99.95%. It can be switched on later with a modify, so leaving it off now is reasonable.

### Cited Findings
- Retention is 0–35 days. The default is 7 days when created in the console and 1 day via API/CLI. 0 disables automated backups. "An outage occurs if you change the backup retention period … from 0 to a nonzero value or from a nonzero value to 0" — [RDS backup retention period](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html)
- Time spent stopped doesn't count toward retention, and no automated backups are taken while stopped — [RDS backup retention period](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html)
- Free backup storage equals 100% of total provisioned DB storage per account per region, applied as a percentage discount across all snapshots. The first snapshot is full and later ones are incremental. Unless you choose "Retain automated backups", deleting an instance deletes its automated backups. Manual and final snapshots persist and keep billing. There is a limit of 100 manual snapshots per region — [RDS introduction to backups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)
- Backup storage price: one undated NetApp blog cites $0.095/GB-month for Seoul. That figure is for AWS Backup warm storage and may be stale. Billing-code pages confirm the Seoul line item `APN2-RDS:ChargedBackupUsage` exists but give no price — [NetApp backup pricing blog](https://www.netapp.com/ko/blog/understanding-backup-pricing-aws-cvo-blg/); [Vantage CUR: APN2-RDS:ChargedBackupUsage](https://cur.vantage.sh/aws/amazonrds/storage%20snapshot/apn2-rds:chargedbackupusage)
- PITR: "RDS uploads transaction logs for DB instances to Amazon S3 every five minutes". `LatestRestorableTime` shows the newest restorable point. A restore creates a new instance whose volumes "continue to load data blocks from Amazon S3 in the background", with reduced performance until initialization finishes. "Restored DB instances are automatically associated with the default DB parameter and option groups" unless you specify otherwise via CLI/API. Storage can't be reduced on restore — [RDS restore to a point in time](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html)
- Snapshot export to S3 writes compressed Parquet for Athena or Redshift Spectrum. "You can't restore exported snapshot data from S3 to a new DB instance". It requires a KMS key and allows up to 5 concurrent exports per account. Unlogged and temp tables are skipped — [Exporting DB snapshot data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ExportSnapshot.html)
- Snapshot export is billed per GB of snapshot size ($0.013/GB in the US East example) — [RDS for PostgreSQL pricing](https://aws.amazon.com/rds/postgresql/pricing/)
- Multi-AZ instance deployment keeps a synchronous standby in another AZ that "can't [be used] to serve read traffic". It may increase write and commit latency. Existing instances can be converted by modifying the instance with the Multi-AZ option — [Multi-AZ DB instance deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html)
- In Multi-AZ, OS patches are applied standby-first, followed by a failover that "typically lasts less than a minute". An engine version upgrade still takes primary and standby down together — [Maintaining a DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html)
- The SLA targets 99.95% monthly uptime for Multi-AZ and 99.5% for a Single-DB instance, with service credits tiered below those — [Amazon RDS SLA](https://aws.amazon.com/rds/sla/)
- Seoul Multi-AZ db.t4g.micro is about $0.051/h, roughly 2× single-AZ — [Spare Cores: db.t4g.micro](https://sparecores.com/database/aws/db.t4g.micro)

### Inferences
- Recommended settings: `BackupRetentionPeriod=7` (or 14), set explicitly in IaC/CLI. Set a preferred backup window in low traffic, for example 18:00–18:30 UTC (03:00 KST), that does not overlap the maintenance window. Turn on deletion protection and a final snapshot on delete. Take a manual snapshot before every risky migration or major upgrade.
- Restore drill, once before launch and then about monthly: (1) restore to a point in time as `mitjip-restore-test` with the custom parameter group, the same subnet group and SG, and db.t4g.micro. (2) Run row-count and checksum queries on key tables (users, quotes, jobs, sessions). (3) Point a staging FastAPI at it and run smoke tests. (4) Delete it. Record RTO, which is roughly instance-creation time plus lazy load, and RPO of about 5 minutes or less.
- 99.5% allows about 3.6 h/month of downtime, and 99.95% about 22 min/month. For a student project with tens of users, the extra ~$18–37/month for Multi-AZ isn't justified. It becomes worth it when there are real paying vendors or customers, or a contractual uptime promise, or when the team can no longer accept 10–30 min of downtime during maintenance or AZ incidents. It is a one-click modify later.
- Optional: export a monthly snapshot to S3 Parquet only if analytics on historical quotes is needed. It is not part of DR.

### Gaps
- Official Seoul backup storage $/GB-month (AWS page not rendered).
- Measured restore time for a small (<5 GB) gp3 instance (no source).

---

## 3. Parameter group settings, TLS from asyncpg, IAM DB auth, encryption at rest, network placement, RDS Proxy

### Takeaway
Create a custom parameter group before creating the instance. Applying one later needs a reboot, and restores fall back to the default group. `rds.force_ssl` already defaults to 1 on PG 15+. asyncpg defaults to `ssl='prefer'`, so pass `ssl='verify-full'` with the RDS global CA bundle. Skip IAM DB auth: AWS says it needs 300–1000 MiB of extra DB memory, which a 1 GiB micro does not have. Encryption at rest must be chosen at creation (`--storage-encrypted`), and the free `aws/rds` key is fine. Place the instance in private subnets with no public access and an SG that allows 5432 only from the EC2 SG. RDS Proxy is unnecessary for about 3 processes and roughly 35 connections.

### Cited Findings
- `rds.force_ssl` defaults to 1 for RDS PostgreSQL 15 and later. Changing it requires a custom parameter group, plus a reboot if the group is attached after creation. Non-SSL clients get `FATAL: no pg_hba.conf entry … SSL off`. TLS 1.1/1.2 are supported and TLS 1.3 on PG 16+. `ssl_min_protocol_version` shows TLSv1.2. Use `sslmode=verify-full` with `sslrootcert` pointing to the RDS CA. RDS PG 18 also lets you set `ssl_tls13_ciphers` and `ssl_groups`, including ML-KEM hybrids — [Using SSL with a PostgreSQL DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html)
- asyncpg `connect(ssl=...)` accepts `True`, an `SSLContext`, or `'disable'|'prefer'|'allow'|'require'|'verify-ca'|'verify-full'`. "The default is 'prefer'". `sslrootcert` is a recognized DSN option, defaulting to files under `~/.postgresql/` as libpq does. "Default system root CA certificates won't be loaded when specifying a particular sslmode". `statement_cache_size` defaults to 100 and `max_cached_statement_lifetime` to 300 s — [asyncpg API reference](https://magicstack.github.io/asyncpg/current/api/index.html)
- IAM DB auth tokens last 15 minutes, and the token only authenticates the connection. "IAM DB authentication requires compute resources … You must have between 300 and 1000 MiB extra memory on your database for reliable connectivity". On burstable classes, reduce other memory parameters to compensate. Once `rds_iam` is granted, IAM auth takes precedence over password auth. CloudTrail doesn't log `generate-db-auth-token` — [IAM database authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
- Encryption at rest uses AES-256 and covers storage, logs, automated backups, read replicas, and snapshots. "You can only encrypt an Amazon RDS DB instance when you create it". To add it later you copy a snapshot with encryption and restore, or use blue/green. Without a customer key, RDS uses the AWS managed key. Disabling the KMS key makes the instance inaccessible. T2.micro is the only burstable class listed as unsupported, so T4g is supported — [Encrypting Amazon RDS resources](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html)
- `idle_in_transaction_session_timeout`: AWS recommends configuring it in the parameter group so long idle transactions end without manual intervention. The log shows `FATAL: terminating connection due to idle in transaction timeout` — [RDS DevOps Guru proactive insights for PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Tuning_proactive_insights.html)
- PG 17 timeouts all default to 0 (disabled), in ms: `statement_timeout`, `transaction_timeout` (new in 17), `lock_timeout`, `idle_in_transaction_session_timeout`, `idle_session_timeout`. The docs say "Setting statement_timeout in postgresql.conf is not recommended because it would affect all sessions", and give the same warning for `lock_timeout` and `transaction_timeout`. "An open transaction prevents vacuuming away recently-dead tuples … can contribute to table bloat". On `idle_session_timeout`: "Be wary of enforcing this timeout on connections made through connection-pooling software" — [PostgreSQL 17: Client connection defaults](https://www.postgresql.org/docs/17/runtime-config-client.html)
- `idle_in_transaction_session_timeout` measures each idle gap, not total transaction time. `transaction_timeout` (PG 17) bounds the total — [thebuild.com: idle_in_transaction_session_timeout](https://thebuild.com/blog/all-your-gucs-in-a-row-idle_in_transaction_session_timeout/)
- Even with both statement_timeout and idle_in_transaction set, transactions made of short statements with intermittent waits can live long — [Chat2DB: statement timeout in PostgreSQL](https://chat2db.ai/resources/blog/statement-timeout-in-postgresql)
- RDS logs capture login failures, fatal errors, deadlocks, and query failures by default. Logs can be published to CloudWatch Logs under `/aws/rds/instance/<id>/postgresql`, which allows things like alarms on DDL with `log_statement=ddl`. Only new logs are uploaded after you enable it — [RDS for PostgreSQL database log files](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Concepts.PostgreSQL.html)
- RDS Proxy is priced per vCPU-hour for provisioned RDS PostgreSQL, billed per second with a 10-minute minimum — [RDS Proxy pricing](https://aws.amazon.com/rds/proxy/pricing/)
- The AWS China price table lists a 2-vCPU minimum. A third-party guide estimates about $21.90/month at the minimum in the US ($0.015/vCPU-h × 2) — [AWS China RDS Proxy pricing](https://amazonaws.cn/en/rds/proxy/pricing); [usage.ai RDS Proxy cost](https://www.usage.ai/blogs/aws/reserved-instances/rds/proxy-cost/)
- SQLAlchemy asyncpg: the prepared statement cache holds 100 statements per DBAPI connection (`prepared_statement_cache_size`). Behind PgBouncer-style proxies, use `prepared_statement_name_func` and `NullPool`. After DDL from another process, asyncpg may raise `InvalidCachedStatementError` or "cache lookup failed for type". The dialect clears its cache but cannot retry, "because the PostgreSQL transaction is invalidated" — [SQLAlchemy 2.0 PostgreSQL dialect (asyncpg section)](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)

### Inferences
- Suggested custom parameter group `mitjip-pg17` (or `-pg18`) for a 1–2 GiB instance. Set these at instance level where it is low-risk:
  - `rds.force_ssl=1` (already the default; set it explicitly)
  - `idle_in_transaction_session_timeout=60000` (60 s)
  - `log_min_duration_statement=500` (ms; use 200–1000 by taste)
  - `log_lock_waits=1`
  - `log_temp_files=0` (or 1024 kB)
  - `log_autovacuum_min_duration=1000`
  - `track_io_timing=1`
  - `track_activity_query_size=4096` (raise if queries are truncated)
  - `shared_preload_libraries` = `pg_stat_statements,pg_cron`
  - `cron.database_name=mitjip` (optional)
  - Leave `work_mem` at 4 MB, or 8 MB on db.t4g.small.
  - Raise `maintenance_work_mem` per session only when building HNSW (`SET maintenance_work_mem='128MB'`).
  - Leave `max_connections` at its default.
- Set request-path timeouts per role or connection, not globally, as the PG docs advise. For the app role: `ALTER ROLE mitjip_app SET statement_timeout='5s'` (15–30 s for report endpoints), `lock_timeout='3s'`, and `transaction_timeout='30s'` (PG 17+). The worker role gets a longer `statement_timeout`, for example 60 s. The migration role uses `SET lock_timeout='5s'` inside Alembic so DDL fails fast instead of queueing behind app locks. Don't set `idle_session_timeout` for the app role, because it would close pooled connections.
- TLS in SQLAlchemy: build an `ssl.create_default_context(cafile="/etc/ssl/rds/global-bundle.pem")` and pass `connect_args={"ssl": ctx}`, or use `?ssl=verify-full&sslrootcert=...` in the asyncpg URL. Bake the AWS RDS global bundle into the API and worker images.
- IAM auth: skip it on micro and small. The memory cost and the 15-minute token refresh complexity outweigh the benefit for one app user. Use a strong password in Secrets Manager or SSM Parameter Store, with separate `mitjip_app`, `mitjip_migrator`, and read-only `mitjip_ro` roles.
- Network: put a DB subnet group across 2 private subnets in 2 AZs (needed even for Single-AZ, and it lets Multi-AZ be enabled later). Set `PubliclyAccessible=false`. The RDS SG allows inbound TCP 5432 only from the EC2 app SG. For developer access, use SSM Session Manager port forwarding through the EC2 host rather than opening 5432.
- Encryption: enable `--storage-encrypted` with the default `aws/rds` key at creation. It can't be added cheaply later, and the managed key has no key-management overhead.

### Gaps
- No primary source fetched for the exact name and URL of the current RDS CA bundle (global-bundle.pem) or for the default CA for new instances in 2026.
- Whether RDS Proxy supports db.t4g.micro or small was not confirmed. It is not needed in any case.

---

## 4. PostgreSQL 17 lifecycle on RDS, Extended Support charges, minor auto-upgrade, maintenance windows; PG 18 availability; should a new project start on 18?

### Takeaway
Start on PostgreSQL 18 (18.6) unless a dependency blocks it. RDS has had PG 18 since 2025-11-14. Its RDS standard support runs to 2031-02-28, versus 2030-02-28 for PG 17. It ships the same extension set (pgvector 0.8.2, pg_bigm, pg_cron 1.6.7) and adds uuidv7(), skip scan, and parallel GIN builds. Either version is safe for the project horizon. Two practical warnings. First, minors 17.5 and 17.6 reach end of standard support on 2026-10-31 (two days from now), and 17.8 and 18.2 are NO_CREATE, so pin 17.11 or 18.6. Second, the default Seoul maintenance window block is 13:00–21:00 UTC, which is 22:00–06:00 KST.

### Cited Findings
- RDS PostgreSQL major-version calendar. PG 17: RDS release 2024-11-14, community EOL Nov 2029, RDS end of standard support 2030-02-28, Extended Support Y1 from 2030-03-01 and Y3 from 2032-03-01, ending 2033-02-28. PG 18: RDS release 2025-11-14, community EOL Nov 2030, end of standard support 2031-02-28, Extended Support to 2034-02-28. PG 14 reaches end of standard support on 2027-02-28 — [RDS PostgreSQL release calendar](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html)
- RDS minor calendar. 18.6 and 17.11 were released on RDS 2026-08-25 and are supported to Sep 2027. 17.7–17.10 run to Mar or Sep 2027. 17.5 and 17.6 reach end of standard support on 2026-10-31. 17.8 and 18.2 are marked NO_CREATE. Majors arrive on RDS within 30 days of community x.1, and minors within 7 days — [RDS PostgreSQL release calendar](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html)
- Community: PG 18 is at 18.6 with EOL 2030-11-14, and PG 17 is at 17.11 with EOL 2029-11-08. A banner announces "PostgreSQL 19 RC 1 Released!" on 2026-10-15, so 19 is not yet GA per that page — [PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/)
- RDS for PostgreSQL 18 GA was announced 2025-11-14, starting at 18.1. It brought skip scan for multicolumn B-tree, parallel GIN builds, UUIDv7, better observability, and the pgcollection extension. Extension updates included pgvector 0.8.1, pgaudit 18.0, and pg_cron 1.6.7. Upgrade paths are Blue/Green, in-place, or snapshot restore — [AWS What's New: RDS for PostgreSQL 18](https://aws.amazon.com/about-aws/whats-new/2025/11/amazon-rds-postgresql-major-version-18/)
- PG 18.0 was earlier offered in the RDS Database Preview Environment (Sep 2025) — [AWS What's New: PG 18.0 in RDS Preview](https://aws.amazon.com/de/about-aws/whats-new/2025/09/postgresql-180-amazon-rds-database-preview-environment/)
- PG 18 features per secondary sources: an async I/O subsystem (`io_method` = worker, sync, or io_uring; reads only in v1), `uuidv7()`, virtual generated columns, planner statistics preserved across pg_upgrade, `OLD`/`NEW` in RETURNING, and temporal `WITHOUT OVERLAPS` constraints. Performance claims of 2–3× are unverified — [Bytebase: What's new in Postgres 18](https://bytebase.com/blog/what-is-new-in-postgres-18); [Neon: PostgreSQL 18 new features](https://neon.com/postgresql/postgresql-18-new-features)
- Extended Support charges start the day after RDS end of standard support. They apply to Multi-AZ standbys too and stop on upgrade or deletion. You can avoid enrollment at create or restore time with `--engine-lifecycle-support open-source-rds-extended-support-disabled` — [RDS Extended Support charges](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support-charges.html)
- The Extended Support example rate is $0.100 per vCPU-hour in years 1–2 and $0.200 per vCPU-hour from year 3 (US East (Ohio) example) — [RDS for PostgreSQL pricing](https://aws.amazon.com/rds/postgresql/pricing/)
- Maintenance window: 30 minutes weekly, chosen at random from an 8-hour per-region block. Seoul (ap-northeast-2) is 13:00–21:00 UTC. Required patching is "typically once every few months". OS updates "typically … take about 10 minutes". Mandatory updates apply after their apply date even if you keep moving the window. To cancel an auto minor upgrade, disable Auto minor version upgrade. The maintenance and backup windows can't overlap — [Maintaining a DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html)

### Inferences
- Choose 18.6 for a new instance created in late October 2026. It gives one more year of standard support and uuidv7() for time-ordered primary keys, which helps B-tree locality on quotes, jobs, and sessions. It also has the same pgvector version as 17.11 on RDS. Stay on 17 only if a library in the stack is verified not to support 18. No such incompatibility was found for SQLAlchemy 2, asyncpg, or Alembic, though this was not explicitly verified.
- Do not wait for PG 19. RC1 was out 2026-10-15, and RDS adds a major within 30 days of 19.1, so 19 would likely land on RDS late in 2026 or early 2027. That is after the project's demo date.
- Set `AutoMinorVersionUpgrade=true`, with the maintenance window at `sun:17:00-sun:17:30` UTC (Mon 02:00 KST) and the backup window at `18:00-18:30` UTC. Opt out of Extended Support at create time as a guardrail against surprise charges.
- Single-AZ means OS or engine patching causes about 10 minutes of downtime a few times a year. Tell users it falls in the KST early-morning window.

### Gaps
- Not verified: whether RDS PG 18 exposes `io_method` or io_uring as a parameter.

---

## 5. pgvector on RDS: versions, HNSW vs IVFFlat for small corpora, iterative scans, dimension limits, memory on micro; Korean text search (pg_trgm, pg_bigm, PGroonga)

### Takeaway
RDS ships pgvector 0.8.2 on both 17.11 and 18.6. That includes iterative index scans from 0.8.0, but upstream is now at 0.8.7 (2026-10-01). Upstream 0.8.3–0.8.7 fixed HNSW vacuum corruption, IVFFlat build overflows, and memory issues that RDS has not picked up yet. For a few dozen to a few thousand chunks, start with no ANN index: exact scan gives perfect recall and is cheap at that size. Add HNSW only past roughly 10k–50k rows, and use halfvec if dimensions exceed 2,000. For Korean keyword search, pg_bigm (2-gram, GIN, `LIKE '%…%'`) is available on RDS and suits Korean better than pg_trgm for 1–2 character terms. PGroonga was not found in the RDS extension list.

### Cited Findings
- RDS extension versions: pgvector 0.8.2 on both PostgreSQL 17.11 and 18.6. pg_trgm 1.6, pg_bigm 1.2_20250903, pg_stat_statements 1.11 (17) and 1.12 (18), pg_cron 1.6.7, pg_partman 5.4.3, pgAudit 17.1 and 18, pg_repack 1.5.3. PGroonga and RUM did not appear in the portion of the table read (about the first 100k of 209k characters) — [RDS for PostgreSQL extensions table](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html)
- pgvector changelog. 0.7.0 (2024-04-29) added halfvec, sparsevec, and binary quantization. 0.8.0 (2024-10-30) added iterative index scans and improved HNSW and filtered-query costing. 0.8.1 (2025-09-04) added PG 18 support. 0.8.2 (2026-02-25) fixed a parallel HNSW build buffer overflow. 0.8.3 (2026-06-17) fixed "possible HNSW vacuum corruption". 0.8.4 (2026-06-30) fixed HNSW vacuum and insert errors and an IVFFlat build overrun. 0.8.5–0.8.7 (Jul–Oct 2026) brought IVFFlat memory and overflow fixes. 0.9.0 is unreleased and adds async I/O for HNSW while dropping PG 13/14 — [pgvector CHANGELOG](https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md)
- Limits: `vector` can be indexed up to 2,000 dims and stored up to 16,000. `halfvec` can be indexed up to 4,000 dims. `bit` can be indexed up to 64,000. `sparsevec` can index up to 1,000 non-zeros. HNSW has a better speed-recall tradeoff with slower builds and more memory, and needs no training, so it works on an empty table. IVFFlat builds faster with less memory but has lower query performance. It must be built after data exists, with lists = rows/1000 (≤1M rows) and probes ≈ sqrt(lists). `hnsw.ef_search` defaults to 40. Iterative scans use `hnsw.iterative_scan = strict_order | relaxed_order`, with `hnsw.max_scan_tuples` defaulting to 20,000. HNSW builds are "much faster when the graph fits into maintenance_work_mem". Filtering "is applied after the index is scanned", so a 10% filter with ef_search 40 returns about 4 rows. Use B-tree or partial indexes for selective filters — [pgvector README](https://github.com/pgvector/pgvector)
- RDS added pgvector 0.8.0 on 2024-11-21 for 17.1+, 16.5+, and older lines, highlighting iterative scans and better planner index choice with filters — [AWS What's New: RDS pgvector 0.8.0](https://aws.amazon.com/about-aws/whats-new/2024/11/amazon-rds-for-postgresql-pgvector-080/); [PostgreSQL.org: pgvector 0.8.0 released](https://www.postgresql.org/about/news/pgvector-0.8.0-released-2952/)
- AWS's pgvector 0.8.0 benchmark post (Aurora, so only indicative for RDS) shows enabling `hnsw.iterative_scan='relaxed_order'` to fix over-filtering — [AWS Database Blog: pgvector 0.8.0 on Aurora PostgreSQL](https://aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql)
- RDS has supported pg_bigm since 2021-04 "for faster full text search of languages that require multi-byte character sets such as Japanese, Chinese, and Korean" — [AWS What's New: RDS supports pg_bigm (2021, older)](https://aws.amazon.com/about-aws/whats-new/2021/04/amazon-rds-for-postgresql-supports-pg-bigm-extension-for-faster-full-text-search)
- pg_bigm works with CJK without extra configuration. Indexes use `gin_bigm_ops`, and queries use `LIKE '%keyword%'` — [Pigsty: pg_bigm](https://pigsty.io/ext/e/pg_bigm/); [pg_bigm docs (GitHub)](https://github.com/pgbigm/pg_bigm/blob/REL1_0_STABLE/docs/pg_bigm_en.md)
- pg_bigm vs pg_trgm: pg_bigm is 2-gram and GIN-only with `LIKE` only. pg_trgm is 3-gram, supports GIN and GiST, and handles `LIKE`/`ILIKE`/`~`/`~*` plus similarity. pg_bigm is faster for 1–2 character keywords. This comparison comes from Alibaba PolarDB docs, not AWS — [Alibaba Cloud PolarDB: pg_bigm](https://help.aliyun.com/en/polardb/polardb-for-postgresql/pg-bigm-1)

### Inferences
- Memory on micro, assuming OpenAI text-embedding-3-small at 1,536 dims (from training knowledge, not re-verified here). 5,000 chunks × 1,536 × 4 B ≈ 30 MB of raw vectors, plus an HNSW graph of a similar order. With halfvec that is about 15 MB. This fits easily on disk. The HNSW graph would fit in a 64–128 MB maintenance_work_mem for a fast build. At this size exact scan (`ORDER BY embedding <=> $1 LIMIT k` with no index) is a few-ms sequential scan with 100% recall, which also avoids the HNSW vacuum-corruption class fixed after 0.8.2.
- If text-embedding-3-large at 3,072 dims is used (training knowledge), the `vector` type can't be indexed above 2,000 dims. Store `halfvec(3072)` (indexable to 4,000) or request a reduced `dimensions` value such as 1,024 or 1,536 from the API.
- Hybrid retrieval: combine pg_bigm `LIKE '%키워드%'` (or a pg_trgm similarity score) with vector cosine distance via reciprocal-rank fusion in SQL. Use `simple` tsvector only for exact token fields such as 시공 항목 codes. The built-in `korean` text search config doesn't exist in core PostgreSQL (training knowledge), which is why the bigram approach is the common fallback on RDS.
- Apply metadata filters (trade = 도배 or 목공, region, document type) through B-tree or partial indexes, or rely on exact scan. If HNSW is added later, turn on `hnsw.iterative_scan='relaxed_order'`.

### Gaps
- PGroonga availability on RDS couldn't be confirmed or ruled out because the extension table was only partly read. No AWS announcement of PGroonga support was found.
- No benchmark of pg_bigm vs pg_trgm on Korean text on RDS was found.

---

## 6. Redis on the same EC2 vs ElastiCache Serverless (Valkey): durability, memory, failure behaviour; Redis 8 licensing; Valkey image

### Takeaway
For rate-limit counters plus an arq queue at this scale, a Redis or Valkey container on the app host is fine and nearly free. Its durability is only as good as its config. The official Redis image has no persistence and protected mode off by default. If it holds the job queue, enable AOF (`appendfsync everysec`, ≤1 s loss) plus RDB on a named volume. Set `maxmemory` with `noeviction`, never publish 6379, and set a password. The Postgres `jobs` ledger already makes the queue recoverable. ElastiCache Serverless Valkey starts at about $6/month (us-east-1 rate) and buys HA, which this architecture deliberately skips. Redis 8 under AGPLv3 is fine for unmodified internal use. Valkey (BSD-3, Linux Foundation) is equally good and avoids license questions.

### Cited Findings
- Redis 8+ is tri-licensed: RSALv2, SSPLv1, or AGPLv3 at the user's choice. Redis ≤7.2 is BSD-3, and 7.4–7.8 is RSALv2/SSPLv1. FAQ: using code "as-is" means no impact. Under AGPL, operators of modified Redis servers must provide the modified source to users. "If you are building a solution that leverages Redis, but does not specifically compete with Redis itself, there is no impact" — [Redis licenses](https://redis.io/legal/licenses/)
- Secondary summaries agree that self-hosting under AGPLv3 is free and that obligations arise when you modify Redis or offer it as a service. They disagree on SaaS edge cases, and some overstate the AGPL reach — [OneUptime: Redis licensing explained (2026-03)](https://oneuptime.com/blog/post/2026-03-31-redis-licensing-sspl-agplv3-explained/view); [Upstash: How to self-host Redis in 2026](https://upstash.com/blog/how-to-self-host-redis-in-2026)
- Docker official `redis` image: the latest line is 8.10.3 (tags `8.10`, `8`, `latest`), and 8.8.4, 8.6.8, 8.4.8, and 8.2.11 are also listed. "Protected mode" is off by default, so set a password before exposing. Persistence is not on by default (the example uses `--save 60 1`), and data lives in `VOLUME /data`. The container drops privileges to the `redis` user — [Docker Hub: redis](https://hub.docker.com/_/redis)
- Persistence: RDB snapshots can lose "the latest minutes of data". AOF with `appendfsync everysec` (the default and suggested policy) loses at most about 1 s. `always` is "very very slow". Redis recommends both RDB and AOF for Postgres-like safety. Multi-part AOF has existed since 7.0. Redis 8.10 adds a `BACKUP` command family for online backups — [Redis persistence docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
- Valkey releases: 9.1.3, 9.0.7, 8.1.11, 8.0.12, and 7.2.15 all shipped 2026-10-26 as security releases (a cluster Pub/Sub heap overflow, GHSA-f4q9-j22m-xqq9). 9.1.2 (2026-08-31) fixed an unauthenticated Lua use-after-free. 9.2.0-rc1 came out 2026-09-16 — [Valkey GitHub releases](https://github.com/valkey-io/valkey/releases)
- The Valkey image `valkey/valkey:9.0.0` is used in guides. Distributions package it as BSD-3-Clause (plus BSD-2/MIT components) — [Percona: How to set up Valkey](https://www.percona.com/blog/how-to-set-up-valkey-the-alternative-to-redis/); [Alpine package: valkey](https://pkgs.alpinelinux.org/package/v3.23/main/x86/valkey); [community-scripts: Valkey](https://community-scripts.org/scripts?id=valkey)
- ElastiCache Serverless for Valkey: $0.084 per GB-hour storage and $0.0023 per million ECPUs (US East). There is a minimum metered storage of 100 MB per cache for Valkey, against 1 GB for Redis OSS and Memcached. Valkey "starts at $6/month". Seoul rates were not shown — [AWS ElastiCache pricing](https://aws.amazon.com/elasticache/pricing/)
- Floor math: 0.1 GB × $0.084 × 730 h ≈ $6.13/month before ECPUs — [Upstash: ElastiCache pricing explained (2026)](https://upstash.com/blog/aws-elasticache-pricing-explained-2026-full-cost-breakdown)

### Inferences
- Failure behaviour on the single EC2. If the host dies, Redis, the app, and the worker all die together, so Redis HA adds nothing without app HA. On a container restart without persistence, rate-limit counters reset (harmless) and queued or in-flight arq jobs are lost. The 1-minute ledger cron re-enqueues them, so only latency is lost. With AOF everysec, at most about 1 s of enqueues is lost, and the ledger covers that as well.
- Project rule check: `mitjip/AGENTS.md` §2 already says Redis holds only the queue, rate limits and short caches ("지워져도 되는 것", data that may be lost). PostgreSQL `jobs` is the source of truth. Under that rule AOF is optional: it only shortens re-enqueue latency after a restart. Treat it as a cheap safety option, not a requirement. PG 17 is also named in AGENTS.md §2, so moving to PG 18 (§4) or to a Postgres-only queue (§7) is a team decision and should be recorded as an ADR. AGENTS.md §5 also requires new dependencies to be announced in an issue or PR.
- Recommended Compose config: `valkey/valkey:9.0` or `redis:8.10-alpine`, using a pinned minor and patching on security releases. Command: `--appendonly yes --appendfsync everysec --save 900 1 --maxmemory 128mb --maxmemory-policy noeviction --requirepass ${REDIS_PASSWORD}`. Use a named volume `/data`, keep the service on the internal Compose network only with no `ports:`, and set a `mem_limit` of about 192 MB. `noeviction` matters because eviction would silently drop queue keys (inference; not stated in the sources fetched).
- With a t4g.small EC2 (2 GiB) also running Next.js, FastAPI, and the worker, Redis's footprint (tens of MB) is negligible. The risk is the whole host running out of memory, not Redis itself.
- Choose Valkey if the team wants a simple license story or a later lift to ElastiCache Valkey with the same engine. Choose Redis 8 if Redis-only features are wanted. Neither choice affects arq, SAQ, or redis-py (wire-compatible, inference).
- ElastiCache Serverless becomes worth it only when the app tier runs on more than one host. At that point a shared limiter or queue and HA matter.

### Gaps
- ElastiCache Serverless and node-based (cache.t4g.micro) prices in Seoul were not available.
- No primary source checked on redis-py or arq compatibility with Valkey 9 specifically.

---

## 7. arq in 2026, alternatives (SAQ, PgQueuer, Procrastinate, Taskiq, Celery, Dramatiq, DBOS), and Postgres-only queues

### Takeaway
arq is officially maintenance-only (Samuel Colvin, 2025-10-18). It still received small releases, 0.27.0 (2026-02-02) and 0.28.0 (2026-04-16, Python 3.14 support), so the `arq>=0.28,<0.29` pin is workable for a project ending in weeks. Its at-least-once ("Jobs may be called more than once!") and 0.5 s polling semantics fit an outbox-backed design.

The cleanest simplification for this stack is a Postgres-native queue, PgQueuer. It speaks asyncpg, enqueues inside the app's transaction, wakes workers through LISTEN/NOTIFY, claims jobs with SKIP LOCKED, and has built-in cron and retries. That removes both Redis from the job path and the 1-minute re-enqueue relay. SAQ is the closest drop-in successor if Redis stays. Procrastinate requires psycopg (a second driver). DBOS is a heavier durable-workflow paradigm. Taskiq is active but broker-centric.

### Cited Findings
- Issue #510 was opened and pinned 2025-10-18 by Samuel Colvin and is titled "Maintenance only mode". It says "the pydantic team and I don't have time right now to put significant effort into arq", "We'll continue to fix critical security issues", the repo won't be archived, and "don't expect work on new fixes" — [arq issue #510](https://github.com/python-arq/arq/issues/510)
- arq releases: 0.27.0 (2026-02-02) added Python 3.13, dropped 3.8, and switched to uv. 0.28.0 (2026-04-16) added only Python 3.14 support, released by Viicos. The last redis-py bump listed is in 0.26.1 (constraint `<5` → `<6`). The repo shows 87 open issues and 24 open PRs — [arq GitHub releases](https://github.com/python-arq/arq/releases)
- PyPI: arq 0.28.0 released 2026-04-16, requiring Python ≥3.9 — [PyPI: arq](https://pypi.org/project/arq/)
- arq semantics: jobs are "pessimistic" and stay queued until success or failure, and the docs warn "Jobs may be called more than once!", so make them idempotent. Defaults: `job_timeout` 300 s, `max_tries` 5 (cron 1), `poll_delay` 0.5 s, `max_jobs` 10, `keep_result` 3600 s, and enqueued jobs expire after 24 h. A custom `_job_id` dedupes until the result clears, and `enqueue_job` returns None if the id exists. Cron `unique=True` runs once across workers. The health check key is written every 3,600 s and checked with `arq --check`. `allow_abort_jobs` defaults to False — [arq documentation](https://arq-docs.helpmanual.io/)
- SAQ is "built on top of asyncio and redis or postgres" (extra `saq[postgres]`). It avoids polling with BLMOVE/RPOPLPUSH plus NOTIFY and reports <5 ms latency against arq's 0.5 s poll, "up to 8x faster". It adds a web UI, a heartbeat monitor for abandoned jobs, and before/after hooks, and has 895 stars — [SAQ GitHub](https://github.com/tobymao/saq)
- SAQ benchmark (N = 1000, seconds, SAQ vs arq): enqueue 0.18 vs 0.54, noop 0.92 vs 5.01, sleep 2.82 vs 5.01. It stores stack traces, sweeps stuck jobs, and treats cancelled jobs separately from failed ones. These are vendor-reported numbers — [SAQ: Comparison to ARQ](https://saq-py.readthedocs.io/en/latest/comparison.html)
- The SAQ docs header shows 0.26.5. The changelog lists v0.26.4 (2026-05-21) fixing a same-key job race and relaxing the redis-py pin from `<7` to `<8` — [SAQ docs](https://saq-py.readthedocs.io/en/latest/); [SAQ changelog](https://saq-py.readthedocs.io/en/stable/changelog.html)
- PgQueuer is a Postgres-only queue. "Enqueuing can happen inside the same transaction as your application data". Workers claim with `FOR UPDATE SKIP LOCKED` and wake on LISTEN/NOTIFY with a polling fallback. It supports asyncpg and psycopg (async and sync), cron-style recurring tasks, `execute_after` deferral, per-entrypoint concurrency limits, retry with exponential backoff, a CompletionWatcher, Prometheus metrics, a dashboard, and an in-memory test mode. It requires Python 3.11+ and PG 14+, is MIT-licensed, has 1.5k stars, and includes a FastAPI example — [PgQueuer GitHub](https://github.com/janbjorge/pgqueuer)
- Procrastinate is a Postgres task queue for Python 3.10+ and PG 13+. It is async-first, with periodic tasks, retries, queueing locks, priorities, and Django integration — [Procrastinate docs](https://procrastinate.readthedocs.io/en/stable/)
- Procrastinate connectors are PsycopgConnector (async psycopg3), AiopgConnector, SyncPsycopgConnector, Psycopg2Connector, and SQLAlchemyPsycopg2Connector (defer only). asyncpg is not listed, and running a worker needs an async connector — [Procrastinate: connectors](https://procrastinate.readthedocs.io/en/stable/howto/basics/connector.html)
- Taskiq is an "asyncio celery implementation" with brokers for NATS, Redis, RabbitMQ, Kafka, and others. It has a FastAPI integration that reuses app dependencies, and 2.4k stars — [Taskiq GitHub](https://github.com/taskiq-python/taskiq); [Taskiq docs](https://taskiq-python.github.io/)
- In Nov 2025 a commit in the Taskiq repo referencing arq #510 updated arq's status in a comparison table. This is an indirect signal of users migrating — [arq issue #510](https://github.com/python-arq/arq/issues/510)
- DBOS Transact records durable workflows and steps in Postgres, with Postgres as the sole dependency. It provides queues, scheduling, and a FastAPI pattern of `@DBOS.workflow()` plus `DBOS.launch()`. Version 2.17.0 came out 2026-03-31 for Python 3.10–3.13. The April 2026 release added delayed workflow scheduling and enqueueing from Postgres functions and triggers — [DBOS Python programming guide](https://docs.dbos.dev/python/programming-guide); [DBOS: April 2026 enhancements](https://www.dbos.dev/blog/dbos-new-features-april-2026); [CERN simple-repository: dbos 2.17.0](https://simple-repository.app.cern.ch/project/dbos)
- Postgres-queue risk: long-running transactions block vacuum of processed job rows. Dead tuples pile up, and lock times rose about 15× in the author's test. Mitigations are killing long transactions and statement timeouts. This is an older source (2015), so treat it as background — [Brandur: Postgres job queues & failure by MVCC (2015)](https://brandur.org/postgres-queues)
- "An open transaction prevents vacuuming away recently-dead tuples … can contribute to table bloat" — [PostgreSQL 17 docs: idle_in_transaction_session_timeout](https://www.postgresql.org/docs/17/runtime-config-client.html)

### Inferences
- Fit ranking for "async FastAPI + SQLAlchemy asyncpg + Postgres outbox":
  1. **PgQueuer.** Same driver (asyncpg). Its transactional enqueue replaces the `jobs` outbox and the 1-minute relay cron. Built-in cron covers session purges. Redis would then be needed only for rate limits, which could also move to Postgres or an in-process limiter.
  2. **SAQ (Redis).** Near drop-in for arq's API style, actively released, lower latency, with a UI. Keeps the current outbox design.
  3. **Keep arq 0.28 pinned.** Lowest migration effort. Acceptable for a short-lived project because the ledger plus re-enqueue already covers its at-least-once and loss cases.
  4. **DBOS.** Compelling if the AI-agent pipeline (schedule explanation → recommendation reasons → notification) is treated as a multi-step durable workflow, but it is a new paradigm to learn.
  5. **Procrastinate.** Solid but needs psycopg alongside asyncpg.
  6. **Taskiq.** Fine, but it means a broker plus extra packages.
  7. **Celery and Dramatiq.** Sync-first and heavier, not researched here.
- Postgres-only queue, pros: one durable store (RDS backups and PITR cover jobs), transactional enqueue with no dual-write, no Redis durability tuning, one less moving part on the 2 GiB EC2. Cons: adds write and vacuum load to a micro instance (tiny at this volume), holds a LISTEN connection per worker, is sensitive to idle-in-transaction bloat (mitigated by the timeouts in §3), and makes the DB a single point of failure for jobs (already true for the app).
- If arq stays: make every job handler idempotent and keyed by `jobs.id` as `_job_id`. Mark `jobs.status` in Postgres inside the handler's transaction. The relay cron should re-enqueue only `status in ('pending','failed_retryable') and updated_at < now()-interval '2 min'`. arq's `_job_id` dedupe lasts only until `keep_result` (1 h) expires, so Postgres status, not Redis, must be the source of truth. Also check that the installed redis-py satisfies arq's `<6` constraint if it still holds in 0.28, which could conflict with other libraries wanting redis-py 6 or 7.

### Gaps
- No arq-specific bug reports (job loss on SIGKILL, redis-py 6/7 compatibility) were retrieved before the search budget ran out.
- Not confirmed whether SAQ's Postgres backend uses psycopg or asyncpg.
- Current maintenance status and versions of Celery, Dramatiq, and Taskiq were not checked.
- No independent benchmark of PgQueuer throughput on small RDS instances was found.

---

## 8. Session storage in Postgres, cleanup jobs, SQLAlchemy asyncpg pooling (pool_pre_ping, prepared statements), migrations on deploy

### Takeaway
Postgres-backed server sessions are fine at this scale. Index `expires_at`, purge expired rows on a schedule with pg_cron (supported on RDS, needs `shared_preload_libraries` and a reboot) or the app worker's cron, and also purge `cron.job_run_details`. In SQLAlchemy, keep `pool_size=5, max_overflow=5`, add `pool_pre_ping=True` (small checkout overhead) and `pool_recycle` of about 1800 s, and keep asyncpg's 100-statement prepared cache. Run Alembic as a one-shot container before starting new API and worker containers, then restart them. This sequencing avoids `InvalidCachedStatementError` from stale prepared statements after DDL.

### Cited Findings
- QueuePool defaults are `pool_size` 5, `max_overflow` 10, and `pool_timeout` 30 s. `pool_pre_ping` "adds a small bit of overhead to the connection checkout process" and "does not accommodate for connections dropped in the middle of transactions". `pool_recycle` replaces connections older than N seconds at checkout. After `os.fork()`, call `engine.dispose(close=False)` in the child ("This is the recommended approach") — [SQLAlchemy 2.0 connection pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- asyncpg dialect: 100 prepared statements per connection by default. DDL from another process can cause `InvalidCachedStatementError` or "cache lookup failed for type", which can't be retried in the same transaction — [SQLAlchemy 2.0 PostgreSQL dialect](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- pg_cron on RDS needs engine 12.5 or later. Add `pg_cron` to `shared_preload_libraries`, reboot, then `CREATE EXTENSION pg_cron` as rds_superuser. Metadata lives in `postgres` by default (`cron.database_name` changes this), and jobs can target other databases. The default `cron.max_running_jobs` is 5 and must be below `max_worker_processes`. AWS recommends purging `cron.job_run_details`, for example keeping 7 days with a daily `DELETE … WHERE end_time < now() - interval '7 days'` — [RDS: pg_cron](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL_pg_cron.html)
- RDS pg_cron version is 1.6.7 on 17.11 and 18.6 — [RDS extensions table](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html)
- `lock_timeout` applies per lock acquisition. "If statement_timeout is nonzero, it is rather pointless to set lock_timeout to the same or larger value" — [PostgreSQL 17: Client connection defaults](https://www.postgresql.org/docs/17/runtime-config-client.html)

### Inferences
- Sessions table sketch: `sessions(id uuid pk default uuidv7(), user_id fk, created_at, last_seen_at, expires_at, ip inet, user_agent text, revoked_at)` with an index on `expires_at` and one on `user_id`. Write `last_seen_at` lazily, at most once per 5–15 minutes, to avoid a write per request (training knowledge). Cleanup: `SELECT cron.schedule('purge-sessions','*/30 * * * *', $$DELETE FROM sessions WHERE expires_at < now() - interval '1 day'$$)`. If pg_cron is avoided, do the same via an arq, SAQ, or PgQueuer cron job.
- Pool settings: `create_async_engine(url, pool_size=5, max_overflow=5, pool_timeout=10, pool_pre_ping=True, pool_recycle=1800, connect_args={"ssl": ctx, "server_settings": {"application_name": "mitjip-api"}})`. Use distinct `application_name` values for the API, worker, and migrator so `pg_stat_activity` and Database Insights show who holds connections. Uvicorn `--workers 2` forks after import, so create the engine in the lifespan startup, not at import time. Otherwise call `dispose(close=False)` as the SQLAlchemy docs advise.
- Migrations on deploy: (1) take a manual RDS snapshot for risky migrations, (2) `docker compose run --rm migrate alembic upgrade head` with `SET lock_timeout='5s'` and `statement_timeout='60s'` for the migrator role, (3) `docker compose up -d api worker`, which recreates processes and so refreshes prepared-statement caches. Write expand/contract-style migrations (add nullable column → backfill → enforce), and use `CREATE INDEX CONCURRENTLY` in an autocommit block for large tables. Never run Alembic from each uvicorn worker at startup, because 2 workers would race.

### Gaps
- No 2025–2026 practitioner source was retrieved specifically on Alembic plus RDS deployment patterns or on Postgres session-store benchmarks.

---

## 9. What else to add at the data layer (pg_stat_statements, Database Insights, restore tests, retention/purge, audit tables)

### Takeaway
Add the following, most of them cheap or free:
- pg_stat_statements, which RDS PG 11+ preloads by default (just `CREATE EXTENSION`)
- Database Insights Standard mode (default; 7 days of per-query metrics free; it replaced Performance Insights, whose EOL was 2026-07-31)
- PostgreSQL log export to CloudWatch with a slow-query threshold
- CloudWatch alarms on FreeableMemory, CPUCreditBalance, FreeStorageSpace, and DatabaseConnections
- An RDS event subscription for failover, maintenance, and low storage
- Storage autoscaling with a max cap
- A documented monthly PITR restore drill
- Scheduled purge jobs (sessions, job ledger, pg_cron history, AI-output and log tables)
- An append-only `audit_events` table for vendor approval, quote, and confirmation state changes (pgAudit available if needed)
- Separate DB roles

### Cited Findings
- pg_stat_statements: "For PostgreSQL DB instances that are compatible with PostgreSQL 11 or later, the database loads this library by default". Queries over 4,096 bytes are truncated unless `track_activity_query_size` is raised (reboot required) — [RDS: SQL statistics for RDS PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.UsingDashboard.AnalyzeDBLoad.AdditionalMetrics.PostgreSQL.html)
- Database Insights: Performance Insights EOL was 2026-07-31 and users were migrated. "Standard mode is the default". Standard includes top contributors to DB load and "up to 7 days of detailed database and per-query metrics retention at no additional cost", with paid retention of 1–24 months. Advanced mode adds per-query statistics, slow SQL analysis (needs log export), SQL lock analysis for RDS PostgreSQL, fleet views, and on-demand analysis — [CloudWatch Database Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Database-Insights.html)
- The Performance Insights API continues and its costs appear under CloudWatch Database Insights — [RDS Performance Insights doc (EOL notice)](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.md)
- RDS logs can be exported to CloudWatch Logs, and the logging docs cover pgAudit for audit trails — [RDS for PostgreSQL database log files](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Concepts.PostgreSQL.html)
- pgAudit 17.1 and 18, pg_partman 5.4.3, and pg_repack 1.5.3 are available on RDS — [RDS extensions table](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html)
- RDS PITR and restore mechanics, including the default parameter group on restore, apply to restore drills — [RDS restore to a point in time](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html)
- To get notified of optional OS patches, subscribe to RDS-EVENT-0230 — [Maintaining a DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html)
- The `EBSByteBalance%` metric approaching 0 means the instance is out of burst I/O capacity. Watch DiskQueueDepth, Read/WriteIOPS, and latency — [RDS DB instance storage](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html)

### Inferences
Concrete additions checklist, mostly configuration:
1. `CREATE EXTENSION pg_stat_statements; CREATE EXTENSION pg_bigm; CREATE EXTENSION vector;` in an Alembic baseline migration. Add `pg_cron` too if used.
2. Keep Database Insights in Standard mode (free 7 days). Don't buy Advanced at this scale.
3. Export the `postgresql` and `upgrade` logs to CloudWatch with a 14–30 day log-group retention, so CloudWatch Logs costs stay small. Set `log_min_duration_statement=500`.
4. CloudWatch alarms, using the free 10 alarms (free-tier count from training knowledge):
   - `FreeableMemory < 150 MB` (micro) or `< 300 MB` (small)
   - `CPUCreditBalance < 50`, and `CPUSurplusCreditBalance > 0` for 1 h
   - `FreeStorageSpace < 4 GiB`
   - `DatabaseConnections > 60`
   - `EBSByteBalance% < 20`
   - `ReadLatency/WriteLatency > 20 ms`
   Send them to an SNS topic, with the existing SES email or a Slack webhook.
5. Turn on storage autoscaling with `MaxAllocatedStorage=100` GiB to avoid a `storage_full` outage. Note that automated backups don't run in that state.
6. Monthly PITR restore drill (see §2) with a short runbook in `mitjip/docs`.
7. Purge and retention jobs:
   - sessions: expired + 1 day
   - `jobs` ledger: done older than 30 days → delete; failed → keep 90 days
   - AI agent output tables: keep per product need
   - rate-limit audit/log tables: 30 days
   - `cron.job_run_details`: 7 days
   - uploaded business-registration certificate metadata: aligned to the S3 lifecycle and the privacy policy
   Personal data such as phone numbers, addresses, and business registration numbers needs a stated retention under PIPA (개인정보보호법; training knowledge, verify with the legal and policy research stream).
8. Append-only `audit_events(id uuidv7, actor_id, actor_role, action, entity_type, entity_id, before jsonb, after jsonb, created_at, ip)`. Write it from the service layer in the same transaction as state changes: vendor approve or reject, quote submit, compare, confirm, site-visit schedule, admin edits. Use pgAudit only if the course requires DB-level auditing, because it is noisy on a micro instance.
9. Roles: `mitjip_migrator` (DDL), `mitjip_app` (DML only), `mitjip_ro` (read-only for analytics and admin dashboards). Use the master user only for break-glass.
10. Opt out of Extended Support at create time, turn on deletion protection, and create the DB instance from IaC (Terraform, CDK, or a CLI script) so restore drills can reproduce the parameter group, subnet group, and SG.

### Gaps
- Exact Database Insights Standard paid-retention price and Advanced mode price per vCPU-hour in Seoul (AWS CloudWatch pricing page not fetched).
- No Korean-language RDS PostgreSQL operations blog was retrieved; the search budget ran out before a targeted Korean search could be done.

### Sources consulted (all URLs used in these notes)
- https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html
- https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.Types.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Tuning.concepts.memory.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Tuning_proactive_insights.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ExportSnapshot.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support-charges.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL_pg_cron.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Concepts.PostgreSQL.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.UsingDashboard.AnalyzeDBLoad.AdditionalMetrics.PostgreSQL.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.md
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Database-Insights.html
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html
- https://aws.amazon.com/rds/postgresql/pricing/
- https://aws.amazon.com/rds/proxy/pricing/
- https://amazonaws.cn/en/rds/proxy/pricing
- https://aws.amazon.com/rds/sla/
- https://aws.amazon.com/elasticache/pricing/
- https://aws.amazon.com/about-aws/whats-new/2026/03/amazon-aurora-postgresql-aws-free-tier
- https://aws.amazon.com/about-aws/whats-new/2025/11/amazon-rds-postgresql-major-version-18/
- https://aws.amazon.com/de/about-aws/whats-new/2025/09/postgresql-180-amazon-rds-database-preview-environment/
- https://aws.amazon.com/about-aws/whats-new/2024/11/amazon-rds-for-postgresql-pgvector-080/
- https://aws.amazon.com/about-aws/whats-new/2021/04/amazon-rds-for-postgresql-supports-pg-bigm-extension-for-faster-full-text-search
- https://aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql
- https://www.bytebase.com/dbcost/rds/instance/db.t4g.micro.md
- https://www.bytebase.com/dbcost/rds/instance/db.t4g.small.md
- https://sparecores.com/database/aws/db.t4g.micro
- https://instances.vantage.sh/aws/rds/db.t4g.micro
- https://aiven.io/tools/instances/db.t4g.micro
- https://cur.vantage.sh/aws/amazonrds/storage%20snapshot/apn2-rds:chargedbackupusage
- https://www.usage.ai/blogs/aws/reserved-instances/rds/storage-cost/
- https://www.usage.ai/blogs/aws/reserved-instances/rds/proxy-cost/
- https://www.netapp.com/ko/blog/understanding-backup-pricing-aws-cvo-blg/
- https://infratally.com/articles/aws-free-tier-2026/
- https://tech-insider.org/what-changed-in-the-aws-free-tier-for-2026/
- https://stackharbor.com/en/knowledge-base/awsrds-parameter-group-tuning/
- https://www.postgresql.org/support/versioning/
- https://www.postgresql.org/docs/17/runtime-config-client.html
- https://www.postgresql.org/about/news/pgvector-0.8.0-released-2952/
- https://bytebase.com/blog/what-is-new-in-postgres-18
- https://neon.com/postgresql/postgresql-18-new-features
- https://thebuild.com/blog/all-your-gucs-in-a-row-idle_in_transaction_session_timeout/
- https://chat2db.ai/resources/blog/statement-timeout-in-postgresql
- https://brandur.org/postgres-queues
- https://github.com/pgvector/pgvector
- https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md
- https://pigsty.io/ext/e/pg_bigm/
- https://github.com/pgbigm/pg_bigm/blob/REL1_0_STABLE/docs/pg_bigm_en.md
- https://help.aliyun.com/en/polardb/polardb-for-postgresql/pg-bigm-1
- https://redis.io/legal/licenses/
- https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
- https://hub.docker.com/_/redis
- https://oneuptime.com/blog/post/2026-03-31-redis-licensing-sspl-agplv3-explained/view
- https://upstash.com/blog/how-to-self-host-redis-in-2026
- https://upstash.com/blog/aws-elasticache-pricing-explained-2026-full-cost-breakdown
- https://github.com/valkey-io/valkey/releases
- https://www.percona.com/blog/how-to-set-up-valkey-the-alternative-to-redis/
- https://pkgs.alpinelinux.org/package/v3.23/main/x86/valkey
- https://community-scripts.org/scripts?id=valkey
- https://github.com/python-arq/arq/issues/510
- https://github.com/python-arq/arq/releases
- https://pypi.org/project/arq/
- https://arq-docs.helpmanual.io/
- https://github.com/tobymao/saq
- https://saq-py.readthedocs.io/en/latest/
- https://saq-py.readthedocs.io/en/latest/comparison.html
- https://saq-py.readthedocs.io/en/stable/changelog.html
- https://github.com/janbjorge/pgqueuer
- https://procrastinate.readthedocs.io/en/stable/
- https://procrastinate.readthedocs.io/en/stable/howto/basics/connector.html
- https://github.com/taskiq-python/taskiq
- https://taskiq-python.github.io/
- https://docs.dbos.dev/python/programming-guide
- https://www.dbos.dev/blog/dbos-new-features-april-2026
- https://simple-repository.app.cern.ch/project/dbos
- https://docs.sqlalchemy.org/en/20/core/pooling.html
- https://docs.sqlalchemy.org/en/20/dialects/postgresql.html
- https://magicstack.github.io/asyncpg/current/api/index.html
