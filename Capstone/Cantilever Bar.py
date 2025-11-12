#This will be a simple calculation for a cantilever bar with a point load at the free end. 
# w/ the inputs being the dimension and the out put will be min Module of Elasticity required, 
# along with the minimum stress

#%%
import sympy as sp
#Beam for pin would be cantilever beam with force at the free end (5.2)

#Inputs -- Dimensions for the cantilever bar
l=10.0  #Length of the beam in mm
w=1     #Width of the beam in mm
h=1     #Height of the beam in mm


#PRBM -- Creates a sympy symbolic equation for the moduls of elasticity based on the inputs

#Solves for moduls of Elasticity
#%%
K, l, y, I, E,w,h,n, phi, theta = sp.symbols('K l y I E w h n phi theta')
n_num=3

phi = sp.Eq(sp.atan(1/-n), phi)         #5.41
n=sp.simplify(sp.solve(phi, n)[0])
phi=theta + sp.pi/2       
   

if n_num<10 and n_num>.5:
    y=.841655-.0067807*n+.000438*n**2   #5.48
elif n_num<.5 and n_num>-1.8316:
    y=.852144-0.0182867*n               #5.48
elif n_num<1.8316 and n_num>-5:
    y=.912364+.0145928*n                #5.48

I=w*h**3/12                             #Moment of Inertia for rectangular cross section
K=sp.Eq(sp.pi*y**2*E*I/l,K)             #5.73
E=sp.simplify(sp.solve(K,E)[0])         #Solves for E

    #

#Outputs
# %%
