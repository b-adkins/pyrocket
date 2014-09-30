import numpy as np
from scipy.integrate import odeint

import matplotlib.pyplot as pyplot

## 
# Kerbin planetary constants
# @todo, refactor to Planet class
rho_0 = 101325 # Sea level pressure [Pa]
h_sc = 5000 # Scale height [m]

##
# Barometric pressure
#
# x    Altitude [m]
#
# Returns pressure [Pa]
def atm_pressure(x):
    return rho_0*np.exp(-x/h_sc)

##
# Atmospheric density
#
# x    Altitude [m]
#
# Returns density [kg/m^3]
def atm_density(x):
    pressure_to_dens =  1.2230948554874 # [kg/(m^3*atm)]
    pressure_to_dens = pressure_to_dens/rho_0 # Convert from atm to Pa
    return atm_pressure(x) * pressure_to_dens

##
# Calculates area for use in drag equations. Grossly oversimplified, based on mass.
#
# m - Vehicle mass
#
# Returns "area" [m^2]
def dragArea(m):
    return 0.008*m

##
# Calculates drag force.
#
# rho  Atmospheric pressure [Pa]
# v    Velocity [m/s]
# Cd   Drag coefficient
# A    Effective area [m^2]
#
# Returns drag [N].
def drag(rho, v, Cd, A):
    return 0.5 * rho * Cd * A * v**2


## Vehicle constants
# @todo Refactor into "stage" class.

# Vehicle parameters
m_0 = 7.95e3 # Wet mass [kg]
m_f = 3.55e3 # Dry mass [kg]

# Thruster parameters
g = 9.81 # Kerbin gravity [m/s]
T = 200e3 # Thrust [N]
Isp = 320 # Isp [s]

# Aerodynamic parameters
C_d = 0.2 # Coefficient of drag

##
# Calculates mass flow rate of engine
# 
# Uses the relation T = dm * v_e = dm * Isp * g
#
# return mass flow [kg/s]
def mass_flow():
    return T/(Isp*g)

##
# Calculates vehicle mass from wet/dry mass and engine parameters.
#
# t Time elapsed [s]
#
# Returns mass [kg]
def mass(t):
    dm = mass_flow()
    return m_0 - dm*t

##
# Flight equation
#
# Y  Variables [x, v]
# t  Time [s]
#
# return dY = [v, a]
def rocket1dode(Y, t):
    # Readability aliases
    x = Y[0]
    v = Y[1]

    # Current mass
    m = mass(t)
    
    # Calculate drag force
    D = drag(atm_density(x), v, C_d, dragArea(m))
    
    # Check for burnout
    if(m < m_f):
        dv = -g
    else:
        dv = T/m - g - D/m
         
    dx = v

    return [dx, dv]

def main():
    # x, v
    Y0 = [0, 0]

    # Burnout time
    dm = mass_flow()
    t_b = (m_0 - m_f)/dm
    
    t = np.arange(0, t_b, .001)
    sol = odeint(rocket1dode, Y0, t, full_output = 1)
    
    # Aliases
    Y = sol[0]
    x = Y[:, 0]
    v = Y[:, 1]

    # Burnout values
    x_b = x[-1]
    v_b = v[-1]

    # Rocket equation
    deltav = Isp * g * np.log(m_0/m_f) # log is ln by default in Python
    deltav_g = g * t_b # Gravity drag
    deltav_d = deltav - deltav_g - v_b # Aerodynamic drag
    
    # Display results
    print "Mass flow rate:  ", dm
    print "Burn time:       ", t_b
    print "Burnout altitude:", x_b
    print "Burnout velocity:", v_b
    print "----"    
    print "Stage deltaV:    ", deltav
    print "Gravity drag:    ", deltav_g
    print "Aerodynamic drag:", deltav_d
    
#    pyplot.plot(t, x, t, v)
#    pyplot.show()

    return t, Y

if __name__ == "__main__":
    main()
