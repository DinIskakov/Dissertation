from collections import Counter
import re
import pandas as pd

from .preprocess import normalize_text


def expand_subject_keywords_frequency(
    df: pd.DataFrame,
    subject: str,
    top_n: int = 25,
) -> list[str]:
    """
    Expand a subject keyword by counting the most common co-occurring words.
    Returns up to top_n keywords from rows that contain the subject.
    """
    subject = (subject or "").strip()
    if not subject:
        raise ValueError("subject must be non-empty")
    if "text" not in df.columns:
        raise KeyError("df must contain a 'text' column")
    if top_n <= 0:
        raise ValueError("top_n must be > 0")

    subject_norm = normalize_text(subject)
    subject_terms = set(subject_norm.split())

    stopwords = {
        "a", "an", "and", "are", "as", "at", "be", "but", "by",
        "for", "from", "has", "he", "i", "in", "is", "it", "its",
        "me", "my", "of", "on", "or", "our", "she", "so", "that",
        "the", "their", "they", "this", "to", "was", "we", "were",
        "with", "you", "your",
    }

    text_norm = df["text"].fillna("").astype(str).map(normalize_text)
    mask = text_norm.str.contains(subject_norm, case=False, na=False)
    matched = text_norm[mask]

    counter: Counter[str] = Counter()
    for text in matched:
        for token in re.findall(r"[a-z0-9]+", text):
            if token in subject_terms:
                continue
            if token in stopwords:
                continue
            counter[token] += 1

    return [word for word, _ in counter.most_common(top_n)]
