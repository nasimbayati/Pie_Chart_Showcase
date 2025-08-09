"""
Pie Chart Showcase (GitHub‑ready)
---------------------------------
Original mini‑project demonstrating a clean, publication‑quality
**pie chart** with custom colors, value + percent labels, and optional
PNG export for README previews.

Run:
    python pie_chart_showcase.py

Save a PNG for GitHub README:
    python -c "import pie_chart_showcase as p; p.main(save_png=True)"
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt


# ----------------- data synthesis -------------------------------------------
@dataclass
class Slice:
    label: str
    value: float


def make_dataset(seed: int = 11) -> List[Slice]:
    """Create a synthetic, non‑course dataset.

    We model fictional market share for 6 products. Values are normalized to
    sum to ~100 for intuitive labels.
    """
    rng = np.random.default_rng(seed)
    raw = rng.uniform(8, 30, size=6)  # six positive values
    raw[0] += 10  # make one a little larger to test explode visuals
    total = raw.sum()
    pct = raw / total * 100
    labels = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot"]
    return [Slice(l, float(v)) for l, v in zip(labels, pct)]


# ----------------- plotting helpers -----------------------------------------
PALETTE = [
    "#5B8FF9",  # blue
    "#5AD8A6",  # green
    "#5D7092",  # slate
    "#F6BD16",  # yellow
    "#E8684A",  # red
    "#6DC8EC",  # light blue
]


def autopct_with_value(values: List[float]):
    # values expected to be *percentages* already
    def _fmt(pct):
        # Recompute to avoid rounding drift
        absolute = pct
        if pct < 5:
            return f"{pct:.1f}%"  # tiny slice: only percent
        return f"{pct:.1f}%"
    return _fmt


# ----------------- main ------------------------------------------------------

def main(*, save_png: bool = False) -> None:
    data = make_dataset()

    labels = [s.label for s in data]
    values = [s.value for s in data]  # these are already in percent

    # explode the largest slice slightly for emphasis
    largest_idx = int(np.argmax(values))
    explode = [0.06 if i == largest_idx else 0.02 for i in range(len(values))]

    fig, ax = plt.subplots(figsize=(7.0, 5.2))

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct=autopct_with_value(values),
        startangle=115,
        colors=PALETTE,
        explode=explode,
        pctdistance=0.7,
        labeldistance=1.05,
        counterclock=False,
    )

    # style labels
    plt.setp(texts, fontsize=10)
    plt.setp(autotexts, fontsize=10, weight="bold")

    ax.set_title("Market Share by Product (synthetic)")
    ax.axis("equal")  # perfect circle
    ax.legend(wedges, labels, title="Products", loc="center left", bbox_to_anchor=(1.02, 0.5))

    if save_png:
        fig.savefig("pie_chart_showcase.png", dpi=160, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
