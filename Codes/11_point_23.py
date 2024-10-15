import math
from sympy import *
from sympy import symbols, solve
from PIL import Image
import pandas as pd

a = None
b = None
X_0 = None
theta = None
LR = None
R = None
V = None
af = None
Fa = None
Fr = None
ld = None
nd = None
LD = None
XD = None


def calculate_LD(ld, nd):
    return 60 * ld * nd


def calculate_XD(LD, LR):
    return float(LD / LR)


def calculate_Fe(V, Fr, Fa, X, Y):
    return float((X * V * Fr) + (Y * Fa))


# Display bearing type options
print("1. Ball bearing")
print("2. Cylinder Roller Bearing")
print("3. Tapered Roller Bearing")

# Validate bearing type input
while True:
    try:
        option = int(input("Select bearing type (1-3) -> "))
        if option in [1, 2, 3]:
            break
        else:
            print("Invalid input, please enter 1, 2, or 3.")
    except ValueError:
        print("Invalid input, please enter a number (1, 2, or 3).")

# Set values based on bearing type selection
if option == 1:
    print("Ball bearing selected")
    a = 1 / 3
    b = 1.488
    X_0 = 0.02
    theta = 4.459
    LR = pow(10, 6)

elif option == 2:
    print("Cylinder Roller Bearing selected")
    a = 10 / 3
    b = 1.488
    X_0 = 0.02
    theta = 4.459
    LR = pow(10, 6)

elif option == 3:
    print("Tapered Roller Bearing selected")
    a = 10 / 3
    b = 1.5
    X_0 = 0.0
    theta = 4.48
    LR = 90 * pow(10, 6)

# Display ring rotation options
print("\n1. Inner Ring Rotating")
print("2. Outer Ring Rotating")

# Validate ring rotation selection input
while True:
    try:
        ring_option = int(input("Select which ring is rotating (1-2) -> "))
        if ring_option in [1, 2]:
            break
        else:
            print("Invalid input, please enter 1 or 2.")
    except ValueError:
        print("Invalid input, please enter a number (1 or 2).")

# Set values based on ring rotation selection
if ring_option == 1:
    print("Inner Ring Rotating selected")
    V = 1

elif ring_option == 2:
    print("Outer Ring Rotating selected")
    V = 1.2

# Validate application factor input
while True:
    af_value = input("\nEnter application factor (default is 1) -> ")
    if not af_value:
        af = 1
        break
    try:
        af = float(af_value)
        break
    except ValueError:
        print("Invalid input, please enter a valid number.")

while True:
    axial_load = input("\nEnter axial load (required) -> ")
    if not axial_load:
        print("Please enter a valid axial load value.")
    else:
        try:
            Fa = float(axial_load)
            break
        except ValueError:
            print("Invalid input, please enter a numerical value.")

while True:
    radial_load = input("\nEnter radial load (required) -> ")
    if not radial_load:
        print("Please enter a valid radial load value.")
    else:
        try:
            Fr = float(radial_load)
            break
        except ValueError:
            print("Invalid input, please enter a numerical value.")

while True:
    desired_life = input("\nEnter desired life in hours (required) -> ")
    if not desired_life:
        print("Please enter a valid desired life value.")
    else:
        try:
            ld = int(desired_life)
            break
        except ValueError:
            print("Invalid input, please enter a numerical value.")

while True:
    desired_speed = input("\nEnter desired speed in rev per minute (required) -> ")
    if not desired_speed:
        print("Please enter a valid desired speed value.")
    else:
        try:
            nd = float(desired_speed)
            break
        except ValueError:
            print("Invalid input, please enter a numerical value.")

while True:
    desired_reliability = input("\nEnter desired reliability in decimal (required) -> ")
    if not desired_reliability:
        print("Please enter a valid desired reliability value.")
    else:
        try:
            R = float(desired_reliability)
            break
        except ValueError:
            print("Invalid input, please enter a numerical value.")

LD = calculate_LD(ld=ld, nd=nd)
XD = calculate_XD(LD=LD, LR=LR)

table11_1 = pd.read_csv("../Data/11_point_1.csv")
num_rows = len(table11_1)
num_rows_half = int(num_rows / 2)

X = table11_1.loc[num_rows_half, "X2"]
Y = table11_1.loc[num_rows_half, "Y2"]
FD = None

while True:
    Fe = calculate_Fe(V=V, Fa=Fa, Fr=Fr, X=X, Y=Y)
    if Fe > Fr:
        FD = Fe
    else:
        FD = Fr

    C_ten = float(af * FD * (XD / (X_0 + (theta - X_0) * (1 - R) ** 1 / b)) ** 1 / a)
