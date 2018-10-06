# Program for computing the height of a ball in vertical motion
# sec. 1.2.1, page 5
# http://hplgit.github.io/prog4comp/doc/pub/p4c-sphinx-Python/._pylight002.html#a-python-program-with-variables

v0 = 5             # Initial velocity
g = 9.81           # Acceleration of gravity
t = 0.6            # Time

y = v0*t - 0.5*g*t**2        # Vertical position

print(y)            ### print y
