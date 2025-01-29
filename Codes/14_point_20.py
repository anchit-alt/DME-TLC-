import math
import pandas as pd
import numpy as np

type_of_gear = float(input("1. Spur , 2. bevel"))
pressure_angle = float(input("Pressure angle"))
number_of_teeth= int(input("No . of teeth in pinion "))
Number_of_teeth_gear= float(input("No . of teeth in gear"))
Module = float(input("Enter Module"))
Transmitted_power_by_pinion = float(input("Transmitted_power_by_pinion (Watt)"))
Pinion_speed = float(input("Pinion Speed in rev/min"))
Grade = float(input("Grade 1 or 2"))
Face_width = float(input("Enter Face width (mm)"))
Hbp = float(input("Hardness of pinion in Brinel"))
Hbg = float(input("Hardness of gear in Brinel"))
Crowned_Uncrowned = float(input("1. Crowned / 2. Uncrowned"))
if Crowned_Uncrowned == 1:
    cmc = 0.8
elif Crowned_Uncrowned ==2:
    cmc = 1
Quality_standard_number = float(input("Quality standard number"))
Pinion_life_in_no_of_cycles = float(input("Enter Pinion Life in number of Cycles"))
reliability = float(input("Enter reliabilty in decimal"))

pitch_dia_pinion = Module * number_of_teeth
pitch_dia_gear = Module * Number_of_teeth_gear
pitch_line_velocity = float((math.pi * pitch_dia_pinion * Pinion_speed)/ 60)
load = float(Transmitted_power_by_pinion / pitch_line_velocity)
b = float(0.25*(12-Quality_standard_number)**(2/3))
A = 50 + 56*(1-b)
Kv = float((A+math.sqrt(200*pitch_line_velocity)/(A))**b)
print("Kv", Kv)

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

number_of_teeth = int(input("No . of teeth in gear "))
interpolated_y_gear = interpolate_y(number_of_teeth,data)
print(f"Interpolated Y for {number_of_teeth} teeth: {interpolated_y_gear}")



Ks_p = 0.8433 * (Module * Face_width * math.sqrt(interpolated_y_pinion)**0.0535)
Ks_g = 0.8433 * (Module * Face_width * math.sqrt(interpolated_y_gear)**0.0535)

if Face_width <=25:
    cpf = (Face_width/(10*pitch_dia_pinion)) - 0.025 
elif Face_width > 25 and Face_width <=425:
    (Face_width/(10*pitch_dia_pinion)) - 0.0375 +4.92*pow(10,-4)*Face_width
elif Face_width >425 and Face_width <=1000:
    (Face_width/(10*Face_width)) - 0.1109 +8.15*pow(10,-4)*Face_width - 3.53*pow(10,-7)*Face_width**2

cpm = 1 
gear_condition = float(input("1. Open Gearing , 2. Commercial, 3. Precision, 4. Extraprecision"))
gear_conditions = pd.read_csv("Data/corrected_gear_conditions.csv")

if gear_condition == 1:
    A_gear = 0.247
    B_gear = 0.0167
    C_gear = -0.765 * pow (10,-4)
elif gear_condition == 2:
    A_gear = 0.127
    B_gear = 0.0158
    C_gear = -0.930 * pow(10,-4)
elif gear_condition == 3:
    A_gear = 0.0675
    B_gear = 0.0128
    C_gear = -0.926 * pow(10,-4)
elif gear_condition == 4:
    A_gear = 0.00360
    B_gear = 0.0102
    C_gear = -0.822 * pow(10,-4)

Face_width_in_inch = Face_width / 12

cma = A_gear + B_gear*Face_width_in_inch + C_gear*pow(Face_width_in_inch,2)

for_ce = float(input(" 1. bearing adjusted at assembly or compatibilty improved by lapping or bore , 2. for all other conditions"))
if for_ce == 1:
    ce = 0.8
elif for_ce ==2:
    ce =1 

Kh = 1 + cmc * (cpf*cpm + cma * ce)

