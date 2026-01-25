# Dissertation Data Workspace

Tweet and news datasets for exploratory analysis and topic work.

## Contents
- `2011-12-csv/` and `2011-12-uncompressed/`: December 2011 tweets (CSV shards + NDJSON). Note: `2011-12-29.csv` is header-only (0 rows).
- `2010-05-csv/` and `2010-05-uncompressed/`: May 2010 tweets (smaller sample; early/late gaps).
- `eda_2011_12_daily_counts.csv`, `eda_2011_12_country_counts.csv`: precomputed daily and country totals for 2011-12.
- `news_uk_dataset.csv`: UK news headlines with `title`, `published`, `source`, `category`.
- `nyt_2011_12.csv`: NYT text with `Text`, `Origin`, `id`, `country`, `language`.
- Notebooks/scripts: `main.ipynb`, `eda_csv.ipynb`, `run_bertopic.py`, `bertopic_jsd.py`, etc.
- UI: `streamlit_dashboard.py` for subject/topic selection form.

## Quick EDA (tweets)
- 2011-12 volume: 5,459,773 tweets; daily 175k–205k except 2011-12-28 (110k) and empty 2011-12-29.
- Top countries (2011-12): US ~2.19M; UK ~442k; Brasil ~439k; Indonesia ~333k; Japan ~185k; 91 countries total.
- 2010-05 volume: 217,636 tweets; gaps on many days; 24 countries total.
- CSV columns: `Text`, `Origin`, `id`, `country` (language derivable from uncompressed JSON `user.lang` or downstream langdetect outputs).

## How to reproduce counts
- Chunked script (memory-safe):
  ```bash
  python eda_2011_12.py            # writes daily and country CSVs; prints summary
  ```
  Adjust `--data-dir`, `--chunksize`, `--top-n` as needed.

## Streamlit form
- Lightweight dashboard to capture a subject, topic list, country, and language:
  ```bash
  streamlit run streamlit_dashboard.py
  ```
  Produces a structured JSON block for copy/paste.

## Next analysis ideas
- Plot daily volumes and weekday/hour patterns.
- Country share charts and geo heatmaps (using `place.bounding_box` from NDJSON).
- Hashtag/source top lists from `entities`/`source`.
- Align tweets with `news_uk_dataset.csv` and `nyt_2011_12.csv` by date or topic for correlation/coverage comparisons.
