import numpy as np

class Data_bearing:
    Fa = 0
    Fr = 0
    Fi = 0
    Fe = 0

    V = 1
    C10 = 0
    C0 = 0
    Bore = 40
    C10_actual = 0
    e = 0
    e_data = 0
    selection = 0

    X = 1
    Y = 0
    K = 1.5      

    L = 30       # Life kh
    n = 300       # rpm
    LR = 10**6   # Rated Life
    xD = 0
    R = 0.9
    af = 1

    a = 3
    x0 = 0.02
    theta = 4.459
    b = 1.483

    number = 0
    Cup = 'NA'
    Cone = 'NA'



def SingleRow_02_DeepGroove_AngularContact(bearing = Data_bearing()):
    ## Table 11-2 (Change: dH, Angular Contact C0 C10)
    Dim_Load_Ratings = np.array(   [[10, 30, 9, 0.6, 12.5, 27, 5.07, 2.24, 4.94, 2.12],
                                    [12, 32, 10, 0.6, 14.5, 28, 6.89, 3.10, 4.94, 2.12],
                                    [15, 35, 11, 0.6, 17.5, 31, 7.80, 3.55, 4.94, 2.12],
                                    [17, 40, 12, 0.6, 19.5, 27, 9.56, 4.50, 4.94, 2.12],
                                    [20, 47, 14, 1.0, 25, 27, 12.7, 6.20, 4.94, 2.12],
                                    [25, 52, 15, 1.0, 30, 27, 14.0, 6.95, 4.94, 2.12],
                                    [30, 62, 16, 1.0, 35, 27, 19.5, 10.0, 4.94, 2.12],
                                    [35, 72, 17, 1.0, 41, 27, 25.5, 13.7, 4.94, 2.12],
                                    [40, 80, 18, 1.0, 46, 27, 30.7, 16.6, 4.94, 2.12],
                                    [45, 85, 19, 1.0, 52, 27, 33.2, 18.6, 4.94, 2.12],
                                    [50, 90, 20, 1.0, 56, 27, 35.1, 19.6, 4.94, 2.12],
                                    [55, 100, 21, 1.5, 63, 27, 43.6, 25.0, 4.94, 2.12],
                                    [60, 110, 22, 1.5, 70, 27, 47.5, 28.0, 4.94, 2.12],
                                    [65, 120, 23, 1.5, 74, 27, 55.9, 34.0, 4.94, 2.12],
                                    [70, 125, 24, 1.5, 79, 27, 61.8, 37.5, 4.94, 2.12],
                                    [75, 130, 25, 1.5, 86, 27, 66.3, 40.5, 4.94, 2.12],
                                    [80, 140, 26, 2.0, 93, 27, 70.2, 45.0, 4.94, 2.12],
                                    [85, 150, 28, 2.0, 99, 27, 83.2, 53.0, 4.94, 2.12],
                                    [90, 160, 30, 2.0, 104, 27, 95.6, 62.0, 4.94, 2.12],
                                    [95, 170, 32, 2.0, 110, 27, 108, 69.5, 4.94, 2.12]] )

    if bearing.selection == 0:
        for i in range(0,len(Dim_Load_Ratings[:,0])):
            if bearing.Bore == Dim_Load_Ratings[i,0]:
                bearing.C10 = Dim_Load_Ratings[i,6]
                bearing.C0 = Dim_Load_Ratings[i,7]
                print("Data found for: ", bearing.Bore, "mm")
                break
    
    elif bearing.selection == 1 and (bearing.C10_actual>bearing.C10):
        for i in range(0,len(Dim_Load_Ratings[:,0])):
            if bearing.C10_actual < Dim_Load_Ratings[i,6]:
                bearing.Bore = Dim_Load_Ratings[i,0]
                bearing.C10 = Dim_Load_Ratings[i,6]
                bearing.C0 = Dim_Load_Ratings[i,7]
                print("New Bearing chosen: ", bearing.Bore, "mm")
                break
    elif bearing.selection == 1 and (bearing.C10_actual <= bearing.C10):
        bearing.selection = 0

    return bearing

