import { describe, expect, it } from "vitest";
import {
  applyCorsAndResourceMetadata,
  corsPreflightResponse,
  DEFAULT_ALLOWED_ORIGINS,
  isOriginAllowed,
  isRedirectUriAllowed,
  resolveOrigin
} from "../src/cors";
import type { CorsEnv } from "../src/cors";

const NO_OVERRIDE: CorsEnv = { OAUTH_ALLOWED_REDIRECT_ORIGINS: "" };

describe("isOriginAllowed — allowlist semantics", () => {
  it("allows every default origin", () => {
    for (const origin of DEFAULT_ALLOWED_ORIGINS) {
      expect(isOriginAllowed(origin, NO_OVERRIDE)).toBe(true);
    }
  });

  it("rejects an origin not on the list", () => {
    expect(isOriginAllowed("https://evil.example", NO_OVERRIDE)).toBe(false);
  });

  // Decision 3's named pin: a lookalike host must not piggyback on the
  // loopback carve-out.
  it("rejects a lookalike loopback host (127.0.0.1.evil.example)", () => {
    expect(isOriginAllowed("http://127.0.0.1.evil.example", NO_OVERRIDE)).toBe(false);
    expect(isOriginAllowed("http://localhost.evil.example", NO_OVERRIDE)).toBe(false);
  });

  it("accepts an exact loopback origin on ANY port (VS Code's random-port fallback)", () => {
    expect(isOriginAllowed("http://127.0.0.1:33418", NO_OVERRIDE)).toBe(true);
    expect(isOriginAllowed("http://127.0.0.1:54213", NO_OVERRIDE)).toBe(true);
    expect(isOriginAllowed("http://localhost:9999", NO_OVERRIDE)).toBe(true);
    expect(isOriginAllowed("http://[::1]:9999", NO_OVERRIDE)).toBe(true);
  });

  // Decision 3's named pin: Origin: null.
  it("rejects a null Origin", () => {
    expect(isOriginAllowed(null, NO_OVERRIDE)).toBe(false);
    expect(isOriginAllowed(undefined, NO_OVERRIDE)).toBe(false);
    expect(isOriginAllowed("null", NO_OVERRIDE)).toBe(false);
  });

  // Decision 3's named pin: a non-special scheme.
  it("rejects a non-special scheme even if the host part looks like an allowed one", () => {
    expect(isOriginAllowed("javascript:alert(1)", NO_OVERRIDE)).toBe(false);
    expect(isOriginAllowed("data:text/html,<script>", NO_OVERRIDE)).toBe(false);
    expect(isOriginAllowed("file:///etc/passwd", NO_OVERRIDE)).toBe(false);
  });

  it("rejects an unparsable origin string without throwing", () => {
    expect(isOriginAllowed("not a url at all", NO_OVERRIDE)).toBe(false);
    expect(isOriginAllowed("", NO_OVERRIDE)).toBe(false);
  });

  // Decision 3's named pin: an empty-string env override falls back to
  // defaults (never treated as "clear the allowlist").
  it("falls back to the built-in defaults when OAUTH_ALLOWED_REDIRECT_ORIGINS is an empty string", () => {
    expect(isOriginAllowed("https://claude.ai", { OAUTH_ALLOWED_REDIRECT_ORIGINS: "" })).toBe(true);
    expect(isOriginAllowed("https://claude.ai", {})).toBe(true);
  });

  // Decision 3's named pin: a non-empty override EXTENDS (never replaces)
  // the defaults — this is the exact ottoman-archives-style pitfall called
  // out in CureoHub's CLAUDE.md.
  it("unions a non-empty override with the defaults instead of replacing them", () => {
    const env: CorsEnv = { OAUTH_ALLOWED_REDIRECT_ORIGINS: "https://extra.example" };
    expect(isOriginAllowed("https://extra.example", env)).toBe(true);
    // Every built-in default must STILL be allowed — proving union, not
    // replacement.
    for (const origin of DEFAULT_ALLOWED_ORIGINS) {
      expect(isOriginAllowed(origin, env)).toBe(true);
    }
    expect(isOriginAllowed("https://still-not-allowed.example", env)).toBe(false);
  });

  it("supports multiple comma-separated extras, trimming whitespace", () => {
    const env: CorsEnv = { OAUTH_ALLOWED_REDIRECT_ORIGINS: " https://one.example , https://two.example" };
    expect(isOriginAllowed("https://one.example", env)).toBe(true);
    expect(isOriginAllowed("https://two.example", env)).toBe(true);
  });
});

