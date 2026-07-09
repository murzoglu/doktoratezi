import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { buildEricSearchQuery } from "../query";
import { fetchEricSearch, SEARCH_FIELDS } from "../eric-client";
import { asToolContent, formatSearchMarkdown } from "../format";
import type { Env } from "../types";
import { ericSearchInputSchema, ericSearchInputShape, ericSearchOutputShape } from "./schemas";

export function registerEricSearchTool(server: McpServer, env: Env): void {
  server.registerTool(
    "eric_search",
    {
      title: "Search ERIC",
      description: "Search the ERIC education research database with free-text terms plus structured filters.",
      inputSchema: ericSearchInputShape,
      outputSchema: ericSearchOutputShape,
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true
      }
    },
    async (input) => {
      const args = ericSearchInputSchema.parse(input);
      const search = buildEricSearchQuery(args);
      const result = await fetchEricSearch(
        {
          search,
          fields: SEARCH_FIELDS,
          rows: args.limit,
          start: args.offset
        },
        env
      );

      return asToolContent(result, args.response_format, formatSearchMarkdown(result));
    }
  );
}
