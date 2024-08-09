import numpy as np
from scipy.optimize import fsolve

# constants
k = 1.380649e-23  # boltzman constant, J/K
q = 1.602176634e-19  # elementary charge, C
T = 298.15  # temperature in Kelvin (25 deg celc)
V_T = k * T / q  # thermal voltage

# given data points (I, V)

data_points = np.array([
    [5.997, 0.075],
    [5.973, 0.675],
    [5.733, 1.525],
    [5.275, 1.60],
    [4.495, 1.65],
])


# define the system of equations

def equations(params):
    I_PV, I_O, R_S, R_P, n = params

    equations_array = []
    for I, V in data_points:
        equation = I - (I_PV - I_O(np.exp((V + I * R_S) / (n * V_T)) - 1) - (V + I * R_S) / R_P)
        equations_array.append(equation)
    return equations_array


# initial guess for the parameters [I_PV,I_O,R_S,R_P, n]
initial_guess = [6, 1e-10, 0.01, 1000, 1]

# solve the system of equations

solution = fsolve(equations(), initial_guess)

# extract the parameters

I_PV, I_O, R_S, R_P, n = solution

# display the results

print(f"I_PV: {I_PV}")
print(f"I_O: {I_O}")
print(f"R_S: {R_S}")
print(f"R_P: {R_P}")
print(f"n: {n}")
