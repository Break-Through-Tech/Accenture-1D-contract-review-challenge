"""Text normalization with a map from normalized offsets back to source offsets.

Steps (Issue #8 spec): NFKC, casefold, unify quotes/dashes, collapse whitespace runs
to one space. Done cluster by cluster (a base character plus its combining marks) so
every normalized character knows which source characters it came from.

Output is identical to normalize_text in PR #34 (TF-IDF baseline), which also maps the
low/high-9 and prime quote variants; that function returns a string only, this one
also returns the offset map.
"""
import re
import unicodedata

_QUOTES = {
    "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'", "\u2032": "'",
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"', "\u2033": '"',
}
_DASHES = re.compile("[‐-―−]")


def _clusters(text):
    start = 0
    for i in range(1, len(text) + 1):
        if i == len(text) or unicodedata.combining(text[i]) == 0:
            yield start, i
            start = i


def normalize_with_map(text):
    """Return (normalized, src_start, src_end); for normalized char k the source span
    is text[src_start[k]:src_end[k]]. A whitespace run maps to one space."""
    out, starts, ends = [], [], []
    pending_space = None  # (start, end) of the current whitespace run
    for a, b in _clusters(text):
        piece = unicodedata.normalize("NFKC", text[a:b]).casefold()
        piece = "".join(_QUOTES.get(c, c) for c in piece)
        piece = _DASHES.sub("-", piece)
        for c in piece:
            if c.isspace():  # includes a space made by NFKC inside a cluster (e.g. U+00A8)
                if pending_space is None:
                    pending_space = [a, b]
                else:
                    pending_space[1] = b
                continue
            if pending_space is not None:
                out.append(" "); starts.append(pending_space[0]); ends.append(pending_space[1])
                pending_space = None
            out.append(c); starts.append(a); ends.append(b)
    if pending_space is not None:
        out.append(" "); starts.append(pending_space[0]); ends.append(pending_space[1])
    return "".join(out), starts, ends


def normalize(text):
    return normalize_with_map(text)[0]
