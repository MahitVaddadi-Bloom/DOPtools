#!/usr/bin/env python3
"""
DOPtools Command Line Interface

A comprehensive CLI for molecular descriptor calculation, model optimization,
and chemical analysis using DOPtools.
"""

import click
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

import doptools
from doptools.chem import (
    ChythonCircus, ChythonLinear, Fingerprinter, ComplexFragmentor,
    PassThrough, SolventVectorizer, ColorAtom
)
from doptools.estimators.consensus import ConsensusModel
from doptools.estimators.ad_estimators import FragmentControl, BoundingBox, PipelineWithAD


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    """
    DOPtools - Molecular descriptors and model optimization toolkit
    
    A comprehensive toolkit for calculating molecular descriptors,
    optimizing machine learning models, and analyzing chemical data.
    """
    ctx.ensure_object(dict)


@cli.group()
def descriptors():
    """Calculate molecular descriptors from chemical structures."""
    pass


@cli.group()
def models():
    """Model optimization and analysis tools."""
    pass


@cli.group()
def analysis():
    """Chemical analysis and visualization tools."""
    pass


@descriptors.command()
@click.option('--input', '-i', 'input_file', required=True,
              help='Input file containing SMILES (CSV, TSV, or TXT)')
@click.option('--output', '-o', 'output_file', required=True,
              help='Output file for descriptors (CSV)')
@click.option('--smiles-column', default='SMILES',
              help='Column name containing SMILES (default: SMILES)')
@click.option('--id-column', default='ID',
              help='Column name containing molecule IDs (default: ID)')
@click.option('--lower', default=0, type=int,
              help='Lower bound for CircuS descriptor radius (default: 0)')
@click.option('--upper', default=3, type=int,
              help='Upper bound for CircuS descriptor radius (default: 3)')
@click.option('--on-bond', is_flag=True,
              help='Calculate bond-centered descriptors instead of atom-centered')
@click.option('--separator', default='\t',
              help='Input file separator (default: tab)')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def circus(input_file, output_file, smiles_column, id_column, lower, upper, 
           on_bond, separator, verbose):
    """Calculate CircuS molecular descriptors."""
    try:
        if verbose:
            click.echo(f"Loading data from {input_file}...")
        
        # Load input data
        df = pd.read_csv(input_file, sep=separator)
        
        if smiles_column not in df.columns:
            raise click.ClickException(f"Column '{smiles_column}' not found in input file")
        
        if verbose:
            click.echo(f"Loaded {len(df)} molecules")
            click.echo(f"Calculating CircuS descriptors (radius {lower}-{upper})...")
        
        # Calculate CircuS descriptors
        circus_calc = ChythonCircus(
            lower=lower, 
            upper=upper, 
            on_bond=on_bond,
            fmt='smiles'
        )
        
        # Fit and transform
        smiles_data = df[smiles_column].tolist()
        circus_calc.fit(smiles_data)
        descriptors = circus_calc.transform(smiles_data)
        
        # Add IDs if available
        if id_column in df.columns:
            descriptors.insert(0, 'ID', df[id_column])
        else:
            descriptors.insert(0, 'ID', range(len(descriptors)))
        
        # Save results
        descriptors.to_csv(output_file, index=False)
        
        if verbose:
            click.echo(f"Calculated {descriptors.shape[1]-1} descriptors")
            click.echo(f"Results saved to {output_file}")
            
    except Exception as e:
        raise click.ClickException(f"Error calculating CircuS descriptors: {str(e)}")


@descriptors.command()
@click.option('--input', '-i', 'input_file', required=True,
              help='Input file containing SMILES (CSV, TSV, or TXT)')
@click.option('--output', '-o', 'output_file', required=True,
              help='Output file for descriptors (CSV)')
@click.option('--smiles-column', default='SMILES',
              help='Column name containing SMILES (default: SMILES)')
@click.option('--id-column', default='ID',
              help='Column name containing molecule IDs (default: ID)')
@click.option('--fp-type', default='morgan',
              type=click.Choice(['morgan', 'atompairs', 'torsion', 'rdkfp', 'avalon']),
              help='Fingerprint type (default: morgan)')
@click.option('--nbits', default=1024, type=int,
              help='Number of bits in fingerprint (default: 1024)')
@click.option('--radius', default=2, type=int,
              help='Radius for Morgan fingerprints (default: 2)')
