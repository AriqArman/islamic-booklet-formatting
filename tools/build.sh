#!/usr/bin/env bash
# build.sh — build a document and report whether it passed.
#
#   bash tools/build.sh starter-book          # by name, found under starters/ or booklets/
#   bash tools/build.sh "booklets/my book/my book"
#   bash tools/build.sh                        # every booklet + starter
#
# Run it from anywhere: it moves to the kit's main folder first. LaTeX
# runs there, so islamicbooklet.sty and fonts/ are always found, and
# -output-directory puts each PDF next to its .tex.
#
# Three passes: the contents, the cover frame's page anchors, and one to
# settle.
#
# LuaLaTeX is found on PATH, or in the usual MiKTeX / TeX Live / MacTeX
# places. Set LUALATEX=/path/to/lualatex to override.
set -u
cd "$(dirname "$0")/.."

find_lualatex() {
  if [ -n "${LUALATEX:-}" ]; then echo "$LUALATEX"; return; fi
  if command -v lualatex >/dev/null 2>&1; then command -v lualatex; return; fi
  for c in \
    "$HOME/AppData/Local/Programs/MiKTeX/miktex/bin/x64/lualatex.exe" \
    "/c/Program Files/MiKTeX/miktex/bin/x64/lualatex.exe" \
    /Library/TeX/texbin/lualatex \
    /usr/local/texlive/*/bin/*/lualatex; do
    [ -x "$c" ] && { echo "$c"; return; }
  done
}
LUALATEX=$(find_lualatex)
if [ -z "$LUALATEX" ]; then
  echo "LuaLaTeX not found. Install MiKTeX (Windows), MacTeX (Mac) or TeX Live,"
  echo "or set LUALATEX=/path/to/lualatex."
  exit 2
fi
# On Windows, MiKTeX can fail if something odd sits on PATH; give it a
# PATH holding only its own folder and the system.
LDIR=$(dirname "$LUALATEX")
RUNPATH="$LDIR:/usr/bin:/bin:${SYSTEMROOT:+/c/Windows/system32:/c/Windows}"

PY=""
for p in python3 python; do command -v "$p" >/dev/null 2>&1 && { PY=$p; break; }; done

resolve() {
  local n="${1%.tex}"
  if [ -f "$n.tex" ]; then echo "$n"; return; fi
  local hit
  hit=$(find booklets starters -name "$(basename "$n").tex" 2>/dev/null | head -1)
  [ -n "$hit" ] && echo "${hit%.tex}"
}

targets=()
if [ "$#" -gt 0 ]; then
  for a in "$@"; do
    t=$(resolve "$a"); [ -z "$t" ] && { echo "not found: $a"; exit 1; }
    targets+=("$t")
  done
else
  while IFS= read -r f; do
    grep -q '^[^%]*\documentclass' "$f" 2>/dev/null && targets+=("${f%.tex}")
  done < <(find booklets starters -name '*.tex' 2>/dev/null | sort)
fi

fail=0
for path in "${targets[@]}"; do
  dir=$(dirname "$path"); name=$(basename "$path")
  # Box the Arabic words that would otherwise break vowel stacking —
  # before building, every time. Idempotent.
  [ -n "$PY" ] && "$PY" tools/fixmarks.py "$path.tex" 2>&1 | sed 's/^/    /'
  for _ in 1 2 3; do
    PATH="$RUNPATH" "$LUALATEX" -interaction=nonstopmode \
      -output-directory="$dir" "$path.tex" >/dev/null 2>&1
  done
  log="$path.log"; pdf="$path.pdf"
  e=$(grep -cE '^! ' "$log" 2>/dev/null); e=${e:-0}
  m=$(grep -c 'Missing character' "$log" 2>/dev/null); m=${m:-0}
  o=$(grep -c 'Overfull .hbox' "$log" 2>/dev/null); o=${o:-0}
  p=$(grep -oE '\([0-9]+ pages?' "$log" 2>/dev/null | head -1 | tr -d '(')
  # marks= counts Arabic vowels that landed ON their shadda. Nothing in the
  # log shows this, so it is read from the finished PDF (needs pypdf).
  k=0
  if [ -n "$PY" ] && [ -f "$pdf" ]; then
    k=$("$PY" tools/checkmarks.py "$pdf" 2>/dev/null); k=${k:-0}
  fi
  verdict=PASS
  if [ "$e" -ne 0 ] || [ "$m" -ne 0 ] || [ "$k" -ne 0 ]; then verdict=FAIL; fail=1; fi
  printf '%-36s %s  errors=%s missing=%s overfull=%s marks=%s %s\n' \
         "$name" "$verdict" "$e" "$m" "$o" "$k" "${p:-}"
  [ "$e" -ne 0 ] && grep -E '^! ' "$log" | head -5 | sed 's/^/    /'
  [ "$k" -ne 0 ] && "$PY" tools/checkmarks.py "$pdf" -v 2>&1 >/dev/null | head -5
  rm -f "$dir"/*.aux "$dir"/*.log "$dir"/*.toc "$dir"/*.out
done
exit "$fail"
