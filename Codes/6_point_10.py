import csv

import numpy as np
import cv2
import math

from sympy import *

from sympy import symbols, solve

dia = 0
r = dia/2
loadoption = ""
Sut = 0

def fluctuating_simple_loading():
    global Sut
    Sut = float(input("Enter the value of Sut in MPa :"))
    Se = calculate_endurance_limit(Sut)

    print("The calculated value of endurance limit is :", Se)
    Kf = float(input("Enter the value of Kf :"))
    if Kf:
        pass
    else:
        Kf, Kfs = determineK(Sut)
    Sy = float(input("Enter the value of yield strength Sy (MPa) :"))
    stress_given = input("Is varying stress given Y/N:")
    if stress_given == 'Y':
        sig_max = float(input("Enter value of maximum stress (MPa) :"))
        sig_min = float(input("Enter the value of minimum stress (MPa) :"))
        sig_m = Kf * (sig_max + sig_min) / 2  #### have changed - to +
        sig_a = Kf * abs(sig_max - sig_min) / 2
    elif stress_given == 'N':
        F_max = float(input("Enter value of maximum Force (N) :"))
        F_min = float(input("Enter the value of minimum Force (N) :"))
        F_m =  (F_max + F_min) / 2  #### have changed - to +
        F_a =  abs(F_max - F_min) / 2
        sigma_ao = ((4*F_a)/(math.pi*(dia/1000)**2))/pow(10,6) ## in MPa
        sigma_mo = ((4*F_m)/(math.pi*(dia/1000)**2))/pow(10,6) ## in MPa

        sig_m = Kf * sigma_ao #### have changed - to +
        sig_a = Kf * sigma_mo

        print(sigma_ao, sigma_mo, Kf,sig_a,sig_m)


    n = symbols
    if sig_m >= 0:
        failurecriterion = input("Enter fatigue failure criterion ('1. Soderberg', '2. mod-Goodman', '3. Gerber', '4. ASME-elliptic') :")
        failurecriterion = failurecriterion.lower()
        if failurecriterion == '1':
            print("Soderberg was chosen")
            n = 1/(sig_a/Se + sig_m/Sy)
        elif failurecriterion == '2':
            print("mod-goodman was chosen")
            n = 1/(sig_a/Se + sig_m/Sut)
        elif failurecriterion == '3':
            print("gerber was chosen")
            n = symbols('n')
            print(sig_m,sig_a,Sut,Se)
            n = (-sig_a*pow(Sut,2) + sqrt(pow(sig_a,2)*pow(Sut,4) + 4*sig_m**2*Se**2*Sut**2))/(2*sig_m**2*Se)
            # n = solve(n*sig_a/Se + pow(n*sig_m/Sut, 2), n)
            print(n)
            r = 1
            Sa = ((pow(r,2)*pow(Sut,2))/(2*Se))*(-1 + sqrt(1 + ((2*Se)**2/(r*Sut)**2)))
            Sm = Sa/r
            print("When load line and Gerber line intersects, Sa is equal to  ", round(Sa, 2))
            print("When load line and Gerber line intersects, Sm is equal to ", round(Sm, 2))

            Sm_ = (Sut**2/(2*Se))*(1-sqrt(1+((2*Se)**2/(Sut**2))*(1-(Sy/Se))))
            Sa_ = Sy - Sm_
            r_crit =Sa_/Sm_
            print("When langer line and Gerber line intersects, Sa is equal to  ", round(Sa_, 2))
            print("When langer line and Gerber line intersects, Sm is equal to  ", round(Sm_, 2))
            print("rcrit",r_crit)


        elif failurecriterion == '4':
            print("asme-elliptic was chosen")
            n = 1/math.sqrt(pow(sig_a/Se, 2) + pow(sig_m/Sy, 2))
            r = 1
            Sa = sqrt((pow(r,2)*pow(Se,2)*pow(Sy,2))/(Se**2 + (r*Sy)**2))
            Sm = Sa / r
            print("When load line and asme-elliptic intersects, Sa is equal to  ", round(Sa, 2))
            print("When load line and asme-elliptic intersects, Sm is equal to ", round(Sm, 2))

            Sa_ = (2*Sy*Se**2)/(Se**2 + Sy**2)
            Sm_ = Sy - Sa_
            r_crit = Sa_ / Sm_
            print("When langer line and asme-elliptic intersects, Sa is equal to  ", round(Sa_, 2))
            print("When langer line and asme-elliptic intersects, Sm is equal to  ", round(Sm_, 2))
            print("rcrit", r_crit)


    else:
        n = (Se/sig_a)

    print("Factor of saftey n on applying fatigue failure criterion is ", round(n,2))

    # ny = Sy/(sig_a + sig_m)
    # if ny>n:
    #     print("ny = ",round(ny,2))
    #     print("First Fatigue will take place")
    # else:
    #     print("Yielding will happen first")


    n_yield = Sy/(sig_a + sig_m)
    if n_yield >= 1:
        print("No localised yielding.")
    sig_rev = sig_a/(1 - (sig_m/Sut))
    
    a, b = fatiguelifeconstants(Sut, Se)
    
    N = pow(sig_rev/(n*a), 1/b)
    print("Finite life N with factor of saftey n is ", round(N, 2))


    
