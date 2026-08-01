#!/usr/bin/env python3
"""Atıf-bağlı sayısal iddiaları tam-metin/abstract üzerinden doğrular.

Her hedef için fulltext_cascade ile kaynak metni çeker (tam-metin → abstract),
tezdeki her sayıyı kaynak metinde arar (birebir + virgül/nokta + binlik-ayraç
normalize). Bulunamayan sayılar için Galileo claim_source_match semantik skoru.

Çıktı: JSON — her hedef için matched/missing sayılar + kaynak katmanı + semantik skor.
KVKK: yalnız yayınlanmış literatür metni gateway'e gider.
"""
import json, os, re, subprocess, sys, time

REPO = os.environ.get("CLAUDE_PROJECT_DIR", "/workspaces/T1DM-Tez")
sys.path.insert(0, os.path.join(REPO, "scripts", "eval"))
try:
    import galileo_bridge as G
    _CFG = G._load_cfg()
except Exception:
    G = None
    _CFG = None


sys.path.insert(0, os.path.join(REPO, "scripts", "mcp"))
import fulltext_cascade as FC


def cascade(doi, pmid, title=""):
    """PubMed/EPMC MCP'den TAM (kesilmemiş) tam-metin+abstract gövdesini çeker."""
    url, _ = FC.ENDPOINTS["pubmed"]
    try:
        m = FC.HttpMcp(url)
        m.open()
        srch = m.call("pubmed_europepmc_search", {"query": doi or title, "pageSize": 5})
        sbody = FC._text_of(srch)
        ids = FC._extract_ids(sbody, want_doi=doi, want_title=title)
        pmid2, pmcid = ids["pmid"] or pmid, ids["pmcid"]
        ft_args = {}
        if pmcid:
            ft_args["pmcids"] = [pmcid]
        elif pmid2:
            ft_args["pmids"] = [pmid2]
        elif doi:
            ft_args["dois"] = [doi]
        fbody = FC._text_of(m.call("pubmed_fetch_fulltext", ft_args)) if ft_args else ""
        abody = FC._text_of(m.call("pubmed_fetch_articles", {"pmids": [pmid2]})) if pmid2 else ""
    except Exception as e:
        return "", "error:%s" % str(e)[:80]
    ft_ok = bool(fbody) and not FC._is_error_body(fbody) and len(fbody) > 400
    ab_ok = bool(abody) and not FC._is_error_body(abody) and len(abody) > 200
    if ft_ok:
        return fbody + "\n" + (abody or ""), "fulltext"
    # PMC tam-metin yoksa Anna's read_article (DOI) fallback — kurumsal tam-metin
    if doi:
        try:
            au, aenv = FC.ENDPOINTS["annas"]
            am = FC.HttpMcp(au, os.environ.get(aenv, ""))
            am.open()
            at = FC._text_of(am.call("read_article", {"doi": doi, "max_chars": 40000}))
            # SciDB fuzzy-match veya 404 uyarılarını ele: DOI/başlık metinde geçmeli
            bad = ("does NOT contain this DOI" in at or "Not Found" in at[:80]
                   or "is registered" in at[:120])
            if at and len(at) > 1500 and not bad:
                return at + "\n" + (abody or ""), "annas-fulltext"
        except Exception:
            pass
    if ab_ok:
        return abody, "abstract"
    return "", "none"


def norm_variants(num):
    """Bir sayının kaynak metinde aranacak varyantları (TR virgül <-> EN nokta,
    binlik ayracı kaldır, % işaretini ayır)."""
    n = num.strip()
    n = re.sub(r"^%\s?", "", n)
    n = re.sub(r"[=<>≈]", "", n)
    n = re.sub(r"^(g|d|r|β|OR|HR|RR|Mz|M|SD|n)\s*", "", n, flags=re.I)
    n = n.strip().rstrip(",.")
    variants = set()
    core = n.replace("yüz binde", "").replace("binde", "").strip()
    for base in {core}:
        if not base:
            continue
        variants.add(base)
        dot = base.replace(",", ".")              # TR->EN ondalık
        variants.add(dot)
        variants.add(base.replace(".", ","))      # EN->TR
        variants.add(base.replace(".", ""))       # binlik ayracı kaldır (108300)
        variants.add(base.replace(".", "").replace(",", ""))
        # APA lider-sıfır düşürme: 0,28 -> .28 ; 0.28 -> .28
        if dot.startswith("0."):
            variants.add(dot[1:])                 # ".28"
        # ondalık ayracı çevresinde boşluk toleransı için ayrı desen yok;
        # find_num zaten esnek sınır kullanır
    return {v for v in variants if v and re.search(r"\d", v)}


def find_num(num, src):
    for v in norm_variants(num):
        # kelime-sınırına yakın ara (ondalık için sınır esnek)
        if re.search(r"(?<![\d])" + re.escape(v) + r"(?![\d])", src):
            return v
    return None


def main():
    targets = json.load(open("/tmp/verify_targets.json", encoding="utf-8"))
    results = []
    for i, t in enumerate(targets):
        src, layer = cascade(t.get("doi", ""), t.get("pmid", ""), t.get("key", ""))
        srcl = src.lower()
        matched, missing = [], []
        for num in t["numbers"]:
            hit = find_num(num, srcl)
            (matched if hit else missing).append(num)
        rec = {"key": t["key"], "layer": layer, "file": t["file"],
               "n_num": len(t["numbers"]), "matched": matched, "missing": missing,
               "src_len": len(src)}
        # eksikler için semantik skor (judge/embedding)
        if missing and src and G is not None:
            try:
                r = G.t_galileo_claim_source_match({"claim": t["sent"], "source_text": src[:6000]})
                rec["semantic_score"] = r.get("score")
                rec["semantic_mode"] = r.get("mode")
            except Exception as e:
                rec["semantic_score"] = None
                rec["semantic_err"] = str(e)[:80]
        results.append(rec)
        print("[%d/%d] %-30s layer=%-9s matched=%d/%d missing=%s" % (
            i + 1, len(targets), t["key"][:30], layer,
            len(matched), len(t["numbers"]), missing), file=sys.stderr)
        time.sleep(1.5)  # rate-limit nezaketi
    json.dump({"n": len(results), "results": results},
              open("/tmp/verify_results.json", "w"), ensure_ascii=False, indent=2)
    print(json.dumps({"n": len(results)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
