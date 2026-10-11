#!/usr/bin/env python3
"""checkmarks.py — find Arabic vowels that have landed ON their shadda.

    python3 tools/checkmarks.py "my booklet.pdf"        # prints a count
    python3 tools/checkmarks.py "my booklet.pdf" -v     # lists each one

WHY THIS EXISTS
    Certain Qur'anic marks corrupt the font engine's mark-attachment state
    for the rest of the shaping run. Every shadda+vowel cluster after one of
    them silently loses its mark-to-mark step: the vowel stops being lifted
    onto the shadda and lands on top of it instead. It still builds clean —
    no error, no missing character, no overfull box — so nothing in the log
    tells you. The only witness is the geometry in the finished PDF.

    A healthy cluster puts the vowel about 2.3pt above the shadda. A broken
    one puts it about 0.2pt away. This reads the glyph coordinates straight
    out of the PDF content stream and counts the ones that collapsed.

    Being a check on the OUTPUT, it catches every trigger, including ones
    nobody has identified yet. That is the point: you do not have to know
    the list. Build, and if marks= is not 0, run tools/fixmarks.py.

    Exits 0 even when it cannot read the file, printing 0, so that a missing
    pypdf never fails a build. Run it by hand if a count looks wrong.
"""
import re
import sys

# a pair closer than this in x is the same cluster; farther apart in y than
# this is two unrelated marks and not our business
SAME_CLUSTER_X = 0.6
UNRELATED_Y = 6.0
# below this vertical gap the vowel is sitting on the shadda, not above it
COLLAPSED_Y = 1.0

VOWELS = set(range(0x064B, 0x0651))          # fathatan..kasra
SHADDA = 0x0651

_hexpair = re.compile(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>")
_ops = re.compile(
    r"/(F\d+)\s+([\d.]+)\s+Tf"
    r"|(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+Tm"
    r"|\[(.*?)\]\s*TJ"
    r"|<([0-9A-Fa-f]+)>\s*Tj",
    re.S)


def _tounicode(fontobj):
    """glyph id -> character, from the font's ToUnicode CMap"""
    out = {}
    tu = fontobj.get("/ToUnicode")
    if tu is None:
        return out
    data = tu.get_object().get_data().decode("latin-1")
    for blk in re.findall(r"beginbfchar(.*?)endbfchar", data, re.S):
        for src, dst in _hexpair.findall(blk):
            try:
                out[int(src, 16)] = "".join(
                    chr(int(dst[i:i + 4], 16)) for i in range(0, len(dst) - 3, 4))
            except ValueError:
                pass
    return out


def collapsed(pdf_path):
    """[(page, x, y, vowel_name, gap_pt)] for every vowel sitting on a shadda"""
    from pypdf import PdfReader
    import unicodedata

    hits = []
    for pageno, page in enumerate(PdfReader(pdf_path).pages, 1):
        fonts = page.get("/Resources", {}).get("/Font", {})
        umap = {str(k).lstrip("/"): _tounicode(v.get_object()) for k, v in fonts.items()}

        content = page.get_contents().get_data().decode("latin-1")
        font = None
        x = y = None
        marks = []
        for m in _ops.finditer(content):
            if m.group(1):
                font = m.group(1)
                continue
            if m.group(3) is not None:
                x, y = float(m.group(7)), float(m.group(8))
                continue
            body = m.group(9) if m.group(9) is not None else "<%s>" % m.group(10)
            gids = []
            for h in re.findall(r"<([0-9A-Fa-f]+)>", body):
                gids += [int(h[i:i + 4], 16) for i in range(0, len(h) - 3, 4)]
            if not gids or x is None:
                continue
            chars = "".join(umap.get(font, {}).get(g, "") for g in gids)
            if len(chars) == 1:
                marks.append((x, y, ord(chars)))

        # pair each shadda with a vowel sitting in the same column
        for xs, ys, cs in marks:
            if cs != SHADDA:
                continue
            for xv, yv, cv in marks:
                if cv not in VOWELS:
                    continue
                if abs(xs - xv) >= SAME_CLUSTER_X:
                    continue
                gap = abs(ys - yv)
                if gap < UNRELATED_Y and gap < COLLAPSED_Y:
                    hits.append((pageno, round(xv, 1), round(yv, 1),
                                 unicodedata.name(chr(cv), "?").replace("ARABIC ", ""),
                                 round(gap, 2)))
    return hits


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    verbose = any(a in ("-v", "--verbose") for a in sys.argv[1:])
    if not args:
        print("usage: checkmarks.py <file.pdf> [-v]", file=sys.stderr)
        return 0
    try:
        hits = collapsed(args[0])
    except Exception as exc:                       # never break a build
        if verbose:
            print("checkmarks: %s" % exc, file=sys.stderr)
        print(0)
        return 0
    if verbose:
        for pageno, x, y, name, gap in hits:
            print("  page %-3d x=%-7.1f y=%-7.1f %-12s gap=%.2fpt" %
                  (pageno, x, y, name, gap), file=sys.stderr)
    print(len(hits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
