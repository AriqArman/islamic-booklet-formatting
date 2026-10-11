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

## How a booklet is made — the full process

The style can be used by hand. In practice the booklets it was built for
are made with **Claude Code** doing the typesetting and the source
checking, and a person approving every citation. This is that process.

### In short

*lesson notes → agree the format on a sample page → every āyah, ḥadīth
and athar verified at its source → typeset → machine-checked → every page
looked at → a person signs off each citation.*

### The steps

1. **The notes come in** — what the teacher said, in the note-taker's
   words: short lines, half sentences, references jotted quickly
   ("An'am 153", "Sahih by Albani").
2. **Agree the format first.** Before anything is typeset, settle the
   questions that decide the look: the shape, footnotes, whether the
   note-taker's own renderings of āyāt are kept or replaced by the
   published translation, how gaps are shown, how dialogue is set. Then
   typeset **one sample page** of the real content and adjust it until it
   is right. (Claude asks these as numbered questions with a recommended
   answer each — the `grilling` skill below works well for this.)
3. **Every reference is checked against the original**, not against the
   notes:
   - **Qurʾān** — quran.com: the Uthmani Arabic and the translation.
   - **Ḥadīth** — sunnah.com for the text; **dorar.net** for the
     scholars' gradings.
   - **Athar** (sayings of the Companions and the Salaf) — al-Maktabah
     ash-Shāmilah (shamela.ws), then dorar.net.

   The source **agrees** → its Arabic and reference go in. It
   **disagrees** (a saying credited to the wrong person, a wrong āyah
   number) → nothing is quietly corrected: the notes stay as written and
   the problem is flagged. **Not found** → flagged too; a near match is
   never substituted.
4. **The speaker's words are not rewritten.** Only spelling slips are
   fixed, each one recorded. Where something was not caught, the page
   says *[not captured]* rather than guessing.
5. **Typeset** with this style, from a starter.
6. **Checked twice.** The build must report 0 errors, 0 missing
   characters and 0 collapsed vowel marks; then every page is looked at
   for bad breaks, crowded quotations and stranded lines.
7. **A person has the final say.** With the PDF comes a short list of
   everything that needs a decision, and a numbered list of links — one
   per citation — written to `sources.md` beside the booklet. The editor
   clicks through each one. Nothing is published on an automated check
   alone.

### Prerequisites for the Claude workflow

Follow each project's own setup page — they stay current when an
address or a step changes.

| what | why | setup |
|---|---|---|
| **Claude Code** | does the typesetting, building and checking | [claude.com/claude-code](https://claude.com/claude-code) |
| **Qurʾān MCP** | the exact Uthmani text and translations from quran.com — never from memory | [quran-mcp](https://github.com/quran/quran-mcp) |
| **Ḥadīth MCP** | ḥadīth text by collection and number, from sunnah.com data | [hadith-mcp.org](https://hadith-mcp.org) |
| **Shamela MCP** | the classical books, for āthār and their sources | [Shamela Link](https://shamela.link/en) — independent, not shamela.ws |
| *(optional)* **Turath MCP** | a second classical library (turath.io) | [turath-mcp](https://github.com/adelpro/turath-mcp) — community project, runs on your own computer |
| **Web access** | sunnah.com and **dorar.net** for gradings | Claude's built-in browser or web fetch |
| **The `typeset-booklet` skill** | the rules and steps above, so Claude follows them every time | in this folder: `claude-skill/typeset-booklet/` |
| *(optional)* the `grilling` skill | the numbered format questions in step 2 | [Matt Pocock's skills](https://github.com/mattpocock/skills) |

**Installing the skill.** Copy the folder into your Claude skills folder:

```bash
cp -r claude-skill/typeset-booklet ~/.claude/skills/
```

### How you go about it

1. Open Claude Code in this folder (`cd islamic-booklet`, then `claude`).
2. Hand over your notes — paste them, or give the path to a PDF or
   document — and say *"typeset this"* (or `/typeset-booklet`).
3. Answer the format questions; react to the sample page.
4. When the full booklet comes back, read **"Needs you"** first and answer
   each question; then click through every link in `sources.md`.
5. Tell Claude what is wrong; it edits and rebuilds. Repeat until every
   citation is confirmed — that second pass is yours.

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
claude-skill/        the typeset-booklet skill for Claude Code
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
