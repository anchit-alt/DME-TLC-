import numpy as np
import cv2
import math
#from sympy import symbols, solve

dia = 0
r = dia/2
loadoption = ""
Sut = 0

def fluctuating_simple_loading():
    global Sut
    Sut = float(input("Enter the value of Sut in MPa :"))
    Se = calculate_endurance_limit(Sut)
    print("The calculated value of endurance limit is :", Se)
    
    Kf, Kfs = determineK(Sut)
    Sy = float(input("Enter the value of yield strength Sy (MPa) :"))
    sig_max = float(input("Enter value of maximum stress (MPa) :"))
    sig_min = float(input("Enter the value of minimum stress (MPa) :"))
    
    sig_m = Kf * (sig_max - sig_min)/2
    sig_a = Kf * abs(sig_max - sig_min)/2
    
    if sig_m >= 0:
        failurecriterion = input("Enter fatigue failure criterion ('Soderberg', 'mod-Goodman', 'Gerber', 'ASME-elliptic') :")
        failurecriterion = failurecriterion.lower()
        if failurecriterion == 'soderberg':
            n = 1/(sig_a/Se + sig_m/Sy)
        elif failurecriterion == 'mod-goodman':
            n = 1/(sig_a/Se + sig_m/Sut)
        elif failurecriterion == 'gerber':
            n = symbols
            n = solve(n*sig_a/Se + pow(n*sig_m/Sut, 2), n)
        elif failurecriterion == 'asme-elliptic':
            n = 1/math.sqrt(pow(sig_a/Se, 2) + pow(sig_m/Sy, 2))
    else:
        n = Se/sig_a

    print("Factor of saftey n on applying fatigue failure criterion is ", round(n, 2))
    
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
        failurecriterion = input("Enter fatigue failure criterion ('Soderberg', 'mod-Goodman', 'Gerber', 'ASME-elliptic') :")
        failurecriterion = failurecriterion.lower()
        if failurecriterion == 'soderberg':
            n = 1/(sig_a/Se + sig_m/Sy)
        elif failurecriterion == 'mod-goodman':
            n = 1/(sig_a/Se + sig_m/Sut)
        elif failurecriterion == 'gerber':
            n = symbols
            n = solve(n*sig_a/Se + pow(n*sig_m/Sut, 2), n)
        elif failurecriterion == 'asme-elliptic':
            n = 1/math.sqrt(pow(sig_a/Se, 2) + pow(sig_m/Sy, 2))
    else:
        n = Se/sig_a, 2

    print("Factor of saftey n on applying fatigue failure criterion is ", round(n, 2))
    
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
    
    surfacefinish = input("What is the desired surface finish ('ground','machined','cold-drawn','hot-rolled','as-forged'): ")
    surfacefinish = surfacefinish.lower()
    
    if surfacefinish == 'ground':
        a = 1.58
        b = -0.085
    elif surfacefinish == 'machined' or surfacefinish == 'cold-drawn':
        a = 4.51
        b = -0.265
    elif surfacefinish == 'hot-rolled':
        a = 57.7
        b = -0.718
    elif surfacefinish == 'as-forged':
        a = 272
        b = -0.995
    
    ka = a * pow(Sut, b)
    
    kb = 1
    kc = 1
    kd = 1
    ke = 1
    kf = 1
    
    
    loadoption = input("Enter load option ('bending', 'torsion', or 'axial'): ")
    loadoption = loadoption.lower()
    
    if loadoption == 'bending':
        kc = 1
    elif loadoption == 'axial':
        kc = 0.85
    elif loadoption == 'torsion':
        kc = 0.59
    
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
    
    rotresp = input("Is it a Rotating Shaft or Non-rotating Member? ")
    rotresp = rotresp.lower()     
    if rotresp == 'rotating shaft':  
            
        if loadoption == 'bending' or loadoption == 'torsion':
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
    
    if 2.79 <= d and d <= 51:
        kb = 1.24 * pow(d, -0.107)
    elif 51 <= d and d <=254:
        kb = 1.51 * pow(d, -0.157)
    elif d == 0:
        assumption = input("Do you want to assume the value of kb or d?")
        assumption = assumption.lower()
        if assumption == 'kb':
            assumedkb = float(input("Enter assumed value of Kb :")) #assume kb = 0.85 to start iterations
            #kb = iterate(assumedkb, Sut, Se) 
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

# def iterate(assumedKb, Sut, Se):
#     sig_max = float(input("Enter the value of maximum stress (MPa) :"))
#     N = float(input("Enter number of cycles to failure"))
#     a, b = fatiguelifeconstants(Sut, Se)
    
#     d = 0.808*pow(h*b, 0.5)
#     if 2.79 <= d <= 51:
#         kb = 1.24 * pow(d, -0.107)
#     else:
#         kb = 1.51 * pow(d, -0.157)
        
#     return kb

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
    load = input("Enter load option ('bending' , 'axial', or 'torsion'): ")
    load = load.lower()
    r = dia/2
    if load == 'bending' or load == 'axial':
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
    user_input = input("Enter loading option ('completely reversing simple loading', 'fluctuating simple loading', or 'combination of loading modes'): ")
    user_input = user_input.lower()  

    if user_input == 'completely reversing simple loading':
        reverse_simple_loading()
        
    elif user_input == 'fluctuating simple loading':
        result = fluctuating_simple_loading()
        print(result)
    elif user_input == 'combination of loading modes':
        result = combination_loading_modes()
        print(result)
    else:
        print("Invalid option. Please enter a valid loading option.")

#test run
process_loading_option()
