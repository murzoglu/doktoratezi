#!/usr/bin/env python3
"""CSR-FINAL.md -> render qmd: Quarto YAML (csr) + figur gomme + karar paneli chunk."""
import os
from pathlib import Path
import re

ROOT = Path(
    os.environ.get("CLAUDE_PROJECT_DIR")
    or Path(__file__).resolve().parents[1]
).resolve()
SRC = ROOT / "docs" / "CLINICAL-STUDY-REPORT-FINAL.md"
OUT = ROOT / "CSR-FINAL-render.qmd"

P = "docs/assets/figures/carbon/primary"
F2 = "outputs/figures"
PSY = "docs/assets/figures/carbon/psychometric"
DEM = "docs/assets/figures/carbon/demographic"

# heading-prefix -> [(relpath, caption, figid)]
FIG_MAP = {
    "## 9.3 ": [(f"{DEM}/demo-01-grup-dagilim.svg", "Ornelem grup dagilimi (DM vs Kontrol aile sayilari).", "fig-d01"),
               (f"{DEM}/demo-02-cocuk-yas-dagilim.svg", "Cocuk yasi dagilimi (indeks ve kardes, grup bazinda).", "fig-d02"),
               (f"{DEM}/demo-03-cinsiyet-grup.svg", "Cinsiyet dagilimi grup bazinda.", "fig-d03"),
               (f"{DEM}/demo-05-aile-buyuklugu.svg", "Aile buyuklugu (cocuk sayisi) dagilimi.", "fig-d05"),
               (f"{DEM}/demo-06-anne-yas.svg", "Anne yasi dagilimi grup bazinda.", "fig-d06"),
               (f"{DEM}/demo-11-egitim.svg", "Anne/es egitim duzeyi dagilimi grup bazinda.", "fig-d11"),
               (f"{DEM}/demo-07-beck-grup.svg", "Beck depresyon toplam puani grup karsilastirmasi.", "fig-d07"),
               (f"{DEM}/demo-09-antidep.svg", "Anne antidepresan kullanimi grup bazinda.", "fig-d09")],
    "## 9.4 ": [(f"{DEM}/demo-15-dm-suresi.svg", "DM hastalik suresi dagilimi.", "fig-d15"),
               (f"{DEM}/demo-16-tani-strata.svg", "Tani yasi strata dagilimi (erken/okul/ergen).", "fig-d16")],
    "## 8.6 ": [(f"{P}/fig-02-causal-dag.svg", "Birincil etki modelleri icin yonlu asiklik graf (DAG) ve backdoor ayarlama seti.", "fig-dag")],
    "## 8.7 ": [(f"{P}/fig-05-ses-correlation-heatmap.svg", "SES latent kompoziti: bilesen korelasyon isi haritasi.", "fig-ses")],
    "## 8.8 ": [(f"{P}/fig-03-smd-love-plot.svg", "Eslem oncesi/sonrasi standardize ortalama fark (love plot).", "fig-love"),
                (f"{P}/fig-04-propensity-overlap.svg", "Egilim skoru ortak destek (overlap) dagilimi.", "fig-ps")],
    "## 9.1 ": [(f"{P}/fig-01-strobe-flow.svg", "STROBE katilimci akis diyagrami (dahil edilen 241 aile / 482 cocuk).", "fig-strobe")],
    "## 9.5 ": [(f"{P}/fig-06-missing-pattern-primary.svg", "Birincil degiskenlerde eksik veri oruntu haritasi.", "fig-miss"),
                (f"{DEM}/demo-12-dm-eksik.svg", "DM-spesifik klinik degiskenlerde eksik veri profili.", "fig-d12"),
                (f"{DEM}/demo-20-eksik-degisken.svg", "Degisken duzeyinde eksik veri oranlari.", "fig-d20")],
    "## 10.1 ": [(f"{PSY}/psychval-01-reliability.svg", "Ic tutarlilik: Cronbach alpha ve McDonald omega alt olcek bazinda.", "fig-rel"),
                 (f"{PSY}/psychval-03-cfa.svg", "Dogrulayici faktor analizi uyum indeksleri.", "fig-cfa")],
    "### 11.1.1 ": [(f"{P}/fig-07-h1-forest.svg", "H1 cok-duzeyli kovaryans analizi forest plot (EMBU-C dort alt olcek).", "fig-h1")],
    "### 11.1.4 ": [(f"{P}/fig-08-h1-three-way-emm.svg", "H1 uclu etkilesim (rol x yas x cinsiyet) kestirilen marjinal ortalamalar.", "fig-h1emm")],
    "### 11.2.1 ": [(f"{P}/fig-09-h2-apim-path.svg", "H2 aktor-partner bagimlilik modeli (APIM) yol diyagrami.", "fig-h2")],
    "### 11.3.1 ": [(f"{P}/fig-10-h3-stratified-forest.svg", "H3 anne oz-bildirim katmanli forest plot (antidepresan strata).", "fig-h3")],
    "### 11.4.2 ": [(f"{P}/fig-11-h4-sem-path.svg", "H4 Beck -> EMBU-P latent yapisal esitlik modeli yol diyagrami.", "fig-h4")],
    "### 11.5.1 ": [(f"{P}/fig-12-h5-ba-grid.svg", "H5 Strateji 1: ICC + Bland-Altman uyum izgarasi (anne-cocuk duad).", "fig-h5ba")],
    "### 11.5.2 ": [(f"{P}/fig-13-h5-rsa-surface.svg", "H5 Strateji 2: Edwards-Parry yanit yuzeyi analizi (RSA).", "fig-h5rsa")],
    "## 12.1 ": [(f"{P}/fig-14-mediation-effects.svg", "Aracilik analizi: Beck -> EMBU-P -> EMBU-C dolayli etki [KESIFSEL].", "fig-med")],
    "## 12.2 ": [(f"{P}/fig-15-lpa-fit-indices.svg", "Latent profil analizi uyum indeksleri (BIC/entropy) [KESIFSEL].", "fig-lpa")],
    "## 12.3 ": [(f"{P}/fig-16-network-graph.svg", "Gauss grafik modeli (GGM) ag yapisi [KESIFSEL].", "fig-net"),
                 (f"{P}/fig-17-network-nct.svg", "Ag karsilastirma testi (NCT) DM vs Kontrol [KESIFSEL].", "fig-nct")],
    "## 12.4 ": [(f"{P}/fig-18-clinical-roc.svg", "Yuksek-riskli anne tahmin modeli ROC egrisi [KESIFSEL].", "fig-roc"),
                 (f"{P}/fig-19-clinical-dca.svg", "Karar egrisi analizi (DCA) net fayda [KESIFSEL].", "fig-dca"),
                 (f"{P}/fig-20-clinical-calibration.svg", "Kalibrasyon egrisi [KESIFSEL].", "fig-cal"),
                 (f"{P}/fig-21-clinical-cart-rf.svg", "CART ve Random Forest degisken onemi [KESIFSEL].", "fig-cart")],
    "## 13.1 ": [(f"{P}/fig-22-specification-curve.svg", "Coklu evren / spesifikasyon egrisi (H3 EMBU-P, 120 spesifikasyon).", "fig-spec")],
    "## 13.3 ": [(f"{P}/fig-23-sensemakr-contour.svg", "Olculmemis karistirici dayanikliligi (sensemakr kontur).", "fig-sens")],
    "## 14.1 ": [(f"{P}/fig-24-bayesian-forest.svg", "Bayesci paralel hat: posterior etki forest plot.", "fig-bayf")],
    "## 14.2 ": [(f"{P}/fig-25-bayesian-diagnostics.svg", "MCMC yakinsama tanilari (R-hat / ESS / trace).", "fig-bayd")],
    # NOT: §18 phase2 figurleri rapor govdesinde zaten gomulu (assets/->docs/assets/ ile onarilir).
}

