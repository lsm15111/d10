# 구조도

| 파일 | 내용 | 상태 |
| --- | --- | --- |
| `system-config.svg` · `.png` | 시스템 구성도 · 완성 구성 예시 (AWS → EC2 → Docker Compose, RDS · S3 · SES, 배포 · 감시, 외부 API). 근거: [target-architecture.md](../design/target-architecture.md) | 현재 |
| `system-v3.2.svg` · `.png` | 전체 시스템 구조 (요구사항 v3.2, 배지 = 지금 상태) | 현재 |
| `ai-v3.2.svg` · `.png` | AI 구조 (첨부안 반영, [ai-architecture.md](../design/ai-architecture.md)) | 현재 |
| `code-flow.svg` · `.png` | 코드 흐름: 요청 하나가 지나가는 층 · 파일, 대표 흐름 4개 | 현재 |
| `target.svg` · `.png` | 리뷰 반영 목표 구조 (계약 · 채팅 · 후기 포함, v3.2 이전) | 지난 안 |
| `current.svg` | 초기 구조 | 지난 안 |

다시 만들기 (`src/`의 파이썬 스크립트, PNG는 headless Chrome으로 찍는다):

```bash
cd docs/architecture/src && python deploy.py ../system-config.svg && python system.py ../system-v3.2.svg && python ai.py ../ai-v3.2.svg && python code_flow.py ../code-flow.svg
```

화면설계서는 [docs/screens](../screens/README.md)에 있다.
