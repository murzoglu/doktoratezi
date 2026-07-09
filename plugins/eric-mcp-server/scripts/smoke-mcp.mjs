const base = (process.argv[2] ?? "https://eric-mcp.cureonics.workers.dev").replace(/\/$/, "");
const redirectUri = "http://127.0.0.1:9999/callback";
const verifier = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-._~";

const challenge = Buffer.from(
  await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier))
).toString("base64url");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

async function registerClient() {
  const response = await fetch(`${base}/register`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      redirect_uris: [redirectUri],
      client_name: "eric-mcp-smoke",
      token_endpoint_auth_method: "none",
      grant_types: ["authorization_code", "refresh_token"],
      response_types: ["code"],
      scope: "eric.read"
    })
  });

  if (!response.ok) {
    throw new Error(`register failed ${response.status}: ${await response.text()}`);
  }
  return response.json();
}

async function getAuthorizationCode(clientId) {
  const url = new URL(`${base}/authorize`);
  for (const [key, value] of Object.entries({
    response_type: "code",
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: "eric.read",
    state: "smoke-state",
    code_challenge: challenge,
    code_challenge_method: "S256"
  })) {
    url.searchParams.set(key, value);
  }

  const response = await fetch(url, { redirect: "manual" });
  const location = response.headers.get("location");
  if (!location) {
    throw new Error(`authorize failed ${response.status}: ${await response.text()}`);
  }
  const code = new URL(location).searchParams.get("code");
  assert(code, `authorize redirect did not contain code: ${location}`);
  return code;
}

async function getToken(clientId, code) {
  const response = await fetch(`${base}/token`, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      redirect_uri: redirectUri,
      client_id: clientId,
      code_verifier: verifier
    })
  });

  if (!response.ok) {
    throw new Error(`token failed ${response.status}: ${await response.text()}`);
  }
  return response.json();
}

async function mcp(accessToken, body) {
  const response = await fetch(`${base}/mcp`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${accessToken}`,
      "content-type": "application/json",
      accept: "application/json, text/event-stream"
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    throw new Error(`mcp failed ${response.status}: ${await response.text()}`);
  }
  const payload = await response.json();
  if (payload.error) {
    throw new Error(`mcp error: ${JSON.stringify(payload.error)}`);
  }
  return payload;
}

async function callTool(accessToken, id, name, args) {
  const response = await mcp(accessToken, {
    jsonrpc: "2.0",
    id,
    method: "tools/call",
    params: { name, arguments: args }
  });
  return response.result.structuredContent;
}

const client = await registerClient();
const code = await getAuthorizationCode(client.client_id);
const token = await getToken(client.client_id, code);

const init = await mcp(token.access_token, {
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "2025-06-18",
    capabilities: {},
    clientInfo: { name: "eric-mcp-smoke", version: "1.0.0" }
  }
});
assert(init.result?.serverInfo?.name === "eric-mcp-server", "initialize did not return eric-mcp-server");

const tools = await mcp(token.access_token, { jsonrpc: "2.0", id: 2, method: "tools/list", params: {} });
const toolNames = tools.result?.tools?.map((tool) => tool.name).sort() ?? [];
assert(
  JSON.stringify(toolNames) === JSON.stringify(["eric_get_full_text", "eric_get_record", "eric_search"]),
  `unexpected tools: ${toolNames.join(", ")}`
);

const record = await callTool(token.access_token, 3, "eric_get_record", {
  eric_id: "EJ1444884",
  response_format: "json"
});
assert(record.source === "Scientific Studies of Reading", "EJ1444884 source mismatch");

const search = await callTool(token.access_token, 4, "eric_search", {
  query: "executive function",
  peer_reviewed_only: true,
  limit: 5,
  response_format: "json"
});
assert(search.total > 10000, "executive function peer-reviewed total should be > 10000");
assert(search.count === 5, "search should return 5 records");
assert(search.items.every((item) => item.peer_reviewed === true), "search returned non-peer-reviewed record");

const fullText = await callTool(token.access_token, 5, "eric_get_full_text", {
  eric_id: "ED659153",
  verify: true
});
assert(fullText.available === true, "ED659153 full text should be available");
assert(fullText.content_type?.includes("application/pdf"), "ED659153 content type should be application/pdf");

const noFullText = await callTool(token.access_token, 6, "eric_get_full_text", {
  eric_id: "EJ1444884",
  verify: true
});
assert(noFullText.available === false, "EJ1444884 should not have ERIC-hosted full text");

console.log(
  JSON.stringify(
    {
      base,
      server: init.result.serverInfo.name,
      tools: toolNames,
      record_source: record.source,
      search_total: search.total,
      full_text_available: fullText.available,
      no_full_text_available: noFullText.available
    },
    null,
    2
  )
);
