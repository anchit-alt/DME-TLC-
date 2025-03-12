import pandas as pd
import math

type_of_spring_ends = float(input("Enter type of spring ends, 1. Plain and ground 2. Squared or Closed, 3. Squared and Ground"))

fmax = float(input("Enter fmax "))
ymax = float(input("Enter ymax "))
# assumed_dia = float(input("Enter assumed Dia "))

# Load the dataset
file_path = "Data/spring_wire_constants.csv"
data = pd.read_csv(file_path)

material_name = None
a_mpa = None
exponent_m = None
e_gpa = None
g_gpa = None
# Ask the user for material name and diameter
diameter = float(input("Enter the wire diameter (mm): "))
diameter = diameter / 25.4
user_input = input("Enter the material name: ")


# Search for the material
material_data = data[data['Material'].str.contains(user_input, case=False, na=False)]

if material_data.empty:
    print("Material not found. Please check the name and try again.")
else:
    # Filter rows where the diameter falls within the range
    matched_rows = []
    for i, row in material_data.iterrows():
        try:
            d_min, d_max = map(float, row['Diameter (in)'].split('-'))
            if d_min <= diameter <= d_max:
                matched_rows.append(row)
        except ValueError:
            continue
    
    if matched_rows:
        selected_material = matched_rows[0]
        
        # Store selected material properties in variables

        material_name = selected_material['Material']
        astm_no = selected_material['ASTM No.']
        a_ksi = selected_material['A (ksi·in^m)']
        a_mpa = selected_material['A (MPa·mm^m)']
        exponent_m = selected_material['Exponent m']
        
        # Print the extracted info
        print(f"Material: {material_name}")
        print(f"ASTM No.: {astm_no}")
        print(f"A (ksi·in^m): {a_ksi}")
        print(f"A (MPa·mm^m): {a_mpa}")
        print(f"Exponent m: {exponent_m}")
    else:
        print("No matching row found for the given diameter.")


# material_name = "Music wire A228"
file_path_2 = "Data/spring_wire_mechanical_properties.csv"
data_2 = pd.read_csv(file_path_2)
# Filter the data for the specified material
# material_data = data_2[data_2['Material'].str.contains(material_name, case=False, na=False)]

# if material_data.empty:
#     print(f"No data found for material: {material_name}")
# else:
#     # Extract the exact values of E and G in GPa
#     e_gpa = material_data['E (GPa)'].values
#     g_gpa = material_data['G (GPa)'].values
    
#     print(f"For material: {material_name}")
#     print(f"E (GPa): {e_gpa}")
#     print(f"G (GPa): {g_gpa}")


def is_diameter_in_range(dia_range, dia_value):
    if '<' in dia_range:
        return dia_value < float(dia_range.replace('<', ''))
    elif '>' in dia_range:
        return dia_value > float(dia_range.replace('>', ''))
    elif '-' in dia_range:
        lower, upper = map(float, dia_range.split('-'))
        return lower <= dia_value <= upper
    return False

# Filter the data based on material and diameter range
filtered_data = data_2[data_2['Material'].str.contains(material_name, case=False, na=False)]

matching_row = None
for _, row in filtered_data.iterrows():
    if is_diameter_in_range(row['Diameter d (in)'], diameter):
        matching_row = row
        break

if matching_row is not None:
    e_gpa = matching_row['E (GPa)']
    g_gpa = matching_row['G (GPa)']
    print(f"For material: {material_name} and diameter {diameter} in")
    print(f"E (GPa): {e_gpa}")
    print(f"G (GPa): {g_gpa}")
else:
    print(f"No matching entry found for material: {material_name} with diameter {diameter} in")

design_factor = float(input("Enter design factor ns(d) "))
robus_linearity = float(input("Enter Robust linearity "))

Ssy = (0.45 * a_mpa )/ pow(diameter,exponent_m)
print("Ssy",Ssy)

alpha = Ssy / design_factor
print("alpha",alpha)

beta = (8 * (1 + robus_linearity) * fmax )/ (math.pi * diameter**2)
print("beta",beta)
x = (2*alpha - beta)/(4*beta) 
C = x + math.sqrt((pow(x,2) - ((3*alpha)/(4*beta))))
print("C",C)

D = C * diameter
print("D",D)

KB = (4 * C +2)/(4*C - 3)
print("KB",KB)
tau_s = (8 * KB * (1 +robus_linearity) * fmax * D)/(math.pi * pow(diameter,3))
print("tau_s",tau_s)

design_factor = Ssy / tau_s
print("design_factor",design_factor)

OD  = D + diameter
print("OD",OD)

ID = D - diameter
print("ID",ID)

Na = (g_gpa * pow(diameter,4) * ymax) / (8 * pow(D,3)*fmax)
print("Na",Na)

if type_of_spring_ends == 1:
    Nt = Na +1
    Ls = diameter * Nt
    L_o = Ls + (1+robus_linearity)*ymax
    pitch = L_o/(Na + 1)
    Lcr = 2.63*D/alpha
    fom = (2.6 * pow(math.pi,2) * diameter**2 * Nt * D )/ (4*pow(25.4,3))
if type_of_spring_ends == 2:
    Nt = Na +2
    Ls = diameter *( Nt + 1)
    L_o = Ls + (1+robus_linearity)*ymax
    pitch = (L_o - 3*diameter)/Na
    Lcr = 2.63*D/alpha
    fom = (2.6 * pow(math.pi,2) * diameter**2 * Nt * D )/ (4*pow(25.4,3))
if type_of_spring_ends == 3:
    Nt = Na +2
    Ls = diameter * Nt
    L_o = Ls + (1+robus_linearity)*ymax
    pitch = (L_o - 2*diameter)/Na
    Lcr = 2.63*D/alpha
    fom = (2.6 * pow(math.pi,2) * diameter**2 * Nt * D )/ (4*pow(25.4,3))

print("Nt,Ls,L_o,Lcr,pitch,fom",Nt,Ls,L_o,Lcr,pitch,fom)