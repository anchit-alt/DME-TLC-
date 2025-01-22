import math
import pandas as pd
import numpy as np

# type_of_gear = input("1. Spur , 2. bevel")
# pressure_angle = input("Pressure angle")
number_of_teeth = int(input("No . of teeth in pinion "))
# Number_of_teeth_gear= input("No . of teeth in gear")
# Module = input("Enter Module")
# Transmitted_power_by_pinion = input("Transmitted_power_by_pinion (Watt)")
# Pinion_speed = input("Pinion Speed in rev/min")
# Grade = input("Grade 1 or 2")
# Face_width = input("Enter Face width (mm)")
# hardness_of_steel = input("Hardness of Steel in Brinel")
# Crowned_Uncrowned = input("1. Crowned / 2. Uncrowned")
# Quality_standard_number = input("Quality standard number")
# Pinion_life_in_no_of_cycles = input("Enter Pinion Life in number of Cycles")
# reliability = float(input("Enter reliabilty in decimal"))

# pitch_dia_pinion = Module * Number_of_teeth_pinion
# pitch_dia_gear = Module * Number_of_teeth_gear
# pitch_line_velocity = float((math.pi * pitch_dia_pinion * Pinion_speed)/ 60)
# load = float(Transmitted_power_by_pinion / pitch_line_velocity)
# b = 0.25(12-Quality_standard_number)**(2/3)
# A = 50 + 56(1-b)
# Kv = float((A+math.sqrt(200*pitch_line_velocity)/(A))**b)
# print("Kv", Kv)

data = pd.read_csv("Data/teeth_vs_y.csv")

data['Number_of_Teeth'] = pd.to_numeric(data['Number_of_Teeth'])
data['Y'] = pd.to_numeric(data['Y'])

def interpolate_y(number_of_teeth, data):
    teeth = data['Number_of_Teeth'].values
    y_values = data['Y'].values

    if number_of_teeth < teeth.min() or number_of_teeth > teeth.max():
        raise ValueError("Number of teeth is outside the range of available data.")

    # Find the two nearest points
    for i in range(len(teeth) - 1):
        if teeth[i] <= number_of_teeth <= teeth[i + 1]:
            # Perform linear interpolation
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

