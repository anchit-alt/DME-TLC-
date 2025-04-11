import numpy as np
import matplotlib.pyplot as plt

# Take user inputs
L = float(input("Enter the beam length L (in mm): "))
a = float(input("Enter the load position a (in mm): "))
P = float(input("Enter the load (KN) "))

# Validate: a should not exceed L
if a > L:
    print("Error: Load position 'a' cannot be greater than beam length 'L'.")
else:
    # Define x range based on beam length
    x = np.linspace(0, L, 1000)

    # Define V(x) and M(x)
    V = np.where(x < a, P, 0)
    M = np.where(x <= a, P * x, P * a)

    # Plot V(x)
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(x, V, color='blue', linewidth=2, label='V(x)')
    plt.axvline(x=a, color='red', linestyle='--', label=f'Load at x = {a} mm')
    plt.title('Shear Force Diagram')
    plt.ylabel('V (N)')
    plt.grid(True)
    plt.legend()

    # Plot M(x)
    plt.subplot(2, 1, 2)
    plt.plot(x, M, color='green', linestyle='--', linewidth=2, label='M(x)')
    plt.axvline(x=a, color='red', linestyle='--', label=f'Load at x = {a} mm')
    plt.title('Bending Moment Diagram')
    plt.xlabel('x (mm)')
    plt.ylabel('M (N·mm)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