YAML = '''---
title: "Tip 1 Diyabetli Çocuklar, Sağlıklı Kardeşleri ve Annelerinde Ebeveynlik Tutumlarının Vaka-Kontrol Çalışması"
subtitle: "Klinik Çalışma Raporu — ICH E3 Uyumlu Bütünleşik Rapor"
author:
  - name: "Uzm. Dr. Özlem Murzoğlu Kurt"
    affiliation: "Marmara Üniversitesi SBE, Sosyal Pediatri Doktora Programı"
  - name: "Prof. Dr. Eren Özek"
    affiliation: "Tez danışmanı — MÜTF Neonatoloji"
  - name: "Prof. Dr. Belma Haliloğlu"
    affiliation: "Yardımcı araştırıcı — MÜTF Pediatrik Endokrinoloji"
date: "1 Mayıs 2026"
keywords: ["Tip 1 Diyabet", "ebeveynlik tutumu", "çoklu-informant", "diadik tutarlılık", "vaka-kontrol"]
lang: tr
format:
  html:
    toc: true
    toc-depth: 3
    toc-title: "İçindekiler"
    number-sections: false
    section-divs: true
    embed-resources: true
    fig-format: svg
    fig-dpi: 300
    fig-align: center
    df-print: kable
    theme: cosmo
execute:
  echo: false
  warning: false
  message: false
crossref:
  fig-prefix: Şekil
  tbl-prefix: Tablo
knitr:
  opts_chunk:
    R.options:
      digits: 2
      OutDec: "."
      scipen: 999
    dev: "svg"
    fig.width: 8
    fig.height: 4.6
---

```{r}
#| label: setup
#| include: false
source("~/.claude/skills/carbon-quarto-scientific/assets/r-init-carbon.R")
suppressPackageStartupMessages({
  library(ggplot2); library(dplyr); library(tibble); library(forcats)
})
```

```{r}
#| label: fig-decision-panel
#| fig-cap: "Hipotez karar paneli — beş ön-kayıtlı birincil hipotezin (H1–H5) standardize etki büyüklüğü, %95 güven aralığı, Bayesçi destek ve nihai kararı. H5 manifest ICC yön göstergesi (DM−Kontrol) ile temsil edilir; tek bir etki büyüklüğü değildir."
#| fig-width: 9
#| fig-height: 5
#| out-width: 98%

dec <- tibble::tribble(
  ~y, ~hip,                                 ~eff,  ~lo,    ~hi,   ~karar,                      ~ev,            ~grp,
  5,  "H1 · Çocuk algısı (reddetme)",        0.16,  0.05,  0.26,  "Doğrulandı (+)",            "BF = 8.12",    "Pozitif",
  4,  "H2 · Kardeş ilişkisi (çatışma)",      0.00, -0.18,  0.18,  "Belirsiz (kanıt yetersiz)", "BF/TOST yok",  "Belirsiz",
  3,  "H3 · Anne öz-bildirim (reddetme)",   -0.16, -0.41,  0.09,  "Üç-katmanlı negatif",       "BF = 0.17",    "Negatif",
  2,  "H4 · Beck→EMBU-P (reddetme yolu)",    0.33,  0.19,  0.53,  "Kısmen doğrulandı",         "FDR < .001",   "Kısmi",
  1,  "H5 · Diadik tutarlılık (ICC yön)",   -0.09, -0.20,  0.02,  "Triangülasyon yok",         "tek-strateji", "H5"
) |> mutate(grp = factor(grp, levels = c("Pozitif","Kısmi","Belirsiz","Negatif","H5")))

pal <- c("Pozitif"="#0f62fe","Kısmi"="#007d79","Belirsiz"="#8d8d8d","Negatif"="#da1e28","H5"="#8a3ffc")

ggplot(dec, aes(x = eff, y = reorder(hip, y), color = grp)) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "#a8a8a8") +
  geom_errorbarh(aes(xmin = lo, xmax = hi), height = 0.22, linewidth = 0.7, na.rm = TRUE) +
  geom_point(size = 3.6, na.rm = TRUE) +
  geom_text(aes(x = 0.66, label = karar), hjust = 0, size = 3.3, fontface = "bold") +
  geom_text(aes(x = 0.66, label = ev), hjust = 0, vjust = 2.1, size = 2.7, color = "#525252") +
  scale_color_manual(values = pal, guide = "none") +
  scale_x_continuous(limits = c(-0.55, 1.25), breaks = seq(-0.4, 0.6, 0.2)) +
  labs(x = "Standardize etki büyüklüğü (H1–H4) · ICC yön farkı DM−Kontrol (H5)", y = NULL) +
  theme_carbon(base_size = 11) +
  theme(plot.margin = margin(8, 12, 8, 8))
```

'''


