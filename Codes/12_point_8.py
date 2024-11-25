import pandas as pd 
import cv2

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
cmin = (d - b)/2
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




S = (((r_by_c)**2)*(mue*N/P))
print("Sommerfield Number ", S)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# Load an image
img_12_16 = mpimg.imread('/Users/anchit/Documents/GitHub/DME-TLC-/Images/12_16.png')


# Display the image
imgplot_12_16 = plt.imshow(img_12_16)
plt.show()

hnot_by_c = float(input("Enter the value of ho / c "))




