import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
# Import the Fortran module
import Advection_One_Dim as Numerical_Scheme 

# Define simulation parameters 
dt = 0.01          #s time step
dx = 0.5            #m spatial resolution
x_dim = 200          #Model gridpoints 
# Domain
x_w = - 15
x_e = 15 
x = np.linspace(x_w, x_e, x_dim)
# Stop time
t_stop = 10 # s


# Initialize target variable
C = np.zeros(x_dim) 

## CHOICES OF INITIAL CONDITIONS 
#C[6:9] = 1 # Step function
C[1:200] = np.random.random(200-1) # Pulse of random values

# Initilize wind distribution
u = np.zeros(x_dim)
u = [1 - 1/(1 + x**2) if x >= 0 else 0 for x in x] 

# Prepare the animation plot
fig, ax = plt.subplots() 
line, = ax.plot([],[], lw=2, label='C') 
text = ax.text(0.20, 0.95, '', horizontalalignment='center',
        verticalalignment='center', transform = ax.transAxes)
FONTSIZE = 16 # Plot fontsizes
animation_interval = 0 # Go as fast as possible

# Plot the wind distribution
ax.plot(x, u, label='Wind distribution')

def Init():
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(0, 1.2)
    ax.set_xlabel("x-axis position [m]", fontsize=FONTSIZE)
    ax.set_ylabel("C", fontsize=FONTSIZE)
    ax.set_title("One-dimensional advection simulation", fontsize=FONTSIZE) 
    ax.legend(loc='upper right')
    return line,

def Run(i): 
    global C 
    # Call the Fortran numerical scheme to get the next time step distribution
    C = Numerical_Scheme.step_advection(dx, dt, u, C) 
    # Update animation plot data
    line.set_data(x, C) 

    # Every 50:th iteration 
    if (i % 50 == 0):
        text.set_text('Current time: ' + str(dt*i*1000) + ' ms')
        # Stop if zero values in simulation window
        if (dt * i > t_stop):
            ani.event_source.stop()

    return line, text

ani = animation.FuncAnimation(fig, Run, frames=10**100,
        interval=animation_interval, blit=True, init_func=Init)
plt.show() 