# Benchmarks & missing components for the 믿집 completed architecture

Scope: comparable Korean and global home-service/interior marketplaces, AWS Well-Architected and startup guidance, small-team single-instance failure stories, production-readiness items (including Korean legal ones), analytics and consent, search, and vendor trust & safety. The goal is to find what the proposed architecture is missing. The proposal under review is: one EC2 t4g.small running Docker Compose (Caddy, Next.js 16, FastAPI modular monolith, Redis, arq), plus RDS PostgreSQL 17 with pgvector, S3, SES, Route 53, GitHub Actions → ECR → SSM, CloudWatch, OpenAI (3 agents), and public data APIs.

Research date: 2026-10-29. Labels: **[old]** = before 2024; **[3rd-party]** = not the primary or official source; **[snippet]** = taken from a search-result summary, not a full-page read.

---

## 1. What do comparable Korean platforms (오늘의집, 숨고, 집닥, 아파트멘터리 etc.) use and offer?

### Takeaway
The Korean interior and home-service leaders now compete on **trust infrastructure** more than on matching:
- 오늘의집 has 책임보장, a standard contract, and bank-guaranteed cash payment.
- 숨고 runs a 2026 "trust TF" with public-API vendor verification, periodic re-verification, scam-account checks, and refund guarantees up to 500만원.

Interior platforms that lacked this trust layer shut down in 2023–2025. On the engineering side, 오늘의집 runs dedicated platforms for search, experimentation, a feature store, and self-service analytics. That is far beyond 믿집's scale. The transferable lessons are product-level: verification, guarantees, standard contracts, and transparency.