def SingleRow_02_StraightRow_TimkenRoller(bearing = Data_bearing()):
    ## Table 11-15 
                                    # 'd',     'N-r',   'K',    'cone',  'cup'
    Dim_Load_Ratings = np.array(   [['25.000', '8190', '1.56', '30205', '30205'], 
                                    ['25.159', '6990', '1.45', '07096', '07196'], 
                                    ['25.400', '6990', '1.45', '07100', '07196'], 
                                    ['25.400', '6990', '1.45', '07100-S', '07196'], 
                                    ['25.400', '6990', '1.45', '07100', '07204'], 
                                    ['25.400', '7210', '1.56', 'L44642', 'L44610'], 
                                    ['25.400', '7210', '1.56', 'L44643', 'L44610'], 
                                    ['26.988', '7210', '-3.3', 'L44649', 'L44610'], 
                                    ['25.000', '9520', '1', '32205-B', '32205-B'], 
                                    ['25.400', '10900', '1.9', '1780', '1719'], 
                                    ['25.400', '11000', '1.69', '15578', '15523'], 
                                    ['26.988', '11000', '1.69', '15580', '15523'], 
                                    ['28.575', '11000', '1.69', '15590', '15520'], 
                                    ['28.575', '11000', '1.69', '15590', '15523'], 
                                    ['25.400', '11600', '1.77', '1986', '1932'], 
                                    ['26.975', '11600', '1.77', '1987', '1932'], 
                                    ['28.575', '11600', '1.77', '1985', '1930'], 
                                    ['28.575', '11600', '1.77', '1985', '1932'], 
                                    ['28.575', '11600', '1.77', '1988', '1932'], 
                                    ['28.575', '11600', '1.77', '1985', '1931'], 
                                    ['25.400', '11700', '1.07', 'M184548', 'M84510'], 
                                    ['25.400', '12100', '1.67', '15101', '15243'], 
                                    ['25.400', '12100', '1.67', '15100', '15245'], 
                                    ['25.400', '12100', '1.67', '15101', '15245'], 
                                    ['25.400', '12100', '1.67', '15102', '15245'], 
                                    ['25.400', '12100', '1.67', '15101', '15244'], 
                                    ['25.400', '12100', '1.67', '15101', '15250'], 
                                    ['25.400', '12100', '1.67', '15101', '15250X'], 
                                    ['26.157', '12100', '1.67', '15103', '15245'], 
                                    ['26.988', '12100', '1.67', '15106', '15245'], 
                                    ['25.000', '13000', '1.95', '30305', '30305'], 
                                    ['25.400', '13100', '0.8', '23100', '23256'], 
                                    ['25.000', '13200', '1.66', '33205', '33205'], 
                                    ['25.400', '13900', '1.07', 'M84249', 'M84210'], 
                                    ['25.400', '14500', '1.07', 'M86643', 'M86610'], 
                                    ['25.400', '15300', 'Jan 00', '02473', '02420'], 
                                    ['25.000', '17400', '1.95', '32305', '32305'], 
                                    ['25.400', '18400', '2.3', '02687', '02631'], 
                                    ['25.400', '18400', '1.07', 'HM88630', 'HM88610'], 
                                    ['26.162', '18400', '2.3', '2682', '2630'], 
                                    ['26.162', '18400', '2.3', '2682', '2631'], 
                                    ['26.988', '18400', '2.3', '2688', '2631'], 
                                    ['25.400', '22700', '1.76', '3189', '3120']] )
    if bearing.selection == 0:
        bearing.Bore = float(Dim_Load_Ratings[bearing.number,0])
        bearing.C10 = float(Dim_Load_Ratings[bearing.number,1])/1000
        bearing.K = float(Dim_Load_Ratings[bearing.number,2])
        bearing.Cone = Dim_Load_Ratings[bearing.number,3]
        bearing.Cup = Dim_Load_Ratings[bearing.number,4]

    elif bearing.selection == 1 and (bearing.C10_actual>bearing.C10):
        for i in range(0,len(Dim_Load_Ratings[:,0])):
            if bearing.C10_actual < float(Dim_Load_Ratings[i,1])/1000:
                print("New Bearing Options")
                print()
                for j in range(i,len(Dim_Load_Ratings[:,0])):
                    if Dim_Load_Ratings[i,1] == Dim_Load_Ratings[j,1]:
                        print("Bearing:", j)
                        print("Bore: ", Dim_Load_Ratings[j,0])
                        print("Radial Rating: ", Dim_Load_Ratings[j,1])
                        print("K: ", Dim_Load_Ratings[j,2])
                        print("Cone: ", Dim_Load_Ratings[j,3])
                        print("Cup: ", Dim_Load_Ratings[j,4])
                        print()
                
                bearing.number = int(input("Select bearing number: "))
                bearing.selection = 0
                bearing = SingleRow_02_StraightRow_TimkenRoller(bearing) 
                bearing.selection = 1
                break
    elif bearing.selection == 1 and (bearing.C10_actual <= bearing.C10):
        bearing.selection = 0

    return bearing


