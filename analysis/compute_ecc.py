"""
Envelope Correlation Coefficient (ECC) from S-parameters.

For a two-port MIMO antenna the ECC can be computed directly from the
scattering matrix:

                 | S11* S12  +  S21* S22 |^2
    ECC = ------------------------------------------------
          (1 - |S11|^2 - |S21|^2)(1 - |S22|^2 - |S12|^2)

ECC quantifies how correlated the radiation patterns of two elements are.
Uncorrelated elements give independent fading paths, which is the entire point
of MIMO. ECC < 0.5 is the usual acceptance threshold; this design achieves
ECC < 0.1 across its operating bands.

Note: the S-parameter method assumes lossless, highly efficient elements. For a
lossy substrate such as FR4 it is a good approximation but the far-field
integration method is more rigorous.

Usage:
    python analysis/compute_ecc.py --data data/s_parameters.csv
"""

import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUTPUT_DIR = "outputs"
ECC_LIMIT = 0.5


def to_complex(df, name):
    """Build a complex S-parameter from whatever form the CSV provides."""
    upper = {c.strip().upper(): c for c in df.columns}
    key = name.upper()

    # Preferred: explicit real / imaginary columns
    re_col = upper.get(f"RE({key})") or upper.get(f"{key}_RE")
    im_col = upper.get(f"IM({key})") or upper.get(f"{key}_IM")
    if re_col and im_col:
        return df[re_col].to_numpy(float) + 1j * df[im_col].to_numpy(float)

    # Next: magnitude in dB plus phase in degrees
    db_col = upper.get(key) or upper.get(f"{key}_DB")
    ph_col = upper.get(f"{key}_PHASE") or upper.get(f"ANG({key})")
    if db_col and ph_col:
        mag = 10 ** (df[db_col].to_numpy(float) / 20)
        phase = np.deg2rad(df[ph_col].to_numpy(float))
        return mag * np.exp(1j * phase)

    # Fallback: magnitude only. Phase is unknown, so ECC is an approximation.
    if db_col:
        return 10 ** (df[db_col].to_numpy(float) / 20) + 0j

    raise SystemExit(
        f"Could not find {name} in the CSV. Columns present: {list(df.columns)}"
    )


def ecc_from_s(s11, s12, s21, s22):
    numerator = np.abs(np.conj(s11) * s12 + np.conj(s21) * s22) ** 2
    denominator = (
        (1 - np.abs(s11) ** 2 - np.abs(s21) ** 2)
        * (1 - np.abs(s22) ** 2 - np.abs(s12) ** 2)
    )
    with np.errstate(divide="ignore", invalid="ignore"):
        ecc = numerator / denominator
    # Outside the matched band the denominator can go non-physical
    ecc[~np.isfinite(ecc)] = np.nan
    ecc[(ecc < 0) | (ecc > 1)] = np.nan
    return ecc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/s_parameters.csv")
    args = parser.parse_args()

    if not os.path.exists(args.data):
        raise SystemExit(
            f"No data at {args.data}\n"
            "Export the full S-parameter matrix (S11, S12, S21, S22) from CST, "
            "ideally with real/imaginary or magnitude+phase columns."
        )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(args.data)

    freq_col = next(
        (c for c in df.columns if c.strip().lower().startswith(("freq", "f "))), None
    )
    if freq_col is None:
        raise SystemExit(f"No frequency column found. Columns: {list(df.columns)}")
    freq = df[freq_col].to_numpy(float)

    s11 = to_complex(df, "S11")
    s12 = to_complex(df, "S12")
    s21 = to_complex(df, "S21")
    s22 = to_complex(df, "S22")

    ecc = ecc_from_s(s11, s12, s21, s22)
    diversity_gain = 10 * np.sqrt(1 - np.nan_to_num(ecc) ** 2)

    valid = ~np.isnan(ecc)
    if valid.any():
        print("=== Envelope Correlation Coefficient ===")
        print(f"  Points evaluated : {valid.sum()} of {len(ecc)}")
        print(f"  Max ECC          : {np.nanmax(ecc):.4f}")
        print(f"  Mean ECC         : {np.nanmean(ecc):.4f}")
        print(f"  Threshold        : {ECC_LIMIT}")
        verdict = "PASS" if np.nanmax(ecc) < ECC_LIMIT else "FAIL"
        print(f"  Verdict          : {verdict}")
        print(f"  Min diversity gain: {np.nanmin(diversity_gain):.2f} dB")
    else:
        print("No physically valid ECC values - check the S-parameter columns.")

    out_csv = f"{OUTPUT_DIR}/ecc.csv"
    pd.DataFrame(
        {"frequency_ghz": freq, "ecc": ecc, "diversity_gain_db": diversity_gain}
    ).to_csv(out_csv, index=False)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(freq, ecc, linewidth=1.6, label="ECC")
    ax.axhline(
        ECC_LIMIT, color="crimson", linestyle="--", linewidth=1,
        label=f"acceptance limit ({ECC_LIMIT})",
    )
    ax.axhline(0.1, color="tab:green", linestyle=":", linewidth=1, label="design target (0.1)")
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("ECC")
    ax.set_title("Envelope correlation coefficient")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/ecc.png", dpi=150)

    print(f"\nWritten to {out_csv} and {OUTPUT_DIR}/ecc.png")


if __name__ == "__main__":
    main()
