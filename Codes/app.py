from bs4 import BeautifulSoup
import lxml
import math
from sympy import *
from sympy import symbols, solve
import time 
from flask import Flask , render_template , request
import pandas as pd 
app = Flask(__name__)

def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        function()
        function()
    return wrapper_function


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ball_bearing.html",methods = ["POST","GET"])
def ball():
    if request.method == "POST":
        ###bearing type
        ball = request.form.get('ball')
        print(ball)
        taper = request.form.get('taper')
        cylindrical = request.form.get('cylindrical')
        if ball == "Ball":
            print("Ball bearing selected")
            a = 3
            b = 1.483
            X_0 = 0.02
            theta = 4.459
            LR = pow(10, 6)
        elif taper == "Taper":
            print("Tapered Roller Bearing selected")
            a = 10 / 3
            b = 1.5
            X_0 = 0.0
            theta = 4.48
            LR = 90 * pow(10, 6)
        elif cylindrical == "Cylindrical":
            print("Cylinder Roller Bearing selected")
            a = 10 / 3
            b = 1.483
            X_0 = 0.02
            theta = 4.459
            LR = pow(10, 6)
        inner_ring = request.form.get('jweb')
        if inner_ring == "Inner":
            V =1
        # outer_ring = request.form.get('sweb')
        # elif outer_ring == "Outer":
        #     V = 1.2
        

        af = request.form.get('af')
        Fa = request.form.get("Axial_load")
        Fr = request.form.get("Radial_load")
        ld = float(request.form.get("desired_life"))
        nd = float(request.form.get("desired_speed"))
        def calculate_LD(ld, nd):
            return 60 * ld * nd
        def calculate_XD(LD, LR):
            return float(LD / LR)
        def calculate_Fe(V, Fr, Fa, X, Y):
            return float((X * V * Fr) + (Y * Fa))
        LD = calculate_LD(ld, nd)
        R = request.form.get("desired_reliability")
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
                            return True  # Exit the loop
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
        return iteration(X,Y)
    else:
        return render_template("ball_bearing.html")


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