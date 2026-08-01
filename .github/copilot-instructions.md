# Copilot yönergeleri — Doktoratezi (T1DM & Ebeveynlik) nicel kol

Bu depo Quarto + R ile yazılan doktora tezidir. Ayrıntılı proje bağlamı için
[AGENTS.md](../AGENTS.md), [CLAUDE.md](../CLAUDE.md) ve
[CONVENTIONS.md](../CONVENTIONS.md) kanonik kaynaklardır; bu dosya Claude Code
katmanındaki **hook + izin (permissions.deny) güvenlik kurallarının** Copilot
karşılığıdır ve her oturumda bağlayıcıdır.

## Dil ve kaynak temeli
- Tez/depo açıklamaları, kod yorumları ve commit mesajları **Türkçe**dir
  (`_quarto.yml` `lang: tr`), kullanıcı aksini istemedikçe.
- Depo iddialarını kontrol edilmiş dosyalara dayandır: `AGENTS.md`, `CLAUDE.md`,
  `_targets.R`, `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`, kanonik kilit
  dosyası, `tez-yazim/README.md`, `docs/tez-kilavuz/`, ilgili `R/` veya `tests/`.
- Tez-içi olgular ile dış klinik/istatistik iddiaları ayır; dış iddialarda
  birincil literatür veya resmi dokümantasyon kullan ve tarih/sürüm koru.

## Veri yönetişimi sınırı (SERT — asla ihlal etme)
Aşağıdaki yolları **okuma, düzenleme, içeriğini yazdırma veya özetleme**:
- `data/raw/**`, `data/identified/**`, `data/cleaned/**`, `data/backup/**`
- `data/processed/**` içindeki satır-düzeyi veri: `*.csv`, `*.tsv`, `*.rds`,
  `*.parquet`, `*.xlsx` (yalnız `.lock` ve veri-haritası METADATA dosyaları okunabilir)
- `outputs/**` içindeki `*.csv`, `*.tsv`, `*.rds`, `*.parquet`
- `_targets/**`
- `.env`, `.env.*`, `**/.env`, `**/client_secret*`, `**/credentials*`,
  `**/dr-murzoglu-doktora.json`
- `data/**` ve `_targets/**` altında **düzenleme (Edit) yapma**.

Analiz targets pipeline'ı ve aggregate çıktılar üzerinden yürür; ham satır-düzeyi
içerik hiçbir çıktı veya sohbete sızmaz (KVKK).

## Sır ve komut güvenliği
- Hiçbir API anahtarı, parola, token veya kimlik değerini **yazdırma/loglama**;
  `.env`/credential dosyalarının içeriğini isteme veya gösterme.
- Yıkıcı/geri döndürülemez kabuk komutlarını (`rm -rf`, `git push --force`,
  `git reset --hard`, korumalı veri klasörlerine yazma, `_targets/` silme)
  açık kullanıcı onayı olmadan çalıştırma.
- Terminal çıktısında ham veri veya sır görürsen özetleme; yalnız güvenli/aggregate
  sonucu bildir.

## İş bitirme kapısı (kaynaksız-sayı yasağı)
- Metne giren her **dış** sayısal iddia (oran, etki büyüklüğü, prevalans vb.)
  bir kaynağa bağlı olmalıdır; kaynağı doğrulanmamış dış sayı yazma.
- **Uydurma referans yasağı**: DOI/PMID/kaynak doğrulanmadan citation üretme.
  Referanslar `/referans-kapisi` sürecinden geçer; kaynakçaya yalnız `cite-ok` girer.

## Araç yönlendirme (görev tipine göre)
- Tez/veri/istatistik/yazım işinin ana kapısı `t1dm-tez-rehberi` skill'idir.
- Dış literatür, citation, tam metin, KOL, ön-kayıt, YÖK tez veya benchmark
  kanıtı için Evidentia katmanı (pubmed-epmc, openalex, semantic-scholar,
  anamnesis, evidentia-kb, annas-reader, openathens, yok-akademik) devreye girer.
- **MCP iki yüzeylidir; ikisi de tutulur.** Copilot CLI **yalnız** `.mcp.json` ve
  `.github/mcp.json` okur — `.vscode/mcp.json` **VS Code Chat paneline özeldir** ve
  CLI tarafından okunmaz. Bu yüzden aynı 14 sunucu her iki dosyada da tanımlıdır;
  birine sunucu eklenince diğerine de eklenir (parite şartı, iki dosyanın başındaki
  `_surface` notunda yazılıdır). Roster: `minerva-evidence` (Roche literatür
  vektör-korpusu; **yalnız literatür terimi**, asla katılımcı/ham veri),
  `galileo-audit`, `zotero-refs`, `eric-mcp` (stdio/`.env`); `openathens`,
  `annas-reader`, `resmi-gazete-mcp`, `anamnesis`, `evidentia-kb`, `yok-akademik`
  (HTTP, token); `pubmed`, `pubmed-epmc`, `openalex`, `semantic-scholar` (HTTP,
  auth-siz; sci-audit citation-forensics ve `/referans-kapisi` DOI doğrulaması
  bunları kullanır).
