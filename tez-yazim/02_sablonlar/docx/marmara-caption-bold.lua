--[[
  marmara-caption-bold.lua

  Marmara Tez Formati Talimatnamesi §1.6/§1.7 geregi tablo ve sekil
  basliklarinda etiket ("Tablo 1:", "Sekil 2a:") KALIN, devami normal olmalidir.

  Quarto DOCX hattinda crossref filtresi ("quarto") caption'i bagimsiz bir
  Para blogu olarak birakir. Bu blogun yapisi:
     [1] RawInline (OOXML <w:pPr> stil/anchor)
     [2] Str "Tablo" | "Şekil"
     [3] Str " "
     [4] Str "1"        (numara; alt-grup icin "1a" olabilir)
     [5] Str ":"
     [6..] Space + baslik metni
  Bu filtre 2..5 arasindaki etiket token'larini Strong (bold) ile sarar.
  Enstitu teslim duzeltmesi geregi basliklar haricindeki kullanici kaynakli
  Strong bicimleri ciktida normal yaziya cevrilir; tablo/sekil etiket kalinligi
  bu temizlikten sonra yeniden yalniz caption etiketi icin uygulanir.

  ÖNEMLI: Bu filtre "quarto" filtresinden SONRA calismali (bkz. _quarto.yml
  filters listesinde "quarto" sentinel'inden sonra gelir). Ayrica dogrudan
  Para/Plain element fonksiyonu Quarto AST'sinde tetiklenmedigi icin
  Pandoc(doc) icinde walk ile uygulanir.
]]

local function strip_strong(inline)
  return inline.content
end

-- inlines listesinde etiketi bulup Strong ile sarar; degistiyse yeni liste,
-- degilse nil doner.
local function bolden_caption_inlines(inlines)
  if not inlines or #inlines < 2 then return nil end

  -- Etiket kelimesinin indeksini bul (RawInline anchor'lari atla)
  local start = nil
  for i = 1, math.min(#inlines, 3) do
    local el = inlines[i]
    if el.t == "Str" and (el.text == "Tablo" or el.text == "Şekil") then
      start = i
      break
    end
  end
  if not start then return nil end

  -- Etiketin sonu: ":" ile biten ilk Str token'i. Nokta, eski DOCX
  -- girdileriyle uyumluluk için de kabul edilir.
  local label_end = nil
  for i = start, math.min(#inlines, start + 5) do
    local el = inlines[i]
    if el.t == "Str" and el.text:match("[%.:]$") then
      label_end = i
      break
    end
  end
  if not label_end then return nil end

  -- Yeni liste: start'tan onceki token'lar aynen, start..label_end Strong,
  -- sonrasi aynen.
  local out = {}
  for i = 1, start - 1 do table.insert(out, inlines[i]) end
  local label = {}
  for i = start, label_end do table.insert(label, inlines[i]) end
  table.insert(out, pandoc.Strong(label))
  for i = label_end + 1, #inlines do table.insert(out, inlines[i]) end
  return out
end

local function process_block(b)
  if b.t == "Para" or b.t == "Plain" then
    local s = pandoc.utils.stringify(b)
    if s:match("^Tablo") or s:match("^Şekil") then
      local nc = bolden_caption_inlines(b.content)
      if nc then b.content = nc end
    end
  end
  return b
end

-- Marmara §2.5: kısaltma, ayraç ve açıklama aynı satırda hizalı kalmalıdır.
-- İlk satırdaki "ABD" ile bu tek tabloyu tanır ve kaynak metindeki kısa
-- ayraç çizgilerinden bağımsız, PDF/DOCX ortak kolon genişliği uygular.
local function size_abbreviation_table(tbl)
  if #tbl.bodies == 0 or #tbl.bodies[1].body == 0 then return nil end
  local first_row = tbl.bodies[1].body[1]
  if #first_row.cells == 0 then return nil end
  if pandoc.utils.stringify(first_row.cells[1].contents) ~= "ABD" then return nil end

  tbl.colspecs = {
    {pandoc.AlignLeft, 0.17},
    {pandoc.AlignCenter, 0.03},
    {pandoc.AlignLeft, 0.80},
  }
  return tbl
end

local function has_caption(tbl)
  if not tbl.caption then return false end
  if tbl.caption.short and #tbl.caption.short > 0 then return true end
  return tbl.caption.long and #tbl.caption.long > 0
end

-- LaTeX longtable ortami, altyazisi olmasa da `table` sayacini artirir.
-- Bu tur yapisal tablolar (onay, kisaltmalar, ozgecmis) dizinde gorunur
-- bir tez tablosu olmadigindan sonraki baslikli tablonun sayisini koruruz.
local function preserve_unnumbered_table_counter(blocks)
  local out = {}
  for _, block in ipairs(blocks) do
    table.insert(out, block)
    if block.t == "Table" and not has_caption(block) then
      table.insert(out, pandoc.RawBlock("latex", "\\addtocounter{table}{-1}"))
    end
  end
  return out
end

function Pandoc(doc)
  doc.blocks = doc.blocks:walk({
    Strong = strip_strong,
  })
  doc.blocks = doc.blocks:walk({
    Para = process_block,
    Plain = process_block,
    Table = size_abbreviation_table,
  })
  doc.blocks = doc.blocks:walk({
    Blocks = preserve_unnumbered_table_counter,
  })
  return doc
end
