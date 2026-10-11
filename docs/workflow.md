# Workflow

How booklets are made with Claude Code: Claude typesets and checks the
sources; a person approves every citation.

*notes → agree the format on a sample page → verify every citation →
typeset → build checks → look at every page → a person signs off*

## Steps

1. **Notes come in** — the teacher's words as taken down.
2. **Agree the format** — shape, footnotes, gaps, dialogue — then
   approve one sample page.
3. **Verify every citation at its source:**
   - Qurʾān → quran.com
   - Ḥadīth → sunnah.com, gradings from dorar.net
   - Athar → Shamela, then dorar.net

   Source agrees → its Arabic and reference go in. Disagrees or not
   found → flagged, never quietly corrected.
4. **The speaker's words aren't rewritten** — spelling fixes only;
   gaps shown as *[not captured]*.
5. **Typeset and build** — must `PASS`.
6. **Look at every page.**
7. **A person signs off** — every flag answered, every link in
   `sources.md` checked.

## Setup

| | | |
|---|---|---|
| Claude Code | does the work | [claude.com/claude-code](https://claude.com/claude-code) |
| Qurʾān MCP | Uthmani text and translations | [quran-mcp](https://github.com/quran/quran-mcp) |
| Ḥadīth MCP | ḥadīth by collection and number | [hadith-mcp.org](https://hadith-mcp.org) |
| Shamela MCP | classical books, for āthār | [Shamela Link](https://shamela.link/en) (independent) |
| Turath MCP *(optional)* | a second library | [turath-mcp](https://github.com/adelpro/turath-mcp) (runs locally) |
| Web access | sunnah.com, dorar.net | Claude's browser or web fetch |
| `typeset-booklet` skill | the steps above | `cp -r claude-skill/typeset-booklet ~/.claude/skills/` |
| `grilling` skill *(optional)* | the format questions | [Matt Pocock's skills](https://github.com/mattpocock/skills) |

## Using it

1. Open Claude Code in this folder.
2. Give it your notes and say *"typeset this"*.
3. Answer the format questions; approve the sample page.
4. Read **"Needs you"** first, then check every link in `sources.md`.
5. Say what's wrong; it fixes and rebuilds.
