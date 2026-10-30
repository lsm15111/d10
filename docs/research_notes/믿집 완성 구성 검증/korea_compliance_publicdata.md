# 믿집 — Korean legal/compliance requirements & public-data APIs (checked 2026-10-29)

Method note: research, not legal advice. Statute texts were read mainly through nepla.ai/korea.legal/itwiki mirrors of 국가법령정보센터 (law.go.kr itself does not render to the fetch tool), plus PIPC/KISA/data.go.kr pages, law-firm newsletters and news. The shared WebSearch budget ran out after about 25 searches. After that I fetched known or already-found URLs directly, so a few items stay unverified (see each Gaps list). "법령 mirror" means a third-party copy of the official text; a lawyer or law.go.kr should confirm the exact wording. Today is 2026-10-29. Several rules changed in 2025–2026, and their effective dates are given below.

## 1. 개인정보 보호법 (PIPA): legal basis, 처리방침 contents, CPO, and the 2026 amendment

### Takeaway
Since the 2023 amendment, signup, quote and account data can be processed without consent under 제15조①4 (계약 이행/체결 과정의 요청). The 처리방침 must still list those items and their legal basis. Giving 동·호수 and contact details to a vendor is 제3자 제공 and needs consent. The PIPA amendment in force since 2026-09-11 (법률 제21445호) adds 대표자 최종책임, 유출 "가능성" notification, and 10% 과징금 for serious or repeat violations. Its board-approval CPO rule and mandatory ISMS-P cover only very large processors, not 믿집.

