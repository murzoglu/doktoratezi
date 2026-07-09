const FIELD_PATTERN = /\b[a-z_][a-z0-9_]*\s*:/i;
const BOOLEAN_PATTERN = /\b(AND|OR|NOT)\b/;
const RANGE_PATTERN = /\[[^\]]+\s+TO\s+[^\]]+\]/i;
const LUCENE_SPECIAL = /([+\-!(){}[\]^"~*?:\\/])/g;

export function shouldPassThroughQuery(query: string): boolean {
  return FIELD_PATTERN.test(query) || BOOLEAN_PATTERN.test(query) || RANGE_PATTERN.test(query);
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

export function buildEricSearchQuery(options: BuildSearchOptions): string {
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
