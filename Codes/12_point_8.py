import pandas as pd 
import cv2
import math
from PIL import Image
table_12_13 = pd.read_csv("/Users/anchit/Documents/GitHub/DME-TLC-/Data/viscosity_data.csv")

def mue_if_temp():
    for i in range(1,len(table_12_13['Temperature (°C)'])):
        if table_12_13['Temperature (°C)'][i] == temp:
            if lub == 1:
                mue = table_12_13['SAE 10'][i]
                break
            if lub == 2:
                mue = table_12_13['SAE 20'][i]
                break
            if lub == 3:
                mue = table_12_13['SAE 30'][i]
                break
            if lub == 4:
                mue = table_12_13['SAE 40'][i]
                break
            if lub == 5:
                mue = table_12_13['SAE 50'][i]
                break
            if lub == 6:
                mue = table_12_13['SAE 60'][i]
                break
            if lub == 7:
                mue = table_12_13['SAE 70'][i]
                break
    return mue

def mue_ifnot_temp():
    for i in range(1,len(table_12_13['Temperature (°C)'])):
        if table_12_13['Temperature (°C)'][i] > temp:
            print("hi ",table_12_13['Temperature (°C)'][i])
            c = table_12_13['Temperature (°C)'][i]
            a = table_12_13['Temperature (°C)'][i-2]
            b = table_12_13['Temperature (°C)'][i-1]
            if lub == 1:
                d = table_12_13['SAE 10'][i]
                e = table_12_13['SAE 10'][i-2]
                mue = (((e-d)*(b-c))/(a-c)) + d
                break
            if lub == 2:
                d = table_12_13['SAE 20'][i]
                e = table_12_13['SAE 20'][i-2]
                mue = (((e-d)*(b-c))/(a-c)) + d
                break
            if lub == 3:
                d = table_12_13['SAE 30'][i]
                e = table_12_13['SAE 30'][i-2]
                mue = (((e-d)*(b-c))/(a-c)) + d
                break
            if lub == 4:
                d = table_12_13['SAE 40'][i]
                e = table_12_13['SAE 40'][i-2]
                mue = (((e-d)*(b-c))/(a-c)) + d
                break
            if lub == 5:
                d = table_12_13['SAE 50'][i]
                e = table_12_13['SAE 50'][i-2]
                mue = (((e-d)*(b-c))/(a-c)) + d
                break
            if lub == 6:
                d = table_12_13['SAE 60'][i]
                e = table_12_13['SAE 60'][i-2]
                mue = (((e-d)*(b-c))/(a-c)) + d
                break
            if lub == 7:
                d = table_12_13['SAE 70'][i]
                e = table_12_13['SAE 70'][i-2]
                mue = (((e-d)*(b-c))/(a-c)) + d
                break
    return mue

d = float(input("Enter the value of d "))
b = float(input("Enter bushing bore diameter "))
cmin = (b-d)/2
print("cmin ",cmin)

l = int(input("Enter the value of bushing length "))
W = int(input("Enter the value of load "))
N = int(input("Enter the value of Speed "))
print("N in rev/sec", N/60)

l_by_d = l/d
r = d/2
r_by_c = r/cmin

P = W/(l*d)

print("P in MPa ", P)

lub = int(input("1. SAE 10, 2. SAE 20, 3. SAE 30, 4. SAE 40, 5. SAE 50, 6. SAE 60, 7. SAE 70 "))
temp = float(input("Enter the value of temp in degree celcuis "))

given_temp = [10,20,30,40,50,60,70,80,90,100,110,120,130,140]

if temp in given_temp:
    mue = mue_if_temp()
if temp not in given_temp:
    mue = mue_ifnot_temp()
    





print("mue ", mue)




S = (((r_by_c)**2) *  (mue*pow(10,-3)) *  ((N)/ (pow(10,6) *P)) ) * pow(10,-2)
print("Sommerfield Number ", S)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg



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

# img_12_18 = Image.open(r"/Users/anchit/Documents/GitHub/DME-TLC-/Images/12_18.png")
# img_12_18.show()


# rfbyc = float(input("Enter the value of r * f / c "))
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

# img_12_21 = Image.open(r"/Users/anchit/Documents/GitHub/DME-TLC-/Images/12_21.png")
# img_12_21.show()

# p_by_pmax = float(input("Enter the value of p / pmax "))
pmax = P / p_by_pmax

print("pmax " , pmax)

T = f * W * r * pow ( 10, -3)
H_loss = 2 * math.pi * T * N * pow ( 10, -3)



print("Torque ", T)
print("H_loss ",H_loss)



# # Load an image
# img_12_16 = Image.open(r"/Users/anchit/Documents/GitHub/DME-TLC-/Images/12_16.png")
# img_12_16.show()

# hnot_by_c = float(input("Enter the value of ho / c "))