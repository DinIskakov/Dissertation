import pandas as pd

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

# 1) Load your CSV
df = pd.read_csv("2010-05-csv/2010-05-07.csv")

# ✅ IMPORTANT: set this to your actual text column name
TEXT_COL = "Text"   # change if needed (e.g., "text")

if TEXT_COL not in df.columns:
    raise KeyError(f"'{TEXT_COL}' not found. Columns: {list(df.columns)}")

texts = df[TEXT_COL].fillna("").astype(str).tolist()
texts = [t for t in texts if t.strip()]
print("Loaded docs:", len(texts))

# 2) Embedding model (fast/light)
encoder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = encoder.encode(
    texts,
    show_progress_bar=True,
    batch_size=64,
    normalize_embeddings=True,
)

# 3) UMAP (fixed hyperparams)
umap_model = UMAP(
    n_neighbors=15,
    n_components=5,
    min_dist=0.0,
    metric="cosine",
    random_state=42,
)

# 4) HDBSCAN (fixed hyperparams)
hdbscan_model = HDBSCAN(
    min_cluster_size=15,
    metric="euclidean",
    cluster_selection_method="eom",
    prediction_data=True,
)

# 5) Vectorizer (for c-TF-IDF keywords)
vectorizer_model = CountVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2,
)

# 6) BERTopic
topic_model = BERTopic(
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    calculate_probabilities=True,
    verbose=True,
)

topics, probs = topic_model.fit_transform(texts, embeddings)

# 7) Save outputs
topic_info = topic_model.get_topic_info()
topic_info.to_csv("topic_info_2010-05-07.csv", index=False)
print("Saved topic info -> topic_info_2010-05-07.csv")

doc_topics = pd.DataFrame({"text": texts, "topic": topics})
doc_topics.to_csv("doc_topics_2010-05-07.csv", index=False)
print("Saved doc->topic -> doc_topics_2010-05-07.csv")

# 8) Quick sanity stats
n_outliers = sum(1 for t in topics if t == -1)
print(f"Outliers: {n_outliers}/{len(texts)} = {n_outliers/len(texts):.3f}")
print("Topics (excluding -1):", (topic_info["Topic"] != -1).sum())