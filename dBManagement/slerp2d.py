import numpy as np
import matplotlib.pyplot as plt

# Define the smoothstep equation
def smoothstep(t):
    return 3*t**2 - 2*t**3

# Create an array of t values from 0 to 1
t_values = np.linspace(0, 1, 500)
y_values = smoothstep(t_values)

# Plot the function
plt.figure(figsize=(8, 6))
plt.plot(t_values, y_values, label=r'$3t^2 - 2t^3$', color='b')
plt.title("Plot of the Smoothstep Function $3t^2 - 2t^3$")
plt.xlabel("t")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.show()
