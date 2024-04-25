import numpy as np

# function to determine failure theory to be employed0
def select_failure_theory():
    fos = 0
    eps_f = float(input("Enter the strain value: "))

    if eps_f < 0.05:
        conserv = input("Is it conservative? ").lower()
        if conserv == 'yes':
            return "Brittle Coulomb-Mohr Theory"
        else:
            return "Modified Mohr Theory"
    elif eps_f >= 0.05:
        # input material from the user and determine Sut and Syt from A-20 A-21
        Syt = float(input("Enter the value of Ultimate tensile strength of the material (Syt in MPa): "))
        Syc = float(input("Enter the value of Ultimate compressive strength of the material (Syc in MPa): "))
        if Syt != Syc:
            return "Ductile Coulomb-Mohr Theory"
        else:
            conserv = input("Is it conservative? ").lower()
            if conserv == 'yes':
                return "Maximum Shear Stress Theory"
            else:
                return "Distortion-Energy Theory"
    else:
        return "Incorrect Input"

# function to calculate stress tensor
def input_stress():
    stress_tensor = np.zeros((3, 3))

    print("Enter the components of the stress tensor in the given format:")
    print(f"[ σxx, τxy, τxz ]")
    print(f"[ τyx, σyy, τyz ]")
    print(f"[ τzx, τzy, σzz ]")
    for i in range(3):
        for j in range(3):
            stress_tensor[i, j] = float(input(f"σ_{i+1}{j+1}: "))

    return stress_tensor

# function to calculate principal stresses
def principal_stresses(stress_tensor):
    # Calculate principal stresses
    eigenvalues, _ = np.linalg.eig(stress_tensor)

    # Sort the eigenvalues in descending order
    sorted_eigenvalues = np.sort(eigenvalues)[::-1]

    return sorted_eigenvalues

def MaxShear(principal_stresses_array, Sy):
    Tmax = (principal_stresses_array[0] - principal_stresses_array[2]) / 2
    fos = Sy / (2 * Tmax)
    return fos

def DistEnergy(principal_stresses_array, Sy):
    sigma = np.sqrt(np.power(principal_stresses_array[0], 2) - principal_stresses_array[0] * principal_stresses_array[1] + np.power(principal_stresses_array[1], 2))
    fos = Sy / sigma
    return fos

def CoulombMohr(principal_stresses_array, St, Sc):
    fos = 1 / ((principal_stresses_array[0] / St) - (principal_stresses_array[2] / Sc))
    return fos

def ModMohr(principal_stresses_array, Sut, Suc):
    if principal_stresses_array[1] >= principal_stresses_array[2] and principal_stresses_array[2] >= 0:
        fos = Sut / principal_stresses_array[1]
    elif principal_stresses_array[1] >= 0 and 0 >= principal_stresses_array[2] and abs(principal_stresses_array[2] / principal_stresses_array[1]) <= 1:
        fos = Sut / principal_stresses_array[1]
    elif principal_stresses_array[1] >= 0 and 0 >= principal_stresses_array[2] and abs(principal_stresses_array[2] / principal_stresses_array[1]) > 1:
        fos = (Suc - Sut) * principal_stresses_array[1] / (Suc * Sut) - principal_stresses_array[2] / Suc
        fos = 1 / fos
    elif 0 >= principal_stresses_array[2] and principal_stresses_array[2] >= principal_stresses_array[0]:
        fos = -(Suc) / principal_stresses_array[2]
    return fos
    
# code snippet for determining the failure theory to be used
result = select_failure_theory()
print("The employed theory is:", result)

# code snippet calling the stress tensor
stress_tensor = input_stress()
principal_stresses_array = principal_stresses(stress_tensor)

print("\nPrincipal Stresses:")
print(principal_stresses_array)

def calculate_fos_using_theory(result, principal_stresses_array, Sut, Syt, Syc=None):
    if result == "Brittle Coulomb-Mohr Theory":
        # You need Syc for Brittle Coulomb-Mohr Theory
        if Syc is None:
            raise ValueError("Ultimate compressive strength (Syc) is required for Brittle Coulomb-Mohr Theory.")
        return CoulombMohr(principal_stresses_array, Sut, Syc)
    elif result == "Modified Mohr Theory":
        return ModMohr(principal_stresses_array, Sut, Syt)
    elif result == "Ductile Coulomb-Mohr Theory":
        # You need Syc for Ductile Coulomb-Mohr Theory
        if Syc is None:
            raise ValueError("Ultimate compressive strength (Syc) is required for Ductile Coulomb-Mohr Theory.")
        return CoulombMohr(principal_stresses_array, Sut, Syc)
    elif result == "Maximum Shear Stress Theory":
        return MaxShear(principal_stresses_array, Syt)
    elif result == "Distortion-Energy Theory":
        return DistEnergy(principal_stresses_array, Syt)
    else:
        raise ValueError("Invalid failure theory selected.")

# Example usage:
Sut_input = float(input("Enter the value of Ultimate tensile strength of the material (Sut in MPa): "))
Syt_input = float(input("Enter the value of Yield strength of the material (Syt in MPa): "))
Syc_input = float(input("Enter the value of Ultimate compressive strength of the material (Syc in MPa): "))

fos_result = calculate_fos_using_theory(result, principal_stresses_array, Sut_input, Syt_input, Syc_input)
print(f"Factor of safety using {result} is: {fos_result}")
