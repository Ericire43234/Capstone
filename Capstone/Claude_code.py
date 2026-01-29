import numpy as np
import matplotlib.pyplot as plt # type: ignore
from CM_Functions import *
import pandas as pd

def calculation_single_beam(E=0.2e6, Sy=4e3):
    """Calculate properties for a single fixed-guided beam"""
    l = mm2in(11)
    w = mm2in(5.75)
    h = mm2in(1)
    b_total = mm2in(2.44)
    phi = 90

    n = -1/np.tan(np.radians(phi))
    eta = np.sqrt(1+n**2)
    y = gamma(n)
    K_theta = Ktheta(n)

    I = w*h**3/12
    A = w*h
    K = 2*y*K_theta*E*I/l
    
    b = b_total/2
    theta = np.arcsin(b/(y*l))
    P = K*theta/(eta*y*l*np.sin(np.radians(phi) - theta))
    F = P*eta
    a = l*(1 - y*(1 - np.cos(theta)))
    c = h/2
    
    stress_max = abs((P*(a + n*b)*c)/I) - (n*P)/A
    safety_factor = Sy/stress_max

    return {
        'safety_factor': safety_factor,
        'force': F,
        'stiffness': K,
        'stress_max': stress_max,
        'deflection': b_total,
        'length': l
    }

def calculation_series_beams(N_beams, E=0.2e6, Sy=4e3):
    """
    Calculate properties for N fixed-guided beams in SERIES (end-to-end)
    
    Series configuration:
    |====| → |====| → |====| → ... (chained end-to-end)
    
    Parameters:
    -----------
    N_beams : int
        Number of beams in series
    E : float
        Modulus of elasticity (psi)
    Sy : float
        Yield strength (psi)
    
    Returns:
    --------
    dict with:
        - safety_factor: same as single beam (all carry same force)
        - force: force through the chain (same for all beams)
        - total_stiffness: combined stiffness (softer)
        - total_deflection: sum of all deflections
        - stress_max: maximum stress (same in all beams)
    """
    # Get single beam properties
    single = calculation_single_beam(E, Sy)
    
    # Series combination (like springs in series)
    # 1/K_total = 1/K1 + 1/K2 + ... + 1/KN = N/K_single
    # Therefore: K_total = K_single / N
    total_stiffness = single['stiffness'] / N_beams
    
    # Same force through all beams in series
    force = single['force']
    
    # Deflections add up
    total_deflection = N_beams * single['deflection']
    
    # Total length is N times single beam length
    total_length = N_beams * single['length']
    
    # Stress is the same in each beam (they all carry the same force)
    # Safety factor is the same as single beam
    
    return {
        'N_beams': N_beams,
        'safety_factor': single['safety_factor'],
        'force': force,
        'total_stiffness': total_stiffness,
        'total_deflection': total_deflection,
        'total_length': total_length,
        'stress_max': single['stress_max'],
        'deflection_per_beam': single['deflection'],
        'stiffness_per_beam': single['stiffness']
    }

# Example usage
if __name__ == "__main__":
    print("="*60)
    print("SINGLE FIXED-GUIDED BEAM")
    print("="*60)
    single = calculation_single_beam()
    print(f"Safety Factor: {single['safety_factor']:.3f}")
    print(f"Force: {single['force']:.3f} lbf")
    print(f"Stiffness: {single['stiffness']:.3f} lb·in/rad")
    print(f"Deflection: {single['deflection']:.4f} in ({single['deflection']*25.4:.3f} mm)")
    print(f"Max Stress: {single['stress_max']:.1f} psi")
    print(f"Length: {single['length']:.4f} in ({single['length']*25.4:.3f} mm)")
    
    # Calculate spring rate (force per unit deflection)
    spring_rate_single = single['force'] / single['deflection']
    print(f"Spring Rate: {spring_rate_single:.2f} lbf/in")
    
    print("\n" + "="*60)
    print("SERIES BEAM SPRING (10 beams end-to-end)")
    print("="*60)
    series = calculation_series_beams(N_beams=10)
    print(f"Number of Beams: {series['N_beams']}")
    print(f"Safety Factor: {series['safety_factor']:.3f}")
    print(f"Force: {series['force']:.3f} lbf")
    print(f"Total Stiffness: {series['total_stiffness']:.3f} lb·in/rad")
    print(f"Total Deflection: {series['total_deflection']:.4f} in ({series['total_deflection']*25.4:.3f} mm)")
    print(f"Total Length: {series['total_length']:.4f} in ({series['total_length']*25.4:.3f} mm)")
    print(f"Max Stress (per beam): {series['stress_max']:.1f} psi")
    
    # Calculate spring rate for series configuration
    spring_rate_series = series['force'] / series['total_deflection']
    print(f"Spring Rate: {spring_rate_series:.2f} lbf/in")
    
    print("\n" + "="*60)
    print("COMPARISON")
    print("="*60)
    print(f"Single beam spring rate: {spring_rate_single:.2f} lbf/in")
    print(f"Series spring rate: {spring_rate_series:.2f} lbf/in")
    print(f"Series spring is {series['N_beams']}x SOFTER (spring rate is 1/{series['N_beams']} of single beam)")
    print(f"Series spring deflects {series['N_beams']}x MORE for the same force")
    print(f"\nFor the same force:")
    print(f"  Single beam: {single['deflection']*25.4:.3f} mm deflection")
    print(f"  Series chain: {series['total_deflection']*25.4:.3f} mm deflection")