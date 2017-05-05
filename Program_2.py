import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numerical_schemes

""" Define simulation parameters """
dt = 0.1            # s time step
dx = 0.5            # m spatial resolution
# Domain
x_w = - 15
x_e = 15

""" Initialize, dimensions, coordinates and variables """
x_dim = int((x_e - x_w)//dx)
C = np.zeros(x_dim, order='F')
x = np.linspace(x_w, x_e, x_dim)
u = np.zeros(x_dim,order='F')

""" choices of initial conditions """
C[x_dim//2:x_dim//2+10] = 1 # Step function
#C = np.random.random(x_dim) # Pulse of random values
# Wind distribution
u = [1 - 1/(1 + x**2) if x >= 0 else 0 for x in x]

""" Prepare the animation plot """
fig, ax = plt.subplots()
line, = ax.plot([],[], lw=2, label='C')
text = ax.text(0.20, 0.95, '', horizontalalignment='center',
        verticalalignment='center', transform = ax.transAxes)
FONTSIZE = 16 # Plot fontsizes
animation_interval = 0 # Go as fast as possible
# Plot the wind distribution
ax.plot(x, u, label='Wind distribution')

def Init():
    ax.set_xlim(x_w, x_e)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel("x-axis position [m]", fontsize=FONTSIZE)
    ax.set_ylabel("C", fontsize=FONTSIZE)
    ax.set_title("One-dimensional advection simulation", fontsize=FONTSIZE)
    ax.legend(loc='upper right')
    line.set_data(x, C)
    return line,

""" Simulation """
def Run(i):
    global C
    C = numerical_schemes.step_ftbs(dx, dt, u, C)
    line.set_data(x, C)
    text.set_text('Current time: ' + str(int(dt*i)) + ' s')
    return line, text

ani = animation.FuncAnimation(fig, Run, frames=10**100,
        interval=animation_interval, blit=True, init_func=Init)
plt.show()
