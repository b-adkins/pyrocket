from scipy.integrate import odeint
import numpy as np

from planet import *
from stage import *

##
# Class to keep track of one flight of one vehicle.
#
class Flight:
    ##
    # vehicle The first Stage of a vehicle.
    # Y0      Initial position and velocity [x, v] in [m, m/s]
    # planet  Planet object
    # t       Time argument for odeint. Intermediate value logging will break if time step isn't constant!
    def __init__(self, vehicle, Y0, planet = Kerbin, t = None):
        self.vehicle = vehicle
        self.Y0 = Y0
        self.planet = planet
        if t is None:
        # Default, time until burnout
            self.dt = 0.05
            self.t = np.arange(0, vehicle.time_burnout(), self.dt)
        else:
            self.t = t
            self.dt = t[1] - t[0] # Assumes constant time interval
        self.i_t = 0 # Index of current timestep

    ##
    # Calculates drag force.
    #
    # In Flight because it is a property of both the vehicle and the flight conditions
    #
    # rho  Atmospheric pressure [Pa]
    # v    Velocity [m/s]
    # Cd   Drag coefficient
    # A    Effective area [m^2]
    #
    # Returns drag [N].
    def drag(self, rho, v, Cd, A):
        return 0.5 * rho * Cd * A * v**2

            
    ##
    # Flight equation
    #
    # Y  Variables [x, v]
    # t  Time [s]
    #
    # return dY = [v, a]
    def rocket1dode(self, Y, t):
        # Readability aliases
        x = Y[0]
        v = Y[1]
    
        # Current mass
        m = self.vehicle.mass(t)
        
        # Calculate drag force
        D = self.drag(self.planet.atm_density(x), v, self.vehicle.C_d, self.vehicle.dragArea(m))
        
        # Check for burnout
        if(m < self.vehicle.m_f):
            dv = -g0
        else:
            dv = self.vehicle.T/m - g0 - D/m
        dx = v

        # Log forces
        self.D[self.i_t] = -D
        self.W[self.i_t] = -m*g0
        
        # Keep track of the current timestep
        # Step forward until t is within step i_t (but don't go past array end)
        while not t > self.t[-1] and t >= self.t[self.i_t]:
            self.i_t += 1
        
        return [dx, dv]
        
    ##
    # Solves the flight ODE
    #
    # Returns 2D array with the following values in columns:
    # [x, v, D, W]
    #
    # x - position [m]
    # v - velocity [m]
    # D - drag force [N]
    # W - weight/gravitational force [N]
    def solve(self):
        # Initialize log of forces
        self.D = np.empty(self.t.size)
        self.W = np.empty(self.t.size)
        self.D.fill(np.NaN)
        self.W.fill(np.NaN)
        
        sol = odeint(self.rocket1dode, self.Y0, self.t, full_output = 1)    
        # Extracts Y vector from solution tuple
        self.Y = sol[0]

        return np.c_[self.Y, self.D, self.W]


    def getTimes(self):
        return self.t
