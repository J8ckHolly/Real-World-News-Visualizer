import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create data for a red sphere with radius 1 centered at the origin
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

# Plot the sphere in red
ax.plot_surface(x, y, z, color='r', alpha=0.6)

# Generate 20 points evenly spaced around the equator
num_points = 20
radius = 1

theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)  # Angles for points

equator_x = radius * np.cos(theta)
equator_y = radius * np.sin(theta)
equator_z = np.zeros(num_points)  # Equator is at z = 0

# Plot the blue dots on the equator
ax.scatter(equator_x, equator_y, equator_z, color='b', s=100, label='Equator Points')

# Set labels for axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Red Sphere with Equator Points')

# Show the plot
ax.legend()
plt.show()
