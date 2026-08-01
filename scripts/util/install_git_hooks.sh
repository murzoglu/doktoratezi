#!/usr/bin/env bash
# Tez QC pre-commit kurucu (opt-in).
#
# Kurulunca: `chapters/*.qmd` veya `references/references.bib` staged olan her
# commit'te `tez_checklist_verify.py --fast` çalışır; FAIL ise commit durur.
# Böylece 28+ maddelik ana kalite kapısı teslim/commit sınırında OTOMATİK
# ateşlenir (etüt madde A — ana kapı hiçbir git akışına bağlı değildi).
#
# Kullanım:
#   bash scripts/util/install_git_hooks.sh              # kur
#   bash scripts/util/install_git_hooks.sh --uninstall  # kaldır
# Bypass (tek seferlik):  git commit --no-verify
set -euo pipefail

HOOK="$(git rev-parse --git-path hooks/pre-commit)"

if [[ "${1:-}" == "--uninstall" ]]; then
  if [[ -f "$HOOK" ]] && grep -q "tez_checklist_verify" "$HOOK" 2>/dev/null; then
    rm -f "$HOOK"
    echo "pre-commit kaldırıldı: $HOOK"
  else
    echo "kaldırılacak tez pre-commit yok ($HOOK)"
  fi
  exit 0
fi

if [[ -f "$HOOK" ]] && ! grep -q "tez_checklist_verify" "$HOOK" 2>/dev/null; then
  echo "UYARI: mevcut (tez-dışı) bir pre-commit var: $HOOK" >&2
  echo "Üzerine yazmak için önce yedekleyin; iptal edildi." >&2
  exit 1
fi

mkdir -p "$(dirname "$HOOK")"
cat > "$HOOK" <<'HOOKEOF'
#!/usr/bin/env bash
# doktoratezi QC pre-commit (scripts/util/install_git_hooks.sh ile kuruldu)
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
if git diff --cached --name-only \
    | grep -Eq '^chapters/.*\.qmd$|^references/references\.bib$'; then
  echo "[QC] tez kontrol checklisti (--fast) çalışıyor..."
  if ! python3 "$ROOT/scripts/util/tez_checklist_verify.py" --fast; then
    echo "[QC] checklist FAIL — commit durduruldu." >&2
    echo "     Düzeltin ya da 'git commit --no-verify' ile atlayın." >&2
    exit 1
  fi
fi
exit 0
HOOKEOF
chmod +x "$HOOK"
echo "pre-commit kuruldu: $HOOK"
echo "Bypass: git commit --no-verify"
echo "Kaldır: bash scripts/util/install_git_hooks.sh --uninstall"
