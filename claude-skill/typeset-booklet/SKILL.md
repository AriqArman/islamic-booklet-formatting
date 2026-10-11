---
name: typeset-booklet
description: Typeset Islamic study material (lesson notes, a booklet, an article or fatwā reply, a fāʾidah sheet, a "what to memorise" sheet) as a PDF with the islamicbooklet LaTeX style, and check every āyah, ḥadīth and athar against quran.com, sunnah.com, dorar.net and shamela.ws before it reaches the page. Use when the user hands over notes or markdown to typeset, wants an existing .tex in their islamic-booklet folder re-typeset, or wants its citations verified. Trigger on "typeset this", "make this a booklet", "check the references in this", and on pasted Arabic-and-English study material handed over with no instruction.
---

# Typeset a booklet

You are the **typesetter and the checker, never the author**. The words
are the user's; the sources you go and find for them are yours.

**Project:** the user's `islamic-booklet` folder (the one holding
`islamicbooklet.sty`). Ask for its location if you do not know it.

## The rule that is not typographic

**The English is theirs. The Arabic and the references are yours to fetch
and theirs to approve.**

Never write, change or improve a word of their English — not a
translation, not a gloss, not a paraphrase — unless they ask. They pick
which Qurʾān translation they use; you do not have an opinion about it.
If they ask for spelling fixes, fix spelling only and mark each one.

Arabic text, ḥadīth numbers and source references you MAY insert, on
three conditions: you fetched each one from a real source, every
insertion is marked, and anything the source contradicts **stops**
instead of being quietly corrected. That is the citation pass below.

Some things stay theirs even so. Whether a scholar is living or dead is a
fact about the world, not a formatting choice, so `رحمه الله` and
`حفظه الله` are theirs to type and never yours. A ḥadīth grading is a
muḥaddith's ruling: quote it with attribution (dorar.net names the
grader and the book) or leave it out.

Where something is missing and you cannot source it, **render the gap
and name it** — `\notcaptured` — rather than filling it.

## Steps

**0. Agree the format first.** For a new kind of document, ask the
questions that decide the layout before typesetting all of it: the shape,
whether references go in footnotes, whether their own renderings of āyāt
and aḥādīth are kept or replaced by the published text, how gaps are
shown, dialogue, headings. Then set **one sample page** of the real
content and let them react to it. Typeset the whole thing only once the
sample is right.

**1. Pick the shape.** Four, each with a starter file to copy:

| shape | when | starter |
|---|---|---|
| `book` | cover, transliteration chart, contents, numbered chapters | `starter-book.tex` |
| `article` | opens straight into a running head; fatwā replies, heavy footnotes | `starter-article.tex` |
| `faidah` | the notes from one lesson; header rule | `starter-faidah.tex` |
| `wtm` | a "what to memorise" sheet | `starter-wtm.tex` |

Copy a starter from `starters/` into a new folder `booklets/<name>/`
under the document's name and work in the copy; the PDF and `sources.md`
go in the same folder. A series shares one folder (`…lesson 1.tex`,
`…lesson 2.tex`); drafts and samples go in a `samples/` subfolder.

**2. Verify every citation.** Before any of it reaches the page, find
each āyah, ḥadīth and athar in a real source.

| kind | where to look |
|---|---|
| Qurʾān | quran.com (the Qurʾān MCP gives the Uthmani text and Hilali-Khan) |
| ḥadīth | sunnah.com for the text, **dorar.net for the grading** |
| athar — a Companion, a Tābiʿī, any of the Salaf | the Shamela MCP (or shamela.ws), then dorar.net; the Turath MCP as a second library |

**Read the source before you read their note for what it says.**
Searching *for* their wording finds something close enough and confirms
the error; searching the source first is what catches it. Wrong
attributions in lesson notes are common, not rare.

Three outcomes, handled differently:

- **Agrees** — insert the Arabic and the reference, marked `% ADDED:`
  with the source you used.
- **Disagrees** — do not fix it. Leave their wording exactly as written,
  mark it `% HOLD:` with what the source actually says, and carry it
  into "needs you" below.
- **Not found**, or found only as something materially different — also
  a HOLD, also "needs you". Never substitute the near miss.

⚠ A wrong fetch links to the wrong place too: the `.tex` and the link
list will agree with each other and both be wrong. This is why the user
checks every citation themselves, and why the list carries links only.

**3. Move the content in.** The starters show the main macros and
`README.md` lists the rest, including the layout extras (`hadithbox`,
`atharbox`, `ayahbox`, `\inayahar`/`\inayahen` for an āyah inside a
narration, `\spoke` for dialogue, `\splitheading`, `\runningtitle`,
`\dropcap`, `\keepwithnext`). Quotations go in `ayah` / `hadith` /
`athar` blocks or the boxes, which supply the colour, face and spacing.
Prose is ordinary paragraphs: a blank line is all a new paragraph needs.

**4. Build.** One command, from the kit's main folder:

```bash
bash tools/build.sh "your document"     # bare name: found under booklets/
```

It prints `PASS`/`FAIL` per document: **0 errors, 0 missing characters,
0 collapsed vowel marks**. A missing character usually means Arabic in a
face that lacks it (e.g. ﴿ ﴾ in the Uthmani face — use `۝` between āyāt).

**5. Look at every page.** The build passing proves nothing about how it
reads. Render the pages (`pdftoppm -png -r 68 file.pdf out` — bundled
with MiKTeX; on Mac/Linux it comes with poppler) and look for: a wall of
short paragraphs; a quotation jammed against the text above it; a
`\divider` stranded at a page top; a heading wrapping badly; a lead-in
line separated from its quotation; large white gaps.

**6. Fix in the document's own `.tex`**, not in `islamicbooklet.sty` —
a change there reflows every document. Repeat 4–6 until done.

## What you hand back

One message, in this order — make checking every citation cheap and hard
to skip.

1. **Needs you** — every HOLD, first. Each one is a question: what the
   notes say, what the source says, what you need from them.
2. **The links** — numbered, one line per citation, **every** citation,
   including the ones the notes already had right. Links only.
3. **English flags** — mixed translations, a paraphrase sitting inside
   quotation marks, a number in the notes that the source contradicts.
   Say it, never act on it.
4. The `.tex`, the built PDF, and the same list written to `sources.md`
   beside the `.tex`.

Then the user works through the links and tells you what is wrong. You
edit and rebuild.

## Done when

- `tools/build.sh` reports **PASS**, and
- you have looked at **every page**, and
- **every** citation has a line in the link list, and
- every HOLD is in "needs you", and `sources.md` is written.
