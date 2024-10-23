import math
from sympy import *
from sympy import symbols, solve
# from PIL import Image
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
C_o = None
e1 = None
e2 = None
X2 = None
Y2 = None
Fa_by_Co = None
Fa_by_VFr = None

C_ten_list = []

def calculate_LD(ld, nd):
    return 60 * ld * nd


def calculate_XD(LD, LR):
    return float(LD / LR)


def calculate_Fe(V, Fr, Fa, X, Y):
    return float((X * V * Fr) + (Y * Fa))

def iteration(j,l):
    Fe = calculate_Fe(V=V, Fa=Fa, Fr=Fr, X=j, Y=l)
    if Fe > Fr:
        FD = Fe
        print("FD\n",round(FD,2))
    else:
        FD = Fr
        print("FD\n",round(FD,2))
    C_ten = af * FD * ((XD / (X_0 + (theta - X_0) * (1 - R) ** (1 / b))) ** (1 / a))
    print("C_ten\n",round(C_ten,2))
    for i in range(len(table11_2['Load Rating Deep Groove C10 (kN)'])):
        if table11_2['Load Rating Deep Groove C10 (kN)'][i] > C_ten:
            if C_ten in C_ten_list:
                print("Choose Bore of ", Bore (mm)[i-1])
                return True
                break
            else:
                C_ten_list.append(table11_2['Load Rating Deep Groove C10 (kN)'][i])
                C_o_sec = table11_2['Load Rating Deep Groove C0 (kN)'][i]
                print(C_o_sec)
                break
        if C_o_sec is not None:
            Fa_by_Co = (Fa / C_o_sec)
            for i in range(len(table11_1['Fa/C0'])):
                print(i)
                print("Fa_by_Co\n", round(Fa_by_Co,2))
                if table11_1['Fa/C0'][i] > Fa_by_Co:
                    e2 = table11_1['e'][i]
                    e1 = table11_1['e'][i- 1]
                    print("e2 and e1\n", e2, e1)
                    break
            Fa_by_VFr = Fa / (V * Fr)
            print("Fa_by_VFr\n", Fa_by_VFr)
            if e1 is not None:
                if Fa_by_VFr <= e1:
                    j = 1
                    l = 1
            elif Fa_by_VFr >= e2:
                X2 = 0.56
                g = table11_1['Y2'][i - 1]
                h = table11_1['Y2'][i]
                k = table11_1['Fa/C0'][i - 1]
                l = table11_1['Fa/C0'][i]
                Y2 = g - (((g) -(h))*(k-Fa_by_Co))/(k-l)
                print("X2 and Y2\n", X2, round(Y2,2))
    # if len(C_ten_list) != 0:
    #     print("need more iterations")

#
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
#
#
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
#
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
#
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
#
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
#
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
print("XD",XD)
print("LD",LD)

table11_1 = pd.read_csv("/Users/anchit/Documents/GitHub/DME-TLC-/Data/11_point_1.csv")
table11_2 = pd.read_csv("/Users/anchit/Documents/GitHub/DME-TLC-/Data/11_point_2.csv")
num_rows = len(table11_1)
num_rows_half = int(num_rows / 2)

