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

// ER-7: same 600-char cap formatRecordSummary already applies to markdown.
const ABSTRACT_TEXT_CAP = 600;

// ER-7: content[0].text is what actually lands in an LLM's context window
// (the "bağlam ekonomisi" invariant); structuredContent is a separate
// machine-readable channel many hosts never tokenize. Capping content.text's
// byte size independently of structuredContent's fidelity is what makes
// `eric_search limit=200 response_format=json` bounded regardless of how
// long ERIC's real abstracts run (measured up to ~2.4k chars/record; with
// all 200 records' full metadata the plain per-item 600-char abstract cap
// alone is NOT enough to reach a reasonable budget — see report-O.md's
// measurement). 45 KB leaves headroom under the 50 KB validation target.
const JSON_TEXT_MIRROR_BUDGET_BYTES = 45_000;

function byteLength(value: string): number {
  return new TextEncoder().encode(value).length;
}

function truncate(text: string, maxLength: number): string {
  return text.length <= maxLength ? text : `${text.slice(0, maxLength - 1).trimEnd()}…`;
}

function capDescription(record: EricRecord): EricRecord {
  if (!record.description || record.description.length <= ABSTRACT_TEXT_CAP) {
    return record;
  }
  return { ...record, description: truncate(record.description, ABSTRACT_TEXT_CAP) };
}

function isSearchResult(data: unknown): data is EricSearchResult {
  return typeof data === "object" && data !== null && Array.isArray((data as EricSearchResult).items);
}

function hasDescriptionField(data: unknown): data is EricRecord {
  return typeof data === "object" && data !== null && "description" in data;
}

/**
 * Builds the bounded JSON text mirror for response_format="json". Per-item
 * abstracts are capped at ABSTRACT_TEXT_CAP, matching the markdown path. For
 * an EricSearchResult, if capping abstracts alone still leaves the mirror
 * over budget (a realistic outcome at limit=200 — see the module comment
 * above), trailing items are dropped from the TEXT MIRROR ONLY via binary
 * search for the largest item count that fits, with an explicit
 * `_text_mirror_truncated` note stating the true shown/total counts —
 * no-fabrication: the note says what was cut, it never silently hides rows.
 * structuredContent (built separately by the caller from the untouched
 * original `data`) always carries the full, uncapped result.
 */
function buildJsonTextMirror(data: unknown): string {
  if (isSearchResult(data)) {
    const cappedItems = data.items.map(capDescription);
    const fullText = JSON.stringify({ ...data, items: cappedItems });
    if (cappedItems.length === 0 || byteLength(fullText) <= JSON_TEXT_MIRROR_BUDGET_BYTES) {
      return fullText;
    }

    const renderWithCount = (count: number): string =>
      JSON.stringify({
        ...data,
        items: cappedItems.slice(0, count),
        _text_mirror_truncated: {
          shown: count,
          total: cappedItems.length,
          note: "content[0].text is capped for context economy; structuredContent carries the full result."
        }
      });

    let lo = 0;
    let hi = cappedItems.length;
    while (lo < hi) {
      const mid = Math.ceil((lo + hi) / 2);
      if (byteLength(renderWithCount(mid)) <= JSON_TEXT_MIRROR_BUDGET_BYTES) {
        lo = mid;
      } else {
        hi = mid - 1;
      }
    }

    return renderWithCount(lo);
  }

  if (hasDescriptionField(data)) {
    return JSON.stringify(capDescription(data));
  }

  return JSON.stringify(data);
}

export function asToolContent(data: unknown, responseFormat: ResponseFormat, markdown: string) {
  const text = responseFormat === "json" ? buildJsonTextMirror(data) : markdown;
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
    record.description ? `Abstract: ${truncate(record.description, ABSTRACT_TEXT_CAP)}` : "Abstract: Not available"
  ].join("\n");
}
