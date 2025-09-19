#!/bin/bash

# Define the Python version. Streamlit Cloud uses Python 3.9 or higher.
PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

# Define the ifcopenshell wheel URL for a common Python 3.9 Linux build
# NOTE: You may need to change this URL if a new version is released or a different Python version is used.
# Check the official IfcOpenShell releases page for the latest URL.
IFCOPENSHELL_WHEEL_URL="https://github.com/IfcOpenShell/IfcOpenShell/releases/download/v0.7.0/ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl"

echo "Installing IfcOpenShell from URL: $IFCOPENSHELL_WHEEL_URL"
pip install --no-index --find-links https://github.com/IfcOpenShell/IfcOpenShell/releases $IFCOPENSHELL_WHEEL_URL

echo "IfcOpenShell installation complete."
