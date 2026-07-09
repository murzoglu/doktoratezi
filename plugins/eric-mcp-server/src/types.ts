import type { OAuthHelpers } from "@cloudflare/workers-oauth-provider";

export interface Env {
  MCP_OBJECT: DurableObjectNamespace;
  OAUTH_KV: KVNamespace;
  OAUTH_PROVIDER: OAuthHelpers;
  ERIC_CONTACT_EMAIL?: string;
}

export interface EricApiResponse {
  response?: {
    numFound?: number;
    start?: number;
    numFoundExact?: boolean;
    docs?: EricApiDoc[];
  };
}

export interface EricApiDoc {
  id?: string;
  title?: string;
  author?: string[] | string;
  source?: string;
  description?: string;
  subject?: string[] | string;
  publicationdateyear?: number | string;
  publicationtype?: string[] | string;
  peerreviewed?: string;
  e_fulltextauth?: number | string;
  institution?: string[] | string;
  sponsor?: string[] | string;
  issn?: string[] | string;
  isbn?: string[] | string;
  audience?: string[] | string;
  language?: string[] | string;
  educationlevel?: string[] | string;
  e_yearadded?: number | string;
  url?: string[] | string;
  [key: string]: unknown;
}

export interface EricRecord {
  id: string;
  title: string;
  author: string[];
  source: string | null;
  publicationdateyear: number | null;
  description: string | null;
  subject: string[];
  publicationtype: string[];
  peerreviewed: string | null;
  peer_reviewed: boolean;
  e_fulltextauth: number;
  full_text_available: boolean;
  full_text_url: string | null;
  institution?: string[];
  sponsor?: string[];
  issn?: string[];
  isbn?: string[];
  audience?: string[];
  language?: string[];
  educationlevel?: string[];
  e_yearadded?: number | null;
  url?: string[];
}

export interface Pagination {
  total: number;
  count: number;
  offset: number;
  has_more: boolean;
  next_offset: number | null;
}

export interface EricSearchResult extends Pagination {
  items: EricRecord[];
}