- **sci-audit + evidentia skilleri kuruludur** (cureonics-marketplace →
  `~/.claude/plugins/marketplaces/cureonics-marketplace`; skiller `~/.agents/skills/`
  sembolik bağlarıyla keşfedilir): `turkish-sci-style` (axis G Türkçe imla/okunabilirlik),
  `citation-forensics` (axis A uydurma kaynak), `claim-grounding` (axis B),
  `stats-forensics` (axis C), `hallucination-signals` (axis D), `ai-transparency` (axis F),
  `sci-audit-orchestrator`, `medical-research`, `start`. Slash komutları (`/sci-audit:*`)
  Copilot'ta yoktur; skiller otomatik tetiklenir, scriptler doğrudan çalıştırılır.
- **Depo skilleri** `.claude/skills/` altındadır ve Copilot bu dizini de tarar:
  `t1dm-tez-rehberi` (ana kapı), `niteliksel-arastirma-rehberi-t1dm`,
  `data-narrative`, `klinisyen-diline-uyarlama`. Skill kaydı **oturum başında
  dondurulur**; yeni/değişmiş skill için `/skills reload` ya da yeni oturum gerekir.
  Frontmatter `description` alanı ~1024 karakteri aşarsa skill sessizce yüklenmez;
  tam tetikleyici listesi her SKILL.md sonundaki
  "Ek: tam tetikleyici kapsamı (arşiv)" bölümünde tutulur.

## Zorlama katmanı (`.github/hooks/`)
`.claude/settings.json` yalnız Claude Code tarafından okunur. Copilot proje
hook'larını **git kökündeki `.github/hooks/*.json`** dosyalarından yükler ve Claude
olay adlarını (`SessionStart`, `PreToolUse`, …) otomatik olarak Copilot adlarına
çevirip `_vsCodeCompat` bayrağını kendisi koyar — yani yapılandırma Claude
sözdiziminde yazılır. Aynı beş zorlama hook'u
[.github/hooks/hooks.json](hooks/hooks.json) ile taşınmıştır: SessionStart
konvansiyon enjeksiyonu, UserPromptSubmit sır taraması, PreToolUse yıkıcı/kimlik
komut deny-list'i, PostToolUse çıktı incelemesi (Bash 15 sn + yazma araçları 200 sn),
Stop kaynaksız-sayı kapısı.

**Kurulum gerekmez** — dosya depoda olduğu için sonraki oturumda kendiliğinden
yüklenir. Betikler kopyalanmaz: [.github/hooks/dispatch.py](hooks/dispatch.py)
köprüsü depodaki `.claude/hooks/*.py` betiklerini çalıştırır (tek doğruluk kaynağı;
ikizi `.codex/hooks/`) ve iki çıktı sözleşmesi farkını çevirir — Claude'un `exit 2`
bloku Copilot'ta yalnız *uyarı* sayıldığı için olay-özel `deny`/`block` kararına,
`hookSpecificOutput.additionalContext` ise Copilot'un okuduğu üst düzeye taşınır.
Politika değişirse `.claude/hooks/` + `.codex/hooks/` birlikte güncellenir; bu
katman betikleri kopyalamadığı için otomatik güncel kalır.

Not: `permissions.deny` listesinin Copilot karşılığı yoktur; yukarıdaki veri
yönetişimi sınırı bu oturumlarda **talimat düzeyinde** bağlayıcıdır ve
PreToolUse deny-list'i ile pekiştirilir.

## Tez yazımı
- Resmi bölüm sırası, format, özet/summary, ondalık virgül, tablo/şekil ve
  kaynakça kararlarında önce `tez-yazim/README.md` ve `docs/tez-kilavuz/`
  kullanılır; bu resmi Marmara kaynakları eski stil notlarına üstündür.
- Slash komut karşılıkları `.github/prompts/` altındadır ve `.claude/commands/` ile
  **birebir paritededir (9/9)**: `tez-oturum`, `bolum-sertifika`, `referans-kapisi`,
  `tez-dogrulama`, `tez-literatur`, `data-narrative`, `klinisyen-diline-uyarlama`.
  Bulgular bölümü için iki kardeş zenginleştirme kapısı da Copilot prompt ikizi
  olarak buradadır: `anlatim-zenginligi` (nesir + referans) ve
  `veri-gosterimi-zenginligi` (figür/tablo/R-çıktı sunum katmanı); ikisi de
  sayı/yön/anlamlılığı değiştirmez. Claude tarafında bir komut değişirse Copilot
  ikizi de aynı işlemde güncellenir.
