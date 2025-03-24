# from bs4 import BeautifulSoup
from flask import redirect, url_for
import cv2
import csv
# import os
# import lxml
import math
from sympy import *
from sympy import symbols, solve
import time 
from flask import Flask , render_template , request , current_app , jsonify
import pandas as pd 
app = Flask(__name__)
dummy = None
def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        function()
        function()
    return wrapper_function


axial = 0
radial = 0
@app.route("/")
def home():
    # template_path = os.path.abspath("/Users/anchit/Documents/GitHub/DME-TLC-/Codes/templates/index.html")
    return render_template("index.html")
            # render_template("/Users/anchit/Documents/GitHub/DME-TLC-/Codes/templates/index.html")

@app.route("/chapter8.html",methods = ["POST","GET"])
def chapter8():
    if request.method == "POST":  
        # Load data
        A31 = pd.read_csv("Data/nominal_sizes_mm.csv")
        table_8_1 = pd.read_csv("Data/screw_thread_data.csv")

        # User input
        type_of_nut = request.form.get("type_of_nut")
        print("Selected Nut:", type_of_nut)

        d = float(type_of_nut.removeprefix("M"))  # Convert to float
        print("Nominal Diameter d:", d)

        l = float(request.form.get("l"))

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

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Calculation Results</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    text-align: center;
                    padding: 50px;
                }}
                .container {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    display: inline-block;
                }}
                h2 {{
                    color: #333;
                }}
                .result {{
                    font-size: 18px;
                    margin: 10px 0;
                    padding: 10px;
                    background: #e6f7ff;
                    border-left: 5px solid #007bff;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Calculation Results</h2>
                <div class="result"><strong>Bolt Length (L):</strong> {L} mm</div>
                <div class="result"><strong>Bolt Stiffness (Kb):</strong> {Kb:.2f} N/mm</div>
                <div class="result"><strong>Joint Stiffness (Km):</strong> {Km:.2f} N/mm</div>
            </div>
        </body>
        </html>
        """

    else:
        return render_template("chapter8.html")


@app.route("/chapter_10.html",methods = ["POST","GET"])
def chapter_10():
    if request.method == "POST":
        # Collect initial inputs
        type_of_spring_ends = (request.form.get("type_of_spring_ends"))
        fmax = float(request.form.get("fmax"))
        ymax = float(request.form.get("ymax"))
        design_factor = float(request.form.get("design_factor")) 
        robus_linearity = float(request.form.get("robus_linearity"))

        diameter = float(request.form.get("diameter")) 
        user_input = (request.form.get("user_input"))

        # Load datasets
        file_path = "Data/spring_wire_constants.csv"
        data = pd.read_csv(file_path)
        file_path_2 = "Data/spring_wire_mechanical_properties.csv"
        data_2 = pd.read_csv(file_path_2)


        def get_material_properties(d, material_name):
            material_data = data[data['Material'].str.contains(material_name, case=False, na=False)]
            matched_rows = []
            
            for i, row in material_data.iterrows():
                try:
                    d_min, d_max = map(float, row['Diameter (in)'].split('-'))
                    if d_min <= d <= d_max:
                        matched_rows.append(row)
                except ValueError:
                    continue
            
            if matched_rows:
                return matched_rows[0]
            else:
                return None


        def get_mechanical_properties(d, material_name):
            filtered_data = data_2[data_2['Material'].str.contains(material_name, case=False, na=False)]
            for _, row in filtered_data.iterrows():
                if is_diameter_in_range(row['Diameter d (in)'], d):
                    return row['E (GPa)'], row['G (GPa)']
            return None, None


        def is_diameter_in_range(dia_range, dia_value):
            if '<' in dia_range:
                return dia_value < float(dia_range.replace('<', ''))
            elif '>' in dia_range:
                return dia_value > float(dia_range.replace('>', ''))
            elif '-' in dia_range:
                lower, upper = map(float, dia_range.split('-'))
                return lower <= dia_value <= upper
            return False


        def calculate_spring_parameters(diameter):
            d = diameter / 25.4
            material_info = get_material_properties(d, user_input)
            
            if material_info is None or material_info.empty:
                print(f"Material {user_input} not found for diameter {diameter} mm")
                return
            
            a_mpa = material_info['A (MPa·mm^m)']
            exponent_m = material_info['Exponent m']
            e_gpa, g_gpa = get_mechanical_properties(d, material_info['Material'])
            
            Ssy = (0.45 * a_mpa) / pow(diameter, exponent_m)
            alpha = Ssy / design_factor
            beta = (8 * (1 + robus_linearity) * fmax) / (math.pi * diameter ** 2)
            x = (2 * alpha - beta) / (4 * beta)
            C = x + math.sqrt((x ** 2 - (3 * alpha) / (4 * beta)))
            
            D = C * diameter
            KB = (4 * C + 2) / (4 * C - 3)
            tau_s = (8 * KB * (1 + robus_linearity) * fmax * D) / (math.pi * pow(diameter, 3))
            OD = D + diameter
            ID = D - diameter
            Na = ((g_gpa * pow(diameter, 4) * ymax) / (8 * pow(D, 3) * fmax)) * 1e3
            
            Nt, Ls, L_o, pitch, Lcr, fom = 0, 0, 0, 0, 0, 0
            if type_of_spring_ends == "P&G":
                Nt = Na + 1
                Ls = diameter * Nt
                L_o = Ls + (1 + robus_linearity) * ymax
                pitch = L_o / (Na + 1)
                Lcr = 2.63 * D / 0.5
            elif type_of_spring_ends == "SOC":
                Nt = Na + 2
                Ls = diameter * (Nt + 1)
                L_o = Ls + (1 + robus_linearity) * ymax
                pitch = (L_o - 3 * diameter) / Na
                Lcr = 2.63 * D / 0.5
            elif type_of_spring_ends == "S&G":
                Nt = Na + 2
                Ls = diameter * Nt
                L_o = Ls + (1 + robus_linearity) * ymax
                pitch = (L_o - 2 * diameter) / Na
                Lcr = 2.63 * D / 0.5

            print(f"Results for diameter {diameter} mm:")
            print(f"OD: {OD}, ID: {ID}, Nt: {Nt}, Ls: {Ls}, L_o: {L_o}, Pitch: {pitch}, Lcr: {Lcr}, Na: {Na} , C: {C}")
            print("------------------------")
            return {
                "Diameter (mm)": diameter, "OD": OD, "ID": ID, "Nt": Nt, "Ls": Ls,
                "L_o": L_o, "Pitch": pitch, "Lcr": Lcr, "Na": Na , "C":C
            }
            

        
        diameters = [diameter - 0.2, diameter - 0.1, diameter, diameter + 0.1, diameter + 0.2, diameter + 0.3]
        
        results = [calculate_spring_parameters(dia) for dia in diameters]
        results = [r for r in results if r is not None]
        
        response = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Spring Design Results</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f4f4f4;
                }}
                h2 {{
                    text-align: center;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: #fff;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: center;
                }}
                th {{
                    background: #007bff;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background: #f2f2f2;
                }}
                .highlight {{
                    background-color: yellow;
                }}
            </style>
        </head>
        <body>
            <h2>Spring Design Results</h2>

            <table>
                <tr>
                    <th>Diameter (mm)</th>
                    <th>Outer Diameter (OD)</th>
                    <th>Inner Diameter (ID)</th>
                    <th>Total Coils (Nt)</th>
                    <th>Solid Length (Ls)</th>
                    <th>Free Length (L_o)</th>
                    <th>Pitch</th>
                    <th>Critical Length (Lcr)</th>
                    <th>Active Coils (Na)</th>
                    <th>C</th>

                </tr>
        '''
        for result in results:
            highlight_Na = 'highlight' if not 3 <= result["Na"] <= 15 else ''
            # highlight_Lcr = 'highlight' if not  4 <= result["Lcr"] <= 12 else ''
            highlight_Ls = 'highlight' if not  result["Ls"] <= 25.4 else ''
            highlight_Lo = 'highlight' if not result["L_o"] <= 101.6 else ''
            highlight_C = 'highlight' if not 4 <= result["C"] <=12 else ''

            response += f'''
                <tr>
                    <td>{result["Diameter (mm)"]:.2f}</td>
                    <td>{result["OD"]:.2f}</td>
                    <td>{result["ID"]:.2f}</td>
                    <td>{result["Nt"]:.2f}</td>
                    <td class="{highlight_Ls}">{result["Ls"]:.2f}</td>
                    <td class="{highlight_Lo}">{result["L_o"]:.2f}</td>
                    <td>{result["Pitch"]:.2f}</td>
                    <td>{result["Lcr"]:.2f}</td>
                    <td class="{highlight_Na}">{result["Na"]:.2f}</td>
                    <td class="{highlight_C}">{result["C"]:.2f}</td>
                </tr>
            '''

        response += '''
            </table>
            <a href="/chapter_10.html"><button>Back</button></a>
            <a href="/"><button>Return to Home</button></a>
        </body>
        </html>
        '''

        return response
        # for dia in diameters:
        #     calculate_spring_parameters(dia)

    else:
        return render_template("chapter_10.html")


@app.route("/chapter12.html",methods = ["POST","GET"])
def chapter12():
    if request.method == "POST":
        table_12_13 = pd.read_csv("Data/viscosity_data.csv")
        def mue_ifnot_temp():
            for i in range(1,len(table_12_13['Temperature (°C)'])):
                if table_12_13['Temperature (°C)'][i] > temp:
                    print("hi ",table_12_13['Temperature (°C)'][i])
                    c = table_12_13['Temperature (°C)'][i]
                    a = table_12_13['Temperature (°C)'][i-2]
                    b = table_12_13['Temperature (°C)'][i-1]
                    if lub == 10:
                        d = table_12_13['SAE 10'][i]
                        e = table_12_13['SAE 10'][i-2]
                        mue = (((e-d)*(b-c))/(a-c)) + d
                        break
                    if lub == 20:
                        d = table_12_13['SAE 20'][i]
                        e = table_12_13['SAE 20'][i-2]
                        mue = (((e-d)*(b-c))/(a-c)) + d
                        break
                    if lub == 30:
                        d = table_12_13['SAE 30'][i]
                        e = table_12_13['SAE 30'][i-2]
                        mue = (((e-d)*(b-c))/(a-c)) + d
                        break
                    if lub == 40:
                        d = table_12_13['SAE 40'][i]
                        e = table_12_13['SAE 40'][i-2]
                        mue = (((e-d)*(b-c))/(a-c)) + d
                        break
                    if lub == 50:
                        d = table_12_13['SAE 50'][i]
                        e = table_12_13['SAE 50'][i-2]
                        mue = (((e-d)*(b-c))/(a-c)) + d
                        break
                    if lub == 60:
                        d = table_12_13['SAE 60'][i]
                        e = table_12_13['SAE 60'][i-2]
                        mue = (((e-d)*(b-c))/(a-c)) + d
                        break
                    if lub == 70:
                        d = table_12_13['SAE 70'][i]
                        e = table_12_13['SAE 70'][i-2]
                        mue = (((e-d)*(b-c))/(a-c)) + d
                        break
            return mue
        def mue_if_temp():
            for i in range(1,len(table_12_13['Temperature (°C)'])):
                if table_12_13['Temperature (°C)'][i] == temp:
                    if lub == 10:
                        mue = table_12_13['SAE 10'][i]
                        break
                    if lub == 20:
                        mue = table_12_13['SAE 20'][i]
                        break
                    if lub == 30:
                        mue = table_12_13['SAE 30'][i]
                        break
                    if lub == 40:
                        mue = table_12_13['SAE 40'][i]
                        break
                    if lub == 50:
                        mue = table_12_13['SAE 50'][i]
                        break
                    if lub == 60:
                        mue = table_12_13['SAE 60'][i]
                        break
                    if lub == 70:
                        mue = table_12_13['SAE 70'][i]
                        break
            return mue
        
        d = float(request.form.get("d"))
        b = float(request.form.get("bush"))
        cmin = (b-d)/2
        print("cmin ",cmin)

        l = float(request.form.get("bush_len"))
        W = float(request.form.get("bush_load"))
        N = float(request.form.get("speed"))
        print("N in rev/sec", N/60)

        l_by_d = l/d
        print("l/d",l_by_d)
        r = d/2
        r_by_c = r/cmin

        P = W/(l*d)
        print("P in MPa ", P)
        lub = float(request.form.get("SAE"))
        temp = float(request.form.get("temp"))
        given_temp = [10,20,30,40,50,60,70,80,90,100,110,120,130,140]
        if temp in given_temp:
            mue = mue_if_temp()
        if temp not in given_temp:
            mue = mue_ifnot_temp()
        print("mue ", mue)
        S = (((r_by_c)**2) *  (mue*pow(10,-3)) *  ((N)/ (pow(10,6) *P)) ) * pow(10,-2)
        print("Sommerfield Number ", S)

        if l_by_d >= 0.5 and l_by_d <=1:
            if S <=0.15:
                if S <=0.04:
                    a = 2.7258
                    b1 = 0.83621
                    b2 = 0.75101
                    b3 = 0.08113
                elif S> 0.04:
                    a = 1.7176
                    b1 = 1.0478
                    b2 = 0.4999
                    b3 = 0.1868
            elif S >0.15:
                if S <= 1:
                    a = 0.91437
                    b1 = 0.4538
                    b2 = 0.6119
                    b3 = -0.2840
                elif S >1:
                    a = 0.89574
                    b1 = 0.3895
                    b2 = 0.3076
                    b3 = -0.2537
        elif l_by_d >= 0.25 and l_by_d < 0.5:
            if S <=0.15:
                if S <=0.04:
                    a = 9.2341
                    b1 = 2.0673
                    b2 = 0.4286
                    b3 = 0.9247
                elif S> 0.04:
                    a = 1.1545
                    b1 = 0.4637
                    b2 = 0.7851
                    b3 = -0.3788
            elif S >0.15:
                if S <= 1:
                    a = 1.1674
                    b1 = 0.80824
                    b2 = 0.48016
                    b3 = -0.02463
                elif S >1:
                    a = 1.1263
                    b1 = 0.7279
                    b2 = 0.5117
                    b3 = -0.6581
        print(" a , b1 , b2 , b3 for hnot/c",a,b1,b2,b3)
        hnot_by_c = a * pow(l_by_d,b1) * pow (S, (b2 + b3 * l_by_d ))
        ho = hnot_by_c * cmin
        print("ho ",ho)


        if l_by_d >= 0.5 and l_by_d <=1:
            if S <=0.15:
                a = 9.4533
                b1 = -0.4758
                b2 = 0.6705
                b3 = -0.1124
            elif S >0.15:
                a = 3.5251
                b1 = -0.2333
                b2 = -0.1926
                b3 = 0.1149

        if l_by_d >= 0.25 and l_by_d <0.5:
            if S <=0.15:
                a = 9.4896
                b1 = -0.5446
                b2 = 0.7290
                b3 = -0.2293
            elif S >0.15:
                a = 17.1869
                b1 = -0.3133
                b2 = 0.7993
                b3 = 0.2887

        rfbyc = a * pow(l_by_d,b1) * pow (S, (b2 + b3 * l_by_d ))
        f = rfbyc * cmin / r

        print("f ",f)

        if l_by_d >= 0.5 and l_by_d <=1:
            if S <=0.15:
                a = 0.74567
                b1 = 0.59651
                b2 = 0.25659
                b3 = 0.04321
            elif S >0.15:
                a = 0.52529
                b1 = 0.2986
                b2 = 0.2335
                b3 = -0.1579

        if l_by_d >= 0.25 and l_by_d <0.5:
            if S <=0.15:
                a = 0.78635
                b1 = 0.57452
                b2 = 0.23670
                b3 = 0.0840
            elif S >0.15:
                a = 0.64927
                b1 = 0.5037
                b2 = 0.2783
                b3 = -0.3536

        p_by_pmax = a * pow(l_by_d,b1) * pow (S, (b2 + b3 * l_by_d ))
        pmax = P / p_by_pmax

        print("pmax " , pmax)

        T = f * W * r * pow ( 10, -3)
        H_loss = 2 * math.pi * T * N * pow ( 10, -3)

        print("Torque ", T)
        print("H_loss ",H_loss)
        return f"""
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
                .result-container {{ background-color: #f8f9fa; padding: 20px; border-radius: 10px; width: 50%; margin: auto; box-shadow: 2px 2px 10px #ccc; }}
                h2 {{ color: #007bff; }}
                p {{ font-size: 18px; font-weight: bold; }}
            </style>
            <div class='result-container'>
                <h2>Results:</h2>
                <p><strong>Heat Loss (H_loss):</strong> {H_loss:.3f} W</p>
                <p><strong>Torque (T):</strong> {T:.3f} Nm</p>
                <p><strong>Maximum Pressure (pmax):</strong> {pmax:.3f} MPa</p>
                <a href="/chapter12.html"><button>Back</button></a>
                <a href="/"><button>Return to Home</button></a>
            </div>
        """
    else:
        return render_template("chapter12.html")


@app.route("/fos_design.html",methods = ["POST","GET"])
def fos_design():
    if request.method == "POST":
        rod_length = float(request.form.get("rod"))
        load = float(request.form.get("load"))
        N = float(request.form.get("N"))
        design_factor = float(request.form.get("design_factor"))
        Sut = float(request.form.get("Sut"))
        if Sut <= 1400:
            Se_ = 0.5 * Sut
        else:
            Se_ = 700
        Sy = float(request.form.get("Sy"))
        surfacefinish = request.form.get("surface_finish")
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
        print("ka",ka)
        assumdkb = float(request.form.get("Kb"))

        loadoption = request.form.get("loading_option_1")
            
        if loadoption == 'bending':
            kc = 1
        elif loadoption == 'torsion':
            # kb =1
            kc = 0.59
        elif loadoption == 'axial':
            kc = 0.85
            kb=1
        kd = 1
        reliability = float(request.form.get("desired_reliability"))
        if reliability == 0:
            ke = 1
        else:
            reliability_values = {50: 1.000, 90: 0.897, 95: 0.868, 99: 0.814, 99.9: 0.753, 99.99: 0.702, 99.999: 0.659, 99.9999: 0.620}
            ke = reliability_values.get(reliability, 1)  # Default to 1 if reliability value not in the dictionary

        kf = 1 ##misc factor 
        Se = ka * assumdkb * kc * kd * ke * kf * Se_
        print("Se",Se)
        f = 1.06 - 4.1 * pow(10,-4) * Sut + 1.5 * pow(10,-7) * pow(Sut,2)
        print("f",f)
        a = (pow((f*Sut),2) / Se)
        b = (- math.log10(f*Sut/Se))/3

        print("a,b",a,b)
        Sf = a * pow(N,b)

        print("Sf",Sf)

        Mmax = load * pow(10,3) * rod_length


        B = pow(((6*Mmax*design_factor)/(Sf * pow(10,6))),0.33333)

        B = B * 1000
        print("B",B)
        d_e = 0.808 * B 

        print("d_e",d_e)
        if 2.79 <= d_e and d_e <= 51 and loadoption != '3':
            kb = 1.24 * pow(d_e, -0.107)
            return f'''
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f4f4f4;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        p {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        button {{
            margin-top: 15px;
            padding: 10px 15px;
            font-size: 16px;
            color: white;
            background: #007BFF;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }}
        button:hover {{
            background: #0056b3;
        }}
    </style>

    <div class="container">
        <p>Kb: <span style="color: #007BFF;">{round(kb,2)} </span></p>
        <a href="/fos_design.html"><button>Back</button></a>
        <a href="/"><button>Return to Home</button></a>
    </div>
'''
            
        elif 51 <= d_e and d_e <=254:
            kb = 1.51 * pow(d_e, -0.157)
            return f'''
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f4f4f4;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        p {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        button {{
            margin-top: 15px;
            padding: 10px 15px;
            font-size: 16px;
            color: white;
            background: #007BFF;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }}
        button:hover {{
            background: #0056b3;
        }}
    </style>

    <div class="container">
        <p>Kb: <span style="color: #007BFF;">{round(kb,2)} </span></p>
        <a href="/fos_design.html"><button>Back</button></a>
        <a href="/"><button>Return to Home</button></a>
    </div>
'''

    else:
        return render_template("fos_design.html")

@app.route("/chapter_14.html",methods = ["POST","GET"])
def chapter_14():
    if request.method == "POST":
        type_of_gear = request.form.get("type_of_gear")
        pressure_angle = float(request.form.get("pressure_angle"))
        number_of_teeth = float(request.form.get("number_of_pinion"))
        Number_of_teeth_gear = float(request.form.get("number_of_gear"))
        Module = float(request.form.get("module"))
        Transmitted_power_by_pinion = float(request.form.get("power_by_Pinion"))
        Pinion_speed = float(request.form.get("pinion_speed"))
        Grade = request.form.get("grade")
        Face_width = float(request.form.get("face_width"))
        Hbp = float(request.form.get("pinion_hardness"))
        Hbg = float(request.form.get("gear_hardness"))
        Crowned_Uncrowned = request.form.get("crowned/uncrowned")
        Quality_standard_number = float(request.form.get("quality_standard_number"))
        Pinion_life_in_no_of_cycles = float(request.form.get("pinion_number_of_cycles"))
        reliability = float(request.form.get("reliability"))
        gear_condition = request.form.get("gear_condition")
        for_ce = request.form.get("assembly/other")
        external_or_internal_gear = request.form.get("external/internal")
        power_source = request.form.get("power_source")
        driven_machine = request.form.get("driven_machine")
        if Crowned_Uncrowned == "crowned":
            cmc = 0.8
        elif Crowned_Uncrowned =="uncrowned":
            cmc = 1
        pitch_dia_pinion = Module * number_of_teeth
        pitch_dia_gear = Module * Number_of_teeth_gear
        pitch_line_velocity = float((math.pi * ((pitch_dia_pinion)*pow(10,-3)) * Pinion_speed)/ 60)
        load = float(Transmitted_power_by_pinion / pitch_line_velocity)
        b = float(0.25*(12-Quality_standard_number)**(2/3))
        A = 50 + 56*(1-b)
        Kv = float(((A+math.sqrt(200*pitch_line_velocity))/A)**b)
        data = pd.read_csv("Data/teeth_vs_y.csv")
        data['Number_of_Teeth'] = pd.to_numeric(data['Number_of_Teeth'])
        data['Y'] = pd.to_numeric(data['Y'])

        def interpolate_y(number_of_teeth, data):
            teeth = data['Number_of_Teeth'].values
            y_values = data['Y'].values

            if number_of_teeth < teeth.min() or number_of_teeth > teeth.max():
                raise ValueError("Number of teeth is outside the range of available data.")


            for i in range(len(teeth) - 1):
                if teeth[i] <= number_of_teeth <= teeth[i + 1]:
                    
                    x1, x2 = teeth[i], teeth[i + 1]
                    y1, y2 = y_values[i], y_values[i + 1]
                    interpolated_y = y1 + (y2 - y1) * ((number_of_teeth - x1) / (x2 - x1))
                    return interpolated_y

            raise ValueError("Interpolation failed. Check the input data.")

        interpolated_y_pinion = interpolate_y(number_of_teeth, data)
        print(f"Interpolated Y for {number_of_teeth} teeth: {interpolated_y_pinion}")
        gear_ratio = float(Number_of_teeth_gear/number_of_teeth)
        number_of_teeth = Number_of_teeth_gear
        interpolated_y_gear = interpolate_y(number_of_teeth,data)
        print(f"Interpolated Y for {number_of_teeth} teeth: {interpolated_y_gear}")



        Ks_p = 0.8433 * ((Module * Face_width * math.sqrt(interpolated_y_pinion))**0.0535)
        Ks_g = 0.8433 * ((Module * Face_width * math.sqrt(interpolated_y_gear))**0.0535)

        print("Ks_p,Ks_g",Ks_p,Ks_g)

        if Face_width <=25:
            cpf = (Face_width/(10*pitch_dia_pinion)) - 0.025 
        elif Face_width > 25 and Face_width <=425:
            cpf = (Face_width/(10*pitch_dia_pinion)) - 0.0375 +4.92*pow(10,-4)*Face_width
        elif Face_width >425 and Face_width <=1000:
            cpf = (Face_width/(10*Face_width)) - 0.1109 +8.15*pow(10,-4)*Face_width - 3.53*pow(10,-7)*Face_width**2
        print("cpf",cpf)
        cpm = 1 
        gear_conditions = pd.read_csv("Data/corrected_gear_conditions.csv")
        if gear_condition == "O":
            A_gear = 0.247
            B_gear = 0.0167
            C_gear = -0.765 * pow (10,-4)
        elif gear_condition == "C":
            A_gear = 0.127
            B_gear = 0.0158
            C_gear = -0.930 * pow(10,-4)
        elif gear_condition == "P":
            A_gear = 0.0675
            B_gear = 0.0128
            C_gear = -0.926 * pow(10,-4)
        elif gear_condition == "E":
            A_gear = 0.00360
            B_gear = 0.0102
            C_gear = -0.822 * pow(10,-4)

        Face_width_in_inch = Face_width / 25.4
        print("Face_width_in_inch",Face_width_in_inch)
        print("A_gear,B_gear,C_gear",A_gear,B_gear,C_gear)
        cma = A_gear + B_gear*Face_width_in_inch + C_gear*pow(Face_width_in_inch,2)


        print("cma",cma)
        if for_ce == "assembly":
            ce = 0.8
        elif for_ce =="other":
            ce =1 
        Kh = 1 + cmc * (cpf*cpm + cma * ce)
        print("cmc,cma,cpm,cpf,ce",cmc,cma,cpm,cpf,ce)
        print("Kh",Kh)
        N = Pinion_life_in_no_of_cycles
        Yn_pinion = 1.3558 * pow(N,-0.0178)
        Yn_gear = 1.3558 * pow((N / (Number_of_teeth_gear/number_of_teeth)),-0.0178)

        print("Yn_pinion,Yn_gear",Yn_pinion,Yn_gear)
        ################################
        Yj_p = 0.33
        Yj_g = 0.38 
        ################################
        if reliability > 0.5 and reliability < 0.99:
            Yz = 0.658 - 0.0759*math.log(1-reliability)
        elif reliability >= 0.99 and reliability <= 0.9999:
            Yz = 0.50 - 0.109*math.log(1-reliability)

        mn = 1
        

        if external_or_internal_gear =="external":
            a = math.cos(math.radians(pressure_angle))*math.sin(math.radians(pressure_angle))*gear_ratio
            b = 2*mn*(gear_ratio+1)
            zi = a/b
        elif external_or_internal_gear=="internal":
            a = math.cos(math.radians(pressure_angle))*math.sin(math.radians(pressure_angle))*gear_ratio
            b = 2*mn*(gear_ratio-1)
            zi = a/b
        Ze = (191 * math.sqrt(pow(10,6)))/1000
        print("Ze",Ze)
        print("pressure_angle,gear_ratio,mn",pressure_angle,gear_ratio,mn)
        print("zi",zi)
        if Grade == "1":
            Stp = 0.553 * Hbp + 88.3 
            Stg = 0.553 * Hbg + 88.3
        elif Grade == "2":
            Stp = 0.703 * Hbp + 113
            Stg = 0.703 * Hbg + 113

        if Grade == "1":
            Scp = 2.22 * Hbp + 200
            Scg = 2.22 * Hbg + 200
        elif Grade == "2":
            Scp = 2.41 * Hbp + 237
            Scg = 2.41 * Hbg + 237

        Zn = 1.4488 * pow(N,-0.023)
        if float(Hbp/Hbg) <1.2:
            Ch = 1

        if power_source == "U":
            if driven_machine == "U":
                Ko =1
            if driven_machine == "ModS":
                Ko = 1.25
            if driven_machine == "HS":
                Ko =1.75
        if power_source == "LS":
            if driven_machine == "U":
                Ko =1.25
            if driven_machine == "ModS":
                Ko = 1.5
            if driven_machine == "HS":
                Ko =2
        if power_source == "MS":
            if driven_machine == "U":
                Ko =1.5
            if driven_machine == "ModS":
                Ko = 1.75
            if driven_machine == "HS":
                Ko =2.25
        Kb = 1 
        Y_thetha = 1

        sigma_p = (load  * Ko * Kv * Ks_p * Kh * Kb)/(Face_width * Module * Yj_p)
        sigma_g= (load  * Ko * Kv * Ks_g * Kh * Kb)/(Face_width * Module * Yj_g)

        Sf_p = (Stp * Yn_pinion)/(sigma_p*Y_thetha*Yz)
        Sf_g = (Stg * Yn_gear)/(sigma_g*Y_thetha*Yz)
        Zr = 1
        sigma_c_p = Ze * math.sqrt((load*Ko*Kv*Ks_p*Kh*Zr)/(pitch_dia_pinion*Face_width*zi))
        print("load,Ko,Kv,A,b,Ks_p,Kh,Zr,pitch_dia_pinion,Face_width,zi",load,Ko,Kv,A,b,Ks_p,Kh,Zr,pitch_dia_pinion,Face_width,zi)
        print("pitch_line_velocity",pitch_line_velocity)
        # sigma_c_g = Ze * math.sqrt((load*Ko*Kv*Ks_g*Kh*Zr)/(pitch_dia_gear*Face_width*zi))
        sigma_c_g = math.sqrt(Ks_g/Ks_p) * sigma_c_p

        print("sigma_c_g", sigma_c_g)
        print("sigma_c_p",sigma_c_p)
        Zw = 1
        print("Scp,Zn,Zw,Y_thetha,Yz",Scp,Zn,Zw,Y_thetha,Yz)
        Sh_p = (Scp*Zn*Zw)/(sigma_c_p * Y_thetha * Yz)
        Sh_g = (Scg*Zn*Zw)/(sigma_c_g * Y_thetha * Yz)

        print("Sh_p",Sh_p)
        print("Sh_g",Sh_g)

        return f'''
    <style>
        table {{
            width: 50%;
            border-collapse: collapse;
            margin: 20px auto;
            background: white;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }}
        th, td {{
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #007BFF;
            color: white;
        }}
        tr:hover {{
            background-color: #f1f1f1;
        }}
        button {{
            display: block;
            margin: 20px auto;
            padding: 10px 15px;
            font-size: 16px;
            color: white;
            background: #007BFF;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }}
        button:hover {{
            background: #0056b3;
        }}
    </style>

    <table>
        <tr>
            <th>Parameter</th>
            <th>Value</th>
        </tr>
        <tr><td>σ<sub>c_g</sub> (MPa)</td><td>{round(sigma_c_g,3)}</td></tr>
        <tr><td>σ<sub>c_p</sub> (MPa)</td><td>{round(sigma_c_p,3)}</td></tr>
        <tr><td>Sh<sub>p</sub></td><td>{round(Sh_p,9)}</td></tr>
        <tr><td>Sh<sub>g</sub></td><td>{round(Sh_g,9)}</td></tr>
        <tr><td>σ<sub>p</sub> (MPa)</td><td>{round(sigma_p,9)}</td></tr>
        <tr><td>σ<sub>g</sub> (MPa)</td><td>{round(sigma_g,3)}</td></tr>
        <tr><td>Sf<sub>p</sub></td><td>{round(Sf_p,3)}</td></tr>
        <tr><td>Sf<sub>g</sub></td><td>{round(Sf_g,3)}</td></tr>
    </table>

    <a href="/chapter_14.html"><button>Back</button></a>
    <a href="/"><button>Return to Home</button></a>
'''     
        # return f'''<p> sigma_c_g: {round(sigma_c_g,3)} MPa</p><br><p>sigma_c_p: {round(sigma_c_p,3)} MPa</p><br><p>Sh_p: {round(Sh_p,9)}</p><br><p>Sh_g: {round(Sh_g,9)}</p><br><p>Sigma Pinion: {round(sigma_p,9)} MPa</p><br><p>Sigma gear: {round(sigma_g,3)} MPa</p><br><p>Sf_p: {round(Sf_p,3)}</p><br><p>Sf_g: {round(Sf_g,3)}</p>
        #     <a href="/"><button>Return to Home</button></a>
        #     '''
    else:
        return render_template("chapter_14.html")

@app.route("/bearing_selection.html",methods = ["POST","GET"])
def select():
    if request.method == "POST":
        global axial
        global radial
        axial = float(request.form.get('ax_load'))
        radial = float(request.form.get('r_load'))
        if axial <= 0.05*radial:
            return redirect(url_for('cylindrical_bearing'))
        else:
            return redirect(url_for('ball_bearing'))
    else:
        return render_template("bearing_selection.html")


@app.route("/ball_bearing.html",methods = ["POST","GET"])
def ball_bearing():
    if request.method == "POST":
        ###bearing type
        # if request.form.get('name') == "Ball":
        print("Ball bearing selected")
        a = 3
        b = 1.483
        X_0 = 0.02
        theta = 4.459
        LR = pow(10, 6)
        # elif request.form.get('name') == "Taper":
        #     print("Tapered Roller Bearing selected")
        #     a = 10 / 3
        #     b = 1.5
        #     X_0 = 0.0
        #     theta = 4.48
        #     LR = 90 * pow(10, 6)
        # else:
        #     print("Cylinder Roller Bearing selected")
        #     a = 10 / 3
        #     b = 1.483
        #     X_0 = 0.02
        #     theta = 4.459
        #     LR = pow(10, 6)
        inner_ring = request.form.get('ring_rotation')
        if inner_ring == "inner":
            V =1.0
        else:
            outer_ring = request.form.get('ring_rotation')
            V = 1.2
        
        af = float(request.form.get('af')) or int(request.form.get('af'))
        Fa = axial
        Fr = radial
        print("Fa",axial)
        print("Fr",radial)
        # Fa = float(request.form.get("Axial_load"))
        # Fr = float(request.form.get("Radial_load"))
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
            return f'''
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f4f4f4;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        p {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        button {{
            margin-top: 15px;
            padding: 10px 15px;
            font-size: 16px;
            color: white;
            background: #007BFF;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }}
        button:hover {{
            background: #0056b3;
        }}
    </style>

    <div class="container">
        <p>Bore Selection: <span style="color: #007BFF;">{selected_bore} mm</span></p>
        <a href="/ball_bearing.html"><button>Back</button></a>
        <a href="/"><button>Return to Home</button></a>
    </div>
'''
            # return f'''<p>Select bore of: {selected_bore} mm</p>
            # <a href="/"><button>Return to Home</button></a>
            # '''
        else:
            return "Unable to select a suitable bore, possibly the diameter exceeds 95 mm"
    else:
        return render_template("ball_bearing.html")
    
@app.route("/cylindrical_bearing.html", methods=["POST", "GET"])
def cylindrical_bearing():
    if request.method == "POST":
        print("Cylinder Roller Bearing selected")
        try:
            a = 10 / 3
            b = 1.483
            X_0 = 0.02
            theta = 4.459
            LR = pow(10, 6)

            inner_ring = request.form.get('ring_rotation')
            if inner_ring == "inner":
                V = 1.0
            else:
                V = 1.2

            af = float(request.form.get('af') or 0)  # Default to 0 if not provided
            global axial
            global radial
            Fa = axial
            Fr = radial

            print("Fa and Fr are ",Fa,Fr)
            # Fa = float(request.form.get("Axial_load") or 0)
            # Fr = float(request.form.get("Radial_load") or 0)
            ld = float(request.form.get("desired_life") or 0)
            nd = float(request.form.get("desired_speed") or 0)

            print(af, Fa, Fr, ld, nd)

            def calculate_LD(ld, nd):
                return 60 * ld * nd

            def calculate_XD(LD, LR):
                return float(LD / LR)

            def calculate_Fe(V, Fr, Fa, X, Y):
                return float((X * V * Fr) + (Y * Fa))

            LD = calculate_LD(ld, nd)
            R = float(request.form.get("desired_reliability") or 0.9)  # Default reliability

            XD = calculate_XD(LD=LD, LR=LR)

            # Load the required CSV files
            table11_1 = pd.read_csv("Data/11_point_1.csv")
            table_11_3_series_02 = pd.read_csv("Data/Cylindrical_Roller_Bearings.csv")
            table_11_3_series_03 = pd.read_csv("Data/Cylindrical_Roller_Bearings_03_Series.csv")

            num_rows = len(table11_1)
            num_rows_half = int(num_rows / 2)

            X = table11_1.loc[num_rows_half, "X2"]
            # Y = table11_1.loc[num_rows_half, "Y2"]
            Y = 0
            
            print("X and Y", X, Y)

            def iteration(j, l):
                C_ten_list = []  # To store C_10 values from the table that are greater than C_ten

                while True:
                    # Step 1: Calculate Fe
                    Fe = calculate_Fe(V=V, Fa=Fa, Fr=Fr, X=j, Y=l)
                    FD = Fe if Fe > Fr else Fr
                    print("FD\n", round(FD, 2))

                    # Step 2: Calculate the new C_ten
                    C_ten = af * FD * ((XD / (X_0 + (theta - X_0) * (1 - R) ** (1 / b))) ** (1 / a))
                    print("New C_ten\n", round(C_ten, 6))

                    # Series logic
                    series = float(request.form.get("series") or 0)
                    series_table = table_11_3_series_02 if series == 2 else table_11_3_series_03

                    for i in range(len(series_table['Load Rating C10 (kN)'])):
                        if series_table['Load Rating C10 (kN)'][i] > C_ten:
                            if series_table['Load Rating C10 (kN)'][i] in C_ten_list:
                                print(f"Converged on C_10 value: {series_table['Load Rating C10 (kN)'][i]} kN")
                                print(f"Select bore of :{series_table['Bore (mm)'][i]} mm")
                                return series_table['Bore (mm)'][i]
                            else:
                                C_ten_list.append(series_table['Load Rating C10 (kN)'][i])
                                break
                    else:
                        return None

            selected_bore = iteration(X, Y)
            if selected_bore:
                return f'''
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f4f4f4;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        p {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        button {{
            margin-top: 15px;
            padding: 10px 15px;
            font-size: 16px;
            color: white;
            background: #007BFF;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }}
        button:hover {{
            background: #0056b3;
        }}
    </style>

    <div class="container">
        <p>Bore Selection: <span style="color: #007BFF;">{selected_bore} mm</span></p>
        <a href="/cylindrical_bearing.html"><button>Back</button></a>
        <a href="/"><button>Return to Home</button></a>
    </div>s
'''


            #     return f'''<p>Select bore of: {selected_bore} mm</p>
            # <a href="/"><button>Return to Home</button></a>
            # '''
            else:
                return "Unable to select a suitable bore, possibly the diameter exceeds 95 mm"
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred during processing."
    else:
        return render_template("cylindrical_bearing.html")


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
                if N != 0.0:
                    Sf = a*pow(N, b)
                    print("Fatigue strength at N cycles :", Sf)
                    print("N",N)
                    return "Fatigue Strength (MPa) : ", round(Sf,2) 
            else:
                N = pow(sig_rev/a, 1/b)
                print("Number of cycles to failure at reversing stress :", round(N, 2))
                print("N",N)
                return "Number of cycles to Failure :" , round(N,2)
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
                assumption = request.form.get("kb_d")
                # assumption = input("Do you want to assume the value of kb or d?")
                # assumption = assumption.lower()
                if assumption == 'Kb':
                    assumedkb = float(request.form.get("assumed_kb"))
                    # assumedkb = float(input("Enter assumed value of Kb :")) #assume kb = 0.85 to start iterations
                    kb = iterate(assumedkb) 
                    print(kb)
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
            global d
            global dia
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
            
            if kb <= assumedKb:
                return kb
                dia = d
            else:

                return assumedKb

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
            print("dia in notch", dia)
            r = dia/2
            print("r",r)
            if load == 'bending' or load == 'axial':
                sqrta = 1.24 - 2.25*10E-3*Sut + 1.60*10E-5*Sut**2 - 4.11*10E-8*Sut**3
            else:
                sqrta = 0.958 -1.83*10E-3*Sut + 1.43*10E-5*Sut**2 - 4.11*10E-8*Sut**3
            q = 1/(1+(sqrta/math.sqrt(r))) 
            
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
        return f'''Answer :  {result}
                <a href="/"><button>Return to Home</button></a>'''
        
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