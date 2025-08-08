import streamlit as st
import os

# Configuração da página
st.set_page_config(page_title="IFC to GLB Converter", page_icon=":building:", layout="wide")

st.sidebar.title("Visualizador IFC")
st.sidebar.markdown("Faça upload do seu arquivo IFC para visualizar.")

uploaded_file = st.sidebar.file_uploader("Escolha um arquivo IFC", type=["ifc"])

# Verifica se um arquivo foi carregado
if uploaded_file is not None:
    st.sidebar.success("Arquivo carregado com sucesso!")
    
    # Salva o arquivo carregado como um arquivo temporário
    uploaded_file_path = os.path.join(os.getcwd(), 'temp_model.ifc')
    with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Estrutura HTML/JavaScript com uma referência atualizada ao arquivo IFC
    viewer_html_code = f"""
    <html>
    <head>
        <script type="module">
            import {{ IfcViewerAPI }} from 'https://cdn.jsdelivr.net/npm/@ifcjs/viewer@3.0.0/dist/index.js';

            const container = document.getElementById('viewer');
            const viewer = new IfcViewerAPI({{ container, backgroundColor: new THREE.Color(0xffffff) }});
            viewer.addAxes();
            viewer.addGrid();

            async function loadIfcUrl() {{
                await viewer.IFC.loadIfcUrl('{uploaded_file_path}');
                viewer.fitToFrame();
            }}

            loadIfcUrl();
        </script>
        <style>
            #viewer {{
                width: 100%;
                height: 800px;
                border: 1px solid #ccc;
            }}
        </style>
    </head>
    <body>
        <div id="viewer"></div>
    </body>
    </html>
    """

    # Renderiza o HTML
    st.components.v1.html(viewer_html_code, height=800)
else:
    st.sidebar.warning("Por favor, carregue um arquivo IFC.")
