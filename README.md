# Islamic Booklet — a LaTeX style for Arabic–English study material

Typesets lesson notes, booklets, articles and memorisation sheets with
the Qurʾān, ḥadīth and the sayings of the Salaf set properly: Uthmani
script for the Qurʾān, colour-coded quotations, honorific glyphs, and
Arabic and English sitting together on the same line without any markup.

## What you need

1. **LuaLaTeX.** Install one of:
   - Windows: [MiKTeX](https://miktex.org) (let it install missing packages on the fly)
   - Mac: [MacTeX](https://tug.org/mactex/)
   - Linux: TeX Live (`texlive-full`, or `texlive-luatex` + `texlive-lang-arabic`)

   It must be **LuaLaTeX** — pdfLaTeX and XeLaTeX will not work, and
   neither will Overleaf (see *Fonts* below).
2. **Bash** to run the build script — built into Mac and Linux; on
   Windows it comes with [Git for Windows](https://gitforwindows.org).
3. *Optional:* **Python 3** with `pypdf` (`pip install pypdf`). The build
   uses it to catch Arabic vowel marks that collapse onto their shadda —
   a fault that is otherwise invisible until someone reads the page.

## Quick start

```bash
bash tools/build.sh starter-faidah
```

That builds `starters/starter-faidah.pdf`. To start your own document,
copy a starter into a new folder under `booklets/` and build it by name:

```
booklets/
  my first booklet/
    my first booklet.tex
```

```bash
bash tools/build.sh "my first booklet"
```

The build prints `PASS` only with **0 errors, 0 missing characters and
0 collapsed vowel marks**. Always look at every page as well.

## The four shapes

| option | what it is | starter |
|---|---|---|
| `book` *(default)* | cover, transliteration chart, contents, numbered chapters | `starter-book.tex` |
| `article` | opens straight into a running head; footnote-heavy replies | `starter-article.tex` |
| `faidah` | the notes from one lesson, with a header rule | `starter-faidah.tex` |
| `wtm` | a "what to memorise" sheet | `starter-wtm.tex` |

```latex
\newcommand{\ibfontpath}{fonts/}
\usepackage[faidah]{islamicbooklet}
```

## Options

| | |
|---|---|
| `text=libron` | Set the English in **Libron** instead of EB Garamond. |
| `classic` | Headings and transliteration in **Baskerville** — only if you have `Baskerville.ttc` in `fonts/` (see *Fonts*). |
| `\bookletdomain{www.example.org}` | Your website, in the header of a fāʾidah/WTM sheet and at the foot of a cover. Leave it out for none. |
| `\bookletlogo{my-logo.png}` | Your logo, bottom right of a fāʾidah/WTM sheet. Leave it out for none. |
| `cover-frame.pdf` | Put full-page artwork with this name in the main folder and the book cover uses it. Without one, a frame is drawn from ornaments. |

## Writing

| you type | you get |
|---|---|
| `\begin{ayah} \ar{…} \en{…} \surah{Al-Fātiḥah}{1:5} \end{ayah}` | an āyah: red, Uthmani script, ornate brackets, the reference after |
| `\begin{hadith} … \src{Al-Bukhārī, no. 1} \end{hadith}` | a ḥadīth, in green |
| `\begin{athar} … \end{athar}` | a saying of other than the Prophet ﷺ, in blue |
| `\arpara{…}` | a plain Arabic paragraph, right to left |
| `\inquran{…}` `\inhadith{…}` `\inathar{…}` | colour a stretch inside a quotation |
| `\saw` `\ra` `\rmhu` `\swt` `\azza` … | the honorific glyphs (ﷺ and the rest) |
| `\tr{Tawḥīd}` | a transliterated term |
| `\g{…}` `\ed{…}` | a grey gloss `( )`, an editor's note `[ ]` |
| `\heading{…}` | a numbered chapter heading |
| `\divider` | a section ornament (never strands at a page top) |

### Layout extras

All optional — use them where you want them.

| you type | you get |
|---|---|
| `\begin{hadithbox} … \end{hadithbox}` | a ḥadīth in a quote block: pale green tint, a rule down the left, a small "ḤADĪTH" label |
| `\begin{atharbox} … \end{atharbox}` | the same in blue, labelled "ATHAR" |
| `\begin{quotebox}[Label]{colour} … \end{quotebox}` | any colour, any label (or `[]` for none) |
| `\begin{ayahbox}\begin{ayah} … \end{ayah}\end{ayahbox}` | an āyah with a thin red line down its left |
| `\inayahar{…}{النور:~٦٣}` / `\inayahen{…}{An-Nūr (24:63)}` | an āyah quoted *inside* a ḥadīth or athar — red, ornate brackets, reference after |
| `He said: \spoke{…}` / `\plainspoke{…}` | dialogue: the scholar's words in colour, the other party's in black, one paragraph per turn |
| `\begin{arabicturns} \arpara{…} \arpara{…} \end{arabicturns}` | the same dialogue in Arabic, turns set close |
| `\splitheading{The first pillar}{What Allah clarified…}` | a small spaced-caps line above a heading |
| `\runningtitle{My Booklet}` | header: title left, page number right |
| `\dropcap{S}{alafi} Manhaj is…` | a two-line drop cap |
| `\keepwithnext` | keeps a lead-in line on the same page as the block after it |
| `\notcaptured` | a grey *[not captured]* where the notes have a gap |

A `\footnote` inside a quote block prints inside the block. Put
`\footnotemark` in the block and `\footnotetext{…}` right after it.

Type transliteration characters directly — ā ī ū ḥ ṣ ṭ ḍ ẓ ʿ ʾ — never an
apostrophe for ʿ or ʾ. Arabic in an English sentence needs no markup.

**The one rule that is not typographic:** nothing in this style inserts
content you did not type — no honorific, no grading, no translation, no
ḥadīth number. Check every āyah and ḥadīth against its source before it
goes on the page.

## Fonts

`fonts/` already holds everything the style needs to build:

| font | used for | licence |
|---|---|---|
| EB Garamond | English text (default) | SIL Open Font License |
| Libron | English text with `text=libron` | SIL Open Font License |
| Amiri | the Qurʾānic brackets ﴿ ﴾ | SIL Open Font License |
| KFGQPC Uthmanic Script HAFS | the Qurʾān | King Fahd Complex — free to use and share, not to sell or modify |
| KFGQPC Uthmanic Taha Naskh | ḥadīth, athar, all other Arabic | as above |
| KFGQPC Arabic Symbols 01 | the honorific glyphs | as above |
| QCF_BSML | not used by the style — calligraphic Basmalah, Istiʿādhah, *qāla taʿālā*, *ṣadaqa Allāhu al-ʿAẓīm*, ornate brackets and sūrah names, for your own use | King Fahd Complex; no licence text in the file |

See `fonts/LICENSES.md`. Some faces **cannot be shared** and are not
included. If you own them, copy them into `fonts/` and the style picks
them up by itself:

| file | where to get it | used for | without it |
|---|---|---|---|
| `Baskerville.ttc` | macOS (`/System/Library/Fonts/Supplemental/`) | headings + transliteration with `classic` | the text font |
| `SnellRoundhand.ttc` | macOS | honorific phrases written out (`\hon{…}`) | the text font, italic |
| `majalla.ttf` (Sakkal Majalla) | Windows (`C:\Windows\Fonts`) | English of poetry | the text font |
| `Bahij Muna.ttf` | Bahij Virtual Academy | Arabic poetry, and the ❊❊❊ divider | Naskh; the divider becomes ❦ |

This is also why there is no Overleaf version: those faces cannot be
uploaded, and the honorific glyphs exist only in the KFGQPC symbols font.

## What's in the folder

```
islamicbooklet.sty   the style
fonts/               the shareable fonts and their licences
starters/            one starting file per shape
booklets/            your own documents go here
tools/build.sh       build + check
tools/fixmarks.py    boxes Arabic words that would otherwise break vowel stacking
tools/checkmarks.py  finds vowels that collapsed onto their shadda, in the PDF
```

## Licence

Copyright (C) 2026 Ariq

The style, the starters and the tools are released under the **LaTeX
Project Public License, version 1.3c** or later — see `LICENSE`. In
short: use it, share it and change it freely; if you distribute a
changed version, give it a different name so `islamicbooklet` always
means this one.

The fonts are **not** covered by that licence. Each keeps its own terms;
see `fonts/LICENSES.md`.

## Credits

Page design based on the books typeset by Suheyl bin Munir Mangá, used with his permission.

Fonts: EB Garamond (Georg Duffner, Octavio Pardo), Libron (Nico
Verbruggen), Amiri (Khaled Hosny), and the King Fahd Glorious Qur'an
Printing Complex for the Qurʾānic, Naskh, symbol and calligraphy faces.
