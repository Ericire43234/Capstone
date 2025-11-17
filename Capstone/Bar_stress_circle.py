#%%Imprts
import numpy as np

#%%
def gamma(n_num):
    if n_num<10 and n_num>.5:
        y=.841655-.0067807*n_num+.000438*n_num**2   #5.48
    elif n_num<.5 and n_num>-1.8316:
        y=.852144-0.0182867*n_num             
    elif n_num<1.8316 and n_num>-5:
        y=.912364+.0145928*n_num
    return y  

def Ktheta(n):
    if n>-5 and n<=-2.5:
        K_theta=3.024112 + 0.121290*n+.0031696*n**2
    elif n>-2.5 and n<=-1:
        K_theta=1.967647-2.616021*n-3.738166*n**2-2.649437*n**3-.891906*n**4-.113063*n**5
    elif n>-1 and n<=10:
        K_theta=2.654855-.509896*10**-1*n+.126749*10**-1*n**2-.142039*10**-2*n**3+.584525*10**-4*n**4
    return K_theta

def ctheta(n):
    if n>0 and n<=.5:
        c=1.2385
    elif n>.5 and n<=1:
        c=1.2430
    elif n>1 and n<=1.5:
        c=1.2467
    elif n>1.5 and n<=2:
        c=1.2492
    elif n>2 and n<=3:
        c=1.2511
    elif n>3 and n<=4:
        c=1.2534
    elif n>4 and n<=5:
        c=1.2548
    elif n>5 and n<=7.5:
        c=1.2557
    elif n>7.5 and n<=10:
        c=1.257
    elif n>10:
        c=1.2578
    elif n<-.5:
        c=1.2348
    elif n>=-.5 and n<0:
        c=1.2348
    elif n>=-1 and n<=-.5:
        c=1.2323
    elif n>=-1.5 and n<-1:
        c=1.2322
    elif n>=-2 and n<-1.5:
        c=1.2293
    elif n>=-3 and n<-2:
        c=1.2119
    elif n>=-4 and n<-3:
        c=1.1971
    elif n>=-5 and n<-4:
        c=1.1788
    return c


def calculation():
#%% Inputs
    E=30*10**6         #Module of Elasticity in lb/in^2
    l=20             #Length of the beam in in
    r=.1           #Radius of the beam in in
    b=.5            #Deflection of the beam required in in
    phi=135         #Angle of deflection in degrees

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
    print("Required Force F: ", F, "lb")
    print("stress at top fiber: ", stress_top, "lb/in^2")
    print("stress at bottom fiber: ", stress_bottom, "lb/in^2")



if __name__ == "__main__":
    calculation()