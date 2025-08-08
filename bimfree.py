import streamlit as st
import ifcopenshell
import pandas as pd

# Função para extrair materiais e seus quantitativos do arquivo IFC
def extrair_materiais(ifc_file):
    materiais = []
    # Buscar todas as entidades de materiais (Material, Quantity, etc.)
    for material in ifc_file.by_type("IfcMaterial"):
        nome_material = material.Name
        # Buscar quantidades relacionadas ao material
        # Aqui, você pode precisar explorar entidades relacionadas, como Quantities
        # Exemplo simples: verificar se há entidades relacionadas
        quantidades = []
        for rel in ifc_file.by_type("IfcQuantitySet"):
            for qty in rel.Quantities:
                if hasattr(qty, 'Name') and hasattr(qty, 'Quantity'):
                    quantidades.append({
                        'Material': nome_material,
                        'Quantidade': qty.Quantity,
                        'Nome Quantidade': qty.Name
                    })
        if quantidades:
            materiais.extend(quantidades)
        else:
            # Caso não encontre quantidade, apenas registre o material
            materiais.append({
                'Material': nome_material,
                'Quantidade': None,
                'Nome Quantidade': None
            })
    return materiais

# Interface Streamlit
st.title("Extrator de Quantitativos de Materiais de Arquivo IFC")
uploaded_file = st.file_uploader("Faça upload do arquivo IFC", type=["ifc"])

if uploaded_file:
    # Carregar o arquivo IFC
    with open("temp.ifc", "wb") as f:
        f.write(uploaded_file.read())
    try:
        ifc_model = ifcopenshell.open("temp.ifc")
        st.success("Arquivo IFC carregado com sucesso!")
        # Extrair materiais
        materiais = extrair_materiais(ifc_model)
        # Converter para DataFrame
        df_materiais = pd.DataFrame(materiais)
        st.write("Materiais e Quantitativos encontrados:")
        st.dataframe(df_materiais)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo IFC: {e}")
else:
    st.info("Por favor, envie um arquivo IFC para análise.")
