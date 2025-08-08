import streamlit as st
import ifcopenshell
import pandas as pd

# Função para extrair materiais únicos do arquivo IFC
def listar_materiais(ifc_file):
    materiais = set()
    for material in ifc_file.by_type("IfcMaterial"):
        if material.Name:
            materiais.add(material.Name)
    return list(materiais)

# Função para extrair uma visualização simples (exemplo: lista de elementos)
def extrair_elementos(ifc_file):
    elementos = []
    for elem in ifc_file.by_type("IfcProduct"):
        nome = getattr(elem, 'Name', 'Sem nome')
        global_id = getattr(elem, 'GlobalId', 'Sem ID')
        elementos.append({'Nome': nome, 'GlobalId': global_id})
    return elementos

# Interface Streamlit
st.title("Visualizador e Extrator de Materiais de Arquivo IFC")
uploaded_file = st.file_uploader("Faça upload do arquivo IFC", type=["ifc"])

if uploaded_file:
    # Carregar o arquivo IFC
    with open("temp.ifc", "wb") as f:
        f.write(uploaded_file.read())
    try:
        ifc_model = ifcopenshell.open("temp.ifc")
        st.success("Arquivo IFC carregado com sucesso!")

        # Listar materiais únicos
        materiais = listar_materiais(ifc_model)
        st.subheader("Materiais presentes no modelo")
        st.write(materiais)

        # Listar elementos para visualização básica
        elementos = extrair_elementos(ifc_model)
        df_elementos = pd.DataFrame(elementos)
        st.subheader("Elementos do Modelo")
        st.dataframe(df_elementos)

        # Opcional: visualização 3D básica (exemplo simples com lista de elementos)
        # Para visualizações mais avançadas, seria necessário integrar com um visualizador 3D externo ou usar bibliotecas específicas.
        # Aqui, apenas mostramos uma lista de elementos como base.

    except Exception as e:
        st.error(f"Erro ao processar o arquivo IFC: {e}")
else:
    st.info("Por favor, envie um arquivo IFC para análise.")
