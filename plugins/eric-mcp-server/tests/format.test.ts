import { describe, expect, it } from "vitest";
import { asToolContent, formatFullTextMarkdown, formatRecordMarkdown, formatSearchMarkdown } from "../src/format";
import type { EricRecord, EricSearchResult } from "../src/types";

function makeRecord(overrides: Partial<EricRecord> = {}): EricRecord {
  return {
    id: "EJ1000000",
    title: "A Sample Record",
    author: ["Doe, Jane"],
    source: "Journal of Testing",
    publicationdateyear: 2022,
    description: "A short abstract.",
    subject: ["Testing"],
    publicationtype: ["Journal Articles"],
    peerreviewed: "T",
    peer_reviewed: true,
    e_fulltextauth: 0,
    full_text_available: false,
    full_text_url: null,
    ...overrides
  };
}

function makeSearchResult(items: EricRecord[], total = items.length): EricSearchResult {
  return {
    total,
    count: items.length,
    offset: 0,
    has_more: items.length < total,
    next_offset: items.length < total ? items.length : null,
    items
  };
}

describe("asToolContent — markdown format", () => {
  it("uses the supplied markdown text verbatim and sets structuredContent to the raw data", () => {
    const record = makeRecord();
    const result = asToolContent(record, "markdown", formatRecordMarkdown(record));
    expect(result.content).toHaveLength(1);
    expect(result.content[0].type).toBe("text");
    expect(result.content[0].text).toBe(formatRecordMarkdown(record));
    expect(result.structuredContent).toBe(record);
  });
});

describe("asToolContent — json format, single record", () => {
  it("caps a long description at 600 chars in content[0].text but keeps structuredContent full", () => {
    const longDescription = "x".repeat(2000);
    const record = makeRecord({ description: longDescription });
    const result = asToolContent(record, "json", "unused-markdown");

    const parsedText = JSON.parse(result.content[0].text as string) as EricRecord;
    expect(parsedText.description?.length).toBeLessThanOrEqual(600);
    expect(parsedText.description?.endsWith("…")).toBe(true);

    // structuredContent (the machine-readable surface) is the original,
    // uncapped object — ER-7 explicitly keeps it full-fidelity.
    expect((result.structuredContent as unknown as EricRecord).description).toBe(longDescription);
  });

  it("leaves a short description untouched", () => {
    const record = makeRecord({ description: "short" });
    const result = asToolContent(record, "json", "unused-markdown");
    const parsedText = JSON.parse(result.content[0].text as string) as EricRecord;
    expect(parsedText.description).toBe("short");
  });
});

describe("asToolContent — json format, search result (ER-7 double-encoding fix)", () => {
  it("does not exceed the content[0].text size budget even at limit=200 with long abstracts", () => {
    // "Realistic" abstract length per a live measurement against
    // api.ies.ed.gov (avg ~900 chars, max ~2400 chars across a 200-record
    // sample fetched 2026-09-12) — see report-O.md for the raw numbers.
    const items = Array.from({ length: 200 }, (_, i) =>
      makeRecord({
        id: `EJ${1000000 + i}`,
        title: `Record number ${i} with a moderately descriptive title about executive function and reading comprehension`,
        author: ["Smith, John", "Doe, Jane"],
        subject: ["Reading Comprehension", "Executive Function", "Cognitive Development"],
        description: "Purpose: this synthetic abstract text repeats to simulate a realistic ERIC abstract length. ".repeat(12)
      })
    );
    const result = makeSearchResult(items, 59_445);
    const toolResult = asToolContent(result, "json", "unused-markdown");

    const text = toolResult.content[0].text as string;
    const textBytes = Buffer.byteLength(text, "utf8");
    expect(textBytes).toBeLessThanOrEqual(50 * 1024);

    // structuredContent must still carry every item, untouched — a
    // consumer reading structuredContent never loses data to this cap.
    expect((toolResult.structuredContent as unknown as EricSearchResult).items).toHaveLength(200);
  });

  it("is honest about a truncated text mirror via _text_mirror_truncated, never silently dropping rows", () => {
    const items = Array.from({ length: 200 }, (_, i) =>
      makeRecord({
        id: `EJ${2000000 + i}`,
        description: "Purpose: this synthetic abstract text repeats to simulate a realistic ERIC abstract length. ".repeat(12)
      })
    );
    const result = makeSearchResult(items, 59_445);
    const toolResult = asToolContent(result, "json", "unused-markdown");
    const parsed = JSON.parse(toolResult.content[0].text as string) as {
      items: EricRecord[];
      _text_mirror_truncated?: { shown: number; total: number };
    };

    expect(parsed._text_mirror_truncated).toBeDefined();
    expect(parsed._text_mirror_truncated?.total).toBe(200);
    expect(parsed.items.length).toBe(parsed._text_mirror_truncated?.shown);
    expect(parsed.items.length).toBeLessThan(200);
  });

  it("does not truncate a small result set (no budget pressure)", () => {
    const items = Array.from({ length: 5 }, (_, i) => makeRecord({ id: `EJ${3000000 + i}` }));
    const result = makeSearchResult(items, 5);
    const toolResult = asToolContent(result, "json", "unused-markdown");
    const parsed = JSON.parse(toolResult.content[0].text as string) as {
      items: EricRecord[];
      _text_mirror_truncated?: unknown;
    };
    expect(parsed.items).toHaveLength(5);
    expect(parsed._text_mirror_truncated).toBeUndefined();
  });

  it("caps each item's description independently of the array-level truncation", () => {
    const items = [makeRecord({ description: "y".repeat(5000) })];
    const result = makeSearchResult(items, 1);
    const toolResult = asToolContent(result, "json", "unused-markdown");
    const parsed = JSON.parse(toolResult.content[0].text as string) as { items: EricRecord[] };
    expect(parsed.items[0].description?.length).toBeLessThanOrEqual(600);
  });
});

describe("formatSearchMarkdown / formatRecordMarkdown (existing markdown truncation, unchanged)", () => {
  it("still caps abstracts at 600 chars for the markdown path", () => {
    const record = makeRecord({ description: "z".repeat(1000) });
    const markdown = formatSearchMarkdown(makeSearchResult([record], 1));
    const abstractLine = markdown.split("\n").find((line) => line.startsWith("Abstract:"));
    expect(abstractLine).toBeDefined();
    expect(abstractLine!.length).toBeLessThanOrEqual("Abstract: ".length + 600);
  });

  it("reports no matches without throwing", () => {
    const markdown = formatSearchMarkdown(makeSearchResult([], 0));
    expect(markdown).toContain("No ERIC records matched");
  });
});

describe("formatFullTextMarkdown", () => {
  it("renders the unavailable branch with a reason", () => {
    const markdown = formatFullTextMarkdown({
      available: false,
      url: null,
      content_type: null,
      eric_id: "EJ1",
      title: "Title",
      source: "Source",
      reason: "No ERIC-hosted full text."
    });
    expect(markdown).toContain("Full text unavailable for EJ1");
    expect(markdown).toContain("No ERIC-hosted full text.");
  });
});
