import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
G = 6.67430e-11  # gravitational constant in m^3 kg^-1 s^-2
M_sun = 1.989e30  # mass of the Sun in kg
dt = 86400  # time step in seconds (1 day)
m_mars = 6.4171e23
m_earth = 5.97219e24
m_halley = 2.2e14

# Initial conditions at 1985-Jan-01 00:00:00.0000 TDB
# Position vector (x, y, z) in meters
r_mars = np.array([2.063912153671112E+11, 3.863440991132106E+10, -4.315752342443038E+09])
r_earth = np.array([-2.739967871190767E+10,  1.458701315273963E+11, -1.190579976484925E+07])
r_halley = np.array([5.157148272046394E+09,  7.807237634620279E+11, -1.276650673647241E+11])
# Velocity vector (vx, vy, vz) in meters per second
v_mars = np.array([-3.386014196397585E+03, 2.590498514527732E+04, 6.259094874285172E+02])
v_earth = np.array([-2.976221215759604E+04, -5.672803560198480E+03, -9.085689680690123E-01])
v_halley = np.array([5.737671459695651E+03, -1.538682030308552E+04, 4.123355639302506E+03])

# Function to compute the gravitational force on Mars by the Sun
def gravitational_force(r, m):
    r_mag = np.linalg.norm(r)  # magnitude of the position vector
    force_mag = G * M_sun * m / r_mag**2  # magnitude of the gravitational force
    force_dir = -r / r_mag  # direction of the force (towards the Sun)
    return force_mag * force_dir

# Simulation for 365 days
positions_mars = []  # list to store positions for plotting
positions_earth = []
positions_halley = []

for day in range(1000):
    # Update the force, velocity, and position
    force = gravitational_force(r_mars, m_mars)
    v_mars += (force / m_mars) * dt  # update velocity
    r_mars += v_mars * dt  # update position
    positions_mars.append(r_mars.copy())  # store the new position

    force = gravitational_force(r_earth, m_earth)
    v_earth += (force / m_earth) * dt  # update velocity
    r_earth += v_earth * dt  # update position
    positions_earth.append(r_earth.copy())  # store the new position

    force = gravitational_force(r_halley, m_halley)
    v_halley += (force / m_halley) * dt  # update velocity
    r_halley += v_halley * dt  # update position
    positions_halley.append(r_halley.copy())  # store the new position

# Convert list to numpy array for easy handling
positions_mars = np.array(positions_mars)
positions_earth = np.array(positions_earth)
positions_halley = np.array(positions_halley)

# Creating the figure and setting up the plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-4e11, 4e11)
ax.set_ylim(-4e11, 4e11)
ax.scatter([0], [0], color='yellow', s=100, label='Sun')  # Sun at the origin
line_mars, = ax.plot([], [], 'b-', label='Orbit of Mars')  # Line plot for the trajectory
dot_mars, = ax.plot([], [], 'ro', label='Mars')  # Red dot to represent Mars
line_earth, = ax.plot([], [], 'g-', label='Orbit of Earth')  # Line plot for the trajectory
dot_earth, = ax.plot([], [], 'bo', label='Earth')
line_halley, = ax.plot([], [], 'r-', label='Orbit of Halley')  # Line plot for the trajectory
dot_halley, = ax.plot([], [], 'go', label='Halley')


def init():
    line_mars.set_data([], [])
    dot_mars.set_data([], [])
    line_earth.set_data([], [])
    dot_earth.set_data([], [])
    line_halley.set_data([], [])
    dot_halley.set_data([], [])
    return line_mars, dot_mars, line_earth, dot_earth, line_halley, dot_halley

def animate(i):

    x = positions_mars[:i, 0]
    y = positions_mars[:i, 1]
    if i == 0:
        dot_mars.set_data(r_mars[0], r_mars[1])
    else:
        dot_mars.set_data(x[-1], y[-1])  # Update Mars' position
    line_mars.set_data(x, y)

    x = positions_earth[:i, 0]
    y = positions_earth[:i, 1]
    if i == 0:
        dot_earth.set_data(r_earth[0], r_earth[1])
    else:
        dot_earth.set_data(x[-1], y[-1])  # Update Earths position
    line_earth.set_data(x, y)

    x = positions_halley[:i, 0]
    y = positions_halley[:i, 1]
    if i == 0:
        dot_halley.set_data(r_halley[0], r_halley[1])
    else:
        dot_halley.set_data(x[-1], y[-1])  # Update Halley's position
    line_halley.set_data(x, y)

    return line_mars, dot_mars, line_earth, dot_earth, line_halley, dot_halley

# Creating the animation
ani_mars = animation.FuncAnimation(fig, animate, frames=len(positions_mars), init_func=init,
                              interval=25, blit=True)


plt.title("Heliocentric Orbit of Mars (Animated)")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.legend()
plt.grid(True)
plt.axis('equal')

# Show the animation
plt.show()
