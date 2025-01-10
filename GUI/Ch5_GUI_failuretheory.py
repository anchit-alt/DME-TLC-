import numpy as np
import customtkinter

# Ductile Brittle
def select_brittle_ductile(ef):
    if ef < 0.05:
        return 0
    else:
        return 1

# function to determine failure theory to be employed0
def select_failure_theory(ef, Syc, Syt, Conservative):
    fos = 0

    if ef < 0.05:
        if Conservative == "Conservative":
            return "Modified Mohr Theory" 
        else:
            return "Brittle Coulomb-Mohr Theory"          
    else:
        if Syc == Syt:
            if Conservative == "Conservative":
                return "Maximum Shear Stress Theory"
            else: 
                return "Distortion-Energy Theory"
        else: 
            return "Ductile Coulomb-Mohr Theory"

# function to calculate stress tensor
# def input_stress():
#     stress_tensor = np.zeros((3, 3))

#     print("Enter the components of the stress tensor in the given format:")
#     print(f"[ σxx, τxy, τxz ]")
#     print(f"[ τyx, σyy, τyz ]")
#     print(f"[ τzx, τzy, σzz ]")
#     for i in range(3):
#         for j in range(3):
#             stress_tensor[i, j] = float(input(f"σ_{i+1}{j+1}: "))

#     return stress_tensor

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
    print(principal_stresses_array)
    # sigma = np.sqrt(np.power(principal_stresses_array[0], 2) - principal_stresses_array[0] * principal_stresses_array[1] + np.power(principal_stresses_array[1], 2))
    sigma = np.sqrt((np.power(principal_stresses_array[0]-principal_stresses_array[1],2) + np.power(principal_stresses_array[1]-principal_stresses_array[2],2) + np.power(principal_stresses_array[0]-principal_stresses_array[2],2))/2)
    print(sigma)
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

def calculate_fos_using_theory(result, principal_stresses_array, Syt, Syc, Sut, Suc):
    if result == "Brittle Coulomb-Mohr Theory":
        return CoulombMohr(principal_stresses_array, Sut, Suc)
    elif result == "Modified Mohr Theory":
        return ModMohr(principal_stresses_array, Sut, Suc)
    elif result == "Ductile Coulomb-Mohr Theory":
        return CoulombMohr(principal_stresses_array, Syt, Syc)
    elif result == "Maximum Shear Stress Theory":
        return MaxShear(principal_stresses_array, Syt)
    elif result == "Distortion-Energy Theory":
        return DistEnergy(principal_stresses_array, Syt)
    else:
        raise ValueError("Invalid failure theory selected.")

class stage1_frame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title = title
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew",columnspan=2)

        self.label = customtkinter.CTkLabel(self, text="Strain at Fracture (ef)", fg_color="transparent")
        self.label.grid(row=1, column=0, padx=10, pady=10, sticky="w", columnspan=1)
        self.entry = customtkinter.CTkEntry(self, placeholder_text="0.05")
        self.entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=1)

    def get(self):
        ef_text = self.entry.get()
        return ef_text


class stage2_frame_yn(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.radiobuttons = []
        self.values = values
        self.variable = customtkinter.StringVar(value="")

        self.title = title
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=2)

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

class stage2_frame_S(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=2)

        self.title = title
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=4)

        self.label1 = customtkinter.CTkLabel(self, text="Syc", fg_color="transparent")
        self.label1.grid(row=1, column=0, padx=10, pady=10, sticky="w", columnspan=2)
        self.entry1 = customtkinter.CTkEntry(self, placeholder_text="100 (MPa)")
        self.entry1.grid(row=1, column=2, padx=10, pady=10, sticky="ew", columnspan=2)

        self.label2 = customtkinter.CTkLabel(self, text="Syt", fg_color="transparent")
        self.label2.grid(row=2, column=0, padx=10, pady=10, sticky="w", columnspan=2)
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="100 (MPa)")
        self.entry2.grid(row=2, column=2, padx=10, pady=10, sticky="ew", columnspan=2)

    def get(self):
        Syc = self.entry1.get()
        Syt = self.entry2.get()

        return Syc, Syt

