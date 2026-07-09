import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { WebStandardStreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js";
import { createEricMcpServer } from "./server";
import { registerEricTools } from "./tools";
import type { Env } from "./types";

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

export default new OAuthProvider({
  apiHandlers: {
    "/mcp": statelessMcpHandler
  },
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/token",
  clientRegistrationEndpoint: "/register",
  defaultHandler: {
    async fetch(request: Request, env: unknown, ctx: ExecutionContext): Promise<Response> {
      const url = new URL(request.url);
      const typedEnv = env as Env;

      if (url.pathname === "/authorize") {
        const oauthRequest = await typedEnv.OAUTH_PROVIDER.parseAuthRequest(request);
        const grantedScope = oauthRequest.scope.length > 0 ? oauthRequest.scope : ["eric.read"];
        const { redirectTo } = await typedEnv.OAUTH_PROVIDER.completeAuthorization({
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

      if (url.pathname === "/" || url.pathname === "/health") {
        return Response.json({
          name: "eric-mcp-server",
          status: "ok",
          upstream: "https://api.ies.ed.gov/eric/",
          tools: ["eric_search", "eric_get_record", "eric_get_full_text"]
        });
      }

      return statelessMcpHandler.fetch(request, typedEnv);
    }
  },
  scopesSupported: ["eric.read"],
  refreshTokenTTL: 2592000
});
