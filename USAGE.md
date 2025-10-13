# Telemac Plugin Usage Guide

This guide provides detailed instructions on how to use the Telemac plugin with the fz parametric computation framework.

## Prerequisites

1. **Python 3.6+** with fz installed:
   ```bash
   pip install git+https://github.com/Funz/fz.git
   ```

2. **Telemac installation** via one of:
   - Local installation (see http://www.opentelemac.org/)
   - Docker: `docker pull irsn/telemac-mascaret:latest`
   - Singularity: `singularity pull docker://irsn/telemac-mascaret:latest`

## Quick Start

### 1. Setup the Plugin

Copy the `.fz` directory to your project or home directory:

```bash
# For project-specific use
cp -r fz-telemac/.fz /path/to/your/project/

# For global use
cp -r fz-telemac/.fz ~/
```

### 2. Prepare Your Telemac Case

Create or modify a Telemac case file (`.cas`) with variable placeholders:

```text
/ Original:
FRICTION COEFFICIENT = 15.

/ Modified with variable:
FRICTION COEFFICIENT = $(friction_coef)

/ Original:
TIME STEP = 0.5

/ Modified with variable:
TIME STEP = $(time_step)
```

Variables use the syntax: `$(variable_name)`

### 3. Configure Output Parsing

Edit `.fz/models/Telemac.json` to define how to extract outputs:

```json
{
    "id": "Telemac",
    "varprefix": "$",
    "formulaprefix": "@",
    "delim": "()",
    "commentline": "/",
    "output": {
        "max_elevation": "grep 'MAXIMUM' results.log | awk '{print $3}'",
        "final_velocity": "grep 'VELOCITY' results.log | tail -1 | awk '{print $2}'"
    }
}
```

See `.fz/models/Telemac.json.example` for more examples.

### 4. Run Parametric Study

Create a Python script:

```python
import fz

# Define parameters
input_variables = {
    "friction_coef": [10, 15, 20],
    "time_step": [0.5, 1.0]
}

# Run study
results = fz.fzr(
    input_path="t2d_breach.cas",
    input_variables=input_variables,
    model="Telemac",
    calculators=".fz/calculators/Localhost_Telemac.json",
    results_dir="results"
)

print(results)
```

## Variable Syntax

### Variables

Use `$(variable_name)` to define variables in your `.cas` file:

```text
FRICTION COEFFICIENT = $(friction_coef)
DURATION = $(simulation_time)
```

### Formulas

Use `@(expression)` to define calculated values:

```text
/ Calculate final time from hours
DURATION = @($(hours) * 3600)

/ Calculate friction from Manning coefficient
FRICTION COEFFICIENT = @(1.0 / $(manning_n))
```

### Comments

Lines starting with `/` are treated as comments by Telemac.

## Calculator Options

### Local Installation

Use `Telemac.sh` for local Telemac installation:

```json
{
    "uri": "sh://",
    "n": 2,
    "models": {
        "Telemac": "bash .fz/calculators/Telemac.sh"
    }
}
```

Requirements:
- Telemac installed in `$HOME/opt/telemac-mascaret/v7p3r1/`
- Telemac profile sourced

### Docker

Use `Telemac-docker.sh` for Docker-based execution:

```json
{
    "uri": "sh://",
    "n": 2,
    "models": {
        "Telemac": "bash .fz/calculators/Telemac-docker.sh"
    }
}
```

Requirements:
- Docker installed
- `docker pull irsn/telemac-mascaret:latest`

On Windows, use `Telemac-docker.bat` with WSL2:

```json
{
    "uri": "sh://",
    "n": 2,
    "models": {
        "Telemac": "cmd /c .fz/calculators/Telemac-docker.bat"
    }
}
```

### Singularity

Use `Telemac-singularity.sh` for HPC environments:

```json
{
    "uri": "sh://",
    "n": 4,
    "models": {
        "Telemac": "bash .fz/calculators/Telemac-singularity.sh"
    }
}
```

Requirements:
- Singularity installed
- Telemac singularity image available

## Output Parsing

### Simple Text Output

Extract values from text files using grep/awk:

```json
{
    "output": {
        "max_depth": "grep 'MAXIMUM DEPTH' *.log | awk '{print $3}'"
    }
}
```

### CSV Output

If you post-process results to CSV files:

```json
{
    "output": {
        "water_level": "python -c 'import pandas; df=pandas.read_csv(\"results.csv\"); print(df[\"water_level\"].max())'"
    }
}
```

### Multiple Outputs

Extract multiple values from the same file:

```json
{
    "output": {
        "max_velocity": "grep 'MAX VELOCITY' output.txt | awk '{print $3}'",
        "min_elevation": "grep 'MIN ELEVATION' output.txt | awk '{print $3}'",
        "simulation_time": "grep 'SIMULATION TIME' output.txt | awk '{print $3}'"
    }
}
```

## Advanced Usage

### Remote Execution

Run calculations on remote servers via SSH:

```json
{
    "uri": "ssh://user@server.example.com",
    "n": 8,
    "models": {
        "Telemac": "bash .fz/calculators/Telemac.sh"
    }
}
```

### Caching

Enable caching to reuse previous calculation results:

```python
results = fz.fzr(
    input_path="t2d_breach.cas",
    input_variables=input_variables,
    model="Telemac",
    calculators=".fz/calculators/Localhost_Telemac.json",
    results_dir="results",
    cache="cache_dir"  # Enable caching
)
```

### Retry on Failure

Configure automatic retry with alternative calculators:

```python
results = fz.fzr(
    input_path="t2d_breach.cas",
    input_variables=input_variables,
    model="Telemac",
    calculators=[
        ".fz/calculators/Localhost_Telemac.json",
        ".fz/calculators/Remote_Telemac.json"  # Fallback
    ],
    results_dir="results",
    retry=2  # Retry up to 2 times
)
```

## Troubleshooting

### Issue: "No .cas file found"

**Solution**: Ensure your case file has a `.cas` extension and is in the specified directory.

### Issue: "Telemac will not support non ISO char in path"

**Solution**: Ensure your working directory path contains only ASCII characters.

### Issue: "Could not find .slf files"

**Solution**: Ensure all required geometry and initial condition files are present. See the `GEOMETRY FILE` and other file references in your `.cas` file.

### Issue: Output parsing returns empty values

**Solution**: 
1. Check that output files are being generated
2. Verify the grep/awk patterns match your actual output format
3. Test the parsing command manually in the results directory

### Issue: Docker container fails to start

**Solution**:
1. Verify Docker is running: `docker ps`
2. Check Docker image exists: `docker images | grep telemac`
3. Ensure you have permission to run Docker

## Examples

See `example_run.py` for a complete working example.

For more information on fz, see: https://github.com/Funz/fz
For more information on Telemac, see: http://www.opentelemac.org/