def effectiveLoad(bearing = Data_bearing()):
    ## Table 11-1
    RadLoadFactor = np.array(  [[0.014, 0.19, 1.0, 0, 0.56, 2.30],
                                [0.021, 0.21, 1.0, 0, 0.56, 2.15],
                                [0.028, 0.22, 1.0, 0, 0.56, 1.99],
                                [0.042, 0.24, 1.0, 0, 0.56, 1.85],
                                [0.056, 0.26, 1.0, 0, 0.56, 1.71],
                                [0.070, 0.27, 1.0, 0, 0.56, 1.63],
                                [0.084, 0.28, 1.0, 0, 0.56, 1.55],
                                [0.110, 0.30, 1.0, 0, 0.56, 1.45],
                                [0.170, 0.34, 1.0, 0, 0.56, 1.31],
                                [0.280, 0.38, 1.0, 0, 0.56, 1.15],
                                [0.420, 0.42, 1.0, 0, 0.56, 1.04],
                                [0.560, 0.44, 1.0, 0, 0.56, 1.00]])
    
    i = 0
    Fa_C0 = bearing.Fa/bearing.C0
    for i in range(0,len(RadLoadFactor[:,0])):
        if Fa_C0 < RadLoadFactor[i,0]:
            interpolate_factor = (Fa_C0-RadLoadFactor[i-1,0])/(RadLoadFactor[i,0]-RadLoadFactor[i-1,0])
            bearing.e_data = RadLoadFactor[i-1,1] + interpolate_factor*(RadLoadFactor[i,1]-RadLoadFactor[i-1,1])

            break
    
    bearing.e = bearing.Fa/bearing.V/bearing.Fr
    if bearing.e > bearing.e_data:
        bearing.X = RadLoadFactor[i-1,4] + interpolate_factor*(RadLoadFactor[i,4]-RadLoadFactor[i-1,4])
        bearing.Y = RadLoadFactor[i-1,5] + interpolate_factor*(RadLoadFactor[i,5]-RadLoadFactor[i-1,5])

    bearing.Fe = bearing.X*bearing.V*bearing.Fr + bearing.Y*bearing.Fa
    return bearing

def DesignLife(bearing = Data_bearing()):
    bearing.xD = bearing.L*1000*bearing.n*60/bearing.LR
    return bearing

def C10_calculate(bearing = Data_bearing()):
    bearing.C10_actual = bearing.af*bearing.Fe*(bearing.xD/(bearing.x0+(bearing.theta-bearing.x0)*(np.log(1/bearing.R))**(1/bearing.b)))**(1/bearing.a)
    return bearing

def LoadBased(bearing = Data_bearing()):

    # Getting Data for that bore
    print("Guess: ", bearing.Bore, "mm")
    bearing.selection = 0
    bearing = SingleRow_02_DeepGroove_AngularContact(bearing)  

    # Effective Load
    bearing = effectiveLoad(bearing)
    print("Effective Load: ", bearing.Fe, "kN")

    # Design Life
    bearing = DesignLife(bearing)
    print("xD: ", bearing.xD, "")

    # Calculate C10
    bearing = C10_calculate(bearing)
    print("C10 Actual: ", bearing.C10_actual, "kN")
    print("C10 Rated: ", bearing.C10, "kN")
    

    # Checking C10
    bearing.selection = 1
    bearing = SingleRow_02_DeepGroove_AngularContact(bearing) 

    if bearing.selection == 1:
        print("Iterating...")
        LoadBased(bearing)

    return bearing

