import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  buildUserAgent,
  EricClientError,
  ericRequest,
  fetchEricRecord,
  fetchEricSearch,
  fullTextUrl,
  normalizeEricRecord,
  verifyFullTextUrl
} from "../src/eric-client";
import type { EricApiDoc } from "../src/types";

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" }
  });
}

function docsResponse(docs: EricApiDoc[], numFound = docs.length): Response {
  return jsonResponse({ response: { numFound, start: 0, docs } });
}

describe("fullTextUrl / buildUserAgent", () => {
  it("builds the expected ERIC full-text PDF URL", () => {
    expect(fullTextUrl("EJ1444884")).toBe("https://files.eric.ed.gov/fulltext/EJ1444884.pdf");
  });

  it("omits the mailto clause when no contact email is configured", () => {
    expect(buildUserAgent({})).toBe("eric-mcp/1.0");
    expect(buildUserAgent({ ERIC_CONTACT_EMAIL: "" })).toBe("eric-mcp/1.0");
    expect(buildUserAgent(undefined)).toBe("eric-mcp/1.0");
  });

  it("includes a mailto clause when a contact email is configured", () => {
    expect(buildUserAgent({ ERIC_CONTACT_EMAIL: "ops@example.org" })).toBe(
      "eric-mcp/1.0 (mailto:ops@example.org)"
    );
  });
});

describe("normalizeEricRecord", () => {
  it("maps a full ERIC doc into the EricRecord shape, including e_fulltextauth=1", () => {
    const record = normalizeEricRecord({
      id: "ED659153",
      title: "Sample",
      author: ["A", "B"],
      source: "Region 18",
      description: "abstract",
      subject: ["x", "y"],
      publicationdateyear: "2023",
      publicationtype: "Reports - Research",
      peerreviewed: "F",
      e_fulltextauth: 1,
      institution: "Some Institution",
      e_yearadded: "2023"
    });
    expect(record.id).toBe("ED659153");
    expect(record.author).toEqual(["A", "B"]);
    expect(record.publicationdateyear).toBe(2023);
    expect(record.publicationtype).toEqual(["Reports - Research"]);
    expect(record.peer_reviewed).toBe(false);
    expect(record.full_text_available).toBe(true);
    expect(record.full_text_url).toBe("https://files.eric.ed.gov/fulltext/ED659153.pdf");
    expect(record.institution).toEqual(["Some Institution"]);
    expect(record.e_yearadded).toBe(2023);
  });

  it("defaults missing/absent fields to empty arrays, null, or 0 without throwing", () => {
    const record = normalizeEricRecord({});
    expect(record.id).toBe("");
    expect(record.title).toBe("");
    expect(record.author).toEqual([]);
    expect(record.source).toBeNull();
    expect(record.publicationdateyear).toBeNull();
    expect(record.description).toBeNull();
    expect(record.e_fulltextauth).toBe(0);
    expect(record.full_text_available).toBe(false);
    expect(record.full_text_url).toBeNull();
  });

  it("treats peerreviewed values other than exactly 'T' as not peer-reviewed", () => {
    expect(normalizeEricRecord({ peerreviewed: "T" }).peer_reviewed).toBe(true);
    expect(normalizeEricRecord({ peerreviewed: "F" }).peer_reviewed).toBe(false);
    expect(normalizeEricRecord({}).peer_reviewed).toBe(false);
  });

  it("filters out non-string entries from array-shaped fields", () => {
    const record = normalizeEricRecord({ author: ["Real Author", 42, null, ""] as unknown as string[] });
    expect(record.author).toEqual(["Real Author"]);
  });
});

