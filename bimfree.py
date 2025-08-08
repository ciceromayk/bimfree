import streamlit as st
import ifcopenshell
import os
import tempfile

# Definindo cores e estilo
PRIMARY_COLOR = "#007BFF"
SECONDARY_COLOR = "#6C757D"
SUCCESS_COLOR = "#28A745"
ERROR_COLOR = "#DC3545"
BACKGROUND_COLOR = "#F8F9FA"

st.set_page_config(
    page_title="IFC to GLB Converter",
    page_icon=":building:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {BACKGROUND_COLOR};
        }}
        .stButton>button {{
            color: white;
            background-color: {PRIMARY_COLOR};
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }}
        .stButton>button:hover {{
            background-color: {SECONDARY_COLOR};
        }}
        .stFileUploader label {{
            color: {PRIMARY_COLOR};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar para configurações
with st.sidebar:
    st.title("IFC to GLB Converter")
    st.markdown("Upload your IFC file to convert it to GLB format for 3D visualization.")
    uploaded_file = st.file_uploader("Choose an IFC file", type=["ifc"])

# Main area
st.markdown(
    f"""
    <h1 style='text-align: center; color: {PRIMARY_COLOR};'>
        IFC to GLB Converter
    </h1>
    """,
    unsafe_allow_html=True,
)

if uploaded_file is not None:
    with st.spinner("Processing file..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            ifc_path = os.path.join(tmpdir, "modelo.ifc")
            glb_path = os.path.join(tmpdir, "modelo.glb")

            # Salva o arquivo IFC no diretório temporário
            with open(ifc_path, "wb") as f:
                f.write(uploaded_file.read())

            # Tenta carregar o arquivo IFC
            try:
                ifc_model = ifcopenshell.open(ifc_path)
            except Exception as e:
                st.error(f"Error opening IFC file: {e}")
                st.stop()

            # Tentativa de converter IFC → GLB
            try:
                import ifcopenshell.geom as geom

                # Configuração do ambiente de geometria
                settings = geom.settings()
                settings.set(settings.USE_WORLD_COORDS, True)

                from ifcopenshell.geom.utils import initialize_processor, finalize_processor, add_shape, export_gltf

                scene = initialize_processor(settings)
                for element in ifc_model.by_type("IfcProduct"):
                    try:
                        shape = geom.create_shape(settings, element)
                        add_shape(scene, shape)
                    except:
                        pass

                export_gltf(scene, glb_path)
                finalize_processor(scene)

                st.success("IFC to GLB conversion successful!", icon="✅")

                # Exibe visualizador 3D externo
                st.markdown("### 3D Model Visualization")
                viewer_url = f"https://3dviewer.net/#model={glb_path}"
                st.components.v1.iframe(viewer_url, height=600, scrolling=True)

            except Exception as e:
                st.error("Error converting to GLB. The `geom` module may not be available.", icon="🚨")
                st.code(f"{e}", language="python")
                st.markdown("**⚠️ Tip:** Try using an `ifcopenshell` version with `geom` support. See [instructions here](https://github.com/IfcOpenShell/IfcOpenShell).")