def reverse_simple_loading():
    global Sut
    Sut = float(input("Enter the value of Sut in MPa :"))
    Se = calculate_endurance_limit(Sut)
    print("The calculated value of endurance limit is :", round(Se, 2))
    
    Kf, Kfs = determineK(Sut)
    
    sig_rev = Kf * float(input("Enter value of purely reversing stress :"))
    
    a, b = fatiguelifeconstants(Sut, Se)
    print("Fatigure life constant a :", round(a, 2))
    print("Fatigure life constant b :", round(b, 2))
    
    N = float(input("Enter number of cycles to failure N, 0 if unknown:")) #computes Sf
    if N != 0:
        Sf = a*pow(N, b)
        print("Fatigure strength at N cycles :", Sf)
    else:
        N = pow(sig_rev/a, 1/b)
        print("Number of cycles to failure at reversing stress :", round(N, 2))

def combination_loading_modes():
    global Sut
    Sut = float(input("Enter the value of Sut in MPa :"))
    Se = calculate_endurance_limit(Sut)
    print("The calculated value of endurance limit is :", round(Se, 2))
    Sy = float(input("Enter the value of yield strength Sy (MPa)"))
    Kf = []
    print("Kf = [Kf_bending, Kf_axial, Kf_torsion]")
    for i in range(3):
        while True:
            try:
            # Input float value from the user
                value = float(input(f"Enter element {i+1} of the array: "))
            # Append the float value to the list
                Kf.append(value)
                break  # Exit the loop if input is successful
            except ValueError:
                print("Invalid input. Please enter a float value.")
    sig_mid = []
    print("Midrange Stress States = [Bending, Axial, Torsion]")
    for i in range(3):
        while True:
            try:
            # Input float value from the user
                value = float(input(f"Enter element {i+1} of the array: "))
            # Append the float value to the list
                sig_mid.append(value)
                break  # Exit the loop if input is successful
            except ValueError:
                print("Invalid input. Please enter a float value.")
    sig_alt = []
    print("Alternating Stress States = [Bending, Axial, Torsion]")
    for i in range(3):
        while True:
            try:
            # Input float value from the user
                value = float(input(f"Enter element {i+1} of the array: "))
            # Append the float value to the list
                sig_alt.append(value)
                break  # Exit the loop if input is successful
            except ValueError:
                print("Invalid input. Please enter a float value.")
                
    sig_a = ((Kf[0]*sig_alt[0] + Kf[1]*sig_alt[1]/0.85)**2 + 3*(Kf[2]*sig_alt[2])**2)**0.5
    sig_m = ((Kf[0]*sig_mid[0] + Kf[1]*sig_mid[1]/0.85)**2 + 3*(Kf[2]*sig_mid[2])**2)**0.5

    if sig_m >= 0:
        failurecriterion = input("Enter fatigue failure criterion (1. Soderberg', '2. mod-Goodman', '3. Gerber', '4. ASME-elliptic') :")
        failurecriterion = failurecriterion.lower()
        if failurecriterion == '1':
            n = 1/(sig_a/Se + sig_m/Sy)
        elif failurecriterion == '2':
            n = 1/(sig_a/Se + sig_m/Sut)
        elif failurecriterion == '3':
            n = symbols('n')
            equation = (n*sig_a/Se) + pow(n*sig_m/Sut, 2)
            n = solve(equation,n)
        elif failurecriterion == '4':
            n = 1/math.sqrt(pow(sig_a/Se, 2) + pow(sig_m/Sy, 2))
    else:
        n = Se/sig_a, 2

    print("Factor of saftey n on applying fatigue failure criterion is ", n)
    
    n_yield = Sy/(sig_a + sig_m)
    if n_yield >= 1:
        print("No localised yielding.")
    
