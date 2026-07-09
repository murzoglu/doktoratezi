import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { EricClientError, fetchEricRecord, fullTextUrl, verifyFullTextUrl } from "../eric-client";
import { asToolContent, formatFullTextMarkdown, type FullTextResult } from "../format";
import type { Env } from "../types";
import { ericFullTextOutputShape, ericGetFullTextInputSchema, ericGetFullTextInputShape } from "./schemas";

export function registerEricGetFullTextTool(server: McpServer, env: Env): void {
  server.registerTool(
    "eric_get_full_text",
    {
      title: "Get ERIC full text PDF URL",
      description:
        "Resolve and optionally verify an ERIC-hosted full-text PDF URL. The Worker returns metadata and URL only; it does not parse PDF content.",
      inputSchema: ericGetFullTextInputShape,
      outputSchema: ericFullTextOutputShape,
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true
      }
    },
    async (input) => {
      const args = ericGetFullTextInputSchema.parse(input);
      const record = await fetchEricRecord(args.eric_id, env);
      if (!record) {
        throw new EricClientError(`ERIC record not found; verify the ERIC ID (EJ/ED prefix): ${args.eric_id}`);
      }

      if (!record.full_text_available) {
        const unavailable: FullTextResult = {
          available: false,
          url: null,
          content_type: null,
          eric_id: record.id,
          title: record.title,
          source: record.source,
          reason: "No ERIC-hosted full text; likely behind publisher paywall (typical for EJ records)."
        };
        return asToolContent(unavailable, "markdown", formatFullTextMarkdown(unavailable));
      }

      const url = fullTextUrl(record.id);
      const verification = args.verify ? await verifyFullTextUrl(url) : { ok: true, content_type: null };
      const result: FullTextResult = {
        available: verification.ok,
        url,
        content_type: verification.content_type,
        eric_id: record.id,
        title: record.title,
        source: record.source,
        ...(verification.ok
          ? {}
          : {
              reason: "ERIC marks this record as full text, but the PDF URL could not be verified as 200 application/pdf."
            })
      };

      return asToolContent(result, "markdown", formatFullTextMarkdown(result));
    }
  );
}