describe("ericRequest — fetch-stubbed error paths (ER-10, no network)", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("throws EricClientError immediately on a 4xx without retrying", async () => {
    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    fetchMock.mockResolvedValue(jsonResponse({ error: "bad query" }, 400));

    await expect(ericRequest({ search: "bad:(", fields: "id", rows: 1, start: 0 })).rejects.toThrow(
      EricClientError
    );
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("retries once on a 5xx then throws EricClientError after exhausting attempts", async () => {
    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    fetchMock.mockResolvedValue(jsonResponse({ error: "down" }, 503));

    await expect(ericRequest({ search: "x", fields: "id", rows: 1, start: 0 })).rejects.toThrow(
      EricClientError
    );
    // MAX_ATTEMPTS = 2: one initial attempt + one retry.
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("treats a malformed (unparsable) JSON body as EricClientError", async () => {
    fetch as unknown as ReturnType<typeof vi.fn>;
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue(
      new Response("this is not json{", { status: 200, headers: { "Content-Type": "application/json" } })
    );

    await expect(ericRequest({ search: "x", fields: "id", rows: 1, start: 0 })).rejects.toThrow(
      EricClientError
    );
  });

  it("treats an unexpected-but-valid JSON shape (missing response.docs) as EricClientError", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue(jsonResponse({ unexpected: true }));

    await expect(ericRequest({ search: "x", fields: "id", rows: 1, start: 0 })).rejects.toThrow(
      EricClientError
    );
  });

  it("treats a fetch rejection (network error / aborted timeout) as a retryable failure, eventually surfacing EricClientError", async () => {
    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    // Simulates what a real AbortController-driven timeout looks like from
    // fetch's perspective (ER-10: clearTimeout must run on this path too —
    // proven by this test completing without an unhandled/dangling timer).
    fetchMock.mockRejectedValue(new DOMException("The operation was aborted.", "AbortError"));

    await expect(ericRequest({ search: "x", fields: "id", rows: 1, start: 0 })).rejects.toThrow(
      EricClientError
    );
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("returns a successful, well-shaped response without needing a retry", async () => {
    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    fetchMock.mockResolvedValue(docsResponse([{ id: "EJ1", title: "One" }], 1));

    const data = await ericRequest({ search: "one", fields: "id,title", rows: 1, start: 0 });
    expect(data.response?.docs?.[0]?.id).toBe("EJ1");
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});

describe("fetchEricSearch / fetchEricRecord", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("fetchEricSearch normalizes docs and computes pagination", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue(
      docsResponse([{ id: "EJ1" }, { id: "EJ2" }], 10)
    );
    const result = await fetchEricSearch({ search: "x", fields: "id", rows: 2, start: 0 });
    expect(result.total).toBe(10);
    expect(result.count).toBe(2);
    expect(result.has_more).toBe(true);
    expect(result.next_offset).toBe(2);
    expect(result.items.map((i) => i.id)).toEqual(["EJ1", "EJ2"]);
  });

  it("fetchEricRecord returns the record when the upstream id matches the request", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue(
      docsResponse([{ id: "EJ1444884", title: "Match" }], 1)
    );
    const record = await fetchEricRecord("EJ1444884");
    expect(record?.id).toBe("EJ1444884");
  });

  // ER-10: fetchEricRecord must not trust positional items[0] blindly.
  it("fetchEricRecord returns null (not the wrong record) when the upstream doc id does not match the request", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue(
      docsResponse([{ id: "ED999999", title: "Wrong record" }], 1)
    );
    const record = await fetchEricRecord("EJ1444884");
    expect(record).toBeNull();
  });

  it("fetchEricRecord returns null when ERIC has no matching doc at all", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue(docsResponse([], 0));
    const record = await fetchEricRecord("EJ0000000");
    expect(record).toBeNull();
  });
});

describe("verifyFullTextUrl", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("confirms a 200 application/pdf HEAD response", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue(
      new Response(null, { status: 200, headers: { "Content-Type": "application/pdf" } })
    );
    const result = await verifyFullTextUrl("https://files.eric.ed.gov/fulltext/ED1.pdf");
    expect(result.ok).toBe(true);
    expect(result.content_type).toBe("application/pdf");
  });

  it("rejects a non-PDF content type even on HTTP 200", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue(
      new Response(null, { status: 200, headers: { "Content-Type": "text/html" } })
    );
    const result = await verifyFullTextUrl("https://files.eric.ed.gov/fulltext/ED1.pdf");
    expect(result.ok).toBe(false);
  });

  it("degrades to ok:false on a network error instead of throwing", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockRejectedValue(new Error("network down"));
    const result = await verifyFullTextUrl("https://files.eric.ed.gov/fulltext/ED1.pdf");
    expect(result.ok).toBe(false);
    expect(result.content_type).toBeNull();
  });
});