def LoadBased_Taper(bearingA = Data_bearing(), bearingB = Data_bearing()):

    # Induced Loads
    bearingA.Fi = 0.47*bearingA.Fr/bearingA.K
    bearingB.Fi = 0.47*bearingB.Fr/bearingB.K

    # Effective Loads
    if bearingA.Fi <= (bearingB.Fi + bearingA.Fa):
        if bearingA.Fr < 0.4*bearingA.Fr + bearingA.K*(bearingB.Fi + bearingA.Fa):
            bearingA.Fe = 0.4*bearingA.Fr + bearingA.K*(bearingB.Fi + bearingA.Fa)
        else:
            bearingA.Fe = bearingA.Fr
        bearingB.Fe = bearingB.Fr
    else:
        if bearingB.Fr < 0.4*bearingB.Fr + bearingB.K*(bearingA.Fi - bearingA.Fa):
            bearingB.Fe = 0.4*bearingB.Fr + bearingB.K*(bearingA.Fi - bearingA.Fa)
        else:
            bearingB.Fe = bearingB.Fr
        bearingA.Fe = bearingA.Fr

    # Design Life
    bearingA = DesignLife(bearingA)
    print("A-xD: ", bearingA.xD, "")

    bearingB = DesignLife(bearingB)
    print("B-xD: ", bearingB.xD, "")
    print()

    # Calculate C10
    bearingA = C10_calculate(bearingA)
    bearingB = C10_calculate(bearingB)

    print("A-C10 Actual: ", bearingA.C10_actual, "kN")
    print("A-C10 Rated: ", bearingA.C10, "kN")
    print("B-C10 Actual: ", bearingB.C10_actual, "kN")
    print("B-C10 Rated: ", bearingB.C10, "kN")
    print()

    # Checking C10
    bearingA.selection = 1
    bearingB.selection = 1
    print("Bearing A")
    bearingA = SingleRow_02_StraightRow_TimkenRoller(bearingA) 

    print()
    print("Bearing B")
    bearingB = SingleRow_02_StraightRow_TimkenRoller(bearingB) 

    if bearingA.selection == 1 and bearingB.selection == 1:
        print()
        print()
        print("##### Iterating... #####")
        LoadBased_Taper(BearingA,BearingB)

    else:
        print()
        print("##### Final Values #####")
        print()
        print("Bearing A")
        print("Bore: ", bearingA.Bore)
        print("Radial Rating: ", bearingA.C10)
        print("K: ", bearingA.K)
        print("Cone: ", bearingA.Cone)
        print("Cup: ", bearingA.Cup)
        print()
        print("Bearing B")
        print("Bore: ", bearingA.Bore)
        print("Radial Rating: ", bearingA.C10)
        print("K: ", bearingA.K)
        print("Cone: ", bearingA.Cone)
        print("Cup: ", bearingA.Cup)




###### Deep Groove ########
# Bearing1 = Data_bearing()

# Bearing1.Fr = 1.792 # kN    Radial Load
# Bearing1.Fa = 0     # kN    Axial Load
# Bearing1.Bore = 25  # mm    Initial Guess
# Bearing1.V = 1.2    #       Rotation Factor
# Bearing1.R = 0.96   #       Reliability
# Bearing1.L = 30     # kh    Life
# Bearing1.n = 300    # rev/min RPM

# # Values for deep groove
# Bearing1.a = 3
# Bearing1.x0 = 0.02
# Bearing1.theta = 4.459
# Bearing1.b = 1.483
# Bearing1.LR = 10**6

# Bearing1 = LoadBased(Bearing1)


####### Rolling Contact ########
BearingA = Data_bearing()
BearingB = Data_bearing()

# Bearing A - Squezed bearing guess, based on axial load
BearingA.Fr = 2.17  #kN
BearingA.Fa = 1.69  #kN
BearingA.R = 0.995
BearingA.L = 5    # kh
BearingA.n = 800    # rev/min

BearingB.Fr = 2.654 #kN
BearingA.R = 0.995
BearingA.L = 5     # kh
BearingA.n = 800    # rev/min

# Taper roller values
BearingA.a = 10/3
BearingA.x0 = 0
BearingA.theta = 4.48
BearingA.b = 1.5
BearingA.LR = 90*10**6
BearingA.V = 1

BearingB.a = 10/3
BearingB.x0 = 0
BearingB.theta = 4.48
BearingB.b = 1.5
BearingB.LR = 90*10**6

LoadBased_Taper(BearingA,BearingB)