class stage2_frame_B(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=2)

        self.title = title
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=4)

        self.label1 = customtkinter.CTkLabel(self, text="Suc", fg_color="transparent")
        self.label1.grid(row=1, column=0, padx=10, pady=10, sticky="w", columnspan=2)
        self.entry1 = customtkinter.CTkEntry(self, placeholder_text="100 (MPa)")
        self.entry1.grid(row=1, column=2, padx=10, pady=10, sticky="ew", columnspan=2)

        self.label2 = customtkinter.CTkLabel(self, text="Sut", fg_color="transparent")
        self.label2.grid(row=2, column=0, padx=10, pady=10, sticky="w", columnspan=2)
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="100 (MPa)")
        self.entry2.grid(row=2, column=2, padx=10, pady=10, sticky="ew", columnspan=2)

    def get(self):
        Suc = self.entry1.get()
        Sut = self.entry2.get()

        return Suc, Sut


class stage4_frame_tensor(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.stress_tensor = np.zeros((3, 3))

        self.title = title
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=4)

        self.entry11 = customtkinter.CTkEntry(self, placeholder_text="11")
        self.entry11.grid(row=1, column=0, padx=10, pady=10, sticky="", columnspan=1)

        self.entry12 = customtkinter.CTkEntry(self, placeholder_text="12")
        self.entry12.grid(row=1, column=1, padx=10, pady=10, sticky="", columnspan=1)

        self.entry13 = customtkinter.CTkEntry(self, placeholder_text="13")
        self.entry13.grid(row=1, column=2, padx=10, pady=10, sticky="", columnspan=1)

        self.entry21 = customtkinter.CTkEntry(self, placeholder_text="21")
        self.entry21.grid(row=2, column=0, padx=10, pady=10, sticky="", columnspan=1)

        self.entry22 = customtkinter.CTkEntry(self, placeholder_text="22")
        self.entry22.grid(row=2, column=1, padx=10, pady=10, sticky="", columnspan=1)

        self.entry23 = customtkinter.CTkEntry(self, placeholder_text="23")
        self.entry23.grid(row=2, column=2, padx=10, pady=10, sticky="", columnspan=1)

        self.entry31 = customtkinter.CTkEntry(self, placeholder_text="31")
        self.entry31.grid(row=3, column=0, padx=10, pady=10, sticky="", columnspan=1)

        self.entry32 = customtkinter.CTkEntry(self, placeholder_text="32")
        self.entry32.grid(row=3, column=1, padx=10, pady=10, sticky="", columnspan=1)

        self.entry33 = customtkinter.CTkEntry(self, placeholder_text="33")
        self.entry33.grid(row=3, column=2, padx=10, pady=10, sticky="", columnspan=1)

    def get(self):
        self.stress_tensor[0, 0] = float(self.entry11.get())
        self.stress_tensor[0, 1] = float(self.entry12.get())
        self.stress_tensor[0, 2] = float(self.entry13.get())

        self.stress_tensor[1, 0] = float(self.entry21.get())
        self.stress_tensor[1, 1] = float(self.entry22.get())
        self.stress_tensor[1, 2] = float(self.entry23.get())

        self.stress_tensor[2, 0] = float(self.entry31.get())
        self.stress_tensor[2, 1] = float(self.entry32.get())
        self.stress_tensor[2, 2] = float(self.entry33.get())

        return self.stress_tensor

