from bs4 import BeautifulSoup
import cv2
import csv
import os
import lxml
import math
from sympy import *
from sympy import symbols, solve
import time 
from flask import Flask , render_template , request , current_app
import pandas as pd 
app = Flask(__name__)
dummy = None
def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        function()
        function()
    return wrapper_function


@app.route("/")
def home():
    # template_path = os.path.abspath("/Users/anchit/Documents/GitHub/DME-TLC-/Codes/templates/index.html")
    return render_template("index.html")
            # render_template("/Users/anchit/Documents/GitHub/DME-TLC-/Codes/templates/index.html")


@app.route("/ball_bearing.html",methods = ["POST","GET"])
def ball():
    if request.method == "POST":
        ###bearing type
        if request.form.get('name') == "Ball":
            print("Ball bearing selected")
            a = 3
            b = 1.483
            X_0 = 0.02
            theta = 4.459
            LR = pow(10, 6)
        elif request.form.get('name') == "Taper":
            print("Tapered Roller Bearing selected")
            a = 10 / 3
            b = 1.5
            X_0 = 0.0
            theta = 4.48
            LR = 90 * pow(10, 6)
        else:
            print("Cylinder Roller Bearing selected")
            a = 10 / 3
            b = 1.483
            X_0 = 0.02
            theta = 4.459
            LR = pow(10, 6)
        inner_ring = request.form.get('ring_rotation')
        if inner_ring == "inner":
            V =1.0
        else:
            outer_ring = request.form.get('ring_rotation')
            V = 1.2
        
        af = float(request.form.get('af')) or int(request.form.get('af'))
        Fa = float(request.form.get("Axial_load"))
        Fr = float(request.form.get("Radial_load"))
        ld = float(request.form.get("desired_life"))
        nd = float(request.form.get("desired_speed"))

        print(af,Fa,Fr,ld,nd)
        def calculate_LD(ld, nd):
            return 60 * ld * nd
        def calculate_XD(LD, LR):
            return float(LD / LR)
        def calculate_Fe(V, Fr, Fa, X, Y):
            return float((X * V * Fr) + (Y * Fa))
        LD = calculate_LD(ld, nd)
        R = float(request.form.get("desired_reliability"))
        XD = calculate_XD(LD=LD, LR=LR)

        table11_1 = pd.read_csv("Data/11_point_1.csv")
        table11_2 = pd.read_csv("Data/11_point_2.csv")
        num_rows = len(table11_1)
        num_rows_half = int(num_rows / 2)

        X = table11_1.loc[num_rows_half, "X2"]
        Y = table11_1.loc[num_rows_half, "Y2"]
        print("X and Y" , X,Y)
        def iteration(j, l):
            C_ten_list = []  # To store C_10 values from the table that are greater than C_ten

            while True:
            # Step 1: Calculate Fe
                Fe = calculate_Fe(V=V, Fa=Fa, Fr=Fr, X=j, Y=l)
                if Fe > Fr:
                    FD = Fe
                    print("FD\n", round(FD, 2))
                else:
                    FD = Fr
                    print("FD\n", round(FD, 2))

                # Step 2: Calculate the new C_ten
                C_ten = af * FD * ((XD / (X_0 + (theta - X_0) * (1 - R) ** (1 / b))) ** (1 / a))
                print("New C_ten\n", round(C_ten, 6))

                # Step 3: Find the smallest C_10 from the table greater than C_ten
                C_o_sec = None  # Initialize C_o_sec
                for i in range(len(table11_2['Load Rating Deep Groove C10 (kN)'])):
                    if table11_2['Load Rating Deep Groove C10 (kN)'][i] > C_ten:
                        # If the same C_10 value has been chosen before, stop iterating
                        if table11_2['Load Rating Deep Groove C10 (kN)'][i] in C_ten_list:
                            print(f"Converged on C_10 value: {table11_2['Load Rating Deep Groove C10 (kN)'][i]} kN")
                            print(f"Select bore of :{table11_2['Bore (mm)'][i]} mm" )
                            dummy = table11_2['Bore (mm)'][i]
                            return table11_2['Bore (mm)'][i]  # Exit the loop
                        else:
                            C_ten_list.append(table11_2['Load Rating Deep Groove C10 (kN)'][i])
                            C_o_sec = table11_2['Load Rating Deep Groove C0 (kN)'][i]  # Update C_o_sec
                            print("C_o_sec", C_o_sec)
                            break

                # Step 4: Check if C_o_sec was found, proceed to update X2 and Y2
                if C_o_sec is not None:
                    # Calculate Fa_by_Co
                    Fa_by_Co = (Fa / C_o_sec)
                    for i in range(1, len(table11_1['Fa/C0'])):
                        if table11_1['Fa/C0'][i] > Fa_by_Co:
                            e2 = table11_1['e'][i]
                            e1 = table11_1['e'][i - 1]
                            print("e2 and e1\n", e2, e1)
                            break

                    # Calculate Fa_by_VFr
                    Fa_by_VFr = Fa / (V * Fr)
                    print("Fa_by_VFr\n", Fa_by_VFr)

                    # Step 5: Update X2 and Y2 based on Fa_by_VFr, then continue the loop
                    if e1 is not None:
                        if Fa_by_VFr <= e1:
                            j = 1  # X1
                            l = 0  # Y1
                        elif Fa_by_VFr >= e2:
                            X2 = 0.56  # Set X2 value
                            g = table11_1['Y2'][i - 1]
                            h = table11_1['Y2'][i]
                            k = table11_1['Fa/C0'][i - 1]
                            l = table11_1['Fa/C0'][i]
                            Y2 = g - (((g) - (h)) * (k - Fa_by_Co)) / (k - l)  # Linear interpolation for Y2
                            j = X2  # Update j to X2
                            l = Y2  # Update l to Y2
                            print("X2 and Y2\n", X2, round(Y2, 2))
                else:
                    print("Error: C_o_sec is None, cannot proceed with calculations.")
                    break
        # iteration(X,Y)
        selected_bore = iteration(X,Y)
        if selected_bore:
            return f"Select bore of: {selected_bore} mm"
        else:
            return "Unable to select a suitable bore."
    else:
        return render_template("ball_bearing.html")