def calculate_endurance_limit(Sut):
    global loadoption
    global dia
    if Sut <= 1400:
        Se_ = 0.5 * Sut
    else:
        Se_ = 700
    
    surfacefinish = input("What is the desired surface finish ('1. ground','2. machined','3. cold-drawn','4. hot-rolled','5. as-forged'): ")
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
    
    kb = 1
    kc = 1
    kd = 1
    ke = 1
    kf = 1
    
    
    loadoption = input("Enter load option ('1. bending', '2. torsion', or '3. axial'): ")
    loadoption = loadoption.lower()
    
    if loadoption == '1':
        kc = 1
    elif loadoption == '2':
        # kb =1
        kc = 0.59
    elif loadoption == '3':
        kc = 0.85
        kb=1
    
    temp = float(input("Enter temperature Tf if specified, 0 otherwise: "))
    if temp == 0:
        kd = 1
    else:
        kd = 0.975 + 0.432 * 10E-3 * temp - 0.115 * 10E-5 * pow(temp, 2) + 0.104 * 10E-8 * pow(temp, 3) - 0.595 * 10E-12 * pow(temp, 4)
    
    reliability = float(input("Enter reliability value if specified, 0 otherwise: "))
    if reliability == 0:
        ke = 1
    else:
        reliability_values = {50: 1.000, 90: 0.897, 95: 0.868, 99: 0.814, 99.9: 0.753, 99.99: 0.702, 99.999: 0.659, 99.9999: 0.620}
        ke = reliability_values.get(reliability, 1)  # Default to 1 if reliability value not in the dictionary
    
    kf = 1
    
    rotresp = input("Is it a 1. Rotating Shaft or 2. Non-rotating Member? ")
    rotresp = rotresp.lower()     
    if rotresp == '1':  
            
        if loadoption == '1' or loadoption == '2':
            d = float(input("Enter the value of diameter in mm, and 0 if unknown: "))
            dia = d       
        else:
            d = float(input("Enter the value of diameter in mm, and 0 if unknown: "))
            dia = d
            kb = 1
             
    else:
        h = float(input("Input value h (in mm) of rectangular cross-section of shaft :"))
        b = float(input("Enter value b (in mm) of rectangular cross-section of shaft :"))
        d = 0.808 * pow(h*b, 0.5)
        dia = d
        print("Effective diameter :", d)
    
    if 2.79 <= d and d <= 51 and loadoption != '3':
        kb = 1.24 * pow(d, -0.107)
    elif 51 <= d and d <=254:
        kb = 1.51 * pow(d, -0.157)
    elif d == 0:
        assumption = input("Do you want to assume the value of kb or d?")
        assumption = assumption.lower()
        if assumption == 'kb':
            assumedkb = float(input("Enter assumed value of Kb :")) #assume kb = 0.85 to start iterations
            kb = iterate(assumedkb) 
        else:
            while True:
                assume_d = float(input("Enter assumed value of d: "))
                Kb_calc, Kb = checkcompatibility(assume_d, ka, kc, kd, ke, kf, Se_)
                print("Assumed value of Kb:", Kb)
                print("Calculated value of Kb:", Kb_calc)
                if Kb_calc >= Kb:
                    print("Assumed value of d is valid.")
                    d = assume_d
                    break 
            
    else:
        kb = 1
        
    Se = ka * kb * kc * kd * ke * kf * Se_
    
    # Store values in a dictionary
    values = {
        'ka': round(ka, 2),
        'kb': round(kb, 2),
        'kc': round(kc, 2),
        'kd': round(kd, 2),
        'ke': round(ke, 2),
        'kf': round(kf, 2),
        'Se_ (MPa)': round(Se_, 2)
    }
    
    # Display values in a table
    print("\nParameter\t\tValue")
    print("-----------------------------")
    for key, value in values.items():
        print(f"{key}\t\t\t{value}")
    
    return round(Se, 2)

def iterate(assumedKb):
    sig_max = float(input("Enter the value of maximum stress (MPa) :"))
    N = float(input("Enter number of cycles to failure"))
    # a, b = fatiguelifeconstants(Sut, Se)
    h = float(input("Input value h (in mm) of rectangular cross-section of shaft :"))
    b = float(input("Enter value b (in mm) of rectangular cross-section of shaft :"))
    
    d = 0.808*pow(h*b, 0.5)
    if 2.79 <= d <= 51:
        kb = 1.24 * pow(d, -0.107)
    else:
        kb = 1.51 * pow(d, -0.157)
        
    return kb

