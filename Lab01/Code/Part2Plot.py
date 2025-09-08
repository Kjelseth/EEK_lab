import matplotlib.pyplot as plt
import numpy as np

# V_D values
x_values = [0, # Extended to origin
            0.507,
            0.538,
            0.556,
            0.57,
            0.58,
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

# Convert to numpy arrays for calculations
x = np.array(x_values)
y = np.array(y_values)

# --- Plot settings ---
plt.figure(figsize=(7,5))

# Scatter plot of points
plt.scatter(x, y, color="blue", marker="o", label="Data points")

# Connect points with a line
plt.plot(x, y, color="purple", linestyle="-", alpha=0.7)

# Axis labels with subscript (using LaTeX formatting)
plt.xlabel(r"$V_{D}$ (V)", fontsize=12)
plt.ylabel(r"$I_{D}$ (mA)", fontsize=12)

# Formatting
plt.title("Forward-bias charachteristics", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

plt.show()