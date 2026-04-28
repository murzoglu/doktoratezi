source("renv/activate.R")
renv_activate <- file.path("renv", "activate.R")

if (file.exists(renv_activate)) {
  source(renv_activate)
}

user_library <- path.expand("~/R/libs")
if (!nzchar(Sys.getenv("RENV_PROJECT")) && dir.exists(user_library)) {
  .libPaths(c(user_library, .libPaths()))
}
