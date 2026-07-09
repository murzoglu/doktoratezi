import tempfile
import unittest
from pathlib import Path

from dm_niteliksel_toolkit.common import is_protected_path
from dm_niteliksel_toolkit.tool_bridge import build_bridge_context, route_query


class ToolBridgeTests(unittest.TestCase):
    def test_bridge_context_links_dmnitel_evidentia_and_t1dm(self):
        context = build_bridge_context()

        self.assertIn("./dmnitel route-tool", context)
        self.assertIn("annas-reader", context)
        self.assertIn("Anamnesis/context gate", context)
        self.assertIn("Anna's Library full-text gate", context)
        self.assertIn("medical-research", context)
        self.assertIn("no-web-tier", context)
        self.assertIn("PsyArXiv/OSF", context)
        self.assertIn("sci-audit@cureonics-marketplace", context)
        self.assertIn("/sci-audit:check-turkish", context)
        self.assertIn("Kapı 4", context)
        self.assertIn("Kapı 5", context)
        self.assertIn("Task-Gated MCP Layers", context)
        self.assertIn("clinical_terminology_regulatory", context)
        self.assertIn("turkish_legislation", context)
        self.assertIn("life-science-research:research-router-skill", context)
        self.assertIn("zotero:Zotero", context)
        self.assertIn("/mnt/thunderbolt/workspaces/doktoratezi", context)
        self.assertIn("tez-yazim/README.md", context)

    def test_thesis_writing_query_routes_to_official_guide(self):
        route = route_query("Marmara tez yazım formatı ve özet şablonu")

        self.assertIn("Anamnesis context management gate", route.gate_order)
        self.assertIn("Marmara official thesis guide gate", route.gate_order)
        self.assertEqual(route.paired_repo, "/mnt/thunderbolt/workspaces/doktoratezi")
        self.assertTrue(any("ana merkez" in action for action in route.recommended_actions))
        self.assertTrue(any("kanonik nitel sonuç raporu" in action for action in route.recommended_actions))
        self.assertFalse(any("cross-repo-status" in command for command in route.dmnitel_commands))

    def test_literature_query_routes_to_evidentia(self):
        route = route_query("RTA bilgi gücü için PubMed ve tam metin kaynak taraması")

        self.assertIn("Evidentia external evidence gate", route.gate_order)
        self.assertIn("Anna's Library full-text gate", route.gate_order)
        self.assertIn("dual AI-reliability gate", route.gate_order)
        self.assertIn("annas-reader", route.mcp_servers)
        self.assertIn("evidentia:medical-research", route.plugin_layers)
        self.assertTrue(any("Native-first" in action for action in route.recommended_actions))
        self.assertTrue(any("retrieve-don't-dump" in action for action in route.recommended_actions))

    def test_quantitative_query_routes_to_paired_repo(self):
        route = route_query("H5 EMBU Beck KIA targets pipeline joint display")

        self.assertIn("paired doktoratezi + t1dm-tez-rehberi", route.gate_order)
        self.assertEqual(route.paired_repo, "/mnt/thunderbolt/workspaces/doktoratezi")

    def test_biomedical_query_routes_to_life_science_plugin(self):
        route = route_query("HLA genetik mekanizma ve beta cell pathway")

        self.assertIn("life-science-research plugin gate", route.gate_order)
        self.assertIn("life-science-research:research-router-skill", route.plugin_layers)
        self.assertIn("biocontext_kb", route.mcp_servers)
        self.assertIn("meta-analysis-skills", route.mcp_servers)

    def test_general_thesis_query_does_not_route_to_gene_tools(self):
        route = route_query("tez yazım giriş genel bilgiler Evidentia kanonik nitel sonuç raporu")

        self.assertNotIn("life-science-research plugin gate", route.gate_order)
        self.assertNotIn("life-science-research:research-router-skill", route.plugin_layers)
        self.assertIn("Evidentia external evidence gate", route.gate_order)
        self.assertIn("Anna's Library full-text gate", route.gate_order)
        self.assertIn("evidentia:medical-research", route.plugin_layers)
        self.assertTrue(any("cross-repo-status" in command for command in route.dmnitel_commands))

    def test_psyarxiv_osf_routes_with_blocked_endpoint_warning(self):
        route = route_query("PsyArXiv OSF preregistration preprint taraması")

        self.assertIn("Evidentia external evidence gate", route.gate_order)
        self.assertIn("psyarxiv-osf", route.mcp_servers)
        self.assertTrue(any("404 bloklu" in warning for warning in route.warnings))

    def test_sci_audit_query_routes_to_plugin_and_tez_yazim_rules(self):
        route = route_query("sci-audit ile Türkçe bilimsel yazım ve bölüm sertifikasyon denetimi")

        self.assertIn("sci-audit manuscript audit gate", route.gate_order)
        self.assertIn("dual AI-reliability gate", route.gate_order)
        self.assertIn("sci-audit@cureonics-marketplace", route.plugin_layers)
        self.assertTrue(any("/sci-audit:check-turkish" in action for action in route.recommended_actions))
        self.assertTrue(any("/sci-audit:audit" in action for action in route.recommended_actions))
        self.assertTrue(any("tez-yazim" in action for action in route.recommended_actions))
        self.assertTrue(any("repo/veri invaryantı" in warning for warning in route.warnings))

    def test_turkish_academic_query_routes_to_yok_and_eric_layers(self):
        route = route_query("YÖK tez merkezi ve eğitim akademik literatür taraması")

        self.assertIn("Turkish thesis and academic MCP gate", route.gate_order)
        self.assertIn("yoktez-mcp", route.mcp_servers)
        self.assertIn("yok-akademik", route.mcp_servers)
        self.assertIn("eric-mcp", route.mcp_servers)

    def test_legislation_query_routes_to_turkish_legislation_mcps(self):
        route = route_query("KVKK etik kurul yönetmelik ve sağlık mevzuatı kontrolü")

        self.assertIn("Turkish legislation MCP gate", route.gate_order)
        self.assertIn("mevzuat", route.mcp_servers)
        self.assertIn("mevzuat-bilgisi", route.mcp_servers)

    def test_clinical_terminology_query_routes_to_regulatory_mcps(self):
        route = route_query("TITCK ATC RxNorm ICD SNOMED ilaç terminoloji doğrulaması")

        self.assertIn("clinical terminology and regulatory MCP gate", route.gate_order)
        self.assertIn("titck-cache", route.mcp_servers)
        self.assertIn("nlm-rxnorm", route.mcp_servers)
        self.assertIn("med-terminologies", route.mcp_servers)
        self.assertIn("openfda", route.mcp_servers)

    def test_context_query_routes_to_memory_qdrant_and_sequentialthinking(self):
        route = route_query("Anamnesis bağlam hafıza qdrant karar geçmişi")

        self.assertIn("context/memory MCP gate", route.gate_order)
        self.assertIn("memory", route.mcp_servers)
        self.assertIn("qdrant", route.mcp_servers)
        self.assertIn("sequentialthinking", route.mcp_servers)

    def test_render_query_routes_to_technical_delivery_mcps(self):
        route = route_query("Quarto render PDF screenshot GitHub issue kontrolü")

        self.assertIn("technical delivery MCP gate", route.gate_order)
        self.assertIn("playwright", route.mcp_servers)
        self.assertIn("chrome-devtools", route.mcp_servers)
        self.assertIn("github", route.mcp_servers)

    def test_platform_query_routes_to_default_off_platform_mcps(self):
        route = route_query("Firebase Supabase Cloudflare Figma dashboard deploy")

        self.assertIn("platform/design MCP gate", route.gate_order)
        self.assertIn("firebase", route.mcp_servers)
        self.assertIn("supabase", route.mcp_servers)
        self.assertIn("cloudflare-api", route.mcp_servers)
        self.assertIn("figma", route.mcp_servers)

    def test_code_search_query_routes_to_sourcegraph_and_serena(self):
        route = route_query("Sourcegraph ile açık kaynak kod arama ve sembol navigasyonu")

        self.assertIn("code search MCP gate", route.gate_order)
        self.assertIn("sourcegraph", route.mcp_servers)
        self.assertIn("serena", route.mcp_servers)
        self.assertTrue(any("doppler run -p cureohub -c dev_personal" in action for action in route.recommended_actions))
        self.assertTrue(any("KVKK" in warning for warning in route.warnings))

    def test_reference_manager_query_routes_to_zotero(self):
        route = route_query("references.bib Zotero citation key BibTeX eşitle")

        self.assertIn("Zotero reference manager gate", route.gate_order)
        self.assertLess(route.gate_order.index("Anna's Library full-text gate"), route.gate_order.index("Zotero reference manager gate"))
        self.assertIn("dual AI-reliability gate", route.gate_order)
        self.assertIn("zotero:Zotero", route.plugin_layers)
        self.assertTrue(any("zotero_env_bridge.py status --json" in command for command in route.zotero_commands))
        self.assertTrue(any("references/references.bib" in command for command in route.zotero_commands))

    def test_reference_work_routes_to_anamnesis_annas_zotero_and_dual_ai(self):
        route = route_query("Anna's Library tam metin Anamnesis bağlam Zotero referans AI reliability")

        self.assertEqual(route.gate_order[0], "dmnitel local gate")
        self.assertEqual(route.gate_order[1], "Anamnesis context management gate")
        self.assertIn("Anna's Library full-text gate", route.gate_order)
        self.assertIn("Zotero reference manager gate", route.gate_order)
        self.assertIn("dual AI-reliability gate", route.gate_order)
        self.assertIn("anamnesis", route.mcp_servers)
        self.assertIn("annas-reader", route.mcp_servers)

    def test_coreq_quote_query_routes_to_local_dmnitel_commands(self):
        route = route_query("COREQ ve alıntı bütünlüğü denetimi yap")

        self.assertTrue(any("audit-coreq" in command for command in route.dmnitel_commands))
        self.assertTrue(any("check-quotes" in command for command in route.dmnitel_commands))

    def test_real_repo_sensitive_paths_are_protected(self):
        protected = [
            Path("01_raw_data/interviews_docx/a.docx"),
            Path("02_processed/transcripts/a.md"),
            Path("01_deidentified/coded_segments.csv"),
            Path(".remember/cache.json"),
        ]

        for path in protected:
            self.assertTrue(is_protected_path(path), path)
        self.assertFalse(is_protected_path(Path("07_reports/tool_bridge.md")))

    def test_cli_output_path_guard_covers_sensitive_dirs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            safe_path = Path(tmpdir) / "07_reports/tool_bridge.md"
            unsafe_path = Path(tmpdir) / "01_raw_data/tool_bridge.md"

            self.assertFalse(is_protected_path(safe_path))
            self.assertTrue(is_protected_path(unsafe_path))


if __name__ == "__main__":
    unittest.main()
