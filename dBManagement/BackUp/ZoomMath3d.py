import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

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

# Function to compute spherical linear interpolation (Slerp)
def slerp(p, q, t):
    # Normalize the vectors
    p_norm = p / np.linalg.norm(p)
    q_norm = q / np.linalg.norm(q)

    # Compute the dot product and angle
    dot = np.dot(p_norm, q_norm)
    dot = np.clip(dot, -1.0, 1.0)  # Clip to avoid numerical errors
    
    theta = np.arccos(dot)
    
    # If theta is zero, the points are identical, return one of them
    if np.isclose(theta, 0.0):
        return p
    
    # Perform the interpolation
    sin_theta = np.sin(theta)
    a = np.sin((1 - t) * theta) / sin_theta
    b = np.sin(t * theta) / sin_theta
    
    # Perform interpolation
    interp_point = a * p_norm + b * q_norm
    
    # Scale the result to the magnitude of the original q (off-surface point)
    interp_point = interp_point / np.linalg.norm(interp_point)  # Get the magnitude of q (the off-surface point)
    return interp_point  # Scale the interpolated result

# Input coordinates for two points (x, y, z)
# First point on the surface of the sphere (unit vector)
x1, y1, z1 = -.688, 1.44, 1.22  # Example point 1 (on the surface, unit vector)

# Second point off the surface of the sphere (non-unit vector)
x2, y2, z2 = 0, 2, 4  # Example point 2 (not a unit vector)

# Create the points as numpy arrays
p = np.array([x1, y1, z1])  # First point (on the sphere)
q = np.array([x2, y2, z2])  # Second point (off the sphere)
def slerp_points(p,q):
    # Number of points to interpolate
    num_points = 10
    liftrate = 1.2
    q_mag = np.linalg.norm(q)
    p_mag = np.linalg.norm(p)
    # Generate interpolated points
    interpolated_points = []
    for t in np.linspace(0, 1, num_points):
        point = slerp(p, q, t)  # Interpolate between p and q
        liftrate = math.sin(t*math.pi/2) * ( q_mag-p_mag) + p_mag
        point = point * liftrate
        interpolated_points.append(point)
    for points in interpolated_points:
        print(points)
    # Convert list of points to array for easy plotting
    interpolated_points = np.array(interpolated_points)
    return interpolated_points

interpolated_points = slerp_points(p,q)
# Plot the blue dots at the interpolated points
ax.scatter(interpolated_points[:, 0], interpolated_points[:, 1], interpolated_points[:, 2], color='b', s=100)

# Plot the original points (for visualization)
ax.scatter(x1, y1, z1, color='g', s=200, label='Point 1 (on sphere)')
ax.scatter(x2, y2, z2, color='m', s=200, label='Point 2 (off sphere)')

# Set labels for axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Red Sphere with Interpolated Blue Dots')

# Show the plot
ax.legend()
plt.show()
