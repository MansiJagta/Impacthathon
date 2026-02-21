import json
import os
from pathlib import Path

from rapidfuzz import fuzz


WATCHLIST_DIR_ENV = "WATCHLIST_DIR"
FUZZY_THRESHOLD_ENV = "WATCHLIST_FUZZY_THRESHOLD"


def _default_watchlist_dir():
    return Path(__file__).resolve().parents[3] / "data" / "watchlists"


def _resolve_watchlist_dir():
    configured = os.getenv(WATCHLIST_DIR_ENV)
    return Path(configured) if configured else _default_watchlist_dir()


def _get_threshold():
    raw_threshold = os.getenv(FUZZY_THRESHOLD_ENV, "85")
    try:
        return float(raw_threshold)
    except ValueError:
        return 85.0


def _load_watchlist_entries():
    watchlist_dir = _resolve_watchlist_dir()
    if not watchlist_dir.exists():
        return []

    entries = []
    for path in watchlist_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() == ".txt":
            lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
            entries.extend([line for line in lines if line])
        elif path.suffix.lower() == ".json":
            try:
                content = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(content, list):
                    entries.extend([str(item).strip() for item in content if str(item).strip()])
            except json.JSONDecodeError:
                continue

    normalized = []
    seen = set()
    for entry in entries:
        key = entry.upper()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(key)
    return normalized


def watchlist_match(name):
    if not name:
        return False, None

    normalized_name = str(name).upper()
    threshold = _get_threshold()
    for watch_name in _load_watchlist_entries():
        score = fuzz.token_sort_ratio(normalized_name, watch_name)
        if score > threshold:
            return True, watch_name
    return False, None