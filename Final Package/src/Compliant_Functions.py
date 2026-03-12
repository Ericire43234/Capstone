# Imports
import numpy as np
from Howell_Consts import *
from utils import *

def SF_Rectangular_Follower(E = 0.2e6, Sy=60e3):
    # Inputs
    # E  - Young's Modulus of Material [psi]
    # Sy - Yield Stress of material [psi]

    # Default Values
    l = mm2in(19.2)       # Beam Length [in]
    h = mm2in(0.8)        # Beam Height [in (Perpendicular to direction of bending. Sensitive parameter)
    w = mm2in(2.9)        # Beam Width [in] (Parallel to direction of bending. Same as b when calculating I normally)
    b = mm2in(9)          # Required transverse deflection [in]
    phi = 160             # Beam tip rotation angle [deg]

    # Compliant mechanism coefficients from Howell's textbook
    # These depend only on the beam deflection angle
    n = -1/np.tan(np.radians(phi))
    eta = np.sqrt(1+n**2)

    # Empirical correction factors from Howell
    y = gamma(n)   
    K_theta = Ktheta(n)

    # Geometric properties of rectangular cross section
    I = w*h**3/12    # Area moment of inertia [in^4]
    A = w*h          # Cross-sectional area [in^2]

    # Beam stiffness and deflection relations
    K = y*K_theta*E*I/l

    # Angular deflection required for the specified displacement
    theta = np.arcsin (b/(y*l))

    # Required applied load
    P = K*theta/(eta*y*l*np.sin(np.radians(phi)-theta))

    # Resultant force
    F = P*eta

    # Location parameters used in stress evaluation
    a = l*(1-y*(1-np.cos(theta)))
    
    # Maximum bending stress and top and bottom fibers
    stress_top = -6*(P*a+n*P*b)/(w*h**2)-n*P/A
    stress_bottom = 6*(P*a+n*P*b)/(w*h**2)-n*P/A

    max_stress = max(stress_top, stress_bottom)

    # Safety Metrics
    stress_alternating = max_stress/2
    safety_factor = Sy/max_stress

    return safety_factor, F, stress_alternating


def SF_Circular_Follower(E = 4e5, Sy=8e3):
    # Inputs
    # E  - Young's Modulus of Material [psi]
    # Sy - Yield Stress of material [psi]

    # Default Inputs
    l = mm2in(18)      # Beam length [in]
    r = 0.005/2        # Beam radius [in]
    b = mm2in(4)       # Required transverse deflection [in]
    phi = 160          # Beam tip rotation angle [deg]

    # Compliant mechanism coefficients from Howell's textbook
    # These depend only on the beam deflection angle
    n = -1/np.tan(np.radians(phi))
    N = np.sqrt(1 + n**2)

    # Empirical correction factors from Howell
    y = gamma(n)
    K_theta = Ktheta(n)

    # Geometric properties of circular cross section
    I = (1/4) * np.pi * r**4   # Area moment of inertia [in^4]
    A = np.pi * r**2           # Cross-sectional area [in^2]

    # Beam stiffness and deflection relations
    K = y * K_theta * E * I / l

    # Angular deflection required for the specified displacement
    theta = np.arcsin(b / (y * l))

    # Required applied load
    P = K * theta / (N * y * l * np.sin(np.radians(phi) - theta))

    # Resultant force
    F = P * N

    # Location parameters used in stress evaluation
    a = l * (1 - y * (1 - np.cos(theta)))

    # Maximum bending stress at top and bottom fibers
    stress_top = (P*a + n*P*b)*(r/2)/(I) - n*P/A
    stress_bottom = -(P*a + n*P*b)*(r/2)/(I) - n*P/A

    max_stress = max(stress_top, stress_bottom)

    # Safety Metrics
    safety_factor = Sy/max_stress
    sig_alt = max_stress/2

    return safety_factor, F, sig_alt


def Deflection_Spring(F = 0.5,E = 0.2e6, Sy=4e3):
    # Inputs
    # F - Force applied to spring [lbf]
    # Sy - Yield Stress of material [psi]

    # Default Inputs
    l = mm2in(11)        # Beam Length [in]
    h = mm2in(1)         # Beam Height [in]  (Perpendicular to direction of bending - sensitive)
    w = mm2in(5.75)      # Beam Width [in] (Parallel to the direction of bending. Same as b when calculating I normally)
    N = 4                # Number of cantilevers in series
    phi = 90             # Beam tip rotation angle [deg]
    safety_factor = 1    # Safety Factor

    # Compliant mechanism coefficients from Howell's textbook
    # These depend only on the beam deflection angle
    n = -1/np.tan(np.radians(phi))
    eta = np.sqrt(1+n**2)

    # Empirical correction factors from Howell
    y = gamma(n)

    # Geometric properties of rectangular cross section
    I = w*h**3/12    # Area Moment of Inertia [in^4]
    c = h/2          # Used to calculate bending stress

    # Find the maximum allowable stress
    stress_max = Sy/safety_factor

    # Required applied load
    P = F/eta

    # Calculate a (horizontal deflection) This equation only works for n=0
    # The two comes from Equation 5.106 of Howell's "Compliant Mechanisms"
    a = 2*I*stress_max/(P*c)

    # Find b (vertical deflection) and theta_max (angular deflection)
    b = np.sqrt((y*l)**2 - a**2)
    theta_max = np.asin(b/(y*l))

    return b, np.degrees(theta_max)


def SF_Spring(E = 0.2e6, Sy=4e3):
    # Inputs
    # F - Force applied to spring [lbf]
    # Sy - Yield Stress of material [psi]

    # Default Inputs
    l = mm2in(11)        # Beam Length [in]
    w = mm2in(5.75)      # Beam Width [in] (Parallel to the direction of bending. Same as b when calculating I normally)
    h = mm2in(1)         # Beam Height [in]  (Perpendicular to direction of bending - sensitive)
    b = mm2in(2.44)      # Required transverse deflection [in]
    N = 4                # Number of beams in series to form spring
    phi = 90             # Beam tip rotation angle [deg]

    # Compliant mechanism coefficients from Howell's textbook
    # These depend only on the beam deflection angle
    n = -1/np.tan(np.radians(phi))
    eta = np.sqrt(1+n**2)

    # Empirical correction factors from Howell
    y = gamma(n)
    K_theta = Ktheta(n)

    # Geometric properties of rectangular cross section
    I = w*h**3/12    # Area moment of inertia [in^4]
    A = w*h          # Cross-sectional area [in^2]
    c = h/2          # Used to calculate bending stress [in]

    # Beam stiffness and deflection relations
    K = 2*y*K_theta*E*I/l

    # Effective Stiffness due to beams acting as springs in series
    k_eff = (N/K)**-1

    # We're saying that the fixed guided beam can be cut into two cantilever beams (See fixed guided of Howell)
    b = b/2

    # Angular deflection required for the specified displacement
    theta=np.arcsin(b/(y*l))

    # Required applied load
    P=k_eff*theta/(eta*y*l*np.sin(np.radians(phi)-theta))

    # Resultant force
    F=P*eta

    # Location parameters used in stress evaluation
    a=l*(1-y*(1-np.cos(theta)))
    
    # Maximum Bending Stress and Safety Factor
    stress_max = abs((P*(a+n*b)*c)/I) - (n*P)/A
    n = Sy/stress_max

    return n, F