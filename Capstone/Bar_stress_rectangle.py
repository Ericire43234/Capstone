#%%Imprts
import numpy as np
from CM_Functions import *
import pandas as pd

def calculation(E = 0.2e6, Sy=60e3):
#%% Inputs

    # Default Values
    # E=.2*10**6        #Module of Elasticity in lb/in^2
    # Sy=60*10**3       #Yield Strength in lb/in^2
    l=mm2in(20)         #Length of the beam in in
    w=mm2in(3)          #Width of the beam in in
    h=mm2in(.5)          #Height of the beam in in
    b=mm2in(6)          #Deflection of the beam required in in
    phi=160             #Angle of deflection in degrees


    n=-1/np.tan(np.radians(phi))
    N=np.sqrt(1+n**2)
    y=gamma(n)   #Calculates n based on angle of deflection
    K_theta=Ktheta(n)
    I=w*h**3/12                             #Moment of Inertia for rectangular cross section
    A=w*h
    K=y*K_theta*E*I/l
    theta=np.arcsin (b/(y*l))
    P=K*theta/(N*y*l*np.sin(np.radians(phi)-theta))
    F=P*N
    a=l*(1-y*(1-np.cos(theta)))
    c=ctheta(n)
    theta_not=c*theta
    stress_top=-6*(P*a+n*P*b)/(w*h**2)-n*P/A
    stress_bottom=6*(P*a+n*P*b)/(w*h**2)-n*P/A
    max_stress=max(stress_top, stress_bottom)
    # print("Required Force F: ", F, "lb")
    safety_factor=Sy/max_stress
    # print("Safety Factor: ", safety_factor)

    return safety_factor, F



if __name__ == "__main__":

    df = pd.read_excel("Capstone/BookMaterials.xlsx", skiprows=1)
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

    # calculation()