from rapidfuzz import fuzz


def similarity_score(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return fuzz.token_sort_ratio(a, b) / 100.0


def is_match(a: str, b: str, threshold=0.85) -> bool:
    return similarity_score(a, b) >= threshold