import re

def normalize_text(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"http\S+|www\.\S+", " ", s)   # URLs
    s = re.sub(r"@\w+", " ", s)              # mentions
    s = s.replace("#", " ")                  # keep hashtag words, drop '#'
    s = re.sub(r"\s+", " ", s).strip()
    return s