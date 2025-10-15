# DOPtools CLI Usage Guide

The DOPtools CLI provides a comprehensive interface for molecular descriptor calculation, model optimization, and chemical analysis.

## Installation

The CLI is automatically available after installing DOPtools:

```bash
pip install doptools
```

## Main Commands

### 1. Descriptors

Calculate molecular descriptors from chemical structures:

#### CircuS Descriptors
```bash
doptools descriptors circus -i input.csv -o output.csv --smiles-column SMILES --id-column ID
```

Options:
- `--lower`: Lower bound for radius (default: 0)
- `--upper`: Upper bound for radius (default: 3)
- `--on-bond`: Calculate bond-centered descriptors

#### RDKit Fingerprints
```bash
doptools descriptors rdkit -i input.csv -o output.csv --fp-type morgan --nbits 1024 --radius 2
```

Supported fingerprint types:
- `morgan`: Morgan fingerprints
- `rdkfp`: RDKit fingerprints

#### Complex Descriptors
```bash
doptools descriptors complex -i input.csv -o output.csv --descriptor-type fingerprinter
```

### 2. Models

Model optimization and analysis tools:

#### Optimize Models
```bash
doptools models optimize -c config.yaml
```

#### Rebuild Models
```bash
doptools models rebuild -m model.pkl -d data.csv
```

### 3. Analysis

Chemical analysis and visualization:

#### ColorAtom Analysis
```bash
doptools analysis coloratom -m model.pkl -i input.csv -o output.html
```

#### Plotting
```bash
doptools analysis plot -d data.csv -t scatter
```

### 4. Utility Commands

#### System Information
```bash
doptools info
```

#### Initialize Configuration
```bash
doptools init
```

## Input File Format

Input files should be CSV/TSV with columns containing:
- SMILES strings (molecular structures)
- Molecule IDs (optional)

Example CSV:
```csv
SMILES,ID,Activity
CC,ethane,1.2
CCO,ethanol,2.1
CCC,propane,0.8
```

## Output

Descriptor calculations output CSV files with:
- Molecule IDs (if provided)
- Calculated descriptors as columns

## Examples

### Basic CircuS Descriptors
```bash
# Simple CircuS calculation
doptools descriptors circus -i molecules.csv -o circus_desc.csv

# With custom radius range
doptools descriptors circus -i molecules.csv -o circus_desc.csv --lower 1 --upper 2
```

### Fingerprint Calculation
```bash
# Morgan fingerprints
doptools descriptors rdkit -i molecules.csv -o morgan_fp.csv --fp-type morgan --nbits 2048

# RDKit fingerprints
doptools descriptors rdkit -i molecules.csv -o rdkit_fp.csv --fp-type rdkfp
```

### Complex Multi-column Analysis
```bash
# Process multiple descriptor types
doptools descriptors complex -i molecules.csv -o complex_desc.csv --descriptor-type fingerprinter
```

## Error Handling

The CLI provides helpful error messages and validation:
- File format validation
- SMILES structure checking
- Parameter validation

Use the `-v/--verbose` flag for detailed output during processing.

## Getting Help

```bash
# Main help
doptools --help

# Command-specific help
doptools descriptors --help
doptools descriptors circus --help
```