# %% Imports
import numpy as np
import matplotlib.pyplot as plt # type: ignore
from CM_Functions import *

def calculation():
    # Inputs
    E = 0.2e6            # Modulus of Elasticity in lb/in^2
    Sy = 4e3             # Yield Strength in lb/in^2
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
    print("Required Force F: ", F, "lb")
    print("Maximum Stress: ", stress_max, "lb/in^2")
    if abs(stress_max)>=Sy:
        print("Stress exceeds Yield Strength!")
        print(f'Factor of Safety: {n}')
    else:
        print("Stress is within Yield Strength.")
        print(f'Factor of Safety: {n}')



if __name__ == "__main__":

    mats = {}
    calculation()