### Cited Findings
**오늘의집 (버킷플레이스)**
- The 오늘의집 app markets three construction trust products:
  - '오늘의집 스탠다드', which discloses vendor margin 100%
  - '책임보장', an A/S guarantee
  - '직시공', where 오늘의집 manages the whole process
  
  — [App Store listing](https://apps.apple.com/KR/app/id1008236892) [snippet]
- 오늘의집 expert pages state two things:
  - Cash payments are protected by a 채무지급보증 contract with 우리은행.
  - "(주)버킷플레이스는 통신판매중개자로 거래 당사자가 아니므로…", i.e. a broker disclaimer.
  
  — [ohou.se expert review page](https://ohou.se/experts/review/9926) [snippet]
- 시공책임보장 took effect 2023-06-30. **[old]**
  - It covers defects and delays by contractors the platform introduced. A dedicated satisfaction team mediates disputes. If a contractor can't finish, a designated partner completes the work and the A/S.
  - Covered vendors use a contract based on the Fair Trade Commission's 실내건축·창호공사 표준계약서, plus an e-contract with consumer-protection clauses.
  - Delay compensation is up to **200,000원 per day**.
  - Covered vendors get a "책임보장" badge and priority exposure. Non-covered vendors show a warning.
  - All registered contractors must set a warranty period of **at least 1 year**.
  - Internal stats: ≥95% satisfied reviews and a 0.8% dissatisfaction rate over 3 years.
  
  — [이코노미스트, 2023-06-23](https://economist.co.kr/article/view/ecn202306230017)
- Results after introducing 책임보장 + the standard contract in 2023:
  - 오늘의집's construction transaction value nearly doubled in 2024, and cumulative value passed **1조원**.
  - 2024 revenue was 2,879억원 (+22.3%), with a first annual operating profit of 5억7,000만원.
  
  — [유니콘팩토리, 2025-04](https://www.unicornfactory.co.kr/article/2025040919455238744)
- Bucketplace tech blog topics (2025-12 to 2026-10):
  - generalized multilingual retrieval for search (2026-01)
  - in-house search and display ads (2026-01)
  - a "trustworthy metrics & experimentation platform" (XPC, 2026-02)
  - server-driven UI built with Kotlin + HTMX (2026-01)
  - a Feature Store for personalized recommendation (2025-12)
  - DBRE automation, where DB changes go through Git PRs and routine operations are self-service (2026-10)
  - AI self-service data analytics (2026-10)
  - an internal AI app platform, "올리고" (2026-10)
  
  — [Bucketplace Tech blog index](https://www.bucketplace.com/culture/Tech/)
- 오늘의집 image search usage rose 430% (2026-02). Searches for 3D/AI interior terms rose about 24× year over year. — [디지털데일리](https://www.ddaily.co.kr/page/view/2026021117004423417); [바이라인네트워크](https://byline.network/2026/01/19_ohouse/)
- 오늘의집 search job posts describe:
  - query correction
  - filter and option refinement
  - search-dictionary operations to improve morphological-analysis quality
  
  — [Wanted](https://www.wanted.co.kr/wd/139631); [inthiswork](https://inthiswork.com/?p=404546)
- 오늘의집 has a dedicated 정보보안팀 covering intrusion defense through security-law compliance. — [Wanted job post](https://www.wanted.co.kr/wd/355928)

**숨고 (브레이브모바일)**
- 숨고's "3대 신뢰 프로젝트", run by a 신뢰 구축 TF and announced 2026-03-19:
  - **Name mismatch:** if the 사업자등록증 representative name ≠ the account's verified name, the vendor must submit a 위임장 and supporting documents.
  - **Automated checks:** public-data API checks of 전문건설업 등록 정보, 사업자등록번호 and 대표자명.
  - **Ongoing checks:** periodic re-verification after approval, to catch 폐업, administrative sanctions, or 영업정지.
  - **Scam checks:** account numbers and phone numbers in chat are checked against 경찰청 더치트, with a caution notice shown. 숨고 has also linked to the police "사이버 사기 신고 이력 조회" service since 2025.
  - **Guarantees:** the 숨고페이 refund guarantee rises from 100만원 to **500만원**. A property guarantee covers up to **1,000만원**.
  - **Planned for 2H 2026:** a dedicated dispute-care counselor system and standard contracts.
  
  — [바이라인네트워크](https://byline.network/2026/03/19_291873/); [머니투데이](https://www.mt.co.kr/future/2026/03/19/2026031909204971718)
- 숨고 business model:
  - The customer writes one 요청서, multiple pros send quotes, and the customer compares them.
  - Pros pay about **3,000–4,000원 per quote**, charged when the quote is sent, win or lose. The charge is refunded as bonus cash if the customer doesn't open the quote within 48h.
  - There is no transaction commission.
  - Revenue was 458억원 in 2023 (first profit, 53억원 OP) and 624억원 in 2024 (OP 137억원, about 22% margin).
  - The page cites "AI 추천" and portfolio-based matching.
  
  — [데모데이 BM 분석](https://demoday.co.kr/bm-analysis/104) [3rd-party]
- 숨고's App Store text: "숨고페이로 결제 시, 서비스 품질에 문제가 발생하면 숨고에서 도움을 드려요". — [App Store](https://apps.apple.com/es/app/%EC%88%A8%EA%B3%A0-%EC%9D%B4%EC%82%AC-%EC%B2%AD%EC%86%8C-%EC%B7%A8%EB%AF%B8-%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4-%EC%A0%84%EB%AC%B8%EA%B0%80-%EC%B0%BE%EA%B8%B0/id1250771188?l=ca) [snippet]
- In 2020, a change that charged pros merely for proposing caused user backlash. — [일간스포츠, 2020](https://isplus.com/article/view/isp202004240015) **[old]**
- 숨고 Tech works in cross-functional squads and documents in JIRA/Confluence. Mobile engineering is React Native/React, per job posts. — [숨고 brunch Tech team post](https://brunch.co.kr/@soomgo/1198); [theteams listing](https://www.theteams.kr/recruit/wanted/29745) [snippet]

**집닥 / 아파트멘터리 / market**
- 집닥's app shows whether each selected contractor carries 보증보험 (guarantee insurance). — [App Store, 집닥](https://apps.apple.com/co/app/%EC%A7%91%EB%8B%A5-%EA%B0%84%ED%8E%B8%EC%95%88%EC%8B%AC-%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4/id1250743410) [snippet]
- 집닥 emphasized managing A/S itself rather than just connecting customers to vendors. — [비즈워치, 2019](https://news.bizwatch.co.kr/article/real_estate/2019/09/10/0020) **[old]**
- 집닥 claims more than 2,000억원 cumulative construction transaction value and about 1,800 partner contractors. The base year of the figures is unclear. — [인사이트](https://www.insight.co.kr/news/225305) [snippet]
- Interior platform shutdowns:
  - 집꾸미기: revenue fell from 124억 (2019) to 8.7억 (2023); closed 2025-03.
  - 알렛츠: closed 2024-08.
  - 문고리닷컴: bankrupt 2024-07.
  - 하우스앱: closed 2023-02.
  - 어반베이스: closed 2024-07.
  
  아파트멘터리 grew by focusing on "인테리어 시장의 정보 불균형 해소". Its NPS passed +90 in 2024-03. — [유니콘팩토리, 2025-04](https://www.unicornfactory.co.kr/article/2025040919455238744)

### Inferences
- 믿집's core value is public-price-based reference quotes plus line-by-line comparison. That sits close to 오늘의집 스탠다드 ("margin disclosed") and 아파트멘터리's "정보 불균형 해소". But every successful comparable pairs transparency with a **trust/guarantee layer**: a standard contract, a 1-year A/S rule, insurance/guarantee badges, and dispute mediation. 믿집 has none yet beyond admin approval of a certificate.
- 숨고's 2026 measures are the closest blueprint for 믿집's vendor-verification module, and most can be built cheaply with public APIs (§8).
- The 오늘의집 engineering platforms (experimentation, feature store, retrieval search) are scale-driven. They are not evidence that 믿집 needs more infrastructure. The one transferable engineering practice is "DB changes via Git PR", meaning migrations reviewed in PRs.
- 숨고's quote-charging history shows that vendor-side economics (who pays per quote) are a product risk. 믿집 has no vendor fee yet, which is fine for a demo.

### Gaps
- No public tech-stack write-ups were found for 숨고 backend/infra, 집닥, 아파트멘터리, 반셀끝, or 다방/직방 interior. Job posts surfaced only frontend/mobile stacks.
- No 당근 sources specific to search, chat, or notifications were collected in this pass.
- The details of 집닥's 안심예치 (escrow-like deposit) could not be confirmed. Searches returned no official page.
- No source showed which notification channels (알림톡 vs push) 오늘의집/숨고 use. That they use 알림톡 is an assumption, not verified.

---

## 2. Global comparables (Thumbtack, Angi/HomeAdvisor, Houzz, Checkatrade) — quotes, verification, lead routing, trust & safety

### Takeaway
Global marketplaces converge on four things:
1. Layered vendor verification: ID, background, insurance, licences, with ongoing re-checks.
2. Money-back and property-damage guarantees with claim windows.
3. Review moderation that combines ML and human reviewers.
4. Honest claims about lead quality. The FTC fined HomeAdvisor over misrepresented leads.

Architecturally, Thumbtack moved from a PHP/Postgres monolith to services only at large scale. That supports 믿집's modular-monolith choice.

### Cited Findings
- Thumbtack background and guarantee policy:
  - Every new account owner must clear a third-party criminal check, re-run annually with monitoring in between.
  - The badge covers the account holder, not necessarily the worker who arrives.
  - The guarantee covers up to **$2,500** money-back (claim within 45 days) and up to **$100,000** property damage (claim within 14 days).
  
  — [Thumbtack Safety](https://www.thumbtack.com/safety) [snippet]; [Thumbtack Safety Guidelines](https://www.thumbtack.com/safetyguidelines/) [snippet]
- One consumer review says Thumbtack denied a claim by reclassifying damage and didn't verify a handyman's liability insurance. This is an anecdote. — [ConsumerAffairs](https://www.consumeraffairs.com/homeowners/thumbtack.html?page=3) [3rd-party]
- Thumbtack's architecture:
  - It moved from an async bidding queue to synchronous "instant" matching, where a request becomes a search query against an index of pros. — [Software Engineering Daily SED468, 2017](https://softwareengineeringdaily.com/wp-content/uploads/2017/11/SED468-Thumbtack-Marketplace-Evolution.pdf) **[old]**
  - Infrastructure evolved from a PHP/PostgreSQL monolith with self-managed Hadoop to Dockerized services plus managed data infrastructure (BigQuery, Pub/Sub, ECS, Airflow). — [QCon SF talk](https://archive.qconsf.com/node/71046); [podcast](https://podcast.app/thumbtack-infrastructure-with-nate-kupp-e97221528) **[old]**
  - A job listing mentions Elasticsearch autocomplete plus a policy re-ranking layer. — [startup.jobs listing](https://startup.jobs/backend-engineer-marketplace-thumbtack-5504025) [snippet]
- Checkatrade vetting:
  - Up to **12 checks** before joining, including ID, company history, CCJ (county court judgment) and adverse-media screening, with continued checks during membership.
  - It asks for proof of public liability insurance and of required qualifications, e.g. Gas Safe registration.
  
  — [Checkatrade trust page](https://www.checkatrade.com/blog/trust/) [snippet]; [Checkatrade approved & guaranteed](https://www.checkatrade.com/blog/trade/checkatrade-approved-and-guaranteed/) [snippet]; [Fixflo × Checkatrade](https://www.fixflo.com/blog/how-vetting-builds-trust-fixflo-and-checkatrade) [snippet]
- An older description of Checkatrade adds an interview and **5 references**. — [electriciancourses4u](https://electriciancourses4u.co.uk/blog/can-customers-trust-trade-directories-to-find-a-trusted-tradesperson/) [3rd-party, old]
- Angi review moderation, per a third-party guide:
  - ML models scan reviews for fraud and send suspicious ones to human moderators.
  - Red flags include identical text, many reviews from one IP, and accounts with no prior activity.
  - Pros can respond publicly and flag reviews.
  
  — [ExpertBeacon guide](https://expertbeacon.com/an-experts-guide-to-angi-reviews-earning-5-stars-the-right-way/) [3rd-party]
- The FTC notes that companies use automated systems plus human moderators, and expects "reasonable processes" to verify that reviews are genuine. — [FTC](https://www.ftc.gov/node/78110)
- A UK government impact assessment estimated **about 11–15%** of e-commerce product reviews are fake despite moderation. — [UK DBT fake reviews impact assessment](https://assets.publishing.service.gov.uk/media/650c015c52e73c000d9425b6/fake-reviews-consultation-impact-assessment.pdf)
- FTC v. HomeAdvisor (an Angi affiliate):
  - The complaint alleged false or unsubstantiated claims about lead quality and source since about 2014, and overstated lead-to-job conversion.
  - The final order requires up to **$7.2M** in redress and bans misleading lead claims. Finalized in 2023 by a 3-0 vote.
  - Pros reportedly got leads outside their service area or for services they don't offer.
  
  — [FTC final order](https://www.ftc.gov/node/80884); [FTC press release 2023-01](https://ftc.gov/news-events/news/press-releases/2023/01/ftc-order-requires-homeadvisor-pay-72-million-stop-deceptively-marketing-its-leads-home-improvement); [ABC15](https://www.abc15.com/homeadvisor-to-pay-7-2-million-for-misleading-gig-contractors) **[old]**
- Houzz Pro markets AI-backed estimates generated from voice or text prompts, plus templates and assemblies. Its app lists AI estimates with local pricing data and automated takeoffs from plans. — [Houzz estimating page](https://www.houzz.com/for-pros/feature-estimating.md); [Houzz Pro App Store](https://apps.apple.com/app/id1488002482) [vendor marketing]

### Inferences
- 믿집's "3 AI-recommended vendors" is functionally lead routing. The HomeAdvisor case shows that claims about recommendation quality ("verified", "best match") create liability. 믿집 should show the **basis** of each recommendation (region, trade, rating, response rate) and avoid guarantee-like wording.
- Thumbtack's re-verification cadence (annual) and Checkatrade's ongoing checks match 숨고's 2026 periodic re-verification. "Approve once" is the industry anti-pattern.
- Houzz Pro's AI estimate generation is the vendor-side analogue of 믿집's 표준견적서. This supports making the reference estimate a **pre-filled template** the vendor edits, which is likely already planned for vendor quote writing.

### Gaps
- No Angi or Thumbtack primary documentation on review-verification mechanics was retrieved, and the Checkatrade page returned 403.
- No MyBuilder sources were collected.
- No 2024–2026 architecture write-ups from Angi or Houzz were found.

---

## 3. AWS Well-Architected / startup guidance — which pillars small single-instance setups commonly miss

### Takeaway
For small startups, the most commonly flagged gaps are:
- **Untested backups**. Well-Architected rates this risk "Medium" and gives a step-by-step restore-test procedure.
- **Single-AZ databases and a single instance**, which are accepted trade-offs here.
- **Account hygiene**: root MFA, no root keys, CloudTrail, Budgets, GuardDuty.
- **Burstable-instance surprises.** t4g.small defaults to *unlimited* mode, so CPU spikes become bill surprises rather than slowdowns.

### Cited Findings
- **REL09-BP04: periodically restore backups to verify integrity.**
  - Anti-patterns: restoring without querying data, assuming a backup exists, assuming restore time fits the RTO, and restoring without a runbook.
  - "Level of risk exposed if this best practice is not established: **Medium**."
  - Steps: identify data sources → define validation criteria → set RTO/RPO → test restore → validate → measure time → notify → automate periodically.
  - RDS supports PITR.
  
  — [AWS Well-Architected Reliability Pillar REL09-BP04](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html)
- AWS Backup has scheduled **restore testing**. The validation hook is an EventBridge rule on restore-job COMPLETED that triggers a Lambda to query fixture data. Test resources are deleted after the validation window. — [AWS News Blog](https://aws.amazon.com/blogs/aws/automatic-restore-testing-and-validation-is-now-available-in-aws-backup/); [AWS Backup docs: restore testing validation](https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing-validation.md)
- Practitioner lists of common Well-Architected findings:
  - "Backups exist but have never been restored"
  - no Multi-AZ for databases ("one CLI command")
  - no auto-scaling
  - no timeouts or circuit breakers
  
  — [dev.to/instadevops](https://dev.to/instadevops/how-to-run-an-aws-well-architected-review-the-6-pillars-and-common-findings-3p15) [3rd-party]; [OneUptime 2026-02](https://oneuptime.com/blog/post/2026-02-12-run-well-architected-review-aws-workload/view) [3rd-party]
- RDS automated-backup retention is configurable from 1 to 35 days, with PITR inside that window. A final snapshot taken at deletion **does not expire**. Retained automated backups do expire. — [RDS User Guide: backups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html); [RDS: retaining automated backups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.Retaining.html)
- **AWS Startup Security Baseline (2022-05-13)** **[old but current guidance]**
  - Account controls: root MFA, IAM password policy, CloudTrail logs delivered to S3, Budgets alerts, GuardDuty, Trusted Advisor.
  - Workload controls: scoped app secrets, minimized access routes, encryption in transit and at rest, RDS/EBS encryption, VPC endpoints, Systems Manager for remote sessions.
  
  — [AWS Startups Blog: SSB](https://aws.amazon.com/blogs/startups/aws-startup-security-baseline-day-one-recommendations-to-secure-your-account-and-workload)
- Community "first hour" guides add four points:
  - Use a hardware key or passkey for root.
  - Use IAM Identity Center instead of long-lived IAM user keys, described as "the most common way credentials leak".
  - Set a budget alert before building anything.
  - In one rollout, GuardDuty flagged outside SSH attempts, which led the team to drop port 22.
  
  — [AWS Builder Center: first hour](https://builder.aws.com/content/3KDsT0KIsMX5GvD3DWhufex9MXA/securing-a-new-aws-account-the-first-hour); [AWS Builder Center: almost free](https://builder.aws.com/content/3KN4kLaajwh3j9BMZ2ywOoBcvsM/secure-a-brand-new-aws-account-in-minutes-almost-free) [community]
- **t4g.small burst credits:**
  - 2 vCPU, earns **24 credits/hour**, max **576** accrued, baseline **20% per vCPU**.
  - T4g defaults to **Unlimited** mode.
  - In Standard mode an instance that runs out of credits drops to baseline. In Unlimited mode, 24h-average usage above baseline is billed at a flat extra rate per vCPU-hour.
  
  — [EC2 docs: burstable credits](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html); [EC2 docs: unlimited mode](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances-unlimited-mode-concepts.html)
- **Metrics to watch:** CPUCreditBalance, CPUSurplusCreditBalance, CPUSurplusCreditsCharged. In standard mode, a throttled instance "feels broken" from inside and steal time rises. — [StackHarbor explainer](https://stackharbor.com/en/knowledge-base/awsfix-t3-cpu-credits-slowdown/) [3rd-party]

### Inferences
- For 믿집, the Well-Architected gaps are:
  - **Reliability:** no restore drill or RTO/RPO defined. Single-instance and single-AZ risk is acceptable if documented.
  - **Security:** account baseline not explicitly listed in the proposal. CloudTrail, GuardDuty, Budgets and root MFA are missing from the component list.
  - **Cost:** no Budgets alarm, and no alarm on `CPUSurplusCreditsCharged`.
  - **Operational excellence:** no runbook or staging environment.
- The proposal already uses SSM for deploys. Closing port 22 entirely (Session Manager only) matches SSB guidance at zero cost.
- Next.js 16 + FastAPI + arq + Redis + Caddy share 2 vCPUs on one burstable instance. AI-agent calls are I/O-bound, but image handling, Next.js SSR or ISR rebuilds, and PDF or report generation are CPU-heavy and could burn credits. Alarms on credit metrics are cheap insurance.

### Gaps
- No primary source was retrieved for t4g.small memory (2 GiB is the commonly known figure and is unverified here) or for current Seoul-region prices of t4g, RDS, GuardDuty or CloudWatch.
- No AWS statistic on "most common HRIs" exists publicly. Only practitioner lists were found.
- The RDS backup-storage free allowance was not verified.

---

## 4. Failure stories from small teams on single-EC2 / Docker Compose — what broke and what they added

### Takeaway
The recurring failure modes are:
1. Unbounded Docker logs filling the disk. The default json-file driver has no size cap.
2. Lost Caddy `/data` volumes causing Let's Encrypt rate-limit lockouts.
3. Silently failing backups. GitLab 2017: five backup mechanisms, none working.
4. Config and operator errors, which cause about half of public outages.

The fixes are cheap: log caps, persisted cert storage, monitored backups with restore drills, and staged config changes.

### Cited Findings
- **Docker logs filling the disk:**
  - The json-file driver sets no max-size or max-file by default, so logs grow indefinitely. Restart loops and stack-trace spam accelerate the growth.
  - Logs live in `/var/lib/docker/containers/<id>/<id>-json.log`, so `docker system df` can look fine while the disk is full.
  - Fix: set `max-size`/`max-file`, or use the `local` driver, in daemon.json or per Compose service. The settings apply only to recreated containers.
  - Truncate the log file; don't delete it.
  
  — [Netdata guide](https://www.netdata.cloud/guides/docker/docker-log-rotation/); [Canadian Web Hosting](https://blog.canadianwebhosting.com/docker-logs-filling-disk/); [OneUptime 2026-02](https://oneuptime.com/blog/post/2026-02-08-how-to-limit-docker-container-log-file-size/view) [3rd-party]
- **Caddy and Let's Encrypt:**
  - Not persisting Caddy's `/data` in Docker discards certificates and keys on every recreate, and repeated re-issuance hits rate limits.
  - LE's failed-validation limit (5 per account per hostname per hour) is "tight". A forum post reports it being hit.
  - Plesk cites 50 certificates per registered domain per week.
  - Use LE staging when testing.
  
  — [Caddy community: rate limit after container update](https://caddy.community/t/lets-encrypt-rate-limit-after-update-of-container/5136); [Caddy community: certs re-requested](https://caddy.community/t/docker-caddy-request-for-certs-having-valid-ones/9303); [Caddy community: too many failed authorizations](https://caddy.community/t/too-many-failed-authorizations-recently/20629) [forum; some posts old]
- **GitLab 2017-01-31:**
  - An engineer deleted the primary DB directory on the wrong server, losing about 6 hours of data (about 5,000 projects and about 700 user accounts affected).
  - None of the 5 backup and replication methods worked reliably. Scheduled pg_dump had been failing silently because of a version mismatch, failure emails were rejected by email security (DMARC), and disk snapshots were not enabled.
  - Recovery came from an ad-hoc manual copy.
  
  — [GitLab postmortem](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/); [The Register](https://www.theregister.com/2017/02/01/gitlab_data_loss/) **[old]**
- **Dan Luu's postmortem review:**
  - About 50% of "global outage" postmortems found by search were caused by config changes. Jim Gray (1985) attributed 42% of failures to operators, configuration and maintenance.
  - 92% of critical failures in a 2014 study came from incorrectly handled errors, and 23% of those were catchable with statement coverage or review.
  - Missing monitoring is a common contributing factor.
  
  — [danluu.com/postmortem-lessons](https://danluu.com/postmortem-lessons/) **[old]**; [danluu/post-mortems README](https://raw.githubusercontent.com/danluu/post-mortems/master/README.md)
- **Single-VPS Compose production checklists:**
  - healthchecks, restart policies, named volumes, isolated networks, secret management, log limits
  - memory and CPU limits to avoid OOM cascades
  - image pinning and rollback procedures
  - three volume-backup strategies: tar snapshots, DB-native dumps, encrypted automated backups
  
  Compose is described as "perfect for small to medium infrastructures (up to ~10-20 containers on one VPS)". — [verycloud docs](https://verycloud.fr/en-US/docs/article/docker-compose); [valebyte guide](https://valebyte.com/es/guides/docker-en-un-vps-desde-cero-instalacion-compose-actualizaciones-y-copias-de-seguridad-de-volumenes/) [3rd-party]

### Inferences
- 믿집-specific must-dos:
  - Set a log cap in `daemon.json` (e.g. `local` driver) baked into the instance setup.
  - Mount Caddy `/data` and `/config` on a named volume. Consider a backup of that volume, or an EBS snapshot.
  - Use `mem_limit` for Next.js and FastAPI so one OOM doesn't take Redis down.
  - Add CloudWatch agent disk and memory alarms. Default EC2 metrics don't include disk or memory.
- RDS removes most of the "DB on the box" risk. Redis (the arq queue) is still on the box. 믿집's AGENTS.md already says Redis holds only disposable data and that services write a `jobs` row in Postgres before enqueueing. The remaining gap is a small **sweeper** that re-enqueues `jobs` rows left pending after a Redis or host restart. Jobs must be idempotent for that to be safe.
- GitLab's "alerts silently rejected" lesson applies to SES. Alert e-mails sent through SES from the same account can fail along with the application, so use a second channel for alerts (e.g. a Slack/Discord webhook or SNS to SMS).

### Gaps
- No HN/Reddit 2024–2026 thread specifically about a small team losing data on single-EC2 Compose was retrieved. The evidence is vendor guides and older canonical postmortems.
- Let's Encrypt's official current rate-limit page was not fetched. The figures above come from forum and Plesk sources.

---

## 5. Production-readiness checklist items for small SaaS (2025–2026), including Korean legal duties

### Takeaway
Generic checklists converge on:
- backups with a restore test
- error tracking
- uptime monitoring and alerting
- rollback and health checks
- secrets outside code

Korea adds concrete legal items for a broker platform:
- 통신판매중개자 고지 on relevant screens
- disclosure of seller (vendor) identity information
- a 개인정보 처리방침 disclosing auto-collection devices (cookies)
- 접속기록 retention of at least 1 year for staff and admin access to personal-data systems, with an inspection procedure in the internal management plan

### Cited Findings
- **Launch checklist (generic):** automated and tested DB backups, uptime monitoring, alerting, on-call contact, tested rollback, health-check endpoint, error tracking, log aggregation, alert rules, secrets outside code. — [production-readiness skill checklist](https://skills.cat/skills/simplerick0/com-ackhax-configs/production-readiness) [3rd-party]
- **Operational readiness:** test and validate DR/BCP and consider RPO/RTO. The list is non-exhaustive. — [Rackspace](https://www.rackspace.com/es/blog/do-you-have-an-operational-readiness-checklist)
- **Error tracking:** Sentry's free Developer plan is commonly listed as 5,000 errors per month for 1 user. One tracker claims 50K errors after an Aug-2025 change, so the sources conflict. Team plan is about $26/month. — [Costbench](https://costbench.com/software/developer-tools/sentry/free-plan/); contradicted by [agentdeals](https://agentdeals.dev/vendor/sentry) [3rd-party]
- **Uptime monitoring:** UptimeRobot's free tier is 50 monitors at 5-minute intervals with 1 basic status page, but it has been **non-commercial only since Oct 2024**. Alternatives: HetrixTools (15 monitors at 1-minute intervals, free). — [notifier.so 2026](https://notifier.so/guides/uptimerobot-pricing-2026/); [productcompass](https://www.productcompass.pm/p/uptimerobot-alternatives) [3rd-party]
- **SES:**
  - Account status values: Healthy / Under review / Pending end-of-review decision / Sending paused / Pending sending pause. Sending can be paused if issues aren't resolved during review.
  - Bounces raise suspension risk "in or out of the sandbox".
  - Production-access requests should describe bounce and complaint handling, e.g. SNS notifications and automatic removal of affected addresses. Requests can be denied without a reason.
  
  — [SES reputation dashboard docs](https://docs.aws.amazon.com/ses/latest/dg/reputation-dashboard-dg.html); [AWS Messaging Blog: mailbox simulator](https://aws.amazon.com/blogs/messaging-and-targeting/introducing-the-amazon-ses-mailbox-simulator); [OneUptime: leaving sandbox](https://oneuptime.com/blog/post/2026-02-12-move-amazon-ses-out-of-sandbox/markdown); [re:Post denial thread](https://repost.aws/ko/questions/QUl1TP2B3cSFSLXnPtXHnG-w/been-denied-production-access-for-transactional-emails-and-have-no-idea-what-else-to-do)
- **Abuse and rate limiting:**
  - Turnstile tokens must be verified server-side through siteverify, because test sitekeys always pass. The free plan doesn't require Cloudflare DNS.
  - Redis-backed FastAPI limiters exist, e.g. `fastapi-user-limiter`. Redis shares one counter across workers.
  
  — [tech-insider Turnstile guide 2026](https://tech-insider.org/?p=25269) [3rd-party]; [PyPI fastapi-user-limiter](https://pypi.org/project/fastapi-user-limiter); [viblo slowapi post](https://viblo.asia/p/rate-limiting-trong-fastapi-tu-khong-co-gi-den-production-ready-phan-1-pPLkN3y8JRZ)
- **Korea: 통신판매중개자 duties**
  - The broker must tell users it is not the selling party on screens where it shows ads, delivers contract documents, or provides payment. Without this notice it can share joint liability with the seller.
  - A court accepted a footer "통신판매 당사자가 아님" notice as sufficient.
  - A National Assembly amendment would impose joint liability where the platform acts like a party.
  
  — [lilys.ai 전자상거래법 교육 요약](https://lilys.ai/ko/notes/online-business-20251205/e-commerce-platform-related-business-duties) [3rd-party]; [로톡 판례 사례](https://www.lawtalk.co.kr/posts/115661); [국회 입법의견 자료](https://opinion.lawmaking.go.kr/file/download/8094187/TLS0HX1X4OJC1D9A8T4C)
- **Korea: seller identity disclosure.** 공정위 sanctioned 당근마켓 under 전자상거래법 제20조 제2항 for not providing seller 성명·주소·상호·사업자등록번호 etc.: a correction order plus a 100만원 fine. — [딜사이트](https://dealsite.co.kr/articles/137678)
- **Korea: 접속기록.**
  - Access records of people who access a 개인정보처리시스템 (excluding data subjects) must be kept **at least 1 year**. The period is **2 years** if the system handles ≥50,000 data subjects, 고유식별정보 or 민감정보.
  - Since the 2025-10-31 amendment, the inspection cycle and method are set in the internal management plan, replacing the fixed "monthly".
  - Records must be protected from forgery, alteration and loss.
  
  — [IT위키: 안전성 확보조치 기준 제8조](https://itwiki.kr/w/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98_%EC%95%88%EC%A0%84%EC%84%B1_%ED%99%95%EB%B3%B4%EC%A1%B0%EC%B9%98_%EA%B8%B0%EC%A4%80_%EC%A0%9C8%EC%A1%B0) [3rd-party wiki]
- **Korea: ISMS.**
  - ISMS (정보통신망법 제47조) is mandatory based on prior-year results: e.g. ≥100억원 ICT-service revenue, or ≥1M average daily users over the last 3 months.
  - ISMS-P itself is voluntary.
  
  — [바이라인네트워크 2025-11](https://byline.network/2025/11/20-518/); [IT위키: ISMS-P 인증 대상](https://www.itwiki.kr/w/ISMS-P_%EC%9D%B8%EC%A6%9D_%EB%8C%80%EC%83%81) [3rd-party]
- **Korea: 처리방침 작성지침.** PIPC revised its 개인정보 처리방침 작성지침 in 2024-04, making the online 행태정보 notices more specific. — [보안뉴스](https://m.boannews.com/html/detail.html?idx=129433)

### Inferences
- 믿집 shows vendor profiles and quotes, and transmits quote documents. So the vendor detail and quote-comparison screens should carry:
  - a 통신판매중개자 notice
  - vendor 상호 / 대표자 / 사업자등록번호 / 주소 / 연락처, as the 당근 sanction shows
  
  Cost is near zero, but if this is missing at launch it is a legal exposure.
- Admin screens that view member or vendor personal data make 믿집 a 개인정보처리시스템 with 개인정보취급자 (admins). An **admin audit log**, recording who viewed, exported or changed what and when, kept ≥1 year in tamper-resistant storage, is effectively a legal requirement, not a nice-to-have.
  - Suggested storage: a Postgres append-only table plus periodic export to S3 with Object Lock or a separate bucket.
- ISMS is not triggered at 믿집's scale.
- Status page: at a few hundred users, a free status page (e.g. the uptime tool's) plus a one-page runbook covers demo and early launch.

### Gaps
- The primary 법령 text (국가법령정보센터) for 안전성 확보조치 기준 was not fetched. The figures come from a wiki summary.
- The exact SES bounce and complaint thresholds were not shown in the docs page retrieved. Commonly cited values (about 5%/10% bounce, 0.1%/0.5% complaint) are **unverified here**.
- No source was found on whether 믿집 must file 통신판매업 신고 as a broker if it never takes payment. This needs legal confirmation.

---

## 6. Product analytics and feedback options under Korean privacy expectations; consent banners in Korea

### Takeaway
Korean law (개인정보보호법 제30조) clearly requires **disclosing** cookies and auto-collection in the 처리방침 and how to refuse them. Whether a prior-consent banner is legally required for first-party analytics is **disputed**. PIPC's behavioral-advertising guidance is aimed at ad targeting and was still contested in 2025.

Low-risk choice for 믿집: first-party product analytics such as the PostHog free tier, no ad pixels, a cookie notice and opt-out, and a 처리방침 section covering the analytics vendor and any 국외 이전.

### Cited Findings
- **Is consent required?**
  - One analysis reads 제30조 as requiring disclosure of installation, operation and refusal methods of auto-collection devices in the 처리방침, but **not** explicitly requiring separate consent for cookies.
  - Another source calls Korea "opt-in" without citing law.
  - PIPC fined Google 600억 and Meta 300억 in 2022-09 for collecting 행태정보 without consent for targeted ads. Both sued, partly because 행태정보 lacks an explicit statutory definition.
  
  — [비즈한국](https://www.bizhankook.com/bk/article/26498); [위픽레터](https://letter.wepick.kr/post/1815) [3rd-party]
- **PIPC policy on behavioral data.** PIPC announced a policy (2024-01-31) to strengthen protection of online 행태정보 used for targeted ads and clarify advertisers' responsibilities. 참여연대 demanded the guideline be scrapped in 2025-05 as industry-biased. — [이투데이](https://www.etoday.co.kr/news/view/2327015); [참여연대](https://peoplepower21.org/publiclaw/1992345)
- **PostHog Cloud free tier:**
  - About 1M events per month, 5K session replays, 1M feature-flag requests, unlimited seats.
  - Overage is usage-based.
  - Self-hosting is free (MIT, Docker Compose) but the team runs the infrastructure.
  - One source conflicts on replay counts.
  
  — [CubeAPM PostHog review](https://cubeapm.com/blog/posthog-pricing-and-review/); [Costbench PostHog vs Amplitude 2026](https://www.costbench.com/compare/posthog-vs-amplitude/) [3rd-party]
- **Microsoft Clarity:**
  - Free.
  - Since **2025-10-31**, Microsoft requires consent signals for EEA, UK and CH visitors. Without them, Clarity runs in a limited mode where each page view is a separate session.
  - Clarity uses its own Consent V2 API.
  
  — [Pandectes 2025](https://pandectes.io/blog/microsoft-clarity-and-gdpr-what-you-need-to-know-in-2025/); [Seers](https://seers.ai/blogs/how-to-enable-clarity-consent-mode/) [3rd-party]

### Inferences
- **Recommended for 믿집:**
  - PostHog Cloud, free tier: funnels such as estimate → vendor pick → quote request → measurement → confirm, plus surveys. This easily fits 1M events per month at a few hundred users.
  - Alternatively GA4, which is also free but ad-ecosystem-adjacent and invites more consent scrutiny.
  - Avoid Clarity or session replay on screens showing addresses, 동·호수 or quotes, or mask them, since apartment address plus unit area is personal data.
- A banner offering "analytics cookies: accept/decline" is cheap (about half a day). It aligns with the conservative reading and with how most global sites behave.
- PostHog US/EU hosting means personal data is processed abroad. The 처리방침 should list the vendor, its country and the items involved. This is inferred from general PIPA 국외이전 rules and was not sourced in this pass.

### Gaps
- No primary PIPC guideline text on first-party analytics cookies was retrieved.
- Amplitude's free-tier figures were not verified.
- PostHog's official pricing page didn't render, so its figures come from secondary sources.
- No Korea-hosted analytics option (e.g. NHN or Naver-based) was assessed.

---

## 7. Search: is Postgres full-text/trigram enough for vendor search at this scale vs OpenSearch/Meilisearch?

### Takeaway
At 믿집's scale (hundreds to low thousands of vendors), vendor discovery is dominated by **structured filters** (trade, region, rating, availability, price band) plus name matching. Postgres is enough.

The one technical caveat is Korean text:
- Postgres has no Korean tokenization dictionary.
- pg_trgm's 3-character trigrams fit poorly with 2-syllable Korean words.
- RDS has offered **pg_bigm** (bigram index) since 2021.

Dedicated engines (Meilisearch/OpenSearch) only pay off for typo-tolerant as-you-type search over large corpora.

### Cited Findings
- Supabase: if Postgres is already the main DB, its full-text search is "probably easier to integrate than anything else". It provides a cross-engine benchmark repo. — [Supabase blog](https://supabase.com/blog/postgres-full-text-search-vs-the-rest)
- Meilisearch, a vendor claim: "PostgreSQL lacks dictionaries for Chinese, Japanese, Korean… requiring complex tokenization". It also says pg_trgm similarity isn't true typo tolerance. — [Meilisearch vs PostgreSQL](https://www.meilisearch.com/docs/resources/comparisons/postgresql) [vendor]
- pg_trgm details:
  - It uses 3-character groups.
  - Each word is padded with two spaces before and one after.
  - It ignores non-word (non-alphanumeric) characters.
  - GIN/GiST indexes support LIKE/ILIKE, and more trigrams in the query make the index more effective.
  
  — [PostgreSQL docs: pg_trgm](https://postgresql.org/docs/current/pgtrgm.html)
- AWS added **pg_bigm** ("faster full text search… using a bigram index") to RDS for PostgreSQL in 2021-04. Support on current major versions must be checked in the extensions list. — [AWS What's New 2021-04](https://aws.amazon.com/about-aws/whats-new/2021/04/amazon-rds-for-postgresql-supports-new-minor-versions) **[old]**; [RDS PostgreSQL extensions list](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html)
- 오늘의집 runs a dedicated search team with morphological-analysis dictionaries and a generalized retrieval system. Thumbtack used Elasticsearch for autocomplete. Both operate at millions-of-documents scale. — [inthiswork](https://inthiswork.com/?p=404546); [Bucketplace Tech](https://www.bucketplace.com/culture/Tech/); [startup.jobs Thumbtack](https://startup.jobs/backend-engineer-marketplace-thumbtack-5504025) [snippet]

### Inferences
- **Recommendation:** stay on Postgres. Vendor search should be:
  - B-tree or GIN indexes on structured columns (trade, sigungu codes, status)
  - a `pg_trgm` or `pg_bigm` index on vendor name, or plain ILIKE, which is trivially fast on fewer than 10k rows
  - pgvector, already present, for "similar vendors" or recommendation if wanted
  
  Adding Meilisearch would be another container on an already-crowded 2 vCPU host for no user-visible gain at this scale.
- **Revisit triggers:** more than about 50k searchable documents (e.g. portfolios or reviews), a need for typo tolerance or autocomplete, or search latency over 200 ms under load.
- Two-syllable queries like "도배" or "목공" generate few trigrams. If free-text search over descriptions matters, test pg_bigm on RDS PG17 first. This is an inference from the pg_trgm docs and was not benchmarked.

### Gaps
- No benchmark of pg_trgm vs pg_bigm on Korean text was found.
- Whether pg_bigm is available on **RDS PostgreSQL 17** was not confirmed. The fetched extension list was truncated.
- How Hangul is classified as "alphanumeric" under the RDS default locale was not verified.

---

## 8. Trust & safety for a vendor marketplace: verification beyond the certificate, review integrity, reporting/blocking, disputes (Korea)

### Takeaway
A certificate image plus a manual admin check is the weakest form of verification. Korea offers **free public APIs** to automate most of what 숨고 announced in 2026:
- 국세청 사업자 진위확인 / 상태조회, which can catch 휴업 and 폐업
- KISCON 건설업체 정보, to check 실내건축공사업 registration

Add a 1-year 하자보수 field, a 보증보험 badge, a link to the FTC standard contract, verified-transaction-only reviews, a report/block flow, and a dispute intake queue. This brings 믿집 to the industry baseline without payments.

### Cited Findings
- **국세청 사업자등록정보 진위확인 및 상태조회 API** (data.go.kr 15081808):
  - Free, REST/JSON, real-time.
  - Status lookup (계속, 휴업 or 폐업, plus tax type) needs only the business number.
  - Authenticity check validates business number + 개업일자 + 대표자명.
  - Up to 100 records per call. Traffic limits differ by dev or prod account.
  
  — [data.go.kr 15081808](https://www.data.go.kr/data/15081808/openapi.do); [Alchera API guide](https://www.alchera.ai/resource/blog/business-registration-certificate-authentication-api) [3rd-party]
- **국토교통부 KISCON 건설업체정보 API** (data.go.kr 15061362):
  - `ConAdminInfoSvc1/GongsiReg` returns registration disclosure records: company, representative, location, registration date, disclosure type (new, correction, change or withdrawal), industry name, registration number, **business registration number**, phone.
  - Required params are `sDate`/`eDate` (from 2003-01-01). Optional params are province and district.
  - Free. Dev account limited to 10,000 calls. Auto-approval.
  
  — [data.go.kr 15061362](https://www.data.go.kr/en/data/15061362/openapi.do)
- KISCON (kiscon.net) lookup: by 상호 or 사업자등록번호. Confirm that 실내건축공사업 is registered, the business is operating, and there is no administrative-sanction history. — [복덕빵 블로그](https://bokduckbbang.com/blog/%EB%82%B4-%EC%A7%91-%EB%A7%88%EB%A0%A8-%ED%9B%84-%EC%B2%AB-%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4-%EA%B3%B5%EC%82%AC-%ED%95%98%EC%9E%90-%EC%98%88%EB%B0%A9%EC%9D%84-%EC%9C%84%ED%95%9C-%EA%B3%B5%EC%A0%95%EA%B1%B0%EB%9E%98%EC%9C%84%EC%9B%90%ED%9A%8C-%ED%91%9C%EC%A4%80%EA%B3%84%EC%95%BD%EC%84%9C-%EC%9E%91%EC%84%B1%EA%B3%BC-%EA%B1%B4%EC%84%A4%EC%97%85%EB%A9%B4%ED%97%88-%EB%93%B1%EB%A1%9D%EC%97%85%EC%B2%B4-%EC%A1%B0%ED%9A%8C-%EA%B2%BD%EB%A1%9C/) [3rd-party]; [iquest KISCON guide](https://blog.iquest.co.kr/entry/%ED%82%A4%EC%8A%A4%EC%BD%98) [3rd-party]
- **실내건축공사업 registration threshold:**
  - Registration is required when the expected price is **≥1,500만원 (VAT incl.)**. Below that is 경미한 건설공사 (건설산업기본법 제9조).
  - Statutory 하자담보책임 for interior work is **1 year** from completion.
  - Typical 하자보수보증 is 3–5% of the price, with a 하자보수보증보험증권 from e.g. 서울보증보험.
  - Hold at least 10% of the price as 잔금 until inspection.
  - Use the FTC 실내건축·창호 공사 표준계약서 (표준약관 제10074호) with a 지체상금율 of about 1–3/1000 per day.
  
  — [복덕빵 블로그](https://bokduckbbang.com/blog/%EB%82%B4-%EC%A7%91-%EB%A7%88%EB%A0%A8-%ED%9B%84-%EC%B2%AB-%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4-%EA%B3%B5%EC%82%AC-%ED%95%98%EC%9E%90-%EC%98%88%EB%B0%A9%EC%9D%84-%EC%9C%84%ED%95%9C-%EA%B3%B5%EC%A0%95%EA%B1%B0%EB%9E%98%EC%9C%84%EC%9B%90%ED%9A%8C-%ED%91%9C%EC%A4%80%EA%B3%84%EC%95%BD%EC%84%9C-%EC%9E%91%EC%84%B1%EA%B3%BC-%EA%B1%B4%EC%84%A4%EC%97%85%EB%A9%B4%ED%97%88-%EB%93%B1%EB%A1%9D%EC%97%85%EC%B2%B4-%EC%A1%B0%ED%9A%8C-%EA%B2%BD%EB%A1%9C/) [3rd-party; check against 법령]
- **숨고 2026:** name-mismatch 위임장, automated 전문건설업, business-number and representative checks, periodic re-verification, scam-account checks via 더치트, refund guarantee up to 500만원, damage guarantee up to 1,000만원, and dispute counselors plus standard contracts planned for 2H 2026. — [바이라인네트워크](https://byline.network/2026/03/19_291873/)
- **오늘의집:** a mandatory ≥1-year warranty for all contractors, a 책임보장 badge, a standard contract plus e-contract, a mediation team, and 우리은행 payment guarantee. — [이코노미스트 2023](https://economist.co.kr/article/view/ecn202306230017); [ohou.se expert page](https://ohou.se/experts/review/9926) [snippet]
- **집닥** displays each contractor's 보증보험 status. — [App Store, 집닥](https://apps.apple.com/co/app/%EC%A7%91%EB%8B%A5-%EA%B0%84%ED%8E%B8%EC%95%88%EC%8B%AC-%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4/id1250743410) [snippet]
- **Review integrity:** ML plus human moderation, red flags (same IP, identical text, new accounts), vendor responses and flags. The FTC expects "reasonable processes", and about 11–15% of reviews are fake despite moderation (UK estimate). — [ExpertBeacon](https://expertbeacon.com/an-experts-guide-to-angi-reviews-earning-5-stars-the-right-way/) [3rd-party]; [FTC](https://www.ftc.gov/node/78110); [UK DBT IA](https://assets.publishing.service.gov.uk/media/650c015c52e73c000d9425b6/fake-reviews-consultation-impact-assessment.pdf)
- **Messaging and alerts:** a Kakao 알림톡 costs 13원 per message (VAT excl.) on Solapi, falling to 10원 at ≥10k per month and 8원 at ≥100k. Templates must be informational (정보성) and are reviewed; ad-like content is rejected. 친구톡 was marked as ending 2025-12-31. Some vendors offer "검수패스" templates. — [Solapi pricing](https://solapi.com/pricing); [Solapi tiered pricing](https://solapi.com/tiered-pricing); [Solapi 알림톡 guide](https://solapi.com/guides/kakao-ata-guide); [Bizgo blog](https://blog.bizgo.io/?p=1672) [vendor]

### Inferences
- **Verification pipeline for 믿집 vendors:**
  1. At sign-up: call the NTS 진위확인 API (number + 개업일 + 대표자) and the 상태조회 API. Reject 휴업 or 폐업 automatically and pre-fill the admin review.
  2. Flag if the 대표자 name ≠ the 본인인증 name, and request a 위임장 (숨고 pattern).
  3. Optional badge "실내건축공사업 등록": match the business number against KISCON disclosure records. The API is date-range based, so run a nightly arq job that syncs new and changed records into a local table. Because 도배-only jobs are often below 1,500만원, the badge should be *optional*, not a gate.
  4. Monthly arq job re-checking NTS status (100 numbers per call) to auto-suspend closed businesses.
  5. Vendor profile fields: 하자보수 기간 (min 1 year, mirroring 오늘의집's rule), 하자보수보증보험 가입 (upload + badge, 집닥 pattern), standard-contract use (link to FTC 10074).
- **Review integrity at 믿집's scale:**
  - Allow reviews only from owners whose quote was confirmed and whose construction period has ended (verified transaction).
  - One review per job.
  - Vendor public reply.
  - "Report review" plus an admin hide/restore queue with reason codes, which feeds the audit log.
  - Simple heuristics (same IP or device across reviews of the same vendor, review within minutes of sign-up) instead of ML.
- **Reporting/blocking and disputes:** add a "신고" button on vendor profiles and quotes, owner-side "block vendor", and a dispute intake form (category, job, evidence upload to S3) with an admin status queue (접수 → 확인 → 중재 → 종결). Even without payments, this is what 숨고 and 오늘의집 operationalized.
- **Quote anti-circumvention:** 숨고 checks account and phone numbers in chat. 믿집 has no chat, but vendor-written quotes are free text and attachments. A regex flag for phone numbers or bank accounts in quote notes is cheap if the platform cares about off-platform leakage. Whether 믿집 cares is a product decision.

### Gaps
- Whether KISCON offers a direct lookup by business number in the open API (versus date-range disclosures only) was not confirmed. The fetched spec shows only date and area parameters.
- No source covered insurance-verification APIs (e.g. 서울보증보험 certificate validation) in Korea.
- No Korean legal source on review-moderation obligations (e.g. 표시광고법 implications of filtered reviews) was retrieved.
- The legal threshold figures come from a secondary blog and should be checked against 건설산업기본법 시행령.

---

## 9. Prioritised additions to the 믿집 completed architecture (bootcamp demo vs real launch)

### Takeaway
The proposed architecture is **right-sized**. Nothing in the benchmarks argues for load balancers, ElastiCache, OpenSearch or microservices at this scale; Thumbtack only split its monolith at large scale.

The gaps are in the **operational and trust layers**:
- tested backups
- log, disk and credit alarms
- AWS account baseline
- legal screens
- admin audit log
- automated vendor verification
- review, report and dispute flows
- 알림톡 for launch

Most are 0.5–3 days of work and about ₩0 to a few thousand won per month. All effort and cost figures below are the researcher's **estimates**, except where cited.

### Cited Findings
(See §§1–8 for sources. Key anchors:)
- Restore-test risk "Medium" — [REL09-BP04](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html)
- T4g Unlimited by default, 24 credits/hour — [EC2 docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html)
- Docker json-file has no log cap — [Netdata](https://www.netdata.cloud/guides/docker/docker-log-rotation/)
- Startup Security Baseline — [AWS Startups](https://aws.amazon.com/blogs/startups/aws-startup-security-baseline-day-one-recommendations-to-secure-your-account-and-workload)
- NTS API free — [data.go.kr](https://www.data.go.kr/data/15081808/openapi.do)
- KISCON API free — [data.go.kr](https://www.data.go.kr/en/data/15061362/openapi.do)
- 알림톡 13원 per message — [Solapi](https://solapi.com/pricing)
- 접속기록 ≥1 year — [IT위키](https://itwiki.kr/w/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98_%EC%95%88%EC%A0%84%EC%84%B1_%ED%99%95%EB%B3%B4%EC%A1%B0%EC%B9%98_%EA%B8%B0%EC%A4%80_%EC%A0%9C8%EC%A1%B0)
- 당근 seller-info sanction — [딜사이트](https://dealsite.co.kr/articles/137678)
- 숨고 trust TF — [바이라인](https://byline.network/2026/03/19_291873/)
- 오늘의집 책임보장 growth — [유니콘팩토리](https://www.unicornfactory.co.kr/article/2025040919455238744)
- HomeAdvisor lead-claims order — [FTC](https://www.ftc.gov/node/80884)

### Inferences

**A. Add for the bootcamp demo** (high value, low effort; mostly ₩0)

| # | Component / capability | Why (evidence) | Effort (est.) | Cost (est.) |
|---|---|---|---|---|
| A1 | **RDS backup posture + 1 documented restore drill**: retention ≥7 days, deletion protection, manual snapshot before demo day, one PITR restore to a temp instance with a row-count/checksum query, RTO/RPO written down | REL09-BP04 anti-patterns; GitLab's 5 failed backup methods | 0.5 day | Temporary restore instance for about 1h, likely under ₩1,000 (unverified) |
| A2 | **Host guardrails**: Docker log cap (`local` driver or json-file max-size), Caddy `/data` and `/config` on named volumes, `mem_limit` per container, swap file, CloudWatch agent disk and memory metrics | json-file has no cap; Caddy LE rate-limit stories; 2 vCPU shared by 5 containers | 0.5 day | ₩0 to a little (a few custom metrics) |
| A3 | **CloudWatch alarms → non-SES channel** (Slack/Discord webhook or SNS SMS): disk >80%, memory, `CPUCreditBalance` low, `CPUSurplusCreditsCharged` >0, RDS FreeStorageSpace, 5xx rate | Unlimited-mode surprise; GitLab alerts silently lost | 0.5 day | ₩0 to a few thousand per month |
| A4 | **AWS account baseline**: root MFA (passkey), no root keys, IAM Identity Center or roles for the team, CloudTrail trail to S3, AWS Budgets alert, GuardDuty (trial at least), port 22 closed (SSM only), secrets in SSM Parameter Store | AWS SSB; Builder Center guides | 0.5 day | GuardDuty and CloudTrail data events cost a little; Budgets free tier (unverified) |
| A5 | **Automated business check at vendor sign-up**: NTS 진위확인 + 상태조회 called from FastAPI, result shown in the admin approval screen | Free API; 숨고 2026 pattern; certificate-only is the weakest check | 1 day | ₩0 |
| A6 | **Legal/trust screens**: 이용약관, 개인정보 처리방침 (cookie and auto-collection, analytics vendor, retention), 통신판매중개자 notice on vendor and quote screens, vendor identity block (상호·대표자·사업자번호·주소·연락처) | 전자상거래법 notice; 당근 sanction; 제30조 disclosure | 1 day (drafting) | ₩0 |
| A7 | **Admin audit log**: an append-only `admin_audit_log` (actor, action, target, before/after, IP, timestamp) for approvals, member edits and personal-data views | 접속기록 ≥1 year duty; GitOps DB-change ethos at 오늘의집 | 1 day | ₩0 |
| A8 | **Error tracking + uptime check**: Sentry free (FastAPI + Next.js SDKs), plus an external HTTP check with a commercial-allowed free tier | Checklist staples; UptimeRobot free is non-commercial | 2–3 h | ₩0 |
| A9 | **Abuse controls**: Redis rate limits on login, sign-up, quote-request and AI endpoints (AI calls cost money); Turnstile on sign-up and vendor registration, verified server-side | Turnstile guide; Redis limiter libs; OpenAI cost exposure | 0.5–1 day | ₩0 |
| A10 | **AI recommendation transparency**: a "추천 근거" chip on each of the 3 recommended vendors, with no "보장/최고" wording, and a log of the inputs behind each recommendation | FTC v. HomeAdvisor lead-claims order | 0.5 day | ₩0 |
| A11 | **SES readiness**: domain verify, DKIM/SPF/DMARC, SNS bounce/complaint → suppression table, and a production-access request filed early (it can be denied) | SES review and pause statuses; re:Post denial | 0.5 day + AWS lead time | ₩0 at this volume |

**B. Add before a real launch** (or as the "next phase" slide)

| # | Component / capability | Why (evidence) | Effort (est.) | Cost (est.) |
|---|---|---|---|---|
| B1 | **Kakao 알림톡 (+ SMS fallback)** for quote received, measurement scheduled, construction period registered, and vendor approval; via a messaging reseller | Korean users expect 알림톡; templates must be 정보성 and pass review | 2–3 days + template review time | 13원 per message (Solapi): 2,000 messages per month ≈ ₩26,000 + VAT |
| B2 | **Periodic re-verification + KISCON badge**: monthly NTS status re-check (100 per call) with auto-suspend for 휴업 or 폐업; nightly KISCON disclosure sync for an "실내건축공사업 등록" badge; 대표자 name mismatch → 위임장 upload | 숨고 2026 periodic re-verification; Checkatrade and Thumbtack ongoing checks | 2–3 days | ₩0 |
| B3 | **Vendor guarantee fields and badges**: 하자보수 기간 (min 1 year), 보증보험 upload with badge, standard contract (FTC 10074) download, final-payment (잔금) guidance on the confirmed-schedule page | 오늘의집 1-year rule; 집닥 보증보험 display; standard-contract-driven growth | 1–2 days | ₩0 |
| B4 | **Reviews with integrity**: verified-transaction-only reviews, one per job, vendor reply, report → admin moderation queue, simple fraud heuristics, published review policy | FTC "reasonable processes"; 11–15% fake-review estimate; Angi ML + human pattern | 3–5 days | ₩0 |
| B5 | **Report/block + dispute intake (CS back-office)**: report button, owner blocks vendor, dispute ticket with evidence on S3, admin status workflow, SLA timestamps | 숨고 dispute counselors; 오늘의집 mediation team | 3–5 days | ₩0 |
| B6 | **Product analytics with consent**: PostHog Cloud (free 1M events) funnel from estimate to confirmation, cookie notice and opt-out, replay masking on address and quote screens, 처리방침 국외이전 entry | Korean consent ambiguity; Google/Meta fines; PostHog free tier | 1–2 days | ₩0 at this scale |
| B7 | **CDN + image derivatives**: CloudFront in front of public S3 assets (portfolio photos, static files); arq generates thumbnails on upload; keep private files (certificates) on presigned URLs only | Offload a 2 vCPU burstable host; CloudFront + resizing pattern | 1–2 days | A few thousand won per month at this traffic (unverified) |
| B8 | **Automated restore testing + snapshot copy**: monthly AWS Backup restore-testing job with a validation Lambda; cross-region snapshot copy (or one manual monthly) | REL09-BP04 "automate periodically"; AWS Backup restore testing | 1 day | Small (restore runtime + snapshot storage) |
| B9 | **Log retention policy**: CloudWatch Logs retention ≥1 year for app and admin access logs (2 years if ≥50k data subjects), archived to S3 with lifecycle and Object Lock | 접속기록 rules | 0.5 day | Low |
| B10 | **Staging + runbook + status page**: a second Compose project or a small instance for staging, so config changes are staged; a one-page incident runbook (disk full, cert failure, DB restore, OpenAI outage fallback); a public status page | About 50% of outages come from config changes; missing monitoring is a common factor | 2–3 days | Staging instance cost (unverified) |
| B11 | **Search tune-up (stay on Postgres)**: structured filters + trigram or pg_bigm index on vendor name and description after confirming on RDS PG17; pgvector for "similar vendors" | Postgres is enough at this scale; Korean tokenization caveat | 0.5–1 day | ₩0 |
| B12 | **Capacity review**: measure memory and CPU under a demo load; if swap-thrashing or credits drain, move to a larger T or M instance before adding servers | t4g.small baseline is 20% per vCPU | 0.5 day | Instance delta (unverified) |

**C. Consciously still excluded (benchmarks agree)**
- ALB with 2+ instances, ElastiCache, OpenSearch or Meilisearch, Kafka, microservices. Thumbtack and 오늘의집 adopted these only at large scale.
- ISMS: thresholds are ≥100억원 revenue or ≥1M daily users.
- **Payments / escrow (안전결제)** remain the largest *product* gap relative to 오늘의집 (bank payment guarantee) and 숨고 (숨고페이, refund up to 500만원). This is the most important "later" item. It is a business, legal and PG decision, not an infrastructure component.
- RDS Multi-AZ: worth reconsidering for a paid launch (Well-Architected's top reliability finding), but it roughly doubles DB cost. This is a team decision.

### Gaps
- Seoul-region prices for GuardDuty, CloudWatch custom metrics, CloudFront, larger instances and RDS Multi-AZ were not retrieved. Every "cost (est.)" marked unverified needs the AWS Pricing Calculator.
- The effort estimates are researcher judgment for a student team and are not sourced.
- Legal items (통신판매업 신고 for a non-paying broker, 국외이전 disclosure wording, review-moderation law) need confirmation from primary 법령 or counsel.

### Source list (all URLs consulted)
1. https://www.bucketplace.com/culture/Tech/
2. https://www.ddaily.co.kr/page/view/2026021117004423417
3. https://byline.network/2026/01/19_ohouse/
4. https://www.wanted.co.kr/wd/139631
5. https://inthiswork.com/?p=404546
6. https://www.wanted.co.kr/wd/355928
7. https://apps.apple.com/KR/app/id1008236892
8. https://ohou.se/experts/review/9926
9. https://economist.co.kr/article/view/ecn202306230017
10. https://www.unicornfactory.co.kr/article/2025040919455238744
11. https://byline.network/2026/03/19_291873/
12. https://www.mt.co.kr/future/2026/03/19/2026031909204971718
13. https://demoday.co.kr/bm-analysis/104
14. https://brunch.co.kr/@soomgo/1198
15. https://www.theteams.kr/recruit/wanted/29745
16. https://apps.apple.com/es/app/%EC%88%A8%EA%B3%A0-%EC%9D%B4%EC%82%AC-%EC%B2%AD%EC%86%8C-%EC%B7%A8%EB%AF%B8-%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4-%EC%A0%84%EB%AC%B8%EA%B0%80-%EC%B0%BE%EA%B8%B0/id1250771188?l=ca
17. https://isplus.com/article/view/isp202004240015
18. https://apps.apple.com/co/app/%EC%A7%91%EB%8B%A5-%EA%B0%84%ED%8E%B8%EC%95%88%EC%8B%AC-%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4/id1250743410
19. https://news.bizwatch.co.kr/article/real_estate/2019/09/10/0020
20. https://www.insight.co.kr/news/225305
21. https://www.data.go.kr/data/15081808/openapi.do
22. https://www.alchera.ai/resource/blog/business-registration-certificate-authentication-api
23. https://www.data.go.kr/en/data/15061362/openapi.do
24. https://bokduckbbang.com/blog/ (내 집 마련 후 첫 인테리어 공사 하자 예방… 표준계약서·건설업면허 등록업체 조회 경로, full URL in §8)
25. https://blog.iquest.co.kr/entry/%ED%82%A4%EC%8A%A4%EC%BD%98
26. https://softwareengineeringdaily.com/wp-content/uploads/2017/11/SED468-Thumbtack-Marketplace-Evolution.pdf
27. https://archive.qconsf.com/node/71046
28. https://podcast.app/thumbtack-infrastructure-with-nate-kupp-e97221528
29. https://startup.jobs/backend-engineer-marketplace-thumbtack-5504025
30. https://www.thumbtack.com/safety
31. https://www.thumbtack.com/safetyguidelines/
32. https://www.consumeraffairs.com/homeowners/thumbtack.html?page=3
33. https://www.checkatrade.com/blog/trust/
34. https://www.checkatrade.com/blog/trade/checkatrade-approved-and-guaranteed/
35. https://www.fixflo.com/blog/how-vetting-builds-trust-fixflo-and-checkatrade
36. https://electriciancourses4u.co.uk/blog/can-customers-trust-trade-directories-to-find-a-trusted-tradesperson/
37. https://expertbeacon.com/an-experts-guide-to-angi-reviews-earning-5-stars-the-right-way/
38. https://www.ftc.gov/node/78110
39. https://assets.publishing.service.gov.uk/media/650c015c52e73c000d9425b6/fake-reviews-consultation-impact-assessment.pdf
40. https://www.ftc.gov/node/80884
41. https://ftc.gov/news-events/news/press-releases/2023/01/ftc-order-requires-homeadvisor-pay-72-million-stop-deceptively-marketing-its-leads-home-improvement
42. https://www.abc15.com/homeadvisor-to-pay-7-2-million-for-misleading-gig-contractors
43. https://www.houzz.com/for-pros/feature-estimating.md
44. https://apps.apple.com/app/id1488002482
45. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html
46. https://aws.amazon.com/blogs/aws/automatic-restore-testing-and-validation-is-now-available-in-aws-backup/
47. https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing-validation.md
48. https://dev.to/instadevops/how-to-run-an-aws-well-architected-review-the-6-pillars-and-common-findings-3p15
49. https://oneuptime.com/blog/post/2026-02-12-run-well-architected-review-aws-workload/view
50. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html
51. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.Retaining.html
52. https://aws.amazon.com/blogs/startups/aws-startup-security-baseline-day-one-recommendations-to-secure-your-account-and-workload
53. https://builder.aws.com/content/3KDsT0KIsMX5GvD3DWhufex9MXA/securing-a-new-aws-account-the-first-hour
54. https://builder.aws.com/content/3KN4kLaajwh3j9BMZ2ywOoBcvsM/secure-a-brand-new-aws-account-in-minutes-almost-free
55. https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html
56. https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances-unlimited-mode-concepts.html
57. https://stackharbor.com/en/knowledge-base/awsfix-t3-cpu-credits-slowdown/
58. https://www.netdata.cloud/guides/docker/docker-log-rotation/
59. https://blog.canadianwebhosting.com/docker-logs-filling-disk/
60. https://oneuptime.com/blog/post/2026-02-08-how-to-limit-docker-container-log-file-size/view
61. https://caddy.community/t/lets-encrypt-rate-limit-after-update-of-container/5136
62. https://caddy.community/t/docker-caddy-request-for-certs-having-valid-ones/9303
63. https://caddy.community/t/too-many-failed-authorizations-recently/20629
64. https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/
65. https://www.theregister.com/2017/02/01/gitlab_data_loss/
66. https://danluu.com/postmortem-lessons/
67. https://raw.githubusercontent.com/danluu/post-mortems/master/README.md
68. https://verycloud.fr/en-US/docs/article/docker-compose
69. https://valebyte.com/es/guides/docker-en-un-vps-desde-cero-instalacion-compose-actualizaciones-y-copias-de-seguridad-de-volumenes/
70. https://skills.cat/skills/simplerick0/com-ackhax-configs/production-readiness
71. https://www.rackspace.com/es/blog/do-you-have-an-operational-readiness-checklist
72. https://costbench.com/software/developer-tools/sentry/free-plan/
73. https://agentdeals.dev/vendor/sentry
74. https://notifier.so/guides/uptimerobot-pricing-2026/
75. https://www.productcompass.pm/p/uptimerobot-alternatives
76. https://docs.aws.amazon.com/ses/latest/dg/reputation-dashboard-dg.html
77. https://aws.amazon.com/blogs/messaging-and-targeting/introducing-the-amazon-ses-mailbox-simulator
78. https://oneuptime.com/blog/post/2026-02-12-move-amazon-ses-out-of-sandbox/markdown
79. https://repost.aws/ko/questions/QUl1TP2B3cSFSLXnPtXHnG-w/been-denied-production-access-for-transactional-emails-and-have-no-idea-what-else-to-do
80. https://tech-insider.org/?p=25269
81. https://pypi.org/project/fastapi-user-limiter
82. https://viblo.asia/p/rate-limiting-trong-fastapi-tu-khong-co-gi-den-production-ready-phan-1-pPLkN3y8JRZ
83. https://lilys.ai/ko/notes/online-business-20251205/e-commerce-platform-related-business-duties
84. https://www.lawtalk.co.kr/posts/115661
85. https://opinion.lawmaking.go.kr/file/download/8094187/TLS0HX1X4OJC1D9A8T4C
86. https://dealsite.co.kr/articles/137678
87. https://itwiki.kr/w/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98_%EC%95%88%EC%A0%84%EC%84%B1_%ED%99%95%EB%B3%B4%EC%A1%B0%EC%B9%98_%EA%B8%B0%EC%A4%80_%EC%A0%9C8%EC%A1%B0
88. https://byline.network/2025/11/20-518/
89. https://www.itwiki.kr/w/ISMS-P_%EC%9D%B8%EC%A6%9D_%EB%8C%80%EC%83%81
90. https://m.boannews.com/html/detail.html?idx=129433
91. https://www.bizhankook.com/bk/article/26498
92. https://letter.wepick.kr/post/1815
93. https://www.etoday.co.kr/news/view/2327015
94. https://peoplepower21.org/publiclaw/1992345
95. https://cubeapm.com/blog/posthog-pricing-and-review/
96. https://www.costbench.com/compare/posthog-vs-amplitude/
97. https://pandectes.io/blog/microsoft-clarity-and-gdpr-what-you-need-to-know-in-2025/
98. https://seers.ai/blogs/how-to-enable-clarity-consent-mode/
99. https://supabase.com/blog/postgres-full-text-search-vs-the-rest
100. https://www.meilisearch.com/docs/resources/comparisons/postgresql
101. https://postgresql.org/docs/current/pgtrgm.html
102. https://aws.amazon.com/about-aws/whats-new/2021/04/amazon-rds-for-postgresql-supports-new-minor-versions
103. https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html
104. https://solapi.com/pricing
105. https://solapi.com/tiered-pricing
106. https://solapi.com/guides/kakao-ata-guide
107. https://blog.bizgo.io/?p=1672
108. https://megazone.com/?p=42127 (CloudFront + Lambda@Edge on-the-fly resizing pattern, supporting B7)

Fetched but returned no usable content: https://posthog.com/pricing (page didn't render), https://www.thumbtack.com/safety (empty on fetch; figures from a search snippet), https://www.checkatrade.com/blog/trust/ (403; figures from a search snippet).
