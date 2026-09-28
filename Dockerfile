FROM rocker/verse:4.5.3

LABEL maintainer="ozlem.murzoglu@gmail.com"
LABEL description="T1DM-EBEVEYN reproducible R/Quarto environment"
LABEL org.opencontainers.image.r_library_mount="/home/rstudio/project/renv/library"

ENV R_PROFILE_USER=/dev/null
ENV R_LIBS=/home/rstudio/project/renv/library/linux-ubuntu-noble/R-4.5/x86_64-pc-linux-gnu

RUN apt-get update && apt-get install -y --no-install-recommends \
    bwidget \
    cmake \
    g++ \
    jags \
    libcurl4-openssl-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libfribidi-dev \
    libgdal-dev \
    libgeos-dev \
    libgit2-dev \
    libharfbuzz-dev \
    libjpeg-dev \
    libpng-dev \
    libproj-dev \
    librsvg2-bin \
    libssl-dev \
    libtiff5-dev \
    libudunits2-dev \
    libv8-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# Quarto renders the thesis with the bundled TeX Live installation. Install
# the thesis preamble's TeX dependencies at build time so an isolated runtime
# never tries to fetch them from the network.
RUN tlmgr install \
    amsfonts \
    anyfontsize \
    babel-turkish \
    bookmark \
    booktabs \
    caption \
    colortbl \
    fancyhdr \
    float \
    fontawesome5 \
    hyphenat \
    microtype \
    multirow \
    parskip \
    polyglossia \
    selnolig \
    setspace \
    tcolorbox \
    titlesec \
    unicode-math \
    xurl \
    && mktexlsr

RUN curl -fsSL --retry 3 --retry-delay 2 \
    https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/pdfcol.tar.xz \
    -o /tmp/pdfcol.tar.xz \
    && echo '91006383de0aa2244953c9d1aca8213316119c8359b836a47a0fc0cbb0b46188  /tmp/pdfcol.tar.xz' | sha256sum --check --status \
    && tar -xJf /tmp/pdfcol.tar.xz -C /opt/texlive/texmf-local tex/latex/pdfcol/pdfcol.sty \
    && rm /tmp/pdfcol.tar.xz \
    && mktexlsr /opt/texlive/texmf-local \
    && kpsewhich pdfcol.sty >/dev/null

RUN curl -fsSL --retry 3 --retry-delay 2 \
    https://ctan.math.illinois.edu/systems/texlive/tlnet/archive/hyphen-turkish.tar.xz \
    -o /tmp/hyphen-turkish.tar.xz \
    && echo 'ab777d12d352d9dd75c2beb9167f21e4c3870f9413d08236342771474e03af68  /tmp/hyphen-turkish.tar.xz' | sha256sum --check --status \
    && tar -xJf /tmp/hyphen-turkish.tar.xz -C /opt/texlive/texmf-local \
        tex/generic/hyph-utf8/loadhyph/loadhyph-tr.tex \
        tex/generic/hyph-utf8/patterns/ptex/hyph-tr.ec.tex \
        tex/generic/hyph-utf8/patterns/tex/hyph-tr.tex \
        tex/generic/hyph-utf8/patterns/txt/hyph-tr.pat.txt \
    && rm /tmp/hyphen-turkish.tar.xz \
    && mkdir -p /opt/texlive/texmf-local/tex/generic/config \
    && printf 'turkish loadhyph-tr.tex\n' > /opt/texlive/texmf-local/tex/generic/config/language-local.dat \
    && mktexlsr /opt/texlive/texmf-local \
    && tlmgr generate language \
    && fmtutil-sys --byhyphen "$(kpsewhich language.dat)" \
    && kpsewhich hyph-tr.tex >/dev/null \
    && grep -q '^turkish' "$(kpsewhich language.dat)"

WORKDIR /home/rstudio/project

COPY . .

RUN chmod -R a+rX /home/rstudio/project \
    && mkdir -p \
    data/processed \
    outputs/quarto \
    outputs/tables \
    outputs/figures \
    outputs/models \
    /home/rstudio/project/renv/library

# The lockfile-restored project library and its linked renv cache are mounted
# read-only at runtime. Keeping both outside the build context avoids copying
# sensitive project material or a multi-gigabyte local package cache into the image.

CMD ["bash", "-lc", "test -f \"$R_LIBS/targets/DESCRIPTION\" || { echo 'Missing read-only project renv library mount.' >&2; exit 64; }; if [ -f data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock ]; then Rscript -e 'targets::tar_make()'; else Rscript -e 'targets::tar_make(names = c(\"project_paths\", \"raw_data_manifest\"))'; fi && quarto render thesis.qmd --to html"]
