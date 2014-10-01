import matplotlib.pyplot as pyplot
import numpy as np
import numpy.ma as ma

from flight import *
from planet import *
from stage import *

T1_test_vehicle = Stage("T-1 Test Vehicle", 2e3, 1.55e3, 4e3, 200e3, 320, 0.2)

T2_stage_2 = Stage("T-2 Stage 2", 1.75e3, 1.49e3, 2e3, 200e3, 370, 0.2)
T2_test_vehicle = Stage("T-2 Test Vehicle", 2.25e3, 5.99e3, 6e3, 200e3, 340, 0.2, payload = T2_stage_2)

def main():
    # rocket = T1_test_vehicle
    rocket = T2_test_vehicle

    # x, v
    Y0 = [0, 0]

    flight = Flight(rocket, Y0)
    Y = flight.solve()
    
    # Aliases
#    print "Y:", Y.shape, Y
    x = np.array(Y[:, 0])
    v = np.array(Y[:, 1])
    D = np.array(Y[:, 2]) 
    W = np.array(Y[:, 3])

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
