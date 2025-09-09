import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# V_D values
x_values = [0.000, # Extended to origin
            0.507,
            0.538,
            0.556,
            0.570,
            0.580,
            0.589,
            0.596,
            0.602,
            0.607,
            0.612,
            0.645,
            0.665,
            0.678,
            0.689]

# I_D calues
y_values = [0, # Extended to origin
            0.107356066,
            0.209349388,
            0.304664576,
            0.403723566,
            0.509966609,
            0.614185976,
            0.707275119,
            0.810482647,
            0.915713852,
            1.017909542,
            2.022665183,
            3.041586563,
            4.048365881,
            5.059192553] # I_D

# --- Convert to numpy arrays ---
x = np.array(x_values)
y = np.array(y_values)

# --- Plot 1: Original data only ---
plt.figure(figsize=(7,5))
plt.scatter(x, y, color="purple", marker="o", label="$I_D$")
plt.plot(x, y, color="purple", linestyle="-", alpha=0.7)
plt.xlabel(r"$V_{D}$ (V)", fontsize=12)
plt.ylabel(r"$I_{D}$ (mA)", fontsize=12)
plt.title("Forward-bias characteristics (Data only)", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# --- Define exponential function ---
def exp_func(x, a, b):
    return a * np.exp(b * x)

# --- Fit the exponential curve ---
params, covariance = curve_fit(exp_func, x, y, p0=(1e-6, 20))  # initial guess
y_fit = exp_func(x, *params)

# Calculate R^2
r2 = r2_score(y, y_fit)

# Format 'a' in scientific notation automatically
a_sci = "{:.2e}".format(params[0])

# --- Plot 2: Data + Exponential Regression ---
plt.figure(figsize=(7,5))
plt.scatter(x, y, color="purple", marker="o", label="$I_D$")
plt.plot(x, y, color="purple", linestyle="-", alpha=0.7)
plt.plot(x, y_fit, color="blue", linestyle="--",
         label=f"$I_D$ fit: exp = {a_sci}·e^({params[1]:.3f}·$V_D$)\n$R^2$ = {r2:.4f}")
plt.xlabel(r"$V_{D}$ (V)", fontsize=12)
plt.ylabel(r"$I_{D}$ (mA)", fontsize=12)
plt.title("Forward-bias characteristics (With regression)", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()