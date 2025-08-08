import streamlit as st
import os
import base64

# Configuração da página
st.set_page_config(page_title="IFC to GLB Converter", page_icon=":building:", layout="wide")

st.sidebar.title("Visualizador IFC")
st.sidebar.markdown("Faça upload do seu arquivo IFC para visualizar.")

uploaded_file = st.sidebar.file_uploader("Escolha um arquivo IFC", type=["ifc"])

# Verifica se um arquivo foi carregado
if uploaded_file is not None:
    st.sidebar.success("Arquivo carregado com sucesso!")
    
    # Lê o arquivo carregado e encode em base64
    file_content = uploaded_file.getvalue()
    encoded_file = base64.b64encode(file_content).decode('utf-8')
    file_name = uploaded_file.name

    # Estrutura HTML/JavaScript usando Blob para carregar o IFC
    viewer_html_code = f"""
    <html>
    <head>
        <script type="module">
            import {{ IfcViewerAPI }} from 'https://cdn.jsdelivr.net/npm/@ifcjs/viewer@3.0.0/dist/index.js';

            const container = document.getElementById('viewer');
            const viewer = new IfcViewerAPI({{ container, backgroundColor: new THREE.Color(0xffffff) }});
            viewer.addAxes();
            viewer.addGrid();

            async function loadIfc() {{
                const response = await fetch('data:application/octet-stream;base64,{encoded_file}');
                const ifcBlob = await response.blob();
                const ifcURL = URL.createObjectURL(ifcBlob);
                await viewer.IFC.loadIfcUrl(ifcURL);
                viewer.fitToFrame();
            }}

            loadIfc();
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
