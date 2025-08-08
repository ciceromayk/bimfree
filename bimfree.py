import streamlit as st

# Configuração da página
st.set_page_config(page_title="IFC to GLB Converter", page_icon=":building:", layout="wide")

st.sidebar.title("Visualizador IFC")
st.sidebar.markdown("Faça upload do seu arquivo IFC para visualizar.")

uploaded_file = st.sidebar.file_uploader("Escolha um arquivo IFC", type=["ifc"])

# Verifica se um arquivo foi carregado
if uploaded_file is not None:
    st.sidebar.success("Arquivo carregado com sucesso!")
    
    # Cria um URL temporário para carregar no IFC.js
    with open("temp_model.ifc", "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Estrutura HTML/JavaScript para carregar o IFC.js
    viewer_html_code = """
    <html>
    <head>
        <script type="module">
            import { IfcViewerAPI } from 'https://cdn.jsdelivr.net/npm/@ifcjs/viewer@3.0.0/dist/index.js';

            const container = document.getElementById('viewer');
            const viewer = new IfcViewerAPI({ container, backgroundColor: new THREE.Color(0xffffff) });
            viewer.addAxes();
            viewer.addGrid();

            async function loadIfcUrl() {
                await viewer.IFC.loadIfcUrl("temp_model.ifc");
                viewer.fitToFrame();
            }

            loadIfcUrl();
        </script>
        <style>
            #viewer {
                width: 100%;
                height: 800px;
                border: 1px solid #ccc;
            }
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
