# Fortran-Python Advection and Diffusion Models
These programs use numerical schemes to simulate the time-evolution of physical
advection and diffusion.

The programs have a consistent structure where Fortran subroutines handle the
numerical schemes and Python programs to visualize the results.

## Makefile commands
### make 
Creates the Python module from the Fortran source 
### make check
checks the syntax in the Fortran source code.
### make clean
removes any final and intermediary files created during compilation

## Build Dependencies
### py2f
Creation of wrapper function 
### gfortran 
### python 3
### numpy
### scipy
### matplotlib
