from pathlib import Path
import json
import csv
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

def detect_language(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    try:
        return detect(text)
    except LangDetectException:
        return ""

input_dir = Path("2011-12-uncompressed")
output_dir = Path("2011-12-csv-langdetect")

print("CWD:", Path.cwd())
print("Input exists:", input_dir.exists())
output_dir.mkdir(parents=True, exist_ok=True)
print("Output dir:", output_dir.resolve())

for i, json_path in enumerate(sorted(input_dir.glob("*.json")), 1):
    csv_path = output_dir / (json_path.stem + ".csv")
    if csv_path.exists():
        continue

    with csv_path.open("w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["Text", "Origin", "id", "country", "language"])

        with json_path.open("r", encoding="utf-8") as f_in:
            for line in f_in:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                text = record.get("text", "")
                msg_id = record.get("id") or record.get("id_str") or ""
                place = record.get("place") or {}
                country = place.get("country", "") if isinstance(place, dict) else ""
                lang = detect_language(text)

                writer.writerow([text, "Twitter", msg_id, country, lang])

    if i % 5 == 0:
        print(f"Processed {i} files...")

print("Done.")
