# 믿집 완성 구성 검증 — File storage (S3) and transactional email / notifications (SES + Korean channels)

Scope: the proposed design is one EC2 instance in ap-northeast-2 running Docker Compose (Caddy, Next.js 16, FastAPI, Redis, arq). Files go to a private S3 bucket through the FastAPI API, which checks magic bytes and size, strips EXIF and GPS with Pillow and converts HEIC to JPEG. Downloads use short-lived presigned GET URLs after an ownership or admin check. Email goes through SES Seoul, sent from the arq worker. Research date: 2026-10-29. The shared web-search budget ran out partway through. Later facts come from direct fetches of primary pages, and the remaining open items are listed under Gaps.

---

## 1. S3 private bucket best practices (2026): Block Public Access, Object Ownership, encryption, TLS policy, versioning/lifecycle, EC2 instance role

### Takeaway
The proposed private bucket matches AWS's 2026 guidance. Most of the important settings are now defaults: ACLs disabled through bucket-owner-enforced ownership, SSE-S3 encryption, and SSE-C blocked on new buckets since April 2026. The team still has to add five things itself: Block Public Access (all four settings), a bucket policy that denies non-TLS requests, a short limit on signature age, lifecycle rules (abort incomplete multipart uploads, expire orphan/tmp uploads, expire noncurrent versions), and a least-privilege EC2 instance role instead of access keys.

