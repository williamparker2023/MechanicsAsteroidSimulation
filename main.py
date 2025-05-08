import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Constants
G = 6.6743e-11
M = 1.9891e30
R_initial = 149597871000
dt = 60 * 60
skip_frames = 24 * 7

c = 2.998e8
asteroidRadius = 100  # meters
asteroidDensity = 2630  # kg/m^3
m = (4/3) * math.pi * (asteroidRadius)**3 * asteroidDensity
A = math.pi * asteroidRadius**2
a = 1
L = 3.828e26
lamb = (L*A*(1+a)) / (4 * math.pi * m * 299792458) - G*M

orbit_count = 0
prev_angle = None
pause_frames = 90  # e.g. 3 seconds at 30 FPS
pause_counter = 0

# Initial conditions
x1, y1 = 149597871000, 0.0
vx1, vy1 = -8000.0, 29789.8
x2, y2 = 149597871000, 0.0
vx2, vy2 = -8000.0, 29789.8

# Set up figure
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_xlim(-5e11, 5e11)
ax.set_ylim(-5e11, 5e11)
ax.set_aspect('equal')
ax.set_title("Photon Pressure on Spray Painted Asteroid", color='white')

ax.plot(0, 0, 'yo', markersize=12)

asteroid1, = ax.plot([], [], 'ro', markersize=6)
trail1, = ax.plot([], [], 'r-', linewidth=1)
asteroid2, = ax.plot([], [], 'go', markersize=6)
trail2, = ax.plot([], [], 'g-', linewidth=1)

radius_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, color='white', fontsize=10, ha='left', va='top')
mass_text = ax.text(0.05, 0.90, '', transform=ax.transAxes, color='white', fontsize=10, ha='left', va='top')
iradius_text = ax.text(0.05, 0.85, '', transform=ax.transAxes, color='white', fontsize=10, ha='left', va='top')
time_text = ax.text(0.05, 0.80, '', transform=ax.transAxes, color='white', fontsize=10, ha='left', va='top')

x_data1, y_data1 = [], []
x_data2, y_data2 = [], []

def physics_step():
    global x1, y1, vx1, vy1, x2, y2, vx2, vy2

    r1 = np.sqrt(x1**2 + y1**2)
    ax1 = -G * M * x1 / r1**3
    ay1 = -G * M * y1 / r1**3
    vx1 += ax1 * dt
    vy1 += ay1 * dt
    x1 += vx1 * dt
    y1 += vy1 * dt

    r2 = np.sqrt(x2**2 + y2**2)
    a_solar = (L * (1 + a) * A) / (4 * math.pi * m * c * r2**2)
    ax2 = (-G * M * x2 / r2**3) + (a_solar * x2 / r2)
    ay2 = (-G * M * y2 / r2**3) + (a_solar * y2 / r2)
    vx2 += ax2 * dt
    vy2 += ay2 * dt
    x2 += vx2 * dt
    y2 += vy2 * dt

    radius_text.set_text(f"Distance from Normal Orbit: {(r2-r1)/1000:.2f} km\n")
    mass_text.set_text(f"Mass: {m:.2e} kg\n")
    iradius_text.set_text(f"Radius: {asteroidRadius} m\n")

def update(frame):
    global orbit_count, prev_angle, pause_counter

    if orbit_count < 10:
        for _ in range(skip_frames):
            physics_step()
    else:
        pause_counter += 1
        if pause_counter >= pause_frames:
            ani.event_source.stop()

    x_data1.append(x1)
    y_data1.append(y1)
    asteroid1.set_data([x1], [y1])
    trail1.set_data(x_data1, y_data1)

    x_data2.append(x2)
    y_data2.append(y2)
    asteroid2.set_data([x2], [y2])
    trail2.set_data(x_data2, y_data2)

    elapsed_days = frame * dt / (60 * 60 * 24) * skip_frames
    elapsed_years = elapsed_days / 365.25
    time_text.set_text(f"Time Elapsed: {elapsed_years:.2f} years\n")

    angle = math.atan2(y1, x1)

    if prev_angle is not None:
        if prev_angle < 0 and angle >= 0:
            orbit_count += 1

    prev_angle = angle

    return asteroid1, trail1, asteroid2, trail2, radius_text, mass_text, iradius_text, time_text

ani = FuncAnimation(
    fig, update, frames=1000,
    init_func=lambda: (asteroid1, trail1, asteroid2, trail2, radius_text, mass_text, iradius_text, time_text),
    blit=True, interval=1
)

ani.save("asteroid_simulation_ellipse2.gif", writer=PillowWriter(fps=30))
plt.show()