###########################################################################################################################
@app.route("/fos.html",methods = ["POST","GET"])
def page1():
    if request.method == "POST":
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
            Sut = float(request.form.get("Sut"))
            Se = calculate_endurance_limit(Sut)
            print("The calculated value of endurance limit is :", round(Se, 2))
            
            Kf, Kfs = determineK(Sut)
            sig_rev = Kf * float(request.form.get("reversing_stress"))
            # sig_rev = Kf * float(input("Enter value of purely reversing stress :"))
            
            a, b = fatiguelifeconstants(Sut, Se)
            print("Fatigure life constant a :", round(a, 2))
            print("Fatigure life constant b :", round(b, 2))
            
            known_unknown_N = request.form.get("known_unknown")
            # N = float(input("Enter number of cycles to failure N, 0 if unknown:")) #computes Sf
            if known_unknown_N == "known":
                N = float(request.form.get("Number_of_cycles"))
                if N != 0:
                    Sf = a*pow(N, b)
                    print("Fatigure strength at N cycles :", Sf)
                    return Sf
            else:
                N = pow(sig_rev/a, 1/b)
                print("Number of cycles to failure at reversing stress :", round(N, 2))
                return round(N,2)
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
            
            surfacefinish = request.form.get("surface_finish")
            # surfacefinish = input("What is the desired surface finish ('1. ground','2. machined','3. cold-drawn','4. hot-rolled','5. as-forged'): ")
            # surfacefinish = surfacefinish.lower()
            
            if surfacefinish == 'G':
                a = 1.58
                b = -0.085
            elif surfacefinish == 'M' or surfacefinish == 'COLD':
                a = 4.51
                b = -0.265
            elif surfacefinish == 'HR':
                a = 57.7
                b = -0.718
            elif surfacefinish == 'AS':
                a = 272
                b = -0.995
            
            ka = a * pow(Sut, b)
            
            kb = 1
            kc = 1
            kd = 1
            ke = 1
            kf = 1
            
            
            # loadoption = input("Enter load option ('1. bending', '2. torsion', or '3. axial'): ")
            # loadoption = loadoption.lower()
            loadoption = request.form.get("loading_option_1")
            
            if loadoption == 'bending':
                kc = 1
            elif loadoption == 'torsion':
                # kb =1
                kc = 0.59
            elif loadoption == 'axial':
                kc = 0.85
                kb=1
            
            # temp = float(input("Enter temperature Tf if specified, 0 otherwise: "))
            temp = float(request.form.get("T"))
            if temp == 0:
                kd = 1
            else:
                kd = 0.975 + 0.432 * 10E-3 * temp - 0.115 * 10E-5 * pow(temp, 2) + 0.104 * 10E-8 * pow(temp, 3) - 0.595 * 10E-12 * pow(temp, 4)
            
            # reliability = float(input("Enter reliability value if specified, 0 otherwise: "))
            reliability = float(request.form.get("desired_reliability"))
            if reliability == 0.0:
                ke = 1
            else:
                reliability_values = {50: 1.000, 90: 0.897, 95: 0.868, 99: 0.814, 99.9: 0.753, 99.99: 0.702, 99.999: 0.659, 99.9999: 0.620}
                ke = reliability_values.get(reliability, 1)  # Default to 1 if reliability value not in the dictionary
            
            kf = 1
            
            # rotresp = input("Is it a 1. Rotating Shaft or 2. Non-rotating Member? ")
            # rotresp = rotresp.lower()   
            rotresp = request.form.get("rotating/non-rotating")
            if rotresp == 'rotating':  
                if loadoption == 'bending' or loadoption == 'torsion':
                    # d = float(input("Enter the value of diameter in mm, and 0 if unknown: "))
                    d = float(request.form.get("dia"))
                    dia = d       
                else:
                    # d = float(input("Enter the value of diameter in mm, and 0 if unknown: "))
                    d = float(request.form.get("dia"))
                    dia = d
                    kb = 1
                    
            else:
                h = float(request.form.get("height"))
                b = float(request.form.get("width"))
                # h = float(input("Input value h (in mm) of rectangular cross-section of shaft :"))
                # b = float(input("Enter value b (in mm) of rectangular cross-section of shaft :"))
                d = 0.808 * pow(h*b, 0.5)
                dia = d
                print("Effective diameter :", d)
            
            if 2.79 <= d and d <= 51 and loadoption != 'axial':
                kb = 1.24 * pow(d, -0.107)
            elif 51 <= d and d <=254:
                kb = 1.51 * pow(d, -0.157)
            elif d == 0:
                assumption = float(request.form.get("kb/d"))
                # assumption = input("Do you want to assume the value of kb or d?")
                # assumption = assumption.lower()
                if assumption == 'kb':
                    assumedkb = float(request.form.get("assumed_kb"))
                    # assumedkb = float(input("Enter assumed value of Kb :")) #assume kb = 0.85 to start iterations
                    kb = iterate(assumedkb) 
                else:
                    while True:
                        assume_d = float(request.form.get("assumed_dia"))
                        # assume_d = float(input("Enter assumed value of d: "))
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
            sig_max = float(request.form.get("sigma_max"))
            # sig_max = float(input("Enter the value of maximum stress (MPa) :"))
            N = float(request.form.get("N_assume_kb_case"))
            # N = float(input("Enter number of cycles to failure"))
            # a, b = fatiguelifeconstants(Sut, Se)
            h = float(request.form.get("h_assume_kb_case"))
            b = float(request.form.get("b_assume_kb_case"))
            # h = float(input("Input value h (in mm) of rectangular cross-section of shaft :"))
            # b = float(input("Enter value b (in mm) of rectangular cross-section of shaft :"))
            
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
            load = request.form.get("loading_option_2")
            # load = input("Enter load option ('1. bending' , '2. axial', or '3. torsion'): ")
            if load == 'bending' or load == 'axial' or load == 'torsion':
                load = load.lower()
            else:
                print("Invalid load option entered.")
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
            user_input = request.form.get("type_of_loading")
            # user_input = input("Enter loading option ('1. completely reversing simple loading', '2. fluctuating simple loading', or '3. combination of loading modes'): ")
            # user_input = user_input.lower()  

            if user_input == 'CRSL':
                result = reverse_simple_loading()
                print(result)
                return result
            elif user_input == 'FSL':
                result = fluctuating_simple_loading()
                print(result)
            elif user_input == 'CLM':
                result = combination_loading_modes()
                print(result)
            else:
                print("Invalid option. Please enter a valid loading option.")

        #test run
        result = process_loading_option()
        return f"Answer {result}"
        
    else:
        return render_template("fos.html")


# @app.route("/fos2.html")
# def page2():
#     return render_template("fos2.html")

# @app.route("/fos.html",methods = ["POST","GET"])
# def factor():
#     if request.method == "POST":
#         pass
#     return render_template("fos.html")



if __name__ == "__main__":
    app.run(debug=True)



# class User:
#     def __init__(self, name):
#         self.name = name
#         self.is_logged_in = False

# def is_authenticated_decorator(function):
#     def wrapper(*args, **kwargs):
#         if args[0].is_logged_in == True:
#             function(args[0])
#     return wrapper

# @is_authenticated_decorator
# def create_blog_post(user):
#     print(f"This is {user.name}'s new blog post.")

# new_user = User("angela")
# new_user.is_logged_in = True
# create_blog_post(new_user)