class stage5_frame_result(customtkinter.CTkFrame):
    def __init__(self, master, title, theory, FOS):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.title = title
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew", columnspan=4)

        self.label11 = customtkinter.CTkLabel(self, text="Theory Employed: ", fg_color="transparent")
        self.label11.grid(row=1, column=0, padx=10, pady=10, sticky="w", columnspan=1)

        self.label12 = customtkinter.CTkLabel(self, text=theory, fg_color="transparent")
        self.label12.grid(row=1, column=1, padx=10, pady=10, sticky="w", columnspan=1)

        self.label21 = customtkinter.CTkLabel(self, text="Factor of Safety: ", fg_color="transparent")
        self.label21.grid(row=2, column=0, padx=10, pady=10, sticky="w", columnspan=1)

        self.label22 = customtkinter.CTkLabel(self, text=str(FOS), fg_color="transparent")
        self.label22.grid(row=2, column=1, padx=10, pady=10, sticky="w", columnspan=1)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Failures Resulting From Static Loading")
        self.geometry("600x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.Syc = 0
        self.Syt = 0
        self.Sut = 0
        self.Suc = 0

        # ef value input from user
        self.stage1_frame = stage1_frame(self, title="Brittle or Ductile")
        self.stage1_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=4)

        self.stage1_button = customtkinter.CTkButton(self, text="Confirm", command=self.stage1_button_callback)
        self.stage1_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=4)

    # ef
    def stage1_button_callback(self):

        self.ef = self.stage1_frame.get()

        # Deciding ductile brittle
        if select_brittle_ductile(float(self.ef)) == 0:
            # Ductile - Syt and Syc
            self.stage2_frame_B = stage2_frame_B(self, title="Ultimate Tensile & Compressive")
            self.stage2_frame_B.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)

            self.stage22_button = customtkinter.CTkButton(self, text="Confirm", command=self.stage22_button_callback)
            self.stage22_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=4)

        else:
            # Ductile - Syt and Syc
            self.stage2_frame_S = stage2_frame_S(self, title="Yield Tensile & Compressive")
            self.stage2_frame_S.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)

            self.stage2_button = customtkinter.CTkButton(self, text="Confirm", command=self.stage2_button_callback)
            self.stage2_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=4)

    # Syc and Syt
    def stage2_button_callback(self):

        self.Syc, self.Syt = self.stage2_frame_S.get()

        if self.Syc == self.Syt:
            # Brittle - Conservative and Non-Conservative
            values = ["Conservative", "Non Conservative"]
            self.stage2_frame_yn = stage2_frame_yn(self, title="Conservative or Non-Conservative", values=values)
            self.stage2_frame_yn.grid(row=2, column=2, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)

            self.stage3_button = customtkinter.CTkButton(self, text="Confirm", command=self.stage3_button_callback)
            self.stage3_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=4)
        
        else:
            self.stage31_button_callback()
    
    # Suc and Sut
    def stage22_button_callback(self):

        self.Suc, self.Sut = self.stage2_frame_B.get()

        # Ductile - Conservative and Non-Conservative
        values = ["Conservative", "Non Conservative"]
        self.stage2_frame_yn = stage2_frame_yn(self, title="Conservative or Non-Conservative", values=values)
        self.stage2_frame_yn.grid(row=2, column=2, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)

        self.stage3_button = customtkinter.CTkButton(self, text="Confirm", command=self.stage3_button_callback)
        self.stage3_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=4)

    # Conservative or Non-Conservative
    def stage3_button_callback(self):

        self.conservative = self.stage2_frame_yn.get()
        self.failureTheory = select_failure_theory(float(self.ef), float(self.Syc), float(self.Syt), self.conservative)

        self.stage4_frame_tensor = stage4_frame_tensor(self, title="Stress Tensor")
        self.stage4_frame_tensor.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=4)

        self.stage4_button = customtkinter.CTkButton(self, text="Confirm", command=self.stage4_button_callback)
        self.stage4_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=4)
    
    # Syc != Syt
    def stage31_button_callback(self):

        self.conservative = "NA"
        self.failureTheory = select_failure_theory(float(self.ef), float(self.Syc), float(self.Syt), self.conservative)

        self.stage4_frame_tensor = stage4_frame_tensor(self, title="Stress Tensor")
        self.stage4_frame_tensor.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=4)

        self.stage4_button = customtkinter.CTkButton(self, text="Confirm", command=self.stage4_button_callback)
        self.stage4_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=4)

    # Stress Tensor
    def stage4_button_callback(self):

        self.stress_tensor = self.stage4_frame_tensor.get()
        self.principal_stresses_array = principal_stresses(self.stress_tensor)
        self.fos = calculate_fos_using_theory(self.failureTheory, self.principal_stresses_array, float(self.Syt), float(self.Syc), float(self.Sut), float(self.Suc))

        self.stage5_frame_result= stage5_frame_result(self, title="Result", theory=self.failureTheory, FOS=self.fos)
        self.stage5_frame_result.grid(row=6, column=0, padx=10, pady=10, sticky="nsew", columnspan=4)




        



app = App()
app.mainloop()

# ef value input
# eps_f = float(input("Enter the strain value: "))
    
# code snippet for determining the failure theory to be used
# result = select_failure_theory(eps_f)
# print("The employed theory is:", result)

# # code snippet calling the stress tensor
# stress_tensor = input_stress()
# principal_stresses_array = principal_stresses(stress_tensor)

# print("\nPrincipal Stresses:")
# print(principal_stresses_array)


# # Example usage:
# Sut_input = float(input("Enter the value of Ultimate tensile strength of the material (Sut in MPa): "))
# Syt_input = float(input("Enter the value of Yield strength of the material (Syt in MPa): "))
# Syc_input = float(input("Enter the value of Ultimate compressive strength of the material (Syc in MPa): "))

# fos_result = calculate_fos_using_theory(result, principal_stresses_array, Sut_input, Syt_input, Syc_input)
# print(f"Factor of safety using {result} is: {fos_result}")
