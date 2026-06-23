import re
import unicodedata


ALIASES = {
    "bra": "brazil",
    "brasil": "brazil",
    "brazil national team": "brazil",
    "selecao brasileira": "brazil",
}


def normalize_team_name(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-z0-9]+", " ", ascii_name.lower()).strip()
    normalized = re.sub(r"\s+", " ", cleaned)
    return ALIASES.get(normalized, normalized)
