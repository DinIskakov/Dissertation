import numpy as np
import pandas as pd

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

from stage1_subject_filtering.llm_expansion import get_synonyms
from stage1_subject_filtering.subject_keyword_list_filtering import (
    filter_subject_keywords_list,
)


TWITTER_CSV = "2011-12-csv/2011-12-07.csv"
NEWS_CSV = "nyt_2011_12.csv"
TEXT_COL = "Text"

SUBJECT = "Immigration"
TOPICS = ["Medicine", "Politics", "Mafia"]


def load_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if TEXT_COL not in df.columns:
        raise KeyError(f"'{TEXT_COL}' not found in {path}. Columns: {list(df.columns)}")
    return df


def expand_subject_keywords(subject: str) -> list[str]:
    try:
        synonyms = get_synonyms(subject)
    except Exception as exc:
        print(f"Synonym expansion failed, using subject only: {exc}")
        synonyms = []
    keywords = [subject] + list(synonyms)
    cleaned = []
    for kw in keywords:
        if kw and str(kw).strip():
            cleaned.append(str(kw).strip())
    return cleaned


def to_texts(df: pd.DataFrame) -> list[str]:
    texts = df[TEXT_COL].fillna("").astype(str).tolist()
    return [t for t in texts if t.strip()]


def jsd(p: np.ndarray, q: np.ndarray) -> float:
    p = p / p.sum()
    q = q / q.sum()
    m = 0.5 * (p + q)
    kl_pm = np.where(p > 0, p * np.log2(p / m), 0.0)
    kl_qm = np.where(q > 0, q * np.log2(q / m), 0.0)
    return float(0.5 * (kl_pm.sum() + kl_qm.sum()))


def build_model(seed_topic_list: list[list[str]]) -> BERTopic:
    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
        random_state=42,
    )

    hdbscan_model = HDBSCAN(
        min_cluster_size=15,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )

    vectorizer_model = CountVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
    )

    return BERTopic(
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        seed_topic_list=seed_topic_list,
        calculate_probabilities=True,
        verbose=True,
    )


twitter_df = load_df(TWITTER_CSV)
news_df = load_df(NEWS_CSV)

subject_keywords = expand_subject_keywords(SUBJECT)
print("Subject keywords:", subject_keywords)

twitter_filtered = filter_subject_keywords_list(twitter_df, subject_keywords, text_col=TEXT_COL)
news_filtered = filter_subject_keywords_list(news_df, subject_keywords, text_col=TEXT_COL)

twitter_texts = to_texts(twitter_filtered)
news_texts = to_texts(news_filtered)

texts = twitter_texts + news_texts
sources = (["twitter"] * len(twitter_texts)) + (["nyt"] * len(news_texts))

if not texts:
    raise ValueError("No texts left after subject filtering.")

print("Loaded docs after subject filter:", len(texts))

seed_topic_list = [[t.lower()] for t in TOPICS]
model = build_model(seed_topic_list)

encoder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = encoder.encode(
    texts,
    show_progress_bar=True,
    batch_size=64,
    normalize_embeddings=True,
)

topics, _probs = model.fit_transform(texts, embeddings)

doc_topics = pd.DataFrame({"text": texts, "source": sources, "topic": topics})
doc_topics.to_csv("doc_topics_twitter_nyt_2011-12-07_guided.csv", index=False)

topic_info = model.get_topic_info()
topic_info.to_csv("topic_info_twitter_nyt_2011-12-07_guided.csv", index=False)

filtered = doc_topics[doc_topics["topic"] != -1]
topic_ids = sorted(filtered["topic"].unique())

twitter_counts = (
    filtered[filtered["source"] == "twitter"]["topic"]
    .value_counts()
    .reindex(topic_ids, fill_value=0)
    .to_numpy(dtype=float)
)
nyt_counts = (
    filtered[filtered["source"] == "nyt"]["topic"]
    .value_counts()
    .reindex(topic_ids, fill_value=0)
    .to_numpy(dtype=float)
)

if twitter_counts.sum() == 0 or nyt_counts.sum() == 0:
    raise ValueError("One of the sources has zero non-outlier topics.")

divergence = jsd(twitter_counts, nyt_counts)
print(f"Jensen-Shannon divergence (guided topics): {divergence:.6f}")
