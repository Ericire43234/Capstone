# %% Imports
import numpy as np
import matplotlib.pyplot as plt # type: ignore
from CM_Functions import *
import pandas as pd

def calculation(E = 0.2e6, Sy=4e3):
    # Inputs

    # Default Inputs
    # E = 0.2e6            # Modulus of Elasticity in lb/in^2
    # Sy = 4e3             # Yield Strength in lb/in^2
    l = mm2in(14/2)      # Length of the beam in in
    w = mm2in(6.5)       # Width of the beam in in
    h = mm2in(1)         # Height of the beam in in
    b = mm2in(0.795/2)   # Deflection of the beam required in in
    phi = 90             # Angle of deflection in degrees

    # Get values from tabulated data
    n = -1/np.tan(np.radians(phi))
    N = np.sqrt(1+n**2)
    y = gamma(n)   #Calculates n based on angle of deflection
    K_theta = Ktheta(n)

    # Calculate geometry based parameters
    I = w*h**3/12                             # Moment of Inertia for rectangular cross section
    A = w*h

    # Find Stiffness
    K = 2*y*K_theta*E*I/l
    theta=np.arcsin (b/(y*l))
    P=K*theta/(N*y*l*np.sin(np.radians(phi)-theta))
    F=P*N
    a=l*(1-y*(1-np.cos(theta)))
    ctheta = 0
    c = h/2
    theta_not=c*theta
    stress_max = P*a*c/(2*I)
    n = Sy/stress_max
    # print("Required Force F: ", F, "lb")
    # print("Maximum Stress: ", stress_max, "lb/in^2")
    # if abs(stress_max)>=Sy:
    #     print("Stress exceeds Yield Strength!")
    #     print(f'Factor of Safety: {n}')
    # else:
    #     print("Stress is within Yield Strength.")
    #     print(f'Factor of Safety: {n}')

    return n, F



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

    #print(material_dict)

    for key in material_dict:
        value = material_dict[key]
        n, F = calculation(value[0],value[2])
        print(f'{key}: n={n:.2f}, F={F:.2f}lbs')

    #calculation()