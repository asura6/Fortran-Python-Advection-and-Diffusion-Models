import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import norm
import matplotlib.colors as colors
import numerical_schemes

""" Define simulation parameters """
dt = 0.40           #s time step
dx = 2.             #m spatial resolution
dy = 2.             #m spatial resolution
u_max = 5           # m/s
v_max = 5           # m/s
# Domain
x_w = - 100         # m
x_e = 100           # m
y_s = - 100         # m
y_n = 100           # m

""" Initialize dimensions, coordinates and variables """
x_dim = int((x_e - x_w)//dx)
y_dim = int((y_n - y_s)//dy)
C = np.zeros([x_dim, y_dim, 2],order='F')
u = np.zeros([x_dim, y_dim], order='F')
v = np.zeros([x_dim, y_dim], order='F')
x = np.linspace(x_w, x_e, x_dim)
y = np.linspace(y_s, y_n, y_dim)
X, Y = np.meshgrid(x, y)

""" Initialize wind field (low pressure system northern hemesphere) """
Ux, Uy = np.meshgrid(np.linspace(-1, 0, x_dim), np.linspace(-1, 0, y_dim))
u[:,:] = np.sin(np.pi * Ux) * np.cos(np.pi * Uy) * u_max
v[:,:] = -np.cos(np.pi * Ux) * np.sin(np.pi * Uy) * v_max
# Uncomment to plot the wind-field
#fig, ax = plt.quiver(X[::30,::30], Y[::30,::30],u[::30,::30],v[::30,::30])
#ax.set_xlabel('x [m]',fontsize=16)
#ax.set_ylabel('y [m]',fontsize=16)
#ax.set_title('Wind field',fontsize=16)

""" Initialize the initial distribution of concentration of C """
mean = [0, -70]     # Location of "blob"
std = [15, 10]      # Size of blob
cx = norm.pdf((x - mean[1])/std[1])*10
cy = norm.pdf((y - mean[0])/std[0])*10

""" Initial and first step """
C[:,:,0] = np.outer(cx, cy)
C[:,:,1] = numerical_schemes.step_upwind(dx, dy, dt, v, u, C[:,:,0])

""" Prepare the animation plot """
fig, ax = plt.subplots()
bounds = np.linspace(0, 1, 11) # Colorbar range
norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
cf = ax.pcolor(x,y,C[:,:,0],cmap='viridis',vmin=0, vmax=1, norm=norm)
plt.colorbar(cf)

""" Simulation """
def Run(i):
    global C
    #C[:,:,1] = numerical_schemes.step_upwind(dx, dy, dt, v, u, C[:,:,1])
    C[:,:,:] = numerical_schemes.step_leapfrog(dx, dy, dt, v, u, C)

    ax.clear()
    ax.pcolor(x,y,C[:,:,1],cmap='viridis',vmin=0, vmax=1, norm=norm)
    ax.set_xlabel('x [m]',fontsize=16)
    ax.set_ylabel('y [m]',fontsize=16)
    ax.set_title('Time: '+ str(int(i*dt)) + 's',fontsize=16)
    return ax

ani = animation.FuncAnimation(fig, Run,interval=0, blit=False)

plt.show()
