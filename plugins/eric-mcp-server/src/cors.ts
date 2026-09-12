/**
 * CORS allowlist for eric-mcp's browser-reachable connector surface (/mcp,
 * the OAuth endpoints, RFC 9728 discovery) — and the same allowlist gates
 * `redirect_uri` at /authorize so an arbitrary open redirect can't be used to
 * steal an authorization code.
 *
 * Convention ported from the Cureonics Worker fleet's `OAUTH_ALLOWED_REDIRECT_ORIGINS`
 * pattern (see e.g. `mcp-servers/pexels-mcp/src/auth.ts` in the sibling CureoHub
 * repo): an exact-origin allowlist, overridable via a comma-separated env var,
 * plus a loopback-any-port carve-out for native MCP clients. VS Code registers
 * redirect port 33418 but falls back to a random free port when that one is
 * taken (microsoft/vscode#278512, closed as not planned) — an exact-origin
 * allowlist cannot cover that, so loopback redirects are accepted on any port
 * instead; this is safe because the code lands on the user's own machine and
 * the authorize step still requires passing the redirect_uri/PKCE checks.
 * The carve-out matches only the exact hostnames 127.0.0.1 / localhost / [::1],
 * so a lookalike such as `127.0.0.1.evil.example` is rejected.
 *
 * Unlike the fleet's custom single-tenant OAuth servers — which reflect any
 * Origin on /mcp because their gate is a bearer token, not a cookie — this
 * server's task brief requires denying unknown origins outright: a disallowed
 * Origin gets NO Access-Control-Allow-Origin header at all (never an echo,
 * never "*").
 */

export interface CorsEnv {
  OAUTH_ALLOWED_REDIRECT_ORIGINS?: string;
}

export const DEFAULT_ALLOWED_ORIGINS: readonly string[] = [
  "https://claude.ai",
  "https://claude.com",
  "https://grok.com",
  "https://chatgpt.com",
  "https://oauth-redirect.googleusercontent.com",
  "https://vscode.dev",
  "https://insiders.vscode.dev",
  "https://vscode.flexdev.roche.com"
];

function configuredAllowlist(env: CorsEnv): Set<string> {
  const configured = (env.OAUTH_ALLOWED_REDIRECT_ORIGINS ?? "")
    .split(",")
    .map((entry) => entry.trim())
    .filter((entry) => entry.length > 0);
  return new Set(configured.length > 0 ? configured : DEFAULT_ALLOWED_ORIGINS);
}

function isLoopbackHostname(hostname: string): boolean {
  // WHATWG URL keeps the brackets in `.hostname` for an IPv6 literal, so the
  // loopback form is "[::1]", never the bare "::1".
  return hostname === "127.0.0.1" || hostname === "localhost" || hostname === "[::1]";
}

/** True only for an exact loopback origin (any port) — never a lookalike host
 *  such as "127.0.0.1.evil.example" or "localhost.evil.example". */
function isLoopbackOrigin(value: string): boolean {
  try {
    return isLoopbackHostname(new URL(value).hostname);
  } catch {
    return false;
  }
}

export function isOriginAllowed(origin: string | null | undefined, env: CorsEnv): boolean {
  if (!origin) return false;
  if (isLoopbackOrigin(origin)) return true;
  try {
    return configuredAllowlist(env).has(new URL(origin).origin);
  } catch {
    return false;
  }
}

export function isRedirectUriAllowed(redirectUri: string, env: CorsEnv): boolean {
  try {
    return isOriginAllowed(new URL(redirectUri).origin, env);
  } catch {
    return false;
  }
}

/**
 * This worker's own origin as seen by the client, honouring X-Forwarded-Proto
 * (set by a proxy/tunnel in front of the Worker) over the request URL's own
 * scheme. Used to build the RFC 9728 resource_metadata URL without ever
 * hardcoding a hostname.
 */
export function resolveOrigin(request: Request): string {
  const url = new URL(request.url);
  const forwardedProto = request.headers.get("X-Forwarded-Proto");
  const protocol = forwardedProto?.split(",")[0]?.trim() || url.protocol.replace(":", "");
  return `${protocol}://${url.host}`;
}

const PREFLIGHT_ALLOW_METHODS = "GET, POST, OPTIONS";
const PREFLIGHT_ALLOW_HEADERS = "Authorization, Content-Type, Mcp-Session-Id, Mcp-Protocol-Version";
const EXPOSE_HEADERS = "WWW-Authenticate, Mcp-Session-Id";

/**
 * Answers a CORS preflight before any routing or auth. Per the brief, OPTIONS
 * must short-circuit with 204 ahead of the bearer gate on every path, not just
 * /mcp. A disallowed Origin gets 204 with no Access-Control-Allow-Origin
 * header (never an echo, never "*"), so the browser itself blocks the
 * follow-up request.
 */
export function corsPreflightResponse(request: Request, env: CorsEnv): Response {
  const origin = request.headers.get("Origin");
  const headers = new Headers({
    "Access-Control-Allow-Methods": PREFLIGHT_ALLOW_METHODS,
    "Access-Control-Allow-Headers": PREFLIGHT_ALLOW_HEADERS,
    "Access-Control-Expose-Headers": EXPOSE_HEADERS,
    "Access-Control-Max-Age": "86400"
  });
  if (origin) {
    headers.set("Vary", "Origin");
    if (isOriginAllowed(origin, env)) {
      headers.set("Access-Control-Allow-Origin", origin);
    }
  }
  return new Response(null, { status: 204, headers });
}

function appendVary(existing: string | null, name: string): string {
  if (!existing) return name;
  const parts = existing
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean);
  if (parts.some((part) => part.toLowerCase() === name.toLowerCase())) return existing;
  parts.push(name);
  return parts.join(", ");
}

/**
 * Finalizes any non-OPTIONS response before it leaves the Worker:
 *  - replaces whatever CORS headers @cloudflare/workers-oauth-provider added
 *    (it reflects any Origin unconditionally on /mcp, /token, /register and
 *    the AS-metadata endpoint — see its `addCorsHeaders`) with our own
 *    allowlist decision;
 *  - exposes WWW-Authenticate + Mcp-Session-Id so a browser client can read
 *    the RFC 9728 pointer off a 401 and the session id off a real response;
 *  - on a 401, appends resource_metadata to WWW-Authenticate when that header
 *    is present and doesn't already carry it. Never fabricates the header —
 *    a 401 without one (there currently is none) is left untouched.
 */
export function applyCorsAndResourceMetadata(response: Response, request: Request, env: CorsEnv): Response {
  const origin = request.headers.get("Origin");
  const headers = new Headers(response.headers);

  headers.delete("Access-Control-Allow-Origin");
  headers.delete("Access-Control-Allow-Methods");
  headers.delete("Access-Control-Allow-Headers");
  headers.delete("Access-Control-Max-Age");

  if (origin) {
    headers.set("Vary", appendVary(headers.get("Vary"), "Origin"));
    headers.set("Access-Control-Expose-Headers", EXPOSE_HEADERS);
    if (isOriginAllowed(origin, env)) {
      headers.set("Access-Control-Allow-Origin", origin);
    }
  }

  if (response.status === 401) {
    const existing = headers.get("WWW-Authenticate");
    if (existing && !existing.includes("resource_metadata=")) {
      const prmUrl = `${resolveOrigin(request)}/.well-known/oauth-protected-resource`;
      headers.set("WWW-Authenticate", `${existing}, resource_metadata="${prmUrl}"`);
    }
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}
