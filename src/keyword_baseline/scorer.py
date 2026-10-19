"""Keyword-baseline scorer: one (chunk, category) score from a rule set.

Anchor +2, support +1, counter -1. Each evidence group counts once per chunk (its
strongest surviving contribution). A match that overlaps a veto phrase for its group
is dropped. Score is floored at 0. Plain substring matching on the normalized text.
"""
from .normalize import normalize, normalize_with_map

WEIGHT = {"anchor": 2, "support": 1, "counter": -1}


def prepare_category(cat_rules):
    """Normalize phrases once. Returns (groups, vetoes) ready for score_chunk."""
    groups = [
        (g["group_id"], g["role"], [(r["rule_id"], normalize(r["phrase"])) for r in g["rules"]])
        for g in cat_rules["groups"]
    ]
    vetoes = [(v["rule_id"], v["cancels_group"], normalize(v["phrase"])) for v in cat_rules["vetoes"]]
    return groups, vetoes


def _find_all(text, phrase):
    out, i = [], text.find(phrase)
    while i >= 0:
        out.append((i, i + len(phrase)))
        i = text.find(phrase, i + 1)
    return out


def score_chunk(norm_text, prepared):
    """Return (score, matches). Each match is a dict with rule/group ids and normalized offsets."""
    groups, vetoes = prepared
    veto_spans = {}
    for vid, gid, phrase in vetoes:
        veto_spans.setdefault(gid, []).extend(_find_all(norm_text, phrase))
    total, matches = 0, []
    for gid, role, rules in groups:
        group_hit = False
        for rid, phrase in rules:
            for s, e in _find_all(norm_text, phrase):
                if any(vs < e and s < ve for vs, ve in veto_spans.get(gid, ())):
                    matches.append({"rule_id": rid, "group_id": gid, "role": role, "start": s, "end": e, "vetoed": True})
                    continue
                matches.append({"rule_id": rid, "group_id": gid, "role": role, "start": s, "end": e, "vetoed": False})
                group_hit = True
        if group_hit:
            total += WEIGHT[role]
    return max(total, 0), matches


def score_text(source_text, prepared, check_offsets=False, normalized=None):
    """Normalize a source chunk, score it, and map match offsets back to the source.

    normalized: optional precomputed normalize_with_map(source_text) so one chunk is
    normalized once for all categories. check_offsets: assert that normalizing the
    source slice gives back the matched phrase."""
    norm_text, starts, ends = normalized or normalize_with_map(source_text)
    score, matches = score_chunk(norm_text, prepared)
    for m in matches:
        m["src_start"] = starts[m["start"]]
        m["src_end"] = ends[m["end"] - 1]
        if check_offsets:
            assert normalize(source_text[m["src_start"]:m["src_end"]]) == norm_text[m["start"]:m["end"]], m
    return score, matches
