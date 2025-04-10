import numpy as np
import matplotlib.pyplot as plt

# Take load position as input
a = float(input("Enter the load position a (in mm) [0–500]: "))
P = float(input("Enter load (KN) "))

# x range
x = np.linspace(0, 500, 1000)

# Define V(x): Shear force

V = np.where(x < a, P, 0)

# Define M(x): Bending moment
M = np.where(x <= a, P * x, P * a)

# Plot V(x)
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(x, V, color='blue', linewidth=2, label='V(x)')
plt.axvline(x=a, color='red', linestyle='--', label=f'x = a = {a} mm')
plt.title('Shear Force Diagram')
plt.ylabel('V')
plt.grid(True)
plt.legend()

# Plot M(x)
plt.subplot(2, 1, 2)
plt.plot(x, M, color='green', linestyle='--', linewidth=2, label='M(x)')
plt.axvline(x=a, color='red', linestyle='--', label=f'x = a = {a} mm')
plt.title('Bending Moment Diagram')
plt.xlabel('x (mm)')
plt.ylabel('M')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
