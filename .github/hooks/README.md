# `.github/hooks` — Copilot zorlama katmanı

Bu dizin, `.claude/settings.json` içindeki **beş zorlama hook'unu** Copilot
oturumlarına taşır. Kurulum adımı yoktur: Copilot proje hook'larını git kökündeki
`.github/hooks/*.json` dosyalarından okur, dosya depoda olduğu için sonraki
oturumda kendiliğinden yüklenir.

| Dosya | Görev |
| --- | --- |
| `hooks.json` | Olay → betik eşlemesi (Claude sözdizimi; `.claude/settings.json` ile aynı) |
| `dispatch.py` | Köprü: `.claude/hooks/*.py` çalıştırır, çıktı sözleşmesini çevirir |

Yalnız `.json` dosyaları taranır; `.py` ve `.md` yok sayılır.

## Neden Claude sözdizimi çalışıyor

Copilot yükleyicisi Claude olay adlarını otomatik çevirir ve `_vsCodeCompat`
bayrağını kendisi koyar (`SessionStart`→`sessionStart`, `UserPromptSubmit`→
`userPromptSubmitted`, `PreToolUse`→`preToolUse`, `PostToolUse`→`postToolUse`,
`Stop`→`agentStop`). İç içe `{matcher, hooks:[…]}` bloklarını da düzleştirir ve
`command`→`bash`+`powershell`, `timeout`→`timeoutSec` normalizasyonunu yapar.
`_vsCodeCompat` sayesinde payload biçimi Claude Code'unkiyle birebir aynı olur —
bu yüzden `.claude/hooks/*.py` betikleri **değişmeden** çalışır.

Matcher'lar da Claude adlandırmasıyla yazılır; Copilot kendi araç adlarını eşler:
`"Bash"` → `bash`/`Bash`, `"Write|Edit|MultiEdit"` → `create`/`edit`/`Write`/
`Edit`/`MultiEdit`.

## dispatch.py neden gerekli

Payload biçimi aynı olsa da iki **çıktı sözleşmesi** farkı kalır:

1. **Bloklama.** Claude'da `exit 2 + stderr` evrensel blok sinyalidir. Copilot bunu
   yalnız *uyarı* sayar ve turu durdurmaz — yani sır taraması sessizce
   etkisizleşirdi. Köprü exit 2'yi olaya uygun karara çevirir:
   `preToolUse` → `hookSpecificOutput.permissionDecision = "deny"`, diğerleri →
   `{"decision":"block","reason":…}`.
2. **Bağlam enjeksiyonu.** Claude `hookSpecificOutput.additionalContext` yazar;
   Copilot'un `sessionStart`/`postToolUse` çıktı dönüştürücüsü **üst düzey**
   `additionalContext` okur. Köprü alanı üst düzeye taşır (ikisini de bırakır).
   `preToolUse` istisnadır: orada `hookSpecificOutput` yerel olarak okunur.

Ayrıca depo parmak izi (`.claude/hooks` + `tez-yazim` + `_targets.R`) tutmazsa
köprü sessizce çıkar.

## Bakım

Politika değişirse sıra:

1. `.claude/hooks/` (kaynak) + `.codex/hooks/` (ikiz) birlikte güncellenir.
2. `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_claude_hooks.py` çalıştırılır —
   `CopilotHookBridgeTests` bu dizinin `.claude/settings.json` ile eşliğini
   (olay kümesi, matcher, timeout, betik varlığı) doğrular.
3. Bu dizin **değişmez** — betikleri kopyalamadığı için otomatik güncel kalır.
   Yalnız yeni bir hook olayı eklenirse `hooks.json` genişletilir.

## Elle doğrulama

```bash
# Sır içeren prompt bloklanmalı
echo '{"hook_event_name":"UserPromptSubmit","cwd":"'"$PWD"'","prompt":"sk-ant-abcdefghijklmnopqrstuvwxyz012345"}' \
  | python3 .github/hooks/dispatch.py user_prompt_submit.py userPromptSubmitted 15
# beklenen: {"decision": "block", "reason": "Blocked: prompt appears to contain a secret …"}

# Ham veri okuma deny olmalı
echo '{"hook_event_name":"PreToolUse","cwd":"'"$PWD"'","tool_name":"Bash","tool_input":{"command":"cat data/raw/x.csv"}}' \
  | python3 .github/hooks/dispatch.py pre_tool_use_policy.py preToolUse 15
# beklenen: {"hookSpecificOutput": {… "permissionDecision": "deny" …}}
```

Oturum içinde hook'ların yüklendiğini görmek için yasaklı bir komut deneyin;
deny gerekçesi görünmelidir.
