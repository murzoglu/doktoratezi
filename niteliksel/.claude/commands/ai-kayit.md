---
description: Harici AI/MCP/plugin kullanımını 99_ai_use_log günlüğüne kaydeder (LLM beyanı + audit trail)
argument-hint: "[kullanılan araç ve amaç]"
allowed-tools: Bash(./dmnitel log-ai-use *)
---

Bu oturumda kullanılan harici AI/MCP/plugin işlemlerini günlüğe kaydet: **$ARGUMENTS**

1. Oturumda hangi harici araçların (Evidentia çekirdeği, PubMed/OpenAlex, YÖK,
   Anna's, Zotero, mevzuat, terminoloji MCP'leri vb.) tez içeriğini etkilediğini
   listele.
2. Her biri için şu komutu doldurup çalıştır:

```
./dmnitel log-ai-use \
  --tool "<araç adı>" \
  --model "<model/sürüm>" \
  --purpose "<amaç>" \
  --data-type "anonim/türetilmiş" \
  --output-summary "<çıktının tek cümlelik özeti>" \
  --external-api-used yes
```

3. Kurallar: `--data-type` daima anonim/türetilmiş kalır; ham/kimliklenebilir veri
   bayrakları `no` olmak zorundadır çünkü o veriler harici araçlara zaten
   gönderilemez. Kayıt sonrası `99_ai_use_log/ai_use_log.csv` son satırını
   doğrula ve raporla.
