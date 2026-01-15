from __future__ import annotations

from typing import List
import os
import re
import pandas as pd

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def expand_subject_keywords_llm(
    df: pd.DataFrame,          # kept for pipeline consistency (unused)
    subject: str,
    n_terms: int = 25,
    model: str = "gpt-4o-mini",
) -> List[str]:
    """
    Expand a subject keyword using an LLM.
    Returns a list of related keywords / short phrases.
    """
    subject = (subject or "").strip()
    if not subject:
        raise ValueError("subject must be non-empty")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in environment")

    client = OpenAI(api_key=api_key)

    prompt = (
        f"Give me {n_terms} keywords or short noun phrases related to the topic '{subject}'.\n"
        "Rules:\n"
        "- One term per line\n"
        "- Lowercase\n"
        "- Max 3 words per term\n"
        "- No explanations\n"
        "- No numbering or bullets\n"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You generate keyword lists for NLP filtering."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    raw_text = response.choices[0].message.content

    # Parse lines into keywords
    terms = []
    seen = set()

    for line in raw_text.splitlines():
        t = re.sub(r"[^a-z\s]", "", line.lower()).strip()
        t = " ".join(t.split())
        if not t:
            continue
        if t in seen:
            continue
        seen.add(t)
        terms.append(t)

    # Ensure subject is included
    subj_norm = subject.lower()
    if subj_norm not in seen:
        terms.insert(0, subj_norm)

    return terms