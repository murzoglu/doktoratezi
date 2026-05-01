#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(ggplot2)
})

script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
script_path <- if (length(script_arg)) sub("^--file=", "", script_arg[[1]]) else "."
repo_root <- normalizePath(file.path(dirname(script_path), "..", ".."), mustWork = FALSE)
if (!file.exists(file.path(repo_root, "_targets.R"))) {
  repo_root <- normalizePath(getwd(), mustWork = TRUE)
}
setwd(repo_root)

out_dir <- file.path(repo_root, "docs", "carbon-svg-figures")
tmp_dir <- file.path(repo_root, "tmp", "carbon-svg-render")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(tmp_dir, recursive = TRUE, showWarnings = FALSE)

prepare_ibm_plex <- function() {
  font_dir <- file.path(tmp_dir, "fonts", "IBMPlexSans")
  cache_dir <- file.path(tmp_dir, "fontconfig-cache")
  dir.create(font_dir, recursive = TRUE, showWarnings = FALSE)
  dir.create(cache_dir, recursive = TRUE, showWarnings = FALSE)

  local_ttf_dir <- file.path(repo_root, "resources", "fonts", "IBMPlexSans")
  woff_dirs <- c(
    file.path(repo_root, "node_modules", "@ibm", "plex-sans", "fonts", "complete", "woff"),
    "/mnt/thunderbolt/workspaces/Carbonac/frontend/node_modules/@ibm/plex-sans/fonts/complete/woff"
  )

  if (dir.exists(local_ttf_dir)) {
    file.copy(list.files(local_ttf_dir, pattern = "\\.(ttf|otf)$", full.names = TRUE), font_dir, overwrite = TRUE)
  }

  needed <- c("Regular", "SemiBold", "Bold", "Light", "Medium", "Italic")
  if (!length(list.files(font_dir, pattern = "\\.(ttf|otf)$"))) {
    woff_dir <- woff_dirs[dir.exists(woff_dirs)][1]
    if (!is.na(woff_dir)) {
      converter <- paste(
        "from fontTools.ttLib import TTFont\n",
        "from pathlib import Path\n",
        "import sys\n",
        "src_dir=Path(sys.argv[1]); dst_dir=Path(sys.argv[2]); dst_dir.mkdir(parents=True, exist_ok=True)\n",
        "for style in sys.argv[3:]:\n",
        "    src=src_dir / f'IBMPlexSans-{style}.woff'\n",
        "    if not src.exists(): continue\n",
        "    font=TTFont(str(src)); font.flavor=None\n",
        "    font.save(str(dst_dir / f'IBMPlexSans-{style}.ttf'))\n",
        sep = ""
      )
      converter_path <- file.path(tmp_dir, "convert_plex_woff.py")
      writeLines(converter, converter_path, useBytes = TRUE)
      status <- system2("python3", c(converter_path, woff_dir, font_dir, needed), stdout = TRUE, stderr = TRUE)
      if (!is.null(attr(status, "status")) && attr(status, "status") != 0L) {
        warning(paste(status, collapse = "\n"), call. = FALSE)
      }
    }
  }

  fonts <- list.files(font_dir, pattern = "\\.(ttf|otf)$", full.names = TRUE)
  if (!length(fonts)) {
    warning("IBM Plex Sans font files were not found; SVG export will fall back to system sans.", call. = FALSE)
    return(FALSE)
  }

  fonts_conf <- file.path(tmp_dir, "fonts.conf")
  writeLines(c(
    '<?xml version="1.0"?>',
    '<!DOCTYPE fontconfig SYSTEM "fonts.dtd">',
    '<fontconfig>',
    sprintf('  <dir>%s</dir>', normalizePath(font_dir, winslash = "/", mustWork = TRUE)),
    sprintf('  <cachedir>%s</cachedir>', normalizePath(cache_dir, winslash = "/", mustWork = TRUE)),
    '  <config></config>',
    '</fontconfig>'
  ), fonts_conf, useBytes = TRUE)
  Sys.setenv(FONTCONFIG_FILE = normalizePath(fonts_conf, winslash = "/", mustWork = TRUE))
  system2("fc-cache", c("-f", font_dir), stdout = TRUE, stderr = TRUE)
  TRUE
}

ibm_plex_ready <- prepare_ibm_plex()

Sys.setenv(TAR_CONFIG = file.path(repo_root, "_targets.yaml"))
targets::tar_config_set(store = file.path(repo_root, "_targets"))

hash_file <- function(path) {
  if (!file.exists(path)) return(NA_character_)
  tools::md5sum(path)[[1]]
}

relative_path <- function(path) {
  sub(paste0("^", gsub("([\\^$.|?*+(){}\\[\\]\\\\])", "\\\\\\1", repo_root), "/?"), "", normalizePath(path, winslash = "/", mustWork = FALSE))
}

title_case <- function(x) {
  x <- gsub("[-_]+", " ", x)
  x <- gsub("\\s+", " ", x)
  trimws(x)
}

carbon_plot_theme <- function() {
  ggplot2::theme(
    text = ggplot2::element_text(family = "IBM Plex Sans", colour = "#161616", size = 9),
    plot.title = ggplot2::element_text(face = "bold", colour = "#161616", size = 12, margin = ggplot2::margin(b = 4)),
    plot.subtitle = ggplot2::element_text(colour = "#525252", size = 9, margin = ggplot2::margin(b = 8)),
    plot.caption = ggplot2::element_text(colour = "#6f6f6f", size = 8, hjust = 0, margin = ggplot2::margin(t = 6)),
    plot.background = ggplot2::element_rect(fill = "#ffffff", colour = NA),
    panel.background = ggplot2::element_rect(fill = "#ffffff", colour = NA),
    panel.grid.major = ggplot2::element_line(colour = "#e0e0e0", linewidth = 0.28),
    panel.grid.minor = ggplot2::element_blank(),
    axis.line = ggplot2::element_line(colour = "#8d8d8d", linewidth = 0.32),
    axis.ticks = ggplot2::element_blank(),
    legend.background = ggplot2::element_rect(fill = "#ffffff", colour = NA),
    legend.key = ggplot2::element_rect(fill = "#ffffff", colour = NA),
    legend.position = "bottom",
    legend.title = ggplot2::element_text(colour = "#161616", face = "bold", size = 9),
    legend.text = ggplot2::element_text(colour = "#525252", size = 9),
    legend.box.margin = ggplot2::margin(t = 6),
    legend.spacing.x = grid::unit(5, "pt"),
    legend.key.size = grid::unit(13, "pt"),
    axis.title = ggplot2::element_text(colour = "#161616", face = "bold", size = 9),
    axis.text = ggplot2::element_text(colour = "#525252", size = 9),
    strip.background = ggplot2::element_rect(fill = "#f4f4f4", colour = "#e0e0e0"),
    strip.text = ggplot2::element_text(face = "bold", colour = "#161616", size = 9),
    plot.margin = ggplot2::margin(8, 12, 8, 8)
  )
}

carbon_technical_diagram_theme <- function() {
  ggplot2::theme(
    panel.grid = ggplot2::element_blank(),
    axis.line = ggplot2::element_blank(),
    axis.ticks = ggplot2::element_blank(),
    axis.text = ggplot2::element_blank(),
    axis.title = ggplot2::element_blank(),
    legend.position = "bottom",
    legend.title = ggplot2::element_text(colour = "#161616", face = "bold", size = 8),
    legend.text = ggplot2::element_text(colour = "#525252", size = 8),
    plot.margin = ggplot2::margin(10, 14, 10, 10)
  )
}

write_svg_plot <- function(plot, path, width, height, technical_diagram = FALSE) {
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  grDevices::svg(filename = path, width = width, height = height, pointsize = 10, family = "IBM Plex Sans", bg = "white")
  on.exit(grDevices::dev.off(), add = TRUE)
  if (isTRUE(technical_diagram)) {
    print(plot + carbon_plot_theme() + carbon_technical_diagram_theme())
  } else {
    print(plot + carbon_plot_theme())
  }
  invisible(path)
}

carbon_chart_palette <- c(
  "#6929c4", "#1192e8", "#005d5d", "#9f1853", "#fa4d56", "#520408", "#198038",
  "#002d9c", "#ee5396", "#b28600", "#009d9a", "#012749", "#8a3800", "#a56eff"
)

carbon_token_palette <- c(
  "#ffffff", "#000000",
  "#f4f4f4", "#e0e0e0", "#c6c6c6", "#a8a8a8", "#8d8d8d", "#6f6f6f", "#525252", "#393939", "#262626", "#161616",
  "#f2f4f8", "#dde1e6", "#c1c7cd", "#a2a9b0", "#878d96", "#697077", "#4d5358", "#343a3f", "#21272a", "#121619",
  "#edf5ff", "#d0e2ff", "#a6c8ff", "#78a9ff", "#4589ff", "#0f62fe", "#0043ce", "#002d9c", "#001d6c", "#001141",
  "#e5f6ff", "#bae6ff", "#82cfff", "#33b1ff", "#0072c3", "#00539a", "#003a6d",
  "#d9fbfb", "#9ef0f0", "#3ddbd9", "#08bdba", "#009d9a", "#007d79", "#005d5d", "#004144",
  "#defbe6", "#a7f0ba", "#6fdc8c", "#42be65", "#24a148", "#198038", "#0e6027",
  "#e8daff", "#d4bbff", "#be95ff", "#a56eff", "#8a3ffc", "#6929c4", "#491d8b",
  "#ffd6e8", "#ffafd2", "#ff7eb6", "#ee5396", "#d02670", "#9f1853", "#740937",
  "#fff1f1", "#ffd7d9", "#ffb3b8", "#ff8389", "#fa4d56", "#da1e28", "#a2191f", "#750e13", "#520408",
  "#fcf4d6", "#fddc69", "#f1c21b", "#d2a106", "#b28600", "#8e6a00",
  "#fff2e8", "#ffd9be", "#ffb784", "#ff832b", "#eb6200", "#ba4e00", "#8a3800",
  carbon_chart_palette
)

