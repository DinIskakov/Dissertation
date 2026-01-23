"""Quick EDA for the 2011-12 tweet dump.

Reads all CSVs under 2011-12-csv, reports tweet counts per day and per country.
Designed to stream in chunks so it fits in memory.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import pandas as pd


def summarize(base_path: Path, chunksize: int = 200_000, top_n: int = 15):
    """Aggregate daily and country counts from the CSV shard directory."""
    files = sorted(base_path.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {base_path}")

    per_day = []
    country_counter: Counter[str] = Counter()

    for file in files:
        total = 0
        for chunk in pd.read_csv(file, usecols=["country"], chunksize=chunksize):
            total += len(chunk)
            country_counter.update(chunk["country"].dropna().str.strip())
        per_day.append((file.stem, total))

    per_day_df = pd.DataFrame(per_day, columns=["day", "tweet_count"])
    per_day_df["day"] = pd.to_datetime(per_day_df["day"], format="%Y-%m-%d")
    per_day_df = per_day_df.sort_values("day").reset_index(drop=True)
    per_day_df["day_str"] = per_day_df["day"].dt.strftime("%Y-%m-%d")

    country_df = (
        pd.DataFrame(country_counter.items(), columns=["country", "tweet_count"])
        .sort_values("tweet_count", ascending=False)
        .reset_index(drop=True)
    )

    return per_day_df, country_df.head(top_n), country_df


def print_summary(per_day_df: pd.DataFrame, top_countries: pd.DataFrame, all_countries: pd.DataFrame):
    total_tweets = per_day_df["tweet_count"].sum()
    zero_days = per_day_df.loc[per_day_df["tweet_count"] == 0, "day_str"].tolist()

    print(f"Total tweets: {total_tweets:,}")
    if zero_days:
        print(f"Days with zero rows: {', '.join(zero_days)}")

    print("\nTweets per day:")
    print(per_day_df[["day_str", "tweet_count"]].to_string(index=False))

    print("\nTop countries:")
    print(top_countries.to_string(index=False))

    print(f"\nUnique countries: {len(all_countries)}")


def main():
    parser = argparse.ArgumentParser(description="Basic EDA for 2011-12 tweet CSVs.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("2011-12-csv"),
        help="Directory containing daily CSV shards (default: 2011-12-csv)",
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=200_000,
        help="Number of rows per chunk when streaming CSVs (default: 200000)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=15,
        help="How many top countries to display (default: 15)",
    )
    args = parser.parse_args()

    per_day_df, top_countries, all_countries = summarize(
        base_path=args.data_dir, chunksize=args.chunksize, top_n=args.top_n
    )
    print_summary(per_day_df, top_countries, all_countries)


if __name__ == "__main__":
    main()
