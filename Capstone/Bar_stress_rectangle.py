#%%Imprts
import numpy as np
from CM_Functions import *

def calculation():
#%% Inputs
    E=.2*10**6        #Module of Elasticity in lb/in^2
    Sy=60*10**3        #Yield Strength in lb/in^2
    l=20             #Length of the beam in in
    w=1.25           #Width of the beam in in
    h=1/32            #Height of the beam in in
    b=10            #Deflection of the beam required in in
    phi=135         #Angle of deflection in degrees


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
    print("Required Force F: ", F, "lb")
    safety_factor=Sy/max_stress
    print("Safety Factor: ", safety_factor)



if __name__ == "__main__":
    calculation()