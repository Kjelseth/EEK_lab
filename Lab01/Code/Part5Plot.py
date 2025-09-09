import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ==============================
# CONFIGURATION
# Number of first datapoints to skip for linear regression.
# Increase this value if you want to ignore more "non-linear" starting points.
SKIP_POINTS = 10
# ==============================

# E values
x_values = [ 00.001,
             01.004,
             02.009,
             03.008,
             04.040,
             05.020,
             06.010,
             07.000,
             08.020,
             09.060,
             09.990,
             11.050,
             12.010]

# V_Z values
y1_values = [ 00.001,
              01.004,
              02.008,
              03.007,
              04.040,
              05.020,
              06.010,
              07.000,
              08.020,
              09.060,
              09.940,
              10.160,
              10.360]

# V_R values
y2_values = [ 00.0000,
              00.0000,
              00.0000,
              00.0000,
              00.0000,
              00.0000,
              00.0000,
              00.0000,
              00.0000,
              00.0000,
              00.0526,
              00.8830,
              01.6280]

# I_Z values
y3_values = [ 00.000000000,
              00.000000000,
              00.000000000,
              00.000000000,
              00.000000000,
              00.000000000,
              00.000000000,
              00.000000000,
              00.000000000,
              00.000000000,
              00.531850354,
              08.928210313,
              16.461071790]


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
plt.scatter(x, y1, color="purple", marker="o", label="$V_Z$")
plt.scatter(x, y2, color="orange", marker="o", label="$V_R$")

# Connecting lines
plt.plot(x, y1, color="purple", linestyle="-", alpha=0.7)
plt.plot(x, y2, color="orange", linestyle="-", alpha=0.7)

# Regression fits
slope1, intercept1, r2_1, model1 = linear_fit(x, y1)
slope2, intercept2, r2_2, model2 = linear_fit(x, y2)

x_line = np.linspace(x[SKIP_POINTS], x[-1], 100).reshape(-1, 1)
plt.plot(x_line, model1.predict(x_line), color="blue", linestyle="--",
         label=f"$V_Z$ fit: slope={slope1:.3f}, $R^2$={r2_1:.3f}")
plt.plot(x_line, model2.predict(x_line), color="red", linestyle="--",
         label=f"$V_R$ fit: slope={slope2:.3f}, $R^2$={r2_2:.3f}")

# Labels & formatting
plt.xlabel(r"$E$ (V)", fontsize=12)
plt.ylabel("Voltage (V)", fontsize=12)
plt.title("Voltage drops vs source voltage", fontsize=14)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

# -------- Plot 2: Diode Current vs Voltage --------
plt.figure(figsize=(7,5))

# Scatter
plt.scatter(y1, y3, color="purple", marker="o", label="$I_Z$")

# Connecting line
plt.plot(y1, y3, color="purple", linestyle="-", alpha=0.7)

# Regression fit
slope3, intercept3, r2_3, model3 = linear_fit(y1, y3)
x_line2 = np.linspace(y1[SKIP_POINTS], y1[-1], 100).reshape(-1, 1)
plt.plot(x_line2, model3.predict(x_line2), color="blue", linestyle="--",
         label=f"$I_Z$ fit: slope={slope3:.3f}, $R^2$={r2_3:.3f}")

# Labels & formatting
plt.xlabel(r"$V_{Z}$ (V)", fontsize=12)
plt.ylabel(r"$I_{Z}$ (mA)", fontsize=12)
plt.title("Diode current vs voltage", fontsize=14)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

# -------- Plot 3: Stacked Voltages as Percentage --------
percent_VR = np.divide(y2, x, out=np.zeros_like(y2), where=x!=0) * 100
percent_VD = np.divide(y1, x, out=np.zeros_like(y1), where=x!=0) * 100

plt.figure(figsize=(8,5))

# Bars
plt.bar(x, percent_VR, color="orange", label=r"$V_R$ % of E")
plt.bar(x, percent_VD, bottom=percent_VR, color="purple", label=r"$V_Z$ % of E")

# Labels & formatting
plt.xlabel(r"$E$ (V)", fontsize=12)
plt.ylabel("Percentage of E (%)", fontsize=12)
plt.title("Stacked voltages as percentage of source voltage", fontsize=14)
plt.legend()
plt.ylim(0, 110)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()

plt.show()