describe("isRedirectUriAllowed", () => {
  it("checks the redirect_uri's origin against the same allowlist", () => {
    expect(isRedirectUriAllowed("https://claude.ai/callback?x=1", NO_OVERRIDE)).toBe(true);
    expect(isRedirectUriAllowed("https://evil.example/callback", NO_OVERRIDE)).toBe(false);
  });

  it("accepts a loopback redirect_uri on any port", () => {
    expect(isRedirectUriAllowed("http://127.0.0.1:33418/callback", NO_OVERRIDE)).toBe(true);
  });

  it("rejects an unparsable redirect_uri without throwing", () => {
    expect(isRedirectUriAllowed("not-a-uri", NO_OVERRIDE)).toBe(false);
  });
});

describe("resolveOrigin — X-Forwarded-Proto handling", () => {
  it("uses the request URL's own scheme when no X-Forwarded-Proto header is present", () => {
    const request = new Request("http://example.com/mcp");
    expect(resolveOrigin(request)).toBe("http://example.com");
  });

  it("honours X-Forwarded-Proto from a trusted proxy hop", () => {
    const request = new Request("http://example.com/mcp", {
      headers: { "X-Forwarded-Proto": "https" }
    });
    expect(resolveOrigin(request)).toBe("https://example.com");
  });

  it("reads the RIGHTMOST (nearest-hop) value in a comma-separated chain", () => {
    const request = new Request("http://example.com/mcp", {
      headers: { "X-Forwarded-Proto": "https, http" }
    });
    expect(resolveOrigin(request)).toBe("http://example.com");
  });

  it("ignores an invalid X-Forwarded-Proto value rather than trusting it", () => {
    const request = new Request("http://example.com/mcp", {
      headers: { "X-Forwarded-Proto": "javascript:alert(1)" }
    });
    expect(resolveOrigin(request)).toBe("http://example.com");
  });
});

describe("corsPreflightResponse", () => {
  it("returns 204 with no Access-Control-Allow-Origin for a disallowed Origin", () => {
    const request = new Request("https://eric-mcp.example/mcp", {
      method: "OPTIONS",
      headers: { Origin: "https://evil.example" }
    });
    const response = corsPreflightResponse(request, NO_OVERRIDE);
    expect(response.status).toBe(204);
    expect(response.headers.get("Access-Control-Allow-Origin")).toBeNull();
    expect(response.headers.get("Vary")).toBe("Origin");
  });

  it("echoes the exact allowed Origin back (never *) for an allowed Origin", () => {
    const request = new Request("https://eric-mcp.example/mcp", {
      method: "OPTIONS",
      headers: { Origin: "https://claude.ai" }
    });
    const response = corsPreflightResponse(request, NO_OVERRIDE);
    expect(response.headers.get("Access-Control-Allow-Origin")).toBe("https://claude.ai");
  });

  it("omits Vary: Origin entirely when no Origin header is present", () => {
    const request = new Request("https://eric-mcp.example/mcp", { method: "OPTIONS" });
    const response = corsPreflightResponse(request, NO_OVERRIDE);
    expect(response.headers.get("Vary")).toBeNull();
  });
});

describe("applyCorsAndResourceMetadata", () => {
  it("strips any CORS headers the inner handler set and substitutes the allowlist decision", () => {
    const inner = new Response("ok", {
      headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET" }
    });
    const request = new Request("https://eric-mcp.example/mcp", {
      headers: { Origin: "https://evil.example" }
    });
    const result = applyCorsAndResourceMetadata(inner, request, NO_OVERRIDE);
    expect(result.headers.get("Access-Control-Allow-Origin")).toBeNull();
  });

  it("appends resource_metadata to an existing WWW-Authenticate header on a 401", () => {
    const inner = new Response("unauthorized", {
      status: 401,
      headers: { "WWW-Authenticate": 'Bearer realm="eric-mcp"' }
    });
    const request = new Request("https://eric-mcp.example/mcp");
    const result = applyCorsAndResourceMetadata(inner, request, NO_OVERRIDE);
    const header = result.headers.get("WWW-Authenticate");
    expect(header).toContain('Bearer realm="eric-mcp"');
    expect(header).toContain("resource_metadata=");
    expect(header).toContain("/.well-known/oauth-protected-resource");
  });

  it("never fabricates a WWW-Authenticate header that was not already present", () => {
    const inner = new Response("unauthorized", { status: 401 });
    const request = new Request("https://eric-mcp.example/mcp");
    const result = applyCorsAndResourceMetadata(inner, request, NO_OVERRIDE);
    expect(result.headers.get("WWW-Authenticate")).toBeNull();
  });

  it("exposes WWW-Authenticate and Mcp-Session-Id when an Origin is present", () => {
    const inner = new Response("ok");
    const request = new Request("https://eric-mcp.example/mcp", {
      headers: { Origin: "https://claude.ai" }
    });
    const result = applyCorsAndResourceMetadata(inner, request, NO_OVERRIDE);
    expect(result.headers.get("Access-Control-Expose-Headers")).toContain("WWW-Authenticate");
    expect(result.headers.get("Access-Control-Expose-Headers")).toContain("Mcp-Session-Id");
  });
});
