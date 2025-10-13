#!/usr/bin/env python3
"""
Example script demonstrating how to use the Telemac plugin with fz.

This example shows how to run a parametric study with Telemac,
varying parameters like friction coefficient and time step.
"""

import fz

# Example 1: Parse input variables from the .cas file
print("Example 1: Parsing variables from Telemac case file")
print("=" * 50)

model = {
    "varprefix": "$",
    "delim": "()"
}

# This would identify all $(variable) patterns in the .cas file
# variables = fz.fzi("t2d_breach.cas/t2d_breach.cas", model)
# print(f"Found variables: {variables}")


# Example 2: Running a parametric study
print("\nExample 2: Running a parametric study")
print("=" * 50)

# First, you need to modify your .cas file to include variable placeholders
# For example, replace:
#   FRICTION COEFFICIENT = 15.
# with:
#   FRICTION COEFFICIENT = $(friction_coef)
#
# And replace:
#   TIME STEP = 0.5
# with:
#   TIME STEP = $(time_step)

# Define the model with output parsing
model = {
    "id": "Telemac",
    "varprefix": "$",
    "formulaprefix": "@",
    "delim": "()",
    "commentline": "/",
    "output": {
        # Define how to extract outputs from your results
        # These are examples - adjust based on your actual output files
        "max_elevation": "grep 'MAXIMUM ELEVATION' *.log | tail -1 | awk '{print $NF}'",
        "final_time": "grep 'TIME' *.log | tail -1 | awk '{print $2}'"
    }
}

# Define parameter values to test
input_variables = {
    "friction_coef": [10, 15, 20],  # Test 3 friction coefficients
    "time_step": [0.5, 1.0],         # Test 2 time steps
}

# Uncomment to run the parametric study
# This would create 3 × 2 = 6 different simulations
"""
results = fz.fzr(
    input_path="t2d_breach.cas",
    input_variables=input_variables,
    model=model,
    calculators=".fz/calculators/Localhost_Telemac.json",
    results_dir="results"
)

print("\nResults:")
print(results)
print(f"\nCompleted {len(results)} calculations")
"""

print("\nNote: To run this example:")
print("1. Modify t2d_breach.cas/t2d_breach.cas to include variable placeholders")
print("2. Obtain the required .slf input files (see t2d_breach.cas/README.txt)")
print("3. Configure output parsing in the model definition")
print("4. Install Telemac or configure Docker/Singularity")
print("5. Uncomment the fz.fzr() call above")
