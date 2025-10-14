import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from scipy.signal import detrend
from scipy.fft import rfft, rfftfreq


from scipy.signal import detrend, butter, filtfilt
from scipy.fft import rfft, rfftfreq

from scipy.signal import butter, filtfilt
from scipy.fft import rfft, rfftfreq
import numpy as np

import numpy as np
from scipy.signal import correlate

def analyze_signal(time, vin, vout):
    """
    Simple time-domain analysis:
      • Finds input/output peak amplitudes
      • Computes voltage gain (linear + dB)
      • Estimates phase shift via cross-correlation
    """

    t = np.asarray(time)
    vin = np.asarray(vin)
    vout = np.asarray(vout)

    # --- Peak amplitude and gain ---
    vin_peak = np.max(np.abs(vin))
    vout_peak = np.max(np.abs(vout))
    gain_linear = vout_peak / vin_peak if vin_peak != 0 else np.nan
    gain_db = 20 * np.log10(gain_linear) if gain_linear > 0 else np.nan

    # --- Phase shift estimation ---
    corr = correlate(vout - np.mean(vout), vin - np.mean(vin))
    lag = np.argmax(corr) - (len(vin) - 1)
    dt = np.mean(np.diff(t))

    # Estimate period of the input signal
    freqs = np.fft.rfftfreq(len(t), dt)
    vin_fft = np.abs(np.fft.rfft(vin))
    vin_fft[0] = 0  # ignore DC
    f_main = freqs[np.argmax(vin_fft)]
    period = 1 / f_main if f_main > 0 else np.inf

    phase_deg = -(lag * dt / period) * 360 if np.isfinite(period) else 0.0

    return vin_peak, vout_peak, gain_linear, gain_db, phase_deg

def plot_csv(
    csv_path: str,
    output_path: str,
    time_unit: str = "ms",
    voltage_unit: str = "V",
    show: bool = False,
    reversed_io: bool = False
):
    """
    Plots transient analysis data from a CSV file with IEEE-style formatting.

    Parameters
    ----------
    csv_path : str
        Full path to the input CSV file (semicolon-separated).
    output_path : str
        Full path (including file name) for the output figure (PDF).
    time_unit : str
        Unit for time axis: "s", "ms", or "us".
    voltage_unit : str
        Unit for voltage axis: "V" or "mV".
    show : bool
        If True, display the plot instead of saving it.
    """

    # --- Validate input arguments and paths ---
    valid_time_units = ["s", "ms", "µs", "us", "ns"]
    valid_voltage_units = ["V", "mV", "µV", "uV"]

    if time_unit not in valid_time_units:
        raise ValueError(
            f"❌ Invalid time unit '{time_unit}'. Must be one of: {', '.join(valid_time_units)}"
        )

    if voltage_unit not in valid_voltage_units:
        raise ValueError(
            f"❌ Invalid voltage unit '{voltage_unit}'. Must be one of: {', '.join(valid_voltage_units)}"
        )

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ Input CSV not found: {csv_path}")

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Created missing output directory: {output_dir}")

    # --- Validate CSV structure ---
    expected_cols = 3

    try:
        df_preview = pd.read_csv(csv_path, sep=';', nrows=1, engine='python')
        # Drop "Unnamed" columns from trailing semicolons
        df_preview = df_preview.loc[:, ~df_preview.columns.str.startswith("Unnamed")]
    except Exception as e:
        raise ValueError(f"❌ Failed to read CSV header from '{csv_path}': {e}")

    header = list(df_preview.columns)

    if len(header) != expected_cols:
        raise ValueError(
            f"❌ CSV '{os.path.basename(csv_path)}' must contain exactly {expected_cols} columns "
            f"(time + 2 signals), but has {len(header)}: {header}"
        )

    if not header[0].lower().startswith("time"):
        raise ValueError(
            f"❌ First column must represent time in '{os.path.basename(csv_path)}', "
            f"found '{header[0]}' instead."
        )

    # --- Print detected signal order ---
    signal_cols = header[1:]
    print(f"📈 Detected {len(signal_cols)} signals in '{os.path.basename(csv_path)}':")
    print(f"   • {signal_cols[0]} → Input")
    print(f"   • {signal_cols[1]} → Output")
    if not reversed_io:
        print("🔁 Tip: set reversed_io=True to swap order")

    # --- Apply IEEE style ---
    style_path = os.path.join(os.path.dirname(__file__), "ieee_dark_signature.mplstyle")
    plt.style.use(style_path)

    # --- Load font by path (for local font setup) ---
    font_path = os.path.expanduser("~/Documents/Fonts/AvenirNextRegular.ttf")
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        print(f"🖋️ Using custom font: {os.path.basename(font_path)}")
    else:
        print("🖋️ Custom font not found — using default matplotlib font.")

    # --- Ensure output directory exists ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # --- Load and clean data ---
    df = pd.read_csv(csv_path, sep=';').dropna(axis=1, how='all')
    print(f"📄 Loaded data from '{os.path.basename(csv_path)}'")

    # --- Fix display units for labels ---
    time_unit = time_unit.replace("us", "µs")
    voltage_unit = voltage_unit.replace("uV", "µV")

    # --- Determine unit scaling ---
    time_scale = {"s": 1, "ms": 1e3, "µs": 1e6, "ns": 1e9}.get(time_unit, 1)
    volt_scale = {"V": 1, "mV": 1e3, "µV": 1e6}.get(voltage_unit, 1)

    # --- Prepare scaled signals ---
    time = df.iloc[:, 0] * time_scale
    signals = df.iloc[:, 1:] * volt_scale

    # --- Optionally swap Input/Output order for plotting ---
    if reversed_io:
        signals = signals.iloc[:, [1, 0]]
        print("🔁 Reversed I/O order for plotting.")

    # Auto-rename if exactly two traces
    if len(signals.columns) == 2:
        signals.columns = ["Input", "Output"]

    # --- Signal arrays for analysis ---
    vin = signals.iloc[:, 0].to_numpy()
    vout = signals.iloc[:, 1].to_numpy()

    # --- FFT-based analysis ---
    vin_peak, vout_peak, gain_linear, gain_db, phase_deg = analyze_signal(time, vin, vout)
    print("📊 Time-domain analysis:")
    print(f"   • Input peak: {vin_peak:.3f} {voltage_unit}")
    print(f"   • Output peak: {vout_peak:.3f} {voltage_unit}")
    print(f"   • Gain: {gain_linear:.2f}×  ({gain_db:.2f} dB)")
    print(f"   • Phase shift: {phase_deg:+.1f}°")

    # --- Plot ---
    plt.figure(figsize=(4.0, 3.0), dpi=300)
    for col in signals.columns:
        plt.plot(time, signals[col], label=col)

    plt.xlabel(f"Time, {time_unit}")
    plt.ylabel(f"Voltage, {voltage_unit}")

    # --- Legend in (best) corner ---
    legend_best_corner(fallback='upper right')
    
    plt.margins(x=0.002, y=0.05)
    plt.grid(True)
    plt.tight_layout(pad=0.1)

    if show:
        plt.show()
        print("👀 Displayed plot (not saved).")
    else:
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()
        print(f"✅ Plot saved successfully → {os.path.basename(output_path)}\n")


