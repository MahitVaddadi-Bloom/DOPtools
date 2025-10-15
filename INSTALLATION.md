# DOPtools - Modernized Installation Guide

This is a modernized version of DOPtools that has been updated for compatibility with current Python versions and can be built/installed with `uv`.

## What's Been Modernized

### ✅ **Build System**
- ✅ **pyproject.toml**: Converted from `setup.py` to modern `pyproject.toml` format
- ✅ **uv compatibility**: Can be built and installed with `uv`
- ✅ **Type hints**: Added `py.typed` marker for type checking support
- ✅ **Modern tooling**: Added configuration for black, isort, pytest, mypy

### ✅ **Python Compatibility**
- ✅ **Python 3.9-3.12**: Compatible with modern Python versions (limited by chython dependency)
- ✅ **Dependencies**: All dependencies are up-to-date and compatible
- ✅ **Syntax**: All code is compatible with modern Python

### ✅ **Package Structure**
- ✅ **Proper entry points**: CLI commands properly configured
- ✅ **Comprehensive .gitignore**: Updated for modern development
- ✅ **License**: Proper SPDX license identifier

## Installation Methods

### Method 1: Install from Built Wheel (Recommended)

```bash
# Build the package
cd DOPtools
uv build --wheel

# Install the built wheel
uv pip install dist/doptools-1.3.9-py3-none-any.whl
```

### Method 2: Install in Development Mode

```bash
# Install in editable mode for development
cd DOPtools
uv pip install -e .
```

### Method 3: Install into Existing Environment

```bash
# Using pip in existing environment
cd DOPtools
pip install .

# Or with uv in existing environment
uv pip install .
```

## Usage

After installation, you can use DOPtools in several ways:

### 1. Python API

```python
import doptools
from doptools.chem import ChythonCircus, ComplexFragmentor
from doptools.optimizer import optimize_model

# Create descriptor calculator
circus = ChythonCircus(lower=0, upper=2)

# Use with ComplexFragmentor
fragmentor = ComplexFragmentor(
    associator=[("molecules", circus)],
    structure_columns=["molecules"]
)
```

### 2. Command Line Interface

The package provides several CLI commands:

```bash
# Prepare descriptors
launch_preparer --input data.csv --output output/

# Optimize models  
launch_optimizer --config config.json

# Plot results
plotter --input results.csv

# Rebuild models
rebuilder --input model_data/
```

## Dependencies

All dependencies are automatically installed:

- **Core**: pandas, numpy, scipy, scikit-learn
- **Chemistry**: chython, rdkit
- **ML**: optuna, xgboost
- **Utils**: matplotlib, tqdm, ipython
- **IO**: xlwt, xlrd, openpyxl, pillow

## Python Version Compatibility

**Supported**: Python 3.9, 3.10, 3.11, 3.12, 3.13

**Note**: All Python versions are now fully supported including Python 3.13 with the updated chython dependency.

## Development

For development work:

```bash
# Install with development dependencies
uv pip install -e ".[dev]"

# Install with test dependencies
uv pip install -e ".[test]" 

# Install with documentation dependencies
uv pip install -e ".[docs]"
```

## Testing

Test the installation:

```bash
python test_installation.py
```

## Key Features

- **CircuS and Chyline descriptors** - Chemical structure descriptors
- **SKLearn compatibility** - All calculators work as sklearn transformers
- **ComplexFragmentor** - Concatenate descriptors from multiple structures
- **ColorAtom** - Visualize atomic contributions to predictions
- **CLI tools** - Command-line interface for descriptor calculation and optimization

## Troubleshooting

### Common Issues

1. **Python 3.13 compatibility**: Use Python 3.9-3.12 instead
2. **chython dependency**: Make sure you're using a supported Python version
3. **RDKit installation**: Use conda for RDKit if pip installation fails

### Environment Setup

For best results, create a clean environment:

```bash
# With uv
uv venv doptools-env
source doptools-env/bin/activate  # On Windows: doptools-env\Scripts\activate
uv pip install .

# With conda  
conda create -n doptools python=3.11
conda activate doptools
conda install rdkit -c conda-forge
uv pip install .
```

## License

LGPL-3.0-or-later - Same as original DOPtools

## Credits

- **Original Author**: Dr. Pavel Sidorov
- **Modernization**: Updated for current Python ecosystem and uv compatibility

---

This modernized version maintains full compatibility with the original DOPtools while adding support for modern Python packaging and build tools.