N = Pinion_life_in_no_of_cycles
Yn_pinion = 1.3388 * pow(N,-0.0178)
Yn_gear = 1.388 * pow((N / (Number_of_teeth_gear/number_of_teeth)),-0.0178)

################################
Yj_p = 0.33
Yj_g = 0.38 
################################

if reliability > 0.5 and reliability < 0.99:
    Yz = 0.658 - 0.0759*math.log(1-reliability)
elif reliability >= 0.99 and reliability <= 0.9999:
    Yz = 0.50 - 0.109*math.log(1-reliability)

mn = 1
gear_ratio = Number_of_teeth_gear/number_of_teeth
external_or_internal_gear = float(input("1. External Gear, 2. Internal Gear"))
if external_or_internal_gear ==1:
    zi = (math.cos(pressure_angle)*math.sin(pressure_angle)*gear_ratio)/(2*mn*(gear_ratio+1))
elif external_or_internal_gear==2:
    zi = (math.cos(pressure_angle)*math.sin(pressure_angle)*gear_ratio)/(2*mn*(gear_ratio-1))

Ze = 191 * math.sqrt(pow(10,6))

if Grade == 1:
    Stp = 0.553 * Hbp + 88.3 
    Stg = 0.553 * Hbg + 88.3
elif Grade == 2:
    Stp = 0.703 * Hbp + 113
    Stg = 0.703 * Hbg + 113

if Grade == 1:
    Scp = 0.568 * Hbp + 83.8
    Scg = 0.568 * Hbg + 83.8
elif Grade == 2:
    Scp = 0.749 * Hbp + 110
    Scg = 0.749 * Hbg + 110

Zn = 1.4488 * pow(N,-0.023)

if Hbp/Hbg <1.2:
    Ch = 1

power_source = float(input("1. Uniform, 2. Light Shock, 3. Medium Shock"))
driven_machine = float(input("1. Uniform, 2. Moderate Shock, 3. Heavy Shock"))
overload_factors_table = pd.read_csv("Data/overload_factors.csv")

if power_source == 1:
    if driven_machine == 1:
        Ko =1
    if driven_machine == 2:
        Ko = 1.25
    if driven_machine == 3:
        Ko =1.75
if power_source == 2:
    if driven_machine == 1:
        Ko =1.25
    if driven_machine == 2:
        Ko = 1.5
    if driven_machine == 3:
        Ko =2
if power_source == 3:
    if driven_machine == 1:
        Ko =1.5
    if driven_machine == 2:
        Ko = 1.75
    if driven_machine == 3:
        Ko =2.25

Kb = 1 
Y_thetha = 1

sigma_p = (load  * Ko * Kv * Ks_p * Kh * Kb)/(Face_width * Module * Yj_p)
sigma_g= (load  * Ko * Kv * Ks_g * Kh * Kb)/(Face_width * Module * Yj_g)

print("sigma pinion" , sigma_p)
print("sigma gear" , sigma_g)

Sf_p = (Stp * Yn_pinion)/(sigma_p*Y_thetha*Yz)
Sf_g = (Stg * Yn_gear)/(sigma_g*Y_thetha*Yz)

print("Sf pinion", Sf_p)
print("Sf gear",Sf_g)

#surface condition factor (Zr)
Zr = 1
sigma_c_p = Ze * math.sqrt((load*Ko*Kv*Ks_p*Kh*Zr)/(pitch_dia_pinion*Face_width*zi))
sigma_c_g = Ze * math.sqrt((load*Ko*Kv*Ks_g*Kh*Zr)/(pitch_dia_gear*Face_width*zi))

print("sigma_c_g", sigma_c_g)
print("sigma_c_p",sigma_c_p)
Zw = 1
Sh_p = (Scp*Zn*Zw)/(sigma_c_p * Y_thetha * Yz)
Sh_g = (Scg*Zn*Zw)/(sigma_c_g * Y_thetha * Yz)

print("Sh_p",Sh_p)
print("Sh_g",Sh_g)
