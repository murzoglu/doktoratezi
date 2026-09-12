import type { Env, EricApiDoc, EricApiResponse, EricRecord, EricSearchResult } from "./types";

const BASE_URL = "https://api.ies.ed.gov/eric/";
const FULL_TEXT_BASE = "https://files.eric.ed.gov/fulltext";
const REQUEST_TIMEOUT_MS = 20_000;
const MAX_ATTEMPTS = 2;
// ER-8: ERIC's corpus is read-only from this Worker's perspective and the
// upstream has no visible rate-limit documentation of its own — a 1-hour
// read-through cache (the brief's figure) cuts upstream load for repeat
// queries (the same search/filters combination, or the same record id) with
// no correctness cost: a record added to ERIC an hour ago showing up an hour
// late is an acceptable staleness window for a bibliographic database that
// does not retract/correct entries on a sub-hourly cadence.
const CACHE_TTL_SECONDS = 60 * 60;

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

/**
 * ER-8 read-through cache around `caches.default` (the Workers edge cache),
 * keyed on the full upstream request URL (so distinct search/fields/rows/
 * start combinations never collide). Must degrade silently if the Cache API
 * isn't available in the current runtime (a local/test environment, or any
 * future Cloudflare runtime change) — every call here is wrapped so a
 * missing/erroring cache never breaks or even slows down a real request; it
 * just always falls through to a live upstream fetch.
 */
function defaultCache(): Cache | undefined {
  try {
    return typeof caches !== "undefined" ? caches.default : undefined;
  } catch {
    return undefined;
  }
}

async function readCachedEricResponse(url: string): Promise<EricApiResponse | null> {
  const cache = defaultCache();
  if (!cache) return null;
  try {
    const cached = await cache.match(url);
    if (!cached) return null;
    const data = (await cached.json()) as EricApiResponse;
    if (!data.response || !Array.isArray(data.response.docs)) return null;
    return data;
  } catch {
    return null;
  }
}

async function writeCachedEricResponse(url: string, response: Response): Promise<void> {
  const cache = defaultCache();
  if (!cache) return;
  try {
    const cacheable = new Response(response.body, response);
    cacheable.headers.set("Cache-Control", `public, max-age=${CACHE_TTL_SECONDS}`);
    await cache.put(url, cacheable);
  } catch {
    // Degrade silently — see defaultCache's doc comment.
  }
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
  const cacheKey = url.toString();

  const cached = await readCachedEricResponse(cacheKey);
  if (cached) {
    return cached;
  }

  let lastError: unknown;
  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt += 1) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
    // ER-10: clearTimeout must run on every exit from this attempt — the
    // success path, every error path, and every `continue` into the next
    // attempt — not just the success path. A nested try/finally (rather than
    // only the inner try/catch below) guarantees that regardless of which
    // branch returns, throws, or continues.
    try {
      try {
        const response = await fetch(cacheKey, {
          method: "GET",
          headers: {
            Accept: "application/json",
            "User-Agent": buildUserAgent(env)
          },
          signal: controller.signal
        });

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

        // ER-8: cache the raw response before consuming its body — .json()
        // below exhausts the stream, so the cached copy is taken from a
        // clone made while the body is still intact.
        await writeCachedEricResponse(cacheKey, response.clone());

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
    } finally {
      clearTimeout(timeout);
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

  const record = result.items[0];
  // ER-10: an `id:<ericId>` Lucene query is an exact-match field lookup in
  // principle, but asserting the returned doc's id rather than trusting
  // position [0] costs nothing and turns any future upstream relaxation
  // (fuzzy matching, a query-escaping regression letting ericId's value leak
  // into a broader query) into an honest "not found" instead of silently
  // handing back the wrong record under the id the caller asked for.
  if (!record || record.id !== ericId) {
    return null;
  }
  return record;
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