X = table11_1.loc[num_rows_half, "X2"]
Y = table11_1.loc[num_rows_half, "Y2"]
print("X and Y" , X,Y)
FD = None
#
while True:
    Fe = calculate_Fe(V=V, Fa=Fa, Fr=Fr, X=X, Y=Y)
    print("Fe\n",round(Fe,2))
    if Fe > Fr:
        FD = Fe
        print("FD\n",round(FD,2))
    else:
        FD = Fr
        print("FD\n",round(FD,2))

    # C_ten = float(af * FD * ((XD / (X_0 + (theta - X_0) * ((1 - R) ** 1 / b))) ** 1 / a))
    C_ten = af * FD * ((XD / (X_0 + (theta - X_0) * (1 - R) ** (1 / b))) ** (1 / a))
   

    print("Intial C_ten\n",round(C_ten,2))
    for i in range(len(table11_2['Load Rating Deep Groove C10 (kN)'])):
        if table11_2['Load Rating Deep Groove C10 (kN)'][i] > C_ten:
            C_ten_list.append(table11_2['Load Rating Deep Groove C10 (kN)'][i])
            C_o = table11_2['Load Rating Deep Groove C0 (kN)'][i]
            break
    if C_o is not None:
        Fa_by_Co = (Fa / C_o)

    else:
        print("Error: C_o is None, cannot perform division.")
    for i in range(len(table11_1['Fa/C0'])):
        print(i)
        print("Fa_by_Co\n", round(Fa_by_Co,2))
        if table11_1['Fa/C0'][i] > Fa_by_Co:
            e2 = table11_1['e'][i]
            e1 = table11_1['e'][i- 1]
            print("e2 and e1\n", e2, e1)
            break
    Fa_by_VFr = Fa / (V * Fr)
    print("Fa_by_VFr\n", Fa_by_VFr)
    if e1 is not None:
        if Fa_by_VFr <= e1:
            X1 = 1
            Y1 = 0
        elif Fa_by_VFr >= e2:
            X2 = 0.56
            g = table11_1['Y2'][i - 1]
            h = table11_1['Y2'][i]
            k = table11_1['Fa/C0'][i - 1]
            l = table11_1['Fa/C0'][i]
            Y2 = g - (((g) -(h))*(k-Fa_by_Co))/(k-l)
            print("X2 and Y2\n", X2, round(Y2,2))

    else:
        print("e1 is none")
    if iteration == True:
        iteration(X2,Y2)
    else:
        break


           # while C_ten_list[i] != C_ten_list[i+1]:
            # iteration(X2,Y2)
# second iteration
            # Fe = calculate_Fe(V=V, Fa=Fa, Fr=Fr, X=X2, Y=Y2)
            # if Fe > Fr:
            #     FD = Fe
            #     print("FD\n",round(FD,2))
            # else:
            #     FD = Fr
            #     print("FD\n",round(FD,2))
            # C_ten = af * FD * ((XD / (X_0 + (theta - X_0) * (1 - R) ** (1 / b))) ** (1 / a))
            # print("C_ten\n",round(C_ten,2))
            # for i in range(len(table11_2['Load Rating Deep Groove C10 (kN)'])):
            #     if table11_2['Load Rating Deep Groove C10 (kN)'][i] > C_ten:
            #         C_o = table11_2['Load Rating Deep Groove C0 (kN)'][i]
            #         break
            # if C_o is not None:
            #     Fa_by_Co = (Fa / C_o)
            # for i in range(len(table11_1['Fa/C0'])):
            #     print(i)
            #     print("Fa_by_Co\n", round(Fa_by_Co,2))
            #     if table11_1['Fa/C0'][i] > Fa_by_Co:
            #         e2 = table11_1['e'][i]
            #         e1 = table11_1['e'][i- 1]
            #         print("e2 and e1\n", e2, e1)
            #         break
            # Fa_by_VFr = Fa / (V * Fr)
            # print("Fa_by_VFr\n", Fa_by_VFr)
            # if e1 is not None:
            #     if Fa_by_VFr <= e1:
            #     X1 = 1
            #     Y1 = 1
            # elif Fa_by_VFr >= e2:
            #     X2 = 0.56
            #     g = table11_1['Y2'][i - 1]
            #     h = table11_1['Y2'][i]
            #     k = table11_1['Fa/C0'][i - 1]
            #     l = table11_1['Fa/C0'][i]
            #     Y2 = g - (((g) -(h))*(k-Fa_by_Co))/(k-l)
            #     print("X2 and Y2\n", X2, round(Y2,2))







    # for index,val in table11_2['Load Rating Deep Groove C10 (kN)']:
    #     if val>C_ten:
    #         C_o = table11_2['Load Rating Deep Groove C0 (kN)'][index]
    #         print(C_o)
    #
    # Fa_by_Co = Fa/C_o
    # for index,val in table11_1['Fa/C0']:
    #     if val>Fa_by_Co:
    #         e2 = table11_1['e'][index+1]
    #         e1 = table11_1['e'][index-1]
    #     print("e2 and e1",e2,e1)
    #     Fa_by_VFr = Fa/(V*Fr)
    #     if Fa_by_VFr <=e1:
    #         X1 = 1
    #         Y1=1
    #     elif Fa_by_VFr >=e2:
    #         X2 = 0.56
    #         Y2 = (table11_1['Y2'][index-1] - ((table11_1['Y2'][index-1]-table11_1['Y2'][index])*(table11_1['Y2'][index]-Fa_by_Co))/((table11_1['Fa/C0'][index-1])-(table11_1['Fa/C0'][index])))
    #         print("X2 and Y2",X2,Y2)
