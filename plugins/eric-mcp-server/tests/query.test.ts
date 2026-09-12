import { describe, expect, it } from "vitest";
import {
  buildEricSearchQuery,
  escapeLuceneFreeText,
  InvalidYearRangeError,
  quoteLuceneValue,
  shouldPassThroughQuery
} from "../src/query";

describe("shouldPassThroughQuery", () => {
  it("passes through a real ERIC field:value query", () => {
    expect(shouldPassThroughQuery('title:"Bi/Multilingual Programs"')).toBe(true);
    expect(shouldPassThroughQuery("subject:Reading")).toBe(true);
    expect(shouldPassThroughQuery("peerreviewed:T")).toBe(true);
  });

  it("passes through an explicit Lucene range", () => {
    expect(shouldPassThroughQuery("publicationdateyear:[2020 TO 2024]")).toBe(true);
    expect(shouldPassThroughQuery("[2020 TO 2024]")).toBe(true);
  });

  // ER-9 regression: an ordinary colon in free text is not Lucene field
  // syntax just because *some* word precedes it — only a RECOGNISED ERIC
  // field name does.
  it("does NOT treat an ordinary colon in free text as field syntax", () => {
    expect(shouldPassThroughQuery("note: reading comprehension")).toBe(false);
    expect(shouldPassThroughQuery("time: 3pm meeting notes")).toBe(false);
  });

  // ER-9 regression: a bare capitalised AND/OR/NOT should no longer, on its
  // own, flip the whole query into "already Lucene-formatted" mode.
  it("does NOT treat a bare boolean word alone as field syntax", () => {
    expect(shouldPassThroughQuery("Will Smith NOT Jaden Smith")).toBe(false);
    expect(shouldPassThroughQuery("READING OR WRITING SKILLS")).toBe(false);
    expect(shouldPassThroughQuery("executive function AND reading")).toBe(false);
  });

  it("still passes through when a boolean word accompanies real field syntax", () => {
    expect(shouldPassThroughQuery("title:reading AND subject:writing")).toBe(true);
  });

  it("rejects a field-like token that is not in the recognised ERIC schema", () => {
    expect(shouldPassThroughQuery("randomfield:value")).toBe(false);
  });
});

describe("escapeLuceneFreeText", () => {
  it("escapes Lucene special characters", () => {
    expect(escapeLuceneFreeText("note: reading")).toBe("note\\: reading");
    expect(escapeLuceneFreeText("C++ programming")).toBe("C\\+\\+ programming");
    expect(escapeLuceneFreeText("(parenthetical)")).toBe("\\(parenthetical\\)");
  });

  it("escapes && and || as two-character tokens", () => {
    // The function's own && literal-substitution inserts a backslash that
    // LUCENE_SPECIAL's own pass then escapes again, so && becomes a DOUBLE
    // backslash — documenting the function's real (if unusual) output
    // rather than an idealized one.
    expect(escapeLuceneFreeText("cats && dogs")).toBe("cats \\\\&& dogs");
    expect(escapeLuceneFreeText("cats || dogs")).toBe("cats \\\\|| dogs");
  });

  it("leaves plain free text untouched", () => {
    expect(escapeLuceneFreeText("executive function reading")).toBe("executive function reading");
  });
});

describe("quoteLuceneValue", () => {
  it("wraps a value in quotes and escapes embedded quotes/backslashes", () => {
    expect(quoteLuceneValue("Journal Articles")).toBe('"Journal Articles"');
    expect(quoteLuceneValue('say "hi"')).toBe('"say \\"hi\\""');
    expect(quoteLuceneValue("back\\slash")).toBe('"back\\\\slash"');
  });
});

describe("buildEricSearchQuery", () => {
  it("escapes plain free text and joins filter clauses with AND", () => {
    const result = buildEricSearchQuery({
      query: "executive function",
      peer_reviewed_only: true,
      full_text_only: true,
      publication_type: "Journal Articles"
    });
    expect(result).toBe(
      'executive function AND peerreviewed:T AND e_fulltextauth:1 AND publicationtype:"Journal Articles"'
    );
  });

  it("passes through a real field query unescaped", () => {
    const result = buildEricSearchQuery({ query: 'title:"Bi/Multilingual Programs"' });
    expect(result).toBe('title:"Bi/Multilingual Programs"');
  });

  it("builds a publicationdateyear range clause from year_from/year_to", () => {
    const result = buildEricSearchQuery({ query: "reading", year_from: 2020, year_to: 2024 });
    expect(result).toContain("publicationdateyear:[2020 TO 2024]");
  });

  it("uses an open-ended range when only one bound is given", () => {
    expect(buildEricSearchQuery({ query: "reading", year_from: 2020 })).toContain(
      "publicationdateyear:[2020 TO *]"
    );
    expect(buildEricSearchQuery({ query: "reading", year_to: 2024 })).toContain(
      "publicationdateyear:[* TO 2024]"
    );
  });

  // ER-9: previously this silently built
  // `publicationdateyear:[2030 TO 1990]` — a well-formed but never-matching
  // Lucene range — and ERIC would just return 0 results with no indication
  // anything was wrong. Inverted bounds must now be a clear, catchable error
  // instead of a silent empty result.
  it("throws InvalidYearRangeError for inverted year bounds instead of silently building a backwards range", () => {
    expect(() => buildEricSearchQuery({ query: "reading", year_from: 2030, year_to: 1990 })).toThrow(
      InvalidYearRangeError
    );
    expect(() => buildEricSearchQuery({ query: "reading", year_from: 2030, year_to: 1990 })).toThrow(
      /year_from \(2030\) must be less than or equal to year_to \(1990\)/
    );
  });

  it("allows year_from === year_to (a single-year window)", () => {
    expect(buildEricSearchQuery({ query: "reading", year_from: 2020, year_to: 2020 })).toContain(
      "publicationdateyear:[2020 TO 2020]"
    );
  });
});
