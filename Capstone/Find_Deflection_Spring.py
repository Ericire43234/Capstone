# %% Imports
import numpy as np
import matplotlib.pyplot as plt # type: ignore
from CM_Functions import *
import pandas as pd

def calculation(F = 0.5,E = 0.2e6, Sy=4e3):
    # Inputs

    # Default Inputs
    # E = 0.2e6            # Modulus of Elasticity in lb/in^2
    # Sy = 4e3             # Yield Strength in lb/in^2
    l = mm2in(11)        # Length of the beam in in
    w = mm2in(5.75)      # Width of the beam in in (Parallel to the direction of bending. Same as b when calculating I normally)
    h = mm2in(1)         # Height of the beam in in  (Perpendicular to direction of bending - sensitive)
    N = 4                # Number of cantilevers
    phi = 90             # Angle of deflection in degrees
    safety_factor = 1    # Safety Factor

    # Get values from tabulated data
    n = -1/np.tan(np.radians(phi))
    eta = np.sqrt(1+n**2)
    y = gamma(n)   #Calculates n based on angle of deflection
    K_theta = Ktheta(n)

    # Calculate geometry based parameters
    I = w*h**3/12                             # Moment of Inertia for rectangular cross section
    A = w*h                                   # Cross sectional area
    c = h/2

    # Find Stiffness
    K = 2*y*K_theta*E*I/l
    k_eff = (N/K)**-1

    # Find the maximum allowable stress
    stress_max = Sy/safety_factor
    P = F/eta

    # Calculate a (horizontal deflection) This equation only works for n=0
    # The two comes from Equation 5.106
    a = 2*I*stress_max/(P*c)

    # Find b (vertical deflection)
    b = np.sqrt((y*l)**2 - a**2)
    theta_max = np.asin(b/(y*l))

    # print((y*l)**2)
    # print(a**2)

    # # We're saying that the fixed guided beam can be cut into two cantilever beams
    # b = b/2

    # theta=np.arcsin(b/(y*l))
    # P=k_eff*theta/(eta*y*l*np.sin(np.radians(phi)-theta))
    # F=P*eta
    # a=l*(1-y*(1-np.cos(theta)))
    # stress_max_vertical = P*a*c/I    # Bending Stress
    # stress_max = abs((P*(a+n*b)*c)/I) - (n*P)/A
    # n = Sy/stress_max

    return b, np.degrees(theta_max)



if __name__ == "__main__":

    df = pd.read_excel("BookMaterials.xlsx", skiprows=1)
    materials = df.iloc[:, 0].to_numpy()      # names
    Epsi  = df.iloc[:, 1].to_numpy()          # property column 1
    EPa   = df.iloc[:, 2].to_numpy()
    Sypsi = df.iloc[:, 3].to_numpy()
    SyPa  = df.iloc[:, 4].to_numpy()

    material_dict = {
    name: [p1, p2, p3, p4]
    for name, p1, p2, p3, p4 in zip(materials, Epsi, EPa, Sypsi, SyPa)
    }   

    deflections = {}

    for key in material_dict:
        value = material_dict[key]
        b, theta = calculation(0.3479,value[0],value[2])

        if(np.isnan(b)):
            continue
        else:
            deflections[key] = b, theta


    print("   ")
    print("Deflection for Each Material:")
    for key in deflections:
        value = deflections[key]
        print(f'{key}: b={value[0]:.2f} in or {in2mm(value[0]):.2f} mm')
        print(f'{key }: theta={value[1]:.2f}')
