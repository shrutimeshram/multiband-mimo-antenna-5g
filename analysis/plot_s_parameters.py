"""
Plot S-parameters exported from CST Studio Suite and annotate the -10 dB bands.

The -10 dB threshold is the usual definition of "the antenna is matched here":
below it, under 10% of incident power is reflected back at the port.

Usage:
    python analysis/plot_s_parameters.py --data data/s_parameters.csv
"""

import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Design bands reported in the ICICICT 2022 paper, for reference on the plot.
DESIGN_BANDS = [
    (3.28, 3.72, "Band 1"),
    (4.33, 5.25, "Band 2"),
    (5.81, 6.00, "Band 3"),
]

OUTPUT_DIR = "outputs"


def find_bands(freq, s_db, threshold=-10.0):
    """Return contiguous frequency ranges where |S11| stays below the threshold."""
    below = s_db <= threshold
    bands = []
    start = None

    for i, flag in enumerate(below):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            bands.append((freq[start], freq[i - 1]))
            start = None
    if start is not None:
        bands.append((freq[start], freq[-1]))

    return bands


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/s_parameters.csv")
    parser.add_argument(
        "--threshold", type=float, default=-10.0, help="Matching threshold in dB"
    )
    args = parser.parse_args()

    if not os.path.exists(args.data):
        raise SystemExit(
            f"No data at {args.data}\n"
            "Export the S-parameter results from CST as CSV with a 'frequency' column "
            "(in GHz) and S-parameter columns in dB, e.g. S11, S21."
        )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(args.data)

    # Accept a few common CST export header spellings
    freq_col = next(
        (c for c in df.columns if c.strip().lower().startswith(("freq", "f "))), None
    )
    if freq_col is None:
        raise SystemExit(f"No frequency column found. Columns: {list(df.columns)}")

    freq = df[freq_col].to_numpy(dtype=float)
    s_cols = [c for c in df.columns if c.strip().upper().startswith("S") and c != freq_col]
    if not s_cols:
        raise SystemExit(f"No S-parameter columns found. Columns: {list(df.columns)}")

    fig, ax = plt.subplots(figsize=(9, 5))

    for col in s_cols:
        s_db = df[col].to_numpy(dtype=float)
        ax.plot(freq, s_db, label=col, linewidth=1.6)

        # Report measured bands for the reflection coefficient only
        if col.strip().upper() in ("S11", "S(1,1)", "S1,1"):
            bands = find_bands(freq, s_db, args.threshold)
            print(f"\n=== {col}: bands below {args.threshold:g} dB ===")
            for lo, hi in bands:
                span = hi - lo
                centre_idx = np.argmin(np.abs(freq - (lo + hi) / 2))
                print(
                    f"  {lo:.3f} - {hi:.3f} GHz   "
                    f"(bandwidth {span * 1000:.0f} MHz, "
                    f"min S11 {s_db[(freq >= lo) & (freq <= hi)].min():.2f} dB, "
                    f"centre {freq[centre_idx]:.3f} GHz)"
                )
            if not bands:
                print("  none - the antenna is not matched anywhere in this sweep")

    ax.axhline(
        args.threshold,
        color="crimson",
        linestyle="--",
        linewidth=1,
        label=f"{args.threshold:g} dB threshold",
    )

    for lo, hi, name in DESIGN_BANDS:
        ax.axvspan(lo, hi, alpha=0.10, color="tab:green")
        ax.text(
            (lo + hi) / 2,
            ax.get_ylim()[1] - 2,
            name,
            ha="center",
            fontsize=8,
            color="tab:green",
        )

    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title("Multi-band MIMO antenna - S-parameters")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()

    out = f"{OUTPUT_DIR}/s_parameters.png"
    fig.savefig(out, dpi=150)
    print(f"\nPlot written to {out}")


if __name__ == "__main__":
    main()
