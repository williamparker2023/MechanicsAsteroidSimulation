import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G = 6.6743e-11
M = 1.9891e30
dt = 60*60*72

# Initial conditions
x1 = 149597871000
y1 = 0.0
vx1 = 0.0
vy1 = 33784.8

x2 = 149597871000 
y2 = 0.0
vx2 = 0.0
vy2 = 33784.8

# Set up figure
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_xlim(-1000000000000, 1000000000000)
ax.set_ylim(-1000000000000, 1000000000000)
ax.set_aspect('equal')
ax.set_title("Two Asteroids Orbiting the Sun", color='white')

# Plot the Sun
ax.plot(0, 0, 'yo', markersize=12)  # Yellow sun

# Create asteroid and trail objects
asteroid1, = ax.plot([], [], 'ro', markersize=6)  # Red asteroid
trail1, = ax.plot([], [], 'r-', linewidth=1)      # Red trail
asteroid2, = ax.plot([], [], 'go', markersize=6)  # Red asteroid
trail2, = ax.plot([], [], 'g-', linewidth=1)      # Red trail

# Store trail points
x_data1, y_data1 = [], []
x_data2, y_data2 = [], []

def init():
    asteroid1.set_data([], [])
    trail1.set_data([], [])
    asteroid2.set_data([], [])
    trail2.set_data([], [])
    return asteroid1, trail1, asteroid2, trail2

def update(frame):
    global x1, y1, vx1, vy1, x2, y2, vx2, vy2

    #asteroid 1
    r1 = np.sqrt(x1**2 + y1**2)
    ax_acc1 = -G * M * x1 / r1**3
    ay_acc1 = -G * M * y1 / r1**3

    vx1 += ax_acc1 * dt
    vy1 += ay_acc1 * dt
    x1 += vx1 * dt
    y1 += vy1 * dt

    x_data1.append(x1)
    y_data1.append(y1)

    asteroid1.set_data([x1], [y1])  # <- wrapped in lists now
    trail1.set_data(x_data1, y_data1)


    #asteroid 2
    r2 = np.sqrt(x2**2 + y2**2)
    acc_factor = .8
    ax_acc2 = -G * M * x2 / r2**3 * acc_factor
    ay_acc2 = -G * M * y2 / r2**3 * acc_factor

    vx2 += ax_acc2 * dt
    vy2 += ay_acc2 * dt
    x2 += vx2 * dt
    y2 += vy2 * dt

    x_data2.append(x2)
    y_data2.append(y2)
    asteroid2.set_data([x2], [y2])
    trail2.set_data(x_data2, y_data2)

    return asteroid1, trail1, asteroid2, trail2

ani = FuncAnimation(fig, update, frames=5000, init_func=init, blit=True, interval=10)
plt.show()
