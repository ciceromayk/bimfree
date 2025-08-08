import streamlit as st
import ifcopenshell
import ifcopenshell.geom
import pandas as pd
import os
import uuid
import tempfile

from streamlit.components.v1 import html

st.set_page_config(page_title="Visualizador IFC 3D", layout="wide")
st.title("Visualizador IFC com Extração de Dados e Visualização 3D")

# ------------------------------
# Funções auxiliares
# ------------------------------

def listar_materiais(ifc_file):
    materiais = set()
    for material in ifc_file.by_type("IfcMaterial"):
        if material.Name:
            materiais.add(material.Name)
    return sorted(list(materiais))

def extrair_elementos(ifc_file):
    elementos = []
    for elem in ifc_file.by_type("IfcProduct"):
        nome = getattr(elem, 'Name', 'Sem nome')
        global_id = getattr(elem, 'GlobalId', 'Sem ID')
        tipo = elem.is_a()
        elementos.append({'Nome': nome, 'GlobalId': global_id, 'Tipo': tipo})
    return elementos

def extrair_quantitativos(ifc_file):
    quant_data = []
    for qty_set in ifc_file.by_type("IfcElementQuantity"):
        nome_set = getattr(qty_set, 'Name', 'Sem nome')
        for qty in qty_set.Quantities:
            quant_data.append({
                'Nome do conjunto': nome_set,
                'Nome da Quantidade': getattr(qty, 'Name', ''),
                'Comprimento': getattr(qty, 'Length', None),
                'Área': getattr(qty, 'Area', None),
                'Volume': getattr(qty, 'Volume', None),
                'Quantidade genérica': getattr(qty, 'Quantity', None),
            })
    return pd.DataFrame(quant_data)

def exportar_glb(ifc_file, caminho_saida):
    # Configuração do contexto geométrico
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    scene = ifcopenshell.geom.utils.initialize_scene()
    
    for product in ifc_file.by_type("IfcProduct"):
        try:
            shape = ifcopenshell.geom.create_shape(settings, product)
            if shape.geometry:
                ifcopenshell.geom.utils.add_to_scene(scene, shape)
        except:
            continue

    # Exportar para GLB
    ifcopenshell.geom.utils.export_gltf(scene, caminho_saida)
    return caminho_saida

def carregar_visualizador_glb(path_glb):
    viewer_html = f"""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.150.1/examples/js/loaders/GLTFLoader.js"></script>
    </head>
    <body style="margin:0;">
    <div id="container" style="width:100%; height:100vh;"></div>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('container').appendChild(renderer.domElement);
        
        const light = new THREE.HemisphereLight(0xffffff, 0x444444);
        scene.add(light);

        const loader = new THREE.GLTFLoader();
        loader.load("{path_glb}", function(gltf) {{
            scene.add(gltf.scene);
            camera.position.set(5, 5, 5);
            const animate = function () {{
                requestAnimationFrame(animate);
                renderer.render(scene, camera);
            }};
            animate();
        }});
    </script>
    </body>
    </html>
    """
    html(viewer_html, height=600)

# ------------------------------
# UPLOAD IFC
# ------------------------------

st.sidebar.header("Upload do Arquivo IFC")
uploaded_file = st.sidebar.file_uploader("Selecione um arquivo IFC", type=["ifc"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ifc") as temp_ifc:
        temp_ifc.write(uploaded_file.read())
        temp_ifc_path = temp_ifc.name

    try:
        ifc_model = ifcopenshell.open(temp_ifc_path)
        st.success("Arquivo IFC carregado com sucesso!")

        # Exportar GLB
        caminho_glb = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.glb")
        exportar_glb(ifc_model, caminho_glb)
        url_glb = f"file://{caminho_glb}"  # Não funciona em Streamlit Cloud, apenas local

        # Extrair dados
        materiais = listar_materiais(ifc_model)
        elementos = extrair_elementos(ifc_model)
        df_elementos = pd.DataFrame(elementos)
        df_quantitativos = extrair_quantitativos(ifc_model)

        # Interface com Tabs
        tab1, tab2, tab3 = st.tabs(["📦 Materiais", "📊 Elementos IFC", "📐 Quantitativos"])

        with tab1:
            st.subheader("Materiais encontrados")
            st.write(materiais)

        with tab2:
            tipos_unicos = sorted(df_elementos["Tipo"].unique())
            filtro_tipo = st.sidebar.multiselect("Filtrar por Tipo", tipos_unicos, default=tipos_unicos)
            df_filtrado = df_elementos[df_elementos["Tipo"].isin(filtro_tipo)]
            st.subheader("Elementos do modelo")
            st.dataframe(df_filtrado)

        with tab3:
            if not df_quantitativos.empty:
                st.subheader("Quantitativos extraídos")
                st.dataframe(df_quantitativos)
                st.download_button("📥 Baixar planilha", data=df_quantitativos.to_csv(index=False),
                                   file_name="quantitativos.csv", mime="text/csv")
            else:
                st.info("Nenhum quantitativo encontrado no modelo.")

        # Visualização 3D
        st.subheader("Visualização 3D do Modelo IFC (.glb)")
        st.info("A visualização funciona localmente. Em ambiente online, você precisa subir o GLB para um servidor.")
        carregar_visualizador_glb(url_glb)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo IFC: {e}")
else:
    st.info("Por favor, envie um arquivo IFC para análise.")
