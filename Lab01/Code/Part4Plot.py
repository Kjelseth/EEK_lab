import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ==============================
# CONFIGURATION
# Number of first datapoints to skip for linear regression.
# Increase this value if you want to ignore more "non-linear" starting points.
SKIP_POINTS = 2
# ==============================

# E values
x_values = [0.001,
            1.033,
            2.008,
            3.008,
            4.002,
            5.010,
            6.040]

# V_D values
y1_values = [0.001,
             1.032,
             1.860,
             1.987,
             2.066,
             2.135,
             2.201]

# V_R values
y2_values = [0.000,
             0.000,
             0.146,
             1.019,
             1.934,
             2.875,
             3.840]

# I_D values
y3_values = [0.000,
             0.000,
             1.480,
            10.303,
            19.555,
            29.070,
            38.827]

# Convert to numpy arrays
x = np.array(x_values)
y1 = np.array(y1_values)
y2 = np.array(y2_values)
y3 = np.array(y3_values)

# Helper function for regression (skipping SKIP_POINTS points)
def linear_fit(x, y, skip=SKIP_POINTS):
    x_fit = x[skip:].reshape(-1, 1)
    y_fit = y[skip:]
    model = LinearRegression().fit(x_fit, y_fit)
    slope = model.coef_[0]
    intercept = model.intercept_
    y_pred = model.predict(x_fit)
    r2 = r2_score(y_fit, y_pred)
    return slope, intercept, r2, model

# -------- Plot 1: Voltage drops vs Source voltage --------
plt.figure(figsize=(7,5))

# Scatter
plt.scatter(x, y1, color="purple", marker="o", label="$V_D$")
plt.scatter(x, y2, color="orange", marker="o", label="$V_R$")

# Connecting lines
plt.plot(x, y1, color="purple", linestyle="-", alpha=0.7)
plt.plot(x, y2, color="orange", linestyle="-", alpha=0.7)

# Regression fits
slope1, intercept1, r2_1, model1 = linear_fit(x, y1)
slope2, intercept2, r2_2, model2 = linear_fit(x, y2)

x_line = np.linspace(x[SKIP_POINTS], x[-1], 100).reshape(-1, 1)
plt.plot(x_line, model1.predict(x_line), color="blue", linestyle="--",
         label=f"$V_D$ fit: slope={slope1:.3f}, $R^2$={r2_1:.3f}")
plt.plot(x_line, model2.predict(x_line), color="red", linestyle="--",
         label=f"$V_R$ fit: slope={slope2:.3f}, $R^2$={r2_2:.3f}")

# Labels & formatting
plt.xlabel(r"$E$ (V)", fontsize=12)
plt.ylabel("Voltage (V)", fontsize=12)
plt.title("Voltage drops vs Source voltage", fontsize=14)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

# -------- Plot 2: Diode Current vs Voltage --------
plt.figure(figsize=(7,5))

# Scatter
plt.scatter(y1, y3, color="purple", marker="o", label="$I_D$")

# Connecting line
plt.plot(y1, y3, color="purple", linestyle="-", alpha=0.7)

# Regression fit
slope3, intercept3, r2_3, model3 = linear_fit(y1, y3)
x_line2 = np.linspace(y1[SKIP_POINTS], y1[-1], 100).reshape(-1, 1)
plt.plot(x_line2, model3.predict(x_line2), color="blue", linestyle="--",
         label=f"Fit: slope={slope3:.3f}, $R^2$={r2_3:.3f}")

# Labels & formatting
plt.xlabel(r"$V_{D}$ (V)", fontsize=12)
plt.ylabel(r"$I_{D}$ (mA)", fontsize=12)
plt.title("Diode Current vs Voltage", fontsize=14)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

# -------- Plot 3: Stacked Voltages as Percentage --------
percent_VR = np.divide(y2, x, out=np.zeros_like(y2), where=x!=0) * 100
percent_VD = np.divide(y1, x, out=np.zeros_like(y1), where=x!=0) * 100

plt.figure(figsize=(8,5))

# Bars
plt.bar(x, percent_VR, color="orange", label=r"$V_R$ % of E")
plt.bar(x, percent_VD, bottom=percent_VR, color="purple", label=r"$V_D$ % of E")

# Labels & formatting
plt.xlabel(r"$E$ (V)", fontsize=12)
plt.ylabel("Percentage of E (%)", fontsize=12)
plt.title("Stacked Voltages as Percentage of Source Voltage", fontsize=14)
plt.legend()
plt.ylim(0, 110)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()

# -------- Plot 4: Voltages as Percentage --------
plt.figure(figsize=(8,5))

# Scatter + lines
plt.scatter(x, percent_VR, color="orange", marker="o", label=r"$V_R$ % of E")
plt.plot(x, percent_VR, color="orange", linestyle="-", alpha=0.8)

plt.scatter(x, percent_VD, color="purple", marker="o", label=r"$V_D$ % of E")
plt.plot(x, percent_VD, color="purple", linestyle="-", alpha=0.8)

# Labels & formatting
plt.xlabel(r"$E$ (V)", fontsize=12)
plt.ylabel("Percentage of E (%)", fontsize=12)
plt.title("Voltages as Percentage of Source Voltage", fontsize=14)
plt.legend()
plt.ylim(0, 110)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

plt.show()