"""
Compliant Spring Material Screening Tool

This script evaluates candidate materials for a compliant spring with a
rectangular cross section. It computes:

    • Factor of safety
    • Required input force

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
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt # type: ignore
from CM_Functions import *
import pandas as pd

def SF_Spring(E = 0.2e6, Sy=4e3):
    # Inputs
    # F - Force applied to spring [lbf]
    # Sy - Yield Stress of material [psi]

    # Default Inputs
    l = mm2in(11)        # Beam Length [in]
    w = mm2in(5.75)      # Beam Width [in] (Parallel to the direction of bending. Same as b when calculating I normally)
    h = mm2in(1)         # Beam Height [in]  (Perpendicular to direction of bending - sensitive)
    b = mm2in(2.44)      # Required transverse deflection [in]
    N = 4                # Number of beams in series to form spring
    phi = 90             # Beam tip rotation angle [deg]

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
    c = h/2          # Used to calculate bending stress [in]

    # Beam stiffness and deflection relations
    K = 2*y*K_theta*E*I/l

    # Effective Stiffness due to beams acting as springs in series
    k_eff = (N/K)**-1

    # We're saying that the fixed guided beam can be cut into two cantilever beams (See fixed guided of Howell)
    b = b/2

    # Angular deflection required for the specified displacement
    theta=np.arcsin(b/(y*l))

    # Required applied load
    P=k_eff*theta/(eta*y*l*np.sin(np.radians(phi)-theta))

    # Resultant force
    F=P*eta

    # Location parameters used in stress evaluation
    a=l*(1-y*(1-np.cos(theta)))
    
    # Maximum Bending Stress and Safety Factor
    stress_max = abs((P*(a+n*b)*c)/I) - (n*P)/A
    n = Sy/stress_max

    return n, F



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
        n, F, sa = SF_Spring(value[0],value[1])

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
