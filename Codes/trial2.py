import pandas as pd
import math 

# Load data
A31 = pd.read_csv("Data/nominal_sizes_mm.csv")
table_8_1 = pd.read_csv("Data/screw_thread_data.csv")

# User input
type_of_nut = input("Type of Nut (e.g., M10): ")
print("Selected Nut:", type_of_nut)

d = float(type_of_nut.removeprefix("M"))  # Convert to float
print("Nominal Diameter d:", d)

l = float(input("Enter length of steel plates: "))

# Find Regular Hexagonal Value
H = A31.loc[A31["Nominal Size (mm)"] == type_of_nut, "Regular Hexagonal"]
if not H.empty:
    H = float(H.values[0])  # Extract float value
    print(f"Regular Hexagonal value for {type_of_nut}: {H}")
else:
    print("Nominal size not found")
    exit()

# Calculate Total Bolt Length
L = 2 * l + H
print("Initial Bolt Length:", L)

# Rounding function
def myround(x, base=5):
    return base * round(x / base)

L = myround(L)  # Ensure L is a scalar
print("Rounded Bolt Length:", L)

# Determine Thread Length (L_T)
if L <= 125:
    L_T = 2 * d + 6
elif 125 < L <= 200:
    L_T = 2 * d + 12
else:
    L_T = 2 * d + 25

print("Thread Length L_T:", L_T)

# Calculate Lengths of Threaded and Unthreaded Portions
l_d = L - L_T
print("Length of Unthreaded Portion (Grip):", l_d)

l_t = 2*l - l_d
print("Length of Threaded Portion in Grip:", l_t)

# Area Calculations
A_d = math.pi * pow(d, 2) / 4
print("Area of Unthreaded Portion:", A_d)

A_t = table_8_1.loc[table_8_1["Nominal Major Diameter d (mm)"] == d, "Minor-Diameter Area Ar (mm²) (Fine)"]
if not A_t.empty:
    A_t = float(A_t.values[0])
    print("Area of Threaded Portion:", A_t)
else:
    print("Nominal Major Diameter not found in table.")
    exit()

# Stiffness Calculations
E = 207

Kb = (A_d * A_t * E) / (A_d * l_t + A_t * l_d)
print("Bolt Stiffness (Kb):", Kb)

x = 2 * math.log((5 * (0.5774 * 2 * l + 0.5 * d) / (0.5774 *2* l + 2.5 * d)))
if x == 0:
    print("Warning: Division by zero in Km calculation!")
    exit()

Km = (0.5774 * math.pi * E * d) / x
print("Joint Stiffness (Km):", Km)
