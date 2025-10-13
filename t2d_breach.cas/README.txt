Sample Telemac 2D Breach Case
==============================

This directory contains a sample Telemac 2D breach simulation case.

Note: The large binary .slf files (geometry, initial conditions, and results) 
have been excluded from this repository due to their size (40+ MB).

To run this case, you will need to:
1. Obtain the required .slf files:
   - geo_breach.slf (geometry file)
   - ini_breach.slf (initial conditions)
   - f2d_breach.slf (forcing data)
   - r2d_breach.slf (results - will be generated)

2. Place them in this directory alongside the other input files.

The complete sample case with all files can be found in the original plugin:
https://github.com/Funz/plugin-telemac/tree/master/src/main/samples

Files included in this directory:
- t2d_breach.cas: Main case configuration file
- t2d_breach.liq: Liquid boundaries definition
- t2d_breach.poi: Points of interest for output extraction
- geo_breach.cli: Boundary conditions
- breach.txt: Breach data
- breach.xml: Additional configuration
- breach.py: Python script for breach configuration
