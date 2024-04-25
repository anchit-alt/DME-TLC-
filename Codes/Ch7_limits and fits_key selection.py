import numpy as np
    
def Table7_6():
    # [ Shaft Diameter, Key Size, Keyway Depth]
    # [Over,To (Incl.),   w  , h              ]
    t7_6 = [[5/16, 7/16, 3/32, 3/32, 3/64],
            [7/16, 9/16, 1/8,  3/32, 3/64],
            [7/16, 9/16, 1/8,  1/8,  1/16],
            [9/16, 7/8,  3/16, 1/8,  1/16],
            [9/16, 7/8,  3/16, 3/16, 3/32],
            [7/8,  5/4,  1/4,  3/16, 3/32],
            [5/4,  11/8, 5/16, 1/4,  1/8],
            [5/4,  11/8, 5/16, 5/16, 5/32],
            [11/8, 7/4,  3/8,  1/4,  1/8],
            [11/8, 7/4,  3/8,  3/8,  3/16],
            [7/4,  9/4,  1/2,  3/8,  3/16],
            [7/4,  9/4,  1/2,  1/2,  1/4],
            [9/4,  11/4, 5/8,  7/16, 7/32],
            [9/4,  11/4, 5/8,  5/8,  5/16],
            [11/4, 13/4, 3/4,  1/2, 1/4],
            [11/4, 13/4, 3/4,  3/4, 3/8],]
    return t7_6

def TableA_11():
    # A Selection of International Tolerance Grades—Metric Series
    # [Basic Sizes | Tolerance Grades         ]
    # [            | IT6 IT7 IT8 IT9 IT10 IT11]
    tA_11 = [[0, 3, 0.006, 0.010, 0.014, 0.025, 0.040, 0.060],
             [3, 6, 0.008, 0.012, 0.018, 0.030, 0.048, 0.075],
             [6, 10, 0.009, 0.015, 0.022, 0.036, 0.058, 0.090],
             [10, 18, 0.011, 0.018, 0.027, 0.043, 0.070, 0.110],
             [18, 30, 0.013, 0.021, 0.033, 0.052, 0.084, 0.130],
             [30, 50, 0.016, 0.025, 0.039, 0.062, 0.100, 0.160],
             [50, 80, 0.019, 0.030, 0.046, 0.074, 0.120, 0.190],
             [80, 120, 0.022, 0.035, 0.054, 0.087, 0.140, 0.220],
             [120, 180, 0.025, 0.040, 0.063, 0.100, 0.160, 0.250],
             [180, 250, 0.029, 0.046, 0.072, 0.115, 0.185, 0.290],
             [250, 315, 0.032, 0.052, 0.081, 0.130, 0.210, 0.320],
             [315, 400, 0.036, 0.057, 0.089, 0.140, 0.230, 0.360]]
    return tA_11

