# Pyrocket 0.1.0
## By Bea Adkins

Pyrocket is a simulation code for rocket staging and trajectories with atmospheric drag. Uses include trajectory optimization, mass budgeting, and launch vehicle design. It is intended for aerospace engineering students, amateur rocketeers, and Kerbals.

# Dependencies
Requires the following scientific Python libraries:

- numpy
- scipy
- matplotlib

# Usage
Very crude currently. 

1. Modify `liftoff.py`. Create a Stage object and set the `rocket` field in the `main` method to it. 
2. Run `liftoff.py` using your favorite Python 2 interpreter. E.g. `python liftoff.py` at a command line.

# Roadmap
## 0.1 
- Serialize Stages in a simple field:value text format
- Create command-line interface
- Add a switch between Kerbal Space Program drag (effective area is a multiple of mass) and more realistic drag (effective area is a given value). My current solution: drag_area can be a number [m^2] or a string "kerbal", which would then use the vanilla KSP mass multiplier.

## 0.2
- Add 2D flight model (keep 1D for simpler cases)
- Trajectories:
    - Gravity turn trajectories
    - Piecewise trajectories
    - Simple flight control rules

## 0.3
- Variable gravity
- Orbital dynamics (one body, in-plane)

## Possibilities
- Support for  e.g. space shuttle, Falcon Heavy
- Integration with KSP mods (e.g. Flight/Build Engineer)