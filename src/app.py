# src/app.py
import streamlit as st
import plotly.graph_objects as go
import tempfile
import os

from viewer_utils import process_ifc_file

# Configurações da página: usa a largura total para a visualização
st.set_page_config(layout="wide")

# Título e cabeçalho na parte principal da página
st.title("BIM Viewer Online")
st.write("Carregue um arquivo IFC no menu lateral para visualizar o modelo 3D.")

# O uploader de arquivo e a lógica de processamento ficam no menu lateral
with st.sidebar:
    st.header("Carregar Modelo")
    uploaded_file = st.file_uploader("Escolha um arquivo IFC...", type=["ifc"])

    if uploaded_file is not None:
        # Cria um arquivo temporário para o IfcOpenShell ler
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ifc") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        # Adiciona o spinner de carregamento enquanto o arquivo é processado
        with st.spinner('Processando modelo...'):
            try:
                # Chama a função de processamento do modelo
                vertices, faces = process_ifc_file(tmp_path)

                if vertices and faces:
                    st.success("Modelo processado com sucesso!")
                    
                    # Cria o objeto de visualização 3D com Plotly
                    fig = go.Figure(
                        data=[
                            go.Mesh3d(
                                x=[v[0] for v in vertices],
                                y=[v[1] for v in vertices],
                                z=[v[2] for v in vertices],
                                i=[f[0] for f in faces],
                                j=[f[1] for f in faces],
                                k=[f[2] for f in faces],
                                color='lightblue',
                                opacity=0.8,
                            )
                        ]
                    )

                    # Ajusta o layout para uma melhor visualização 3D
                    fig.update_layout(
                        scene_aspectmode='data',
                        scene=dict(
                            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, visible=False),
                            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, visible=False),
                            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, visible=False),
                        )
                    )
                    
                    # Exibe o gráfico na tela principal
                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.warning("O arquivo IFC não contém geometria visível para ser renderizada.")
            
            except Exception as e:
                st.error(f"Erro ao processar o arquivo: {e}")
            
            finally:
                # Remove o arquivo temporário
                os.remove(tmp_path)
