"""
Compliant Spring Material Screening Tool

This script evaluates candidate materials for a compliant spring with a
rectangular cross section. It computes:

    • Vertical Deflection
    • Angular Deflection

The calculations follow the guided compliant beam formulations presented in:

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
    Vertical Deflection
    Angular Deflection
"""
# Imports
import numpy as np
import matplotlib.pyplot as plt # type: ignore
from CM_Functions import *
import pandas as pd

def Deflection_Spring(F = 0.5, Sy=4e3):
    # Inputs
    # F - Force applied to spring [lbf]
    # Sy - Yield Stress of material [psi]

    # Default Inputs
    l = mm2in(11)        # Beam Length [in]
    h = mm2in(1)         # Beam Height [in]  (Perpendicular to direction of bending - sensitive)
    w = mm2in(5.75)      # Beam Width [in] (Parallel to the direction of bending. Same as b when calculating I normally)
    phi = 90             # Beam tip rotation angle [deg]
    safety_factor = 1    # Safety Factor

    # Compliant mechanism coefficients from Howell's textbook
    # These depend only on the beam deflection angle
    n = -1/np.tan(np.radians(phi))
    eta = np.sqrt(1+n**2)

    # Empirical correction factors from Howell
    y = gamma(n)

    # Geometric properties of rectangular cross section
    I = w*h**3/12    # Area Moment of Inertia [in^4]
    c = h/2          # Used to calculate bending stress

    # Find the maximum allowable stress
    stress_max = Sy/safety_factor

    # Required applied load
    P = F/eta

    # Calculate a (horizontal deflection) This equation only works for n=0
    # The two comes from Equation 5.106 of Howell's "Compliant Mechanisms"
    a = 2*I*stress_max/(P*c)

    # Find b (vertical deflection) and theta_max (angular deflection)
    b = np.sqrt((y*l)**2 - a**2)
    theta_max = np.asin(b/(y*l))

    return b, np.degrees(theta_max)



if __name__ == "__main__":

    # Load material property database
    df = pd.read_excel("BookMaterials.xlsx", skiprows=1)
    materials = df.iloc[:, 0].to_numpy()      # 0 : Material Name
    Epsi  = df.iloc[:, 1].to_numpy()          # 1 : Young's Modulus [psi]
    Sypsi = df.iloc[:, 2].to_numpy()          # 2 : Yield Strength [psi]

    material_dict = {
    name: [p1, p2]
    for name, p1, p2 in zip(materials, Epsi, Sypsi)
    }   

    # Initialize dictionary to store results
    deflections = {}

    # Evaluate each material
    for key in material_dict:
        value = material_dict[key]

        # Run Spring Calculation
        b, theta = Deflection_Spring(0.3479,value[1])

        # Store results
        if(np.isnan(b)):
            continue
        else:
            deflections[key] = b, theta

    # Print out calculated deflection
    print("   ")
    print("Deflection for Each Material:")
    for key in deflections:
        value = deflections[key]
        print(f'{key}: b={value[0]:.2f} in or {in2mm(value[0]):.2f} mm')
        print(f'{key }: theta={value[1]:.2f}')