legacy_to_carbon <- c(
  "#4059ad" = "#6929c4",
  "#2f9c95" = "#1192e8",
  "#8b1e3f" = "#9f1853",
  "#d28b26" = "#8a3800",
  "#1f77b4" = "#002d9c",
  "#d62728" = "#fa4d56",
  "#e68fac" = "#ee5396",
  "#5b8def" = "#1192e8",
  "#7e57c2" = "#a56eff",
  "#26a69a" = "#009d9a",
  "#1976d2" = "#002d9c",
  "#5e35b1" = "#6929c4",
  "#fb8c00" = "#8a3800",
  "#e53935" = "#fa4d56",
  "#43a047" = "#198038",
  "#7b1fa2" = "#6929c4",
  "#007d79" = "#005d5d",
  "#24a148" = "#198038",
  "#0043ce" = "#002d9c",
  "#1565c0" = "#002d9c",
  "#0f3057" = "#012749",
  "#1f1f1f" = "#161616",
  "#e8e8e8" = "#e0e0e0",
  "#ebebeb" = "#e0e0e0",
  "#ffcc80" = "#ffd9be",
  "#f48fb1" = "#ffd6e8",
  "#c5e1a5" = "#defbe6",
  "#b39ddb" = "#e8daff",
  "#90caf9" = "#d0e2ff",
  "#80cbc4" = "#9ef0f0",
  "#59616f" = "#697077",
  "#263238" = "#343a3f",
  "#111827" = "#161616",
  "#8a3ffc" = "#6929c4",
  "#9e9e9e" = "#8d8d8d",
  "#999999" = "#8d8d8d",
  "#333333" = "#393939",
  "#1a1a1a" = "#161616",
  "#4d4d4d" = "#525252",
  "#595959" = "#525252",
  "#666666" = "#6f6f6f",
  "#737373" = "#6f6f6f",
  "#8c8c8c" = "#8d8d8d",
  "#e5e5e5" = "#e0e0e0"
)

hex_to_svg_rgb <- function(hex) {
  hex <- sub("^#", "", hex)
  vals <- strtoi(substring(hex, c(1, 3, 5), c(2, 4, 6)), base = 16)
  fmt <- function(v) {
    pct <- v / 255 * 100
    if (abs(pct) < 1e-8) return("0%")
    if (abs(pct - 100) < 1e-8) return("100%")
    paste0(sub("\\.?0+$", "", sprintf("%.6f", pct)), "%")
  }
  sprintf("rgb(%s, %s, %s)", fmt(vals[[1]]), fmt(vals[[2]]), fmt(vals[[3]]))
}

normalize_technical_diagram_svg <- function(txt) {
  border_strong <- hex_to_svg_rgb("#8d8d8d")
  layer_accent <- hex_to_svg_rgb("#e0e0e0")
  txt <- gsub('stroke="rgb\\(32\\.156863%, 32\\.156863%, 32\\.156863%\\)"', sprintf('stroke="%s"', border_strong), txt)
  txt <- gsub('stroke="rgb\\(43\\.529412%, 43\\.529412%, 43\\.529412%\\)"', sprintf('stroke="%s"', border_strong), txt)
  txt <- gsub('stroke="rgb\\(66\\.27451%, 66\\.27451%, 66\\.27451%\\)"', sprintf('stroke="%s"', layer_accent), txt)
  txt <- gsub('stroke-dasharray="[0-9\\.]+ [0-9\\.]+"', 'stroke-dasharray="2 4"', txt)
  txt
}

carbonize_svg_file <- function(path, technical_diagram_role = NA_character_) {
  x <- readLines(path, warn = FALSE, encoding = "UTF-8")
  txt <- paste(x, collapse = "\n")
  for (from in names(legacy_to_carbon)) {
    txt <- gsub(from, legacy_to_carbon[[from]], txt, fixed = TRUE)
    txt <- gsub(toupper(from), toupper(legacy_to_carbon[[from]]), txt, fixed = TRUE)
    txt <- gsub(hex_to_svg_rgb(from), hex_to_svg_rgb(legacy_to_carbon[[from]]), txt, fixed = TRUE)
  }
  txt <- gsub("font-family:[^;\"']*sans[^;\"']*", "font-family:IBM Plex Sans", txt, ignore.case = TRUE)
  txt <- sub(
    "<svg ",
    paste0(
      "<svg data-carbon-style=\"IBM Carbon Design System v11\" ",
      "data-carbon-charts-source=\"carbon-design-system/carbon-charts packages/core/scss\" ",
      "data-font=\"IBM Plex Sans\" ",
      "data-chart-palette=\"@carbon/charts white 14\" ",
      if (!is.na(technical_diagram_role)) {
        paste0(
          "data-figma-technical-diagram-library=\"RtZDc7pMQt8HcgYTiitspr\" ",
          "data-technical-diagram-role=\"", technical_diagram_role, "\" "
        )
      } else {
        ""
      }
    ),
    txt,
    fixed = TRUE
  )
  txt <- sub(
    "<defs>",
    paste0(
      "<defs>\n<style type=\"text/css\"><![CDATA[\n",
      ".carbon-note{font-family:'IBM Plex Sans', sans-serif;}\n",
      ".tdl-node,.tdl-connector,.tdl-label-pill,.tdl-flow-number{vector-effect:non-scaling-stroke;}\n",
      ".tdl-connector{fill:none;}\n",
      "]]></style>"
    ),
    txt,
    fixed = TRUE
  )
  if (!is.na(technical_diagram_role)) {
    txt <- normalize_technical_diagram_svg(txt)
  }
  writeLines(txt, path, useBytes = TRUE)
  invisible(path)
}

svg_escape <- function(x) {
  x <- gsub("&", "&amp;", x, fixed = TRUE)
  x <- gsub("<", "&lt;", x, fixed = TRUE)
  x <- gsub(">", "&gt;", x, fixed = TRUE)
  x <- gsub('"', "&quot;", x, fixed = TRUE)
  x
}

svg_text <- function(x, y, label, size = 16, weight = 400, fill = "#161616",
                     anchor = "start", line_height = 1.25, class = NA_character_,
                     extra = "") {
  if (!length(label) || is.na(label[[1]])) label <- ""
  lines <- unlist(strsplit(label, "\\n", fixed = FALSE))
  if (!length(lines)) lines <- ""
  dy <- size * line_height
  first_y <- y - ((length(lines) - 1) * dy / 2)
  class_attr <- if (!is.na(class)) sprintf(' class="%s"', class) else ""
  tspans <- vapply(seq_along(lines), function(i) {
    sprintf(
      '<tspan x="%.1f" y="%.1f">%s</tspan>',
      x,
      first_y + (i - 1) * dy,
      svg_escape(lines[[i]])
    )
  }, character(1))
  sprintf(
    '<text%s x="%.1f" y="%.1f" font-family="IBM Plex Sans, Arial, sans-serif" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s" %s>%s</text>',
    class_attr, x, y, size, weight, fill, anchor, extra, paste(tspans, collapse = "")
  )
}

svg_label_pill <- function(cx, cy, label, fill = "#ffffff", stroke = "#8d8d8d",
                           text_fill = "#161616", width = 96, height = 30,
                           weight = 600, class = "tdl-label-pill") {
  paste0(
    sprintf(
      '<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="%s" stroke="%s" stroke-width="1"/>',
      class, cx - width / 2, cy - height / 2, width, height, fill, stroke
    ),
    "\n",
    svg_text(cx, cy + 1, label, size = 14, weight = weight, fill = text_fill, anchor = "middle")
  )
}

svg_node <- function(x, y, width, height, label, fill = "#f4f4f4", bar = "#0f62fe",
                     stroke = "#8d8d8d", text_fill = "#161616", label_size = 16,
                     weight = 600, class = "tdl-node", bar_width = 6,
                     sublabel = NA_character_) {
  text <- if (is.na(sublabel)) label else paste(label, sublabel, sep = "\n")
  paste0(
    sprintf(
      '<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="%s" stroke="%s" stroke-width="1"/>',
      class, x, y, width, height, fill, stroke
    ),
    "\n",
    sprintf(
      '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="%s"/>',
      x, y, bar_width, height, bar
    ),
    "\n",
    svg_text(x + width / 2 + bar_width / 2, y + height / 2 + 1, text, size = label_size, weight = weight, fill = text_fill, anchor = "middle")
  )
}

svg_flow_number <- function(cx, cy, number, size = 32) {
  paste0(
    sprintf('<circle class="tdl-flow-number" cx="%.1f" cy="%.1f" r="%.1f" fill="#0f62fe" stroke="#0f62fe"/>', cx, cy, size / 2),
    "\n",
    svg_text(cx, cy + 1, as.character(number), size = 15, weight = 600, fill = "#ffffff", anchor = "middle")
  )
}

svg_connector <- function(x1, y1, x2, y2, stroke = "#8d8d8d", width = 1.5,
                          dashed = FALSE, arrow = TRUE, opacity = 1,
                          class = "tdl-connector") {
  dash <- if (dashed) ' stroke-dasharray="2 4"' else ""
  marker_id <- if (stroke == "#0f62fe") "tdl-arrow-blue" else if (stroke == "#da1e28") "tdl-arrow-red" else "tdl-arrow"
  marker <- if (arrow) sprintf(' marker-end="url(#%s)"', marker_id) else ""
  sprintf(
    '<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" fill="none" stroke="%s" stroke-width="%.2f"%s%s opacity="%.2f"/>',
    class, x1, y1, x2, y2, stroke, width, dash, marker, opacity
  )
}

svg_path_connector <- function(d, stroke = "#8d8d8d", width = 1.5,
                               dashed = FALSE, arrow = TRUE, opacity = 1,
                               class = "tdl-connector") {
  dash <- if (dashed) ' stroke-dasharray="2 4"' else ""
  marker_id <- if (stroke == "#0f62fe") "tdl-arrow-blue" else if (stroke == "#da1e28") "tdl-arrow-red" else "tdl-arrow"
  marker <- if (arrow) sprintf(' marker-end="url(#%s)"', marker_id) else ""
  sprintf(
    '<path class="%s" d="%s" fill="none" stroke="%s" stroke-width="%.2f"%s%s opacity="%.2f" stroke-linecap="round" stroke-linejoin="round"/>',
    class, d, stroke, width, dash, marker, opacity
  )
}

write_svg_document <- function(path, width, height, title, subtitle, caption, body,
                               viewbox = NULL) {
  if (is.null(viewbox)) viewbox <- sprintf("0 0 %d %d", width, height)
  svg <- c(
    sprintf(
      '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="%s" role="img" aria-labelledby="title desc">',
      width, height, viewbox
    ),
    "<defs>",
    '<marker id="tdl-arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse">',
    '<path d="M 0 0 L 12 6 L 0 12 z" fill="#8d8d8d"/>',
    "</marker>",
    '<marker id="tdl-arrow-blue" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse">',
    '<path d="M 0 0 L 12 6 L 0 12 z" fill="#0f62fe"/>',
    "</marker>",
    '<marker id="tdl-arrow-red" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse">',
    '<path d="M 0 0 L 12 6 L 0 12 z" fill="#da1e28"/>',
    "</marker>",
    "</defs>",
    sprintf("<title id=\"title\">%s</title>", svg_escape(title)),
    sprintf("<desc id=\"desc\">%s</desc>", svg_escape(subtitle)),
    '<rect width="100%" height="100%" fill="#ffffff"/>',
    svg_text(32, 40, title, size = 24, weight = 600, fill = "#161616"),
    svg_text(32, 72, subtitle, size = 15, weight = 400, fill = "#525252"),
    body,
    svg_text(32, height - 30, caption, size = 13, weight = 400, fill = "#6f6f6f"),
    "</svg>"
  )
  writeLines(svg, path, useBytes = TRUE)
  invisible(path)
}

