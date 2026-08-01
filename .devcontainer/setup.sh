#!/usr/bin/env bash
# Dev Container postCreate kurulum betigi — T1DM-Tez
#
# Amac: ona-base:2.0 base image'i R / quarto / pandoc / librsvg icermez. Bu arac
# zinciri onceki ortam durumuna gizli baglilik yerine burada acikca kurulur; boylece
# devcontainer rebuild sonrasi tez pipeline'i (targets) ve render (quarto docx/html)
# tekrar uretilebilir kalir.
#
# Bilesenler:
#   - librsvg2-bin : quarto docx render'inde SVG figurleri raster'a cevirip gomer
#                    (eksikse pandoc "rsvg-convert not in path" ile figursuz docx uretir)
#   - pandoc       : sistem pandoc (quarto kendi pandoc'unu tasir; bu ek guvence)
#   - R 4.5.3      : rig (R Installation Manager) ile — renv.lock ile birebir surum
#   - quarto       : pinned .deb (sabit surum -> reprodusibilite)
#   - R paketleri  : renv::restore (renv.lock, 655 paket). PPM noble binary deposu
#                    kaynak-derlemeyi azaltir.
set -euo pipefail

QUARTO_VERSION="1.9.38"
R_VERSION="4.5.3"
export DEBIAN_FRONTEND=noninteractive

echo "==> apt guncelle + sistem araclari + R paketi derleme bagimliliklari"
sudo apt-get update
# Temel araclar + render (librsvg/pandoc) + R kaynak-derleme sistem kutuphaneleri.
# Bagimlilik gerekceleri:
#   fontconfig/freetype/harfbuzz/fribidi -> systemfonts, textshaping, ragg (gt/ggpubr/papaja)
#   png/jpeg/tiff/cairo/xt              -> ragg, Cairo, grafik cihazlari
#   xml2/ssl/curl                       -> xml2, openssl, curl, httr, rvest
#   glpk/gmp/mpfr                       -> igraph, qgraph, Rmpfr
#   cmake + nlopt                       -> nloptr (-> lme4, lmerTest, optimx, mice, ...)
#   gdal/geos/proj/udunits              -> sf, terra, units
#   magick++                            -> magick
#   jags                                -> rjags
#   libnode (V8)                        -> V8
sudo apt-get install -y --no-install-recommends \
  ca-certificates gnupg dirmngr curl wget cmake \
  librsvg2-bin pandoc \
  libfontconfig1-dev libfreetype6-dev libharfbuzz-dev libfribidi-dev \
  libpng-dev libjpeg-dev libtiff5-dev libcairo2-dev libxt-dev \
  libxml2-dev libssl-dev libcurl4-openssl-dev \
  libglpk-dev libgmp-dev libmpfr-dev libnlopt-dev \
  libgdal-dev libgeos-dev libproj-dev libudunits2-dev \
  libmagick++-dev jags libnode-dev

echo "==> rig (R Installation Manager) kur"
if ! command -v rig >/dev/null 2>&1; then
  curl -fsSL https://github.com/r-lib/rig/releases/download/latest/rig-linux-x86_64-latest.tar.gz \
    -o /tmp/rig.tar.gz
  sudo tar xzf /tmp/rig.tar.gz -C /usr/local
  rm -f /tmp/rig.tar.gz
fi

echo "==> R ${R_VERSION} kur (rig) + varsayilan yap"
if ! rig list 2>/dev/null | grep -q "${R_VERSION}"; then
  sudo rig add "${R_VERSION}"
fi
sudo rig default "${R_VERSION}"

echo "==> Posit PPM noble binary CRAN deposu (renv::restore hizlandirma)"
# PPM binary'leri cogu pakette kaynak derlemeyi atlatir. Kullanici .Rprofile.site
# uzerinden repos ayarlanir; renv autoloader bunu miras alir.
cat > "${HOME}/.Rprofile.site.ppm" <<'RPROF'
options(
  repos = c(P3M = "https://p3m.dev/cran/__linux__/noble/latest"),
  HTTPUserAgent = sprintf(
    "R/%s R (%s)", getRversion(),
    paste(getRversion(), R.version["platform"], R.version["arch"], R.version["os"])
  )
)
RPROF

echo "==> quarto ${QUARTO_VERSION} (.deb, pinned)"
if [ "$(quarto --version 2>/dev/null || echo none)" != "${QUARTO_VERSION}" ]; then
  curl -fsSL -o /tmp/quarto.deb \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb"
  sudo apt-get install -y /tmp/quarto.deb
  rm -f /tmp/quarto.deb
fi

echo "==> surumler"
R --version | head -1
quarto --version
rsvg-convert --version | head -1
pandoc --version | head -1

echo "==> R paketleri: renv::restore (renv.lock, PPM binary tercihli)"
if [ -f renv.lock ]; then
  R_PROFILE_USER="${HOME}/.Rprofile.site.ppm" Rscript -e '
    if (!requireNamespace("renv", quietly=TRUE)) install.packages("renv")
    renv::restore(prompt = FALSE)
  ' || echo "!! renv::restore basarisiz — manuel: Rscript -e '\''renv::restore(prompt=FALSE)'\''"
fi

echo "==> Kurulum tamam."
