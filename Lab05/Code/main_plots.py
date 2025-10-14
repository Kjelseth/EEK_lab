import os
from plot_csv import plot_csv

# --- Define directories ---
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "../Data")
figs_dir = os.path.join(base_dir, "../Figures")

# --- Plot calls ---
plot_csv(
    csv_path=os.path.join(data_dir, "TransientInverting.csv"),
    output_path=os.path.join(figs_dir, "TransientPlot_Inverting.pdf"),
    time_unit="ms",
    voltage_unit="V"
)

plot_csv(
    csv_path=os.path.join(data_dir, "TransientNonInverting.csv"),
    output_path=os.path.join(figs_dir, "TransientPlot_NonInverting.pdf"),
    time_unit="ms",
    voltage_unit="V",
    reversed_io="true"
)

plot_csv(
    csv_path=os.path.join(data_dir, "TransientInstrumentation.csv"),
    output_path=os.path.join(figs_dir, "TransientPlot_Instrumentation.pdf"),
    time_unit="ms",
    voltage_unit="mV",
    reversed_io="true"
)