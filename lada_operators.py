from numpy import linspace, exp, sqrt, cos, e, pi
from numpy import meshgrid
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# The Ackley Function


def ackley(x, y):
    a, b, c = 20.0, 0.2, 2 * pi

    return (
        -a * exp(-b * sqrt(0.5 * (x**2 + y**2)))
        - exp(0.5 * (cos(c * x) + cos(c * y)))
        + e
        + 20
    )


r_bounds = -32.768, 32.768

xaxis = linspace(*r_bounds, 150)
yaxis = linspace(*r_bounds, 150)
x, y = meshgrid(xaxis, yaxis)
z = ackley(x, y)

figure = plt.figure()
axis = plt.axes(projection="3d")
axis.contour3D(x, y, z, 80, cmap="hot")

axis.set_xlabel("x")
axis.set_ylabel("y")
axis.set_zlabel("z")

plt.show()