def determineK(Sut):
    global dia
    images = {
    "1": "A_15_1.png",
    "2": "A_15_2.png",
    "3": "A_15_3.png",
    }

    def display_images(images):
        for serial, path in images.items():
            print(f"{serial}: {path}")
            img = cv2.imread(path)
            cv2.imshow(f"Image {serial}", img)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def main():
        display_images(images)
        user_input = input("Enter the serial number of the image you want to select: ")

        if user_input in images:
            selected_image_path = images[user_input]
            print(f"Image with serial number {user_input} selected: {selected_image_path}")
            # Do something with the selected image
        else:
            print("Invalid serial number entered.")
    
    with open('DataExtraction/A-15-1.csv', mode='r') as file:
        csv_data = csv.reader(file)

    Kt = 1
    Kts = 1

    q = notchsensitivity(Sut)
    
    Kf = 1 + q*(Kt -1)
    Kfs = 1 + q*(Kts-1)
    
    # interpolate notch radius to get notch sensitivity q

    return round(Kf, 2), round(Kfs, 2) 

def notchsensitivity(Sut):
    global dia
    global r
    load = input("Enter load option ('1. bending' , '2. axial', or '3. torsion'): ")
    if load == '1' or load == '2' or load == '3':
        load = load.lower()
    else:
        print("Invalid load option entered.")
    r = dia/2
    if load == '1' or load == '2':
        sqrta = 1.24 - 2.25*10E-3*Sut + 1.60*10E-5*Sut**2 - 4.11*10E-8*Sut**3 # Changed ^ to **
    else:
        sqrta = 0.958 -1.83*10E-3*Sut + 1.43*10E-5*Sut**2 - 4.11*10E-8*Sut**3 # Changed ^ to **
    q = 1/(1+(sqrta/math.sqrt(r))) # Variable r is not defined
    
    return round(q, 2)

def fatiguelifeconstants(Sut, Se):
    f = 0.9 #interpolate f from figure 6-18
    
    a = pow(f*Sut, 2)/Se
    b = -math.log((f*Sut)/Se)/3
    return round(a, 2), round(b, 2)
    
def checkcompatibility(d, ka, kc, kd, ke, kf, Se_):
    global r
    global dia
    global loadoption
    global Sut
    
    dia = d
    
    if 2.79 <= d and d <= 51:
        kb = 1.24 * pow(d, -0.107)
    elif 51 <= d and d <=254:
        kb = 1.51 * pow(d, -0.157)
    else:
        kb = 1
    
    Se = ka * kb * kc * kd * ke * kf * Se_
    
    a, b = fatiguelifeconstants(Sut, Se)
    
    Kf, Kfs = determineK(Sut)
    
    sig_rev = Kf * float(input("Enter value of purely reversing stress :"))
    
    
    N = float(input("Enter number of cycles to failure N, 0 if unknown:"))
    
    if N != 0:
        Sf = a*pow(N, b)
    else:
        N = pow(sig_rev/a, 1/b)
        print("Number of cycles to failure at reversing stress :", round(N, 2))

    Sf = a*pow(N, b)
    print("Fatigue strength (MPa) :", Sf)
    
    d_calc = float(input("Enter the value of diameter/effective diameter calculated using Sf (mm) :"))
    
    if 2.79 <= d_calc and d_calc <= 51:
        kb_calc = 1.24 * pow(d_calc, -0.107)
    elif 51 <= d_calc and d_calc <=254:
        kb_calc = 1.51 * pow(d_calc, -0.157)
    else:
        kb_calc = 1
    
    return kb_calc, kb
    
def process_loading_option():
    user_input = input("Enter loading option ('1. completely reversing simple loading', '2. fluctuating simple loading', or '3. combination of loading modes'): ")
    user_input = user_input.lower()  

    if user_input == '1':
        result = reverse_simple_loading()
        print(result)
    elif user_input == '2':
        result = fluctuating_simple_loading()
        print(result)
    elif user_input == '3':
        result = combination_loading_modes()
        print(result)
    else:
        print("Invalid option. Please enter a valid loading option.")

#test run
process_loading_option()
