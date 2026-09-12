// ER-9: the previous FIELD_PATTERN (`/\b[a-z_][a-z0-9_]*\s*:/i`) matched ANY
// identifier-like word followed by a colon, so innocent free text containing
// a colon ("note: reading") was misdetected as Lucene field syntax and the
// WHOLE query skipped escaping (not just the colon — every other special
// character in the same string too). Requiring a recognised ERIC field name
// closes that: only a real field from the schema (src/types.ts's
// EricApiDoc) followed by ":" counts as field syntax.
export const ERIC_QUERY_FIELDS = [
  "id",
  "title",
  "author",
  "source",
  "description",
  "subject",
  "publicationdateyear",
  "publicationtype",
  "peerreviewed",
  "e_fulltextauth",
  "institution",
  "sponsor",
  "issn",
  "isbn",
  "audience",
  "language",
  "educationlevel",
  "e_yearadded",
  "url"
] as const;

const FIELD_PATTERN = new RegExp(`\\b(?:${ERIC_QUERY_FIELDS.join("|")})\\s*:`, "i");
const RANGE_PATTERN = /\[[^\]]+\s+TO\s+[^\]]+\]/i;
const LUCENE_SPECIAL = /([+\-!(){}[\]^"~*?:\\/])/g;

// ER-9: a bare boolean word (AND/OR/NOT) used to be enough on its own to
// treat the ENTIRE query as pre-formed Lucene syntax and skip escaping —
// but escaping never touches plain words like AND/OR/NOT anyway (only
// punctuation), so the only practical effect was to let any OTHER special
// character elsewhere in that same free-text string (a colon, a quote, a
// bracket) slip through unescaped too. A real field:value pair or an
// explicit range is what actually needs pass-through; a bare boolean word by
// itself no longer qualifies. (A deliberate Lucene range query such as
// "[2020 TO 2024]" still needs pass-through — escaping would turn its `[`/`]`
// into literal characters and break the user's intended range — so
// RANGE_PATTERN stays a standalone trigger.)
export function shouldPassThroughQuery(query: string): boolean {
  return FIELD_PATTERN.test(query) || RANGE_PATTERN.test(query);
}

export function escapeLuceneFreeText(query: string): string {
  return query.replace(/&&/g, "\\&&").replace(/\|\|/g, "\\||").replace(LUCENE_SPECIAL, "\\$1");
}

export function quoteLuceneValue(value: string): string {
  return `"${value.replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"`;
}

export interface BuildSearchOptions {
  query: string;
  peer_reviewed_only?: boolean;
  full_text_only?: boolean;
  year_from?: number;
  year_to?: number;
  publication_type?: string;
}

/**
 * Thrown for a request-shaped problem the schema's per-field bounds can't
 * catch on their own (year_from/year_to are each individually in range, but
 * inverted relative to each other). The MCP SDK's tool-call dispatcher turns
 * any thrown Error into a proper `isError: true` tool result carrying this
 * message — see node_modules/@modelcontextprotocol/sdk's
 * server/mcp.js `createToolError` — so this is a clear tool error, not a
 * silent `publicationdateyear:[2030 TO 1990]` that ERIC would just return
 * zero results for (ER-9).
 */
export class InvalidYearRangeError extends Error {
  constructor(yearFrom: number, yearTo: number) {
    super(`year_from (${yearFrom}) must be less than or equal to year_to (${yearTo}).`);
    this.name = "InvalidYearRangeError";
  }
}

export function buildEricSearchQuery(options: BuildSearchOptions): string {
  if (
    options.year_from !== undefined &&
    options.year_to !== undefined &&
    options.year_from > options.year_to
  ) {
    throw new InvalidYearRangeError(options.year_from, options.year_to);
  }

  const base = shouldPassThroughQuery(options.query)
    ? options.query.trim()
    : escapeLuceneFreeText(options.query.trim());

  const clauses = [base];

  if (options.peer_reviewed_only) {
    clauses.push("peerreviewed:T");
  }

  if (options.full_text_only) {
    clauses.push("e_fulltextauth:1");
  }

  if (options.year_from !== undefined || options.year_to !== undefined) {
    const from = options.year_from ?? "*";
    const to = options.year_to ?? "*";
    clauses.push(`publicationdateyear:[${from} TO ${to}]`);
  }

  if (options.publication_type) {
    clauses.push(`publicationtype:${quoteLuceneValue(options.publication_type)}`);
  }

  return clauses.join(" AND ");
}
