import { z } from "zod";

export const responseFormatSchema = z.enum(["json", "markdown"]).default("markdown");

// ER-9: bounds for year_from/year_to. ERIC's corpus starts well after 1900;
// 1900 is a deliberately generous floor (never rejects a real ERIC record)
// and (current year + 1) admits "in press" / forthcoming-year records
// without opening the door to an arbitrary year-far-future typo. Computed
// once at module load — this Worker is redeployed/reloaded far more often
// than once a year, so staleness within a deploy's lifetime isn't a concern.
const MIN_PUBLICATION_YEAR = 1900;
const MAX_PUBLICATION_YEAR = new Date().getFullYear() + 1;

// ER-9: ERIC's own API silently caps `start` well before 10000 for deep
// pagination; bounding offset here turns a would-be confusing upstream
// degradation into an explicit, documented tool-input limit instead.
const MAX_OFFSET = 10_000;

export const ericSearchInputShape = {
  query: z
    .string()
    .min(1)
    .describe(
      "Free-text search terms, e.g. 'executive function reading comprehension'. Lucene field syntax (title:..., subject:...) is also accepted and passed through."
    ),
  peer_reviewed_only: z
    .boolean()
    .default(false)
    .describe("If true, restrict to peer-reviewed records (adds peerreviewed:T)."),
  full_text_only: z
    .boolean()
    .default(false)
    .describe("If true, restrict to records with ERIC-hosted full text (adds e_fulltextauth:1)."),
  year_from: z
    .number()
    .int()
    .min(MIN_PUBLICATION_YEAR)
    .max(MAX_PUBLICATION_YEAR)
    .optional()
    .describe(`Earliest publication year (inclusive), ${MIN_PUBLICATION_YEAR}-${MAX_PUBLICATION_YEAR}.`),
  year_to: z
    .number()
    .int()
    .min(MIN_PUBLICATION_YEAR)
    .max(MAX_PUBLICATION_YEAR)
    .optional()
    .describe(`Latest publication year (inclusive), ${MIN_PUBLICATION_YEAR}-${MAX_PUBLICATION_YEAR}. Must be >= year_from.`),
  publication_type: z
    .string()
    .optional()
    .describe("Exact ERIC publication type, e.g. 'Journal Articles', 'Reports - Research', 'Dissertations/Theses'."),
  limit: z.number().int().min(1).max(200).default(20).describe("Max records (ERIC hard cap = 200)."),
  offset: z.number().int().min(0).max(MAX_OFFSET).default(0).describe(`Pagination offset (capped at ${MAX_OFFSET}).`),
  response_format: responseFormatSchema
};

export const ericSearchInputSchema = z.object(ericSearchInputShape);

export const ericIdSchema = z
  .string()
  .regex(/^E[JD]\d+$/, "Must be an ERIC ID like EJ1444884 or ED659153");

export const ericGetRecordInputShape = {
  eric_id: ericIdSchema,
  response_format: responseFormatSchema
};

export const ericGetRecordInputSchema = z.object(ericGetRecordInputShape);

export const ericGetFullTextInputShape = {
  eric_id: ericIdSchema,
  verify: z.boolean().default(true).describe("If true, HEAD-check the PDF URL returns 200 application/pdf.")
};

export const ericGetFullTextInputSchema = z.object(ericGetFullTextInputShape);

// ER-10: normalizeEricRecord (src/eric-client.ts) always returns these 9
// fields too (institution..url); the output schema previously under-declared
// them, which doesn't break anything today (the SDK's output validation
// strips unknown keys from its own parse result rather than rejecting them,
// and the handler's real structuredContent is sent unmodified regardless —
// see validateToolOutput in @modelcontextprotocol/sdk's server/mcp.js) but
// meant any client that builds its expectations from outputSchema alone
// (JSON-schema-driven tooling, codegen) would never know these fields exist.
export const ericRecordOutputShape = {
  id: z.string(),
  title: z.string(),
  author: z.array(z.string()),
  source: z.string().nullable(),
  publicationdateyear: z.number().nullable(),
  description: z.string().nullable(),
  subject: z.array(z.string()),
  publicationtype: z.array(z.string()),
  peerreviewed: z.string().nullable(),
  peer_reviewed: z.boolean(),
  e_fulltextauth: z.number(),
  full_text_available: z.boolean(),
  full_text_url: z.string().nullable(),
  institution: z.array(z.string()).optional(),
  sponsor: z.array(z.string()).optional(),
  issn: z.array(z.string()).optional(),
  isbn: z.array(z.string()).optional(),
  audience: z.array(z.string()).optional(),
  language: z.array(z.string()).optional(),
  educationlevel: z.array(z.string()).optional(),
  e_yearadded: z.number().nullable().optional(),
  url: z.array(z.string()).optional()
};

export const ericSearchOutputShape = {
  total: z.number(),
  count: z.number(),
  offset: z.number(),
  has_more: z.boolean(),
  next_offset: z.number().nullable(),
  items: z.array(z.object(ericRecordOutputShape))
};

export const ericFullTextOutputShape = {
  available: z.boolean(),
  url: z.string().nullable(),
  content_type: z.string().nullable(),
  eric_id: z.string(),
  title: z.string().nullable(),
  source: z.string().nullable(),
  reason: z.string().optional()
};
