# Reference

## Setup

```latex
\newcommand{\ibfontpath}{fonts/}
\usepackage[faidah]{islamicbooklet}     % book | article | faidah | wtm
```

You need **LuaLaTeX** (not pdfLaTeX or XeLaTeX) and **bash** — on
Windows it comes with [Git for Windows](https://gitforwindows.org).
*Optional:* Python 3 with `pypdf`, so the build can catch collapsed
vowel marks.

## Building

```bash
bash tools/build.sh "my booklet"     # by name, found under booklets/ or starters/
bash tools/build.sh                  # everything
```

Each document lives in its own folder under `booklets/`; the PDF is
written next to it. After a `PASS`, still look at every page.

## Options

| | |
|---|---|
| `text=libron` | English in Libron instead of EB Garamond |
| `classic` | Baskerville headings — needs `fonts/Baskerville.ttc` |
| `\bookletdomain{www.example.org}` | your website in the sheet header / on the cover |
| `\bookletlogo{logo.png}` | your logo at the foot of a sheet |
| `cover-frame.pdf` in the main folder | your own cover artwork (otherwise a drawn frame) |

## Writing

| you type | you get |
|---|---|
| `\begin{ayah} \ar{…} \en{…} \surah{Al-Fātiḥah}{1:5} \end{ayah}` | an āyah, red, Uthmani script |
| `\begin{hadith} … \src{Al-Bukhārī, no. 1} \end{hadith}` | a ḥadīth, green |
| `\begin{athar} … \end{athar}` | an athar, blue |
| `\arpara{…}` | an Arabic paragraph |
| `\inquran{…}` `\inhadith{…}` `\inathar{…}` | colour part of a quotation |
| `\saw` `\ra` `\rmhu` `\swt` `\azza` … | honorific glyphs |
| `\tr{Tawḥīd}` | a transliterated term |
| `\g{…}` `\ed{…}` | grey gloss `( )`, editor's note `[ ]` |
| `\heading{…}` | numbered heading |
| `\divider` | section ornament |

Type ā ī ū ḥ ṣ ṭ ḍ ẓ ʿ ʾ directly — never an apostrophe for ʿ or ʾ.
Arabic inside English needs no markup.

## Layout extras

| you type | you get |
|---|---|
| `\begin{hadithbox} … \end{hadithbox}` | quote block, green, labelled |
| `\begin{atharbox} … \end{atharbox}` | quote block, blue, labelled |
| `\begin{quotebox}[Label]{colour} … \end{quotebox}` | any colour and label |
| `\begin{ayahbox}\begin{ayah}…\end{ayah}\end{ayahbox}` | red line beside an āyah |
| `\inayahar{…}{النور:~٦٣}` · `\inayahen{…}{An-Nūr (24:63)}` | an āyah inside a narration |
| `He said: \spoke{…}` · `\plainspoke{…}` | dialogue, one turn per paragraph |
| `\begin{arabicturns} … \end{arabicturns}` | Arabic dialogue turns |
| `\splitheading{small line}{heading}` | two-part heading |
| `\runningtitle{Title}` | title left, page number right |
| `\dropcap{S}{alafi}` | drop cap |
| `\keepwithnext` | keep a lead-in with the next block |
| `\notcaptured` | grey *[not captured]* |

A `\footnote` inside a quote block stays in the block: use
`\footnotemark` inside and `\footnotetext{…}` after it.

## The one rule

Nothing in this style inserts content you didn't type — no honorific,
grading, translation or ḥadīth number. Check every citation at its
source.

## Folder

```
islamicbooklet.sty   the style
starters/            one file per shape
booklets/            your documents
fonts/               fonts and licences
tools/               build and Arabic mark checks
claude-skill/        the typeset-booklet skill
docs/                these pages
```
