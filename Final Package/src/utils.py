"""
Utility functions for compliant mechanism calculations.

Functions
---------
mm2in(mm)
    Unit conversion from millimeters to inches.

in2mm(inch)
    Unit conversion from inches to millimeters.
"""

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