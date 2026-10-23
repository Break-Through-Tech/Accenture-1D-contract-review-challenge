# Implements the four normalization steps needed for creating keyword and tf-idf baselines

import re
import unicodedata

# Step 3: NFKC does NOT fold curly quotes or en/em dashes, so map them explicitly
_QUOTE_DASH_MAP = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'", "\u2032": "'",   # ‘ ’ ‚ ‛ ′
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"', "\u2033": '"',   # “ ” „ ‟ ″
    "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-",   # ‐ ‑ ‒ – —
    "\u2015": "-", "\u2212": "-",                                                # ― −
})
_WHITESPACE_RUN = re.compile(r"\s+")

def normalize_text(text: str) -> str:
    '''Normalizes text through steps: NFKC normalization, case folding, quote/dash mapping, 
    and whitespace collapsing.'''
    text = unicodedata.normalize("NFKC", text)    # 1
    text = text.casefold()                        # 2
    text = text.translate(_QUOTE_DASH_MAP)        # 3
    return _WHITESPACE_RUN.sub(" ", text)         # 4
