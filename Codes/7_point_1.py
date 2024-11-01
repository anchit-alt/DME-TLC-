import csv
import numpy as np
import cv2
import math
from sympy import *
from sympy import symbols, solve
from PIL import Image
Sut = float(input("Enter Sut (MPa): "))
Sy = float(input("Enter Sy (MPa): "))

q =None
q_shear =None
kt =None
Kf=None
Kfs= None
Se = None
r = None
D = None
d = None

def data():
    global r
    global D
    global d
    r = float(input('Enter r: '))
    D = float(input('Enter D: '))
    d = float(input('Enter d: '))
    return r, D, d
def get_q():
    img3 = Image.open(r"/Users/anchit/Documents/GitHub/DME-TLC-/Images/6-20.png")
    img3.show()
    global q
    q = float(input('Enter q: '))
    return q
def get_q_shear():
    global q_shear
    img4 = Image.open(r"/Users/anchit/Documents/GitHub/DME-TLC-/Images/6-21.png")
    img4.show()
    q_shear = float(input('Enter q_shear: '))
    return q_shear
def get_kt():
    global kt
    print("r/d =",(r/d))
    print("D/d =",(D/d))
    img2 = Image.open(r"/Users/anchit/Documents/GitHub/DME-TLC-/Images/A-15-9.png")
    img2.show()
    kt = float(input('Enter kt: '))
    return kt
def get_kts():
    global kts
    img1 = Image.open(r"/Users/anchit/Documents/GitHub/DME-TLC-/Images/A-15-8.png")
    img1.show()
    kts = float(input('Enter kts: '))
    return kts

def Kf():
    global Kf
    q = get_q()
    kt=get_kt()
    Kf = 1 + q*(kt-1)
    return Kf
def Kfs():
    global Kfs
    q_shear = get_q_shear()
    kts = get_kts()
    Kfs = 1 + q_shear * (kts-1)
    return Kfs

def Se():
    global Se
    if Sut <= 1400:
        Se_ = 0.5 * Sut
    else:
        Se_ = 700
    surfacefinish = input(
        "What is the desired surface finish ('1. ground','2. machined','3. cold-drawn','4. hot-rolled','5. as-forged'): ")
    surfacefinish = surfacefinish.lower()

    if surfacefinish == '1':
        a = 1.58
        b = -0.085
    elif surfacefinish == '2' or surfacefinish == '3':
        a = 4.51
        b = -0.265
    elif surfacefinish == '4':
        a = 57.7
        b = -0.718
    elif surfacefinish == '5':
        a = 272
        b = -0.995

    ka = a * pow(Sut, b)

    ##Kb##
    # r,D,d = data()
    loadoption = input("Enter load option ('1. bending', '2. torsion', or '3. axial'): ")
    loadoption = loadoption.lower()

    if loadoption == '1' or loadoption == '2':
        if d<= 51 and d>=2.79:
            kb =(d/7.62)**-0.107
        elif d>51 and d<=254:
            kb = 1.51 * d **-0.157
    elif loadoption == '3':
        kb = 1
    ##kc##

    if loadoption == '1':
        kc = 1
    elif loadoption == '2':
        kc =0.59
    elif loadoption == '3':
        kc = 0.85
    ##kd##
    temp = float(input("Enter temperature Tf if specified, 0 otherwise: "))
    if temp == 0:
        kd = 1
    else:
        kd = 0.975 + 0.432 * 10E-3 * temp - 0.115 * 10E-5 * pow(temp, 2) + 0.104 * 10E-8 * pow(temp,3) - 0.595 * 10E-12 * pow( temp, 4)
    ##ke##
    reliability = float(input("Enter reliability value if specified, 0 otherwise: "))
    if reliability == 0:
        ke = 1
    else:
        reliability_values = {50: 1.000, 90: 0.897, 95: 0.868, 99: 0.814, 99.9: 0.753, 99.99: 0.702, 99.999: 0.659,99.9999: 0.620}
        ke = reliability_values.get(reliability, 1)  # Default to 1 if reliability value not in the dictionary
    kf = 1

    Se = ka*kb*kc*kd*ke*kf*Se_
    print(Se)
    return Se


data()
# get_kt()
# get_kts()
# get_q()
# get_q_shear()
Kf()
Kfs()
Se()

# Inputs for bending moment and torque type
bending_moment_type = input("Enter bending moment type (1. constant/ 2. alternating): ").lower()
torque_type = input("Enter torque type (1. constant/ 2. alternating): ").lower()

# Decision for M_m (mean bending moment) and M_a (alternating bending moment)
if bending_moment_type == "2":
    Mm = 0
    Ma = float(input("Enter the value of alternating bending moment (M_a): "))
    print(f"Mean bending moment (Mm) is {Mm}.")
    print(f"Alternating bending moment (Ma) is {Ma}.")
else:
    Mm = float(input("Enter the value of mean bending moment (M_m): "))
    Ma = 0
    print(f"Mean bending moment (Mm) is {Mm}.")
    print(f"Alternating bending moment (Ma) is {Ma}.")

# Decision for T_m (mean torque) and T_a (alternating torque)
if torque_type == "2":
    Tm = 0
    Ta = float(input("Enter the value of alternating torque (T_a): "))
    print(f"Mean torque (Tm) is {Tm}.")
    print(f"Alternating torque (Ta) is {Ta}.")
else:
    Tm = float(input("Enter the value of mean torque (T_m): "))
    Ta = 0
    print(f"Mean torque (Tm) is {Tm}.")
    print(f"Alternating torque (Ta) is {Ta}.")

# print("Mm=0 because there is no steady bending force, only alternating bending loads, and 𝑇𝑎=0 because the applied torque is constant, with no fluctuating or alternating component.")

def fac_DE_goodmann():
    x = 16/((math.pi)*(d*pow(10,-3))**3)
    x_ = sqrt(4*(Kf*Ma)**2)/(Se*pow(10,6))
    y = sqrt(3*(Kfs*Tm)**2)/(Sut*pow(10,6))
    a = x_ + y
    ans = x * a
    return 1/ans
def fac_DE_Gerber():
    A = sqrt(4*(Kf*Ma)**2+(3*(Kfs*Ta)**2))
    B = sqrt(4*(Kf*Mm)**2+(3*(Kfs*Tm)**2))
    x = ((8*A)/(math.pi*d**3*(Se)))*(1+sqrt(1+((2*B*Se)/(A*Sut))**2))
    return 1/x
def DE_ASME():
    x = (16/(math.pi*(d*pow(10,-3))**3))*(sqrt((4*(((Kf*Ma)/(Se))**2)) + (3*(((Kfs*Ta)/(Se))**2)) + (4*((Kf*Mm)/((Sy)))**2) + (3*((Kfs*Tm)/((Sy)))**2)))
    return 1/x

def DE_Soderberg():
    x = (16/(math.pi*(d*pow(10,-3))**3))*((sqrt((4*(Kf*Ma)**2) + (3*(Kfs*Ta)**2)))/(Se) + sqrt((4*(Kf*Mm)**2) + (3*(Kfs*Tm)**2))/(Sy))
    return 1/x


sigma_max_ = sqrt(((32*Kf*(Mm + Ma))/(math.pi*(d*pow(10,-3))**3))**2+3*((16*Kfs*(Tm+Ta))/(math.pi*(d*pow(10,-3))**3))**2)
print("goodmann factor ",fac_DE_goodmann())
print(fac_DE_Gerber())
print(DE_ASME())
print(DE_Soderberg())
print("Von misses stress  ", sigma_max_)
ny = Sy/sigma_max_
print("factor of safety",ny)

