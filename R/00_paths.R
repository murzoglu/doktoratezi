thesis_paths <- function(root = getwd()) {
  list(
    root = normalizePath(root, winslash = "/", mustWork = FALSE),
    raw_data_dir = file.path(root, "data", "raw"),
    processed_data_dir = file.path(root, "data", "processed"),
    references_dir = file.path(root, "references"),
    chapters_dir = file.path(root, "chapters"),
    outputs_dir = file.path(root, "outputs")
  )
}
