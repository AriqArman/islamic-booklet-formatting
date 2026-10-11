#!/usr/bin/env python3
"""fixmarks.py — wrap the Arabic words that would break mark stacking.

    python3 tools/fixmarks.py "my booklet.tex"     # fix in place
    python3 tools/fixmarks.py --check "*.tex"         # report, change nothing

WHAT IT IS FOR
    Certain Qur'anic marks corrupt the font engine's mark-attachment state
    for the rest of the shaping run, so every shadda+vowel cluster after one
    of them has its vowel land ON the shadda instead of above it. A box ends
    the shaping run, so the text after it is shaped afresh and stacks right.

    The marks that stand alone between spaces are boxed for you by
    islamicbooklet.sty. The ones that attach to a letter cannot be — boxing the
    mark alone would cut it loose from its letter — so the whole WORD has to
    go in a box, and that is what this does. You never type \\mbox yourself:
    write the ayah as you please and let the build wrap it.

    It is idempotent. Running it twice changes nothing, so build.sh can run
    it every time.

    ⚠ IT SPLITS ON TOP-LEVEL WHITESPACE ONLY. \\inbody{عَنْ أَبِي} is one
      chunk, not three, so its braces survive; the recursion then boxes the
      trigger word INSIDE it rather than boxing the whole \\inbody, which
      would stop the line breaking where it needs to.

    ⚠ AN \\ar{} MAY SPAN LINES. The braces are matched over the whole file,
      not within a line, and the whitespace between words is handed back
      untouched — so the newlines, the indentation and even a blank line in
      the middle of a run come out exactly as they went in. Comments are
      masked first: a comment that mentions \\ar{} must not be treated as a
      call, and one with an unbalanced brace must not run the matcher off
      the end of the file.

    ⚠ آ IS DECOMPOSED to alef + maddah on any line that gains a box. HAFS
      has no precomposed آ; it arrives through a font fallback, and any
      \\mbox in the run disables that fallback and the letter vanishes.
      Decomposed, it needs no fallback. Same letter, same rendering.
"""
import glob
import re
import sys

MADDAH = "\u0653"
ALEFMADDA = "\u0622"

# Measured to poison the rest of the shaping run, and all of them ATTACH to
# a letter, so the word has to carry the box.
#
#   U+0653 maddah above          U+06E1 small high dotless head of khah
#   U+0654 hamza above           U+06E2 small high meem isolated form
#   U+06DC small high seen       U+06E4 small high madda
#   U+06DF small high rounded 0  U+06E7 small high yeh
#   U+06E0 small high rect. 0    U+06E8 small high noon
#                                U+06EB empty centre high stop
#                                U+06EC rounded high stop, filled centre
#
# The list came from sweeping U+06D6-U+06ED plus U+0653-U+0656 and U+0670 one
# mark at a time, each on its own page, measuring the shadda/vowel gap in the
# PDF: healthy clusters sit 2.26-2.34pt apart, poisoned ones 0.19pt. Every
# trigger is a mark that sits ABOVE the letter; every LOW mark tested came
# out clean. U+06E2 is the one that was still biting zz-amiri-test.
#
# The pause marks (U+06D6-U+06DB, U+06DD, U+06DE) are NOT here. They poison a
# run just the same, but islamicbooklet.sty already boxes each one through
# \newunicodechar, whether it stands alone or is written against a word.
# Listing them here too would wrap them a second time, and the file would
# never stop changing.
#
# Verified harmless, do not add: U+06E3, U+06E5, U+06E6, U+06E9, U+06EA,
# U+06ED, U+0655, U+0656, U+0670.
TRIGGERS = {0x0653, 0x0654, 0x06DC, 0x06DF, 0x06E0, 0x06E1,
            0x06E2, 0x06E4, 0x06E7, 0x06E8, 0x06EB, 0x06EC}

AR_CALL = re.compile(r"\\ar\{")


def has_trigger(s):
    return any(ord(c) in TRIGGERS for c in s)


def comment_spans(text):
    """index -> True for every character LaTeX would throw away as a comment.

    Needed because a comment may itself talk about \\ar{}, and one with an
    unbalanced brace in it would send the matcher off the end of the file.
    """
    mask = bytearray(len(text))
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2                       # \% and friends are not comments
            continue
        if c == "%":
            while i < n and text[i] != "\n":
                mask[i] = 1
                i += 1
            continue
        i += 1
    return mask


