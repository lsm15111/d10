// 연결 확인 화면: 웹 → API → DB·Redis가 이어졌는지 보여 준다 (개발용).
export const dynamic = "force-dynamic";
export const metadata = { title: "연결 상태" };

type Ready = { env?: string; checks: Record<string, string> };

async function readyState(): Promise<Ready> {
  const base = process.env.API_INTERNAL_URL ?? "http://localhost:8000";
  try {
    const res = await fetch(`${base}/health/ready`, { cache: "no-store" });
    const body = (await res.json()) as { env?: string; checks?: Record<string, string> };
    return { env: body.env, checks: { api: "ok", ...body.checks } };
  } catch {
    return { checks: { api: "연결 안 됨" } };
  }
}

export default async function Status() {
  const ready = await readyState();
  return (
    <main id="main" className="mj-wrap mj-main" style={{ maxWidth: 480 }}>
      <h1 className="mj-h1">개발 환경 연결 상태</h1>
      <dl className="mj-kv">
        {Object.entries(ready.checks).map(([name, state]) => (
          <div key={name} style={{ display: "contents" }}>
            <dt>{name}</dt>
            <dd style={{ color: state === "ok" ? "var(--ok)" : "var(--danger)", fontWeight: 700 }}>{state}</dd>
          </div>
        ))}
      </dl>
      <p className="mj-small">환경: {ready.env ?? "알 수 없음"}</p>
    </main>
  );
}
