--[[
  marmara-caption-bold.lua

  Marmara Tez Formati Talimatnamesi §1.6/§1.7 geregi tablo ve sekil
  basliklarinda etiket ("Tablo 1.", "Sekil 2a.") KALIN, devami normal olmalidir.

  Quarto DOCX hattinda crossref filtresi ("quarto") caption'i bagimsiz bir
  Para blogu olarak birakir. Bu blogun yapisi:
     [1] RawInline (OOXML <w:pPr> stil/anchor)
     [2] Str "Tablo" | "Şekil"
     [3] Str " "
     [4] Str "1"        (numara; alt-grup icin "1a" olabilir)
     [5] Str "."
     [6..] Space + baslik metni
  Bu filtre 2..5 arasindaki etiket token'larini Strong (bold) ile sarar.

  ÖNEMLI: Bu filtre "quarto" filtresinden SONRA calismali (bkz. _quarto.yml
  filters listesinde "quarto" sentinel'inden sonra gelir). Ayrica dogrudan
  Para/Plain element fonksiyonu Quarto AST'sinde tetiklenmedigi icin
  Pandoc(doc) icinde walk ile uygulanir.
]]

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

  -- Etiketin sonu: "." ile biten (veya "." olan) ilk Str token'i
  local label_end = nil
  for i = start, math.min(#inlines, start + 5) do
    local el = inlines[i]
    if el.t == "Str" and el.text:match("%.$") then
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

function Pandoc(doc)
  doc.blocks = doc.blocks:walk({
    Para = process_block,
    Plain = process_block,
  })
  return doc
end
