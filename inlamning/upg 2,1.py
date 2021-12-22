import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math


def fit(x, y):
    e = math.e

    z0 = x ** 2 + y ** 2
    z1 = e ** (-0.05 * z0)

    z2 = np.arctan(x) - np.arctan(y)
    z3 = e ** -z0
    z4 = (np.cos(x) ** 2) * (np.sin(y) ** 2)

    z5 = z2 + z3 * z4
    z6 = z1 * z5 * 2

    return z6


def fit_min(x, y):
    return fit(x, y)


x, y = np.array(np.meshgrid(np.linspace(-5, 5, 100), np.linspace(-5, 5, 100)))
z = fit_min(x, y)
x_min = x.ravel()[z.argmin()]
y_min = y.ravel()[z.argmin()]

# Hyper-parameter of the algorithm
c1 = c2 = 0.1
w = 0.8

# Create particles
n_particles = 20
np.random.seed(100)
X = np.random.rand(2, n_particles) * 10 - 5
V = np.random.randn(2, n_particles) * 0.1

# Initialize data
pbest = X
pbest_obj = fit(X[0], X[1])
gbest_min = pbest[:, pbest_obj.argmin()]
gbest_obj_min = pbest_obj.min()

gbest_max = pbest[:, pbest_obj.argmax()]
gbest_obj_max = pbest_obj.max()


def update(min):
    "Function to do one iteration of particle swarm optimization"
    global V, X, pbest, pbest_obj, gbest_min, gbest_obj_min, gbest_max, gbest_obj_max
    # Update params

    if min:
        r1, r2 = np.random.rand(2)
        V = w * V + c1 * r1 * (pbest - X) + c2 * r2 * (gbest_min.reshape(-1, 1) - X)
        X = X + V
        obj = fit(X[0], X[1])
        pbest[:, (pbest_obj >= obj)] = X[:, (pbest_obj >= obj)]
        pbest_obj = np.array([pbest_obj, obj]).min(axis=0)
        gbest_min = pbest[:, pbest_obj.argmin()]
        gbest_obj_min = pbest_obj.min()
    else:
        r1, r2 = np.random.rand(2)
        V = w * V + c1 * r1 * (pbest - X) + c2 * r2 * (gbest_max.reshape(-1, 1) - X)
        X = X + V
        obj = fit(X[0], X[1])
        pbest[:, (pbest_obj <= obj)] = X[:, (pbest_obj <= obj)]
        pbest_obj = np.array([pbest_obj, obj]).min(axis=0)
        gbest_max = pbest[:, pbest_obj.argmax()]
        gbest_obj_max = pbest_obj.max()


# Set up base figure: The contour map
fig, ax = plt.subplots(figsize=(8, 6))
fig.set_tight_layout(True)
img = ax.imshow(z, extent=[-5, 5, -5, 5], origin='lower', cmap='viridis', alpha=0.5)
fig.colorbar(img, ax=ax)
ax.plot([x_min], [y_min], marker='x', markersize=5, color="white")
contours = ax.contour(x, y, z, 10, colors='black', alpha=0.4)
ax.clabel(contours, inline=True, fontsize=8, fmt="%.0f")
pbest_plot = ax.scatter(pbest[0], pbest[1], marker='o', color='black', alpha=0.5)
p_plot = ax.scatter(X[0], X[1], marker='o', color='blue', alpha=0.5)
p_arrow = ax.quiver(X[0], X[1], V[0], V[1], color='blue', width=0.005, angles='xy', scale_units='xy', scale=1)
gbest_plot = plt.scatter([gbest_min[0]], [gbest_min[1]], marker='*', s=100, color='black', alpha=0.4)
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])


def animate(i):
    "Steps of PSO: algorithm update and show in plot"
    title = 'Iteration {:02d}'.format(i)
    # Update params
    update(min=True)
    # Set picture
    ax.set_title(title)
    pbest_plot.set_offsets(pbest.T)
    p_plot.set_offsets(X.T)
    p_arrow.set_offsets(X.T)
    p_arrow.set_UVC(V[0], V[1])
    gbest_plot.set_offsets(gbest_min.reshape(1, -1))
    return ax, pbest_plot, p_plot, p_arrow, gbest_plot


anim = FuncAnimation(fig, animate, frames=list(range(1, 50)), interval=500, blit=False, repeat=True)
anim.save("PSO_min.gif", dpi=120, writer="imagemagick")

print("PSO found best solution at f({})={}".format(gbest_min, gbest_obj_max))
print("Global optimal at f({})={}".format([x_min, y_min], fit_min(x_min, y_min)))


def animate(i):
    "Steps of PSO: algorithm update and show in plot"
    title = 'Iteration {:02d}'.format(i)
    # Update params
    update(min=False)
    # Set picture
    ax.set_title(title)
    pbest_plot.set_offsets(pbest.T)
    p_plot.set_offsets(X.T)
    p_arrow.set_offsets(X.T)
    p_arrow.set_UVC(V[0], V[1])
    gbest_plot.set_offsets(gbest_max.reshape(1, -1))
    return ax, pbest_plot, p_plot, p_arrow, gbest_plot


anim = FuncAnimation(fig, animate, frames=list(range(1, 50)), interval=500, blit=False, repeat=True)
anim.save("PSO_max.gif", dpi=120, writer="imagemagick")

print("PSO found best solution at f({})={}".format(gbest_max, gbest_obj_max))
print("Global optimal at f({})={}".format([x_min, y_min], fit_min(x_min, y_min)))
