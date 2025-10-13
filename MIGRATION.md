# Migration from Old Telemac Plugin

This document explains the migration from the old Java-based Telemac plugin to the new fz-based Python plugin.

## Overview

The old plugin (https://github.com/Funz/plugin-telemac) was written in Java and integrated with the Funz framework. This new plugin uses the fz Python framework with a simpler, more flexible configuration format.

## Key Differences

### Old Plugin Structure

```
plugin-telemac/
├── src/main/java/
│   └── org/funz/Telemac/
│       ├── TelemacIOPlugin.java     # Java plugin with output parsing
│       └── TelemacHelper.java       # Helper methods
└── src/main/scripts/
    ├── Telemac.sh
    ├── Telemac-docker.sh
    ├── Telemac-docker.bat
    └── Telemac-singularity.sh
```

### New Plugin Structure

```
fz-telemac/
├── .fz/
│   ├── models/
│   │   ├── Telemac.json           # Model definition (variables, formulas, output)
│   │   └── Telemac.json.example   # Example with output parsing patterns
│   └── calculators/
│       ├── Localhost_Telemac.json # Calculator configuration
│       ├── Telemac.sh             # Calculator scripts (unchanged)
│       ├── Telemac-docker.sh
│       ├── Telemac-docker.bat
│       └── Telemac-singularity.sh
├── t2d_breach.cas/                # Sample case
├── example_run.py                 # Usage example
├── README.md                      # Quick start guide
└── USAGE.md                       # Detailed documentation
```

## Configuration Mapping

### Variable Syntax

**Old Plugin (Java):**
- Variable start symbol: `SyntaxRules.START_SYMBOL_DOLLAR` → `$`
- Variable limit: `SyntaxRules.LIMIT_SYMBOL_PARENTHESIS` → `()`

**New Plugin (JSON):**
```json
{
    "varprefix": "$",
    "delim": "()"
}
```

Usage: `$(variable_name)` in `.cas` files

### Formula Syntax

**Old Plugin (Java):**
- Formula start symbol: `SyntaxRules.START_SYMBOL_AT` → `@`
- Formula limit: `SyntaxRules.LIMIT_SYMBOL_BRACKETS` → `[]`

**New Plugin (JSON):**
```json
{
    "formulaprefix": "@",
    "delim": "()"
}
```

Usage: `@(expression)` in `.cas` files

Note: The delimiter changed from `[]` to `()` for consistency.

### Comment Lines

**Old Plugin:**
- Comment line: `CommentLine` → `/`

**New Plugin:**
```json
{
    "commentline": "/"
}
```

Usage: Lines starting with `/` are comments

## Output Parsing

### Old Plugin Approach

The old plugin had complex Java code in `TelemacIOPlugin.java` with the `readOutput()` method that:

1. Read CSV files from the output directory
2. If no CSV files, read directly from SLF result files using TelemacHelper
3. Parsed POI files to extract points of interest
4. Interpolated values at specified points
5. Returned structured data as HashMap

This logic was tightly coupled to the plugin and handled:
- CSV parsing with `readDoubleArray2D()`
- SLF file reading with `extractPOIfromCASRES()`
- POI file parsing with `readPOI()`
- Array simplification with `simplify()`

### New Plugin Approach

The new plugin intentionally **does not** port this complex output reading logic. Instead:

1. **User-defined output parsing**: Users define their own output extraction in the model JSON
2. **Flexible scripting**: Can use any command-line tool (grep, awk, python, etc.)
3. **Customizable per project**: Each project can define outputs based on their needs

**Example configurations in `.fz/models/Telemac.json.example`:**

```json
{
    "output": {
        "max_depth": "grep 'Maximum depth:' output.txt | awk '{print $3}'",
        "S": "python -c 'import pandas;import glob;import json;print(json.dumps({f.split(\"_S.csv\")[0]:pandas.read_csv(f).to_dict() for f in glob.glob(\"*_S.csv\")}))'",
        "H": "python -c 'import pandas;import glob;import json;print(json.dumps({f.split(\"_H.csv\")[0]:pandas.read_csv(f).to_dict() for f in glob.glob(\"*_H.csv\")}))'"
    }
}
```

### Why This Change?

1. **Simplicity**: No need for complex Java code and dependencies
2. **Flexibility**: Users can customize output parsing for their specific needs
3. **Transparency**: Output parsing commands are visible and modifiable
4. **Extensibility**: Easy to add new output types without modifying plugin code
5. **Tool choice**: Use any available command-line tools (Python, R, grep, awk, etc.)

## Calculator Scripts

The calculator scripts (`.sh` and `.bat` files) are largely unchanged from the old plugin:

### Telemac.sh
- Same functionality as old plugin
- Runs Telemac with local installation

### Telemac-docker.sh
- Same functionality as old plugin
- Uses Docker container for Telemac execution
- Better handling of case directory vs individual files

### Telemac-docker.bat
- Same functionality as old plugin
- Windows version using WSL2

### Telemac-singularity.sh
- Same functionality as old plugin
- For HPC environments with Singularity

## Migration Steps

To migrate from the old plugin to the new one:

1. **Install fz**:
   ```bash
   pip install git+https://github.com/Funz/fz.git
   ```

2. **Copy the `.fz` directory** to your project:
   ```bash
   cp -r fz-telemac/.fz /path/to/your/project/
   ```

3. **Update variable syntax** in your `.cas` files (if different):
   - Old: `$(variable)` or `$[variable]` → New: `$(variable)`

4. **Define output parsing** in `.fz/models/Telemac.json`:
   - Add commands to extract outputs from your result files
   - Use grep, awk, Python, or any other tools
   - See `.fz/models/Telemac.json.example` for examples

5. **Update your run scripts** from Java to Python:
   ```python
   import fz
   
   results = fz.fzr(
       input_path="case.cas",
       input_variables={"param1": [1, 2, 3]},
       model="Telemac",
       calculators=".fz/calculators/Localhost_Telemac.json",
       results_dir="results"
   )
   ```

## Benefits of New Plugin

1. **Simpler configuration**: JSON instead of Java code
2. **More flexible**: Python instead of Java for scripting
3. **Better documentation**: Comprehensive README and USAGE guides
4. **User control**: Output parsing controlled by users
5. **Easier to extend**: Add new calculators or modify existing ones
6. **Modern tooling**: Uses current best practices for scientific computing

## Backward Compatibility

The new plugin is **not directly compatible** with the old plugin due to:
- Different framework (fz vs Funz)
- Different configuration format (JSON vs Java)
- Different output parsing approach (user-defined vs built-in)

However, migration is straightforward following the steps above.

## Support

For issues or questions:
- fz framework: https://github.com/Funz/fz
- This plugin: https://github.com/Funz/fz-telemac
- Original plugin: https://github.com/Funz/plugin-telemac
- Telemac: http://www.opentelemac.org/
