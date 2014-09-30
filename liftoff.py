import matplotlib.pyplot as pyplot
import numpy as np

from flight import *
from planet import *
from stage import *

T1_test_vehicle = Stage(7.95e3, 3.55e3, 200e3, 320, 0.2)

def main():
    rocket = T1_test_vehicle

    # x, v
    Y0 = [0, 0]

    flight = Flight(rocket, Y0)
    Y = flight.solve()
    
    # Aliases
    x = Y[:, 0]
    v = Y[:, 1]

    # Burnout values
    t_b = rocket.time_burnout()
    x_b = x[-1]
    v_b = v[-1]

    # Rocket equation
    deltav = rocket.Isp * g0 * np.log(rocket.m_0/rocket.m_f) # log is ln by default in Python
    deltav_g = g0 * t_b # Gravity drag
    deltav_d = deltav - deltav_g - v_b # Aerodynamic drag

    # Display results
    print "Mass flow rate:  ", rocket.mass_flow()
    print "Burn time:       ", t_b
    print "Burnout altitude:", x_b
    print "Burnout velocity:", v_b
    print "----"    
    print "Stage deltaV:    ", deltav
    print "Gravity drag:    ", deltav_g
    print "Aerodynamic drag:", deltav_d
    
    # pyplot.plot(t, x, t, v)
    # pyplot.show()

if __name__ == "__main__":
    main()
