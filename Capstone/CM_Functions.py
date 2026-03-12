"""
Utility functions for compliant mechanism calculations.

These functions implement curve fits and tabulated values from:

    Howell, L. L. - "Compliant Mechanisms"

They return empirical coefficients used in large-deflection beam
analysis for compliant mechanisms.

Functions
---------
gamma(n)
    Howell coefficient y(n) used in beam deflection relations.

Ktheta(n)
    Rotational stiffness coefficient Kθ(n).

ctheta(n)
    Empirical correction factor relating θ and θ₀.

mm2in(mm)
    Unit conversion from millimeters to inches.

in2mm(inch)
    Unit conversion from inches to millimeters.
"""

import numpy as np

def gamma(n_num):
    """
    Howell gamma coefficient y(n).

    This coefficient appears in the large-deflection analysis of
    compliant beams and is used to relate beam deflection to rotation.

    The function implements piecewise curve fits given in
        Howell, L. L. - "Compliant Mechanisms" (Eq. 5.48).

    Parameters
    ----------
    n_num : float
        Dimensionless beam parameter defined as:

            n = -1 / tan(phi)

        where phi is the beam tip rotation angle.

    Returns
    -------
    y : float
        Gamma coefficient y(n).

    Valid Range
    -----------
    -5 < n < 10
    """

    if n_num<10 and n_num>.5:
        y=.841655-.0067807*n_num+.000438*n_num**2   #5.48
    elif n_num<.5 and n_num>-1.8316:
        y=.852144-0.0182867*n_num             
    elif n_num<-1.8316 and n_num>-5:
        y=.912364+.0145928*n_num
    return y  

def Ktheta(n):
    """
    Howell rotational stiffness coefficient Kθ(n).

    This coefficient modifies the stiffness of a compliant beam
    undergoing large deflections.

    The function uses polynomial curve fits based on tabulated
    data from 
        Howell, L. L. - "Compliant Mechanisms"

    Parameters
    ----------
    n : float
        Dimensionless beam parameter:

            n = -1 / tan(phi)

    Returns
    -------
    K_theta : float
        Dimensionless stiffness coefficient.

    Valid Range
    -----------
    -5 < n < 10
    """

    if n>-5 and n<=-2.5:
        K_theta=3.024112 + 0.121290*n+.0031696*n**2
    elif n>-2.5 and n<=-1:
        K_theta=1.967647-2.616021*n-3.738166*n**2-2.649437*n**3-.891906*n**4-.113063*n**5
    elif n>-1 and n<=10:
        K_theta=2.654855-.509896*10**-1*n+.126749*10**-1*n**2-.142039*10**-2*n**3+.584525*10**-4*n**4
    return K_theta

def ctheta(n):
    """
    Empirical correction factor relating θ₀ and θ.

    In Howell's compliant beam formulation:

        θ₀ = c(n) * θ

    where θ is the beam rotation and θ₀ is the corrected
    rotation used in stress calculations.

    Parameters
    ----------
    n : float
        Dimensionless beam parameter:

            n = -1 / tan(phi)

    Returns
    -------
    c : float
        Dimensionless correction factor c(n).

    Notes
    -----
    Values are taken from tabulated data in Howell's
    "Compliant Mechanisms" and implemented here as
    piecewise constant approximations.
    """ 

    # Tabulated Howell values
    n_vals = np.array([
        -5, -4, -3, -2, -1.5, -1, -0.5, 0,
        0.5, 1, 1.5, 2, 3, 4, 5, 7.5, 10
    ])

    c_vals = np.array([
        1.1788, 1.1971, 1.2119, 1.2293, 1.2322, 1.2323, 1.2348, 1.2385,
        1.2430, 1.2467, 1.2492, 1.2511, 1.2534, 1.2548, 1.2557, 1.2570, 1.2578
    ])

    return np.interp(n, n_vals, c_vals)

def mm2in(mm):
    """
    Convert millimeters to inches.

    Parameters
    ----------
    mm : float
        Length in millimeters.

    Returns
    -------
    float
        Length in inches.
    """
    return mm / 25.4

def in2mm(inch):
    """
    Convert inches to millimeters.

    Parameters
    ----------
    inch : float
        Length in inches.

    Returns
    -------
    float
        Length in millimeters.
    """
    return inch * 25.4