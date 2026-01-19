import re

def normalize_text(s: str) -> str:
    s = (s or "").lower()
    s = s.replace("#", " ")                  # keep hashtag words, drop '#'
    s = re.sub(r"\s+", " ", s).strip()
    return s