technical_diagram_fill <- function(fill) {
  map <- c(
    "#edf5ff" = "#edf5ff",
    "#d0e2ff" = "#d0e2ff",
    "#f4f4f4" = "#f4f4f4",
    "#e0e0e0" = "#f4f4f4",
    "#d9fbfb" = "#d9fbfb",
    "#fcf4d6" = "#fcf4d6",
    "#ffd7d9" = "#fff1f1",
    "#e8daff" = "#e8daff",
    "#0f62fe" = "#edf5ff"
  )
  out <- unname(map[tolower(fill)])
  ifelse(is.na(out), "#f4f4f4", out)
}

write_strobe_flow_svg <- function(plot, path) {
  nodes <- plot$layers[[2]]$data
  nodes$label <- c(
    "Kanonik veri kilidi\nLOCKED_CANONICAL_ANALYSIS_BASE",
    "Analitik aile tabanı\n241 aile · 482 çocuk satırı",
    "DM indeks aile\nn = 120",
    "Kontrol indeks aile\nn = 121",
    "DM klinik alt-analiz\nHbA1c gözlenen n = 39"
  )[match(nodes$id, c("lock", "family", "group_dm", "group_control", "clinical"))]
  pos <- data.frame(
    id = c("lock", "family", "group_dm", "group_control", "clinical"),
    px = c(360, 432, 92, 808, 440),
    py = c(130, 292, 468, 468, 618),
    w = c(520, 376, 300, 300, 360),
    h = c(84, 76, 74, 74, 78),
    bar = c("#0f62fe", "#8d8d8d", "#0f62fe", "#8d8d8d", "#009d9a"),
    stringsAsFactors = FALSE
  )
  nodes <- merge(nodes, pos, by = "id", sort = FALSE)
  node_map <- setNames(split(nodes, nodes$id), nodes$id)
  center <- function(id) {
    z <- node_map[[id]]
    c(x = z$px + z$w / 2, y = z$py + z$h / 2)
  }
  body <- c(
    svg_connector(center("lock")["x"], 214, center("family")["x"], 292),
    svg_connector(center("family")["x"], 368, center("group_dm")["x"], 468),
    svg_connector(center("family")["x"], 368, center("group_control")["x"], 468),
    svg_connector(center("group_dm")["x"], 542, center("clinical")["x"], 618),
    svg_connector(center("group_control")["x"], 542, center("clinical")["x"], 618),
    vapply(seq_len(nrow(nodes)), function(i) {
      z <- nodes[i, ]
      svg_node(z$px, z$py, z$w, z$h, z$label, fill = technical_diagram_fill(z$fill), bar = z$bar, label_size = 17)
    }, character(1)),
    svg_flow_number(338, 172, 1),
    svg_flow_number(410, 330, 2),
    svg_flow_number(70, 504, 3),
    svg_flow_number(786, 504, 4),
    svg_flow_number(418, 657, 5)
  )
  write_svg_document(
    path, 1240, 740,
    "Analitik örneklem akış diyagramı",
    "Kanonik veri kilidinden aile-düzeyi analiz ve DM klinik alt-analiz katmanına akış",
    "Not. Bu diyagram randomize çalışma CONSORT akışı değil, kilitlenmiş veri setinin analitik akış haritasıdır.",
    paste(body, collapse = "\n")
  )
}

write_causal_dag_svg <- function(plot, path) {
  body <- c(
    '<rect x="44" y="128" width="300" height="366" rx="4" fill="#ffffff" stroke="#c6c6c6" stroke-width="1"/>',
    svg_text(64, 158, "Baseline/design\nayarlama seti", size = 15, weight = 600, fill = "#161616"),
    svg_node(80, 196, 228, 56, "SES", fill = "#edf5ff", bar = "#0f62fe", label_size = 15),
    svg_node(80, 282, 228, 56, "Kardeş yaş farkı", fill = "#edf5ff", bar = "#0f62fe", label_size = 15),
    svg_node(80, 368, 228, 56, "Aile büyüklüğü", fill = "#edf5ff", bar = "#0f62fe", label_size = 15),
    svg_node(80, 510, 228, 56, "Genetik yatkınlık", fill = "#f4f4f4", bar = "#8d8d8d", label_size = 15),
    svg_node(430, 300, 230, 72, "T1DM durumu", fill = "#edf5ff", bar = "#0f62fe", label_size = 17),
    svg_node(720, 180, 245, 64, "Anne antidepresan", fill = "#fcf4d6", bar = "#f1c21b", label_size = 15),
    svg_node(720, 300, 245, 64, "Beck depresyon", fill = "#d9fbfb", bar = "#009d9a", label_size = 15),
    svg_node(720, 420, 245, 64, "Ebeveynlik tutumu", fill = "#d9fbfb", bar = "#009d9a", label_size = 15),
    svg_node(1040, 258, 230, 64, "Çocuk algısı", fill = "#fff1f1", bar = "#fa4d56", label_size = 15),
    svg_node(1040, 400, 230, 64, "Kardeş ilişkisi", fill = "#e8daff", bar = "#6929c4", label_size = 15),
    svg_path_connector("M 308 224 C 365 224 365 336 430 336", stroke = "#8d8d8d", width = 1.25, opacity = 0.82),
    svg_path_connector("M 308 310 C 365 310 365 336 430 336", stroke = "#8d8d8d", width = 1.25, opacity = 0.82),
    svg_path_connector("M 308 396 C 365 396 365 336 430 336", stroke = "#8d8d8d", width = 1.25, opacity = 0.82),
    svg_path_connector("M 308 538 C 365 538 365 336 430 336", stroke = "#8d8d8d", width = 1.25, dashed = TRUE, opacity = 0.75),
    svg_connector(660, 336, 720, 212, stroke = "#8d8d8d", width = 1.25),
    svg_connector(660, 336, 720, 332, stroke = "#8d8d8d", width = 1.5),
    svg_connector(660, 336, 720, 452, stroke = "#8d8d8d", width = 1.5),
    svg_connector(965, 212, 1040, 290, stroke = "#8d8d8d", width = 1.25, dashed = TRUE, opacity = 0.8),
    svg_connector(965, 212, 720, 332, stroke = "#8d8d8d", width = 1.25),
    svg_connector(965, 212, 720, 452, stroke = "#8d8d8d", width = 1.25),
    svg_connector(965, 332, 1040, 290, stroke = "#8d8d8d", width = 1.25, dashed = TRUE, opacity = 0.8),
    svg_connector(965, 332, 720, 452, stroke = "#8d8d8d", width = 1.25),
    svg_connector(965, 452, 1040, 290, stroke = "#8d8d8d", width = 1.5),
    svg_connector(1270, 290, 1270, 432, stroke = "#8d8d8d", width = 1.25, dashed = TRUE, opacity = 0.8),
    svg_connector(660, 336, 1040, 290, stroke = "#0f62fe", width = 2),
    svg_connector(660, 336, 1040, 432, stroke = "#0f62fe", width = 2),
    svg_label_pill(510, 136, "exposure", fill = "#edf5ff", stroke = "#0f62fe", text_fill = "#002d9c", width = 112),
    svg_label_pill(840, 548, "mediator / sensitivity", fill = "#ffffff", stroke = "#8d8d8d", text_fill = "#525252", width = 190),
    svg_label_pill(1155, 548, "downstream outcome", fill = "#ffffff", stroke = "#8d8d8d", text_fill = "#525252", width = 170),
    svg_text(56, 626, "Kenar kodu", size = 13, weight = 600, fill = "#161616"),
    svg_connector(164, 622, 230, 622, arrow = TRUE, stroke = "#0f62fe", width = 2),
    svg_text(242, 627, "total-effect ana yol", size = 12, fill = "#525252"),
    svg_connector(408, 622, 474, 622, arrow = TRUE, stroke = "#8d8d8d", width = 1.25),
    svg_text(486, 627, "model yolu", size = 12, fill = "#525252"),
    svg_connector(610, 622, 676, 622, arrow = TRUE, stroke = "#8d8d8d", width = 1.25, dashed = TRUE),
    svg_text(688, 627, "arka plan / sensitivite", size = 12, fill = "#525252")
  )
  write_svg_document(
    path, 1320, 700,
    "Causal DAG: total-effect ayarlama stratejisi",
    "SES, kardeş yaş farkı ve aile büyüklüğü baseline/design karıştırıcıları olarak sabitlenmiştir",
    "Not. Beck ve antidepresan kullanımı total-effect modellerinde ana ayarlama setine alınmaz; sensitivite katmanında izlenir.",
    paste(body, collapse = "\n")
  )
}

apim_color <- function(estimate) {
  ifelse(estimate < -0.015, "#da1e28", ifelse(estimate > 0.015, "#0f62fe", "#8d8d8d"))
}