@click.option('--separator', default='\t',
              help='Input file separator (default: tab)')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def rdkit(input_file, output_file, smiles_column, id_column, fp_type, nbits, 
          radius, separator, verbose):
    """Calculate RDKit molecular descriptors and fingerprints."""
    try:
        if verbose:
            click.echo(f"Loading data from {input_file}...")
        
        # Load input data
        df = pd.read_csv(input_file, sep=separator)
        
        if smiles_column not in df.columns:
            raise click.ClickException(f"Column '{smiles_column}' not found in input file")
        
        if verbose:
            click.echo(f"Loaded {len(df)} molecules")
            click.echo(f"Calculating {fp_type} descriptors...")
        
        # Calculate RDKit descriptors
        fingerprinter = Fingerprinter(
            fp_type=fp_type,
            nBits=nbits,
            radius=radius,
            fmt='smiles'
        )
        
        # Transform
        smiles_data = df[smiles_column].tolist()
        descriptors = fingerprinter.transform(smiles_data)
        
        # Convert to DataFrame
        desc_df = pd.DataFrame(descriptors)
        
        # Add IDs if available
        if id_column in df.columns:
            desc_df.insert(0, 'ID', df[id_column])
        else:
            desc_df.insert(0, 'ID', range(len(desc_df)))
        
        # Save results
        desc_df.to_csv(output_file, index=False)
        
        if verbose:
            click.echo(f"Calculated {desc_df.shape[1]-1} descriptors")
            click.echo(f"Results saved to {output_file}")
            
    except Exception as e:
        raise click.ClickException(f"Error calculating RDKit descriptors: {str(e)}")


@descriptors.command()
@click.option('--config', '-c', 'config_file', required=True,
              help='JSON configuration file for complex descriptor setup')
@click.option('--input', '-i', 'input_file', required=True,
              help='Input file containing molecular data')
@click.option('--output', '-o', 'output_file', required=True,
              help='Output file for combined descriptors')
@click.option('--separator', default='\t',
              help='Input file separator (default: tab)')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def complex(config_file, input_file, output_file, separator, verbose):
    """Calculate complex multi-column descriptors using ComplexFragmentor."""
    try:
        if verbose:
            click.echo(f"Loading configuration from {config_file}...")
        
        # Load configuration
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        if verbose:
            click.echo(f"Loading data from {input_file}...")
        
        # Load input data
        df = pd.read_csv(input_file, sep=separator)
        
        if verbose:
            click.echo(f"Loaded {len(df)} rows")
            click.echo("Setting up ComplexFragmentor...")
        
        # Create ComplexFragmentor from config
        fragmentor = ComplexFragmentor(**config)
        
        # Transform data
        descriptors = fragmentor.transform(df)
        
        # Save results
        descriptors.to_csv(output_file, index=False)
        
        if verbose:
            click.echo(f"Calculated {descriptors.shape[1]} total descriptors")
            click.echo(f"Results saved to {output_file}")
            
    except Exception as e:
        raise click.ClickException(f"Error calculating complex descriptors: {str(e)}")


@models.command()
@click.option('--config', '-c', 'config_file', required=True,
              help='JSON configuration file for model optimization')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def optimize(config_file, verbose):
    """Optimize machine learning models using Optuna."""
    try:
        if verbose:
            click.echo(f"Loading optimization configuration from {config_file}...")
        
        # Use the existing launch_optimizer functionality
        import sys
        original_argv = sys.argv
        sys.argv = ['launch_optimizer', '--config', config_file]
        
        if verbose:
            sys.argv.append('--verbose')
        
        click.echo("Optimization functionality to be implemented")
        sys.argv = original_argv
        
    except Exception as e:
        raise click.ClickException(f"Error during model optimization: {str(e)}")


@models.command()
@click.option('--input-dir', '-i', 'input_dir', required=True,
              help='Directory containing model data')
@click.option('--output-dir', '-o', 'output_dir', required=True,
              help='Output directory for rebuilt models')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def rebuild(input_dir, output_dir, verbose):
    """Rebuild and analyze existing models."""
    try:
        if verbose:
            click.echo(f"Rebuilding models from {input_dir}...")
        
        # Use the existing rebuilder functionality
        import sys
        original_argv = sys.argv
        sys.argv = ['rebuilder', '--input', input_dir, '--output', output_dir]
        
        if verbose:
            sys.argv.append('--verbose')
        
        click.echo("Model rebuilding functionality to be implemented")
        sys.argv = original_argv
        
    except Exception as e:
        raise click.ClickException(f"Error during model rebuilding: {str(e)}")


@analysis.command()
@click.option('--model-file', '-m', required=True,
              help='Trained model file (pickle)')
@click.option('--smiles', '-s', required=True,
              help='SMILES string to analyze')
@click.option('--descriptor-type', default='circus',
              type=click.Choice(['circus', 'morgan', 'rdkfp']),
              help='Descriptor type used for the model (default: circus)')
@click.option('--output', '-o', 'output_file', 
              help='Output image file (PNG, SVG)')
@click.option('--show', is_flag=True,
              help='Display the visualization')