### Cited Findings
- **Object Ownership / ACLs:** Object Ownership now defaults to *bucket owner enforced*, with all ACLs disabled, and ACLs are disabled for new buckets by default. AWS recommends keeping them disabled unless per-object ACLs are required. When ACLs are disabled, a PUT carrying any ACL other than bucket-owner-full-control fails with `400 AccessControlListNotSupported`. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- **Block Public Access:** AWS recommends S3 Block Public Access as a centralized control that is "enforced regardless of how the resources are created". It also recommends checking policies for `"Principal": "*"` and enabling the AWS Config rules `s3-bucket-public-read-prohibited` and `s3-bucket-public-write-prohibited`. Organization-level BPA policies are now available through AWS Organizations. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html); a third-party guide also recommends BPA at both account and bucket level — [Sentra, Mar 2026](https://sentra.io/learn/s3-bucket-security-best-practices)
- **Encryption at rest:** All buckets are encrypted by default, and SSE-S3 is the default for every bucket. SSE-KMS, DSSE-KMS and SSE-C are optional. **Since April 2026 S3 disables SSE-C** for all new general purpose buckets, and for existing buckets in accounts that have no SSE-C objects. SSE-C must now be enabled deliberately with PutBucketEncryption, and AWS recommends leaving it disabled. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- **TLS enforcement:** AWS recommends allowing only HTTPS with the `aws:SecureTransport` condition in the bucket policy, plus the Config rule `s3-bucket-ssl-requests-only`. It also advises against pinning S3 TLS certificates, because S3 rotates them. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- **Bucket namespace (new):** AWS now recommends creating buckets in the *account regional namespace*, so the name can never be re-created by another account. It advises against deleting global-namespace buckets, because a deleted name can be claimed by others. The default quota is now 10,000 buckets per account. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- **Credentials:** AWS says to use IAM roles for applications on EC2, not access keys stored on the instance, because roles supply temporary credentials. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- **Versioning / Object Lock:** AWS recommends S3 Versioning so data can be recovered after accidental deletes or overwrites (Config rule `s3-bucket-versioning-enabled`). Object Lock (WORM) is suggested for logs. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- **Lifecycle:** S3 Storage Lens can flag "buckets that don't have S3 Lifecycle rules to abort incomplete multipart uploads that are more than 7 days old", which AWS treats as a best-practice signal. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- **AbortIncompleteMultipartUpload:** counts days from when the upload was initiated, after which S3 removes the parts. **NoncurrentVersionExpiration:** applies only to versioned or versioning-suspended buckets, counted from when a version becomes noncurrent. A rule filter is exactly one of prefix, tag, object-size bound or an `And` combination. `ExpiredObjectDeleteMarker` cannot be combined with ExpirationInDays, ExpirationDate or TagFilters. — [S3 PUT lifecycle API reference](https://docs.aws.amazon.com/AmazonS3/latest/API/v1-rel-RESTBucketPUTlifecycle.md); [AWS CDK LifecycleRule](https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-s3.LifecycleRule.html); [CfnBucket RuleProperty](https://docs.amazonaws.cn/cdk/api/v1/docs/@aws-cdk_aws-s3.CfnBucket.RuleProperty.html)
- **Monitoring options:** AWS lists server access logging, CloudTrail data events (GetObject/PutObject), AWS Config, IAM Access Analyzer for S3, Macie (PII discovery) and GuardDuty S3 Protection. CloudWatch metrics worth watching are `4xxErrors`, `PutRequests` and `DeleteRequests`. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- **Storage price (approximate):** a third-party price table lists S3 Standard in Asia Pacific (Seoul) at about **$0.025/GB-month** for the first 50 TB. Seoul request prices were not confirmed. For reference, us-east-1 is $0.005 per 1,000 PUTs and $0.0004 per 1,000 GETs. — [CostGoat S3 calculator (third-party, verify)](https://costgoat.com/pricing/amazon-s3); [Upstash S3 pricing 2026](https://upstash.com/blog/aws-s3-pricing-explained-2026.md)

### Inferences
- **Recommended minimum bucket configuration for 믿집:**
  - BPA: all 4 settings ON at both account and bucket level.
  - Object Ownership: BucketOwnerEnforced (the default).
  - Encryption: default SSE-S3. SSE-KMS only adds KMS cost and IAM complexity, and gives no meaningful benefit for a student project. SSE-C stays blocked (the default).
  - Bucket policy statements:
    - (a) Deny `s3:*` when `aws:SecureTransport=false`.
    - (b) Deny when `s3:signatureAge` exceeds about 600000 ms, so even a leaked URL is short-lived (see §2).
    - (c) Optionally, GuardDuty tag-based access control (see §3).
  - Bucket name in the account regional namespace.
- **Lifecycle rules:**
  - (1) `AbortIncompleteMultipartUpload` after 1–7 days.
  - (2) Expiration of a `tmp/` or `incoming/` prefix (or a tag such as `state=pending`) after 1 day, to clean up orphan uploads that were never attached to a quote request or vendor application.
  - (3) If versioning is on, `NoncurrentVersionExpiration` after about 30 days plus `ExpiredObjectDeleteMarker` cleanup, in a separate rule because of the combination restriction.
  - Turning versioning on is cheap insurance against an app bug deleting customer floor plans, and noncurrent expiry caps the cost.
- **IAM role:** attach an instance profile to the EC2 instance with a policy limited to `s3:PutObject`, `s3:GetObject` and `s3:DeleteObject` on `arn:aws:s3:::<bucket>/*`, and nothing account-wide. Do not put access keys in `.env`.
  - **Docker gotcha (prior knowledge, verify):** with IMDSv2 enforced, containers on a Docker bridge network usually need the instance metadata `HttpPutResponseHopLimit` set to 2, or boto3 inside FastAPI and arq cannot obtain role credentials.
- **Cost at 믿집 scale is negligible.** For example, 500 projects × (15 photos × ~2 MB re-encoded JPEG + 1 plan × ~5 MB) ≈ 17.5 GB, which is about $0.45/month in Standard. Requests cost cents.
- AWS Config and CloudTrail data events cost extra. For a student budget, the free default CloudTrail management events plus CloudWatch S3 metrics are probably enough. Enable server access logs only if an audit trail of downloads is needed.

### Gaps
- Exact S3 request and storage prices for ap-northeast-2 were not confirmed on the official AWS pricing page (search budget exhausted). Verify at aws.amazon.com/s3/pricing.
- The IMDSv2 hop-limit detail comes from prior knowledge, not a source fetched in this session.

---

## 2. Presigned GET URLs (expiry, Content-Disposition, caching) and uploads: API proxy vs presigned POST/PUT, EXIF stripping, size limits, cost

### Takeaway
At 믿집's scale (tens of concurrent users, files of 10 MB or 20 MB), proxying uploads through FastAPI is the simpler and safer choice. It is the only option that guarantees EXIF/GPS removal and re-encoding before anything is stored. A direct-to-S3 design would need a quarantine prefix and a worker pass anyway.
- **Downloads:** presigned GET URLs with 1–5 minute expiry, generated per request after the authorization check, with `response-content-disposition` set (attachment for PDFs and documents).
- **Expiry ceiling:** an EC2 instance-role presign can never outlive the role credentials, which last at most about 6 hours.

### Cited Findings
- **Who and how long:** a presigned URL uses the credentials of the principal that generated it. With an IAM user and SigV4 the maximum is 7 days. With **EC2 instance-role credentials it is valid only for the life of those credentials (typically about 6 hours)**, even if a longer expiry is requested. The console allows 1 minute to 12 hours, and the SDK/CLI up to 7 days. — [AWS: presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)
- **Expiry and reuse:** a URL can be reused any number of times until it expires. Expiry is checked when the request starts, so a download that has begun can finish after expiry, but a restart after expiry fails. Presigned URLs are bearer tokens and should be protected. — [AWS: presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)
- **Restricting presigned URLs:** a bucket policy can deny requests whose `s3:signatureAge` exceeds a threshold (AWS's example is 600000 ms = 10 min). Requests can also be limited to network paths with `aws:SourceIp`, or `aws:SourceVpce` for VPC endpoints. — [AWS: presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)
- **Presigned upload overwrites:** if an object with the same key exists, a presigned PUT replaces it. SigV4 presigned uploads support checksums (CRC32/CRC32C/CRC64-NVME/SHA-256 and others). — [AWS: presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)
- **Response header overrides:** a GetObject request can override `Cache-Control`, `Content-Disposition`, `Content-Encoding`, `Content-Language`, `Content-Type` and `Expires` with the query parameters `response-cache-control`, `response-content-disposition`, `response-content-type` and so on. The overrides apply only to `200 OK` responses. — [S3 GetObject API reference](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html)
- **Size limits on direct uploads:** a presigned **POST** policy can enforce `["content-length-range", min, max]` in bytes, for example 1 KB–10 MB using boto3 `generate_presigned_post`. — [OneUptime, Feb 2026](https://oneuptime.com/blog/post/2026-02-12-generate-presigned-post-requests-s3-uploads/view). The equivalent semantics are documented for an S3-compatible POST — [Oracle OCI S3-compat POST](https://docs.oracle.com/en-us/iaas/Content/Object/s3-post-upload.htm). **POST policy conditions are not enforced on presigned PUT**, as a user found when a PUT ignored the size limit — [Fly.io community thread](https://community.fly.io/t/content-length-range-doesnt-limit-file-upload/25260).
- **Re-encoding as sanitization:** OWASP recommends decoding and re-encoding images to an allowed format to strip metadata and embedded content. It warns that rewriting "does not guarantee that all malicious content is removed", so processors should be up to date and sandboxed. — [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- **Decompression bombs:** Pillow's `open()` is lazy and reads pixel data only on processing. It emits `DecompressionBombWarning` above `Image.MAX_IMAGE_PIXELS` and raises `DecompressionBombError` above twice that limit. Setting the value to `None` disables the check, which should not be done. — [Pillow Image reference](https://pillow.readthedocs.io/en/stable/reference/Image.html)
- **HEIC:** pillow-heif reads and writes HEIF through libheif and works as a Pillow plugin. — [pillow-heif docs](https://pillow-heif.readthedocs.io/en/latest/)

### Inferences
- **Keep the API-proxy upload path (as proposed).** It makes these controls easy:
  - (a) Cap the size at Caddy (`request_body max_size` about 25 MB), then check `Content-Length` and stream bytes in FastAPI.
  - (b) Validate magic bytes (JPEG/PNG/HEIC/WebP/PDF allowlist).
  - (c) For images: `ImageOps.exif_transpose()` first so orientation survives, then re-encode to JPEG/WebP without passing `exif=`, which drops EXIF and GPS. Keep `MAX_IMAGE_PIXELS` at its default (about 89.5 MP from prior knowledge, verify), or lower it, for example to 50 MP.
  - (d) Register pillow-heif's opener for HEIC→JPEG (`from pillow_heif import register_heif_opener`; API name from prior knowledge, verify).
  - (e) Generate a UUID key (never the user's filename) and set `ContentType` from the validated type.
  - (f) PutObject from the role.
- **Cost of proxying:** inbound transfer to EC2 and EC2→S3 traffic in the same region are not billed as egress (prior knowledge). The real cost is EC2 CPU and RAM during Pillow work. To avoid blocking the event loop, run heavy re-encoding (HEIC decode, multi-MB JPEG) in a threadpool or hand it to the arq worker. Tens of concurrent 10 MB uploads fit comfortably on a t3.small or medium class instance.
- **If direct upload is wanted later** (for example, mobile bandwidth):
  1. Issue a presigned **POST** (not PUT) restricted to `incoming/{uuid}` with `content-length-range` and an `eq`/`starts-with` Content-Type condition, valid for about 5 minutes.
  2. The client calls `/uploads/{id}/complete`.
  3. The arq worker downloads the object, validates, strips and re-encodes it, writes `clean/{uuid}.jpg` and deletes the `incoming/` original. Alternatively, S3 Event Notifications → SQS → worker.
  4. A lifecycle rule expires `incoming/` after 1 day.
  
  This adds moving parts for no real benefit at 믿집 scale.
- **Download URL policy:**
  - Expiry: about 60–300 s for 사업자등록증 and plans; up to about 10–15 min for photo galleries, matching an `s3:signatureAge` bucket-policy cap.
  - Generate URLs only after the ownership/admin check, and never store them in the DB.
  - Documents: `response-content-disposition=attachment; filename*=UTF-8''<urlencoded Korean name>`. Images: `inline`.
  - Set `response-cache-control=private, max-age=<≤ expiry>`. Because every URL has a unique signature query string, browser and CDN caching across page loads is limited. That is acceptable at this scale; if gallery reloads feel slow, generate thumbnails (see §4) and reuse URLs for a few minutes server-side, for example in Redis.
- S3 serves presigned content from `*.s3.ap-northeast-2.amazonaws.com`, a different origin from the app. Script embedded in an uploaded file therefore cannot read the app's cookies or localStorage, but forcing `attachment` for PDFs is still prudent.

### Gaps
- The AWS primary POST-policy reference page (sigv4-HTTPPOSTConstructPolicy) did not render when fetched. The `content-length-range` semantics are sourced from secondary and S3-compatible docs.
- The Pillow `MAX_IMAGE_PIXELS` default value, the `ImageOps.exif_transpose` behaviour, FastAPI `UploadFile` spooling and Caddy's `request_body` directive were not confirmed on fetched pages (prior knowledge).

---

## 3. Malware scanning (GuardDuty Malware Protection for S3), file-type validation, PDF risks

### Takeaway
GuardDuty Malware Protection for S3 is the lowest-effort managed scanner. It works per bucket without enabling the rest of GuardDuty, writes results as an object tag and an EventBridge event, and supports a tag-based "no read unless clean" bucket policy. It costs about $0.09/GB scanned plus a per-object fee, after a free tier of 1,000 objects and 1 GB per month. At 믿집 volumes that is a few dollars a month at most, so it is a reasonable add-on for the "completed" architecture. Re-encoding images already neutralizes most image-borne payloads. The residual risk sits in PDFs (floor plans and 사업자등록증), which should get AV scanning, be served as `attachment`, and ideally be rendered to images for in-app preview.

### Cited Findings
- **Pricing:** effective 2025-02-01 the per-GB scanning price dropped 85%, from $0.60 to **$0.09/GB in us-east-1**. The per-object-evaluated price did not change, and the cut applied in all regions. — [AWS What's New, Feb 2025](https://aws.amazon.com/about-aws/whats-new/2025/02/amazon-guardduty-malware-protection-s3-price-reduction)
- **Per-object fee:** a third-party source cites **$0.215 per 1,000 objects** in us-east-1. Not confirmed on an AWS page. — [Cloudburn GuardDuty pricing](https://cloudburn.io/blog/amazon-guardduty-pricing)
- **Free tier and extra costs:** each account gets 1,000 requests and 1 GB scanned per month per region, and on-demand scans are excluded. **Not included in the free tier:** S3 object tagging charges, the GET/PUT calls GuardDuty makes, and EventBridge ingestion of S3 events. Malware Protection for S3 has a free tier instead of GuardDuty's usual 30-day trial. — [GuardDuty Malware Protection for S3 pricing](https://docs.aws.amazon.com/guardduty/latest/ug/pricing-malware-protection-for-s3-guardduty.html). A third-party source describes it as a 12-month free tier — [AWS search summary of the same doc; see also Barking Iguana walkthrough](https://barkingiguana.com/writing/how-to-scan-ec2-and-s3-with-guardduty-malware-protection/)
- **Independent mode:** Malware Protection for S3 can be enabled "by itself without enabling the GuardDuty service". In that mode there is no detector ID and **no GuardDuty findings**. Results go to the default EventBridge bus and a CloudWatch namespace, plus an optional object tag. It works only for buckets in the same account and region. — [GuardDuty Malware Protection for S3](https://docs.aws.amazon.com/guardduty/latest/ug/gdu-malware-protection-s3.html); launch blog — [AWS News Blog](https://aws.amazon.com/blogs/aws/introducing-amazon-guardduty-malware-protection-for-amazon-s3)
- **Quotas:** max object size 100 GB, at most 100,000 extracted files and 100 nesting levels, and at most 25 protected buckets per account per region. None of these are adjustable. — [GuardDuty Malware Protection for S3 quotas](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection-s3-quotas-guardduty.html)
- **Tag-based access control:** the tag key is `GuardDutyMalwareScanStatus`. AWS provides a bucket policy that **denies `s3:GetObject`/`GetObjectVersion` to everyone except the GuardDuty role unless the tag equals `NO_THREATS_FOUND`**, and denies `PutObjectTagging` of that key by anyone else. If an object already has 10 tags, GuardDuty cannot add its tag. — [GuardDuty TBAC](https://docs.aws.amazon.com/guardduty/latest/ug/tag-based-access-s3-malware-protection.html)
- **File-type validation (OWASP):**
  - Use an extension allowlist; blocklists are weak.
  - Don't trust Content-Type.
  - Check magic bytes, but "should not be used on its own".
  - Rename to a UUID, enforce size limits (measuring archives after decompression), and store outside the webroot or on a separate host.
  - Apply AV or sandbox scanning, and Content Disarm & Reconstruct for PDF/DOCX. ZIP is not recommended.
  - Uploading requires authorization and CSRF protection.
  
  — [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- **Detection-only services:** GuardDuty S3 Protection (CloudTrail-based threat detection) and Macie (PII discovery) are separate from malware scanning. — [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

### Inferences
- **Cost estimate (us-east-1 rates, Seoul unverified):** 3,000 uploads/month × about 3 MB ≈ 9 GB gives roughly 9 × $0.09 ≈ $0.81 plus 3 × $0.215 ≈ $0.65, about **$1.5/month** before free-tier offsets and small tagging, request and EventBridge charges.
- **Fitting it into the proposed flow:**
  1. The API writes the sanitized object.
  2. GuardDuty scans it asynchronously, typically within seconds to minutes.
  3. Apply the TBAC deny policy, with an exception for the GuardDuty role, so that a presigned GET fails until the tag is `NO_THREATS_FOUND`.
  4. Have the arq worker (or an EventBridge rule → SQS) record `scan_status` in Postgres, so the UI shows "검사 중" until clean and the admin is alerted on `THREATS_FOUND`.
  
  If EventBridge/SQS feels like too much, the worker can poll `GetObjectTagging` a few times after upload.
- **Self-hosted alternative:** ClamAV in a container in the Compose stack costs $0 in AWS fees but needs significant RAM for signatures (prior knowledge, roughly 1 GB+) and signature updates. On a single small EC2 that is a worse trade than GuardDuty's managed pricing.
- **PDF-specific controls:**
  - (a) Magic bytes `%PDF-` plus parsing with a library such as pikepdf or PyMuPDF. Reject encrypted or malformed files and optionally reject files containing `/JavaScript`, `/OpenAction`, `/Launch` or `/EmbeddedFile`.
  - (b) For in-app preview of floor plans, render page 1 to PNG or WebP in the worker and show the image. Keep the original PDF downloadable only as `attachment`.
  - (c) 사업자등록증: accept JPEG/PNG/PDF only. Admins download through a 60-second presigned URL. Retain the file only as long as the vendor-approval policy requires, then delete it (PII minimisation).
- **Default posture:** images are re-encoded (and so effectively CDR'd); PDFs are AV-scanned and served as `attachment`. That is proportionate for a bootcamp project.

### Gaps
- The per-object price and per-GB price in ap-northeast-2 were not confirmed on the official GuardDuty pricing page.
- No 2025–2026 source was found quantifying PDF-borne malware risk specifically for consumer platforms, and no dedicated PDF-sanitization source was fetched (search budget exhausted).

---

## 4. Does this scale need CloudFront? Thumbnail and resizing pipeline

### Takeaway
No. At a few hundred users with private, per-user files, CloudFront adds little. Private objects behind CloudFront would need CloudFront signed URLs or cookies instead of S3 presigned URLs, which is a second signing scheme. Static Next.js assets are small and Caddy can cache them. The new CloudFront flat-rate plans include a $0 Free plan (1M requests, 100 GB) and a $15 Pro plan bundling WAF and DDoS protection. These make CloudFront in front of the *app* an optional hardening step later, not a requirement. Generate thumbnails once, at upload time, in the arq worker.

### Cited Findings
- **Flat-rate plans:** CloudFront flat-rate plans bundle global delivery with AWS WAF, DDoS protection, Route 53 DNS, CloudWatch Logs ingestion, S3 storage credits and edge compute, with **no overage charges**. Tiers:
  - Free: $0/month, 1M requests, 100 GB.
  - Pro: $15/month, 10M requests, 50 TB.
  - Business: $200/month, 125M requests.
  - Premium: from $1,000/month.
  
  Console and email alerts fire at 50%, 80% and 100% of the allowance. **"Free Tier accounts cannot use CloudFront Flat-Rate Plans."** — [AWS Pricing Plan Manager: available plans](https://docs.aws.amazon.com/PricingPlanManager/latest/UserGuide/plans.html)
- **Launch and terms:** the plans launched in November 2025, attach per distribution, and require no annual commitment. — [AWS Networking blog (KO)](https://aws.amazon.com/ko/blogs/networking-and-content-delivery/amazon-cloudfront-flat-rate-pricing-plans-new-features-and-expanded-capabilities/); [BlazingCDN analysis 2026](https://blog.blazingcdn.com/en-us/cloudfront-flat-rate-plans-explained-limits-and-fine-print-2026); [AWS Builder article](https://builder.aws.com/content/3D6DxKr47HkYZkCY7d2efzYTu1B/no-more-surprise-bills-what-cloudfronts-flatrate-pricing-really-changes)
- **Image rewriting:** OWASP recommends rewriting uploaded images (decode and re-encode), which is the same step a thumbnail pipeline performs. — [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)

### Inferences
- **Thumbnail pipeline:** in the same worker job that re-encodes uploads, write two derivatives:
  - `…/{uuid}_w400.webp` for the thumbnail grid.
  - `…/{uuid}_w1600.jpg` for the lightbox.
  
  Record both keys in the `files` table. Pillow handles this in milliseconds per image, so no Lambda or "dynamic image transformation" stack is needed.
- **When CloudFront would become worth it:** public marketing pages with heavy traffic, a need for WAF or bot protection on the login and quote endpoints, or users outside Korea. The Pro plan at $15/month (WAF included) is the natural step. Note the Free Tier account restriction: AWS accounts on the new free plan cannot subscribe.
- Keeping S3 private with S3 presigned URLs, rather than CloudFront OAC plus signed cookies, keeps the authorization logic in one place (FastAPI).

### Gaps
- Not verified whether the Free flat-rate plan allows a private-S3 origin with OAC on the same terms as paid tiers, or exactly which WAF features the Free plan includes.

---

## 5. Amazon SES: sandbox exit, DKIM/SPF/DMARC with Route 53, custom MAIL FROM, Gmail/Yahoo rules, bounce/complaint handling, configuration sets, quotas, 2026 pricing

### Takeaway
SES Seoul is a sound choice, but it needs the following before launch:
- (1) A verified **domain** identity with Easy DKIM (2048-bit, auto-published in Route 53).
- (2) A custom MAIL FROM subdomain, giving SPF alignment and DMARC through both SPF and DKIM.
- (3) A `_dmarc` record starting at `p=none` with reporting.
- (4) The account-level suppression list (bounces and complaints) plus a configuration set publishing bounce, complaint, reject and delivery-delay events to SNS or EventBridge, consumed by the worker.
- (5) CloudWatch alarms on bounce rate at 5% and complaint rate at 0.1%.
- (6) A production-access request in ap-northeast-2, filed as "Transactional", with a real website URL. AWS responds within 96 hours.

Pricing changed in July 2026. New accounts, and accounts without metered SES use since 2025-06-01, start on the **Essentials plan at $0.16/1,000 emails** (VDM included) instead of the $0.10/1,000 à la carte rate, and can switch to à la carte at any time. At 믿집's volume either is well under $1/month.

### Cited Findings
- **Sandbox (per region):**
  - Send only to verified addresses or domains, or the mailbox simulator.
  - At most 200 messages per 24 h and 1 message/s.
  - Suppression-list bulk actions and suppression-management APIs are disabled.
  - After production access you can send to anyone, but From/Source/Sender/Return-Path identities must still be verified.
  
  — [SES: request production access](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html)
- **Production-access request:**
  - Mail type (Marketing vs **Transactional**, "one-to-one … triggered by a user action").
  - Website URL.
  - Up to 4 additional contacts.
  - Contact language (English or Japanese only).
  - An acknowledgement that you send only to people who requested mail and have a bounce/complaint handling process.
  
  Verifying a domain first "helps to get your production access request approved faster". AWS gives an initial response within **96 hours**. The request can also be made with `aws sesv2 put-account-details --production-access-enabled --mail-type TRANSACTIONAL …`. AWS notes that sending from EC2 *over SMTP port 25* may require removing the EC2 port-25 throttle. — [SES: request production access](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html)
- **Third-party advice on the request:** detailed use-case descriptions get approved and vague ones get rejected. Some guides recommend a long write-up and report approvals in about 24 h. These claims are unverified and conflict with AWS's own 96-h statement. — [OneUptime 2026](https://oneuptime.com/blog/post/2026-02-12-move-amazon-ses-out-of-sandbox/view); [DevOpsCube](https://devopscube.com/amazon-ses-production-access/); [MailBluster](https://mailbluster.com/blog/getting-out-of-amazon-ses-sandbox); [CampaignHQ](https://blog.campaignhq.co/how-to-get-aws-ses-production-access/)
- **Quotas:** the sending quota is a rolling 24 h maximum, and there is a per-second rate (short bursts allowed) and a max message size. A 5 MB attachment becomes about 6.85 MB after MIME encoding, and **AWS recommends linking to files instead of attaching them**. Quotas are separate per region and count recipients, not messages; AWS recommends one SendEmail call per recipient. Increases go through Support. — [SES: managing sending limits](https://docs.aws.amazon.com/ses/latest/dg/manage-sending-quotas.html)
- **Easy DKIM:** SES signs every message with a **2048-bit key by default** (1024 is optional). Route 53 records can be created automatically. The key length can change at most once per 24 h. — [SES: Easy DKIM](https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dkim-easy.html)
- **Custom MAIL FROM:**
  - Use a dedicated subdomain (for example `bounce.mitjip.kr`) that is used for nothing else, neither sending nor receiving.
  - Publish exactly one MX `10 feedback-smtp.<region>.amazonses.com` (here ap-northeast-2) and TXT `"v=spf1 include:amazonses.com ~all"`.
  - Behaviour on MX failure: fall back to the amazonses.com default, or reject with `MailFromDomainNotVerified`.
  - Route 53 publishing is one click. Detection can take up to 72 h.
  
  — [SES: custom MAIL FROM](https://docs.aws.amazon.com/ses/latest/dg/mail-from.html)
- **DMARC with SES:** DKIM alignment comes from Easy DKIM. SPF alignment requires a custom MAIL FROM and relaxed SPF alignment (do not set `aspf=s`). AWS's example record is `_dmarc TXT "v=DMARC1;p=quarantine;rua=mailto:…"`. The recommended rollout is `p=none` (monitor) → `quarantine` → `reject`, applied to subdomains first. — [SES: DMARC](https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dmarc.html)
- **Gmail rules (all senders, since 2024-02-01):**
  - SPF **or** DKIM.
  - Valid forward and reverse DNS (PTR).
  - TLS.
  - Spam rate below 0.3%, with a target below 0.10%.
  - RFC 5322 formatting.
  
  **Bulk senders (>5,000/day to Gmail):** SPF **and** DKIM, DMARC (p=none allowed), From aligned with SPF or DKIM, and **one-click unsubscribe for "marketing messages and subscribed messages"** only. DKIM keys must be ≥1024 bits (2048 recommended). Gmail says it "will begin using a DMARC quarantine enforcement policy" but gives no date. — [Google email sender guidelines](https://support.google.com/a/answer/81126?hl=en)
- **Late-2025 enforcement:** third-party sources report that Gmail ramped up enforcement in November 2025, including temporary and permanent rejections of non-compliant mail. — [Zoho community, Nov 2025](https://help.zoho.com/portal/en/community/topic/gmail-is-ramping-up-its-email-sender-policy-from-november-2025?page=1); [Suped](https://www.suped.com/knowledge/email-deliverability/compliance/how-to-comply-with-gmails-new-sending-rules-for-bulk-email-senders); [TechSpot](https://techspot.com/news/100374-google-new-spam-rules-ensures-senders-5000-daily.html)
- **Yahoo Sender Hub:** a working List-Unsubscribe with one-click, spam rate below 0.3%, valid forward/reverse DNS, RFC 5321/5322 compliance, DMARC published, and unsubscribes honoured within 2 days without login. — [Yahoo Sender Best Practices](https://senders.yahooinc.com/best-practices); RFC 8058 POST preferred — [Resend KB](https://resend.com/docs/knowledge-base/how-do-i-avoid-yahoos-spam-folder.md); p=none satisfies the bulk-sender requirement — [AWS Messaging & Targeting blog](https://go.aws/4bwFazW); overview — [MessageGears](https://messagegears.com/blog/google-yahoo-to-combat-spam-with-new-email-rules-for-bulk-senders/)
- **Account-level suppression list:**
  - On by default for bounces and complaints for accounts created after 2019-11-25.
  - **Only hard bounces** are added.
  - SES accepts but does not deliver to suppressed addresses, and those sends still count toward the daily quota.
  - Entries stay until removed.
  - **Gmail does not send complaint data to SES**, so Gmail "Report spam" does not add the address.
  - Configuration sets can override suppression.
  - Bulk management needs production access.
  
  — [SES: account-level suppression list](https://docs.aws.amazon.com/ses/latest/dg/sending-email-suppression-list.html)
- **Event publishing:** events are Send, RenderingFailure, Reject (virus), Delivery, Bounce, Complaint, DeliveryDelay, Subscription, Open and Click. Destinations are CloudWatch, Firehose, Pinpoint, **SNS** and **EventBridge**. A configuration set must be specified per send, by name or as a default. Auto-tags include `ses:configuration-set` and `ses:from-domain`. — [SES: event publishing](https://docs.aws.amazon.com/ses/latest/dg/monitor-using-event-publishing.html)
- **Reputation thresholds:** AWS recommends keeping bounce rate below 5% (it may pause sending above 10%) and complaint rate below 0.1% (it may pause above 0.5%). Alarm at ≥0.05 and ≥0.001 respectively, with missing data treated as "ignore". — [SES: reputation CloudWatch alarms](https://docs.aws.amazon.com/ses/latest/dg/reputationdashboard-cloudwatch-alarm.html)
- **Pricing (official page, current):**
  - À la carte: **$0.10/1,000** emails.
  - Essentials: **$0.16/1,000** (0–10M), no monthly fee, includes outbound, SES deliverability VDM, Mail Manager processing and an authenticated ingress endpoint.
  - Pro: $105/account/region/month plus $0.22/1,000, adding managed dedicated IPs, email validation and Global VDM.
  - Enterprise: $500/month plus $0.23/1,000.
  - Attachments $0.12/GB. Mailbox-simulator mail is billed. Dedicated IP $24.95/month. VDM à la carte $0.07/1,000.
  - **New accounts and account-regions with no metered SES activity since 2025-06-01 "will start on the Essentials plan beginning July 21, 2026"** and can switch to à la carte at any time.
  - New AWS customers get up to $200 in Free Tier credits (6-month free plan, credits usable for 12 months).
  - No Seoul-specific pricing differences are listed.
  
  — [Amazon SES pricing](https://aws.amazon.com/ses/pricing/)
- **Conflicting free-tier claim:** a third-party tracker (last verified 2026-02-23) says new customers get 3,000 messages/month free for 12 months. This conflicts with, or predates, the credit-based model on the official page. — [SaaS Price Pulse](https://www.saaspricepulse.com/tools/amazon-ses); [Cloudburn SES pricing](https://cloudburn.io/blog/amazon-ses-pricing)
- **New in 2026:** SES launched inbox-placement estimates (spam-folder rate by domain and campaign, pre-send content tests) and passive blocklist monitoring on **2026-05-29** in all commercial SES regions. — [AWS What's New (KO), May 2026](https://aws.amazon.com/ko/about-aws/whats-new/2026/05/amazon-ses-global-deliverability/)
- **Single-carrier SMS risk:** AWS documents that SMS in each country runs through a single carrier partner, and recommends redundant channels such as SES email. — [AWS End User Messaging SMS supported countries](https://docs.aws.amazon.com/sms-voice/latest/userguide/phone-numbers-sms-by-country.html)

### Inferences
- **Concrete DNS set for Route 53** (example domain `mitjip.kr`; actual domain TBD):
  - (a) Easy DKIM CNAMEs, auto-published. Prior knowledge says there are 3, but the fetched page did not state the count.
  - (b) `bounce.mitjip.kr` MX `10 feedback-smtp.ap-northeast-2.amazonses.com` plus TXT `v=spf1 include:amazonses.com ~all`.
  - (c) `_dmarc.mitjip.kr` TXT `v=DMARC1; p=none; rua=mailto:dmarc@<team mailbox>`. Move to `quarantine` after about 2–4 weeks of clean reports.
  - (d) Send as `알림 <noreply@mitjip.kr>` with `Reply-To` set to a monitored support address.
- **Use the SES API v2 from the arq worker** (boto3 `sesv2.send_email` over HTTPS with the instance role), not SMTP. This sidesteps the EC2 port-25 throttle and avoids SMTP credentials.
- **Bounce and complaint loop:**
  1. Configuration set `mitjip-tx` with event destination **EventBridge → SQS** (or **SNS → SQS**) for Bounce, Complaint, Reject and DeliveryDelay.
  2. The arq worker polls SQS and updates `users.email_status` (`ok` / `bounced` / `complained`).
  3. The UI prompts the user to fix their email and falls back to in-app notifications.
  
  An SNS HTTPS subscription straight to FastAPI also works but needs SNS signature verification. SQS polling is simpler and keeps no public endpoint.
- **Which Gmail/Yahoo rules apply:** 믿집 will never approach 5,000/day, so the formal bulk-sender rules don't apply. The all-sender rules do apply, and SES already handles PTR and TLS. Implementing SPF + DKIM + DMARC alignment anyway costs nothing and matches what Gmail is moving toward (DMARC quarantine enforcement). Transactional notices are not "marketing/subscribed" mail, so one-click List-Unsubscribe is not required. Adding a "알림 설정" link to notification preferences is still good practice and reduces spam complaints.
- **Production-access request content for 믿집:**
  - Mail type: Transactional. Website URL: the deployed site, not localhost.
  - List the triggers: signup verification, vendor-approval result, 견적 도착, 실측 일정 확정, 시공 기간 등록, password reset.
  - Estimated volume: fewer than 1,000/day.
  - Recipient source: users who registered and verified their address.
  - Bounce/complaint handling: suppression list + SNS/EventBridge → worker → DB flag.
  - Spam-free practice: no purchased lists, no marketing.
  
  Domain identity and DKIM should be verified *before* submitting.
- **Pricing plan:** request à la carte ($0.10/1,000) if the account defaults to Essentials. VDM's value is low at this volume, though the difference is cents per month either way.

### Gaps
- The fetched Easy DKIM page did not state the CNAME count or the auto-rotation details.
- The typical initial production quota in Seoul (often cited as 50,000/day and 14/s) was not confirmed on a fetched AWS page.
- The price difference between the Essentials plan and à la carte for Seoul and the switching mechanics were not tested.
- Whether SES inbound (receiving) is available in ap-northeast-2 was not checked. It is not needed if Reply-To points to an external mailbox.

---

## 6. Deliverability to Korean mailboxes (Naver, Daum/Kakao) and Korean law: (광고) labelling vs transactional notices, unsubscribe

### Takeaway
No primary 2025–2026 Naver or Kakao postmaster documentation could be retrieved; see Gaps.
- **Deliverability:** secondary sources say Naver weighs sender authentication (SPF, DKIM, DMARC, rDNS), RBL status and recipient spam reports into a reputation score, and has historically recommended KISA White Domain registration. The practical plan is full authentication (§5), consistent low-volume transactional mail, and manual seed testing to naver.com, daum.net, hanmail.net and kakao.com inboxes.
- **Legal:** 믿집's notifications (견적 도착, 실측 확정, 시공 기간 등록) are transaction-triggered informational messages. They are not 영리목적 광고성 정보, so they need no (광고) label, no ad consent and no legal unsubscribe. This holds only if no promotional content is mixed in. Anything promotional needs explicit prior consent, labelled "광고성 정보 수신동의" in the consent request. The message itself needs "(광고)" and the sender's name, contact details and an opt-out method. KISA's guide revised on 2026-03-04 tightened these rules.

### Cited Findings
- **Naver's guidance (secondary, via search snippets):** Naver recommends registering the sender with **KISA WHITE DOMAIN** in addition to email authentication. Its guide references RBL, KISA White Domain, SPF, rDNS, DKIM and DMARC settings. A sender rated 'poor' is blocked. Spam filters also learn from recipient behaviour. — [The Teams (KR) article, via search; page returned 403 on fetch](https://www.theteams.kr/teams/1013/post/64764); [i-boss (KR)](https://www.i-boss.co.kr/ab-2987-547579)
- **Naver Cloud Outbound Mailer:** Naver Cloud Platform's own mailer fails sends to Gmail recipients itself unless SPF, DKIM and DMARC are all verified, following Gmail's 2024-01-31 change. Its troubleshooting covers recipient-side rejections ("Connection reset", "NONEXISTENT_DOMAIN_ADDRESS") and does not mention Naver or Daum. — [Naver Cloud: Cloud Outbound Mailer troubleshooting](https://guide.ncloud-docs.com/docs/cloudoutboundmailer-troubleshoot-mail)
- **Using your own domain:** authentication should be set up on the sender's own domain, not public domains like naver.com or kakao.com, and Google Postmaster Tools works only for owned domains. — [inblog (KR), 2024-02-02](https://inblog.ai/ko/blog/outbound-mail-spf-dkim-dmarc-arc)
- **Gmail's Korean guide:** Gmail's Korean-language sender guide sets the same SPF/DKIM/DMARC expectations. Many Korean users also use Gmail. — [Google 이메일 발신자 가이드라인](https://support.google.com/a/answer/81126?hl=ko)
- **정보통신망법 제50조:**
  - ① Explicit prior consent is required for 영리목적 광고성 정보 over electronic media, with exceptions such as same-kind goods to customers whose contact details were collected through a transaction.
  - ② No ads after refusal or withdrawal of consent.
  - ③ Ads between 21:00 and 08:00 need separate consent, "다만, 대통령령으로 정하는 매체의 경우에는 그러하지 아니하다".
  - ④ The ad must state the sender's name and contact details and an easy way to refuse or withdraw.
  - ⑤ Hiding the sender identity, harvesting addresses and similar acts are prohibited.
  - ⑥ Refusing must cost the recipient nothing.
  - ⑦ The sender must notify the result of a consent or refusal.
  - ⑧ Consent must be periodically reconfirmed.
  
  — [korea.legal: 정보통신망법 제50조](https://korea.legal/wiki/%ec%a0%95%eb%b3%b4%ed%86%b5%ec%8b%a0%eb%a7%9d-%ec%9d%b4%ec%9a%a9%ec%b4%89%ec%a7%84-%eb%b0%8f-%ec%a0%95%eb%b3%b4%eb%b3%b4%ed%98%b8-%eb%93%b1%ec%97%90-%ea%b4%80%ed%95%9c-%eb%b2%95-21/)
- **Consent reconfirmation interval:** reconfirmation is required every 2 years from the date of consent. — [Bizgo blog (KR)](https://blog.bizgo.io/?p=3380)
- **Advertising vs informational:** a message is advertising if it has *one or more* promotional elements: product promotion, discounts, coupons, events, or prompts to sign up, repurchase, visit or apply. Informational examples include order and delivery status, reservation confirmation, OTP and service notices. Ads must carry **"(광고)" in both subject and body**, plus the business name and an opt-out method, and consent records must be kept. Night sending needs separate consent. — [Solapi 정책 가이드](https://solapi.com/guides/policyguidelines); [Solapi 광고 문자 가이드](https://solapi.com/guides/sms-ad-guide)
- **Penalties and the 2024 guide:** the 2024-01-23 amendment raised penalties for illegal-spam senders from ≤1 year / ₩10M to **≤3 years imprisonment or ₩30M fine**. The KISA guide was revised in March 2024 to reflect it. — [Boannews (2024 guide)](https://m.boannews.com/html/detail.html?idx=128266)
- **2026-03-04 KISA revision:**
  - Vague consent labels such as "혜택 알림" or "정보제공" do not count as explicit consent; the request must say "광고성 정보 수신동의".
  - App-push ad opt-out must lead straight from the ad to the refusal screen, with no login.
  - Unilateral coupon, mileage or point issuance or expiry notices count as ads needing prior consent.
  
  — [Boannews, 2026-03-04](http://www.boannews.com/news/articleView.html?idxno=142460)
- **Background references:** an earlier edition of the KISA guide (2020-07, mirror) and press coverage. — [KISA guide 2020 mirror](https://www.catchsecu.com/download/%EB%B6%88%EB%B2%95-%EC%8A%A4%ED%8C%B8-%EB%B0%A9%EC%A7%80%EB%A5%BC-%EC%9C%84%ED%95%9C-%EC%A0%95%EB%B3%B4%ED%86%B5%EC%8B%A0%EB%A7%9D%EB%B2%95-%EC%95%88%EB%82%B4%EC%84%9C202007); [Etnews IT law column](https://m.etnews.com/201201030032)

### Inferences
- **What counts as informational for 믿집:**
  - Triggered by the user's own transaction, so informational: 견적 요청 접수, 업체 견적 도착, 실측 일정 제안/확정, 시공 기간 등록, 업체 승인/반려 (to vendors), 비밀번호 재설정, 이메일 인증.
  - These emails must not include cross-sell ("다른 업체 추천", "할인 이벤트", coupons). Such content would turn the whole message into 광고성 정보 under the "one or more elements" test and would also violate Kakao 알림톡 rules (§7).
- **Consent UX:** if a newsletter or promotions are ever planned, add a separate optional checkbox, unchecked by default and labelled "광고성 정보 수신동의 (이메일)". Store consent timestamp and channel, reconfirm every 2 years, and follow the (광고) and opt-out rules. That checkbox should not be bundled with the terms of service.
- **Unsubscribe expectations:** transactional mail has no legal unsubscribe requirement. Users still expect control, so provide per-event notification toggles (email on/off per type) in account settings and a footer link "알림 설정 변경". Keep safety-critical mail (password reset, verification) always on.
- **Deliverability checklist for Naver/Daum:**
  - (a) A custom domain with SPF + DKIM + DMARC aligned (§5).
  - (b) Never send from a naver.com or gmail.com From address through SES. It isn't allowed without verification, and DMARC would fail.
  - (c) Plain Korean subject lines without spammy patterns; avoid URL shorteners and image-only bodies.
  - (d) Include a text/plain part.
  - (e) Low, steady volume.
  - (f) Before launch, send test notifications to naver.com, daum.net/hanmail.net and kakao.com accounts, check spam folders, and view the headers (`Authentication-Results`).
  - (g) Watch SES bounce SMTP diagnostic codes from Korean MTAs.

### Gaps
- **Not found:** official Naver Mail or Daum/Kakao Mail sender or postmaster guidelines (2025–2026), whether Naver or Kakao now require DMARC, and the current status of **KISA 화이트도메인** (whether still operating, discontinued, or replaced). The search budget was exhausted before primary pages could be reached, and the one Naver-related article returned 403. These need manual verification on help.naver.com, cs.daum.net/kakao, and KISA's 불법스팸대응센터 (spam.kisa.or.kr).
- **Unverified decree text:** the exact wording of 정보통신망법 **시행령 제61조 / 별표** (which media are exempt from the night-time restriction, and the email subject-line "(광고)" format) was not retrieved. Prior knowledge suggests email is the media exempted from the 21:00–08:00 rule and that "(광고)" goes at the start of the subject, but this must be checked on law.go.kr.
- No 2025–2026 Korean tech-blog evidence was found specifically about SES deliverability to Naver or Daum.

---

## 7. Is email enough? 카카오 알림톡 (NHN Cloud, Solapi, Aligo, Kakao BizMessage) and SMS (AWS End User Messaging vs Korean providers)

### Takeaway
For Korean consumers, 알림톡 is the expected channel for transaction notices, and email open rates for "견적 도착" alerts will be lower. However, 알림톡 requires a **KakaoTalk business channel reviewed with business-registration information**, sending through an official Kakao dealer, and pre-approved templates. A student team without a 사업자등록 likely cannot get it; this is inferred and unconfirmed. The completed bootcamp version should therefore ship email plus in-app notifications, designed behind a channel abstraction, with 알림톡 (₩13/건 at Solapi) and SMS fallback (₩18/건) documented as the first post-launch addition.
- **AWS SMS:** AWS End User Messaging SMS is not viable for Korea. It has no Korean sender IDs, long codes or short codes, only best-effort international routes. Korea's 발신번호 사전등록제 means SMS must go through a Korean provider anyway.

### Cited Findings
- **Solapi price table** (created 2024-10-07, **last modified 2026-07-31**, VAT excluded), lowest tier 1–9,999/month:
  - **알림톡 ₩13**, 친구톡 ₩19.
  - BMS (브랜드 메시지) 텍스트 ₩53 / 이미지 ₩83.
  - **SMS ₩18**, LMS ₩45, MMS ₩110.
  - RCS SMS ₩18.
  
  At 10,000–99,999/month, 알림톡 is ₩10 and SMS ₩15. — [Solapi 발송 구간별 할인 단가표](https://solapi.com/guides/tiered-pricing)
- **Market range:** 알림톡 is priced at about ₩5–15/건 across providers. There were **15 official Kakao 알림톡 dealers as of July 2026**. — [Bizgo: 알림톡 업체 비교 (2026)](https://blog.bizgo.io/inside/alimtalk-provider-selection-guide/)
- **NHN Cloud:** NHN Cloud Notification bundles 알림톡, 친구톡, SMS, international SMS, push, email and RCS. Salesmap's 알림톡 runs on NHN Cloud. NHN's per-message prices were **not retrieved**. — [SmartToday (NHN Cloud Notification)](https://www.smarttoday.co.kr/ko-kr/articles/79524); [Salesmap docs](https://docs.salesmap.kr/alimtalk/starting)
- **알림톡 prerequisites and rules:**
  - A KakaoTalk business channel reviewed with business-registration information ("사업자 정보로 비즈니스 채널 심사").
  - Sending only through an official dealer.
  - Templates pre-registered and approved by Kakao.
  - Body up to 1,300 characters with up to 5 buttons (basic type).
  - Delivered to the phone number whether or not the user added the channel.
  - Informational messages only (no marketing consent needed for those).
  - Non-KakaoTalk users can't receive it, so SMS fallback (대체발송) is common.
  - Promotions must use 카카오 브랜드 메시지.
  
  — [Bizgo: 알림톡이란? (2026-09-04)](https://blog.bizgo.io/howto/alimtalk-guide/)
- **Channel-opening documents:** individual-business owners submit a KakaoTalk e-certificate; corporations submit the 사업자등록증 plus phone verification. Approval takes about 1–3 days. — [Bizgo: 비즈니스 채널 만들기 2026](https://blog.bizgo.io/howto/create-kakaotalk-business-channel-guide-2026/); [Bizgo: 알림톡 1주일 세팅](https://blog.bizgo.io/howto/how-to-send-alimtalk/)
- **Kakao policy change from 2026-01-01:** 알림톡 coupon, mileage and point messages are limited to transaction or contract payouts, usage or expiry information essential to the transaction, and benefits granted with prior consent. Commercial or promotional ones must move to 브랜드 메시지, and affected templates must be re-reviewed. — [Channel.io 공지 (2025-12-29)](https://docs.channel.io/updates/ko/articles/%EA%B3%B5%EC%A7%80-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%95%8C%EB%A6%BC%ED%86%A1-%EB%B0%9C%EC%86%A1-%EA%B0%80%EB%8A%A5-%EA%B8%B0%EC%A4%80-%EB%B3%80%EA%B2%BD-%EC%95%88%EB%82%B42611-%EC%8B%9C%ED%96%89-f9f70118)
- **AWS End User Messaging SMS for South Korea (KR, +82):** short codes **No**, long codes **No**, sender IDs **No**, two-way **No**, international sending **Yes**. Internationally-enabled numbers are "sent on a best effort basis and may be replaced downstream". — [AWS End User Messaging SMS: supported countries](https://docs.aws.amazon.com/sms-voice/latest/userguide/phone-numbers-sms-by-country.html). Self-service sender-ID registration expanded to 19 more countries in January 2025; Korea is not in the registration-form list. — [AWS What's New, Jan 2025](https://aws.amazon.com/ko/about-aws/whats-new/2025/01/aws-end-user-messaging-self-service-id-registration/); [AWS registrations by country](https://docs.aws.amazon.com/ko_kr/sms-voice/latest/userguide/registrations-country.html)
- **발신번호 사전등록제:**
  - Based on 전기통신사업법 제84조의2 and in force since October 2015.
  - Only pre-registered sender numbers may send, and unregistered numbers are blocked.
  - Required documents: a 통신서비스 이용증명원 issued within 1 month, plus a delegation letter if the number belongs to another party.
  - Providers take about 3 business days to verify and allow about 10 numbers per service.
  
  — [Bizgo: 발신번호 사전등록제](https://blog.bizgo.io/?p=3147); [Solapi 발신번호 FAQ](https://solapi.com/guides/senderid-faq); [LG U+ biz insight](https://www.lguplus.com/biz/insight/trend/815)

### Inferences
- **Is email enough for the bootcamp "completed version"?** Yes, if it is paired with an in-app notification center (§8) and the UI shows "이메일로도 알려드렸어요". Email is free at this scale, already integrated, and needs no business registration.
- **For a real launch:** 알림톡 should become the primary push channel, with email as the record and in-app as the source of truth.
- **Effort estimate for 알림톡 via Solapi** (or Aligo/NHN):
  - (1) Business registration.
  - (2) Open a Kakao business channel (about 1–3 days).
  - (3) Register the 발신프로필 at the dealer.
  - (4) Write about 5–7 templates (견적 도착, 실측 확정, 시공 기간 등록, 업체 승인 결과, 회원가입 인증) with variables `#{고객명}` and `#{링크}`, and get Kakao approval.
  - (5) Register a sender number for SMS fallback (통신서비스 이용증명원).
  - (6) Implement a `KakaoAlimtalkChannel` in the arq worker: REST call, store the message ID, handle the fallback result.
  
  That is about 1–2 developer-days of code plus 1–2 weeks of calendar time for approvals.
- **Cost:** 1,000 notifications/month × ₩13 ≈ ₩13,000/month (VAT excl.), plus fallback SMS for the few non-KakaoTalk users.
- **Templates must stay strictly informational.** No coupons or "추천 업체" lines, per both the Kakao 2026 rules and 정보통신망법.
- **Design now, add later:** store `notification_events` and per-user channel preferences now, with the email address and a verified phone number. Adding 알림톡 then means writing a new channel sender, not a schema change.
- **Do not use AWS End User Messaging SMS for Korean recipients.** Its international routes can't use a registered Korean 발신번호 and are best-effort.

### Gaps
- Whether a **non-business individual or student team** can open a Kakao business channel and send 알림톡 at all was not confirmed. The sources only describe the business-registration path.
- NHN Cloud and Aligo per-message prices, and Kakao's template review SLA, were not retrieved.
- The Solapi Python SDK and API specifics were not checked.

---

## 8. In-app notification center as a complement; web push on iOS/Android browsers (2026)

### Takeaway
An in-app notification table is the cheapest, most reliable channel and should be the system of record: every event creates a row, and email (later 알림톡) is a fan-out from that row.
- **Web push:** possible on Android browsers. On iOS it works only for **Home Screen-installed web apps** (iOS 16.4+, with Declarative Web Push from iOS 18.4) and requires a user-gesture permission prompt. Treat it as an optional stretch feature, not a core channel, for Korean consumers who mostly won't install a PWA.

### Cited Findings
- **iOS/iPadOS 16.4 web push requirements:**
  - The site must be added to the Home Screen as a web app, with a manifest whose `display` is `standalone` or `fullscreen`. Otherwise it is only a bookmark.
  - Permission may be requested only in response to a direct user action.
  - It uses the standard Push API, Notifications API and Service Workers.
  - **No Apple Developer Program membership** is needed.
  - Allowlist `*.push.apple.com` if push endpoints are restricted.
  - The Badging API is supported.
  
  — [WebKit: Web Push for Web Apps on iOS and iPadOS](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/)
- **Declarative Web Push:** lets sites show notifications without a service worker and is backward compatible. It is supported only in installed web apps on iOS/iPadOS 18.4+ (March 2025) and in Safari 18.5 on macOS. — [WebKit: Meet Declarative Web Push](https://webkit.org/?p=16535); [Progressier](https://progressier.com/pwa-capabilities/declarative-web-push); [DEV Community (WWDC25)](https://dev.to/arshtechpro/wwdc-2025-declarative-web-push-dn4)
- **iOS limitations:** the Push API is unavailable inside a normal Safari tab ("a technical choice imposed by Apple"). — [Pushpad](https://pushpad.xyz/blog/ios-special-requirements-for-web-push-notifications); 16.4+ baseline — [Netmera guide](https://user.netmera.com/netmera-user-guide/omnichannel-engagement/web-push/mobile-web-push-for-ios). A 2026 practitioner report says iOS PWA push subscriptions can disappear without a clear cause, and that iOS 18 brought no fundamental fix. — [Webscraft 2026](https://webscraft.org/blog/pwa-pushspovischennya-na-ios-u-2026-scho-realno-pratsyuye?lang=en)
- **Redundancy:** AWS itself recommends redundant channels (email, push) alongside SMS. — [AWS End User Messaging SMS: supported countries](https://docs.aws.amazon.com/sms-voice/latest/userguide/phone-numbers-sms-by-country.html)

### Inferences
- **Proposed minimal design** (fits the existing FastAPI + Postgres + Redis + arq stack):
  - Table `notifications(id, user_id, type, title, body, link_path, payload jsonb, created_at, read_at, email_status, email_message_id)` with an index on `(user_id, read_at, created_at desc)`.
  - Insert the row in the **same DB transaction** as the domain change (for example, when a quote is saved). Then enqueue an arq job `deliver_notification(id)` that checks user preferences and sends the SES email.
  - This is effectively a transactional-outbox pattern. If Redis or SES is down, a periodic arq cron re-enqueues undelivered rows.
- **UI:**
  - A header bell with an unread count, fetched on page load and polled every 30–60 s, or pushed through SSE with Redis pub/sub if real-time is desired.
  - A `/notifications` list page and a "모두 읽음" action.
  - Deep links to the quote or measurement page.
  - Deep links must re-run the authorization check; never embed presigned file URLs in notifications.
- **Web push (if attempted):**
  - VAPID keys plus a `push_subscriptions` table and the Python `pywebpush` library (prior knowledge) sent from the arq worker.
  - Android Chrome/Samsung Internet work in-browser (prior knowledge).
  - iOS requires "홈 화면에 추가" plus a button-triggered permission prompt.
  - Expect low opt-in. Keep it behind a feature flag.
- **Channel priority for the bootcamp:** in-app (always) → email (default on, per-type toggles). In a later launch: 알림톡 (primary) → SMS fallback. Web push is optional.

### Gaps
- No 2026 Apple release notes were checked for iOS 26-era changes to Home Screen web push.
- No Korean usage data on PWA installs or web-push opt-in rates was found.
- Android browser web-push behaviour is from prior knowledge, not a fetched 2026 source.

### Source index (all URLs consulted)
AWS S3 / security / pricing
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html
- https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html
- https://docs.aws.amazon.com/AmazonS3/latest/API/v1-rel-RESTBucketPUTlifecycle.md
- https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-s3.LifecycleRule.html
- https://docs.amazonaws.cn/cdk/api/v1/docs/@aws-cdk_aws-s3.CfnBucket.RuleProperty.html
- https://aws.amazon.com/s3/security
- https://sentra.io/learn/s3-bucket-security-best-practices
- https://costgoat.com/pricing/amazon-s3
- https://upstash.com/blog/aws-s3-pricing-explained-2026.md
- https://oneuptime.com/blog/post/2026-02-12-generate-presigned-post-requests-s3-uploads/view
- https://docs.oracle.com/en-us/iaas/Content/Object/s3-post-upload.htm
- https://community.fly.io/t/content-length-range-doesnt-limit-file-upload/25260
- https://fast.io/resources/s3-presigned-url-file-size-limit/

GuardDuty / file security
- https://aws.amazon.com/about-aws/whats-new/2025/02/amazon-guardduty-malware-protection-s3-price-reduction
- https://docs.aws.amazon.com/guardduty/latest/ug/pricing-malware-protection-for-s3-guardduty.html
- https://docs.aws.amazon.com/guardduty/latest/ug/gdu-malware-protection-s3.html
- https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection-s3-quotas-guardduty.html
- https://docs.aws.amazon.com/guardduty/latest/ug/tag-based-access-s3-malware-protection.html
- https://aws.amazon.com/blogs/aws/introducing-amazon-guardduty-malware-protection-for-amazon-s3
- https://barkingiguana.com/writing/how-to-scan-ec2-and-s3-with-guardduty-malware-protection/
- https://cloudburn.io/blog/amazon-guardduty-pricing
- https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
- https://pillow.readthedocs.io/en/stable/reference/Image.html
- https://pillow-heif.readthedocs.io/en/latest/

CloudFront
- https://docs.aws.amazon.com/PricingPlanManager/latest/UserGuide/plans.html
- https://aws.amazon.com/ko/blogs/networking-and-content-delivery/amazon-cloudfront-flat-rate-pricing-plans-new-features-and-expanded-capabilities/
- https://blog.blazingcdn.com/en-us/cloudfront-flat-rate-plans-explained-limits-and-fine-print-2026
- https://builder.aws.com/content/3D6DxKr47HkYZkCY7d2efzYTu1B/no-more-surprise-bills-what-cloudfronts-flatrate-pricing-really-changes

SES
- https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html
- https://docs.aws.amazon.com/ses/latest/dg/manage-sending-quotas.html
- https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dkim-easy.html
- https://docs.aws.amazon.com/ses/latest/dg/mail-from.html
- https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dmarc.html
- https://docs.aws.amazon.com/ko_kr/ses/latest/dg/send-email-authentication-dmarc.html
- https://docs.aws.amazon.com/ses/latest/dg/sending-email-suppression-list.html
- https://docs.aws.amazon.com/ses/latest/dg/monitor-using-event-publishing.html
- https://docs.aws.amazon.com/ses/latest/dg/reputationdashboard-cloudwatch-alarm.html
- https://aws.amazon.com/ses/pricing/
- https://aws.amazon.com/ko/about-aws/whats-new/2026/05/amazon-ses-global-deliverability/
- https://oneuptime.com/blog/post/2026-02-12-move-amazon-ses-out-of-sandbox/view
- https://devopscube.com/amazon-ses-production-access/
- https://mailbluster.com/blog/getting-out-of-amazon-ses-sandbox
- https://blog.campaignhq.co/how-to-get-aws-ses-production-access/
- https://cloudburn.io/blog/amazon-ses-pricing
- https://www.saaspricepulse.com/tools/amazon-ses
- https://go.aws/4bwFazW

Gmail / Yahoo
- https://support.google.com/a/answer/81126?hl=en
- https://support.google.com/a/answer/81126?hl=ko
- https://help.zoho.com/portal/en/community/topic/gmail-is-ramping-up-its-email-sender-policy-from-november-2025?page=1
- https://www.suped.com/knowledge/email-deliverability/compliance/how-to-comply-with-gmails-new-sending-rules-for-bulk-email-senders
- https://techspot.com/news/100374-google-new-spam-rules-ensures-senders-5000-daily.html
- https://senders.yahooinc.com/best-practices
- https://resend.com/docs/knowledge-base/how-do-i-avoid-yahoos-spam-folder.md
- https://messagegears.com/blog/google-yahoo-to-combat-spam-with-new-email-rules-for-bulk-senders/

Korean mailboxes / law
- https://guide.ncloud-docs.com/docs/cloudoutboundmailer-troubleshoot-mail
- https://inblog.ai/ko/blog/outbound-mail-spf-dkim-dmarc-arc
- https://www.theteams.kr/teams/1013/post/64764 (snippet only; 403 on fetch)
- https://www.i-boss.co.kr/ab-2987-547579
- https://korea.legal/wiki/%ec%a0%95%eb%b3%b4%ed%86%b5%ec%8b%a0%eb%a7%9d-%ec%9d%b4%ec%9a%a9%ec%b4%89%ec%a7%84-%eb%b0%8f-%ec%a0%95%eb%b3%b4%eb%b3%b4%ed%98%b8-%eb%93%b1%ec%97%90-%ea%b4%80%ed%95%9c-%eb%b2%95-21/
- https://solapi.com/guides/policyguidelines
- https://solapi.com/guides/sms-ad-guide
- https://blog.bizgo.io/?p=3380
- https://m.boannews.com/html/detail.html?idx=128266
- http://www.boannews.com/news/articleView.html?idxno=142460
- https://www.catchsecu.com/download/%EB%B6%88%EB%B2%95-%EC%8A%A4%ED%8C%B8-%EB%B0%A9%EC%A7%80%EB%A5%BC-%EC%9C%84%ED%95%9C-%EC%A0%95%EB%B3%B4%ED%86%B5%EC%8B%A0%EB%A7%9D%EB%B2%95-%EC%95%88%EB%82%B4%EC%84%9C202007
- https://m.etnews.com/201201030032

알림톡 / SMS
- https://solapi.com/guides/tiered-pricing
- https://solapi.com/guides/senderid-faq
- https://blog.bizgo.io/inside/alimtalk-provider-selection-guide/
- https://blog.bizgo.io/howto/alimtalk-guide/
- https://blog.bizgo.io/howto/create-kakaotalk-business-channel-guide-2026/
- https://blog.bizgo.io/howto/how-to-send-alimtalk/
- https://blog.bizgo.io/?p=3147
- https://www.lguplus.com/biz/insight/trend/815
- https://docs.channel.io/updates/ko/articles/%EA%B3%B5%EC%A7%80-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%95%8C%EB%A6%BC%ED%86%A1-%EB%B0%9C%EC%86%A1-%EA%B0%80%EB%8A%A5-%EA%B8%B0%EC%A4%80-%EB%B3%80%EA%B2%BD-%EC%95%88%EB%82%B42611-%EC%8B%9C%ED%96%89-f9f70118
- https://docs.salesmap.kr/alimtalk/starting
- https://www.smarttoday.co.kr/ko-kr/articles/79524
- https://docs.aws.amazon.com/sms-voice/latest/userguide/phone-numbers-sms-by-country.html
- https://aws.amazon.com/ko/about-aws/whats-new/2025/01/aws-end-user-messaging-self-service-id-registration/
- https://docs.aws.amazon.com/ko_kr/sms-voice/latest/userguide/registrations-country.html

Web push
- https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
- https://webkit.org/?p=16535
- https://progressier.com/pwa-capabilities/declarative-web-push
- https://dev.to/arshtechpro/wwdc-2025-declarative-web-push-dn4
- https://pushpad.xyz/blog/ios-special-requirements-for-web-push-notifications
- https://user.netmera.com/netmera-user-guide/omnichannel-engagement/web-push/mobile-web-push-for-ios
- https://webscraft.org/blog/pwa-pushspovischennya-na-ios-u-2026-scho-realno-pratsyuye?lang=en
