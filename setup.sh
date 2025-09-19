#!/bin/bash

echo "Iniciando a instalação do ifcopenshell..."

# URL do arquivo binário pré-compilado para o ambiente do Streamlit Cloud
# Esta versão é compatível com Python 3.9 e sistemas Linux (Debian)
WHEEL_URL="https://github.com/IfcOpenShell/IfcOpenShell/releases/download/v0.7.0/ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl"
WHEEL_FILE="ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl"

# Comando para baixar o arquivo .whl de forma direta e silenciosa
# -q: modo silencioso
# -O: salva o arquivo com o nome especificado
wget -q "$WHEEL_URL" -O "$WHEEL_FILE"

echo "Arquivo .whl baixado com sucesso."

# Comando para instalar o pacote usando o pip do ambiente virtual
# O `python -m pip` garante que o pip correto do ambiente virtual seja usado
python -m pip install "$WHEEL_FILE"

echo "ifcopenshell instalado com sucesso."
