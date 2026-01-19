import pandas as pd

from .preprocess import normalize_text 

def filter_subject_keyword_only(
    df: pd.DataFrame,
    subject: str,
    text_col: str = "text",
) -> pd.DataFrame:
    """
    Keeps rows where the subject appears in the text (case-insensitive).
    """
    subject = subject.strip().lower()
    if subject == "":
        raise ValueError("subject must be non-empty")

    work = df.copy()
    work["_text_norm"] = work[text_col].fillna("").astype(str).map(normalize_text)

    mask = work["_text_norm"].str.contains(subject, case=False, na=False)

    out = work.loc[mask].drop(columns=["_text_norm"])
    return out
