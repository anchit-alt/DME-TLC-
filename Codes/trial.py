import pandas as pd
import math

# Collect initial inputs
type_of_spring_ends = float(input("Enter type of spring ends, 1. Plain and ground 2. Squared or Closed, 3. Squared and Ground: "))
fmax = float(input("Enter fmax: "))
ymax = float(input("Enter ymax: "))
design_factor = float(input("Enter design factor ns(d): "))
robus_linearity = float(input("Enter Robust linearity: "))

diameter = float(input("Enter the initial wire diameter (mm): "))
user_input = input("Enter the material name: ")

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
    if type_of_spring_ends == 1:
        Nt = Na + 1
        Ls = diameter * Nt
        L_o = Ls + (1 + robus_linearity) * ymax
        pitch = L_o / (Na + 1)
        Lcr = 2.63 * D / 0.5
    elif type_of_spring_ends == 2:
        Nt = Na + 2
        Ls = diameter * (Nt + 1)
        L_o = Ls + (1 + robus_linearity) * ymax
        pitch = (L_o - 3 * diameter) / Na
        Lcr = 2.63 * D / 0.5
    elif type_of_spring_ends == 3:
        Nt = Na + 2
        Ls = diameter * Nt
        L_o = Ls + (1 + robus_linearity) * ymax
        pitch = (L_o - 2 * diameter) / Na
        Lcr = 2.63 * D / 0.5
    
    print(f"Results for diameter {diameter} mm:")
    print(f"OD: {OD}, ID: {ID}, Nt: {Nt}, Ls: {Ls}, L_o: {L_o}, Pitch: {pitch}, Lcr: {Lcr}, Na: {Na}")
    print("------------------------")


diameters = [diameter - 0.2, diameter - 0.1, diameter, diameter + 0.1, diameter + 0.2, diameter + 0.3]

for dia in diameters:
    calculate_spring_parameters(dia)
