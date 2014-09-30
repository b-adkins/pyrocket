import math

class Planet(object):
    # Sea level pressure [Pa]
    rho_0 = 0
    # Scale height [m]
    h_sc = 0

    ##
    # Barometric pressure
    #
    # x    Altitude [m]
    #
    # Returns pressure [Pa]
    def atm_pressure(self, x):
        return self.rho_0 * math.exp(-x/self.h_sc)
    
    ##
    # Atmospheric density
    #
    # x    Altitude [m]
    #
    # Returns density [kg/m^3]
    def atm_density(self, x):
        pressure_to_dens =  1.2230948554874 # [kg/(m^3*atm)]
        pressure_to_dens = pressure_to_dens/self.rho_0 # Convert from atm to Pa
        return self.atm_pressure(x) * pressure_to_dens

    
Kerbin = Planet()
Kerbin.rho_0 = 1
Kerbin.rho_0 = 101325 
Kerbin.h_sc = 5000 

