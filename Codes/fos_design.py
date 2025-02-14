import math
rod_length = float(input("Enter rod length (m)"))
load = float(input("Enter load (KN)"))
N = float(input("number of cycles "))
design_factor = float(input("Design Factor"))
Sut = float(input("Enter Sut "))
Sy = float(input("Enter Sy "))

B = 0 ## meters

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
print("ka",ka)
assumdkb = float(input("Enter assumed kb "))

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

kd = 1

reliability = float(input("Enter reliability value if specified, 0 otherwise: "))
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
c = B/2
# sigma_max = (6 * Mmax) / pow(B,3)  ## pascals

B = pow(((6*Mmax*design_factor)/(Sf * pow(10,6))),0.33333)

B = B * 1000
print("B",B)
d_e = 0.808 * B 

print("d_e",d_e)
if 2.79 <= d_e and d_e <= 51 and loadoption != '3':
    kb = 1.24 * pow(d_e, -0.107)
    print("kb",kb)
elif 51 <= d_e and d_e <=254:
    kb = 1.51 * pow(d_e, -0.157)
    print("kb",kb)
