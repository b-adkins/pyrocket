import numpy as np

# Standard Earth/Kerbin gravity [m/s]
# Used for Isp calculations.
g0 = 9.81 

##
# Class representing an arbitrary stage of a vehicle.
class Stage(object):
    ## Create a Stage object.
    #
    # To make a multi-stage vehicle, start with the final stage. For each successive stage, include the previous stage
    # as payload.
    #
    # name         A short string naming your Stage, used for pretty printing.
    #
    # Mass budget
    # m_s         Structural mass [kg]. Total mass of engines, fuel tanks (only the tank), and struts.
    # m_l         Payload mass [kg]. Next stage wet mass or total mass of science instruments, capsules, space systems.
    # m_p         Propellant mass [kg].
    # playload    Payload Stage or None (currently only a pointer - next stage's wet mass should be included in
    #               payload mass).
    #
    # Thruster parameters
    # T           Thrust [N]
    # Isp         Specific impulse [s]
    #
    # Aerodynamic parameters
    # C_d         Coefficient of drag
    def __init__(self, name, m_s, m_l, m_p, T, Isp, C_d, payload = None):
        self.name = name
        
        self.m_s = m_s
        self.m_l = m_l
        self.m_p = m_p

        self.T = T
        self.Isp = Isp

        self.C_d = C_d

        self.payload = payload

    @property
    def m_0(self):
        """ Calculate wet mass."""
        return self.m_f + self.m_p

    @property
    def m_f(self):
        """ Calculate dry mass."""
        return self.m_l + self.m_s

    @property
    def m_l(self):
        """ Get payload mass. """
        return self._m_l

    @m_l.setter
    def m_l(self, value):
        """ Set payload mass. """
        self._m_l = value

    @property
    def m_p(self):
        """ Get propellant mass. """
        return self._m_p

    @m_p.setter
    def m_p(self, value):
        """ Set propellant mass. """
        self._m_p = value

    @property
    def m_s(self):
        """ Get structural mass. """
        return self._m_s

    @m_s.setter
    def m_s(self, value):
        """ Set structural mass. """
        self._m_s = value

    
        
    ##
    # Calculates area for use in drag equations. Grossly oversimplified in KSP, based on mass.
    # m    Vehicle mass [kg]
    #
    # Returns "area" [m^2]
    def dragArea(self, m):
        return 0.008 * m
    
    ##
    # Calculates drag force.
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
    # Calculates mass flow rate of engine
    # 
    # Uses the relation T = dm * v_e = dm * Isp * g
    #
    # return mass flow [kg/s]
    def mass_flow(self):
        return self.T/(self.Isp*g0)
    
    ##
    # Calculates vehicle mass from wet/dry mass and engine parameters.
    #
    # t Time since start of burn [s]
    #
    # Returns mass [kg]
    def mass(self, t):
        return self.m_0 - self.mass_flow() * t

    ##
    # Calculates burnout time (at full thrust)
    #
    def time_burnout(self):
        return (self.m_0 - self.m_f)/self.mass_flow()
    
    ##
    # (Almost) Single-line representation.
    def __repr__(self):
        ret = '<Rocket stage "{}">'.format((self.name))

        # Cut possibility
        # ret = "[Stage object: m_0 = {:0,.0f}, m_f = {:0,.0f}, ".format(self.m_0, self.m_f)
        # ret += "T = {:0,.0f}, Isp = {:0,.0f}, ".format(self.T, self.Isp)
        # ret += "C_d = {}, ".format(self.C_d)
        # ret += "payload = {}]".format(self.payload)
        
        return ret
    
    ##
    # Complete representation.
    def __str__(self):
        ret = self.name + "\n"
        ret += "m_p = {:0,g}, m_s = {:0,g}, m_l = {:0,g}\n" \
            .format(self.m_p, self.m_s, self.m_l)
        ret += "m_0 = {:0,g}, m_f = {:0,g}\n".format(self.m_0, self.m_f)    
        ret += "T = {:0,g}, Isp = {:0,g}\n".format(self.T, self.Isp)
        ret += "C_d = {}\n".format(self.C_d)
        ret += "payload = {}".format(repr(self.payload))
    
        return ret
