import streamlit as st
import ifcopenshell
import os
import tempfile

st.title("Visualizador IFC para GLB")

uploaded_file = st.file_uploader("Envie um arquivo IFC", type=["ifc"])

if uploaded_file is not None:
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
            st.error(f"Erro ao abrir o arquivo IFC: {e}")
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

            st.success("Conversão IFC para GLB realizada com sucesso!")

            # Exibe visualizador 3D externo
            st.markdown("### Visualização 3D do Modelo")
            viewer_url = f"https://3dviewer.net/#model={glb_path}"
            st.components.v1.iframe(viewer_url, height=600, scrolling=True)

        except Exception as e:
            st.error("Erro ao tentar converter para GLB. Provavelmente o módulo `geom` não está disponível.")
            st.code(f"{e}", language="python")
            st.markdown("**⚠️ Dica:** Tente usar uma versão do `ifcopenshell` com suporte ao `geom`. Veja [instruções aqui](https://github.com/IfcOpenShell/IfcOpenShell).")
