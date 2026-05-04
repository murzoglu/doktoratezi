# Figma Technical Diagram Library Uyum Audit

Üretim zamanı: `2026-05-01 15:48:49 UTC`

Bu dosya, Carbon SVG setindeki flow/diagram nitelikli figürlerin IBM Technical Diagram Library kaynaklı bileşen rollerine göre nasıl iyileştirildiğini belgeler.

## Figma Kaynak Envanteri

- Figma file key: `RtZDc7pMQt8HcgYTiitspr`
- Okunan sayfalar: `Node`, `Connector`, `Label text`, `Label pill`, `Flow number`, `Legend`, `Indicator badge`, `Flow shape`, `IT architecture`.
- Kullanılan bileşen aileleri: `Large node - Icon default`, `Small node - Icon`, `Connector line + line ending`, `_Connector`, `Line ending`, `Label text`, `Label pill`, `Flow number`, `Legend`.
- Varyant sinyalleri: node renkleri Blue/Cyan/Green/Magenta/Purple/Red/Teal/Cool Gray/Black; connector stilleri Solid 1px, Solid 2px, Dash 4/8/16px, Double, Tunnel; line ending tipleri Arrow/Circle/Square/Diamond/Bar.

## Uygulama Kararları

- Flow/diagram figürleri custom SVG olarak yeniden oluşturuldu; generic chart axis/grid ve raster katmanı yoktur.
- Connector stroke'ları Carbon `border-strong-01` / `layer-accent-01` rampasına normalize edildi; yönlü yollar Figma `Connector line + line ending` davranışına uygun marker ile çizildi.
- SVG köküne `data-figma-technical-diagram-library`, `data-technical-diagram-role` metadata alanları eklendi.
- SVG `<defs>` içine `tdl-node`, `tdl-connector`, `tdl-label-pill`, `tdl-flow-number` sınıfları eklendi; bu sınıflar Figma rol eşlemesini görünür ve yeniden düzenlenebilir kılar.
- Okunurluk için APIM ve SEM diyagramlarında katsayı etiketleri label pill'e alınmış, DAG'de karıştırıcılar bir adjustment-set container'ına toplanmış, network grafiğinde node label'ları clipping üretmeyecek dış offsetlerle yerleştirilmiştir.

## İyileştirilen Figürler

| ID | SVG | Figma Technical Diagram rolü | Native renderer | Durum | Carbon audit |
|---|---|---|---|---|---|
| strobe_flow | [fig-01-strobe-flow.svg](primary/fig-01-strobe-flow.svg) | Flow shape + Flow number + Connector + Label pill | PASS: custom Technical Diagram SVG; no chart grid/axis/raster layer | PASS: full Figma Technical Diagram Library SVG | PASS: Carbon Charts |
| causal_dag | [fig-02-causal-dag.svg](primary/fig-02-causal-dag.svg) | Large node + Connector + Legend | PASS: custom Technical Diagram SVG; no chart grid/axis/raster layer | PASS: full Figma Technical Diagram Library SVG | PASS: Carbon Charts |
| h2_apim_path | [fig-09-h2-apim-path.svg](primary/fig-09-h2-apim-path.svg) | Large node + Connector line ending + Label text | PASS: custom Technical Diagram SVG; no chart grid/axis/raster layer | PASS: full Figma Technical Diagram Library SVG | PASS: Carbon Charts |
| h4_sem_path | [fig-11-h4-sem-path.svg](primary/fig-11-h4-sem-path.svg) | Large node + Connector line ending + Label text | PASS: custom Technical Diagram SVG; no chart grid/axis/raster layer | PASS: full Figma Technical Diagram Library SVG | PASS: Carbon Charts |
| network_graph | [fig-16-network-graph.svg](primary/fig-16-network-graph.svg) | Small node + Connector + Legend | PASS: custom Technical Diagram SVG; no chart grid/axis/raster layer | PASS: full Figma Technical Diagram Library SVG | PASS: Carbon Charts |

## Notlar

- Bu çalışma Figma dosyasını değiştirmez; Figma Technical Diagram Library, yerel SVG üretimi için kaynak/otorite olarak kullanılmıştır.
- Veri yoğun forest plot, ROC/DCA, heatmap, density ve demografik bar/violin grafikleri technical diagram sınıfına alınmadı; bunlar Carbon Charts estetiğiyle bırakıldı.
