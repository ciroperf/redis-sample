# Raccoglie i tempi di risposta degli endpoint cached/no-cache in un CSV.
# Implementazione nei task del piano, non qui.

import csv
from pathlib import Path
from typing import List, Dict, Any

CSV_FIELDS = ["endpoint", "item_id", "request_index", "response_time_ms"]


def write_results_csv(output_path: Path, rows: List[Dict[str, Any]]) -> None:
    """Write benchmark results to a CSV file."""
    with open(output_path, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
