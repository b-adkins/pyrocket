import matplotlib.pyplot as pyplot
import numpy as np
import numpy.ma as ma

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
    x = np.array(Y[:, 0])
    v = np.array(Y[:, 1])
    D = np.array(Y[:, 2]) 
    W = np.array(Y[:, 3])

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

    t = flight.getTimes()
    pyplot.plot(t, x, t, v)

    # odeint can skip over many time steps, leaving blanks for intermediate values
    # Hence, masked arrays to ignore the blank values.
    D = ma.masked_invalid(D)
    W = ma.masked_invalid(W)
    mask = D.mask
    t = ma.masked_array(t, mask=mask)
    D = D.compressed()
    W = W.compressed()
    t = t.compressed()
    
    pyplot.figure()
    pyplot.plot(t, D, t, W)
    pyplot.show()

    return Y
    
if __name__ == "__main__":
    main()