def main():
    raw = SRC.read_text(encoding="utf-8")
    # strip first YAML block
    body = re.sub(r"^---\n.*?\n---\n", "", raw, count=1, flags=re.DOTALL)
    out_lines = []
    refs_section = False
    refs_open = False
    for line in body.splitlines():
        stripped = line.rstrip("\n")
        # orijinal govdedeki phase2 gomme yollarini root-qmd icin onar
        stripped = stripped.replace("](assets/figures/", "](docs/assets/figures/")

        # --- §21 gercek bibliyografya blogu (tek-kosum renumber sonrasi) ---
        if stripped.startswith("# 21. "):
            out_lines.append(stripped)
            refs_section = True
            continue
        if refs_section:
            if stripped.startswith("# ") and not stripped.startswith("# 21"):
                if refs_open:
                    out_lines.append(":::")
                    out_lines.append("")
                    refs_open = False
                refs_section = False
                # asagidaki normal islemeye dus (or. # 22. EKLER)
            elif stripped.startswith("## 21."):
                parts = stripped.split(" ", 2)
                title = parts[2] if len(parts) > 2 else stripped
                if not refs_open:
                    out_lines.append("::: {#refs}")
                    out_lines.append("")
                    refs_open = True
                out_lines.append("")
                out_lines.append(f"**{title}**")
                out_lines.append("")
                continue
            elif stripped.strip() and re.search(r"\(\d{4}[a-z]?\)", stripped):
                if not refs_open:
                    out_lines.append("::: {#refs}")
                    out_lines.append("")
                    refs_open = True
                out_lines.append("::: {.csl-entry}")
                out_lines.append(stripped)
                out_lines.append(":::")
                continue
            else:
                out_lines.append(stripped)
                continue

        # --- normal isleme ---
        if stripped.strip() == "\\newpage":
            out_lines.append("{{< pagebreak >}}")
            continue
        out_lines.append(stripped)
        # figure insertion after matching heading
        for prefix, figs in FIG_MAP.items():
            if stripped.startswith(prefix):
                out_lines.append("")
                for (path, cap, fid) in figs:
                    out_lines.append(f"![{cap}]({path}){{#{fid} width=88%}}")
                    out_lines.append("")
                break
    qmd = YAML + "\n".join(out_lines) + "\n"
    OUT.write_text(qmd, encoding="utf-8")
    n_figs = sum(len(v) for v in FIG_MAP.values()) + 1
    print(f"OK -> {OUT}")
    print(f"figur gomuldu: {n_figs} (1 yeni karar paneli dahil)")
    print(f"qmd satir: {len(qmd.splitlines())}")


if __name__ == "__main__":
    main()
