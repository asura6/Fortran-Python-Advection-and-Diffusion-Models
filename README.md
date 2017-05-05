# Fortran-Python Advection and Diffusion Models
These programs use numerical schemes to simulate the time-evolution of physical
advection and diffusion.

The programs have a consistent structure where Fortran subroutines handle the
numerical schemes and Python programs to visualize the results.

## Programs
`Program_1.py`
One-dimensional simulation of the advection of a gas using the Forward-in-time
Backward-in-space (FTBS) scheme with constant windspeed.

`Program_2.py` One-dimensional simulation of the advection of a gas using the
FTBS scheme with non-constant wind speed

`Program_3.py` One-dimensional simulation of the advection and diffusion of a
gas with constant wind-speed

`Program_4.py` One-dimensional simulation of the advection and diffusion of a
gas with non-constant wind speed

`Program_5.py` Two-dimensional simulation of the advection of a gas in a
low-pressure system using either the upwind-scheme or the leap-frog scheme
without filtering.

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
