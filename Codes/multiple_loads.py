import numpy as np
import matplotlib.pyplot as plt

# Function to calculate reactions at the fixed support
def calculate_reactions(loads, positions, beam_length):
    R_A = sum(loads)  # Total reaction force at A
    M_A = sum([P * x for P, x in zip(loads, positions)])  # Total moment at A
    return R_A, M_A

# Function to compute Shear Force at different points
def shear_force_diagram(loads, positions, beam_length):
    x_vals = np.linspace(0, beam_length, 1000)  # Points along the beam
    shear_forces = []

    for x in x_vals:
        V = sum(load for load, pos in zip(loads, positions) if pos > x)  # Summing all loads after x
        shear_forces.append(V)

    return x_vals, shear_forces

# Function to compute Bending Moment at different points
def bending_moment_diagram(loads, positions, beam_length, R_A):
    x_vals = np.linspace(0, beam_length, 1000)  # Points along the beam
    bending_moments = []

    for x in x_vals:
        M = R_A * x - sum(load * (x - pos) for load, pos in zip(loads, positions) if x >= pos)  # Moment equation
        bending_moments.append(M)

    return x_vals, bending_moments

# Get user input
beam_length = float(input("Enter the length of the beam: "))
num_loads = int(input("Enter the number of point loads: "))

loads = []
positions = []

for i in range(num_loads):
    P = float(input(f"Enter magnitude of load {i+1} (N): "))
    x = float(input(f"Enter position of load {i+1} (m): "))
    loads.append(P)
    positions.append(x)

# Calculate reactions
R_A, M_A = calculate_reactions(loads, positions, beam_length)

# Compute shear force and bending moment values
x_shear, shear_forces = shear_force_diagram(loads, positions, beam_length)
x_moment, bending_moments = bending_moment_diagram(loads, positions, beam_length, R_A)

# Plot Shear Force Diagram (SFD)
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(x_shear, shear_forces, label="Shear Force", color='blue', linewidth=2)
plt.fill_between(x_shear, shear_forces, alpha=0.3, color='blue')
plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel("Beam Length (m)")
plt.ylabel("Shear Force (N)")
plt.title("Shear Force Diagram (SFD)")
plt.legend()
plt.grid()

# Plot Bending Moment Diagram (BMD)
plt.subplot(2, 1, 2)
plt.plot(x_moment, bending_moments, label="Bending Moment", color='red', linewidth=2)
plt.fill_between(x_moment, bending_moments, alpha=0.3, color='red')
plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel("Beam Length (m)")
plt.ylabel("Bending Moment (Nm)")
plt.title("Bending Moment Diagram (BMD)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
