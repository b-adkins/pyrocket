from planet import *
from stage import *

##
# Class to keep track of one flight of one vehicle.
#
class Flight:
    ##
    # vehicle The first Stage of a vehicle.
    # Y0      Initial position and velocity [x, v] in [m, m/s]
    def __init__(self, vehicle, Y0, planet = Kerbin, t = None):
        self.vehicle = vehicle
        self.Y0 = Y0
        self.planet = planet
        if t is None:
        # Default, time until burnout
            self.t = np.arange(0, vehicle.time_burnout(), .001)
        else:
            self.t = t

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
    
        return [dx, dv]
        
    ##
    # Solves the flight ODE
    #
    # Returns array with x in column 0, v in column 1.
    def solve(self):        
        sol = odeint(self.rocket1dode, self.Y0, self.t, full_output = 1)    
        # Extracts Y vector from solution tuple
        return sol[0]
