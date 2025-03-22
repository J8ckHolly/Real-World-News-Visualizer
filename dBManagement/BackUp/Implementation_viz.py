import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk, filedialog

# Open file dialog
Tk().withdraw()  # Hide root window
file_path = filedialog.askopenfilename(title="Select a .txt file", filetypes=[("Text files", "*.txt")])

if not file_path:
    print("No file selected. Exiting.")
    exit()

# Load points from the file
points = np.loadtxt(file_path, delimiter=",")

# Extract x, y, z coordinates
x, y, z = points[:, 0], points[:, 1], points[:, 2]

# Create a 3D figure
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Define the colors (Yellow -> Blue)
colors = np.linspace(0, 1, len(points))
cmap = plt.get_cmap('coolwarm')

# Plot the points with color gradient
for i in range(len(points) - 1):
    ax.plot([x[i], x[i+1]], [y[i], y[i+1]], [z[i], z[i+1]],
            color=cmap(colors[i]), marker="o", linestyle="-", lw=2)

# Create a sphere of radius 1
u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 50)
X = np.outer(np.cos(u), np.sin(v))
Y = np.outer(np.sin(u), np.sin(v))
Z = np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_surface(X, Y, Z, color="r", alpha=0.3)  # Semi-transparent sphere

# Labels and title
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D Camera Path with Gradient (Yellow to Blue)")

# Show plot
plt.show()