def TableA_12():
    # Fundamental Deviations for Shafts—Metric Series
    # [Basic Sizes | Upper Deviation Letter | Lower Deviation Letter]
    # [ x-y        | c d f g h              | k n p s u             ]
    tA_12 = [[0,  3, -0.060, -0.020, -0.006, -0.002, 0,     0, 0.004, 0.006, 0.014, 0.018],
            [3,  6, -0.070, -0.030, -0.010, -0.004, 0, 0.001, 0.008, 0.012, 0.019, 0.023],
            [6, 10, -0.080, -0.040, -0.013, -0.005, 0, 0.001, 0.010, 0.015, 0.023, 0.028],
            [10, 14, -0.095, -0.050, -0.016, -0.006, 0, 0.001, 0.012, 0.018, 0.028, 0.033],
            [14, 18, -0.095, -0.050, -0.016, -0.006, 0, 0.001, 0.012, 0.018, 0.028, 0.033],
            [18, 24, -0.110, -0.065, -0.020, -0.007, 0, 0.002, 0.015, 0.022, 0.035, 0.041],
            [24, 30, -0.110, -0.065, -0.020, -0.007, 0, 0.002, 0.015, 0.022, 0.035, 0.048],
            [30, 40, -0.120, -0.080, -0.025, -0.009, 0, 0.002, 0.017, 0.026, 0.043, 0.060],
            [40, 50, -0.130, -0.080, -0.025, -0.009, 0, 0.002, 0.017, 0.026, 0.043, 0.070],
            [50, 65, -0.140, -0.100, -0.030, -0.010, 0, 0.002, 0.020, 0.032, 0.053, 0.087],
            [65, 80, -0.150, -0.100, -0.030, -0.010, 0, 0.002, 0.020, 0.032, 0.059, 0.102],
            [80, 100, -0.170, -0.120, -0.036, -0.012, 0, 0.003, 0.023, 0.037, 0.071, 0.124],
            [100, 120, -0.180, -0.120, -0.036, -0.012, 0, 0.003, 0.023, 0.037, 0.079, 0.144],
            [120, 140, -0.200, -0.145, -0.043, -0.014, 0, 0.003, 0.027, 0.043, 0.092, 0.170],
            [140, 160, -0.210, -0.145, -0.043, -0.014, 0, 0.003, 0.027, 0.043, 0.100, 0.190],
            [160, 180, -0.230, -0.145, -0.043, -0.014, 0, 0.003, 0.027, 0.043, 0.108, 0.210],
            [180, 200, -0.240, -0.170, -0.050, -0.015, 0, 0.004, 0.031, 0.050, 0.122, 0.236],
            [200, 225, -0.260, -0.170, -0.050, -0.015, 0, 0.004, 0.031, 0.050, 0.130, 0.258],
            [225, 250, -0.280, -0.170, -0.050, -0.015, 0, 0.004, 0.031, 0.050, 0.140, 0.284],
            [250, 280, -0.300, -0.190, -0.056, -0.017, 0, 0.004, 0.034, 0.056, 0.158, 0.315],
            [280, 315, -0.330, -0.190, -0.056, -0.017, 0, 0.004, 0.034, 0.056, 0.170, 0.350],
            [315, 355, -0.360, -0.210, -0.062, -0.018, 0, 0.004, 0.037, 0.062, 0.190, 0.390],
            [355, 400, -0.400, -0.210, -0.062, -0.018, 0, 0.004, 0.037, 0.062, 0.208, 0.435]]
    return tA_12

def Table7_8():
    # [Keyseat Width, in | Shaft Diameter, in  ]
    # [                  | From  To (Inclusive)]
    t7_8 = [[1/16, 5/16, 1/2],
            [3/32, 3/8, 7/8],
            [1/8, 3/8, 3/2],
            [5/32, 1/2, 13/8],
            [3/16, 9/16, 2],
            [1/4, 11/16, 9/4],
            [5/16, 3/4, 19/8],
            [3/8, 1, 21/8]]
    return t7_8

def Table7_9():
    t7_9 = [['loose running fit','H','11','c','11'],
            ['free running fit', 'H','9','d','9'],
            ['close running fit', 'H','8','f','7'],
            ['sliding fit', 'H','7','g','6'],
            ['locational clearnce fit', 'H','7','h','6'],
            ['locational transition fit', 'H','7','k','6'],
            ['locational interference fit', 'H','7','p','6'],
            ['medium drive fit','H','7','s','6'],
            ['force fit','H','7','u','6']]
    return t7_9

def TableA_13():
    # A Selection of International Tolerance Grades—Inch Series
    # [Basic Sizes | Tolerance Grades]
    # [ x- y | IT6 IT7 IT8 IT9 IT10 IT11]
    tA_13 = [[0.00, 0.12, 0.0002, 0.0004, 0.0006, 0.0010, 0.0016, 0.0024],
             [0.12, 0.24, 0.0003, 0.0005, 0.0007, 0.0012, 0.0019, 0.0030],
             [0.24, 0.40, 0.0004, 0.0006, 0.0009, 0.0014, 0.0023, 0.0035],
             [0.40, 0.72, 0.0004, 0.0007, 0.0011, 0.0017, 0.0028, 0.0043],
             [0.72, 1.20, 0.0005, 0.0008, 0.0013, 0.0020, 0.0033, 0.0051],
             [1.20, 2.00, 0.0006, 0.0010, 0.0015, 0.0024, 0.0039, 0.0063],
             [2.00, 3.20, 0.0007, 0.0012, 0.0018, 0.0029, 0.0047, 0.0075],
             [3.20, 4.80, 0.0009, 0.0014, 0.0021, 0.0034, 0.0055, 0.0087],
             [4.80, 7.20, 0.0010, 0.0016, 0.0025, 0.0039, 0.0063, 0.0098],
             [7.20, 10.00, 0.0011, 0.0018, 0.0028, 0.0045, 0.0073, 0.0114],
             [10.00, 12.60, 0.0013, 0.0020, 0.0032, 0.0051, 0.0083, 0.0126],
             [12.60, 16.00, 0.0014, 0.0022, 0.0035, 0.0055, 0.0091, 0.0142]]
    return tA_13

