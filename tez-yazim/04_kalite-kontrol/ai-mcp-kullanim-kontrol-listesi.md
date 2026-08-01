# AI ve MCP Kullanım Kontrol Listesi

> **Kanonik kural otoritesi:** Bu, **Kapı 5** (AI-reliability) + araç kullanımı
> operasyonel checklist'idir. Araç/MCP seçim otoritesi →
> `01_mimari/yetkinlik-ve-arac-mimarisi.md`; süreç/oturum/AI-log →
> `00_kaynak-kurallari/talimatname-claude-code.md`; AI-reliability katman sınırı
> (sci-audit A–G ↔ repo ai-audit KVKK) →
> `bolum-finalizasyon-sertifikasyon-playbook.md`. Klasör haritası:
> `04_kalite-kontrol/README.md`. Otomatik denetim: bu listenin
> makine-doğrulanabilir maddeleri `tez-kontrol-checklisti.md` (K5-*) altında
> `scripts/util/tez_checklist_verify.py --section K5` ile koşulur.

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

## Copilot oturumu ek kontrolleri

Copilot (VS Code) oturumunda keşif yolları farklıdır; yalnız bu oturumlarda:

- [ ] MCP paritesi doğrulandı: `.mcp.json` (Copilot CLI) ile `.vscode/mcp.json`
      (VS Code Chat paneli) aynı sunucu kümesini içeriyor. Copilot CLI
      `.vscode/mcp.json`'u **okumaz**; yeni sunucu ikisine birden eklenir.
- [ ] Slash komut paritesi doğrulandı: `.claude/commands/` ↔ `.github/prompts/`
      birebir (9/9). Claude tarafında komut değişti ise Copilot ikizi de güncellendi.
- [ ] Zorlama katmanı yüklendi: `.github/hooks/hooks.json` depoda mevcut ve
      `.claude/settings.json` ile aynı beş olayı taşıyor (kurulum gerekmez;
      dosya değiştiyse yeni oturum gerekir).
- [ ] Skill kaydı güncel: `.claude/skills/` altında yeni/değişmiş skill varsa
      `/skills reload` çalıştırıldı ve `/skills` listesinde göründüğü doğrulandı
      (`description` ~1024 karakteri aşan skill sessizce yüklenmez).
