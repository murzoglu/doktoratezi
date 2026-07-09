import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { EricClientError, fetchEricRecord } from "../eric-client";
import { asToolContent, formatRecordMarkdown } from "../format";
import type { Env } from "../types";
import { ericGetRecordInputSchema, ericGetRecordInputShape, ericRecordOutputShape } from "./schemas";

export function registerEricGetRecordTool(server: McpServer, env: Env): void {
  server.registerTool(
    "eric_get_record",
    {
      title: "Get ERIC record",
      description: "Retrieve full ERIC metadata for one EJ/ED record ID.",
      inputSchema: ericGetRecordInputShape,
      outputSchema: ericRecordOutputShape,
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true
      }
    },
    async (input) => {
      const args = ericGetRecordInputSchema.parse(input);
      const record = await fetchEricRecord(args.eric_id, env);
      if (!record) {
        throw new EricClientError(`ERIC record not found; verify the ERIC ID (EJ/ED prefix): ${args.eric_id}`);
      }

      return asToolContent(record, args.response_format, formatRecordMarkdown(record));
    }
  );
}
