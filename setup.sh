#!/bin/bash

echo "Starting ifcopenshell installation..."

# URL of the pre-compiled .whl file for Python 3.9 and Linux
WHEEL_URL="https://github.com/IfcOpenShell/IfcOpenShell/releases/download/v0.7.0/ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl"
WHEEL_FILE="ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl"

# Use wget to download the wheel file
wget -q --show-progress "$WHEEL_URL" -O "$WHEEL_FILE"

echo "Downloaded ifcopenshell wheel file."

# Use the correct Python environment's pip to install the downloaded file
python -m pip install "$WHEEL_FILE"

echo "ifcopenshell installation completed."