def TableA_14():
    # Fundamental Deviation for Shafts - Inch Series
    tA_14 = []
    return tA_14

def keyselection():
    P = float(input("Enter the value of power transmitted through the shaft (hp) :"))
    N = float(input("Enter the rotation speed of the shaft (RPM) :"))
    d  = float(input("Enter the diameter of the shaft (inches) :"))
    Sy = float(input("Enter the value of yield strength of shaft material (kpsi) :"))
    n = float(input("Enter the value of design factor :"))
    
    T = (63025*P)/N # torque in lbf/in
    F = T/(d/2) # force at the end of the shaft in lbf
    S_sy = 0.577*Sy # shear strength by distortion energy theory
    
    t = 0
    t7_6 = Table7_6()
    #compare d to be between cloumn 1 and column 2 values and pick value where third and fourth column are the same and return the value
    for row in t7_6:
        if row[0] <= d <= row[1]:
            if row[2] == row[3]:
                t = row[2]  # This is the key size corresponding to the shaft diameter
                break
            
    l = (F*n)/(t*S_sy*1000) # length of key required
    l_c = (F*n*2)/(t*Sy*1000) # length of key required to prevent crushing
    if l_c>l:
        l = l_c
    
    print("Required key length (in) :", round(l,2))
    print("Required key depth (in) :", t)

def limitsandfits():
    letter = 0
    letter2 = 0
    letter3 = 0
    
    D = float(input("Enter basic size (mm) :"))
    d = D
    fit = input("Enter the desired fit according to Table 7_9 :").lower()
    
    t7_9 = Table7_9()
    for row in t7_9:
        if row[0] == fit:
            tol_grade = row[1]+row[2]+'/'+row[3]+row[4]
            print('Tolerance Grade chosen:',tol_grade)
            sizeA_12 = row[4]
            letterA_12 = row[3]
            sizeA_11 = row[2]
            letterA_11 = row[1]
            print(sizeA_12)
            print(letterA_12)
            print(sizeA_11)
            print(letterA_11)
            break
    
    # devF : fundamental deviation from Table A-12
    tol_grade_dict = {'c': 2, 'd': 3, 'f': 4, 'g': 5, 'h': 6, 'k': 7, 'n': 8, 'p': 9, 's': 10, 'u': 11}
    if letterA_12 in tol_grade_dict:
        # if it does, store the corresponding numerical value in the variable 'letter'
        letter = tol_grade_dict[letterA_12]
    else:
        print("The character {} is not in the dictionary.".format(letterA_12))
    
    tA_12 = TableA_12()
    for row in tA_12:
        if row[0] <= D <= row[1]:
            devF = row[letter] 
            print('devF = ', devF)
            break
        
    #deld : tolerance grade for shaft from Table A-11
    tol_grade_dict2 = {'6':2,'7':3,'8':4,'9':5,'10':6,'11':7}
    if sizeA_11 in tol_grade_dict2:
        # if it does, store the corresponding numerical value in the variable 'letter'
        letter2 = tol_grade_dict2[sizeA_11]
        
    for row in TableA_11():
        if row[0] <= d <= row[1]:
            deld = row[letter2] 
            print('deld = ',deld)
            break   
        
    #delD : tolerance grade for hole from Table A-11
    tol_grade_dict2 = {'6':2,'7':3,'8':4,'9':5,'10':6,'11':7}
    if sizeA_11 in tol_grade_dict2:
        # if it does, store the corresponding numerical value in the variable 'letter'
        letter3 = tol_grade_dict2[sizeA_11]
        
    for row in TableA_11():
        if row[0] <= D <= row[1]:
            delD = row[letter3] 
            print('delD = ',delD)
            break   
    
    Dmax = D + delD
    Dmin = D 
    
    if fit == "loose running fit" or "free running fit" or "close running fit" or "sliding fit" or "locational clearance fit":
        dmax = d + devF
        dmin = d + devF - deld
    else:
        dmin = d + devF
        dmax = d + devF + deld
        
    print('Dmax (mm) :', round(Dmax, 3))
    print('Dmin (mm) :', round(Dmin, 3))
    print('dmax (mm) :', round(dmax, 3))
    print('dmin (mm) :', round(dmin, 3))


# implementation
# keyselection()
limitsandfits()
