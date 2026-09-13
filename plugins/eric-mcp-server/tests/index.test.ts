import { describe, expect, it, vi } from "vitest";

// @cloudflare/workers-oauth-provider imports `WorkerEntrypoint` from the
// workerd-only `cloudflare:workers` module, which does not exist under
// vitest's Node runtime. The library only uses it for an `instanceof` check
// on class-style handlers; this Worker passes plain `{ fetch }` objects, so an
// empty class is a faithful stand-in.
vi.mock("cloudflare:workers", () => ({ WorkerEntrypoint: class {} }));

const { default: worker } = await import("../src/index");

/** Minimal in-memory KVNamespace: just the get/put/delete/list surface the
 *  OAuth library touches on these paths. */
function fakeKv(seed: Record<string, unknown> = {}) {
  const store = new Map<string, string>(
    Object.entries(seed).map(([key, value]) => [key, JSON.stringify(value)])
  );
  return {
    async get(key: string, options?: { type?: string } | string) {
      const raw = store.get(key);
      if (raw === undefined) return null;
      const type = typeof options === "string" ? options : options?.type;
      return type === "json" ? JSON.parse(raw) : raw;
    },
    async put(key: string, value: string) {
      store.set(key, value);
    },
    async delete(key: string) {
      store.delete(key);
    },
    async list() {
      return { keys: [...store.keys()].map((name) => ({ name })), list_complete: true };
    }
  };
}

const ALLOWED_REDIRECT = "https://claude.ai/api/mcp/auth_callback";
const FOREIGN_REDIRECT = "https://evil.example/callback";

function makeEnv() {
  return {
    OAUTH_KV: fakeKv({
      // Both clients are validly REGISTERED for their redirect_uri, so the
      // library's own "registered URI" check passes and any 400 below comes
      // from this Worker's handleAuthorize gates, not from the library.
      "client:allowed-client": {
        clientId: "allowed-client",
        redirectUris: [ALLOWED_REDIRECT],
        tokenEndpointAuthMethod: "none"
      },
      "client:foreign-client": {
        clientId: "foreign-client",
        redirectUris: [FOREIGN_REDIRECT],
        tokenEndpointAuthMethod: "none"
      }
    }),
    OAUTH_ALLOWED_REDIRECT_ORIGINS: ""
  };
}

const ctx = { waitUntil() {}, passThroughOnException() {} } as unknown as ExecutionContext;

function call(request: Request) {
  // A fresh env per request: the library memoizes OAUTH_PROVIDER onto env.
  return worker.fetch(request, makeEnv() as never, ctx);
}

const INITIALIZE_BODY = JSON.stringify({
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "2025-06-18",
    capabilities: {},
    clientInfo: { name: "audit-probe", version: "0" }
  }
});

function mcpPost(path: string): Request {
  return new Request(`https://eric-mcp.example${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json, text/event-stream" },
    body: INITIALIZE_BODY
  });
}

function authorizeUrl(params: Record<string, string>): string {
  const url = new URL("https://eric-mcp.example/authorize");
  for (const [key, value] of Object.entries(params)) url.searchParams.set(key, value);
  return url.toString();
}

describe("ER-1 — no unauthenticated MCP on any path but the gated /mcp", () => {
  for (const path of ["/audit-probe", "/sse", "/foo/bar"]) {
    it(`POST ${path} with an MCP initialize body → 404, never an MCP response`, async () => {
      const response = await call(mcpPost(path));
      expect(response.status).toBe(404);
      const text = await response.text();
      expect(JSON.parse(text)).toEqual({ error: "not_found" });
      expect(text).not.toContain("jsonrpc");
      expect(text).not.toContain("serverInfo");
    });
  }

  it("the gated /mcp itself refuses the same body without a bearer token (401)", async () => {
    const response = await call(mcpPost("/mcp"));
    expect(response.status).toBe(401);
    expect(await response.text()).not.toContain("serverInfo");
  });
});

describe("CORS preflight through the default export", () => {
  it("OPTIONS /mcp from a foreign Origin → 204 with NO Access-Control-Allow-Origin", async () => {
    const response = await call(
      new Request("https://eric-mcp.example/mcp", {
        method: "OPTIONS",
        headers: { Origin: "https://evil.example", "Access-Control-Request-Method": "POST" }
      })
    );
    expect(response.status).toBe(204);
    expect(response.headers.has("Access-Control-Allow-Origin")).toBe(false);
  });

  it("control: OPTIONS /mcp from an allowlisted Origin echoes it", async () => {
    const response = await call(
      new Request("https://eric-mcp.example/mcp", {
        method: "OPTIONS",
        headers: { Origin: "https://claude.ai", "Access-Control-Request-Method": "POST" }
      })
    );
    expect(response.status).toBe(204);
    expect(response.headers.get("Access-Control-Allow-Origin")).toBe("https://claude.ai");
  });
});

describe("/authorize gates (redirect allowlist + S256-only PKCE)", () => {
  it("a registered but NOT allowlisted redirect_uri → 400", async () => {
    const response = await call(
      new Request(
        authorizeUrl({
          response_type: "code",
          client_id: "foreign-client",
          redirect_uri: FOREIGN_REDIRECT,
          code_challenge: "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",
          code_challenge_method: "S256"
        })
      )
    );
    expect(response.status).toBe(400);
    const body = (await response.json()) as { error: string; error_description: string };
    expect(body.error).toBe("invalid_request");
    expect(body.error_description).toBe("redirect_uri is not in the allowed origin list");
    expect(response.headers.get("Location")).toBeNull();
  });

  it("code_challenge_method=plain → 400", async () => {
    const response = await call(
      new Request(
        authorizeUrl({
          response_type: "code",
          client_id: "allowed-client",
          redirect_uri: ALLOWED_REDIRECT,
          code_challenge: "plain-verifier-value",
          code_challenge_method: "plain"
        })
      )
    );
    expect(response.status).toBe(400);
    const body = (await response.json()) as { error_description: string };
    expect(body.error_description).toBe("code_challenge_method must be S256");
  });

  it("no code_challenge at all (library would default to plain) → 400", async () => {
    const response = await call(
      new Request(
        authorizeUrl({
          response_type: "code",
          client_id: "allowed-client",
          redirect_uri: ALLOWED_REDIRECT
        })
      )
    );
    expect(response.status).toBe(400);
    const body = (await response.json()) as { error_description: string };
    expect(body.error_description).toBe("code_challenge_method must be S256");
  });

  it("control: allowlisted redirect_uri + S256 → 302 to that redirect_uri with a code", async () => {
    const response = await call(
      new Request(
        authorizeUrl({
          response_type: "code",
          client_id: "allowed-client",
          redirect_uri: ALLOWED_REDIRECT,
          state: "xyz",
          code_challenge: "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",
          code_challenge_method: "S256"
        })
      )
    );
    expect(response.status).toBe(302);
    const location = new URL(response.headers.get("Location") ?? "");
    expect(`${location.origin}${location.pathname}`).toBe(ALLOWED_REDIRECT);
    expect(location.searchParams.get("code")).toBeTruthy();
    expect(location.searchParams.get("state")).toBe("xyz");
  });
});
