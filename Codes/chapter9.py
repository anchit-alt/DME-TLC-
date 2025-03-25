import math
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

