import math
import pandas as pd
b = float(input("b (mm)"))
c = float(input("c (mm)"))
d = float(input("d (mm)"))
h = float(input("h (mm)"))
tau_allow = float(input("Tau (MPa)"))

F = None

A = 1.414 * h * d
print("A ",A)
J_u = d * (3 * pow(b,2) + pow(d,2)) / 6
J = 0.707 * h * J_u
print("J ",J)

m = (((c+ (b/2) ) * (b/2) * pow(10,3))/ J)
n = ( (pow(10,3)/A) + ((c +(d/2)) * (d/2) * (pow(10,3)))/ J )
x = math.sqrt(pow(m,2) + pow(n,2))
F = tau_allow / x 

print(" x ",x)
print("F ", F)

EXX = input("Enter electrode number EXX : ")


def get_weld_strength(aws_number):
    file_path = "Data/Weld_Metal_Properties.csv" 
    df = pd.read_csv(file_path)
    
    row = df[df["AWS Electrode Number"].str.strip() == aws_number.strip()]
    
    if not row.empty:
        tensile_strength = row.iloc[0]["Tensile Strength kpsi (MPa)"]
        yield_strength = row.iloc[0]["Yield Strength kpsi (MPa)"]
        return tensile_strength, yield_strength
    else:
        return None, None


Sut_electrode, Sy_electrode = get_weld_strength(EXX)

if Sut_electrode and Sy_electrode:
    print(f"Sut_electrode: {Sut_electrode}, Sy_electrode: {Sy_electrode}")
else:
    print("AWS Electrode Number not found.")


AISI_BAR = (input("Enter Bar material AISI No. "))
AISI_MAT = input("Enter support material AISI No. ")

def get_aisi_strength(aisi_number, processing_type):
    
    file_path = "Data/ASTM_Steel_Properties.csv" 
    df = pd.read_csv(file_path)
    
    # Search for the AISI number and processing type
    row = df[(df["SAE and/or AISI No."].astype(str).str.strip() == str(aisi_number).strip()) &
             (df["Processing"].str.strip().str.upper() == processing_type.strip().upper())]
    
    if not row.empty:
        tensile_strength = row.iloc[0]["Tensile Strength (MPa) (kpsi)"].split(" (")[0]  # Extract MPa value
        yield_strength = row.iloc[0]["Yield Strength (MPa) (kpsi)"].split(" (")[0]  # Extract MPa value
        return int(tensile_strength), int(yield_strength)
    else:
        return None, None

processing_type_bar = input("Enter Processing Type for BAR (HR or CD): ")
processing_type_mat = input("Enter Processing Type for material (HR or CD): ")

tensile_strength_bar, yield_strength_bar = get_aisi_strength(AISI_BAR, processing_type_bar)
print("tensile_strength_bar,yield_strength_bar ",tensile_strength_bar,yield_strength_bar)

tensile_strength_mat, yield_strength_mat = get_aisi_strength(AISI_MAT, processing_type_mat)
print("tensile_strength_mat,yield_strength_mat ",tensile_strength_mat,yield_strength_mat)


new_t_allow = min(0.30*tensile_strength_mat,0.40*yield_strength_mat)

F_new = new_t_allow / x

print("new_t_allow ",new_t_allow)

print("F new " , F_new)