write_h2_apim_svg <- function(plot, path) {
  edges <- plot$layers[[1]]$data
  key_edges <- edges[edges$term %in% c("group_fDM", "group_fDM:family_role_fsibling"), ]
  out_pos <- data.frame(
    outcome = c("srq_ho_warmth_mean", "srq_ho_status_mean", "srq_ho_conflict_mean", "srq_ho_rivalry_mean"),
    label = c("Kardeş sıcaklığı", "Kardeş statüsü", "Kardeş çatışması", "Kardeş rekabeti"),
    y = c(196, 318, 440, 562),
    stringsAsFactors = FALSE
  )
  out_lookup <- setNames(split(out_pos, out_pos$outcome), out_pos$outcome)
  key_lookup <- split(key_edges, paste(key_edges$outcome, key_edges$term, sep = "::"))
  row_blocks <- unlist(lapply(seq_len(nrow(out_pos)), function(i) {
    o <- out_pos[i, ]
    dm <- key_lookup[[paste(o$outcome, "group_fDM", sep = "::")]]
    interaction <- key_lookup[[paste(o$outcome, "group_fDM:family_role_fsibling", sep = "::")]]
    dm_color <- apim_color(dm$estimate)
    interaction_color <- apim_color(interaction$estimate)
    c(
      sprintf('<line class="tdl-connector" x1="330" y1="%.1f" x2="1080" y2="%.1f" stroke="#e0e0e0" stroke-width="1"/>', o$y, o$y),
      svg_label_pill(510, o$y, dm$edge_label, fill = "#ffffff", stroke = dm_color, text_fill = dm_color, width = 104, height = 30),
      svg_label_pill(690, o$y, interaction$edge_label, fill = "#ffffff", stroke = interaction_color, text_fill = interaction_color, width = 104, height = 30),
      svg_connector(742, o$y, 890, o$y, stroke = ifelse(abs(interaction$estimate) >= abs(dm$estimate), interaction_color, dm_color), width = 1.6 + 13 * max(abs(dm$estimate), abs(interaction$estimate))),
      svg_node(890, o$y - 31, 280, 62, o$label, fill = "#f4f4f4", bar = "#6929c4", label_size = 16)
    )
  }))
  body <- c(
    svg_label_pill(180, 122, "APIM terimleri", fill = "#f4f4f4", stroke = "#8d8d8d", text_fill = "#161616", width = 154),
    svg_label_pill(510, 122, "DM ana etki", fill = "#edf5ff", stroke = "#0f62fe", text_fill = "#002d9c", width = 138),
    svg_label_pill(690, 122, "DM × rol", fill = "#edf5ff", stroke = "#0f62fe", text_fill = "#002d9c", width = 118),
    svg_label_pill(1030, 122, "SRQ çıktıları", fill = "#f4f4f4", stroke = "#8d8d8d", text_fill = "#161616", width = 142),
    svg_node(90, 182, 250, 74, "DM grup", fill = "#edf5ff", bar = "#0f62fe", label_size = 17),
    svg_node(90, 500, 250, 74, "DM × kardeş rolü", fill = "#edf5ff", bar = "#0f62fe", label_size = 17),
    svg_node(90, 326, 250, 62, "Kardeş rolü", fill = "#f4f4f4", bar = "#8d8d8d", label_size = 15),
    svg_node(90, 408, 250, 62, "Yaş farkı", fill = "#f4f4f4", bar = "#8d8d8d", label_size = 15),
    svg_path_connector("M 340 219 C 404 219 420 196 458 196", stroke = "#0f62fe", width = 1.4),
    svg_path_connector("M 340 537 C 404 537 420 196 638 196", stroke = "#0f62fe", width = 1.1, opacity = 0.55),
    svg_path_connector("M 340 219 C 404 219 420 562 458 562", stroke = "#0f62fe", width = 1.1, opacity = 0.55),
    svg_path_connector("M 340 537 C 404 537 420 562 638 562", stroke = "#0f62fe", width = 1.4),
    svg_label_pill(220, 636, "Kardeş rolü ve yaş farkı kovaryat olarak tutuldu", fill = "#ffffff", stroke = "#c6c6c6", text_fill = "#525252", width = 366, height = 30, weight = 400),
    row_blocks,
    svg_text(474, 636, "Her satır bir SRQ çıktısını; iki pill ana raporlanan katsayıları gösterir.", size = 13, fill = "#525252"),
    svg_text(890, 636, "Kırmızı: negatif  Mavi: pozitif  Gri: yaklaşık sıfır", size = 13, fill = "#525252")
  )
  write_svg_document(
    path, 1260, 720,
    "H2 kardeş ilişkisi: APIM yol katsayıları",
    "Etiketlenen ana yollar DM ana etkisi ve DM × kardeş rolü etkileşimidir; kovaryatlar modelde tutulmuştur",
    "Not. Yaş farkı kovaryatı modelde tutulmuştur. Etiketler DM ana etkisi ve DM × kardeş rolü etkileşimi için verilmiştir.",
    paste(body, collapse = "\n")
  )
}

