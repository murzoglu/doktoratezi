# Korumalı Kaynak Envanteri

Niteliksel kaynak dosyalarının ayrıntılı taşıma günlüğü, dosya-yol eşlemesi ve
bütünlük değerleri Git-dışı korumalı depoda tutulur. Bu ayrım, aile/rol düzeyi
metaverinin public çalışma ağacında yayılmasını önler.

## Versioned kapsam

- Kanonik, paylaşılabilir nitel sonuçlar: `03_analysis/` ve
  `06_manuscript_outputs/` altındaki redakte edilmiş belgeler.
- Public bütünlük sözleşmesi: `03_analysis/public_canonical_manifest.json`.
- Korumalı kaynak bütünlüğü: yerel `01_raw_data/audit_manifests/` altında;
  Git, harici MCP/RAG ve bellek katmanları dışındadır.

## Operasyon kuralı

Yeni kaynaklar önce `01_raw_data/v3_incoming/` alanına kısıtlı izinlerle alınır.
Kanonik terfi, yalnız araştırmacı sınıflaması ve içerik-güvenlik değerlendirmesi
sonrasında, ham içerik veya satır-düzeyi metaveri public ağaca taşınmadan yapılır.
