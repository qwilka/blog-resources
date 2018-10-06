# sec. 1.4, page 11
# http://hplgit.github.io/prog4comp/doc/pub/p4c-sphinx-Python/._pylight002.html#a-python-program-with-vectorization-and-plotting
from numpy import linspace

v0 = 5
g = 9.81
t = linspace(0, 1, 1001)

y = v0*t - 0.5*g*t**2

import matplotlib.pyplot as plt
plt.plot(t, y)
plt.xlabel('t (s)')
plt.ylabel('y (m)')
plt.show()
