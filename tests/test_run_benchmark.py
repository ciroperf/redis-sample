# Test dello script di benchmark: verifica la scrittura del CSV senza server.

import csv

from benchmark.run_benchmark import CSV_FIELDS, write_results_csv


def test_write_results_csv_header(tmp_path):
    output_path = tmp_path / "results.csv"
    rows = [
        {
            "endpoint": "/data/nocache",
            "item_id": 1,
            "request_index": 1,
            "response_time_ms": 12.3,
        }
    ]

    write_results_csv(output_path, rows)

    with open(output_path, newline="") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)

    assert header == CSV_FIELDS
