import numpy as np

# Kerbin gravity [m/s]
# Used for Isp calculations
g0 = 9.81 

##
# Class representing
class Stage:
    ##
    #
    # Vehicle parameters
    # m_0  Wet mass [kg]
    # m_f  Dry mass [kg]
    #
    # Thruster parameters
    # T    Thrust [N]
    # Isp  Specific impulse [s]
    #
    # Aerodynamic parameters
    # C_d   Coefficient of drag
    def __init__(self, m_0, m_f, T, Isp, C_d):
        self.m_0 = m_0 
        self.m_f = m_f 

        self.T = T
        self.Isp = Isp

        self.C_d = C_d
        
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
    # t Time elapsed [s]
    #
    # Returns mass [kg]
    def mass(self, t):
        return self.m_0 - self.mass_flow() * t

    ##
    # Calculates burnout time (at full thrust)
    #
    def time_burnout(self):
        return (self.m_0 - self.m_f)/self.mass_flow()
