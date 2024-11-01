from sympy import *
from sympy import symbols, solve

def calculate_LD(ld, nd):
    return 60 * ld * nd

def calculate_XD(LD, LR):
    return float(LD / LR)

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
    a = 3
    b = 1.483
    X_0 = 0.02
    theta = 4.459
    LR = pow(10, 6)

elif option == 2:
    print("Cylinder Roller Bearing selected")
    a = 10 / 3
    b = 1.483
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

radial_load = input("\nEnter radial load (required) KN -> ")

LD = int(input("\nif given, Enter the value of LD in rev -> , else type 0 "))

if LD == 0:
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
    LD = calculate_LD(ld=ld, nd=nd)

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

XD = calculate_XD(LD=LD, LR=LR)
print("XD :",XD)
print("LD :",LD)

C_ten = af * float(radial_load) * ((XD / (X_0 + (theta - X_0) * (1 - R) ** (1 / b))) ** (1 / a))

print("C_ten :",C_ten)