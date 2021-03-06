import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numerical_schemes

""" Define simulation parameters """
u = 1               # m/s
dt = 1/300          # s time step
dx = 0.1            # m spatial resolution
D = 1
# Domain
x_w = - 10
x_e = 10

""" Initialize dimensions, coordinates and variables """
x_dim = int((x_e - x_w)//dx)
x = np.linspace(x_w, x_e, x_dim)
C = np.zeros(x_dim,order='F')
u = np.ones(x_dim,order='F') * u # Constant wind speed

""" choices of initial conditions """
#C[6:9] = 1 # Step function
C = np.random.random(x_dim) # Pulse of random values

""" Prepare the animation plot """
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(x, u, label='Wind distribution', lw=2, color='C1')
line, = ax1.plot([],[], lw=2, label='Concentration C')
text = ax1.text(0.50, 0.90, '', horizontalalignment='center',
        verticalalignment='center', transform = ax1.transAxes)
FONTSIZE = 16 # Plot fontsizes
animation_interval = dt*10 * 100 # Realtime * 100

def Init():
    ax1.set_xlim(x[0], x[-1])
    ax1.set_ylim(0, 1.2)
    ax1.set_xlabel("x-axis position [m]", fontsize=FONTSIZE)
    ax1.set_ylabel("C", fontsize=FONTSIZE)
    ax1.set_title("One-dimensional advection simulation", fontsize=FONTSIZE)
    ax1.legend(loc='upper left')
    ax2.set_ylabel('Wind speed [m/s]',fontsize=FONTSIZE)
    ax2.legend(loc='upper right')
    line.set_data(x, C)
    return line,

""" Simulation """
def Run(i):
    global C
    C = numerical_schemes.step_ftbs_diffusion(dx, dt, u, D, C)
    line.set_data(x, C)
    text.set_text('Current time: ' + str(int(dt*i)) + ' s')
    return line, text

ani = animation.FuncAnimation(fig, Run, frames=10**100,
        interval=animation_interval, blit=True, init_func=Init)
plt.show()
