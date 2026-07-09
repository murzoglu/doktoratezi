import { z } from "zod";

export const responseFormatSchema = z.enum(["json", "markdown"]).default("markdown");

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
  year_from: z.number().int().optional().describe("Earliest publication year (inclusive)."),
  year_to: z.number().int().optional().describe("Latest publication year (inclusive)."),
  publication_type: z
    .string()
    .optional()
    .describe("Exact ERIC publication type, e.g. 'Journal Articles', 'Reports - Research', 'Dissertations/Theses'."),
  limit: z.number().int().min(1).max(200).default(20).describe("Max records (ERIC hard cap = 200)."),
  offset: z.number().int().min(0).default(0).describe("Pagination offset."),
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
  full_text_url: z.string().nullable()
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
