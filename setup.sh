#!/bin/bash

echo "Attempting to install ifcopenshell from a pre-compiled wheel file."

# This URL is for a specific version and Python environment.
# It points to a build that is known to work on Debian-based systems.
# This is more reliable than using --find-links.
WHEEL_URL="https://github.com/IfcOpenShell/IfcOpenShell/releases/download/v0.7.0/ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl"

# Use a direct pip install command
pip install "$WHEEL_URL"

echo "ifcopenshell installation script finished."
