# eric-mcp-server

Remote MCP server over the [ERIC](https://eric.ed.gov/) (Education Resources
Information Center) education-literature database, running on Cloudflare
Workers. ERIC's own API (`api.ies.ed.gov/eric/`) is authless and public; this
server wraps it with MCP tools, OAuth 2.1 (for connector clients that require
it), CORS, caching, and input validation.

## Tools

| Tool | Purpose |
|---|---|
| `eric_search` | Free-text + structured-filter search (peer-reviewed, full-text-only, year range, publication type). |
| `eric_get_record` | Fetch one full ERIC record by ID (`EJ…` / `ED…`). |
| `eric_get_full_text` | Resolve (and optionally HEAD-verify) an ERIC-hosted full-text PDF URL. Does not extract PDF text itself. |

Each accepts `response_format: "markdown" | "json"` (default `markdown`)
except `eric_get_full_text`, which always renders markdown.

## Query syntax

`query` accepts plain free text (escaped before being sent upstream) or
explicit ERIC Lucene field syntax (`title:"...", subject:..., id:EJ...`) or a
range (`publicationdateyear:[2020 TO 2024]`), which is passed through
unescaped. A query is only treated as field syntax if it uses one of ERIC's
recognised field names (see `ERIC_QUERY_FIELDS` in `src/query.ts`) — an
ordinary colon in free text ("note: reading") or a bare `AND`/`OR`/`NOT` word
does not, on its own, switch the query into pass-through mode.

## Response shape and size bounds

- `content[0].text` carries the human/LLM-facing rendering (markdown, or a
  JSON mirror when `response_format: "json"`). Per-item abstracts are capped
  at 600 characters either way. For `eric_search`, if that cap alone still
  leaves the JSON mirror over a ~45 KB budget (a realistic outcome at
  `limit=200` with ERIC's longer abstracts), trailing items are additionally
  dropped from the text mirror — never from `structuredContent` — with an
  explicit `_text_mirror_truncated: { shown, total }` field stating what was
  cut. This keeps a worst-case `eric_search limit=200 response_format=json`
  call's `content[0].text` well under 50 KB.
- `structuredContent` always carries the full, uncapped result — it is the
  machine-readable surface for clients that read it directly rather than
  tokenizing `content[0].text`.

## Caching

Successful (2xx) upstream GETs to the ERIC search API are cached in
Cloudflare's `caches.default` for 1 hour, keyed on the full upstream request
URL (so distinct search/fields/rows/start combinations never collide). The
cache degrades silently if the Cache API is unavailable in the current
runtime — every request still succeeds via a live fetch, just without the
speed/load benefit.

## Rate limiting

`/mcp` is gated at 60 requests/minute/IP via a Workers [rate-limiting
binding](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)
(`MCP_RATE_LIMITER` in `wrangler.jsonc`), keyed on `CF-Connecting-IP`. A
zone-level Cloudflare WAF rate-limit rule was not used because
`eric-mcp.cureonics.workers.dev` is not in a customer zone — zone
`http_ratelimit` rules only apply inside a zone. The limiter degrades open
(never blocks traffic) if the binding is absent or its RPC call fails.

## Auth

OAuth 2.1 with PKCE (S256 only). Any client that completes the authorize flow
is granted read-only `eric.read` access — there is no user-specific gating,
since every ERIC record served here is already public. CORS and the
`redirect_uri` allowlist share one allowlist (`src/cors.ts`); the built-in
defaults cover `claude.ai`, `claude.com`, `grok.com`, `chatgpt.com`, Gemini
Spark, VS Code (including its random-port loopback fallback), and the Roche
corporate VS Code fork. `OAUTH_ALLOWED_REDIRECT_ORIGINS` (comma-separated)
**extends** that list, it never replaces it.

## Development

```bash
npm ci
npm run build      # tsc --noEmit
npm test           # vitest run (no network, no live Worker)
npm run dev         # wrangler dev
```

Tests are pure-function/unit level with `fetch` and `caches` stubbed — no
network access and no Worker runtime required. Covered: the query
pass-through/escaping heuristic (`src/query.ts`), ERIC client response
normalization and every error path (`src/eric-client.ts`), JSON/markdown
formatting and text-mirror size bounding (`src/format.ts`), and the CORS/
redirect_uri allowlist (`src/cors.ts`).

## Deploy

```bash
npm ci
npx wrangler deploy
```

Deployed from this repo (`doktoratezi`), independent of the `CureoHub` repo
that houses most of the Cureonics MCP fleet.

## History

- **1.2.0** (2026-09-12): removed the dead `EricMCP` Durable Object (never
  routed — `/mcp` has always been served by the stateless
  `WebStandardStreamableHTTPServerTransport`); added the vitest suite; fixed
  JSON response double-encoding/unbounded size; added the `caches.default`
  read-through cache; bounded `year_from`/`year_to`/`offset`; tightened the
  Lucene pass-through heuristic to require a recognised field name; added
  `items[0].id === ericId` verification and a `finally`-guarded
  `clearTimeout` to the ERIC client; added the `MCP_RATE_LIMITER` binding.
- **1.1.0** (2026-09-12): closed an unauthenticated catch-all route; added
  CORS allowlist + RFC 9728 Protected Resource Metadata; PKCE S256-only.
