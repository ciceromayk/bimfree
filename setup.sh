#!/bin/bash

# Exibe uma mensagem para o log de implantação
echo "Iniciando a instalação do ifcopenshell..."

# URL do arquivo .whl pre-compilado para Python 3.9 e Linux
WHEEL_URL="https://github.com/IfcOpenShell/IfcOpenShell/releases/download/v0.7.0/ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl"

# Use o comando `uv` para instalar diretamente o arquivo binário
uv pip install "$WHEEL_URL"

echo "Instalação do ifcopenshell concluída."
