# Raccoglie i tempi di risposta degli endpoint cached/no-cache in un CSV.

import argparse
import csv
import statistics
import time
from pathlib import Path

import requests

CSV_FIELDS = ["endpoint", "item_id", "request_index", "response_time_ms"]
ENDPOINTS = ["/data/nocache", "/data/cached"]
DEFAULT_ITEM_ID = 1


def measure_endpoint(base_url: str, endpoint: str, item_id: int, n: int) -> list[dict]:
    """Esegue n richieste sull'endpoint e restituisce le righe di risultato."""
    url = f"{base_url.rstrip('/')}{endpoint}/{item_id}"
    rows = []
    for request_index in range(1, n + 1):
        start = time.perf_counter()
        response = requests.get(url)
        response.raise_for_status()
        elapsed_ms = (time.perf_counter() - start) * 1000
        rows.append(
            {
                "endpoint": endpoint,
                "item_id": item_id,
                "request_index": request_index,
                "response_time_ms": elapsed_ms,
            }
        )
    return rows


def write_results_csv(path: Path, rows: list[dict]) -> None:
    """Scrive le righe di risultato su CSV con l'intestazione attesa."""
    with open(path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def compute_stats(response_times_ms: list[float]) -> dict:
    """Calcola media, p50 e p95 di una lista di tempi di risposta."""
    sorted_times = sorted(response_times_ms)
    return {
        "mean": statistics.mean(sorted_times),
        "p50": statistics.median(sorted_times),
        "p95": sorted_times[max(0, int(len(sorted_times) * 0.95) - 1)],
    }


def print_summary(rows: list[dict]) -> None:
    for endpoint in ENDPOINTS:
        times = [row["response_time_ms"] for row in rows if row["endpoint"] == endpoint]
        if not times:
            continue
        stats = compute_stats(times)
        print(
            f"{endpoint}: "
            f"mean={stats['mean']:.2f}ms p50={stats['p50']:.2f}ms p95={stats['p95']:.2f}ms"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark degli endpoint cached/no-cache")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL dell'API")
    parser.add_argument("-n", "--requests", type=int, default=50, help="Numero di richieste per endpoint")
    parser.add_argument(
        "--output",
        default=str(Path(__file__).parent / "results.csv"),
        help="Percorso del CSV di output",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = []
    for endpoint in ENDPOINTS:
        rows.extend(measure_endpoint(args.base_url, endpoint, DEFAULT_ITEM_ID, args.requests))

    write_results_csv(Path(args.output), rows)
    print(f"Risultati salvati in {args.output}")
    print_summary(rows)


if __name__ == "__main__":
    main()
