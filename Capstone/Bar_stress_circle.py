#%%Imprts
import numpy as np
from CM_Functions import *

def calculation():
#%% Inputs
    E=30*10**6         #Module of Elasticity in lb/in^2
    l=20             #Length of the beam in in
    r=.1           #Radius of the beam in in
    b=.5            #Deflection of the beam required in in
    phi=135         #Angle of deflection in degrees
    Sy=60*10**3        #Yield Strength in lb/in^2

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
    print("Required Force F: ", F, "lb")
    safety_factor=Sy/max_stress
    print("Safety Factor: ", safety_factor)




if __name__ == "__main__":
    calculation()