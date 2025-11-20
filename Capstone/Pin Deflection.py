## Finding the geometry of the pin

# TODO look at this script again to try to fix any errors. Look at where I should use l and where I should use y*l

import numpy as np
import matplotlib.pyplot as plt # type: ignore

# --- Inputs ---
l = 18   # mm (beam length)
n_num = 3  # stiffness ratio
disp = 8.7

# --- Characteristic radius factor (Eq. 5.48 from Howell et al.) ---
if 0.5 < n_num < 10:
    y = 0.841655 - 0.0067807*n_num + 0.000438*(n_num**2)
elif -1.8316 < n_num < 0.5:
    y = 0.852144 - 0.0182867*n_num
elif -5 < n_num < 1.8316:
    y = 0.912364 + 0.0145928*n_num
else:
    raise ValueError("n_num is out of range for y correlation")

# Angle range (radians)
theta = np.radians(np.linspace(0, 77, 1000))
angle = np.arctan2(disp,y*l)

# --- PRBM equations for end coordinates ---
b = l * y * np.sin(theta)                         # vertical deflection
a = l * (1 - y * (1 - np.cos(theta)))             # horizontal displacement

b0 = l * y * np.sin(angle)                         # vertical deflection
a0 = l * (1 - y * (1 - np.cos(angle)))             # horizontal displacement

# --- Plot ---
plt.figure()
plt.plot(b,a, label='End of Beam Path', color='b')
plt.scatter(b0,a0, color='k')
plt.xlabel('b (mm) - horizontal')
plt.ylabel('a (mm) - vertical')
plt.grid(True)
# plt.ylim([0,18])
plt.legend()
plt.savefig('Estimated Deflection.png')
plt.show()

print(f"y (characteristic radius factor) = {y:.4f}")
