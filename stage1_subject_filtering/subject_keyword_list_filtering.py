import re
import pandas as pd
from typing import Iterable, List

from .preprocess import normalize_text


def filter_subject_keywords_list(
    df: pd.DataFrame,
    keywords: Iterable[str],
    text_col: str = "text",
    keep_regex_word_boundary: bool = True,
) -> pd.DataFrame:
    """
    Keeps rows where any keyword appears in the text (case-insensitive).
    """
    cleaned: List[str] = []
    for kw in keywords:
        if kw is None:
            continue
        kw = str(kw).strip().lower()
        if kw:
            cleaned.append(kw)

    if not cleaned:
        raise ValueError("keywords must contain at least one non-empty string")

    work = df.copy()
    work["_text_norm"] = work[text_col].fillna("").astype(str).map(normalize_text)

    joined = "|".join(re.escape(k) for k in cleaned)
    if keep_regex_word_boundary:
        pattern = re.compile(rf"\b(?:{joined})\b", re.IGNORECASE)
    else:
        pattern = re.compile(joined, re.IGNORECASE)

    mask = work["_text_norm"].str.contains(pattern, na=False)
    out = work.loc[mask].drop(columns=["_text_norm"])
    return out
