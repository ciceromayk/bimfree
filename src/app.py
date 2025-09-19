# src/app.py
import streamlit as st
import plotly.graph_objects as go
from viewer_utils import process_ifc_file

st.title("BIM Viewer Online")
st.write("Carregue seu arquivo IFC para visualizar o modelo 3D.")

uploaded_file = st.file_uploader("Escolha um arquivo IFC...", type=["ifc"])

if uploaded_file is not None:
    # Salvar o arquivo temporariamente para o ifcopenshell poder ler
    with open("temp.ifc", "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner('Processando modelo...'):
        vertices, faces = process_ifc_file("temp.ifc")

    if vertices and faces:
        st.success("Modelo processado com sucesso!")
        
        # Criar o objeto de visualização 3D com Plotly
        fig = go.Figure(
            data=[
                go.Mesh3d(
                    x=[v[0] for v in vertices],
                    y=[v[1] for v in vertices],
                    z=[v[2] for v in vertices],
                    i=[f[0] for f in faces],
                    j=[f[1] for f in faces],
                    k=[f[2] for f in faces],
                    color='lightblue', # Cor padrão do modelo
                    opacity=0.8,
                )
            ]
        )
        
        # Opcional: ajustar layout para uma melhor visualização 3D
        fig.update_layout(
            scene_aspectmode='data',
            scene=dict(
                xaxis=dict(showbackground=False, showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showbackground=False, showgrid=False, zeroline=False, visible=False),
                zaxis=dict(showbackground=False, showgrid=False, zeroline=False, visible=False),
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("O arquivo IFC não contém geometria visível para ser renderizada.")