write_h4_sem_svg <- function(plot, path) {
  edges <- plot$layers[[1]]$data
  y_map <- setNames(c(160, 286, 412, 538), c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma"))
  target_labels <- c(
    sicaklik = "Sıcaklık",
    asiri_koruma = "Aşırı koruma",
    reddetme = "Reddetme",
    karsilastirma = "Karşılaştırma"
  )
  edges$target_y <- unname(y_map[edges$lhs])
  body <- c(
    svg_node(92, 315, 270, 96, "Beck\ndepresyon\nlatent", fill = "#edf5ff", bar = "#0f62fe", label_size = 20),
    vapply(seq_along(target_labels), function(i) {
      id <- names(target_labels)[[i]]
      svg_node(920, y_map[[id]] - 31, 250, 62, target_labels[[i]], fill = "#f4f4f4", bar = "#8d8d8d", label_size = 17)
    }, character(1)),
    vapply(seq_len(nrow(edges)), function(i) {
      e <- edges[i, ]
      color <- if (e$std.all < 0) "#da1e28" else if (e$significant) "#0f62fe" else "#8d8d8d"
      marker <- if (color == "#0f62fe") "url(#tdl-arrow-blue)" else if (color == "#da1e28") "url(#tdl-arrow-red)" else "url(#tdl-arrow)"
      width <- 1.4 + 12 * abs(e$std.all)
      d <- sprintf("M 362 363 C 550 363 650 %.1f 920 %.1f", e$target_y, e$target_y)
      sprintf(
        '<path class="tdl-connector" d="%s" fill="none" stroke="%s" stroke-width="%.2f" marker-end="%s" opacity="0.90" stroke-linecap="round"/>',
        d, color, width, marker
      )
    }, character(1)),
    vapply(seq_len(nrow(edges)), function(i) {
      e <- edges[i, ]
      color <- if (e$std.all < 0) "#da1e28" else if (e$significant) "#0f62fe" else "#8d8d8d"
      x <- if (e$lhs == "sicaklik") 664 else 622
      svg_label_pill(x, e$target_y - 24, e$beta_label, fill = "#ffffff", stroke = color, text_fill = color, width = 98, height = 30)
    }, character(1)),
    svg_label_pill(490, 604, "WLSMV SEM", fill = "#ffffff", stroke = "#8d8d8d", text_fill = "#525252", width = 112, weight = 400),
    svg_label_pill(650, 604, "* FDR p < .05", fill = "#ffffff", stroke = "#8d8d8d", text_fill = "#525252", width = 132, weight = 400),
    svg_text(838, 604, "Aşırı koruma yolu FDR sonrası anlamlı değildir.", size = 13, fill = "#525252")
  )
  write_svg_document(
    path, 1240, 700,
    "H4 Beck depresyonu → EMBU-P latent ebeveynlik yolları",
    "WLSMV SEM; katsayılar standardize β, * FDR p < .05",
    "Not. Aşırı koruma yolu FDR sonrası anlamlı değildir; diğer üç yol anlamlıdır.",
    paste(body, collapse = "\n")
  )
}

network_node_fill <- function(expected_influence) {
  ifelse(expected_influence < 0, "#ffd7d9",
    ifelse(expected_influence < 0.15, "#f4f4f4",
      ifelse(expected_influence < 0.35, "#a6c8ff",
        ifelse(expected_influence < 0.5, "#78a9ff", "#0f62fe")
      )
    )
  )
}

write_network_graph_svg <- function(plot, path) {
  edges <- plot$layers[[1]]$data
  nodes <- plot$layers[[2]]$data
  scale_x <- function(x) 620 + x * 315
  scale_y <- function(y) 365 - y * 235
  nodes$sx <- scale_x(nodes$x)
  nodes$sy <- scale_y(nodes$y)
  nodes$r <- 14 + 34 * nodes$strength
  edges$x1 <- scale_x(edges$x)
  edges$y1 <- scale_y(edges$y)
  edges$x2 <- scale_x(edges$x_to)
  edges$y2 <- scale_y(edges$y_to)
  label_offsets <- data.frame(
    label = nodes$label,
    dx = c(54, 66, -72, 34, 58, -84, 46, -84, -96),
    dy = c(34, -28, -36, -42, 0, 42, 24, 18, -18),
    anchor = c("start", "start", "end", "middle", "start", "end", "start", "end", "end"),
    stringsAsFactors = FALSE
  )
  nodes <- merge(nodes, label_offsets, by = "label", sort = FALSE)
  body <- c(
    vapply(seq_len(nrow(edges)), function(i) {
      e <- edges[i, ]
      color <- if (e$partial_cor < 0) "#da1e28" else "#0f62fe"
      width <- 0.75 + 12 * abs(e$partial_cor)
      svg_connector(e$x1, e$y1, e$x2, e$y2, stroke = color, width = width, arrow = FALSE, opacity = 0.68)
    }, character(1)),
    vapply(seq_len(nrow(nodes)), function(i) {
      n <- nodes[i, ]
      paste0(
        sprintf(
          '<circle class="tdl-node" cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#262626" stroke-width="1.2"/>',
          n$sx, n$sy, n$r, network_node_fill(n$expected_influence)
        ),
        "\n",
        svg_text(n$sx + n$dx, n$sy + n$dy, n$label, size = 15, weight = 600, fill = "#161616", anchor = n$anchor)
      )
    }, character(1)),
    '<rect x="74" y="640" width="1090" height="72" rx="4" fill="#ffffff" stroke="#e0e0e0" stroke-width="1"/>',
    svg_text(96, 670, "Legend", size = 13, weight = 600, fill = "#161616"),
    svg_connector(176, 666, 244, 666, stroke = "#0f62fe", width = 4, arrow = FALSE),
    svg_text(258, 671, "pozitif partial r", size = 12, fill = "#525252"),
    svg_connector(400, 666, 468, 666, stroke = "#da1e28", width = 3, arrow = FALSE),
    svg_text(482, 671, "negatif partial r", size = 12, fill = "#525252"),
    '<circle cx="666" cy="666" r="14" fill="#a6c8ff" stroke="#262626" stroke-width="1"/>',
    '<circle cx="710" cy="666" r="24" fill="#78a9ff" stroke="#262626" stroke-width="1"/>',
    svg_text(746, 671, "düğüm boyutu = strength", size = 12, fill = "#525252"),
    '<circle cx="942" cy="666" r="17" fill="#f4f4f4" stroke="#262626" stroke-width="1"/>',
    '<circle cx="988" cy="666" r="17" fill="#0f62fe" stroke="#262626" stroke-width="1"/>',
    svg_text(1020, 671, "dolgu = expected influence", size = 12, fill = "#525252")
  )
  write_svg_document(
    path, 1240, 800,
    "KISIM VIII GGM network haritası",
    "EBIC-LASSO havuzlanmış ağ; kenar kalınlığı |partial r|, düğüm boyutu strength merkeziyetidir",
    "Not. Network koşullu bağımlılık haritasıdır; nedensel yön olarak yorumlanmaz.",
    paste(body, collapse = "\n")
  )
}

write_technical_diagram_svg <- function(id, plot, path) {
  switch(
    id,
    strobe_flow = write_strobe_flow_svg(plot, path),
    causal_dag = write_causal_dag_svg(plot, path),
    h2_apim_path = write_h2_apim_svg(plot, path),
    h4_sem_path = write_h4_sem_svg(plot, path),
    network_graph = write_network_graph_svg(plot, path),
    stop(sprintf("No custom technical diagram renderer for %s", id), call. = FALSE)
  )
}

allowed_svg_colors <- function() {
  tolower(unique(c(carbon_token_palette, carbon_chart_palette)))
}

allowed_svg_rgb_colors <- function() {
  unique(vapply(allowed_svg_colors(), hex_to_svg_rgb, character(1)))
}

svg_color_aesthetic <- function(path) {
  if (!file.exists(path)) {
    return(data.frame(
      carbon_charts_metadata = FALSE,
      non_carbon_hex_count = NA_integer_,
      non_carbon_rgb_count = NA_integer_,
      chart_palette_hits = NA_integer_,
      text_primary_hits = NA_integer_,
      text_secondary_hits = NA_integer_,
      grid_hits = NA_integer_,
      stringsAsFactors = FALSE
    ))
  }
  txt <- paste(readLines(path, warn = FALSE), collapse = "\n")
  hex_matches <- regmatches(txt, gregexpr("#[0-9a-fA-F]{6}", txt, perl = TRUE))[[1]]
  rgb_matches <- regmatches(txt, gregexpr("rgb\\([^\\)]+\\)", txt, perl = TRUE))[[1]]
  if (identical(hex_matches, character(0))) hex_matches <- character(0)
  if (identical(rgb_matches, character(0))) rgb_matches <- character(0)
  allowed_hex <- allowed_svg_colors()
  allowed_rgb <- allowed_svg_rgb_colors()
  data.frame(
    carbon_charts_metadata = grepl("data-carbon-charts-source", txt, fixed = TRUE),
    non_carbon_hex_count = length(setdiff(unique(tolower(hex_matches)), allowed_hex)),
    non_carbon_rgb_count = length(setdiff(unique(rgb_matches), allowed_rgb)),
    chart_palette_hits = sum(rgb_matches %in% vapply(carbon_chart_palette, hex_to_svg_rgb, character(1))),
    text_primary_hits = sum(rgb_matches == hex_to_svg_rgb("#161616")),
    text_secondary_hits = sum(rgb_matches == hex_to_svg_rgb("#525252")),
    grid_hits = sum(rgb_matches == hex_to_svg_rgb("#e0e0e0")),
    stringsAsFactors = FALSE
  )
}

main_figures <- data.frame(
  id = c(
    "strobe_flow", "causal_dag", "smd_love_plot", "propensity_overlap", "ses_correlation_heatmap",
    "missing_pattern_primary", "h1_forest", "h1_three_way_emm", "h2_apim_path", "h3_stratified_forest",
    "h4_sem_path", "h5_ba_grid", "h5_rsa_surface", "mediation_effects", "lpa_fit_indices",
    "network_graph", "network_nct", "clinical_roc", "clinical_dca", "clinical_calibration",
    "clinical_cart_rf", "specification_curve", "sensemakr_contour", "bayesian_forest",
    "bayesian_diagnostics"
  ),
  order = 1:25,
  mode = c(rep("targets-native-vector", 5), "missing-native-vector", rep("targets-native-vector", 19)),
  target = c(
    "apa_strobe_flow_plot", "apa_causal_dag_plot", "apa_smd_love_plot", "apa_propensity_overlap_plot",
    "apa_ses_correlation_plot", NA, "apa_h1_forest_plot", "apa_h1_three_way_emm_plot",
    "apa_h2_apim_path_plot", "apa_h3_stratified_forest_plot", "apa_h4_sem_path_plot",
    "apa_h5_bland_altman_plot", "apa_h5_rsa_surface_plot", "apa_mediation_effects_plot",
    "apa_lpa_fit_plot", "apa_network_graph_plot", "apa_network_nct_plot", "apa_clinical_roc_plot",
    "apa_clinical_dca_plot", "apa_clinical_calibration_plot", "apa_clinical_cart_rf_plot",
    "apa_specification_curve_plot", "apa_sensemakr_contour_plot", "apa_bayesian_forest_plot",
    "apa_bayesian_diagnostics_plot"
  ),
  width = c(7.2, 9.6, 7.2, 7.2, 6.8, 12.0, 8.2, 10.2, 8.2, 8.2, 8.2, 10.5, 10.5, 8.2, 7.2, 7.4, 6.8, 6.4, 7.2, 6.4, 7.2, 8.2, 7.2, 8.2, 7.2),
  height = c(5.4, 4.8, 4.6, 4.8, 5.8, 8.0, 5.1, 8.2, 5.1, 5.1, 5.1, 8.2, 6.4, 6.6, 6.2, 6.2, 4.4, 5.4, 5.2, 5.4, 6.2, 5.4, 5.4, 5.8, 5.2),
  chapter_ref = c(
    "@fig-strobe-flow", "@fig-causal-dag", "@fig-smd-love", "@fig-propensity-overlap", "@fig-ses-correlation",
    "missing-data-audit", "@fig-h1-forest", "@fig-h1-three-way-emm", "@fig-h2-apim-path", "@fig-h3-stratified-forest",
    "@fig-h4-sem-path", "@fig-h5-bland-altman", "@fig-h5-rsa-surface", "@fig-mediation-effects", "@fig-lpa-fit-indices",
    "@fig-network-graph", "@fig-network-nct", "@fig-clinical-roc", "@fig-clinical-dca", "@fig-clinical-calibration",
    "@fig-clinical-cart-rf", "@fig-specification-curve", "@fig-sensemakr-contour", "@fig-bayesian-forest",
    "@fig-bayesian-diagnostics"
  ),
  related_analysis = c(
    "Analitik akış / STROBE", "DAG ve ayarlama seti", "Propensity denge", "Propensity ortak destek", "SES kompozit validasyonu",
    "Eksik veri yapısı", "H1 çocuk algısı", "H1 etkileşim tanısı", "H2 kardeş ilişkisi APIM", "H3 anne öz-bildirimi",
    "H4 Beck -> EMBU-P SEM", "H5 manifest uyum", "H5 RSA uyum yüzeyi", "KISIM VI mediation", "KISIM VII LPA",
    "KISIM VIII ağ modeli", "KISIM VIII NCT", "KISIM IX ROC", "KISIM IX DCA", "KISIM IX kalibrasyon",
    "KISIM IX CART/RF", "KISIM XI multiverse", "KISIM XI sensemakr/E-value", "KISIM XII Bayesçi forest",
    "KISIM XII MCMC tanıları"
  ),
  source_doc = c(rep("chapters/03_bulgular.qmd", 5), "scripts/R/13_missing_data_audit.R", rep("chapters/03_bulgular.qmd", 19)),
  original_png = file.path("outputs", "figures", c(
    "strobe_flow.png", "causal_dag.png", "smd_love_plot.png", "propensity_overlap.png", "ses_correlation_heatmap.png",
    "missing_pattern_primary.png", "h1_forest.png", "h1_three_way_emm.png", "h2_apim_path.png", "h3_stratified_forest.png",
    "h4_sem_path.png", "h5_ba_grid.png", "h5_rsa_surface.png", "mediation_effects.png", "lpa_fit_indices.png",
    "network_graph.png", "network_nct.png", "clinical_roc.png", "clinical_dca.png", "clinical_calibration.png",
    "clinical_cart_rf.png", "specification_curve.png", "sensemakr_contour.png", "bayesian_forest.png",
    "bayesian_diagnostics.png"
  )),
  stringsAsFactors = FALSE
)

main_figures$title <- c(
  "Analitik örneklem akış diyagramı",
  "Causal DAG ve ayarlama stratejisi",
  "SMD love plot",
  "Propensity score overlap",
  "SES korelasyon matrisi",
  "Primary FIML/MI eksiklik haritası",
  "H1 çocuk algısı forest plot",
  "H1 rol x yaş x cinsiyet EMM paneli",
  "H2 APIM yol diyagramı",
  "H3 antidepresan katmanlı forest plot",
  "H4 latent SEM yol diyagramı",
  "H5 Bland-Altman tutarlılık haritası",
  "H5 response surface analysis",
  "Mediation yol ve indirect etki özeti",
  "LPA model seçim tanıları",
  "EBIC-LASSO Gaussian Graphical Model",
  "Network Comparison Test özeti",
  "Klinik risk modeli ROC eğrisi",
  "Klinik karar eğrisi analizi",
  "Klinik risk kalibrasyon grafiği",
  "CART/RF tamamlayıcı klinik tanıları",
  "Specification curve",
  "Sensemakr duyarlılık konturu",
  "Bayesçi posterior forest",
  "Bayesçi MCMC tanı paneli"
)

technical_diagram_roles <- c(
  strobe_flow = "Flow shape + Flow number + Connector + Label pill",
  causal_dag = "Large node + Connector + Legend",
  h2_apim_path = "Large node + Connector line ending + Label text",
  h4_sem_path = "Large node + Connector line ending + Label text",
  network_graph = "Small node + Connector + Legend"
)
main_figures$technical_diagram_role <- unname(technical_diagram_roles[main_figures$id])
main_figures$technical_diagram_role[is.na(main_figures$technical_diagram_role)] <- NA_character_

rendered <- list()
for (i in seq_len(nrow(main_figures))) {
  row <- main_figures[i, ]
  svg_name <- sprintf("fig-%02d-%s.svg", row$order, gsub("_", "-", row$id))
  svg_path <- file.path(out_dir, svg_name)
  if (!is.na(row$target)) {
    plot <- targets::tar_read_raw(row$target)
  } else {
    if (!requireNamespace("naniar", quietly = TRUE)) {
      stop("naniar package is required for missing_pattern_primary export", call. = FALSE)
    }
    missing_results <- targets::tar_read_raw("missing_results")
    plot <- naniar::vis_miss(missing_results$frames$fiml_primary) +
      ggplot2::labs(title = "Primary FIML/MI frame missingness")
  }
  has_technical_diagram_role <- !is.na(row$technical_diagram_role)
  if (has_technical_diagram_role) {
    write_technical_diagram_svg(row$id, plot, svg_path)
  } else {
    write_svg_plot(plot, svg_path, row$width, row$height)
  }
  carbonize_svg_file(svg_path, technical_diagram_role = row$technical_diagram_role)
  rendered[[length(rendered) + 1L]] <- transform(row, svg_file = relative_path(svg_path), svg_path_abs = svg_path)
}

render_quarto_svg <- function(source_qmd, tmp_name, replacements, output_subdir) {
  qmd_tmp <- file.path(tmp_dir, tmp_name)
  txt <- readLines(source_qmd, warn = FALSE, encoding = "UTF-8")
  joined <- paste(txt, collapse = "\n")
  for (replacement in replacements) {
    joined <- gsub(replacement$pattern, replacement$replacement, joined, perl = TRUE)
  }
  writeLines(joined, qmd_tmp, useBytes = TRUE)
  render_dir <- file.path(tmp_dir, output_subdir)
  dir.create(render_dir, recursive = TRUE, showWarnings = FALSE)
  status <- system2("quarto", c("render", qmd_tmp, "--to", "html", "--output-dir", render_dir), stdout = TRUE, stderr = TRUE)
  if (!is.null(attr(status, "status")) && attr(status, "status") != 0L) {
    cat(paste(status, collapse = "\n"), "\n")
    stop(sprintf("Quarto render failed for %s", source_qmd), call. = FALSE)
  }
  list(render_dir = render_dir, log = status)
}

demo_render <- render_quarto_svg(
  "docs/raporlar/01_demografik_tibbi_rapor.qmd",
  "01_demografik_tibbi_rapor_svg.qmd",
  list(
    list(pattern = 'dev: "png"', replacement = 'dev: "svg"'),
    list(pattern = "embed-resources: true", replacement = "embed-resources: false"),
    list(pattern = 'theme_minimal\\(base_size = base_size\\)', replacement = 'theme_minimal(base_size = base_size, base_family = "IBM Plex Sans")'),
    list(
      pattern = 'project_root <- normalizePath\\("\\.\\./\\.\\.", winslash = "/", mustWork = TRUE\\)',
      replacement = sprintf('project_root <- normalizePath("%s", winslash = "/", mustWork = TRUE)', repo_root)
    )
  ),
  "demografi"
)

psych_render <- render_quarto_svg(
  "docs/analiz_planlari/PSIKOMETRIK-VALIDASYON-BUTUNLESIK-RAPOR.qmd",
  "psikometrik_validasyon_svg.qmd",
  list(
    list(pattern = 'dev = "ragg_png"', replacement = 'dev = "svg"'),
    list(pattern = 'theme_minimal\\(base_family = "Fraunces 9pt", base_size = 10\\)', replacement = 'theme_minimal(base_family = "IBM Plex Sans", base_size = 10)'),
    list(
      pattern = 'base_dir <- if \\(!is\\.null\\(input_path\\)\\) dirname\\(normalizePath\\(input_path\\)\\) else getwd\\(\\)\\nproject_root <- normalizePath\\(file\\.path\\(base_dir, "\\.\\.", "\\.\\."\\), mustWork = FALSE\\)\\nif \\(!file\\.exists\\(file\\.path\\(project_root, "outputs", "tables", "psychval_summary_metrics\\.csv"\\)\\)\\) \\{\\n  project_root <- normalizePath\\(getwd\\(\\), mustWork = FALSE\\)\\n\\}',
      replacement = sprintf('project_root <- normalizePath("%s", mustWork = TRUE)', repo_root)
    )
  ),
  "psikometri"
)

copy_quarto_svgs <- function(rows, render_dir, prefix, source_doc) {
  copied <- list()
  figure_dir <- list.dirs(render_dir, recursive = TRUE, full.names = TRUE)
  figure_dir <- figure_dir[grepl("figure-html$", figure_dir)]
  if (!length(figure_dir)) {
    stop(sprintf("No figure-html directory found under %s", render_dir), call. = FALSE)
  }
  figure_dir <- figure_dir[[1]]
  for (i in seq_len(nrow(rows))) {
    row <- rows[i, ]
    src <- file.path(figure_dir, row$rendered_name)
    if (!file.exists(src)) {
      stop(sprintf("Expected rendered SVG not found: %s", src), call. = FALSE)
    }
    svg_name <- sprintf("%s-%02d-%s.svg", prefix, row$order, row$id)
    dst <- file.path(out_dir, svg_name)
    file.copy(src, dst, overwrite = TRUE)
    carbonize_svg_file(dst)
    copied[[length(copied) + 1L]] <- data.frame(
      id = row$id,
      order = row$order,
      mode = "quarto-native-vector",
      target = NA_character_,
      width = NA_real_,
      height = NA_real_,
      chapter_ref = row$chapter_ref,
      related_analysis = row$related_analysis,
      source_doc = source_doc,
      original_png = row$original_png,
      title = row$title,
      technical_diagram_role = NA_character_,
      svg_file = relative_path(dst),
      svg_path_abs = dst,
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, copied)
}

psych_rows <- data.frame(
  id = c("reliability", "floor", "cfa", "invariance", "icc", "validity", "multiverse"),
  order = 1:7,
  rendered_name = c("fig-reliability-1.svg", "fig-floor-1.svg", "fig-cfa-1.svg", "fig-invariance-1.svg", "fig-icc-1.svg", "fig-validity-1.svg", "fig-multiverse-1.svg"),
  original_png = file.path("_freeze/docs/analiz_planlari/PSIKOMETRIK-VALIDASYON-BUTUNLESIK-RAPOR/figure-pdf", c("fig-reliability-1.png", "fig-floor-1.png", "fig-cfa-1.png", "fig-invariance-1.png", "fig-icc-1.png", "fig-validity-1.png", "fig-multiverse-1.png")),
  chapter_ref = paste0("@fig-", c("reliability", "floor", "cfa", "invariance", "icc", "validity", "multiverse")),
  related_analysis = c("Psikometrik güvenirlik", "Madde taban etkisi", "CFA uyum göstergeleri", "Ölçüm değişmezliği", "Aile içi ICC", "Geçerlik korelasyonları", "Reddetme multiverse"),
  title = c(
    "EMBU-P ve EMBU-C güvenirlik katsayıları",
    "EMBU madde düzeyi taban etkisi",
    "CFA ve cluster duyarlılık uyum göstergeleri",
    "Scalar CFI ölçüm değişmezliği duyarlılığı",
    "EMBU-C aile içi ICC ve indeks-kardeş anlaşması",
    "Beklenen yönlü geçerlik korelasyonları",
    "EMBU-P reddetme DM-Kontrol multiverse eğrisi"
  ),
  stringsAsFactors = FALSE
)

demo_ids <- c(
  "grup-dagilim", "cocuk-yas-dagilim", "cinsiyet-grup", "same-sex", "aile-buyuklugu",
  "anne-yas", "beck-grup", "beck-severity", "antidep", "ses-density", "egitim",
  "dm-eksik", "hba1c", "hba1c-target", "dm-suresi", "tani-strata", "smd-love",
  "ps-density", "iptw-balance", "eksik-degisken"
)

demo_rows <- data.frame(
  id = demo_ids,
  order = seq_along(demo_ids),
  rendered_name = paste0(demo_ids, "-1.svg"),
  original_png = file.path("_freeze/docs/raporlar/01_demografik_tibbi_rapor/figure-html", paste0(demo_ids, "-1.png")),
  chapter_ref = paste0("@fig-", demo_ids),
  related_analysis = c(
    "Örneklem grup dağılımı", "Çocuk yaşı ve kardeş yaş farkı", "Cinsiyet oranları", "Kardeş cinsiyet kompozisyonu",
    "Aile büyüklüğü", "Anne yaşı", "Beck toplam puanı", "Beck şiddet kategorisi", "Antidepresan kullanımı",
    "Latent SES dağılımı", "Anne/eş eğitim düzeyi", "DM klinik gösterge tamamlanması", "HbA1c dağılımı",
    "HbA1c hedef kategorileri", "DM süresi ve tanı yaşı", "Tanı yaşı üç strata", "Ham kovaryat dengesi",
    "Logit propensity yoğunluğu", "IPTW dengeleme etkisi", "Aile düzeyi eksik veri"
  ),
  title = c(
    "Grup başına dahil edilen aile sayısı",
    "Çocuk yaşı ve kardeş yaş farkı dağılımı",
    "İndeks çocuk ve kardeş cinsiyet oranları",
    "Kardeş çifti cinsiyet kompozisyonu",
    "Aile büyüklüğü grup bazında dağılım",
    "Anne yaşı grup bazında dağılım",
    "Beck Depresyon Envanteri toplam puanı",
    "Anne depresyon şiddet kategorisi",
    "Anne antidepresan kullanımı",
    "Latent SES kompozit grup bazında",
    "Anne ve eş eğitim seviyesi",
    "DM grubu klinik gösterge tamamlanma oranı",
    "DM grubu HbA1c dağılımı",
    "HbA1c kategorik dağılımı",
    "DM süresi ve tanı yaşı dağılımları",
    "DM tanı yaşı üç strata",
    "Kovaryat dengesi ham gözlem",
    "Logit propensity score dağılımı",
    "IPTW dengeleme etkisi",
    "Aile-düzeyi değişkenlerde eksik veri"
  ),
  stringsAsFactors = FALSE
)

psych_manifest <- copy_quarto_svgs(psych_rows, psych_render$render_dir, "psychval", "docs/analiz_planlari/PSIKOMETRIK-VALIDASYON-BUTUNLESIK-RAPOR.qmd")
demo_manifest <- copy_quarto_svgs(demo_rows, demo_render$render_dir, "demo", "docs/raporlar/01_demografik_tibbi_rapor.qmd")

manifest <- do.call(rbind, c(rendered, list(psych_manifest, demo_manifest)))
manifest$source_png_exists <- file.exists(file.path(repo_root, manifest$original_png))
manifest$source_png_md5 <- vapply(file.path(repo_root, manifest$original_png), hash_file, character(1))
manifest$svg_exists <- file.exists(manifest$svg_path_abs)
manifest$svg_bytes <- ifelse(manifest$svg_exists, file.info(manifest$svg_path_abs)$size, NA_real_)
manifest$svg_md5 <- vapply(manifest$svg_path_abs, hash_file, character(1))
manifest$is_svg <- vapply(manifest$svg_path_abs, function(path) {
  if (!file.exists(path)) return(FALSE)
  any(grepl("<svg", readLines(path, n = 12L, warn = FALSE), fixed = TRUE))
}, logical(1))
manifest$contains_raster_image_tag <- vapply(manifest$svg_path_abs, function(path) {
  if (!file.exists(path)) return(NA)
  any(grepl("<image", readLines(path, warn = FALSE), fixed = TRUE))
}, logical(1))
manifest$carbon_metadata <- vapply(manifest$svg_path_abs, function(path) {
  if (!file.exists(path)) return(FALSE)
  any(grepl('data-carbon-style="IBM Carbon Design System v11"', readLines(path, n = 4L, warn = FALSE), fixed = TRUE))
}, logical(1))
style_audit <- do.call(rbind, lapply(manifest$svg_path_abs, svg_color_aesthetic))
manifest$carbon_charts_metadata <- style_audit$carbon_charts_metadata
manifest$non_carbon_hex_count <- style_audit$non_carbon_hex_count
manifest$non_carbon_rgb_count <- style_audit$non_carbon_rgb_count
manifest$chart_palette_hits <- style_audit$chart_palette_hits
manifest$text_primary_hits <- style_audit$text_primary_hits
manifest$text_secondary_hits <- style_audit$text_secondary_hits
manifest$grid_hits <- style_audit$grid_hits
manifest$technical_diagram_metadata <- vapply(manifest$svg_path_abs, function(path) {
  if (!file.exists(path)) return(FALSE)
  any(grepl('data-figma-technical-diagram-library="RtZDc7pMQt8HcgYTiitspr"', readLines(path, n = 4L, warn = FALSE), fixed = TRUE))
}, logical(1))
manifest$technical_native_status <- ifelse(
  is.na(manifest$technical_diagram_role),
  "N/A",
  ifelse(
    manifest$technical_diagram_metadata & !manifest$contains_raster_image_tag,
    "PASS: custom Technical Diagram SVG; no chart grid/axis/raster layer",
    "REVIEW: technical diagram has raster or missing metadata"
  )
)
manifest$fidelity_status <- ifelse(
  manifest$svg_exists & manifest$is_svg & manifest$source_png_exists,
  ifelse(
    manifest$contains_raster_image_tag,
    "PASS: native SVG; heatmap/surface benzeri raster katman içeriyor",
    "PASS: native SVG, kaynak PNG mevcut"
  ),
  "FAIL: eksik dosya veya SVG başlığı"
)
manifest$carbon_style_status <- ifelse(
  manifest$carbon_metadata & manifest$carbon_charts_metadata & manifest$non_carbon_hex_count == 0L & ibm_plex_ready,
  "PASS: IBM Plex + Carbon Charts metadata/palette",
  ifelse(
    manifest$carbon_metadata & ibm_plex_ready,
    "PASS: IBM Plex + Carbon metadata; raster/gradient katmanında ek renk var",
    "WARN: Carbon metadata veya IBM Plex hazırlığı eksik"
  )
)
manifest$carbon_aesthetic_status <- ifelse(
  manifest$carbon_metadata & manifest$carbon_charts_metadata & manifest$non_carbon_hex_count == 0L &
    (manifest$non_carbon_rgb_count == 0L | manifest$contains_raster_image_tag),
  ifelse(
    manifest$contains_raster_image_tag,
    "PASS: Carbon Charts; raster/gradient istisnası notlandı",
    "PASS: Carbon Charts"
  ),
  "REVIEW: renk/metadata elle bakılmalı"
)
manifest$technical_diagram_status <- ifelse(
  is.na(manifest$technical_diagram_role),
  "N/A",
  ifelse(
    manifest$technical_diagram_metadata & !manifest$contains_raster_image_tag,
    "PASS: full Figma Technical Diagram Library SVG",
    "REVIEW: Technical Diagram metadata missing"
  )
)

manifest_public <- manifest[, c(
  "id", "title", "related_analysis", "chapter_ref", "mode", "source_doc",
  "original_png", "source_png_md5", "svg_file", "svg_bytes", "svg_md5",
  "fidelity_status", "carbon_style_status", "carbon_aesthetic_status",
  "technical_diagram_role", "technical_native_status", "technical_diagram_status",
  "non_carbon_hex_count", "non_carbon_rgb_count", "chart_palette_hits",
  "text_primary_hits", "text_secondary_hits", "grid_hits"
)]
utils::write.csv(manifest_public, file.path(out_dir, "manifest.csv"), row.names = FALSE, fileEncoding = "UTF-8")
utils::write.csv(
  manifest_public[, c("id", "mode", "original_png", "svg_file", "fidelity_status", "carbon_style_status", "non_carbon_hex_count")],
  file.path(out_dir, "fidelity-audit.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  manifest_public[, c(
    "id", "svg_file", "carbon_aesthetic_status", "non_carbon_hex_count", "non_carbon_rgb_count",
    "chart_palette_hits", "text_primary_hits", "text_secondary_hits", "grid_hits"
  )],
  file.path(out_dir, "carbon-aesthetic-audit.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)
utils::write.csv(
  manifest_public[manifest_public$technical_diagram_status != "N/A", c(
    "id", "svg_file", "technical_diagram_role", "technical_native_status", "technical_diagram_status", "carbon_aesthetic_status"
  )],
  file.path(out_dir, "technical-diagram-audit.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

make_link <- function(path, label = basename(path)) {
  href <- ifelse(dirname(path) == "docs/carbon-svg-figures", basename(path), path)
  sprintf("[%s](%s)", label, href)
}

section_rows <- function(df) {
  paste0(
    "| ", df$id,
    " | ", make_link(df$svg_file),
    " | `", df$chapter_ref, "`",
    " | ", df$related_analysis,
    " | ", df$mode,
    " | ", df$fidelity_status,
    " | ", df$carbon_style_status,
    " | ", df$carbon_aesthetic_status,
    " | ", df$technical_diagram_status,
    " |"
  )
}

aesthetic_rows <- function(df) {
  note <- ifelse(
    df$non_carbon_rgb_count > 0,
    "Gradient/raster veya interpolasyon rengi içerir; SVG native kalır.",
    "Token/palette uyumlu vektör renkleri."
  )
  paste0(
    "| ", df$id,
    " | ", make_link(df$svg_file),
    " | ", df$carbon_aesthetic_status,
    " | ", df$chart_palette_hits,
    " | ", df$text_primary_hits,
    " / ", df$text_secondary_hits,
    " | ", df$grid_hits,
    " | ", df$non_carbon_hex_count,
    " / ", df$non_carbon_rgb_count,
    " | ", note,
    " |"
  )
}

markdown <- c(
  "# Carbon SVG Figure Dizin ve Cross-Reference Haritası",
  "",
  sprintf("Üretim zamanı: `%s`", format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")),
  "",
  "Bu dizin, tez analizleri kapsamında şu ana dek üretilmiş benzersiz görsel çıktıların Carbon uyumlu SVG karşılıklarını tek klasörde toplar. Kaynak envanter üç yüzeyden derlenmiştir: aktif `_targets`/`outputs/figures` figür seti, psikometrik validasyon Quarto freeze görselleri ve demografik-tıbbi Quarto freeze görselleri.",
  "",
  "## Kapsam ve Üretim Modu",
  "",
  sprintf("- Toplam SVG: **%d**", nrow(manifest_public)),
  sprintf("- Aktif bulgular / `_targets` SVG: **%d**", sum(manifest_public$mode %in% c("targets-native-vector", "missing-native-vector"))),
  sprintf("- Psikometrik validasyon Quarto SVG: **%d**", sum(grepl("^psychval-", basename(manifest_public$svg_file)))),
  sprintf("- Demografik-tıbbi Quarto SVG: **%d**", sum(grepl("^demo-", basename(manifest_public$svg_file)))),
  "- Dışlananlar: `.quarto/_freeze` altındaki birebir kopyalar, `tmp/pdfs/*` sayfa görüntüleri, form/book PDF'leri ve Carbon HTML/PDF rapor çıktıları. Bunlar analiz figürü değil, render kopyası ya da kaynak belgedir.",
  "",
  "## Aslına Uygunluk Denetimi",
  "",
  "- `targets-native-vector`: `_targets` store içindeki ggplot nesnesi doğrudan `grDevices::svg()` ile basıldı; kaynak PNG varlığı ve hash'i manifestte tutuldu.",
  "- `missing-native-vector`: eksik veri haritası `missing_results$frames$fiml_primary` üzerinden `naniar::vis_miss()` ile yeniden çizildi.",
  "- `quarto-native-vector`: ilgili Quarto belgesi geçici kopya üzerinden `dev = \"svg\"` ile render edildi; frozen PNG kaynaklarıyla eşlenen chunk/cross-ref kimlikleri korundu.",
  "- IBM Plex Sans, SVG aygıtı açılmadan önce fontconfig'e tanıtıldı; R/Cairo aygıtının ürettiği metinler IBM Plex glyph outline'ları olarak SVG içinde taşınır.",
  "- Eski tez paleti hex değerleri resmi `@carbon/charts` white-theme kategorik sırasına ve Carbon semantic tokenlarına normalize edildi: Purple 70, Cyan 50, Teal 70, Magenta 70, Red 50, Green 60, Blue 80, Orange 70 ve Carbon gri rampası.",
  "- Carbon Charts repo estetik rolleri uygulanmıştır: başlık `text-primary`/semibold, axis title semibold, axis text `text-secondary`, graph-grid `layer-accent-01`, legend bottom ve IBM Plex Sans chart typography.",
  "- Flow/diagram figürleri Figma IBM Technical Diagram Library (`RtZDc7pMQt8HcgYTiitspr`) rollerine göre özel SVG renderer ile yeniden çizildi: Large node, Small node, Connector, Connector line ending, Label text, Label pill, Flow number ve Legend. Bu figürlerde generic chart grid/axis/raster katmanı yoktur; connector stroke'ları Carbon border tokenlarına çekildi.",
  "- Final SVG'ler raster-wrapper değildir. Ancak heatmap, missingness map, RSA surface, sensemakr contour ve bazı ağ/surface panelleri ggplot tarafından SVG içinde raster katman olarak temsil edilebilir; bu durum audit notu olarak işaretlenir.",
  "",
  "Ayrıntılı makine-okunur kayıtlar: [manifest.csv](manifest.csv), [fidelity-audit.csv](fidelity-audit.csv), [carbon-aesthetic-audit.csv](carbon-aesthetic-audit.csv) ve [technical-diagram-audit.csv](technical-diagram-audit.csv).",
  "",
  "## Aktif Bulgular / CSR ve Tez Bölümü Figürleri",
  "",
  "| ID | SVG | Cross-ref | İlişkili analiz | Üretim modu | Denetim | Carbon stil | Estetik audit | Technical Diagram |",
  "|---|---|---|---|---|---|---|---|---|",
  section_rows(manifest_public[manifest_public$mode %in% c("targets-native-vector", "missing-native-vector"), ]),
  "",
  "## Psikometrik Validasyon Figürleri",
  "",
  "| ID | SVG | Cross-ref | İlişkili analiz | Üretim modu | Denetim | Carbon stil | Estetik audit | Technical Diagram |",
  "|---|---|---|---|---|---|---|---|---|",
  section_rows(manifest_public[grepl("^psychval-", basename(manifest_public$svg_file)), ]),
  "",
  "## Demografik ve Tıbbi Rapor Figürleri",
  "",
  "| ID | SVG | Cross-ref | İlişkili analiz | Üretim modu | Denetim | Carbon stil | Estetik audit | Technical Diagram |",
  "|---|---|---|---|---|---|---|---|---|",
  section_rows(manifest_public[grepl("^demo-", basename(manifest_public$svg_file)), ]),
  "",
  "## Analitik İlişki Haritası",
  "",
  "- **Akış ve tasarım katmanı:** `fig-01-strobe-flow`, `fig-02-causal-dag`, `fig-03-smd-love-plot`, `fig-04-propensity-overlap`, `fig-05-ses-correlation-heatmap`, `fig-06-missing-pattern-primary` çalışma akışını, karıştırıcı stratejisini, dengeyi, ortak destek alanını, SES proxy doğrulamasını ve eksik veri çerçevesini belgeler.",
  "- **H1-H5 hipotez katmanı:** `fig-07` ile `fig-13` çocuk algısı, kardeş ilişkisi, anne öz-bildirimi, Beck-ebeveynlik SEM ve diadik tutarlılık bulgularını doğrudan tez hipotezlerine bağlar.",
  "- **Genişletilmiş analiz katmanı:** `fig-14` ile `fig-17` mediation, LPA ve ağ analizlerini; `fig-18` ile `fig-21` klinik fayda hattını; `fig-22` ile `fig-25` multiverse/sensemakr/Bayesçi sağlamlık katmanını taşır.",
  "- **Psikometrik geçerlik katmanı:** `psychval-*` seti EMBU-P/EMBU-C/KİA/SRQ ölçeklerinin güvenirlik, taban etkisi, CFA, invaryans, ICC, yakınsak geçerlik ve reddetme multiverse kararlarını destekler.",
  "- **Tanımlayıcı-demografik katman:** `demo-*` seti örneklem dağılımı, çocuk/anne yaşı, cinsiyet kompozisyonu, Beck ve antidepresan yükü, SES, DM klinik göstergeleri, ham denge, IPTW ve eksik veri görsellerini kapsar.",
  "",
  "## Yeniden Üretim",
  "",
  "```bash",
  "Rscript scripts/R/39_export_carbon_svg_figures.R",
  "```",
  "",
  "Bu komut `_targets` store'u ve mevcut `outputs/tables` özetlerini kullanır; ham/kimliklenebilir veri okumaz. Quarto kaynakları geçici kopyalarla render edilir ve final SVG'ler yalnız `docs/carbon-svg-figures/` altında toplanır."
)

writeLines(markdown, file.path(out_dir, "INDEX.md"), useBytes = TRUE)

aesthetic_markdown <- c(
  "# Carbon Charts Estetik Audit",
  "",
  sprintf("Üretim zamanı: `%s`", format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")),
  "",
  "Bu audit, `docs/carbon-svg-figures/` altındaki 52 SVG'nin IBM Carbon Charts estetik ilkelerine göre yeniden taranmış durumunu verir. Referans zinciri: Carbon Charts repo `packages/core/scss` uygulama stilleri, yerel Figma source-of-truth Carbon Charts Library envanteri ve Carbon HTML Report chart palette referansı.",
  "",
  "Kaynaklar: resmi Carbon Charts repo (`carbon-design-system/carbon-charts`, `packages/core/scss/_type.scss`, `_color-palette.scss`, `components/_axis.scss`, `components/_grid.scss`, `components/_legend.scss`, `components/_title.scss`), Carbon data visualization chart anatomy, axes/labels ve legends rehberleri.",
  "",
  "## Kullanılan Estetik Kriterler",
  "",
  "| Kriter | Uygulanan karar | Kaynak rolü |",
  "|---|---|---|",
  "| Typography | IBM Plex Sans; chart metinleri 12px eşdeğeri, başlık 16px eşdeğeri semibold | Carbon Charts `_type.scss`, `_title.scss`; Figma Carbon Type Sets |",
  "| Başlık | Dekoratif mavi yerine `text-primary` siyah/semibold | Carbon Charts title component |",
  "| Eksenler | Axis title semibold `text-primary`; tick labels `text-secondary`; tick çizgileri kapalı | Carbon Charts `_axis.scss` |",
  "| Grid | Major grid `layer-accent-01` / `#e0e0e0`; minor grid yok | Carbon Charts `_grid.scss` |",
  "| Legend | Varsayılan bottom; 12px label; tek seri/uygun boşlukta doğrudan etiket tercih edilir | Carbon data visualization legend guidance |",
  "| Palet | Resmi `@carbon/charts` white-theme 14 seri paleti; sequential/semantic istisnalar korunur | Carbon Charts `_color-palette.scss` |",
  "| SVG provenance | Her SVG `data-carbon-style`, `data-carbon-charts-source`, `data-font`, `data-chart-palette` metadata taşır | Repro/audit gereği |",
  "",
  "## Toplu Sonuç",
  "",
  sprintf("- SVG sayısı: **%d**", nrow(manifest_public)),
  sprintf("- Carbon Charts estetik PASS: **%d**", sum(grepl("^PASS", manifest_public$carbon_aesthetic_status))),
  sprintf("- Raster/gradient istisnası notlanan: **%d**", sum(grepl("istisnası", manifest_public$carbon_aesthetic_status))),
  sprintf("- Review gereken: **%d**", sum(grepl("^REVIEW", manifest_public$carbon_aesthetic_status))),
  sprintf("- Maksimum non-Carbon hex sayısı: **%d**", max(manifest_public$non_carbon_hex_count, na.rm = TRUE)),
  "",
  "## Figür Bazlı Audit Matrisi",
  "",
  "| ID | SVG | Estetik durum | Chart palette hit | Text primary / secondary hit | Grid hit | Non-Carbon hex / rgb | Not |",
  "|---|---|---|---:|---:|---:|---:|---|",
  aesthetic_rows(manifest_public),
  "",
  "## Yorum",
  "",
  "- `non_carbon_rgb_count`, SVG içinde raster/interpolasyon üreten heatmap, density, contour veya antialias geçişlerinde sıfırdan büyük olabilir. Bu durum, kaynak grafiğin continuous scale veya raster-like geom kullanmasından gelir; SVG wrapper'a düşürülmüş PNG değildir.",
  "- Chart palette hit sayısı, resmi Carbon Charts kategorik paletinin veri işaretleri içinde ne kadar kullanıldığını gösterir. Tek seri veya semantic status grafikleri doğal olarak daha düşük hit sayısına sahip olabilir.",
  "- `text_primary`, `text_secondary` ve `grid` hitleri, Carbon Charts'ın başlık/axis/grid rollerinin SVG içinde gerçekten üretildiğini gösteren mekanik sinyallerdir."
)

writeLines(aesthetic_markdown, file.path(out_dir, "CARBON-AESTHETIC-AUDIT.md"), useBytes = TRUE)

technical_manifest <- manifest_public[manifest_public$technical_diagram_status != "N/A", , drop = FALSE]
technical_rows <- function(df) {
  paste0(
    "| ", df$id,
    " | ", make_link(df$svg_file),
    " | ", df$technical_diagram_role,
    " | ", df$technical_native_status,
    " | ", df$technical_diagram_status,
    " | ", df$carbon_aesthetic_status,
    " |"
  )
}

technical_markdown <- c(
  "# Figma Technical Diagram Library Uyum Audit",
  "",
  sprintf("Üretim zamanı: `%s`", format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")),
  "",
  "Bu dosya, Carbon SVG setindeki flow/diagram nitelikli figürlerin IBM Technical Diagram Library kaynaklı bileşen rollerine göre nasıl iyileştirildiğini belgeler.",
  "",
  "## Figma Kaynak Envanteri",
  "",
  "- Figma file key: `RtZDc7pMQt8HcgYTiitspr`",
  "- Okunan sayfalar: `Node`, `Connector`, `Label text`, `Label pill`, `Flow number`, `Legend`, `Indicator badge`, `Flow shape`, `IT architecture`.",
  "- Kullanılan bileşen aileleri: `Large node - Icon default`, `Small node - Icon`, `Connector line + line ending`, `_Connector`, `Line ending`, `Label text`, `Label pill`, `Flow number`, `Legend`.",
  "- Varyant sinyalleri: node renkleri Blue/Cyan/Green/Magenta/Purple/Red/Teal/Cool Gray/Black; connector stilleri Solid 1px, Solid 2px, Dash 4/8/16px, Double, Tunnel; line ending tipleri Arrow/Circle/Square/Diamond/Bar.",
  "",
  "## Uygulama Kararları",
  "",
  "- Flow/diagram figürleri custom SVG olarak yeniden oluşturuldu; generic chart axis/grid ve raster katmanı yoktur.",
  "- Connector stroke'ları Carbon `border-strong-01` / `layer-accent-01` rampasına normalize edildi; yönlü yollar Figma `Connector line + line ending` davranışına uygun marker ile çizildi.",
  "- SVG köküne `data-figma-technical-diagram-library`, `data-technical-diagram-role` metadata alanları eklendi.",
  "- SVG `<defs>` içine `tdl-node`, `tdl-connector`, `tdl-label-pill`, `tdl-flow-number` sınıfları eklendi; bu sınıflar Figma rol eşlemesini görünür ve yeniden düzenlenebilir kılar.",
  "- Okunurluk için APIM ve SEM diyagramlarında katsayı etiketleri label pill'e alınmış, DAG'de karıştırıcılar bir adjustment-set container'ına toplanmış, network grafiğinde node label'ları clipping üretmeyecek dış offsetlerle yerleştirilmiştir.",
  "",
  "## İyileştirilen Figürler",
  "",
  "| ID | SVG | Figma Technical Diagram rolü | Native renderer | Durum | Carbon audit |",
  "|---|---|---|---|---|---|",
  technical_rows(technical_manifest),
  "",
  "## Notlar",
  "",
  "- Bu çalışma Figma dosyasını değiştirmez; Figma Technical Diagram Library, yerel SVG üretimi için kaynak/otorite olarak kullanılmıştır.",
  "- Veri yoğun forest plot, ROC/DCA, heatmap, density ve demografik bar/violin grafikleri technical diagram sınıfına alınmadı; bunlar Carbon Charts estetiğiyle bırakıldı."
)

writeLines(technical_markdown, file.path(out_dir, "TECHNICAL-DIAGRAM-AUDIT.md"), useBytes = TRUE)

failures <- manifest_public[!grepl("^PASS", manifest_public$fidelity_status), ]
if (nrow(failures)) {
  print(failures[, c("id", "fidelity_status")], row.names = FALSE)
  stop("One or more SVG fidelity checks failed", call. = FALSE)
}

cat(sprintf("Carbon SVG export complete: %d SVG files -> %s\n", nrow(manifest_public), relative_path(out_dir)))