def match_brace(text, open_idx, mask):
    """index of the } that closes the { at open_idx, or None"""
    depth, i, n = 0, open_idx, len(text)
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if not mask[i]:
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return None


def tokenize(s):
    """-> [(is_word, text)] splitting on whitespace at brace depth 0.

    The whitespace runs are handed back untouched, so rebuilding the string
    restores the original line breaks and indentation exactly. That is what
    lets an \\ar{} spread over several lines come out the way it went in.
    """
    toks, buf, depth, inword = [], [], 0, None
    for ch in s:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        w = not (depth == 0 and ch.isspace())
        if inword is None:
            inword = w
        elif w != inword:
            toks.append((inword, "".join(buf)))
            buf, inword = [], w
        buf.append(ch)
    if buf:
        toks.append((inword, "".join(buf)))
    return toks


def fix_run(s):
    """box every trigger word in s, keeping its whitespace as it was"""
    out, n = [], 0
    for isword, t in tokenize(s):
        if isword:
            fixed, k = fix_chunk(t)
            out.append(fixed)
            n += k
        else:
            out.append(t)
    return "".join(out), n


def fix_chunk(chunk):
    """box this word, or recurse into its braces if it carries a macro"""
    if not has_trigger(chunk):
        return chunk, 0
    if chunk.startswith("\\mbox{") and chunk.endswith("}"):
        return chunk, 0                                  # already done

    if "{" in chunk:
        # a macro like \inbody{...}: go inside rather than boxing the lot
        head, _, rest = chunk.partition("{")
        cut = rest.rindex("}")
        body, close = rest[:cut], rest[cut:]
        fixed, n = fix_run(body)
        return head + "{" + fixed + close, n

    if "\\" in chunk:
        return chunk, 0                                  # bare macro, leave it
    return "\\mbox{%s}" % chunk, 1


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def fix_text(text):
    """-> new text, words boxed, lines touched, lines with an unclosed \\ar{"""
    mask = comment_spans(text)
    out, total, touched, broken = [], 0, [], []
    i = 0
    while True:
        m = AR_CALL.search(text, i)
        if not m:
            out.append(text[i:])
            break
        start = m.end() - 1                              # at the {
        if mask[m.start()]:                              # \ar{ inside a comment
            out.append(text[i:m.end()])
            i = m.end()
            continue
        end = match_brace(text, start, mask)
        if end is None:
            broken.append(line_of(text, m.start()))
            out.append(text[i:m.end()])
            i = m.end()
            continue

        inner = text[start + 1:end]
        if has_trigger(inner):
            # a box is coming, so precomposed آ can no longer use the fallback
            inner = inner.replace(ALEFMADDA, "\u0627" + MADDAH)
        fixed, n = fix_run(inner)
        if n:
            total += n
            touched.append(line_of(text, m.start()))
        out.append(text[i:start + 1])
        out.append(fixed)
        out.append(text[end])
        i = end + 1
    return "".join(out), total, touched, broken


def fix_file(path, dry_run=False):
    text = open(path, encoding="utf-8").read()
    new, total, touched, broken = fix_text(text)
    if total and not dry_run:
        open(path, "w", encoding="utf-8", newline="\n").write(new)
    return total, touched, broken


def main():
    argv = sys.argv[1:]
    dry_run = "--check" in argv
    pats = [a for a in argv if not a.startswith("-")] or ["*.tex"]

    paths = []
    for p in pats:
        paths += sorted(glob.glob(p))
    rc = 0
    for path in paths:
        try:
            total, touched, broken = fix_file(path, dry_run)
        except Exception as exc:
            print("fixmarks: %s: %s" % (path, exc), file=sys.stderr)
            continue
        if total:
            rc = 1
            verb = "would wrap" if dry_run else "wrapped"
            print("fixmarks: %s: %s %d word(s) on line(s) %s"
                  % (path, verb, total, ", ".join(str(t) for t in touched)))
        for ln in broken:
            print("fixmarks: %s: line %d has \\ar{ with no closing brace"
                  % (path, ln), file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