describe("ER-8 read-through cache (caches.default)", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("degrades silently (no error, no behavior change) when the Cache API is unavailable — the default test environment", async () => {
    expect(typeof (globalThis as { caches?: unknown }).caches).toBe("undefined");
    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    // A fresh Response per call — a Response body can only be read once, so
    // reusing one instance across two real ericRequest() calls would make
    // the SECOND call's own .clone()/.json() fail for reasons that have
    // nothing to do with caching.
    fetchMock.mockImplementation(async () => docsResponse([{ id: "EJ1" }], 1));

    await ericRequest({ search: "same-query", fields: "id", rows: 1, start: 0 });
    await ericRequest({ search: "same-query", fields: "id", rows: 1, start: 0 });

    // No caches.default to serve a hit from, so both calls must reach
    // fetch — proving the absence of a cache never breaks or hangs a
    // request, it just always falls through to a live fetch.
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("serves a second identical request from the cache without calling fetch again, when caches.default IS available", async () => {
    const store = new Map<string, Response>();
    const fakeCache = {
      match: vi.fn(async (key: string) => {
        const hit = store.get(key);
        return hit ? hit.clone() : undefined;
      }),
      put: vi.fn(async (key: string, response: Response) => {
        store.set(key, response);
      })
    };
    vi.stubGlobal("caches", { default: fakeCache });

    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    fetchMock.mockResolvedValue(docsResponse([{ id: "EJ1" }], 1));

    const first = await ericRequest({ search: "cache-me", fields: "id", rows: 1, start: 0 });
    const second = await ericRequest({ search: "cache-me", fields: "id", rows: 1, start: 0 });

    expect(first.response?.docs?.[0]?.id).toBe("EJ1");
    expect(second.response?.docs?.[0]?.id).toBe("EJ1");
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fakeCache.put).toHaveBeenCalledTimes(1);
  });

  it("produces an identical fetchEricSearch result (full pipeline, not just the raw response) on a cache hit as on a live fetch", async () => {
    const store = new Map<string, Response>();
    const fakeCache = {
      match: vi.fn(async (key: string) => {
        const hit = store.get(key);
        return hit ? hit.clone() : undefined;
      }),
      put: vi.fn(async (key: string, response: Response) => {
        store.set(key, response);
      })
    };
    vi.stubGlobal("caches", { default: fakeCache });

    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    fetchMock.mockImplementation(async () =>
      docsResponse([{ id: "EJ1444884", title: "Stable Title", source: "Stable Source", peerreviewed: "T" }], 1)
    );

    const liveResult = await fetchEricSearch({ search: "id:EJ1444884", fields: "id,title,source", rows: 1, start: 0 });
    expect(fetchMock).toHaveBeenCalledTimes(1);

    const cachedResult = await fetchEricSearch({ search: "id:EJ1444884", fields: "id,title,source", rows: 1, start: 0 });
    // Still only ONE real fetch — the second call was served from the cache.
    expect(fetchMock).toHaveBeenCalledTimes(1);

    // Same observable tool output either way — the cache path must not
    // change what a caller sees.
    expect(cachedResult).toEqual(liveResult);
  });

  it("never caches a non-2xx response", async () => {
    const store = new Map<string, Response>();
    const fakeCache = {
      match: vi.fn(async (key: string) => {
        const hit = store.get(key);
        return hit ? hit.clone() : undefined;
      }),
      put: vi.fn(async (key: string, response: Response) => {
        store.set(key, response);
      })
    };
    vi.stubGlobal("caches", { default: fakeCache });

    const fetchMock = fetch as unknown as ReturnType<typeof vi.fn>;
    fetchMock.mockResolvedValue(jsonResponse({ error: "bad" }, 400));

    await expect(ericRequest({ search: "never-cached", fields: "id", rows: 1, start: 0 })).rejects.toThrow(
      EricClientError
    );
    expect(fakeCache.put).not.toHaveBeenCalled();
  });
});
