import type { Env, EricApiDoc, EricApiResponse, EricRecord, EricSearchResult } from "./types";

const BASE_URL = "https://api.ies.ed.gov/eric/";
const FULL_TEXT_BASE = "https://files.eric.ed.gov/fulltext";
const REQUEST_TIMEOUT_MS = 20_000;
const MAX_ATTEMPTS = 2;

export const SEARCH_FIELDS = [
  "id",
  "title",
  "author",
  "source",
  "publicationdateyear",
  "description",
  "subject",
  "publicationtype",
  "peerreviewed",
  "e_fulltextauth"
].join(",");

export const FULL_RECORD_FIELDS = [
  SEARCH_FIELDS,
  "institution",
  "sponsor",
  "issn",
  "isbn",
  "audience",
  "language",
  "educationlevel",
  "e_yearadded",
  "url"
].join(",");

export class EricClientError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "EricClientError";
  }
}

export function fullTextUrl(ericId: string): string {
  return `${FULL_TEXT_BASE}/${ericId}.pdf`;
}

export function buildUserAgent(env?: Pick<Env, "ERIC_CONTACT_EMAIL">): string {
  const contact = env?.ERIC_CONTACT_EMAIL?.trim();
  return contact ? `eric-mcp/1.0 (mailto:${contact})` : "eric-mcp/1.0";
}

export async function ericRequest(
  params: Record<string, string | number>,
  env?: Pick<Env, "ERIC_CONTACT_EMAIL">
): Promise<EricApiResponse> {
  const url = new URL(BASE_URL);
  for (const [key, value] of Object.entries({ ...params, format: "json" })) {
    url.searchParams.set(key, String(value));
  }

  let lastError: unknown;
  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt += 1) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
      const response = await fetch(url.toString(), {
        method: "GET",
        headers: {
          Accept: "application/json",
          "User-Agent": buildUserAgent(env)
        },
        signal: controller.signal
      });
      clearTimeout(timeout);

      if (!response.ok) {
        if (response.status >= 400 && response.status < 500) {
          throw new EricClientError(
            `ERIC rejected the query (HTTP ${response.status}). Check Lucene syntax; for free-text use plain words and let the tool add filters.`
          );
        }

        if (attempt + 1 < MAX_ATTEMPTS) {
          await delay(350 * 2 ** attempt);
          continue;
        }

        throw new EricClientError("ERIC API is temporarily unavailable. Retry shortly or narrow the query.");
      }

      const data = (await response.json()) as EricApiResponse;
      if (!data.response || !Array.isArray(data.response.docs)) {
        throw new EricClientError("ERIC returned an unexpected response shape. Retry shortly or narrow the query.");
      }

      return data;
    } catch (error) {
      lastError = error;
      if (error instanceof EricClientError) {
        throw error;
      }

      if (attempt + 1 < MAX_ATTEMPTS) {
        await delay(350 * 2 ** attempt);
        continue;
      }
    }
  }

  if (lastError instanceof EricClientError) {
    throw lastError;
  }

  throw new EricClientError("ERIC API is temporarily unavailable. Retry shortly or narrow the query.");
}

export async function fetchEricSearch(
  params: {
    search: string;
    fields: string;
    rows: number;
    start: number;
  },
  env?: Pick<Env, "ERIC_CONTACT_EMAIL">
): Promise<EricSearchResult> {
  const data = await ericRequest(params, env);
  const total = Number(data.response?.numFound ?? 0);
  const offset = Number(data.response?.start ?? params.start);
  const docs = data.response?.docs ?? [];
  const items = docs.map(normalizeEricRecord);
  const count = items.length;
  const nextOffset = offset + count;

  return {
    total,
    count,
    offset,
    has_more: nextOffset < total,
    next_offset: nextOffset < total ? nextOffset : null,
    items
  };
}

export async function fetchEricRecord(
  ericId: string,
  env?: Pick<Env, "ERIC_CONTACT_EMAIL">
): Promise<EricRecord | null> {
  const result = await fetchEricSearch(
    {
      search: `id:${ericId}`,
      fields: FULL_RECORD_FIELDS,
      rows: 1,
      start: 0
    },
    env
  );

  return result.items[0] ?? null;
}

export async function verifyFullTextUrl(url: string): Promise<{ ok: boolean; content_type: string | null }> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch(url, { method: "HEAD", signal: controller.signal });
    const contentType = response.headers.get("content-type");
    return {
      ok: response.ok && contentType?.toLowerCase().includes("application/pdf") === true,
      content_type: contentType
    };
  } catch {
    return { ok: false, content_type: null };
  } finally {
    clearTimeout(timeout);
  }
}

export function normalizeEricRecord(doc: EricApiDoc): EricRecord {
  const id = String(doc.id ?? "");
  const fullTextAuth = toNumber(doc.e_fulltextauth) ?? 0;
  const fullTextAvailable = fullTextAuth === 1;

  return {
    id,
    title: String(doc.title ?? ""),
    author: toArray(doc.author),
    source: toNullableString(doc.source),
    publicationdateyear: toNumber(doc.publicationdateyear),
    description: toNullableString(doc.description),
    subject: toArray(doc.subject),
    publicationtype: toArray(doc.publicationtype),
    peerreviewed: toNullableString(doc.peerreviewed),
    peer_reviewed: doc.peerreviewed === "T",
    e_fulltextauth: fullTextAuth,
    full_text_available: fullTextAvailable,
    full_text_url: fullTextAvailable ? fullTextUrl(id) : null,
    institution: toArray(doc.institution),
    sponsor: toArray(doc.sponsor),
    issn: toArray(doc.issn),
    isbn: toArray(doc.isbn),
    audience: toArray(doc.audience),
    language: toArray(doc.language),
    educationlevel: toArray(doc.educationlevel),
    e_yearadded: toNumber(doc.e_yearadded),
    url: toArray(doc.url)
  };
}

function toArray(value: unknown): string[] {
  if (Array.isArray(value)) {
    return value.filter((item): item is string => typeof item === "string" && item.length > 0);
  }

  if (typeof value === "string" && value.length > 0) {
    return [value];
  }

  return [];
}

function toNumber(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }

  if (typeof value === "string" && value.trim() !== "") {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : null;
  }

  return null;
}

function toNullableString(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
