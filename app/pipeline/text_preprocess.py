import re


def normalize_text(text: str) -> str:
    if text is None:
        return ""
    t = str(text).lower()
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"[^a-z0-9\s\.,!\?\-\']", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t
