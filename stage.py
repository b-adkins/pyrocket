import numpy as np
from scipy.integrate import odeint

import matplotlib.pyplot as pyplot

## Vehicle constants
# @todo Refactor into "stage" class.

# Vehicle parameters
m_0 = 9.09e3 # Wet mass [kg]
m_f = 5.09e3 # Dry mass [kg]

# Thruster parameters
g = 9.81 # Kerbin gravity [m/s]
T = 200e3 # Thrust [N]
Isp = 320 # Isp [s]

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

    m = mass(t)
    # Check for burnout
    if(m < m_f):
        dv = -g
    else:
        dv = T/m - g
         
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
    
    # Display results
    print "Burn time:       ", t_b
    print "Mass flow rate:  ", dm
    print "Burnout altitude:", x_b
    print "Burnout velocity:", v_b
    pyplot.plot(t, x, t, v)
    pyplot.show()

    return t, Y

if __name__ == "__main__":
    main()
