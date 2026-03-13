"""
Follower Beam Material Screening Tool

This script evaluates candidate materials for a compliant follower with a
rectangular cross section. It computes:

    • Factor of safety
    • Required input force
    • Alternating stress

The calculations follow the compliant beam formulations presented in:

    Howell, L. L. - "Compliant Mechanisms"

The script reads material properties from `BookMaterials.xlsx`, evaluates
each material, and classifies it as SAFE or UNSAFE based on the computed
factor of safety.

Assumptions
-----------
- Beam has rectangular cross-section
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

def SF_Rectangular_Follower(E = 0.2e6, Sy=60e3):
    # Inputs

    # Default Values
    l = mm2in(19.2)       # Beam Length [in]
    h = mm2in(0.8)        # Beam Height [in (Perpendicular to direction of bending. Sensitive parameter)
    w = mm2in(2.9)        # Beam Width [in] (Parallel to direction of bending. Same as b when calculating I normally)
    b = mm2in(9)          # Required transverse deflection [in]
    phi = 160             # Beam tip rotation angle [deg]

    # Compliant mechanism coefficients from Howell's textbook
    # These depend only on the beam deflection angle
    n = -1/np.tan(np.radians(phi))
    eta = np.sqrt(1+n**2)

    # Empirical correction factors from Howell
    y = gamma(n)   
    K_theta = Ktheta(n)

    # Geometric properties of rectangular cross section
    I = w*h**3/12    # Area moment of inertia [in^4]
    A = w*h          # Cross-sectional area [in^2]

    # Beam stiffness and deflection relations
    K = y*K_theta*E*I/l

    # Angular deflection required for the specified displacement
    theta = np.arcsin (b/(y*l))

    # Required applied load
    P = K*theta/(eta*y*l*np.sin(np.radians(phi)-theta))

    # Resultant force
    F = P*eta

    # Location parameters used in stress evaluation
    a = l*(1-y*(1-np.cos(theta)))
    
    # Maximum bending stress and top and bottom fibers
    stress_top = -6*(P*a+n*P*b)/(w*h**2)-n*P/A
    stress_bottom = 6*(P*a+n*P*b)/(w*h**2)-n*P/A

    max_stress = max(stress_top, stress_bottom)

    # Safety Metrics
    stress_alternating = max_stress/2
    safety_factor = Sy/max_stress

    return safety_factor, F, stress_alternating



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

    # Initialize dictionaries for storing results
    safe = {}
    unsafe = {}

    # Evaluate each material and classify based on safety factor
    for key in material_dict:
        value = material_dict[key]

        # Run beam calculation
        n, F, sa = SF_Rectangular_Follower(value[0],value[1])

        # Store results based on safety factor
        if n < 1:
            unsafe[key] = [n,F,sa]
        else:
            safe[key] = [n,F,sa]

    # Print out calculated values based on safety factor
    print("   ")
    print("Materials that are Unsafe for Use:")
    for key in unsafe:
        value = unsafe[key]
        print(f'{key}: n={value[0]:.2f}, F={value[1]:.2f}lbs, sig_a={value[2]:.2f} psi')

    print("   ")
    print("Materials that are Safe for Use:")
    for key in safe:
        value = safe[key]
        print(f'{key}: n={value[0]:.2f}, F={value[1]:.2f}lbs, sig_a={value[2]:.2f} psi')
