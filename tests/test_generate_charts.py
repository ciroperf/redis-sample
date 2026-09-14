# Test dei grafici KPI: verifica la generazione dei PNG da un CSV di fixture.

import csv

from charts.generate_charts import generate_charts

CSV_FIELDS = ["endpoint", "item_id", "request_index", "response_time_ms"]


def _write_fixture_csv(csv_path):
    rows = []
    for endpoint, base_ms in [("/data/nocache", 100.0), ("/data/cached", 5.0)]:
        for i in range(1, 11):
            rows.append(
                {
                    "endpoint": endpoint,
                    "item_id": 1,
                    "request_index": i,
                    "response_time_ms": base_ms + i,
                }
            )

    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_generate_charts_creates_expected_png_files(tmp_path):
    csv_path = tmp_path / "results.csv"
    _write_fixture_csv(csv_path)
    output_dir = tmp_path / "output"

    generated = generate_charts(csv_path, output_dir)

    expected = {
        output_dir / "mean_response_time.png",
        output_dir / "percentiles.png",
        output_dir / "response_time_distribution.png",
    }
    assert set(generated) == expected
    for path in expected:
        assert path.exists()
        assert path.stat().st_size > 0


def test_generate_charts_missing_csv_prints_message(tmp_path, capsys):
    missing_csv = tmp_path / "does_not_exist.csv"
    output_dir = tmp_path / "output"

    generated = generate_charts(missing_csv, output_dir)

    assert generated == []
    assert not output_dir.exists()
    captured = capsys.readouterr()
    assert "CSV non trovato" in captured.out
