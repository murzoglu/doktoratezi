import type { EricRecord, EricSearchResult } from "./types";

export type ResponseFormat = "json" | "markdown";

export interface FullTextResult {
  available: boolean;
  url: string | null;
  content_type: string | null;
  eric_id: string;
  title: string | null;
  source: string | null;
  reason?: string;
}

export function asToolContent(data: unknown, responseFormat: ResponseFormat, markdown: string) {
  const text = responseFormat === "json" ? JSON.stringify(data, null, 2) : markdown;
  return {
    content: [{ type: "text" as const, text }],
    structuredContent: data as { [key: string]: unknown }
  };
}

export function formatSearchMarkdown(result: EricSearchResult): string {
  const lines = [
    `Total: ${result.total}`,
    `Count: ${result.count}`,
    `Offset: ${result.offset}`,
    `Has more: ${result.has_more ? "yes" : "no"}`,
    result.next_offset === null ? "Next offset: none" : `Next offset: ${result.next_offset}`,
    ""
  ];

  if (result.items.length === 0) {
    lines.push("_No ERIC records matched this query._");
    return lines.join("\n");
  }

  for (const record of result.items) {
    lines.push(formatRecordSummary(record), "");
  }

  return lines.join("\n").trimEnd();
}

export function formatRecordMarkdown(record: EricRecord): string {
  const lines = [
    `# ${record.title || record.id}`,
    "",
    `ID: ${record.id}`,
    `Authors: ${record.author.length ? record.author.join("; ") : "Unknown"}`,
    `Source: ${record.source ?? "Unknown"}${record.publicationdateyear ? ` (${record.publicationdateyear})` : ""}`,
    `Peer-reviewed: ${record.peer_reviewed ? "Yes" : "No"}`,
    `Full text: ${record.full_text_available && record.full_text_url ? `Yes - ${record.full_text_url}` : "No"}`,
    `Publication type: ${record.publicationtype.length ? record.publicationtype.join("; ") : "Unknown"}`,
    `Subjects: ${record.subject.length ? record.subject.join("; ") : "None listed"}`,
    ""
  ];

  if (record.description) {
    lines.push("## Abstract", record.description, "");
  }

  const optional = [
    ["Institution", record.institution],
    ["Sponsor", record.sponsor],
    ["ISSN", record.issn],
    ["ISBN", record.isbn],
    ["Audience", record.audience],
    ["Language", record.language],
    ["Education level", record.educationlevel],
    ["URL", record.url]
  ] as const;

  for (const [label, values] of optional) {
    if (values && values.length > 0) {
      lines.push(`${label}: ${values.join("; ")}`);
    }
  }

  if (record.e_yearadded !== null && record.e_yearadded !== undefined) {
    lines.push(`ERIC year added: ${record.e_yearadded}`);
  }

  return lines.join("\n").trimEnd();
}

export function formatFullTextMarkdown(result: FullTextResult): string {
  if (!result.available) {
    return [
      `# Full text unavailable for ${result.eric_id}`,
      "",
      `Title: ${result.title ?? "Unknown"}`,
      `Source: ${result.source ?? "Unknown"}`,
      `Reason: ${result.reason ?? "No ERIC-hosted full text."}`,
      "",
      "This tool resolves and verifies ERIC-hosted PDF URLs only; it does not parse PDF content inside the Worker."
    ].join("\n");
  }

  return [
    `# Full text available for ${result.eric_id}`,
    "",
    `Title: ${result.title ?? "Unknown"}`,
    `Source: ${result.source ?? "Unknown"}`,
    `URL: ${result.url}`,
    `Content type: ${result.content_type ?? "unknown"}`,
    "",
    "This tool returns a verified PDF URL. PDF text extraction should be handled downstream by a PDF reader, anamnesis, or another full-text pipeline."
  ].join("\n");
}

function formatRecordSummary(record: EricRecord): string {
  return [
    `### ${record.title || record.id}`,
    `Authors: ${record.author.length ? record.author.join("; ") : "Unknown"}`,
    `Source: ${record.source ?? "Unknown"}${record.publicationdateyear ? ` (${record.publicationdateyear})` : ""}`,
    `ID: ${record.id}`,
    `Peer-reviewed: ${record.peer_reviewed ? "Yes" : "No"}`,
    `Full text: ${record.full_text_available && record.full_text_url ? `Yes - ${record.full_text_url}` : "No"}`,
    record.description ? `Abstract: ${truncate(record.description, 600)}` : "Abstract: Not available"
  ].join("\n");
}

function truncate(text: string, maxLength: number): string {
  return text.length <= maxLength ? text : `${text.slice(0, maxLength - 1).trimEnd()}…`;
}
