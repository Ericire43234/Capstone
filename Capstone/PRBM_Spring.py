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
    l = mm2in(13.33)     # Length of the beam in in
    w = mm2in(8.6)       # Width of the beam in in (Parallel to the direction of bending. Same as b when calculating I normally)
    h = mm2in(1.5)       # Height of the beam in in  (Perpendicular to direction of bending - sensitive)
    b = mm2in(3.66)      # Deflection of the beam required in in (currently bit diameter for CNC)
    phi = 90             # Angle of deflection in degrees

    # Get values from tabulated data
    n = -1/np.tan(np.radians(phi))
    N = np.sqrt(1+n**2)
    y = gamma(n)   #Calculates n based on angle of deflection
    K_theta = Ktheta(n)

    # Calculate geometry based parameters
    I = w*h**3/12                             # Moment of Inertia for rectangular cross section
    A = w*h                                   # Cross sectional area

    # Find Stiffness
    K = 2*y*K_theta*E*I/l
    theta=np.arcsin(b/(y*l))
    P=K*theta/(N*y*l*np.sin(np.radians(phi)-theta))
    F=P*N
    a=l*(1-y*(1-np.cos(theta)))
    c = h/2
    # stress_max_vertical = P*a*c/I    # Bending Stress
    stress_max = abs((P*(a+n*b)*c)/I) - (n*P)/A
    n = Sy/stress_max

    # Trying equations from CM book page 36
    M_max = 3*b*E*I/l**2
    F = M_max/l
    sigma = 3*b*E*h/(2*l**2)

    n = Sy/sigma

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

    safe = {}
    unsafe = {}

    for key in material_dict:
        value = material_dict[key]
        n, F = calculation(value[0],value[2])

        if n < 1:
            unsafe[key] = [n,F]
        else:
            safe[key] = [n,F]

    print("   ")
    print("Materials that are Unsafe for Use:")
    for key in unsafe:
        value = unsafe[key]
        print(f'{key}: n={value[0]:.2f}, F={value[1]:.2f}lbs')

    print("   ")
    print("Materials that are Safe for Use:")
    for key in safe:
        value = safe[key]
        print(f'{key}: n={value[0]:.2f}, F={value[1]:.2f}lbs')