#%%Imprts
import numpy as np
from CM_Functions import *
import pandas as pd

def calculation(E = 4e5, Sy=8e3):
#%% Inputs

    # Default Inputs
    # E=400000       # Module of Elasticity in lb/in^2
    # Sy=8000        # Yield Strength in lb/in^2
    l=mm2in(20)      # Length of the beam in in
    r=mm2in(1)       # Radius of the beam in in
    b=mm2in(6)       # Deflection of the beam required in in
    phi=160          # Angle of deflection in degrees


    n=-1/np.tan(np.radians(phi))
    N=np.sqrt(1+n**2)
    y=gamma(n)   #Calculates n based on angle of deflection
    K_theta=Ktheta(n)
    I=(1/4)*np.pi*r**4                             #Moment of Inertia for rectangular cross section
    A=np.pi*r**2
    K=y*K_theta*E*I/l
    theta=np.arcsin (b/(y*l))
    P=K*theta/(N*y*l*np.sin(np.radians(phi)-theta))
    F=P*N
    a=l*(1-y*(1-np.cos(theta)))
    c=ctheta(n)
    theta_not=c*theta
    stress_top=(P*a+n*P*b)*(r/2)/(I)-n*P/A
    stress_bottom=-(P*a+n*P*b)*(r/2)/(I)-n*P/A
    max_stress=max(stress_top, stress_bottom)
    safety_factor=Sy/max_stress

    return safety_factor, F




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