### Cited Findings
- **Current text and dates:** 개인정보 보호법 법률 제21445호, 2026.03.10 일부개정, 시행 2026.09.11. The 시행령 (대통령령 제36671호) took effect the same day. — [법령 mirror: PIPA](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95); [법령 mirror: 시행령](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9); [Yulchon newsletter](https://www.yulchon.com/ko/resources/publications/newsletter-view/45098/page.do); [Newsis 2026-03-09](https://www.newsis.com/view/NISX20260309_0003540588)
- **제15조① legal bases:** (1) consent; (2) a statute or legal obligation; (3) public-institution duties; (4) performing a contract with the data subject, or steps the subject requested while contracting; (5) urgent life/body/property interest; (6) legitimate interest that clearly outweighs the subject's rights; (7) urgent public safety. — [법령 mirror: PIPA](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95)
- **2023 change:** the amendment (2023.3.14 개정) removed "불가피하게" from 제15조①4. Commentators compare the result to GDPR's contractual-necessity basis. — [itwiki 2023 개정 시사점](https://itwiki.kr/w/2023.3.14._%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%EB%B2%95_%EC%A0%84%EB%A9%B4%EA%B0%9C%EC%A0%95_%EC%8B%9C%EC%82%AC%EC%A0%90); [korea.legal 제15조](https://korea.legal/wiki/%ea%b0%9c%ec%9d%b8%ec%a0%95%eb%b3%b4-%eb%b3%b4%ed%98%b8%eb%b2%95-%ec%a0%9c15%ec%a1%b0/)
- **Limit on 제15조①4:** the test is what the data subject could reasonably expect from the contract (대법원 2016두55117 SKT 부활충전). The PIPC 개정 해설 (2023-12-23) says processing within the scope both parties can foresee needs no separate consent. — [nepla wiki 계약 근거](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/계약에-근거하여-개인정보를-적법하게-수집-이용하는-방법-0o486ol18el5); [nepla wiki 해외 클라우드 FAQ](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/-일문일답-해외-클라우드-aws-등-에서-개인정보를-보관-처리할-때-정보주체의-동의를-받아야-하는가-54gnvzpe81pr)
- **PIPC 처리방침 작성지침 (2025-04 개정):**
  - Contract-type processing (예: '회원서비스 운영', A/S 상담) can run without consent.
  - 민감정보, 고유식별정보 and 제3자 제공 still need consent even inside a contract relationship.
  - 필수 기재사항 (목적, 처리·보유기간, 파기 절차 등) are now separated from 권장사항 (third-party 행태정보 collection and refusal, 권익침해 구제방법).
  - Items may be listed by 유형 when itemizing is hard.
  - — [Newsis/검색요약](https://mobile.newsis.com/view/NISX20260424_0003604909); [Daeryun newsletter](https://www.daeryunlaw.com/newsletter/news/151)
- **작성지침 2026-04 개정 (생성형 AI 부록):** AI service providers must state:
  - whether user-entered text, voice or files are collected and stored;
  - whether that data is used for model training, and how users opt out;
  - how users report inappropriate AI answers or object to them.
  - The same revision allows listing 수탁자 by category when there are many or they change often (with a pointer to where the actual 수탁자 can be looked up). If any personal data is stored on a server, a 처리방침 is mandatory.
  - — [Newsis 2026-04-24](https://mobile.newsis.com/view/NISX20260424_0003604909)
- **제30조① 처리방침 기재사항:**
  - 1 처리 목적; 2 처리·보유 기간; 3 제3자 제공; 3의2 파기 절차·방법, including the legal basis and items for any data kept under another law; 3의3 민감정보 공개 가능성 and how to opt out;
  - 4 위탁; 4의2 가명정보 처리;
  - 5 정보주체·법정대리인 권리 and how to exercise them; 6 CPO name (or responsible department) and contact; 7 자동수집장치 (cookies, logs): operation and refusal;
  - 8 대통령령 사항.
  - — [법령 mirror: PIPA](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95)
- **시행령 제31조:** adds 처리 항목, 국외 이전 근거, 안전성 확보조치, and the country name when data is collected directly from abroad. The policy must be posted continuously on the homepage. — [법령 mirror: 시행령](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9)
- **제22조 (consent):**
  - Consent is taken separately per purpose (collection, 제3자 제공, 민감, 고유식별, marketing).
  - For data processed without consent, the controller must disclose the items and legal basis, for example in the 처리방침. The controller carries the burden of proving that consent was not needed.
  - Service may not be refused because a user declines optional or marketing consent.
  - — [법령 mirror: PIPA](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95)
- **CPO (제31조, 시행령 제32조):**
  - If no CPO is designated, the 사업주/대표자 is the CPO.
  - Outside public institutions, the CPO is the 사업주, 대표자 or an 임원 (or a department head if there is no 임원).
  - 소상공인 are exempt from the designation duty.
  - The 2026 시행령 제32조③ requires a qualified CPO only for entities with 매출 over 1,800억원 that also process 민감·고유식별정보 of 5만명+ or personal data of 100만명+ (plus large universities, 상급종합병원 and 공공시스템운영기관).
  - The CPO must be able to act independently.
  - — [법령 mirror: 시행령](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9); [Shin&Kim on the draft 시행령](https://shinkim.com/kor/media/newsletter/3319)
- **New 제30조의3 (2026):** the 사업주/대표자 is the "최종적인 책임자" for safe processing. — [법령 mirror: PIPA](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95)
- **Other 2026 changes:**
  - 과징금 cap of up to 10% of total revenue for repeat (3 years), 1,000만명+ or 시정명령-ignoring breaches; reductions for privacy investment.
  - CPO board approval and filing for large entities only.
  - 기존 CPO 계도기간 until 2027-12-31 (per newsis/search summary).
  - — [Newsis](https://www.newsis.com/view/NISX20260309_0003540588); [Shin&Kim](https://shinkim.com/kor/media/newsletter/3319)
- **제37조의2 (자동화된 결정):** the right to refuse applies only to fully automated decisions that materially affect rights or obligations. It does not apply when the decision rests on 제15조①1·2·4 (consent, law, contract). Controllers must publish their criteria and procedures. — [법령 mirror: PIPA](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95)

### Inferences
- **Who counts as 개인정보처리자:** a student team running a public site with real users likely is one ("업무를 목적으로 … 개인" under 제2조). Not fetched this session; confirm.
- **Legal basis map for 믿집:**
  - 계약 이행 (제15조①4), no consent checkbox:
    - customer: name, email, password hash, home info (region, apartment, size, schedule, budget), uploaded photos and floor plans, quote history;
    - vendor: 담당자 name, email, password, 사업자등록증.
  - Consent: sharing 동·호수 and phone with the chosen vendor (제3자 제공). The 2025 지침 says 제3자 제공 needs consent even within a contract. Take it just-in-time at "실측 요청", per vendor, showing 받는 자, 목적, 항목, 보유기간, 거부권·불이익. These are the standard 제17조② items; verify the wording.
  - Optional consent: marketing (see §6) and any reuse of user data for AI evaluation (see §4).
- **표준견적서 / AI explanations:** these are not "decisions" that bind users, so 제37조의2 is very unlikely to apply. Still, describing the estimate logic in the 처리방침 or an FAQ is cheap.
- **처리방침 skeleton:**
  - 처리 목적·항목·근거 table (marking 계약 vs 동의);
  - 보유기간 / 파기;
  - 제3자 제공 (vendor at measurement request);
  - 위탁 table (AWS, OpenAI, mail/SMS provider);
  - 국외 이전 table (OpenAI US);
  - 안전성 확보조치;
  - 권리 행사 (열람·정정·삭제·처리정지·동의철회 → 탈퇴 button);
  - CPO (team lead name and email);
  - cookies / 자동수집장치;
  - 생성형 AI 부록 (입력 저장 여부, 학습 미사용, 신고 창구);
  - 변경 이력.

### Gaps
- The 시행령 별표 1 CPO 자격요건 text and the exact 시행령 wording for 유출 가능성 통지 criteria were not read.
- The 2026-04 작성지침 PDF was not fetched (news summary only). Rules for 처리방침 변경 notice timing come only from a search summary.
- The 제17조② item list was not re-verified this session.

## 2. 처리위탁 and 국외 이전 (AWS Seoul, SES, OpenAI US, messaging providers)

### Takeaway
List AWS (Seoul), the email/SMS provider and OpenAI as 수탁자 under 제26조②. Sending (masked) user text to the OpenAI API, processed in the US, is a 국외 이전 under 제28조의8. Without separate consent, use the 계약 이행 route (①3) with full disclosure in the 처리방침 or by email. AWS Seoul storage is most plausibly domestic 위탁, not 국외 이전; a lawyer should confirm because AWS is a foreign company.

### Cited Findings
- **제26조 (위탁):**
  - ① requires a written contract (ban on use outside the 위탁 purpose, technical and managerial safeguards, and more).
  - ② requires disclosing the 위탁 업무 and 수탁자, including 재수탁자, so users can check them at any time.
  - ③ requires a separate notice to users when the 위탁 is for marketing or sales.
  - ④ requires training and supervising the 수탁자; ⑥ requires consent before 재위탁.
  - ⑦ treats the 수탁자 as the controller's employee for damages.
  - — [korea.legal 제26조](https://korea.legal/wiki/개인정보-보호법-제26조/)
- **제28조의8① routes:**
  1. 별도 동의;
  2. a law or treaty;
  3. 처리위탁·보관 necessary to conclude and perform a contract with the data subject, plus disclosure in the 처리방침 (가목) or notice by email etc. (나목);
  4. a PIPC-designated 인증 held by the recipient, plus safeguards;
  5. a PIPC 동등성 인정 for the country.
  - — [법령 mirror: PIPA](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95); [nepla wiki 국외이전](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/개인정보의-국외이전-mo59y3rr81vj); [PIPC 국외이전 page](https://pipc.go.kr/np/default/page.do?mCode=D060040000)
- **Items to disclose or consent to (제28조의8②):**
  - 이전 항목;
  - 이전 국가, 시기, 방법;
  - 받는 자 (법인명, 연락처);
  - 받는 자의 이용목적 and 보유·이용기간;
  - 거부 방법, 절차, 효과.
  - Any change requires renewed notice and consent (③).
  - — [nepla wiki 국외이전](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/개인정보의-국외이전-mo59y3rr81vj); [nepla wiki 해외 클라우드 FAQ](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/-일문일답-해외-클라우드-aws-등-에서-개인정보를-보관-처리할-때-정보주체의-동의를-받아야-하는가-54gnvzpe81pr)
- **시행령 제29조의10:** for a transfer, apply 안전성 확보조치 and 고충처리·분쟁해결 measures, agree them with the recipient in advance, and write them into the contract. The 처리방침 must also state the 국외 이전 근거. — [법령 mirror: 시행령](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9); [PIPC 국외이전 page](https://pipc.go.kr/np/default/page.do?mCode=D060040000)
- **Storing Korean users' data on overseas cloud servers counts as 국외 이전.** The PIPC reads "계약 이행에 필요" by service nature and business structure (PIPC 개정 해설 2023-12-23 p.46). An overseas 수탁자 listed only in the 처리방침 does not replace consent outside the contract-necessity case. — [nepla wiki 해외 클라우드 FAQ](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/-일문일답-해외-클라우드-aws-등-에서-개인정보를-보관-처리할-때-정보주체의-동의를-받아야-하는가-54gnvzpe81pr); [search summary](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/개인정보의-국외이전-mo59y3rr81vj)
- **AWS region commitment:** "We will not move or replicate your content outside of your chosen AWS Region(s) without your agreement." The exceptions are what is necessary for services the customer starts, and legal or binding orders. — [AWS Data Privacy FAQ](https://aws.amazon.com/compliance/data-privacy-faq/)
- **AWS Seoul certification:** AWS holds K-ISMS for the Seoul Region and a Seoul edge location (first certified 2017-12-27, annual surveillance; the current certificate is in AWS Artifact). The page claims K-ISMS, not ISMS-P. — [AWS K-ISMS](https://aws.amazon.com/compliance/k-isms/)
- **OpenAI API data handling:**
  - API data is not used for training by default (since 2023-03-01).
  - Abuse-monitoring logs are kept up to 30 days.
  - Zero Data Retention needs approval.
  - Responses API keeps application state at least 30 days unless `store=false`. Chat Completions keeps no state except prompt caching (up to 24h) and audio.
  - South Korea data residency (`kr.api.openai.com`) is **storage only, not regional processing**. It requires ZDR or Modified Abuse Monitoring and a sales contract.
  - — [OpenAI "Your data"](https://developers.openai.com/api/docs/guides/your-data)
- **PIPC 생성형 AI 안내서 (2025-08-06):**
  - Covers 서비스형 LLM, for example ChatGPT API integration.
  - Warns that external API inputs may go to overseas servers, and recommends securing safety through license contracts and terms.
  - Recommends PbD and a 개인정보 영향평가 for large or sensitive processing, and CPO involvement from planning.
  - Recommends input/output filtering and access control for API integrations.
  - — [byline 2025-08-06](https://byline.network/2025/08/6-277/); [Shin&Kim EN](https://www.shinkim.com/eng/media/newsletter/2942); [search summary/DT](https://www.dt.co.kr/article/12009611?ref=naver)

### Inferences
- **위탁 table in the 처리방침:**
  - AWS (hosting and storage: EC2, RDS, S3; email sending: SES);
  - the SMS or 알림톡 vendor, if used;
  - OpenAI (AI 설명 생성).
- **AWS Seoul:** AWS commits to keep content in-region, so it is reasonable to treat it as domestic 위탁 and **not** list it as 국외 이전. Confirm with counsel, because AWS staff may reach the systems remotely from abroad.
- **Check SES region:** confirm SES actually runs in ap-northeast-2. If mail is sent through a US SES region, list it as 국외 이전.
- **OpenAI 국외 이전 table:**
  - 항목: masked text inputs (home attributes, quote line items), never names, emails, phone numbers or 동·호수;
  - 국가: 미국;
  - 시기·방법: when AI 설명 is requested, over HTTPS API;
  - 받는 자: OpenAI (legal entity name and contact to be filled in from the contract);
  - 목적: 설명문 생성;
  - 보유: up to 30 days of abuse-monitoring logs, no training use;
  - 거부: turn off AI 설명; the estimate still works.
- **Engineering:** call with `store=false`; send no images or floor plans unless they are disclosed and needed.
- **Masked data:** if the masked payload truly cannot identify anyone, it may not be personal data. Masked free text and photos can still be identifiable, though, so disclosing anyway is the safer choice.
- **OpenAI DPA:** accept or record OpenAI's DPA in the team's records. That supports both the 제26조① 문서 and the 시행령 제29조의10 contract-reflection duties.

### Gaps
- No PIPC statement was found on whether a foreign CSP's Korea region is 국외 이전.
- The OpenAI DPA page returned 403, so the subprocessor list and transfer clauses were not read.
- SES ap-northeast-2 availability was not verified.
- The PIPC list of designated 국외이전 인증 and 동등성 countries (PIPC menu D060040020) was not read.

## 3. 개인정보의 안전성 확보조치 기준 (고시): concrete controls, including the 2025-10-31 amendment whose deferred items start 2026-10-31

### Takeaway
At 믿집's scale (well under 1만 정보주체), the 고시 still requires:
- 접근권한 minimum and per-person accounts, with records kept 3 years;
- lockout after failed logins;
- secure authentication for remote/admin access;
- password one-way hashing;
- encryption in transit;
- 접속기록 of admins and staff for ≥1년;
- a check cycle defined in a plan.

The 2025-10-31 amendment's deferred provisions take effect 2026-10-31. They replace the fixed "월 1회 점검" with a cycle the controller sets itself, and extend log and authentication duties to all non-data-subject accessors.

### Cited Findings
- **2025-10-31 amendment, timing:** the amended 고시 took effect 2025-10-31. 제2조 (정의) and 제6조의2 (인터넷망 차단) applied immediately. The 내부관리계획, 접근권한, 접근통제 and 접속기록 provisions got a 1-year grace period, to 2026-10-31. — [byline 2025-10-31](https://byline.network/2025/10/31-281/); [nepla wiki 2025 개정](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/망분리에서-위험기반-보호-로-2025년-개정-개인정보-안전성확보조치-고시의-의미-gy3807x469rx)
- **Wider scope after the amendment:**
  - The differentiated-access rule moves from 개인정보취급자 to 업무수행자.
  - The failed-authentication restriction covers everyone who accesses the system.
  - Secure authentication for external access covers all legitimate accessors except data subjects.
  - Open-market sellers' logs are retained only (inspection may be limited to 취급자).
  - 출력·복사 and 파기 are added to the 내부관리계획.
  - Large processors (일평균 100만명+) may exempt low-risk terminals from 망분리 after a risk analysis.
  - — [byline](https://byline.network/2025/10/31-281/); [nepla wiki](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/망분리에서-위험기반-보호-로-2025년-개정-개인정보-안전성확보조치-고시의-의미-gy3807x469rx)
- **제8조 접속기록:**
  - ① keep the access logs of anyone who accessed the 개인정보처리시스템 (except data subjects) for **1년 이상**. Keep them **2년 이상** if the system holds 5만명+ data subjects, processes 고유식별정보 or 민감정보, or belongs to a 기간통신사업자.
  - ② set the check cycle, method and follow-up for 접속기록 and download activity in the 내부관리계획. This replaces the earlier "월 1회 이상 점검".
  - ③ protect logs against forgery, alteration and loss.
  - — [itwiki 제8조](https://itwiki.kr/w/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98_%EC%95%88%EC%A0%84%EC%84%B1_%ED%99%95%EB%B3%B4%EC%A1%B0%EC%B9%98_%EA%B8%B0%EC%A4%80_%EC%A0%9C8%EC%A1%B0)
  - Until the new 제8조② takes effect, the 월 1회 duty still applies, and suspicious lookups or bulk downloads need their reason checked. — [Lawtimes](https://www.lawtimes.co.kr/news/articleView.html?idxno=228195)
- **제5조 접근권한:**
  - ① grant minimum access, differentiated by role;
  - ② change or revoke access without delay when duties change;
  - ③ keep records of grants, changes and revocations **최소 3년**;
  - ④ one account per 취급자, no sharing;
  - ⑤ apply and manage authentication means safely;
  - ⑥ restrict access after a set number of failed authentications.
  - — [itwiki 제5조](https://itwiki.kr/w/개인정보의_안전성_확보조치_기준_제5조)
- **제7조 암호화:**
  - ① passwords, biometric data and other 인증정보 must be encrypted when stored or sent. Passwords must be **one-way encrypted**.
  - ② users' 주민등록번호, passport, driver's license, alien registration, credit card and account numbers, and biometric data must be encrypted at rest.
  - ④ personal data sent over the internet must be encrypted.
  - ⑥ key-management procedures are required only for large/mid-size companies with 10만명+ or SMEs with 100만명+.
  - — [itwiki 제7조](https://itwiki.kr/w/개인정보의_안전성_확보조치_기준_제7조)
- **제4조 내부관리계획:**
  - 18 required items, including CPO, access control, encryption, logs, malware, vulnerability checks, physical, 출력·복사, 파기, incident response, risk analysis and 수탁자 oversight.
  - The plan may be omitted by 소상공인·개인·단체 handling fewer than 1만 정보주체.
  - ④ CPO checks implementation at least once a year.
  - — [itwiki 제4조](https://itwiki.kr/w/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98_%EC%95%88%EC%A0%84%EC%84%B1_%ED%99%95%EB%B3%B4%EC%A1%B0%EC%B9%98_%EA%B8%B0%EC%A4%80_%EC%A0%9C4%EC%A1%B0)
- **Wiki summary of 제6조 (접근통제):** IP restriction and intrusion detection; VPN, dedicated line or 2FA for external access; session timeout; leak prevention. — [itwiki 고시 개요](https://itwiki.kr/w/개인정보의_안전성_확보조치_기준)
- **Cloud users:** under the 2023-09-22 version, 제6조⑥ exempts them from 취급자 network separation (a lighter internet-blocking measure is allowed instead). — [nepla wiki 해외 클라우드 FAQ](https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/-일문일답-해외-클라우드-aws-등-에서-개인정보를-보관-처리할-때-정보주체의-동의를-받아야-하는가-54gnvzpe81pr)

### Inferences
- **Implementation checklist for 믿집:**
  - bcrypt or argon2 for passwords (one-way);
  - TLS everywhere, including the RDS connection;
  - S3 Block Public Access and pre-signed URLs only;
  - RDS and S3 at-rest encryption (KMS);
  - admin console only behind 2FA or VPN/IP allowlist;
  - per-person admin accounts;
  - lockout after N failures (for example 5);
  - session timeout;
  - an append-only admin access log (who, when, what record, and downloads) kept ≥1년, for example in CloudWatch Logs with retention 400 days and write-once (S3 Object Lock);
  - an access-grant change log kept 3년.
- **Optional items:** a 내부관리계획 is optional under 1만명, but a 1–2 page plan (check cycle such as monthly log review, roles, 파기) is cheap. It also turns the new 제8조② "self-defined cycle" into something the team can show.
- **No 2-year retention needed:** none of the 2-year triggers apply (no 고유식별/민감정보, under 5만명). A vendor's 사업자등록번호 is not 고유식별정보, but avoid collecting 대표자 주민번호. A 사업자등록증 image of an 개인사업자 shows 생년월일 and address, so restrict its access.

### Gaps
- The 고시 number and the official consolidated text of the 2025-10-31 version were not read on law.go.kr.
- The exact current 제6조 wording (공개 노출 방지, 미사용 시 차단) is from a wiki summary only.
- The PIPC's 2025 "안전성 확보조치 안내서" was not read.

## 4. 만 14세 미만, 파기 on withdrawal (and retention exceptions), 가명처리 for AI/eval data, 유출 통지

### Takeaway
- **Under-14 users:** block signup with an age check rather than build 법정대리인 consent.
- **Withdrawal:** "delete immediately" is lawful and matches 제21조. Only data another law requires keeping must be split off and kept: 전자상거래법 records only where 믿집 actually processed them, and 통신비밀보호법 로그 3개월 is arguable.
- **AI evaluation:** reusing user data for AI evaluation should use 가명정보 under 제28조의2 (통계·연구), with a set 처리기간.
- **Breaches:** notify within 72h. Report to PIPC/KISA if 1,000+ people are affected, or after any outside hacking (external unlawful access) regardless of count. Since 2026-09-11, even a *possible* leak must be notified.

### Cited Findings
- **제22조의2 (만 14세 미만):**
  - ① controllers need, and must verify, 법정대리인 consent;
  - ② the minimum data needed to get that consent may be collected from the child;
  - ③ notices to children must use easy language;
  - ④ methods are set by 대통령령.
  - — [korea.legal 제22조의2](https://korea.legal/wiki/%ea%b0%9c%ec%9d%b8%ec%a0%95%eb%b3%b4-%eb%b3%b4%ed%98%b8%eb%b2%95-%ec%a0%9c22%ec%a1%b0%ec%9d%982/); [inews24 2022-08](https://www.inews24.com/view/1514669)
- **제21조 (파기):**
  - ① destroy data without delay when it is no longer needed, for example when the 보유기간 ends, the purpose is achieved, or the 가명정보 처리기간 ends, unless another law requires keeping it;
  - ② destroy so it cannot be restored;
  - ③ store data kept under another law separately from other data.
  - — [korea.legal 제21조](https://korea.legal/wiki/개인정보-보호법-제21조/)
  - 시행령 제16조: electronic files must be "복원이 불가능한 방법으로 영구 삭제". — [법령 mirror: 시행령](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9)
- **전자상거래법 시행령 제6조 retention (current 대통령령 제36507호, 시행 2026-07-21):**
  - 표시·광고 6개월;
  - 계약·청약철회 5년;
  - 대금결제·재화공급 5년;
  - 소비자 불만·분쟁처리 3년.
  - 통신판매중개자 must keep these only for records "자신의 정보처리시스템을 통하여 처리한" (processed through its own systems).
  - — [법령 mirror: 전자상거래법 시행령](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0%20%EC%8B%9C%ED%96%89%EB%A0%B9)
- **통신비밀보호법:**
  - 제2조11호 마목 (인터넷 로그기록자료) and 사목 (접속지 추적자료) must be kept for **3개월 이상** (시행령 제41조②, 시행 2026-10-02). Other 통신사실확인자료 are kept 12개월.
  - The duty sits on "전기통신사업자" (제15조의2).
  - — [법령 mirror: 통신비밀보호법](https://www.nepla.ai/law/%ED%86%B5%EC%8B%A0%EB%B9%84%EB%B0%80%EB%B3%B4%ED%98%B8%EB%B2%95); [법령 mirror: 시행령](https://www.nepla.ai/law/%ED%86%B5%EC%8B%A0%EB%B9%84%EB%B0%80%EB%B3%B4%ED%98%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9)
  - Typical Korean 처리방침 list 통비법 접속로그·IP 3개월, 전자상거래법 5년/3년, and 본인확인 기록 6개월 as withdrawal exceptions. — [search summary of corporate policies, e.g.](https://www.spacek.co.kr/etc/privacy.do); [ISMS 3.4.1 파기 해설](https://www.cela.kr/ISMS_3_4)
- **가명정보 (제28조의2~):**
  - May be processed without consent for 통계작성 (including commercial statistics), 과학적 연구 and 공익적 기록보존.
  - 추가정보 (mapping tables) must be stored separately.
  - Re-identification is banned (과징금 up to 3% of revenue), and processing records must be kept.
  - The wiki lists the PIPC 가명정보 처리 가이드라인 as dated 2020-09-24 (possibly outdated).
  - — [itwiki 가명정보](https://itwiki.kr/w/가명정보)
  - **Conflict:** itwiki says 제21조 does not apply to 가명정보. The current 제21조① explicitly lists "가명정보의 처리 기간 경과" as a 파기 trigger (the 2023 amendment). — [korea.legal 제21조](https://korea.legal/wiki/개인정보-보호법-제21조/)
- **유출 등 (제34조, as amended 2026):**
  - ① notify affected users without delay;
  - ② **new**: notify when there is a *possibility* of a leak;
  - "유출 등" now includes 위조·변조·훼손 (for example ransomware);
  - the notice must explain remedies.
  - — [법령 mirror: PIPA](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95); [Newsis](https://www.newsis.com/view/NISX20260309_0003540588)
- **Breach deadlines (시행령):**
  - 제39조: notify data subjects within **72시간**.
  - 제40조: report to 보호위원회 or KISA within 72시간 when 1천명+ are affected, when 민감·고유식별정보 leaks, or when the leak came from **외부 불법접근**.
  - — [법령 mirror: 시행령](https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9); [Shin&Kim draft summary](https://shinkim.com/kor/media/newsletter/3319)

### Inferences
- **Age gate:** at signup, add a required "만 14세 이상입니다" check (or a birth-year field) and refuse under-14 signups. Apartment owners are adults, so building a 법정대리인 flow is unnecessary.
- **Withdrawal flow** ("account + projects + files deleted immediately"):
  - Hard-delete RDS rows and S3 objects, including all versions if S3 Versioning is on, and derived thumbnails.
  - Purge vector or embedding stores and caches.
  - Write down how long backups (RDS automated snapshots, up to 35 days) keep deleted data and how they expire. State this in the 처리방침 ("백업은 최대 N일 후 자동 삭제").
- **What survives withdrawal:**
  - Without payments or contracts, 전자상거래법 5-year records mostly do not arise.
  - Complaint or dispute records 믿집 handled itself could fall under the 3-year rule if 믿집 is a 통신판매중개자 (see §7).
  - Keep 접속 IP logs 3개월 only if the team decides 통비법 applies. Most Korean services keep them, and it is low-risk.
  - Admin 접속기록 (≥1년) and 권한 변경 기록 (3년) concern staff, not the withdrawn user, and stay.
  - List these exceptions explicitly in the 처리방침.
- **AI evaluation data:** use synthetic data, or 가명처리 copies (drop name, email, phone, 동·호수; generalize apartment to region and size band; strip photos). Set a 처리기간, log processing, and store the key mapping separately or not at all. If the data is fully 익명, PIPA no longer applies.
- **Incident runbook:** 72h notify + report, and a "가능성" notice for suspected leaks (for example an exposed S3 bucket).

### Gaps
- 시행령 제17조의2 (법정대리인 동의 확인 방법) was not read.
- The latest version of the PIPC 가명정보 처리 가이드라인 (2024/2025 revisions, 비정형 데이터 such as photos) was not verified.
- Whether a tiny, non-registered web service is an "전기통신사업자" bound by 통비법 retention was not confirmed; lawyer.

## 5. 위치정보법: does photo EXIF GPS make 믿집 subject to 위치정보사업/위치기반서비스사업 신고?

### Takeaway
Stripping EXIF/GPS before storage is the right design. 위치정보 means location "측위된 것" through telecom facilities. Location picked up incidentally, without any collection purpose, has been excluded since the 2022 amendment. A street address or 동·호수 is 개인정보, not 개인위치정보. Keeping GPS coordinates tied to accounts would create an arguable 개인위치정보 issue, and stripping avoids it.

### Cited Findings
- **Definitions:** 제2조1호 defines 위치정보 as information on where a mobile object or person is or was at a given time, "측위(測位)된 것" using telecom facilities. 제2조2호 defines 개인위치정보 as location of a specific person, including when easily combined with other information. — [법령 mirror: 위치정보법](https://www.nepla.ai/law/%EC%9C%84%EC%B9%98%EC%A0%95%EB%B3%B4%EC%9D%98%20%EB%B3%B4%ED%98%B8%20%EB%B0%8F%20%EC%9D%B4%EC%9A%A9%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0)
- **Registration and reporting:**
  - 제5조: 개인위치정보 위치정보사업 requires **등록** with **방송미디어통신위원회** (renamed by 법률 제21066호, 시행 2025-10-01).
  - 제9조: 위치기반서비스사업 requires **신고**. Under 제9조의2, 소상공인 and 1인 창조기업 may start first and report within 1 month.
  - 제15조: collecting 개인위치정보 requires consent.
  - Penalties: unregistered 위치정보사업 5년/5천만원; unreported LBS 3년/3천만원; 양벌규정 applies.
  - — [법령 mirror: 위치정보법](https://www.nepla.ai/law/%EC%9C%84%EC%B9%98%EC%A0%95%EB%B3%B4%EC%9D%98%20%EB%B3%B4%ED%98%B8%20%EB%B0%8F%20%EC%9D%B4%EC%9A%A9%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0)
- **2022 amendment (시행 2022-04-20):** 위치정보 is limited to what is "측위"된 것. Information a service learns incidentally, without a location-collection purpose (card payments, CCTV), falls outside the definition. — [Shin&Kim 2022-04](https://www.shinkim.com/kor/media/newsletter/1789?page=131); [search summary](https://ko.wikisource.org/wiki/%EC%9C%84%EC%B9%98%EC%A0%95%EB%B3%B4%EC%9D%98_%EB%B3%B4%ED%98%B8_%EB%B0%8F_%EC%9D%B4%EC%9A%A9_%EB%93%B1%EC%97%90_%EA%B4%80%ED%95%9C_%EB%B2%95%EB%A5%A0)
- **Practitioner view:**
  - Collecting customers' GPS, Wi-Fi AP or cell data to provide a service triggers the LBS 신고, even if nothing is stored and only a result is returned.
  - Services that don't collect a specific individual's location don't need to report.
  - Residential or delivery addresses are 개인정보, not 개인위치정보.
  - — [CatchSecu](https://www.catchsecu.com/archives/11350)
- **EXIF content:** photo EXIF can carry the GPS latitude and longitude of where the photo was taken. — [GNOME EXIF help](https://help.gnome.org/users/eog/stable/plugin-exif-digital.html.ko)

### Inferences
- Phone EXIF GPS *was* produced by device positioning. If 믿집 kept it linked to a user account, someone could argue it is 개인위치정보 received from the user. 믿집 provides no location-based service and has no purpose of collecting location, so the 2022 "부수적 정보" exclusion likely applies even before stripping. Stripping removes the doubt.
- **Implementation:**
  - Strip EXIF/XMP/GPS **client-side** before upload (canvas re-encode). Also strip again on the server ingest path in memory before writing to S3, covering both originals and derivatives.
  - Never log coordinates.
  - Reject or strip HEIC metadata too.
  - Add a test asserting stored objects have no GPS tags.
  - Mention "사진의 위치정보(EXIF)는 저장 전 삭제" in the 처리방침.
- **동·호수:** handled as 개인정보 under PIPA (§1, §2), not 위치정보법.

### Gaps
- No 방송미디어통신위원회 or KISA 유권해석 specifically on photo EXIF metadata was found; a lawyer could confirm.

## 6. 정보통신망법 / 전기통신사업법: 광고성 정보 vs service notices, 본인확인, 부가통신 신고, CISO

### Takeaway
- **Service notices** ("견적 도착", "실측 일정", "업체 승인/반려") are transactional 정보성 messages and need no 광고 consent, as long as no promotion is mixed in.
- **Marketing** needs explicit opt-in, "(광고)" labeling, easy opt-out, a 14-day result notice and a 2-year re-confirmation.
- **Identity checks:** no law requires 휴대폰 본인인증, and collecting 주민번호 is prohibited.
- **Registrations:** with capital ≤1억원, 부가통신사업 is deemed reported and the CISO is the 대표자. The 2026-07-07 정보통신망법 amendment (허위조작정보) targets distributors, not small boards.

### Cited Findings
- **제50조 (광고성 정보):**
  - ① explicit prior consent, with a transaction-relationship exception;
  - ③ separate consent for **21:00–08:00**;
  - ④ show the sender's name, contact and how to refuse;
  - ⑥ refusal at no cost;
  - ⑦ notify the result of consent or refusal;
  - ⑧ periodically re-confirm consent.
  - — [itwiki 정보통신망법 제50조](https://itwiki.kr/w/정보통신망법_제50조)
- **시행령 (시행 2026-10-02):**
  - 제61조①: the transaction exception covers **6개월** after the transaction ends;
  - 제61조②: **전자우편** is exempt from the night-time separate consent;
  - 제62조의2: send the consent-result notice within **14일**;
  - 제62조의3: re-confirm consent **every 2 years**.
  - — [법령 mirror: 정보통신망법 시행령](https://www.nepla.ai/law/%EC%A0%95%EB%B3%B4%ED%86%B5%EC%8B%A0%EB%A7%9D%20%EC%9D%B4%EC%9A%A9%EC%B4%89%EC%A7%84%20%EB%B0%8F%20%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0%20%EC%8B%9C%ED%96%89%EB%A0%B9)
- **Message classification (practitioner guide):**
  - "(광고)" goes at the start of the title.
  - Transaction notices, requested one-time info, contract or terms changes, and security notices are not ads.
  - Any ad content makes the whole message an ad.
  - Mere sign-ups don't qualify for the transaction exception.
  - — [1point blog](https://1point.kr/blog/insights/ad-message)
- **KISA/방송미디어통신위원회 revised 불법스팸 안내서 (announced 2026-03-04):**
  - Coupon, point and expiry notices are ads needing prior consent.
  - Consent screens labeled "혜택 알림/정보제공" are not valid ad consent.
  - App-push opt-out must not require a login.
  - — [Boannews 2026-03](http://www.boannews.com/news/articleView.html?idxno=142460); [Boannews earlier edition](https://m.boannews.com/html/detail.html?idx=128266)
- **제23조의2 (주민등록번호):** 정보통신서비스 제공자 may not collect or use 주민등록번호 unless designated a 본인확인기관 (or the carrier-resale case). The article imposes no general identity-verification duty. — [itwiki 제23조의2](https://itwiki.kr/w/정보통신망법_제23조의2)
- **부가통신 신고 (전기통신사업법 제22조, 시행 2026-10-01, 법률 제21503호):**
  - ① 부가통신사업 requires a report to 과기정통부.
  - ⑤ a small business meeting the 대통령령 capital test is deemed to have reported.
  - 시행령 제30조: internet-based 부가통신사업자 with **자본금 1억원 이하** qualify. They must report within 1 month once capital exceeds 1억원.
  - — [법령 mirror: 전기통신사업법](https://www.nepla.ai/law/%EC%A0%84%EA%B8%B0%ED%86%B5%EC%8B%A0%EC%82%AC%EC%97%85%EB%B2%95); [법령 mirror: 시행령](https://www.nepla.ai/law/%EC%A0%84%EA%B8%B0%ED%86%B5%EC%8B%A0%EC%82%AC%EC%97%85%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9)
- **CISO (정보통신망법 시행령 제36조의7):** for 자본금 1억원 이하, the 사업주/대표자 fills the role. If no CISO is reported, the 사업주/대표자 is deemed designated. — [법령 mirror: 정보통신망법 시행령](https://www.nepla.ai/law/%EC%A0%95%EB%B3%B4%ED%86%B5%EC%8B%A0%EB%A7%9D%20%EC%9D%B4%EC%9A%A9%EC%B4%89%EC%A7%84%20%EB%B0%8F%20%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0%20%EC%8B%9C%ED%96%89%EB%A0%B9)
- **2026 정보통신망법 amendment (법률 제21305호, 공포 2026-01-06, 시행 2026-07-07):** introduces "허위조작정보", punitive damages up to 5× for knowing distribution, and up to 10억원 fines for repeat business distributors (draft decree threshold around 10만 subscribers or views). — [Lawtalk](https://www.lawtalk.co.kr/posts/164921)

### Inferences
- **Message types:** keep transactional templates (quote arrived, measurement scheduled or changed, vendor approved or rejected, account or security notices) free of promotions. Then no 광고 consent and no "(광고)" label are needed.
- **If newsletters or promotions are added:**
  - a separate optional opt-in (not bundled, per PIPA 제22조);
  - a "(광고)" prefix;
  - a one-click unsubscribe;
  - a 14-day result email;
  - a 2-year re-confirmation job;
  - email only, to avoid the night-time rule.
- **SMS/알림톡 vendor:** list it as a PIPA 수탁자. If it sends marketing, PIPA 제26조③ requires notifying users of that 위탁.
- **No 휴대폰 인증 needed:** email verification is enough. Vendors are businesses, so the 전자상거래법 개인 판매자 phone-verification duty (§7) doesn't apply.
- **Student team:** with no capital, the team falls under the deemed-report rule. Revisit both the 부가통신 report and the CISO question if the team incorporates with more than 1억원 capital.

### Gaps
- The full 정보통신망법 제45조의3 (CISO) text and the 과태료 amounts for 제50조 violations were not verified (one blog says up to 3천만원).
- The new KISA 안내서 PDF was not read.

## 7. 전자상거래법: is a quote-matching platform without payments a 통신판매중개자?

### Takeaway
Probably yes, or close enough that complying is cheap. The 2026 text defines 통신판매중개 as allowing use of a cyber mall to broker a 통신판매 of 재화 *or 용역* between parties. The duties attach without any payment element:
- an up-front notice that "믿집은 통신판매의 당사자가 아님" (initial screen, ads, contract documents, 청약 steps);
- vendor 신원정보 shown before the 청약;
- complaint handling within 3 and 10 business days;
- 사이버몰 operator identity in the footer;
- review-policy disclosure (§8).

The text of 제12조 (신고) is addressed to 통신판매업자. Sources disagree on whether a pure 중개자 must file, so a lawyer should confirm before commercial launch.

### Cited Findings
- **Current text and definitions:** 법률 제21312호 (2026-01-20), 시행 2026-07-21.
  - 제2조2호 통신판매: providing 재화·용역 sale information by telecom and receiving the consumer's 청약.
  - 제2조4호 통신판매중개: "거래 당사자 간의 통신판매를 알선하는 행위" by letting others use a 사이버몰, among other methods.
  - — [법령 mirror: 전자상거래법](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0)
- **제20조 duties:**
  - ① give advance notice that the platform is not a party;
  - ② verify business sellers' 신원정보 and provide it before the 청약;
  - ③ promptly act on complaints and disputes.
  - 제20조의2: joint liability for consumer loss if ① is not given. For ②, joint liability applies if the information is missing or false, unless due care was shown.
  - — [법령 mirror](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0); [korea.legal 통신판매중개자의 책임](https://korea.legal/wiki/%ed%86%b5%ec%8b%a0%ed%8c%90%eb%a7%a4%ec%a4%91%ea%b0%9c%ec%9e%90%ec%9d%98-%ec%b1%85%ec%9e%84/)
- **Where the notice goes (시행규칙 제11조의2):** the 사이버몰 초기화면, the first page of ads in the platform's name, contract documents, and the relevant 청약 step. — [korea.legal](https://korea.legal/wiki/%ed%86%b5%ec%8b%a0%ed%8c%90%eb%a7%a4%ec%a4%91%ea%b0%9c%ec%9e%90%ec%9d%98-%ec%b1%85%ec%9e%84/)
- **신원정보 and complaint handling:**
  - 시행령 제25조 (as of 2026-07-20): 상호, 대표자 (for an 개인 seller, the seller's name), 주소, 전화, 전자우편, 통신판매업 신고번호 (per korea.legal), 사업자등록번호, plus verified identity or credit information if held.
  - 시행령 제25조의2: keep complaint staff and facilities, post dispute-resolution standards in advance, report progress within **3영업일** and the result or plan within **10영업일**.
  - — [법령 mirror: 시행령](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0%20%EC%8B%9C%ED%96%89%EB%A0%B9); [korea.legal](https://korea.legal/wiki/%ed%86%b5%ec%8b%a0%ed%8c%90%eb%a7%a4%ec%a4%91%ea%b0%9c%ec%9e%90%ec%9d%98-%ec%b1%85%ec%9e%84/)
- **제10조 (사이버몰 운영자):** display 상호, 대표자, 주소 (including where complaints are handled), 전화, 전자우편, 사업자등록번호 and the 이용약관. — [법령 mirror](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0)
- **당근마켓 case:** 공정위 (announced 2025-03-05) sanctioned 당근마켓 for not providing business sellers' 신원정보, not giving the "당사자 아님" notice on the initial screen, and not displaying operator info and terms. The result was 시정명령 and a 과태료 of 100만원. — [Dealsite](https://dealsite.co.kr/articles/137678); [Newsseoul](https://newsseoul.co.kr/news/view/1065589816318462)
- **Court view (law-firm summary):** a court declined to hold an open-market 중개자 liable where "거래 당사자가 아님" was clearly shown on the homepage initial screen. — [Lawtalk post](https://www.lawtalk.co.kr/posts/115661)
- **제12조 신고 text:** ① covers only "통신판매업자", with a small-volume exemption set by 공정위 고시. — [법령 mirror](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0)
- **Conflicting views on 신고:**
  - A Toss Payments guide (2025) lists "앱, 플랫폼을 통한 중개 서비스 운영" among cases that must file 통신판매업 신고. It states the exemption as fewer than 20 transactions or under 1,200만원 over 6 months for individuals. — [Toss Payments](https://www.tosspayments.com/blog/articles/sales-registration)
  - A law blog says a platform becomes a 통신판매업자 if it advertises in its own name or handles refunds itself. — [help-me.kr](https://www.help-me.kr/blog/article/ecommerce-brokerage-incorporation-guide/)
  - 크몽 shows sellers filing on the platform. — [kmong](https://kmong.com/support/expert-center/posts/671)
- **제21조의2 (온라인 인터페이스 금지행위, added 2024-02-13):** bans drip pricing, pre-checked options, misleading choice layouts, cancellation harder than signup, and repeated pop-ups. — [법령 mirror](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0)
- **New 제20조의4 (2026):** 중개자 duties for 개인 간 거래, such as verifying an individual seller's phone. Violations carry 과태료 up to 1천만원. — [법령 mirror](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0)
- **Pending bill:** a 2026-06 bill would require platforms to separate their own products from brokered ones. It is not law yet. — [MTN 2026-06-17](https://news.mtn.co.kr/news-detail/2026061711262527736)

### Inferences
- **Whether 믿집 is a 중개자:** interior work is a 용역. 믿집 lets vendors present quotes on its site and customers "request" them, so a regulator could see it as 알선 of 통신판매. A counter-argument is that the actual 청약 and contract happen offline after measurement. The duties are cheap, so comply as if 믿집 is a 중개자:
  - Footer and signup notice: "믿집은 통신판매중개자로서 통신판매의 당사자가 아니며, 업체와 고객 간 계약·시공·대금에 대한 책임은 각 당사자에게 있습니다". Repeat it on the quote-request and measurement-request steps and on any downloadable 표준견적서 PDF.
  - Vendor card shown before the request: 상호, 대표자, 사업장 주소, 전화, 이메일, 사업자등록번호, 통신판매업 신고번호 if the vendor has one.
  - Complaint SLA: acknowledge within 3 business days and resolve or give a plan within 10. Post the dispute-handling standards.
  - Keep complaint records for 3 years. That is a lawful exception to "delete on withdrawal" for those records only.
  - Footer operator info: for a student project, the team name, representative and contact. No 사업자등록번호 exists yet; avoid implying a business.
- **Interface rules (제21조의2):** withdrawal must be as easy as signup (a one-click flow is already planned). No pre-ticked marketing boxes.
- **통신판매업 신고:** obligations generally apply when the activity is carried on as a business ("업"). A non-commercial bootcamp demo is unlikely to need it. Before any commercial operation, get a lawyer's view and register if needed.

### Gaps
- The current 공정위 고시 on 통신판매업 신고 면제 is unverified. Toss's 20회/1,200만원 figure may be outdated; another commonly cited version is 직전년도 50회 미만 or 간이과세자, also not verified.
- No 공정위 유권해석 on 견적 중개 platforms was found.
- The exact 시행규칙 제11조의2 text was not read.

## 8. Reviews and ratings of vendors: 표시광고법 / 추천·보증 심사지침, 전자상거래법 제21조의4, 정보통신망법 임시조치

### Takeaway
A review feature now has a concrete disclosure duty. Since 2026-07-21 (전자상거래법 제21조의4 and 시행령 제27조의3), a business posting consumer reviews must show, on the first review screen or one linked directly from it:
- who may write reviews;
- how long reviews stay posted;
- the rating criteria and their effects;
- the deletion criteria and the objection procedure.

Any reward for reviews (draws, points, "top reviewer") or any vendor-paid review must be disclosed in the title or at the start (추천·보증 심사지침, 시행 2024-12-01). For defamation reports, implement the 30-day 임시조치 workflow (정보통신망법 제44조의2).

### Cited Findings
- **제21조의4 (정보의 투명성 확보 조치, new by 법률 제21312호, 시행 2026-07-21):**
  - Businesses doing e-commerce or 통신판매업자 that post 사용후기 must disclose 게시기간, 등급평가 및 삭제 기준 and 삭제 시 이의제기 절차.
  - Violations carry 과태료 up to **1천만원** (제45조④8) and 공정위 시정조치 (제32조).
  - — [법령 mirror: 전자상거래법](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0)
- **시행령 제27조의3 (added 2026-07-20):** show the writer eligibility, posting period, rating criteria and effects, and deletion criteria and objection procedure on the first screen where reviews appear, or on a screen linked directly from it. — [법령 mirror: 시행령](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0%20%EC%8B%9C%ED%96%89%EB%A0%B9)
- **제21조①1:** bans luring consumers through false or exaggerated facts or "기만적 방법". — [법령 mirror](https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0)
- **추천·보증 심사지침 개정 (행정예고 2024-11-19, 시행 2024-12-01):**
  - Future or conditional rewards are 경제적 이해관계 and must be disclosed.
  - Conditional wording such as "소정의 수수료를 지급받을 수 있음" is not a clear disclosure.
  - Blog and text media must put the disclosure in the title or first part.
  - Violations are likely 부당 표시·광고 under 표시광고법 제3조, leading to 시정명령, 공표, 과징금 and possibly criminal penalties.
  - Example: 2024-07-25, two agencies got 시정명령, 공표 and 과징금 for hidden-sponsorship and no-experience reviews.
  - — [Shin&Kim newsletter 2613](https://shinkim.com/kor/media/newsletter/2613); [i-boss summary](https://www.i-boss.co.kr/ab-74668-1685)
- **공정위 추천보증 안내서 (2025-12-02):**
  - 25 Q&As.
  - Posting to win a draw or to be chosen as a top reviewer counts as a future or conditional benefit.
  - Endorsement means a third party's evaluation that consumers can recognize as such.
  - Economic interest includes cash, free goods, discounts, employment and family ties.
  - — [Ajunews 2025-12-02](https://www.ajunews.com/view/20251202085042877)
- **정보통신망법 제44조의2 (임시조치):**
  - A person claiming rights infringement may request deletion or a rebuttal.
  - The provider must act without delay and notify both sides.
  - If infringement is unclear, the provider may block access for up to **30일**, and the poster can seek reinstatement.
  - Taking these measures can reduce or exempt the provider's liability.
  - 제44조의3 allows voluntary 임시조치.
  - — [Lawtalk 2026](https://www.lawtalk.co.kr/posts/164921); [Lawtalk 임시조치](https://www.lawtalk.co.kr/posts/177280); [nepla wiki 게시글 관리](https://www.nepla.ai/wiki/it-%EC%A0%95%EB%B3%B4-%EB%B0%A9%EC%86%A1%ED%86%B5%EC%8B%A0/%EC%9D%B8%ED%84%B0%EB%84%B7-%EB%B0%A9%EC%86%A1-%ED%86%B5%EC%8B%A0/%EC%A0%95%EB%B3%B4%ED%86%B5%EC%8B%A0%EB%A7%9D%EB%B2%95-%EC%83%81-%ED%94%8C%EB%9E%AB%ED%8F%BC-%EC%9A%B4%EC%98%81%EC%9E%90%EC%9D%98-%EA%B2%8C%EC%8B%9C%EA%B8%80-%EA%B4%80%EB%A6%AC-%EB%B0%A9%EB%B2%95-g6w93mqxnojp)
- **Court and 헌재 positions:**
  - 대법원 2016다271608: without a specific, individual deletion request and with unclear infringement, there is no deletion duty.
  - 헌재 upheld 임시조치 as constitutional (6:3).
  - Defamation under 제70조 is a 반의사불벌죄.
  - — [Lawtalk 임시조치](https://www.lawtalk.co.kr/posts/177280); [Lawtimes 헌재](https://www.lawtimes.co.kr/news/166260)

### Inferences
- **Review policy page** (linked from every vendor's review block):
  - 작성 자격: only customers who received a quote or measurement from that vendor through 믿집 ("인증된 후기");
  - 게시기간: for example until the author deletes it or withdraws;
  - 평점 산정: the average of 1–5 stars; how it affects ranking; no paid boosting;
  - 삭제 기준: 욕설, 개인정보, 허위 확인, 광고, 권리침해 임시조치;
  - 이의제기: a form with response SLA.
- **Vendor and incentive rules:**
  - Vendors cannot delete or hide reviews.
  - Never pay for reviews, or have staff or vendors write them. Selectively hiding negatives risks 제21조①1 기만.
  - If any incentive is given, auto-insert "[포인트 지급 후기]" at the start of the review.
- **임시조치 flow:** report button → hide for up to 30 days → notify the author and the reporter → allow an objection or reinstatement → keep a log. The 2026-07-07 punitive-damages rule targets knowing distributors of false information, not hosts that run this process.
- **Withdrawal and reviews:** decide whether a withdrawn user's reviews are deleted (simplest, and matches "delete everything") or anonymized. State the choice in the 처리방침.

### Gaps
- The 추천·보증 심사지침 full text and its 시행일 were not read on law.go.kr or ftc.go.kr.
- No 공정위 guidance specific to platform-run star ratings was found.
- The 제45조 과태료 amount comes from a mirror summary.

## 9. ISMS / ISMS-P: certification thresholds

### Takeaway
Not required. Mandatory ISMS starts at 정보통신서비스 매출 100억원 or 일평균 이용자 100만명. ISMS-P is voluntary until the 2026 PIPA amendment's mandatory ISMS-P provision. That provision covers only 1조원-revenue/300만-daily-user-class entities, carriers and 본인확인기관, and starts 2027-07-01 (draft deadline 2028-12-31).

### Cited Findings
- **정보통신망법 시행령 제49조②:**
  - 1: 매출 or 세입 1,500억원+ that is a 상급종합병원 or a school with 1만+ students;
  - 2: 정보통신서비스 매출 100억원+;
  - 3: 전년도 일일평균 이용자 100만명+;
  - plus ISPs and IDCs per law.
  - — [법령 mirror: 정보통신망법 시행령](https://www.nepla.ai/law/%EC%A0%95%EB%B3%B4%ED%86%B5%EC%8B%A0%EB%A7%9D%20%EC%9D%B4%EC%9A%A9%EC%B4%89%EC%A7%84%20%EB%B0%8F%20%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0%20%EC%8B%9C%ED%96%89%EB%A0%B9); [Alchera](https://www.alchera.ai/resource/blog/isms-certification-mandatory-subject); [itwiki ISMS-P 대상](https://itwiki.kr/w/ISMS-P_%EC%9D%B8%EC%A6%9D_%EB%8C%80%EC%83%81)
- **ISMS vs ISMS-P status:**
  - ISMS is mandatory under 정보통신망법 제47조; ISMS-P is voluntary (PIPA 제32조의2).
  - Covered companies must certify by 8/31 of the following year; failure can bring a 과태료 of up to 3천만원.
  - 1,222 organizations are certified (921 ISMS, 301 ISMS-P).
  - — [byline 2025-11-20](https://byline.network/2025/11/20-518/)
- **간편인증 (since 2024-07-24):** for SMEs with under 300억원 정보통신서비스 매출 and cloud-hosted firms; 36–40 fewer criteria and 50%/40% lower fees. — [Alchera](https://www.alchera.ai/resource/blog/isms-certification-mandatory-subject)
- **2026 PIPA amendment, mandatory ISMS-P:**
  - The provision starts 2027-07-01. — [Newsis](https://www.newsis.com/view/NISX20260309_0003540588)
  - Draft-decree targets: PIPC-designated 공공시스템운영기관, 이동통신사, 본인확인기관, and entities with 매출 1조원+, 정보통신서비스 매출 100억원+ and 일평균 국내 정보주체 300만명+; certification deadline 2028-12-31. — [Shin&Kim draft summary](https://shinkim.com/kor/media/newsletter/3319)

### Inferences
- With a few hundred users and no revenue, 믿집 is orders of magnitude below every threshold. The ISMS-P control list is still a good checklist for the §3 controls.

### Gaps
- The final 시행령 text of the ISMS-P mandatory criteria (the Shin&Kim figures come from the 입법예고 draft) was not checked.

## 10. AI 기본법 (added because 믿집 shows OpenAI-generated explanations)

### Takeaway
Since 2026-01-22, a business offering a service "based on" generative AI must tell users in advance that the service uses it (제31조①). Generated outputs must also be labeled as AI-generated (②). 믿집 likely counts as an 인공지능이용사업자 once it operates as a business. A label is a cheap fix: "AI가 생성한 설명이며 참고용입니다", plus an up-front notice.

### Cited Findings
- **Definitions (제2조):** 인공지능사업자 includes corporations, organizations, individuals and 국가기관 running an AI-industry business. An 인공지능이용사업자 offers products or services built on AI supplied by a developer. — [법령 mirror: AI 기본법](https://www.nepla.ai/law/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%20%EB%B0%9C%EC%A0%84%EA%B3%BC%20%EC%8B%A0%EB%A2%B0%20%EA%B8%B0%EB%B0%98%20%EC%A1%B0%EC%84%B1%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EA%B8%B0%EB%B3%B8%EB%B2%95)
- **제31조:**
  - ① give advance notice when a product or service is based on 고영향 or 생성형 AI;
  - ② label generative-AI outputs;
  - ③ make clear when virtual content is hard to tell from real (deepfake-type);
  - ④ details are left to 대통령령.
  - 제43조: violating ① carries a 과태료 of up to 3천만원.
  - General 시행 2026-01-22; some provisions start 2026-07-21.
  - — [법령 mirror: AI 기본법](https://www.nepla.ai/law/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%20%EB%B0%9C%EC%A0%84%EA%B3%BC%20%EC%8B%A0%EB%A2%B0%20%EA%B8%B0%EB%B0%98%20%EC%A1%B0%EC%84%B1%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EA%B8%B0%EB%B3%B8%EB%B2%95); [Wikipedia (ko)](https://ko.wikipedia.org/wiki/인공지능_발전과_신뢰_기반_조성_등에_관한_기본법)
- **고영향 AI:** covers fields such as medical, nuclear and disaster management, hiring and credit, with stricter duties. — [Wikipedia (ko)](https://ko.wikipedia.org/wiki/인공지능_발전과_신뢰_기반_조성_등에_관한_기본법)

### Inferences
- Interior quote explanations are not 고영향 AI.
- **Practical steps:**
  - A notice at signup or before the first AI explanation: "견적 설명 일부는 생성형 AI(OpenAI)로 작성됩니다".
  - A visible "AI 생성" badge on each explanation.
  - A "부적절한 답변 신고" link. That link also satisfies the 2026-04 처리방침 지침's 생성형 AI 부록.

### Gaps
- The 시행령 notice and labeling methods, any 과태료 계도기간 announced by 과기정통부, and whether a non-commercial student project is an "사업자" were not verified.

## 11. Vendor verification: 국세청 사업자등록 API, KISCON, 대한전문건설협회, and the 실내건축공사업 registration threshold

### Takeaway
Add the 국세청 사업자등록정보 진위확인·상태조회 API (data.go.kr 15081808). It is free, needs no restrictions, takes 100 records per call and allows 100만 calls a day. Use it at vendor signup (validate 번호 + 개업일자 + 대표자명) and in a periodic status sweep (휴업/폐업 → suspend). Neither KISCON nor 대한전문건설협회 offers an open API for 실내건축공사업 registration. Verify the 업종 manually on KISCON's 건설업체 정보조회 and store the registration number and check date.

Under 건설산업기본법, 전문공사 at or above **1,500만원** (종합 5,000만원) requires a registered contractor. Brokering name-lending is a crime, so 믿집 should flag large quotes from unregistered vendors.

### Cited Findings
- **국세청 API (data.go.kr 15081808):**
  - Two functions: 진위확인 (checks 사업자등록번호, 개업일자, 대표자명) and 상태조회 (계속, 휴업 or 폐업, 과세유형, 폐업일).
  - 1회 100건, 1일 100만건; 무료; 이용허락범위 제한 없음; JSON/XML REST.
  - Synced with NTS data every 30 minutes; new businesses can take 1–2 days to appear.
  - Coverage from 2020-01; last modified 2026-05-13.
  - — [data.go.kr 15081808](https://www.data.go.kr/data/15081808/openapi.do)
- **Call details:**
  - Requests are POST with a JSON body, and the service key goes in the URL.
  - If the encoded key fails, try the decoded one (or the reverse).
  - Call from the server so the key stays hidden.
  - A mismatched 대표자명 returns a non-match even when the number is valid.
  - — [Alchera blog](https://www.alchera.ai/resource/blog/business-registration-certificate-authentication-api)
- **VPC test namespace:** dataset 15142860 offers a test API with the same format, 100 items per call. — [data.go.kr 15142860](https://www.data.go.kr/catalog/15142860/openapi.json)
- **KISCON:**
  - 건설업체 정보조회 searches by 업체명, 대표자, 사업자등록번호, 법인등록번호 or region, and covers "건설업 등록된 모든 업체".
  - 80,573 firms as of 2026-10-28 (18,030 종합, 67,774 전문).
  - No open API or bulk download is mentioned.
  - — [KISCON](https://www.kiscon.net/)
- **국토교통부 "건설사업 업체 목록" API (15061039):** returns 업체명, 사업자번호, 대표자, 주소 and project participation. No 업종 or 건설업 등록 field was found. — [data.go.kr 15061039](https://www.data.go.kr/data/15061039/openapi.do)
- **대한전문건설협회:** has a "전문건설업체조회" menu; no API is mentioned. — [KOSCA](https://www.kosca.or.kr/)
- **건설산업기본법 (시행 2025-11-27, 법률 제21034호):**
  - 제9조: registration is required except for 경미한 건설공사.
  - 제16조: contracting requires registration for the 업종.
  - 제21조③: no one may 알선 name or certificate lending.
  - 제22조: written contract with price and period.
  - 제28조: 하자담보 10년 for structural, 5년 for others.
  - 제95조의2: unregistered construction or brokering lending carries 5년/5천만원.
  - — [법령 mirror: 건설산업기본법](https://www.nepla.ai/law/%EA%B1%B4%EC%84%A4%EC%82%B0%EC%97%85%EA%B8%B0%EB%B3%B8%EB%B2%95)
- **시행령 제8조 (current 대통령령 제36437호, 2026-06-23):** 경미한 건설공사 means 종합공사 under 5,000만원 or 전문공사 under 1,500만원 (공사예정금액, client-supplied materials included, split contracts added together). — [법령 mirror: 시행령](https://www.nepla.ai/law/%EA%B1%B4%EC%84%A4%EC%82%B0%EC%97%85%EA%B8%B0%EB%B3%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9)

### Inferences
- **Vendor signup:**
  - Vendors type 사업자등록번호, 개업일자 and 대표자명 (no OCR needed). The server calls `validate`, then `status`.
  - The admin sees the result next to the uploaded certificate.
  - After approval, keep the number, the result and the date. Consider deleting the certificate image after N days to minimize personal data (an 개인사업자's certificate shows 생년월일 and address).
- **Status sweep:** run weekly (100 per call, negligible quota) and auto-hide 휴업 or 폐업 vendors.
- **실내건축공사업:**
  - Add an optional field "실내건축공사업 등록번호".
  - The admin checks it on KISCON and records a "등록 확인 (YYYY-MM-DD)" badge.
  - For quotes ≥1,500만원, warn customers when the vendor has no verified registration.
  - Never let vendors borrow another firm's registration; that risks 제21조③ 알선.
- **표준견적서 note:** add "실제 계약은 건설산업기본법 제22조에 따라 서면으로 체결하세요" as user guidance.

### Gaps
- The exact JSON field names (commonly cited as `b_no`, `start_dt`, `p_nm`, `b_stt_cd`) were not verified this session; the swagger was not reachable.
- Whether 실내건축공사업 is classed as a 전문공사 in 시행령 별표 1 (it is understood to be a 전문건설업 since the 2022 업종 개편) is unconfirmed.
- KISCON's terms on automated lookup were not checked. Don't scrape it.

## 12. Public data API terms: data.go.kr license, 건축HUB, 조달청 가격정보, KASI 특일정보, 도로명주소 API

### Takeaway
All four planned datasets are listed "이용허락범위 제한 없음" and free, so commercial use, modification and storage are allowed. Still show a source credit. data.go.kr can throttle burdensome use (약관 제14조⑤) and disclaims quality and outage liability (제16조). So cache aggressively:
- 건축물대장 per 단지/호;
- 조달청 prices per semiannual release;
- 공휴일 per year, refreshed when 대체/임시공휴일 are 관보-published.

Keep keys on the server.

### Cited Findings
- **data.go.kr license types (공공누리):**
  - Type 0 / 자유이용 (no conditions), Type 1 (출처표시, commercial and derivative use allowed), Types 2–4 (non-commercial and/or no modification), and an AI-training type.
  - 약관 제12조 lists prohibited user acts; 제14조⑤ lets providers limit burdensome API use; 제16조 limits provider liability (공공데이터법 제36조).
  - No explicit caching or storage rule.
  - — [data.go.kr 이용정책](https://www.data.go.kr/ugs/selectPortalPolicyView.do)
- **KOGL 제1유형 attribution:** state the source or rights holder, link to the source website, and don't imply endorsement. The page includes a sample credit sentence. — [문체부 공공누리](https://www.mcst.go.kr/kor/s_open/kogl/koglType.jsp?pTab=01)
- **건축HUB 건축물대장정보 (15134735):**
  - 10 operations (표제부, 기본개요, 층별개요, **전유공용면적**, 주택가격, 전유부, 총괄표제부, and more).
  - 이용허락 제한 없음; free; updated monthly; source is 세움터.
  - JSON with `_type`, XML by default; `sigunguCd` and `bjdongCd` are required.
  - Primary keys changed in the move from the 건축데이터 민간개방시스템.
  - Last modified 2026-07-10; contact 02-2187-4164.
  - The traffic limit is not shown on the page.
  - — [data.go.kr 15134735](https://www.data.go.kr/data/15134735/openapi.do)
- **조달청 나라장터 가격정보현황서비스 (15129415):**
  - 11 operations (시설공통자재 by field, 시장시공가격, 공종분류, 표준시장단가및시장시공가격, 자원분류및순수자원).
  - 이용허락 제한 없음; free.
  - Prices are 조달청 reference values for cost estimates and can vary with quantity and conditions. Surveys cover the whole country except Jeju.
  - **Conflict:** the metadata says "실시간", but the notes say 자재 prices are updated semiannually.
  - — [data.go.kr 15129415](https://www.data.go.kr/data/15129415/openapi.do)
- **한국천문연구원 특일정보 (15012690):**
  - Covers 공휴일, 국경일, 기념일, 24절기 and 잡절; params `solYear` (required) and `solMonth`.
  - 이용허락 제한 없음; free.
  - 대체공휴일 appear only after the 법제처 review, 국무회의/대통령 approval and **관보 공포**.
  - — [data.go.kr 15012690](https://www.data.go.kr/data/15012690/openapi.do)
- **행정안전부 실시간 주소정보 조회 (검색API, 15057017):** "1 시스템 1 승인키", usable right after applying, free, 이용허락 제한 없음, real-time, JSON/XML. — [data.go.kr 15057017](https://www.data.go.kr/data/15057017/openapi.do)
- **Common data.go.kr error:** an expired key returns a "사용 기한 만료" error and must be renewed on the portal (per search summary). — [data.go.kr error-code dataset listing](https://www.data.go.kr/data/15156198/fileData.do)

### Inferences
- **Source credits** (footer of the 표준견적서 page and PDF):
  - "출처: 국토교통부 건축HUB 건축물대장정보(공공데이터포털)";
  - "조달청 나라장터 가격정보(시장시공가격·표준시장단가, YYYY 상/하반기)";
  - "한국천문연구원 특일정보".
  - Add a disclaimer that prices are public reference values, not quotes, and exclude Jeju. That also reduces 표시광고법 risk from presenting the reference estimate as a price.
- **Caching:**
  - Store 전유/공용 면적 per (sigunguCd, bjdongCd, bun, ji, dongNm, hoNm) for about 30 days, since the source updates monthly.
  - Snapshot 조달청 prices per release, keep version tags in each estimate, and pull about 161 calls a year.
  - Fetch 공휴일 for the next 2 years at startup, with a weekly refresh to catch 임시공휴일.
  - These patterns keep usage far below the dev quotas noted earlier (건축HUB about 10,000/day; 조달청 dev 1,000).
- **Reliability:** neither data.go.kr nor the providers promise uptime, and providers disclaim outage liability. Use timeouts, retries with backoff, and last-good-cache fallback, and show a "데이터 기준일".
- **Key hygiene:** server-only keys in env/Secrets Manager. The juso.go.kr key is per system, so get separate keys for dev and prod domains.

### Gaps
- Traffic quotas for 건축HUB, 특일정보 and juso were not shown on the fetched pages. The numbers above are the team's earlier notes.
- juso.go.kr 승인키 validity (개발 vs 운영 period) and its terms could not be fetched (pages returned only a title or 404).
- data.go.kr key validity (commonly 2 years with extension) was not verified.

## 13. Web accessibility: is it mandatory for a private service of this size?

### Takeaway
Not legally mandatory for an unincorporated student team, as far as the sources show. The duty under 장애인차별금지법 제21조 and 시행령 제14조 was phased in to cover **all 법인** websites by 2013-04-11. It is enforced through 인권위 → 법무부 시정명령 → 과태료 up to 3천만원. It would apply once 믿집 is run by a corporation. Basic KWCAG conformance is recommended regardless.

### Cited Findings
- **Who is covered:** obligors under 제21조① and 시행령 제14조 include public bodies, education bodies, **법인**, cultural, medical and welfare actors, 사용자 (employers) and others. Enforcement runs 인권위 권고 → 법무부 시정명령 → 과태료 ≤3천만원, plus civil damages and criminal penalties for malicious discrimination. — [nepla wiki 장애인차별금지법](https://www.nepla.ai/wiki/it-정보-방송통신/기타/장애인차별금지법과-웹접근성-준수-의무-1509xg246nol)
- **Phase-in:** started 2009-04-11 with public bodies, 300+ employee workplaces and others, and expanded to all 법인 within 5 years. — [DT](https://www.dt.co.kr/article/10535254)
- **2013 deadline:** "국내 모든 법인 웹사이트" had to comply from 2013-04-11. The standard cited then was KWCAG 2.0. The government said it would not monitor every site; enforcement is complaint-driven. — [Gamemeca 2013-03](https://www.gamemeca.com/view.php?gid=268057)

### Inferences
- **Recommended minimum for 믿집:**
  - alt text on room photos and plans;
  - keyboard-operable quote flow;
  - visible focus;
  - contrast ≥4.5:1;
  - form labels and error text;
  - no color-only status (approve/reject badges);
  - captions for any video.
  - It is cheap and a good demo point.

### Gaps
- The current 시행령 별표 text was not read, and it is unknown whether 개인사업자 (not 법인) are covered.
- KWCAG 2.2 (commonly cited as KS X OT0003 rev. 2022, 4 원칙/14 지침/33 검사항목) could not be verified this session.

### Source index (all URLs consulted)
- Statute mirrors:
  - PIPA https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95
  - PIPA 시행령 https://www.nepla.ai/law/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9
  - 위치정보법 https://www.nepla.ai/law/%EC%9C%84%EC%B9%98%EC%A0%95%EB%B3%B4%EC%9D%98%20%EB%B3%B4%ED%98%B8%20%EB%B0%8F%20%EC%9D%B4%EC%9A%A9%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0
  - 전자상거래법 https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0
  - 전자상거래법 시행령 https://www.nepla.ai/law/%EC%A0%84%EC%9E%90%EC%83%81%EA%B1%B0%EB%9E%98%20%EB%93%B1%EC%97%90%EC%84%9C%EC%9D%98%20%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0%20%EC%8B%9C%ED%96%89%EB%A0%B9
  - 통신비밀보호법 https://www.nepla.ai/law/%ED%86%B5%EC%8B%A0%EB%B9%84%EB%B0%80%EB%B3%B4%ED%98%B8%EB%B2%95
  - 통신비밀보호법 시행령 https://www.nepla.ai/law/%ED%86%B5%EC%8B%A0%EB%B9%84%EB%B0%80%EB%B3%B4%ED%98%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9
  - 전기통신사업법 https://www.nepla.ai/law/%EC%A0%84%EA%B8%B0%ED%86%B5%EC%8B%A0%EC%82%AC%EC%97%85%EB%B2%95
  - 전기통신사업법 시행령 https://www.nepla.ai/law/%EC%A0%84%EA%B8%B0%ED%86%B5%EC%8B%A0%EC%82%AC%EC%97%85%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9
  - 정보통신망법 시행령 https://www.nepla.ai/law/%EC%A0%95%EB%B3%B4%ED%86%B5%EC%8B%A0%EB%A7%9D%20%EC%9D%B4%EC%9A%A9%EC%B4%89%EC%A7%84%20%EB%B0%8F%20%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EB%B2%95%EB%A5%A0%20%EC%8B%9C%ED%96%89%EB%A0%B9
  - 건설산업기본법 https://www.nepla.ai/law/%EA%B1%B4%EC%84%A4%EC%82%B0%EC%97%85%EA%B8%B0%EB%B3%B8%EB%B2%95
  - 건설산업기본법 시행령 https://www.nepla.ai/law/%EA%B1%B4%EC%84%A4%EC%82%B0%EC%97%85%EA%B8%B0%EB%B3%B8%EB%B2%95%20%EC%8B%9C%ED%96%89%EB%A0%B9
  - AI 기본법 https://www.nepla.ai/law/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%20%EB%B0%9C%EC%A0%84%EA%B3%BC%20%EC%8B%A0%EB%A2%B0%20%EA%B8%B0%EB%B0%98%20%EC%A1%B0%EC%84%B1%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EA%B8%B0%EB%B3%B8%EB%B2%95
  - https://korea.legal/wiki/개인정보-보호법-제26조/
  - https://korea.legal/wiki/개인정보-보호법-제21조/
  - https://korea.legal/wiki/%ea%b0%9c%ec%9d%b8%ec%a0%95%eb%b3%b4-%eb%b3%b4%ed%98%b8%eb%b2%95-%ec%a0%9c22%ec%a1%b0%ec%9d%982/
  - https://korea.legal/wiki/%ea%b0%9c%ec%9d%b8%ec%a0%95%eb%b3%b4-%eb%b3%b4%ed%98%b8%eb%b2%95-%ec%a0%9c15%ec%a1%b0/
  - https://korea.legal/wiki/%ed%86%b5%ec%8b%a0%ed%8c%90%eb%a7%a4%ec%a4%91%ea%b0%9c%ec%9e%90%ec%9d%98-%ec%b1%85%ec%9e%84/
  - https://itwiki.kr/w/개인정보의_안전성_확보조치_기준
  - https://itwiki.kr/w/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98_%EC%95%88%EC%A0%84%EC%84%B1_%ED%99%95%EB%B3%B4%EC%A1%B0%EC%B9%98_%EA%B8%B0%EC%A4%80_%EC%A0%9C4%EC%A1%B0
  - https://itwiki.kr/w/개인정보의_안전성_확보조치_기준_제5조
  - https://itwiki.kr/w/개인정보의_안전성_확보조치_기준_제7조
  - https://itwiki.kr/w/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98_%EC%95%88%EC%A0%84%EC%84%B1_%ED%99%95%EB%B3%B4%EC%A1%B0%EC%B9%98_%EA%B8%B0%EC%A4%80_%EC%A0%9C8%EC%A1%B0
  - https://itwiki.kr/w/가명정보
  - https://itwiki.kr/w/정보통신망법_제50조
  - https://itwiki.kr/w/정보통신망법_제23조의2
  - https://itwiki.kr/w/2023.3.14._%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%EB%B2%95_%EC%A0%84%EB%A9%B4%EA%B0%9C%EC%A0%95_%EC%8B%9C%EC%82%AC%EC%A0%90
  - https://itwiki.kr/w/ISMS-P_%EC%9D%B8%EC%A6%9D_%EB%8C%80%EC%83%81
  - https://ko.wikisource.org/wiki/%EC%9C%84%EC%B9%98%EC%A0%95%EB%B3%B4%EC%9D%98_%EB%B3%B4%ED%98%B8_%EB%B0%8F_%EC%9D%B4%EC%9A%A9_%EB%93%B1%EC%97%90_%EA%B4%80%ED%95%9C_%EB%B2%95%EB%A5%A0
  - https://ko.wikipedia.org/wiki/인공지능_발전과_신뢰_기반_조성_등에_관한_기본법
- Government and official sites:
  - https://pipc.go.kr/np/default/page.do?mCode=D060040000
  - https://www.data.go.kr/data/15081808/openapi.do
  - https://www.data.go.kr/catalog/15142860/openapi.json
  - https://www.data.go.kr/data/15134735/openapi.do
  - https://www.data.go.kr/data/15129415/openapi.do
  - https://www.data.go.kr/data/15012690/openapi.do
  - https://www.data.go.kr/data/15057017/openapi.do
  - https://www.data.go.kr/data/15061039/openapi.do
  - https://www.data.go.kr/data/15156198/fileData.do
  - https://www.data.go.kr/ugs/selectPortalPolicyView.do
  - https://www.mcst.go.kr/kor/s_open/kogl/koglType.jsp?pTab=01
  - https://www.kiscon.net/
  - https://www.kosca.or.kr/
- Vendors and cloud:
  - https://developers.openai.com/api/docs/guides/your-data
  - https://aws.amazon.com/compliance/data-privacy-faq/
  - https://aws.amazon.com/compliance/k-isms/
- Law-firm and legal commentary:
  - https://www.yulchon.com/ko/resources/publications/newsletter-view/45098/page.do
  - https://shinkim.com/kor/media/newsletter/3319
  - https://shinkim.com/kor/media/newsletter/2613
  - https://www.shinkim.com/kor/media/newsletter/1789?page=131
  - https://www.shinkim.com/eng/media/newsletter/2942
  - https://www.daeryunlaw.com/newsletter/news/151
  - https://www.lawtalk.co.kr/posts/164921
  - https://www.lawtalk.co.kr/posts/177280
  - https://www.lawtalk.co.kr/posts/115661
  - https://www.lawtimes.co.kr/news/articleView.html?idxno=228195
  - https://www.lawtimes.co.kr/news/166260
  - https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/계약에-근거하여-개인정보를-적법하게-수집-이용하는-방법-0o486ol18el5
  - https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/-일문일답-해외-클라우드-aws-등-에서-개인정보를-보관-처리할-때-정보주체의-동의를-받아야-하는가-54gnvzpe81pr
  - https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/개인정보의-국외이전-mo59y3rr81vj
  - https://www.nepla.ai/wiki/it-정보-방송통신/개인정보-위치정보-신용정보/망분리에서-위험기반-보호-로-2025년-개정-개인정보-안전성확보조치-고시의-의미-gy3807x469rx
  - https://www.nepla.ai/wiki/it-정보-방송통신/기타/장애인차별금지법과-웹접근성-준수-의무-1509xg246nol
  - https://www.nepla.ai/wiki/it-%EC%A0%95%EB%B3%B4-%EB%B0%A9%EC%86%A1%ED%86%B5%EC%8B%A0/%EC%9D%B8%ED%84%B0%EB%84%B7-%EB%B0%A9%EC%86%A1-%ED%86%B5%EC%8B%A0/%EC%A0%95%EB%B3%B4%ED%86%B5%EC%8B%A0%EB%A7%9D%EB%B2%95-%EC%83%81-%ED%94%8C%EB%9E%AB%ED%8F%BC-%EC%9A%B4%EC%98%81%EC%9E%90%EC%9D%98-%EA%B2%8C%EC%8B%9C%EA%B8%80-%EA%B4%80%EB%A6%AC-%EB%B0%A9%EB%B2%95-g6w93mqxnojp
- News:
  - https://www.newsis.com/view/NISX20260309_0003540588
  - https://mobile.newsis.com/view/NISX20260424_0003604909
  - https://byline.network/2025/10/31-281/
  - https://byline.network/2025/08/6-277/
  - https://byline.network/2025/11/20-518/
  - https://www.dt.co.kr/article/12009611?ref=naver
  - https://www.dt.co.kr/article/10535254
  - https://www.gamemeca.com/view.php?gid=268057
  - http://www.boannews.com/news/articleView.html?idxno=142460
  - https://m.boannews.com/html/detail.html?idx=128266
  - https://www.ajunews.com/view/20251202085042877
  - https://dealsite.co.kr/articles/137678
  - https://newsseoul.co.kr/news/view/1065589816318462
  - https://news.mtn.co.kr/news-detail/2026061711262527736
  - https://www.inews24.com/view/1514669
- Industry blogs and guides:
  - https://www.catchsecu.com/archives/11350
  - https://www.alchera.ai/resource/blog/business-registration-certificate-authentication-api
  - https://www.alchera.ai/resource/blog/isms-certification-mandatory-subject
  - https://www.tosspayments.com/blog/articles/sales-registration
  - https://www.help-me.kr/blog/article/ecommerce-brokerage-incorporation-guide/
  - https://kmong.com/support/expert-center/posts/671
  - https://1point.kr/blog/insights/ad-message
  - https://www.i-boss.co.kr/ab-74668-1685
  - https://www.spacek.co.kr/etc/privacy.do
  - https://www.cela.kr/ISMS_3_4
  - https://help.gnome.org/users/eog/stable/plugin-exif-digital.html.ko
- Fetch failed or empty (not cited for facts):
  - law.go.kr 제20조 page
  - korea.legal 제28조의8/제30조/제31조 (404)
  - openai.com DPA (403)
  - business.juso.go.kr (title only)
  - wikidocs 292158 (403)
  - help.bznav.com (403)
  - infuser.odcloud.kr swagger (404)
  - ko.wikipedia 웹_접근성 (no KWCAG info)
