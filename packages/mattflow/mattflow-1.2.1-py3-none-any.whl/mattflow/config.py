# config.py is part of MattFlow
#
# MattFlow is free software; you may redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. You should have received a copy of the GNU
# General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.
#
# (C) 2019 Athanasios Mattas
# ======================================================================
"""Configures the simulation"""

# TODO simple API: configuring options on a small window popup

#                  x
#          0 1 2 3 4 5 6 7 8 9
#        0 G G G G G G G G G G
#        1 G G G G G G G G G G
#        2 G G - - - - - - G G
#        3 G G - - - - - - G G
#      y 4 G G - - - - - - G G
#        5 G G - - - - - - G G
#        6 G G - - - - - - G G
#        7 G G - - - - - - G G
#        8 G G G G G G G G G G
#        9 G G G G G G G G G G

import os

import numpy as np


# Pre-processing configuration {
#
# Number of cells on x and y axis
Nx = 120
Ny = 120

# Number of ghost cells (used for applying Boundary Conditions)
# Depends on the used numerical scheme
Ng = 1

# Domain (basin) limits
MIN_X = -1.4
MAX_X = 1.4
MIN_Y = -1.4
MAX_Y = 1.4

# Spatial discretization steps (structured/Cartesian mesh)
dx = (MAX_X - MIN_X) / Nx
dy = (MAX_Y - MIN_Y) / Ny
#
# }

# U_for_ml = np.zeros([conf.MAX_ITERS, conf.Nx * conf.Ny])
# U_for_ml[0] = U[0, conf.Ng: -conf.Ng, conf.Ng: -conf.Ng].flatten()

# Solution configuration {
#
# Ending conditions of the simulation
STOPPING_TIME = 3
MAX_ITERS = 640

# Number of workers for multiprocessing
WORKERS = 1

# Pre-allocate and dump a binary memmap, used by all the workers
DUMP_MEMMAP = False
MEMMAP_DIR = os.path.join(os.getcwd(), "flux_memmap")

# Courant number
# --------------
# dx * COURANT = 0.015 for a more realistic result, in the current fps range
#
#
# dt_sim = dt * COURANT
# dt_sim = dx / wave_vel * COURANT
# dx * COURANT = dt_sim * wave_vel (= dx_sim?)
#
# where:
#   - dt is the time that the slowest wave component (represented by the
#     velocity eagenvector with the min eagenvalue at the jacobian of the
#     non-conservative form of the vectorized representation of the system)
#     takes to travel for dx.
#   - dt_sim is the time that the simulation covers dx
#
COURANT = min(0.9, 0.015 / min(dx, dy))

# Surface level
SURFACE_LEVEL = 1

# Simulation modes (initialization types)
# ---------------------------------------
# Supported:
# 1. 'single drop': modeled via a gaussian distribution
# 1. 'drops'      : configure N_DROPS and ITERS_FOR_NEXT_DROP
# 1. 'rain'       : random drops
MODE = 'drops'

# Number of drops
N_DROPS = 5

# Number of iterations between drops
FIXED_ITERS_BETWEEN_DROPS = False
FIXED_ITERS_TO_NEXT_DROP = 105
ITERS_TO_NEXT_DROP = [0, 80, 90, 130, 110, 60, 120, 120, 150, 100, 130, 120, 120, 100]
ITERS_TO_NEXT_DROP = np.cumsum(ITERS_TO_NEXT_DROP)


RANODM_DROP_CENTERS = True

# Define x, y drop centers (normalized to one)
drop_x_centers = [0, -0.56, 0.28, -0.25, 0.48, -0.42, 0.90, 0.24, -0.78, -0.2, 0.84]
drop_y_centers = [0, 0.25, 0.48, -0.24, -0.59, -0.64, 0.05, -0.40, 0.63, -0.39, -0.40]
drop_x_centers = [x * MAX_X for x in drop_x_centers]
drop_x_centers = [y * MAX_Y for y in drop_y_centers]
drop_centers = list(zip(drop_x_centers, drop_y_centers))


# Boundary conditions
# -------------------
# Supported:
# 1. 'reflective'
BOUNDARY_CONDITIONS = 'reflective'

# Finite Volume Numerical Methods
# -------------------------------
# Supported:
# 1. 'Lax-Friedrichs Riemann'   : 1st order in time: O(Δt, Δx^2, Δy^2)
# 2. '2-stage Runge-Kutta'      : 2nd order in time: O(Δt^2, Δx^2, Δy^2)
# 3. 'MacCormack experimental'  : 2nd order in time: O(Δt^2, Δx^2, Δy^2)
SOLVER_TYPE = '2-stage Runge-Kutta'
#
# }


# Post-processing configuration {
#
# Plotting style
# Options: water, contour, wireframe
PLOTTING_STYLE = 'wireframe'

# frames per sec
FPS = 20
# dots per inch
DPI = 60
# figure size in inches
# golden ratio: 1.618
FIGSIZE = (10 * 1.618, 10)

# resolution = figsize * dpi
# --------------------------
# example:
# figsize = (9.6, 5.4), dpi=200
# resolution: 1920x1080 (1920/200=9.6)

# Rotate the domain at each frame
ROTATION = True

# Render the basin that contains the fluid
SHOW_BASIN = False

# Show the animation
SHOW_ANIMATION = True

# Saving the animation
SAVE_ANIMATION = False

# Path to ffmpeg
PATH_TO_FFMPEG = '/usr/bin/ffmpeg'

# Animation video format
# ----------------------
# Supported:
# 1. 'mp4'
# 2. 'gif'
VID_FORMAT = 'mp4'

# Writing dat files mode
# ----------------------
# Select whether dat files are generated or not
DAT_WRITING_MODE = False
#
# }