def legend_best_corner(ax=None, fallback='upper right'):
    """
    Place legend with 'best'. If its final position isn't near a corner,
    move it to `fallback`.
    """
    ax = ax or plt.gca()
    leg = ax.legend(
        loc='best',
        frameon=True,
        facecolor='white',
        framealpha=0.9,
        handlelength=1.5
    )

    # Force a draw so the legend’s position is computed
    ax.figure.canvas.draw()

    # Get the bounding box of the legend in figure coordinates
    bbox = leg.get_window_extent(ax.figure.canvas.get_renderer())
    bbox_fig = bbox.transformed(ax.figure.transFigure.inverted())

    # Legend center coordinates (0–1 range)
    cx, cy = bbox_fig.x0 + bbox_fig.width / 2, bbox_fig.y0 + bbox_fig.height / 2

    # Define which zones count as "corners"
    corner_margin = 0.25  # top/bottom 25% and left/right 25% of figure
    in_corner = (
        (cx < corner_margin or cx > 1 - corner_margin)
        and (cy < corner_margin or cy > 1 - corner_margin)
    )

    if not in_corner:
        leg.remove()
        leg = ax.legend(
            loc=fallback,
            frameon=True,
            facecolor='white',
            framealpha=0.9,
            handlelength=1.5
        )
        ax.figure.canvas.draw()

    return leg

# ----------------------------------------------------------
# Example usage / quick self-test
# ----------------------------------------------------------
def main():

    print("🧪 Running in demo mode — generating example transient data...")

    # --- Create a small fake transient dataset ---
    t = np.linspace(0, 2e-3, 2000)
    vin = 0.5 * np.sin(2 * np.pi * 2e3 * t)
    vout = -10 * vin * np.exp(-t / 1e-3)

    df_example = pd.DataFrame({
        "time": t,
        "V(input)": vin,
        "V(output)": vout
    })

    # --- Save fake CSV temporarily ---
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "../Data")
    figs_dir = os.path.join(base_dir, "../Figures")
    os.makedirs(data_dir, exist_ok=True)

    fake_csv_path = os.path.join(data_dir, "TEST_FAKE_TRAN.csv")
    df_example.to_csv(fake_csv_path, sep=';', index=False)

    try:
        # --- Run the plotter in demo mode (show only) ---
        plot_csv(
            csv_path=fake_csv_path,
            output_path=os.path.join(figs_dir, "TransientPlot_Example.pdf"),
            time_unit="ms",
            voltage_unit="V",
            show=True
        )
    finally:
        if os.path.exists(fake_csv_path):
            os.remove(fake_csv_path)
            print(f"🧹 Temporary file removed: '{os.path.basename(fake_csv_path)}'")
    
    print("✅ Demo complete.")


if __name__ == "__main__":
    main()