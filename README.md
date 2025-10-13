# fz-telemac

Telemac plugin for the [fz](https://github.com/Funz/fz) parametric computation framework.

This repository contains the model definition and calculator scripts for running Telemac simulations with fz.

## Installation

1. Install fz:
```bash
pip install git+https://github.com/Funz/fz.git
```

2. Clone this repository:
```bash
git clone https://github.com/Funz/fz-telemac.git
```

3. Copy the `.fz` directory to your project or home directory:
```bash
# Copy to your project directory
cp -r fz-telemac/.fz /path/to/your/project/

# Or copy to your home directory for global access
cp -r fz-telemac/.fz ~/
```

## Usage

### Model Configuration

The Telemac model is defined in `.fz/models/Telemac.json`:

```json
{
    "id": "Telemac",
    "varprefix": "$", 
    "formulaprefix": "@", 
    "delim": "()", 
    "commentline": "/",
    "output": {
        "": ""
    }
}
```

The model supports:
- Variables: `$(variable_name)` 
- Formulas: `@(expression)`
- Comments: Lines starting with `/`

### Calculator Scripts

Several calculator scripts are provided in `.fz/calculators/`:

- **Telemac.sh**: Basic script for local Telemac installation
- **Telemac-docker.sh**: Uses Docker container (recommended)
- **Telemac-docker.bat**: Windows version using Docker via WSL2
- **Telemac-singularity.sh**: Uses Singularity container

### Example Usage

Create a parametric study script:

```python
import fz

# Define input variables
input_variables = {
    "breach_width": [10, 20, 30],
    "breach_depth": [1, 2, 3]
}

# Run parametric study
results = fz.fzr(
    input_path="t2d_breach.cas",
    input_variables=input_variables,
    model="Telemac",
    calculators=".fz/calculators/Localhost_Telemac.json",
    results_dir="results"
)

print(results)
```

### Calculator Configuration

The calculator configuration is defined in `.fz/calculators/Localhost_Telemac.json`:

```json
{
    "uri": "sh://",
    "n": 2, 
    "models": {
      "Telemac":"bash .fz/calculators/Telemac.sh"
    }
}
```

You can modify:
- `n`: Number of parallel calculations
- The script path to use different calculator scripts (docker, singularity, etc.)

### Docker Setup

To use the Docker-based calculator:

1. Install Docker
2. Pull the Telemac image:
```bash
docker pull irsn/telemac-mascaret:latest
```

3. Update the calculator configuration to use the Docker script:
```json
{
    "uri": "sh://",
    "n": 2, 
    "models": {
      "Telemac":"bash .fz/calculators/Telemac-docker.sh"
    }
}
```

### Input Files

Telemac requires several input files:
- `.cas` file: Main case configuration file
- `.slf` files: Geometry, initial conditions, etc.
- `.cli` file: Boundary conditions
- `.liq` file: Liquid boundaries
- `.poi` file: Points of interest for output extraction
- Other data files as specified in the `.cas` file

All input files referenced in the `.cas` file must be present in the same directory.

### Output Configuration

The output section in the model definition (`.fz/models/Telemac.json`) is intentionally left empty for users to customize based on their specific output requirements. Users should define output parsers based on their simulation results.

Example output configurations:

```json
{
    "output": {
        "max_depth": "grep 'Maximum depth:' output.txt | awk '{print $3}'",
        "final_velocity": "grep 'Final velocity:' output.txt | awk '{print $3}'"
    }
}
```

For CSV-based outputs (if you process results to CSV format):

```json
{
    "output": {
        "S": "python -c 'import pandas;import glob;import json;print(json.dumps({f.split(\"_S.csv\")[0]:pandas.read_csv(f).to_dict() for f in glob.glob(\"*_S.csv\")}))'",
        "H": "python -c 'import pandas;import glob;import json;print(json.dumps({f.split(\"_H.csv\")[0]:pandas.read_csv(f).to_dict() for f in glob.glob(\"*_H.csv\")}))'"
    }
}
```

## Sample Case

A sample Telemac case (`t2d_breach.cas`) is included in this repository, demonstrating a 2D breach simulation. This case includes all necessary input files and can be used as a template for your own simulations.

## Requirements

- Python 3.6+
- fz package
- Telemac installation or Docker/Singularity with Telemac image

## License

This project follows the same license as the Funz project.

## References

- [Telemac website](http://www.opentelemac.org/)
- [fz framework](https://github.com/Funz/fz)
- [Original Telemac plugin](https://github.com/Funz/plugin-telemac)