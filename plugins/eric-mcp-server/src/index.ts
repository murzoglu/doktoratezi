import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { WebStandardStreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js";
import { createEricMcpServer } from "./server";
import { registerEricTools } from "./tools";
import type { Env } from "./types";
import {
  applyCorsAndResourceMetadata,
  corsPreflightResponse,
  isRedirectUriAllowed,
  resolveOrigin
} from "./cors";

// Out of scope for this hardening pass (ER-1/ER-2/ER-4 router/CORS/PRM fix
// only): this Durable Object class, its MCP_OBJECT binding, and the v1 SQLite
// migration in wrangler.jsonc are dead (never routed — /mcp is served
// statelessly below) but are left exactly as they were.
export class EricMCP extends McpAgent<Env> {
  server = new McpServer({
    name: "eric-mcp-server",
    version: "1.0.0"
  });

  async init(): Promise<void> {
    registerEricTools(this.server, this.env);
  }
}

const statelessMcpHandler = {
  async fetch(request: Request, env: unknown): Promise<Response> {
    const server = createEricMcpServer(env as Env);
    const transport = new WebStandardStreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true
    });

    await server.connect(transport);
    try {
      return await transport.handleRequest(request);
    } finally {
      await server.close();
    }
  }
};

/** 200 JSON for "/" and "/health" — unchanged from before this hardening pass. */
function healthResponse(): Response {
  return Response.json({
    name: "eric-mcp-server",
    status: "ok",
    upstream: "https://api.ies.ed.gov/eric/",
    tools: ["eric_search", "eric_get_record", "eric_get_full_text"]
  });
}

/**
 * RFC 9728 OAuth Protected Resource metadata, served at both the bare
 * well-known path and ChatGPT's "/mcp" path-insertion variant — matching the
 * shape already live on this fleet's Python servers today.
 */
function protectedResourceMetadata(request: Request): Response {
  const origin = resolveOrigin(request);
  return Response.json({
    resource: `${origin}/mcp`,
    authorization_servers: [origin],
    bearer_methods_supported: ["header"],
    scopes_supported: ["eric.read"]
  });
}

async function handleAuthorize(request: Request, env: Env): Promise<Response> {
  let oauthRequest;
  try {
    oauthRequest = await env.OAUTH_PROVIDER.parseAuthRequest(request);
  } catch (error) {
    return Response.json(
      {
        error: "invalid_request",
        error_description: error instanceof Error ? error.message : "Invalid authorization request"
      },
      { status: 400 }
    );
  }

  // Independent of whatever redirect_uri a dynamically-registered client
  // claims for itself (RFC 7591 registration does not host-check it): this is
  // the fleet-wide allowlist gate that stops an arbitrary open redirect from
  // being used to steal an authorization code.
  if (!isRedirectUriAllowed(oauthRequest.redirectUri, env)) {
    return Response.json(
      { error: "invalid_request", error_description: "redirect_uri is not in the allowed origin list" },
      { status: 400 }
    );
  }

  const grantedScope = oauthRequest.scope.length > 0 ? oauthRequest.scope : ["eric.read"];
  const { redirectTo } = await env.OAUTH_PROVIDER.completeAuthorization({
    request: oauthRequest,
    userId: "eric-public-reader",
    metadata: {
      label: "ERIC MCP public read-only access"
    },
    scope: grantedScope,
    props: {
      userId: "eric-public-reader",
      server: "eric-mcp-server"
    }
  });

  return Response.redirect(redirectTo, 302);
}

/**
 * Every route NOT explicitly listed here is a 404. Before this hardening
 * pass, the final line of this handler was `return
 * statelessMcpHandler.fetch(request, typedEnv)`, which served the full MCP
 * protocol — tools/list, tools/call, real ERIC records — unauthenticated on
 * ANY path other than "/mcp" (the only path @cloudflare/workers-oauth-provider
 * actually gates, via apiHandlers below). "/mcp" is never reachable from this
 * handler: the library only calls it for requests that did not already match
 * one of its own special routes (apiHandlers, /token, /register, the AS
 * metadata endpoint).
 */
const defaultHandler = {
  async fetch(request: Request, env: unknown): Promise<Response> {
    const url = new URL(request.url);
    const typedEnv = env as Env;

    if (url.pathname === "/authorize") {
      return handleAuthorize(request, typedEnv);
    }

    if (url.pathname === "/" || url.pathname === "/health") {
      return healthResponse();
    }

    if (
      url.pathname === "/.well-known/oauth-protected-resource" ||
      url.pathname === "/.well-known/oauth-protected-resource/mcp"
    ) {
      return protectedResourceMetadata(request);
    }

    return Response.json({ error: "not_found" }, { status: 404 });
  }
};

const oauthProvider = new OAuthProvider({
  apiHandlers: {
    "/mcp": statelessMcpHandler
  },
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/token",
  clientRegistrationEndpoint: "/register",
  defaultHandler,
  scopesSupported: ["eric.read"],
  refreshTokenTTL: 2592000
});

/**
 * The library's own AS-metadata response hardcodes
 * code_challenge_methods_supported to ["plain", "S256"]; this narrows what is
 * ADVERTISED to ["S256"] only, per the brief. It does not change what the
 * library accepts at the token endpoint — enforcing S256-only PKCE end to end
 * is a separate, not-yet-scoped hardening step (out of scope here).
 */
async function restrictAdvertisedPkceMethods(response: Response): Promise<Response> {
  if (response.status !== 200) return response;
  let metadata: Record<string, unknown>;
  try {
    metadata = (await response.clone().json()) as Record<string, unknown>;
  } catch {
    return response;
  }
  metadata.code_challenge_methods_supported = ["S256"];
  const headers = new Headers(response.headers);
  headers.delete("Content-Length");
  headers.set("Content-Type", "application/json");
  return new Response(JSON.stringify(metadata), {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}

export default {
  async fetch(request: Request, env: unknown, ctx: ExecutionContext): Promise<Response> {
    const typedEnv = env as Env;

    // CORS preflight short-circuits before any routing or auth check, on
    // every path (not just "/mcp") — see cors.ts for the allowlist and the
    // loopback-any-port rule.
    if (request.method === "OPTIONS") {
      return corsPreflightResponse(request, typedEnv);
    }

    let response = await oauthProvider.fetch(request, env, ctx);

    const url = new URL(request.url);
    if (url.pathname === "/.well-known/oauth-authorization-server") {
      response = await restrictAdvertisedPkceMethods(response);
    }

    return applyCorsAndResourceMetadata(response, request, typedEnv);
  }
} satisfies ExportedHandler<Env>;
