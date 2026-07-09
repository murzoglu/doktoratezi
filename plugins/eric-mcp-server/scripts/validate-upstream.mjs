const BASE_URL = "https://api.ies.ed.gov/eric/";

async function eric(params) {
  const url = new URL(BASE_URL);
  for (const [key, value] of Object.entries({ ...params, format: "json" })) {
    url.searchParams.set(key, String(value));
  }
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`ERIC HTTP ${response.status}`);
  }
  return response.json();
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const ej = await eric({
  search: "id:EJ1444884",
  fields: "id,title,source,peerreviewed,e_fulltextauth",
  rows: 1
});
assert(ej.response.docs[0].source === "Scientific Studies of Reading", "EJ1444884 source mismatch");

const ed = await eric({
  search: "id:ED659153",
  fields: "id,title,source,peerreviewed,e_fulltextauth",
  rows: 1
});
assert(ed.response.docs[0].e_fulltextauth === 1, "ED659153 should have ERIC-hosted full text");

const pdf = await fetch("https://files.eric.ed.gov/fulltext/ED659153.pdf", { method: "HEAD" });
assert(pdf.ok, "ED659153 PDF HEAD failed");
assert(pdf.headers.get("content-type")?.includes("application/pdf"), "ED659153 PDF is not application/pdf");

const executive = await eric({
  search: "(executive function) AND peerreviewed:T",
  fields: "id,title,source,publicationdateyear,peerreviewed,e_fulltextauth",
  rows: 1
});
assert(executive.response.numFound > 10000, "executive function peer-reviewed total should be >10000");

const title = await eric({
  search: 'title:"Bi/Multilingual Programs"',
  fields: "id,title,source,publicationdateyear,peerreviewed,e_fulltextauth",
  rows: 1
});
assert(title.response.docs[0].id === "ED659153", "title lookup should return ED659153");

console.log("ERIC upstream validation passed");
