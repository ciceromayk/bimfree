import streamlit as st
import ifcopenshell

def load_ifc(file_content):
    try:
        ifc_file = ifcopenshell.file(schema="IFC4")
        ifc_file.read(file_content)
        return ifc_file
    except:
        st.error("Erro ao ler o arquivo IFC")

st.title("Visualização de Arquivos IFC Online")

uploaded_file = st.file_uploader("Escolha um arquivo IFC", type=["ifc"])

if uploaded_file is not None:
    model = load_ifc(uploaded_file.getvalue())
    if model:
        projects = model.by_type("IfcProject")
        if projects:
            st.write("Nome do Projeto:", projects[0].Name)
        else:
            st.error("Nenhum projeto encontrado no arquivo.")
else:
    st.info("Por favor, faça upload de um arquivo IFC.")
