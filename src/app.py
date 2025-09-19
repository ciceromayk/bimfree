# src/app.py
import streamlit as st
import plotly.graph_objects as go
from viewer_utils import process_ifc_file # Importe a função

st.title("BIM Viewer Online")
st.write("Carregue seu arquivo IFC para visualizar o modelo 3D.")

uploaded_file = st.file_uploader("Escolha um arquivo IFC...", type=["ifc"])

if uploaded_file is not None:
    with open("temp.ifc", "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        model = process_ifc_file("temp.ifc")

        # Lógica para converter o modelo IFC em dados para o Plotly
        # Isso pode envolver a criação de um `go.Mesh3d` para representar as geometrias

        # Exemplo simplificado de visualização com Plotly (lógica de conversão precisa ser implementada)
        fig = go.Figure(data=[go.Mesh3d(
            # Lógica para extrair e preencher vértices e faces
            x=[], y=[], z=[],
            #...
        )])

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
