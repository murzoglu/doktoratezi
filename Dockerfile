FROM rocker/verse:4.5.3

LABEL maintainer="ozlem.murzoglu@gmail.com"
LABEL description="T1DM-EBEVEYN reproducible R/Quarto environment"

ENV RENV_CONFIG_CACHE_ENABLED=FALSE
ENV RENV_CONFIG_REPOS_OVERRIDE="https://cran.r-universe.dev,https://cloud.r-project.org"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
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
    libssl-dev \
    libtiff5-dev \
    libudunits2-dev \
    libv8-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/rstudio/project

COPY renv.lock renv.lock
COPY renv/settings.json renv/settings.json
COPY renv/activate.R renv/activate.R

RUN Rscript -e "install.packages('renv', repos = 'https://cloud.r-project.org')" \
    && Rscript -e "renv::restore(prompt = FALSE)"

COPY . .

RUN mkdir -p data/processed outputs/quarto outputs/tables outputs/figures outputs/models

CMD ["bash", "-lc", "if [ -f data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock ]; then Rscript -e 'targets::tar_make()'; else Rscript -e 'targets::tar_make(names = c(\"project_paths\", \"raw_data_manifest\"))'; fi && quarto render thesis.qmd --to html"]