def coloratom(model_file, smiles, descriptor_type, output_file, show):
    """Visualize atomic contributions to model predictions."""
    try:
        import pickle
        
        # Load model
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
        
        click.echo(f"Analyzing SMILES: {smiles}")
        
        # Create ColorAtom instance
        if descriptor_type == 'circus':
            descriptor = ChythonCircus(lower=0, upper=3, fmt='smiles')
            descriptor.fit([smiles])
        elif descriptor_type == 'morgan':
            descriptor = Fingerprinter(fp_type='morgan', nBits=1024, fmt='smiles')
        else:
            descriptor = Fingerprinter(fp_type='rdkfp', nBits=1024, fmt='smiles')
        
        # Create ColorAtom visualization
        coloratom = ColorAtom(model, descriptor)
        
        # Generate visualization
        fig = coloratom.explain(smiles)
        
        if output_file:
            fig.savefig(output_file, dpi=300, bbox_inches='tight')
            click.echo(f"Visualization saved to {output_file}")
        
        if show:
            fig.show()
            
    except Exception as e:
        raise click.ClickException(f"Error creating ColorAtom visualization: {str(e)}")


@analysis.command()
@click.option('--input', '-i', 'input_file', required=True,
              help='Input data file for plotting')
@click.option('--plot-type', default='scatter',
              type=click.Choice(['scatter', 'histogram', 'correlation']),
              help='Type of plot to generate')
@click.option('--x-column', help='X-axis column name')
@click.option('--y-column', help='Y-axis column name')
@click.option('--output', '-o', 'output_file',
              help='Output image file')
@click.option('--show', is_flag=True,
              help='Display the plot')
def plot(input_file, plot_type, x_column, y_column, output_file, show):
    """Generate plots for data analysis."""
    try:
        # Use the existing plotter functionality
        import sys
        original_argv = sys.argv
        
        args = ['plotter', '--input', input_file, '--type', plot_type]
        
        if x_column:
            args.extend(['--x-column', x_column])
        if y_column:
            args.extend(['--y-column', y_column])
        if output_file:
            args.extend(['--output', output_file])
        if show:
            args.append('--show')
        
        sys.argv = args
        click.echo("Plotting functionality to be implemented")
        sys.argv = original_argv
        
    except Exception as e:
        raise click.ClickException(f"Error generating plot: {str(e)}")


@cli.command()
@click.option('--descriptor-type', default='circus',
              type=click.Choice(['circus', 'rdkit', 'complex']),
              help='Type of descriptor configuration to generate')
@click.option('--output', '-o', 'output_file', default='doptools_config.json',
              help='Output configuration file')
def init(descriptor_type, output_file):
    """Initialize configuration files for DOPtools."""
    try:
        if descriptor_type == 'circus':
            config = {
                "name": "CircuS Descriptors",
                "description": "Basic CircuS molecular descriptors",
                "descriptor": {
                    "type": "circus",
                    "lower": 0,
                    "upper": 3,
                    "on_bond": False,
                    "fmt": "smiles"
                }
            }
        elif descriptor_type == 'rdkit':
            config = {
                "name": "RDKit Descriptors",
                "description": "RDKit molecular fingerprints",
                "descriptor": {
                    "type": "rdkit",
                    "fp_type": "morgan",
                    "nBits": 1024,
                    "radius": 2,
                    "fmt": "smiles"
                }
            }
        elif descriptor_type == 'complex':
            config = {
                "name": "Complex Multi-Column Descriptors",
                "description": "ComplexFragmentor for multiple molecular columns",
                "associator": [
                    ["molecules", {"type": "circus", "lower": 0, "upper": 2}]
                ],
                "structure_columns": ["molecules"],
                "fmt": "smiles"
            }
        
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        click.echo(f"Configuration file created: {output_file}")
        click.echo(f"Edit this file to customize your {descriptor_type} setup")
        
    except Exception as e:
        raise click.ClickException(f"Error creating configuration: {str(e)}")


@cli.command()
def info():
    """Display DOPtools version and system information."""
    try:
        import platform
        import sklearn
        import pandas as pd
        import numpy as np
        
        click.echo("DOPtools System Information")
        click.echo("=" * 30)
        click.echo(f"DOPtools version: {doptools.__version__ if hasattr(doptools, '__version__') else 'Unknown'}")
        click.echo(f"Python version: {platform.python_version()}")
        click.echo(f"Platform: {platform.platform()}")
        click.echo()
        click.echo("Dependencies:")
        click.echo(f"  pandas: {pd.__version__}")
        click.echo(f"  numpy: {np.__version__}")
        click.echo(f"  scikit-learn: {sklearn.__version__}")
        
        try:
            import chython
            click.echo(f"  chython: Available")
        except ImportError:
            click.echo(f"  chython: Not available")
        
        try:
            import rdkit
            click.echo(f"  rdkit: Available")
        except ImportError:
            click.echo(f"  rdkit: Not available")
            
    except Exception as e:
        raise click.ClickException(f"Error getting system info: {str(e)}")


if __name__ == '__main__':
    cli()