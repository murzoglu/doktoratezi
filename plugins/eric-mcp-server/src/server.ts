import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { registerEricTools } from "./tools";
import type { Env } from "./types";

export function createEricMcpServer(env: Env): McpServer {
  const server = new McpServer({
    name: "eric-mcp-server",
    version: "1.0.0"
  });

  registerEricTools(server, env);
  return server;
}
