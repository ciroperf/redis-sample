# Legge il CSV del benchmark e genera i grafici KPI.

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

ENDPOINTS = ["/data/nocache", "/data/cached"]
ENDPOINT_LABELS = {"/data/nocache": "Senza cache", "/data/cached": "Cache Redis"}
ENDPOINT_COLORS = {"/data/nocache": "#2a78d6", "/data/cached": "#eb6834"}
PERCENTILES = [50, 95, 99]

TEXT_PRIMARY = "#0b0b0b"
TEXT_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
SURFACE = "#fcfcfb"

DEFAULT_CSV = Path(__file__).parent.parent / "benchmark" / "results.csv"
DEFAULT_OUTPUT_DIR = Path(__file__).parent / "output"


def load_response_times(csv_path: Path) -> dict[str, list[float]]:
    """Legge il CSV e raggruppa i tempi di risposta per endpoint."""
    times_by_endpoint: dict[str, list[float]] = defaultdict(list)
    with open(csv_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            times_by_endpoint[row["endpoint"]].append(float(row["response_time_ms"]))
    return times_by_endpoint


def _style_axes(ax) -> None:
    ax.set_facecolor(SURFACE)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRIDLINE)
    ax.tick_params(colors=TEXT_MUTED)
    ax.yaxis.grid(True, color=GRIDLINE, linewidth=1)
    ax.set_axisbelow(True)


def plot_mean_comparison(times_by_endpoint: dict[str, list[float]], output_dir: Path) -> Path:
    """Grafico a barre dei tempi medi di risposta, cached vs nocache."""
    endpoints = [e for e in ENDPOINTS if e in times_by_endpoint]
    means = [float(np.mean(times_by_endpoint[e])) for e in endpoints]
    colors = [ENDPOINT_COLORS[e] for e in endpoints]
    labels = [ENDPOINT_LABELS[e] for e in endpoints]

    fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=SURFACE)
    _style_axes(ax)
    bars = ax.bar(labels, means, width=0.5, color=colors)
    for bar, mean in zip(bars, means):
        ax.annotate(
            f"{mean:.1f} ms",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            color=TEXT_PRIMARY,
        )

    ax.set_title("Tempo medio di risposta: cache vs no cache", color=TEXT_PRIMARY)
    ax.set_ylabel("Tempo medio (ms)", color=TEXT_MUTED)

    output_path = output_dir / "mean_response_time.png"
    fig.tight_layout()
    fig.savefig(output_path, facecolor=SURFACE)
    plt.close(fig)
    return output_path


def plot_percentiles(times_by_endpoint: dict[str, list[float]], output_dir: Path) -> Path:
    """Grafico a barre raggruppate dei percentili p50/p95/p99 per endpoint."""
    endpoints = [e for e in ENDPOINTS if e in times_by_endpoint]
    x = np.arange(len(PERCENTILES))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=SURFACE)
    _style_axes(ax)
    offsets = np.linspace(-bar_width / 2, bar_width / 2, num=len(endpoints), endpoint=len(endpoints) > 1)
    for endpoint, offset in zip(endpoints, offsets):
        values = [float(np.percentile(times_by_endpoint[endpoint], p)) for p in PERCENTILES]
        ax.bar(
            x + offset,
            values,
            width=bar_width / max(len(endpoints), 1),
            label=ENDPOINT_LABELS[endpoint],
            color=ENDPOINT_COLORS[endpoint],
        )

    ax.set_title("Percentili del tempo di risposta", color=TEXT_PRIMARY)
    ax.set_ylabel("Tempo di risposta (ms)", color=TEXT_MUTED)
    ax.set_xticks(x)
    ax.set_xticklabels([f"p{p}" for p in PERCENTILES], color=TEXT_MUTED)
    ax.legend(frameon=False, labelcolor=TEXT_PRIMARY)

    output_path = output_dir / "percentiles.png"
    fig.tight_layout()
    fig.savefig(output_path, facecolor=SURFACE)
    plt.close(fig)
    return output_path


def plot_distribution(times_by_endpoint: dict[str, list[float]], output_dir: Path) -> Path:
    """Distribuzione dei tempi di risposta per endpoint (istogrammi affiancati)."""
    endpoints = [e for e in ENDPOINTS if e in times_by_endpoint]
    fig, axes = plt.subplots(
        1, len(endpoints), figsize=(6 * len(endpoints), 4.5), facecolor=SURFACE, sharey=True
    )
    if len(endpoints) == 1:
        axes = [axes]

    for ax, endpoint in zip(axes, endpoints):
        _style_axes(ax)
        ax.hist(times_by_endpoint[endpoint], bins=20, color=ENDPOINT_COLORS[endpoint])
        ax.set_title(ENDPOINT_LABELS[endpoint], color=TEXT_PRIMARY)
        ax.set_xlabel("Tempo di risposta (ms)", color=TEXT_MUTED)

    axes[0].set_ylabel("Numero di richieste", color=TEXT_MUTED)
    fig.suptitle("Distribuzione dei tempi di risposta", color=TEXT_PRIMARY)

    output_path = output_dir / "response_time_distribution.png"
    fig.tight_layout()
    fig.savefig(output_path, facecolor=SURFACE)
    plt.close(fig)
    return output_path


def generate_charts(csv_path: Path, output_dir: Path) -> list[Path]:
    """Genera tutti i grafici KPI a partire dal CSV del benchmark."""
    if not csv_path.exists():
        print(f"CSV non trovato: {csv_path}. Esegui prima benchmark/run_benchmark.py.")
        return []

    times_by_endpoint = load_response_times(csv_path)
    if not times_by_endpoint:
        print(f"Il CSV {csv_path} non contiene righe di dati.")
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    return [
        plot_mean_comparison(times_by_endpoint, output_dir),
        plot_percentiles(times_by_endpoint, output_dir),
        plot_distribution(times_by_endpoint, output_dir),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera i grafici KPI dal CSV del benchmark")
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=str(DEFAULT_CSV),
        help="Percorso del CSV del benchmark (default: benchmark/results.csv)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Cartella di output per i grafici (default: charts/output)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated = generate_charts(Path(args.csv_path), Path(args.output_dir))
    for path in generated:
        print(f"Grafico salvato in {path}")


if __name__ == "__main__":
    main()
