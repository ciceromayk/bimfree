# Usa uma imagem base Python oficial que é compatível com Streamlit
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de dependência para o contêiner
COPY requirements.txt .

# Instala as dependências Python
# O IfcOpenShell requer bibliotecas de sistema, então as instalaremos aqui
# A linha RUN abaixo pode ser adaptada, dependendo da necessidade de pacotes APT
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Agora, instalamos o ifcopenshell usando o mesmo método do script setup.sh
# A URL pode precisar ser atualizada para a versão mais recente
RUN wget https://github.com/IfcOpenShell/IfcOpenShell/releases/download/v0.7.0/ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl \
    && pip install ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl \
    && rm ifcopenshell-0.7.0-cp39-cp39-manylinux_2_17_x86_64.whl

# Instala as outras bibliotecas do seu requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da sua aplicação para o contêiner
COPY . .

# Expõe a porta que o Streamlit usa (8501 por padrão)
EXPOSE 8501

# Comando para rodar a aplicação Streamlit
CMD ["streamlit", "run", "src/app.py"]
