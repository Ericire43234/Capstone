"""
Follower Beam Material Screening Tool

This script evaluates candidate materials for a compliant follower with a
circular cross section. It computes:

    • Factor of safety
    • Required input force
    • Alternating stress

The calculations follow the compliant beam formulations presented in:

    Howell, L. L. - *Compliant Mechanisms*

The script reads material properties from `BookMaterials.xlsx`, evaluates
each material, and classifies it as SAFE or UNSAFE based on the computed
factor of safety.

Assumptions
-----------
- Beam has circular cross-section
- Small deflection approximation used in Howell model
- Units are inches, pounds, and psi

Outputs
-------
Printed list of safe and unsafe materials with:
    safety factor
    required force
    alternating stress
"""

#%%Imports
import numpy as np
from CM_Functions import *
import pandas as pd

#%% Function Definition

def calculation(E = 4e5, Sy=8e3):
# Inputs

    # Default Inputs
    l = mm2in(18)      # Beam length [in]
    r = 0.005/2        # Beam radius [in]
    b = mm2in(4)       # Required transverse deflection [in]
    phi = 160          # Beam tip rotation angle [deg]

    # Compliant mechanism coefficients from Howell's textbook
    # These depend only on the beam deflection angle
    n = -1/np.tan(np.radians(phi))
    N = np.sqrt(1 + n**2)

    # Empirical correction factors from Howell
    y = gamma(n)
    K_theta = Ktheta(n)

    # Geometric properties of circular cross section
    I = (1/4) * np.pi * r**4   # Area moment of inertia [in^4]
    A = np.pi * r**2           # Cross-sectional area [in^2]

    # Beam stiffness and deflection relations
    K = y * K_theta * E * I / l

    # Angular deflection required for the specified displacement
    theta = np.arcsin(b / (y * l))

    # Required applied load
    P = K * theta / (N * y * l * np.sin(np.radians(phi) - theta))

    # Resultant force
    F = P * N

    # Location parameters used in stress evaluation
    a = l * (1 - y * (1 - np.cos(theta)))

    # Maximum bending stress at top and bottom fibers
    stress_top = (P*a + n*P*b)*(r/2)/(I) - n*P/A
    stress_bottom = -(P*a + n*P*b)*(r/2)/(I) - n*P/A

    max_stress = max(stress_top, stress_bottom)

    # Safety Metrics
    safety_factor = Sy/max_stress
    sig_alt = max_stress/2

    return safety_factor, F, sig_alt


#%% Main

if __name__ == "__main__":

    # Load material property database
    df = pd.read_excel("BookMaterials.xlsx", skiprows=1)
    materials = df.iloc[:, 0].to_numpy()      # 0 : Material Name
    Epsi  = df.iloc[:, 1].to_numpy()          # 1 : Young's Modulus [psi]
    Sypsi = df.iloc[:, 2].to_numpy()          # 2 : Yield Strength [psi]

    material_dict = {
    name: [p1, p2,]
    for name, p1, p2, in zip(materials, Epsi, Sypsi)
    }   

    # Initialize Dictionaries for Storing Results
    safe = {}
    unsafe = {}

    # Evaluate each material and classify based on safety factor
    for key in material_dict:
        value = material_dict[key]

        # Run beam calculation
        n, F, sig_alt = calculation(value[0],value[1])

        # Store results based on safety factor
        if n < 1:
            unsafe[key] = [n,F, sig_alt]
        else:
            safe[key] = [n,F, sig_alt]

    # Print out calculated values based on safety factor
    print("   ")
    print("Materials that are Unsafe for Use:")
    for key in unsafe:
        value = unsafe[key]
        print(f'{key}: n={value[0]:.2f}, F={value[1]:.2f}lbs, sig_a={value[2]:.2f}')

    print("   ")
    print("Materials that are Safe for Use:")
    for key in safe:
        value = safe[key]
        print(f'{key}: n={value[0]:.2f}, F={value[1]:.2f}lbs, sig_a={value[2]:.2f}')