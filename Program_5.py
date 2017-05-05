import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
from scipy.stats import norm
import types
# Import the Fortran module
import numerical_schemes
import matplotlib.cm as cm

########
# Define simulation parameters 
dt = 1.0          #s time step
dx = 10           #m spatial resolution
dy = 10
x_dim = 201         #Model gridpoints (use odd number for symmetry)
y_dim = 201
u_max = 5 # m/s
v_max = 5 # m/s
# Domain
x_w = - 10 # m
x_e = 10 
y_s = - 10
y_n = 10
x = np.linspace(x_w, x_e, x_dim)
y = np.linspace(y_s, y_n, y_dim)
X, Y = np.meshgrid(x, y) 

########
# Initialize wind field (low pressure system northern hemesphere) 
u = np.zeros([x_dim, y_dim], order='F')
v = np.zeros([x_dim, y_dim], order='F')
Ux, Uy = np.meshgrid(np.linspace(-1, 0, x_dim), np.linspace(-1, 0, y_dim)) 
u[:,:] = np.sin(np.pi * Ux) * np.cos(np.pi * Uy) * u_max
v[:,:] = -np.cos(np.pi * Ux) * np.sin(np.pi * Uy) * v_max 
#plt.quiver(X[::30,::30], Y[::30,::30],u[::30,::30],v[::30,::30])

#########
# Initialize the initial distribution of concentration of C 
C = np.zeros([x_dim, y_dim, 2],order='F') 
mean = [7, 0]  # Location of "blob"
std = [1, 1]    # Size of blob
cx = norm.pdf((x - mean[1])/std[1])*10
cy = norm.pdf((y - mean[0])/std[0])*10 

#########
# Initial and first step
C[:,:,0] = np.outer(cx, cy) 
C[:,:,1] = numerical_schemes.step_upwind(dx, dy, dt, v, u, C[:,:,0])
#########
# Prepare the animation plot
fig, ax = plt.subplots()
#cax = ax.imshow(C[:,:,1], interpolation='nearest', cmap=cm.viridis) 
cf = ax.contourf(C[:,:,0], np.arange(-0, 1, 0.1), extend='both', cmap=cm.viridis) 
plt.colorbar(cf)


def Run(i): 
    global C 
    #C[:,:,1] = numerical_schemes.step_upwind(dx, dy, dt, u, v, C[:,:,1]) 
    C[:,:,:] = numerical_schemes.step_leapfrog(dx, dy, dt, v, u, C) 

    ax.clear()
    ax.contourf(x,y,C[:,:,1], np.arange(-0, 1, 0.1), extend='both', cmap=cm.viridis) 
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    return ax

ani = animation.FuncAnimation(fig, Run,interval=0, blit=False) 

plt.show() 
