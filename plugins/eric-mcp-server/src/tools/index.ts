import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { Env } from "../types";
import { registerEricGetFullTextTool } from "./full-text";
import { registerEricGetRecordTool } from "./get-record";
import { registerEricSearchTool } from "./search";

export function registerEricTools(server: McpServer, env: Env): void {
  registerEricSearchTool(server, env);
  registerEricGetRecordTool(server, env);
  registerEricGetFullTextTool(server, env);
}
