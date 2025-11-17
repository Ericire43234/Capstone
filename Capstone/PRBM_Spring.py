
import numpy as np
import matplotlib.pyplot as plt # type: ignore


# %% 

# -- Inputs (dimensions, number of springs, total deflection required)
b = 1
h = 1
l = 14
y = 0.85
E = 0.2e6
Sy = 4e3

# %% Outputs (E, smax)

"""
Instead of trying to model each individual beam, we thought about finding the fraction of displacement for each subset of beams.
The spring can be modeled as a fixed-guided beam (in essence fixed-fixed)
"""