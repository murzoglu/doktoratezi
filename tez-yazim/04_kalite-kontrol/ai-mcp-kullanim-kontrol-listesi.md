# AI ve MCP Kullanım Kontrol Listesi

> **Kanonik kural otoritesi:** Bu, **Kapı 5** (AI-reliability) + araç kullanımı
> operasyonel checklist'idir. Araç/MCP seçim otoritesi →
> `01_mimari/yetkinlik-ve-arac-mimarisi.md`; süreç/oturum/AI-log →
> `00_kaynak-kurallari/talimatname-claude-code.md`; AI-reliability katman sınırı
> (sci-audit A–G ↔ repo ai-audit KVKK) →
> `bolum-finalizasyon-sertifikasyon-playbook.md`. Klasör haritası:
> `04_kalite-kontrol/README.md`.

- [ ] Önce local repo kaynakları okundu.
- [ ] Tez formatı için `docs/tez-kilavuz` ve `tez-yazim/` kaynakları kullanıldı.
- [ ] Tool seçimi belirsizse `./dmnitel route-tool --query "<soru>"` çalıştırıldı.
- [ ] Karma yazımda `./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md` güncellendi.
- [ ] Dış literatür için Evidentia MCP çekirdeği kullanıldı.
- [ ] Zotero import/write yapılmadı veya açık onay alındı.
- [ ] Raw `codex mcp list` çalıştırılmadı; redacted roster komutu kullanıldı.
- [ ] Harici MCP/plugin sonucu tez içeriğini etkilediyse AI use log'a kayıt düşüldü.
- [ ] Harici MCP/Evidentia/Zotero'ya yalnız anonim/türetilmiş bağlam gönderildi; `log-ai-use --data-type "anonim/türetilmiş"`, raw/identifiable = no.
- [ ] Üretilen metin resmi kılavuz + repo kanıtı çifte kontrolünden geçti.
- [ ] Bölüm finalize edilmeden önce sertifikasyon playbook'u çalıştırıldı.
- [ ] Sertifika `certified-final` değilse bölüm final olarak etiketlenmedi.
