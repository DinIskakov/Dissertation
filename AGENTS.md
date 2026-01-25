# AGENTS

Quick guardrails for this repository.

## Priorities
- Solve the user’s request with minimal, clear changes; avoid churn.
- Preserve existing work: no `git reset --hard` or destructive commands unless the user explicitly asks.
- Stay in this repo (`/Users/diniskakov/Desktop/Dissertation`) and writable roots; ask before touching anything else.

## Execution defaults
- Use Python scripts/notebooks already here; no package installs or network calls unless approved.
- Prefer fast, safe commands (`rg`, chunked reads) and avoid long-running jobs without warning.
- Keep output short; summarize command results instead of dumping huge logs.

## Data handling
- CSV shards are large; use pandas chunked reads (`chunksize`) for aggregations.
- Don’t load all shards into memory; stream and write lightweight summaries when possible.
- Treat `2011-12-csv/2011-12-29.csv` as empty (header only) unless the user provides data.

## Code/style
- Default to ASCII; add comments only when the code isn’t self-explanatory.
- Keep new files small and purposeful; prefer scripts over sprawling notebooks for automation.

## Testing
- Run only relevant checks; if something is slow/heavy, note it and ask before running.
