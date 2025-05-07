import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G = 6.6743e-11
M = 1.9891e30
R_initial = 149597871000
dt = 60 * 60 * 24
skip_frames = 7

c = 2.998e8
asteroidRadius = 10 #meters
asteroidDensity = 2630 #kg/m^3 (same as dinosaur killing asteroid)
m = (4/3) * math.pi * (asteroidRadius)**3 * asteroidDensity   #asteroid mass
A = math.pi * asteroidRadius**2   # surface area of paint
a = 1   # albedo
L = 3.828e26   # solar constant 
lamb = (L*A*(1+a)) / (4 * math.pi * m * 299792458) - G*M

orbit_count = 0
prev_angle = None


# Initial conditions
x1, y1 = 149597871000, 0.0
vx1, vy1 = 0.0, 29789.8

x2, y2 = 149597871000, 0.0
vx2, vy2 = 0.0, 29789.8

# Set up figure
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_xlim(-5e11, 5e11)
ax.set_ylim(-5e11, 5e11)
ax.set_aspect('equal')
ax.set_title("Photon Pressure on Spray Painted Asteroid", color='white')

# Plot the Sun
ax.plot(0, 0, 'yo', markersize=12)

# Asteroid plot objects
asteroid1, = ax.plot([], [], 'ro', markersize=6)
trail1, = ax.plot([], [], 'r-', linewidth=1)

asteroid2, = ax.plot([], [], 'go', markersize=6)
trail2, = ax.plot([], [], 'g-', linewidth=1)

# Radius label (for asteroid 1)
radius_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, color='white', fontsize=10, ha='left', va='top')
info_text = ax.text(0.05, 0.90, '', transform=ax.transAxes, color='white', fontsize=10, ha='left', va='top')
time_text = ax.text(0.05, 0.85, '', transform=ax.transAxes, color='white', fontsize=10, ha='left', va='top')



# Trail data
x_data1, y_data1 = [], []
x_data2, y_data2 = [], []

def physics_step():
    global x1, y1, vx1, vy1, x2, y2, vx2, vy2

    # Asteroid 1 (gravitational only)
    r1 = np.sqrt(x1**2 + y1**2)
    ax1 = -G * M * x1 / r1**3
    ay1 = -G * M * y1 / r1**3
    vx1 += ax1 * dt
    vy1 += ay1 * dt
    x1 += vx1 * dt
    y1 += vy1 * dt

    # Asteroid 2 (gravitational + solar radiation pressure)
    r2 = np.sqrt(x2**2 + y2**2)
    # Solar pressure acceleration (radial outward from Sun)
    a_solar = (L * (1 + a) * A) / (4 * math.pi * m * c * r2**2)
    # Direction vector from Sun to asteroid
    ax2 = (-G * M * x2 / r2**3) + (a_solar * x2 / r2)
    ay2 = (-G * M * y2 / r2**3) + (a_solar * y2 / r2)
    vx2 += ax2 * dt
    vy2 += ay2 * dt
    x2 += vx2 * dt
    y2 += vy2 * dt

    radius_text.set_text(f"Distance from Normal Orbit: {(r2-r1)/1000:.2f} km")
    info_text.set_text(f"Mass: {m:.2e} kg\nRadius: {asteroidRadius} m")


# Animation frame update
def update(frame):
    global orbit_count, prev_angle

    for _ in range(skip_frames):
        physics_step()

    # Update visuals
    x_data1.append(x1)
    y_data1.append(y1)
    asteroid1.set_data([x1], [y1])
    trail1.set_data(x_data1, y_data1)

    x_data2.append(x2)
    y_data2.append(y2)
    asteroid2.set_data([x2], [y2])
    trail2.set_data(x_data2, y_data2)

    # Time text
    elapsed_days = frame * dt / (60 * 60 * 24) * skip_frames
    elapsed_years = elapsed_days / 365.25
    time_text.set_text(f"Time Elapsed: {elapsed_years:.2f} years")

    # Orbit counting logic (detect when angle crosses 0)
    angle = math.atan2(y1, x1)  # Get angle of asteroid 1 relative to the Sun

    # Check if the angle has passed through 0 (completing a full orbit)
    if prev_angle is not None:
        # Check for full rotation (angle passed from +pi to -pi or vice versa)
        if prev_angle < 0 and angle >= 0:
            orbit_count += 1

    prev_angle = angle

    # Stop after 10 orbits
    if orbit_count >= 10:
        ani.event_source.stop()

    return asteroid1, trail1, asteroid2, trail2, radius_text, info_text, time_text



# Animate
ani = FuncAnimation(
    fig, update, frames=1000,
    init_func=lambda: (asteroid1, trail1, asteroid2, trail2, radius_text, info_text, time_text),
    blit=True, interval=5
)

plt.show()
