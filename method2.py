import numpy as np
from scipy.optimize import fsolve

# Constants
k = 1.380649e-23  # Boltzmann constant (J/K)
q = 1.602176634e-19  # Electron charge (C)
T = 298.15  # Temperature in Kelvin (25°C)
V_T = k * T / q  # Thermal voltage

# Given I-V pairs
I_vals = np.array([5.997, 5.973, 5.733, 5.275, 4.495])
V_vals = np.array([0.075, 0.675, 1.525, 1.60, 1.65])


# Define the system of equations
def equations(params):
    I_PV, I_0, R_S, R_P, n = params
    equations = []

    for i in range(len(I_vals)):
        I = I_vals[i]
        V = V_vals[i]
        eq = I_PV - I_0 * (np.exp((V + I * R_S) / (n * V_T)) - 1) - (V + I * R_S) / R_P - I
        equations.append(eq)

    return equations


# Initial guess for I_PV, I_0, R_S, R_P, n
initial_guess = [6, 1e-10, 0.01, 1000, 1.5]

# Solve the system of equations
solution = fsolve(equations, initial_guess)

# Print the estimated parameters
I_PV, I_0, R_S, R_P, n = solution
print(f"Estimated Parameters:\nI_PV = {I_PV} A\nI_0 = {I_0} A\nR_S = {R_S} ohms\nR_P = {R_P} ohms\nn = {n}")
