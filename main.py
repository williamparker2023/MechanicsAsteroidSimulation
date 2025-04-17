import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G = 6.6743e-11
M = 1.9891e30
dt = 60 * 60 * 24
skip_frames = 10 

# Initial conditions
x1, y1 = 149597871000, 0.0
r0 = 149597871000
vx1, vy1 = 0.0, 29784.8

x2, y2 = 149597871000, 0.0
vx2, vy2 = 0.0, 29784.8

# Set up figure
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_xlim(-1.2e12, 1.2e12)
ax.set_ylim(-1.2e12, 1.2e12)
ax.set_aspect('equal')
ax.set_title("Two Asteroids Orbiting the Sun", color='white')

# Plot the Sun
ax.plot(0, 0, 'yo', markersize=12)

# Asteroid plot objects
asteroid1, = ax.plot([], [], 'ro', markersize=6)
trail1, = ax.plot([], [], 'r-', linewidth=1)

asteroid2, = ax.plot([], [], 'go', markersize=6)
trail2, = ax.plot([], [], 'g-', linewidth=1)

# Trail data
x_data1, y_data1 = [], []
x_data2, y_data2 = [], []

def physics_step():
    global x1, y1, vx1, vy1, x2, y2, vx2, vy2

    # Asteroid 1
    r1 = np.sqrt(x1**2 + y1**2)
    ax1 = -G * M * x1 / r1**3
    ay1 = -G * M * y1 / r1**3
    vx1 += ax1 * dt
    vy1 += ay1 * dt
    x1 += vx1 * dt
    y1 += vy1 * dt

    # Asteroid 2
    r2 = np.sqrt(x2**2 + y2**2)
    ax2 = -G * M * x2 / r2**3 + 1.3e8 * x2 / r2**2
    ay2 = -G * M * y2 / r2**3 + 1.3e8 * y2 / r2**2
    vx2 += ax2 * dt
    vy2 += ay2 * dt
    #x2 += vx2 * dt
    #y2 += vy2 * dt
    


# Animation frame update
def update(frame):
    for _ in range(skip_frames):  # Simulate N frames before rendering
        physics_step()

    x_data1.append(x1)
    y_data1.append(y1)
    asteroid1.set_data([x1], [y1])
    trail1.set_data(x_data1, y_data1)

    x_data2.append(x2)
    y_data2.append(y2)
    asteroid2.set_data([x2], [y2])
    trail2.set_data(x_data2, y_data2)

    return asteroid1, trail1, asteroid2, trail2

# Animate
ani = FuncAnimation(fig, update, frames=1000, init_func=lambda: (asteroid1, trail1, asteroid2, trail2), blit=True, interval=1)
plt.show()
