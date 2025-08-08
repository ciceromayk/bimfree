import streamlit as st
import ifcopenshell
import pandas as pd
from pythreejs import *

# Função para listar materiais únicos
def listar_materiais(ifc_file):
    materiais = set()
    for material in ifc_file.by_type("IfcMaterial"):
        if material.Name:
            materiais.add(material.Name)
    return list(materiais)

# Função para extrair elementos para visualização
def extrair_elementos(ifc_file):
    elementos = []
    for elem in ifc_file.by_type("IfcProduct"):
        nome = getattr(elem, 'Name', 'Sem nome')
        global_id = getattr(elem, 'GlobalId', 'Sem ID')
        # Pode incluir geometria ou atributos adicionais aqui
        elementos.append({'Nome': nome, 'GlobalId': global_id})
    return elementos

# Função para extrair quantitativos e atributos adicionais
def extrair_quantitativos(ifc_file):
    quant_data = []
    for qty_set in ifc_file.by_type("IfcQuantitySet"):
        for qty in qty_set.Quantities:
            material_nome = getattr(qty_set, 'Name', 'Sem nome')
            quantidade = getattr(qty, 'Quantity', None)
            nome_qty = getattr(qty, 'Name', 'Sem nome')
            # Extração de volume, área, comprimento se disponíveis
            volume = getattr(qty, 'Volume', None)
            area = getattr(qty, 'Area', None)
            comprimento = getattr(qty, 'Length', None)
            quant_data.append({
                'Material': material_nome,
                'Quantidade': quantidade,
                'Nome Quantidade': nome_qty,
                'Volume': volume,
                'Área': area,
                'Comprimento': comprimento
            })
    return pd.DataFrame(quant_data)

# Função para criar uma visualização 3D básica usando pythreejs
def criar_visualizacao_3d():
    esfera = Mesh(
        SphereGeometry(radius=1, widthSegments=32, heightSegments=32),
        MeshBasicMaterial(color='blue')
    )
    cubo = Mesh(
        BoxGeometry(width=1, height=1, depth=1),
        MeshBasicMaterial(color='red')
    )
    scene = Scene(children=[esfera, cubo])
    camera = PerspectiveCamera(position=[3, 3, 3], fov=50,
                               children=[DirectionalLight(color='#ffffff', position=[3, 5, 1], intensity=0.5)])
    renderer = Renderer(camera=camera, scene=scene, controls=[OrbitControls(controlling=camera)],
                        width=600, height=400)
    # Retorna o HTML do visualizador
    return renderer._repr_html_()

# Interface Streamlit
st.title("Visualizador e Extrator de Materiais de Arquivo IFC com Visualização 3D")
uploaded_file = st.file_uploader("Faça upload do arquivo IFC", type=["ifc"])

if uploaded_file:
    # Salvar arquivo temporariamente
    with open("temp.ifc", "wb") as f:
        f.write(uploaded_file.read())
    try:
        # Abrir o IFC
        ifc_model = ifcopenshell.open("temp.ifc")
        st.success("Arquivo IFC carregado com sucesso!")

        # Listar materiais únicos
        materiais = listar_materiais(ifc_model)
        st.subheader("Materiais presentes no modelo")
        st.write(materiais)

        # Extrair elementos para visualização
        elementos = extrair_elementos(ifc_model)
        df_elementos = pd.DataFrame(elementos)
        st.subheader("Elementos do Modelo")
        st.dataframe(df_elementos)

        # Visualização 3D
        st.subheader("Visualização 3D do Modelo")
        html_visualizacao = criar_visualizacao_3d()
        st.components.v1.html(html_visualizacao, height=400)

        # Extrair e mostrar quantitativos com volume, área, comprimento
        df_quantitativos = extrair_quantitativos(ifc_model)
        if not df_quantitativos.empty:
            st.subheader("Quantitativos de Materiais")
            st.dataframe(df_quantitativos)
        else:
            st.info("Nenhum dado de quantitativos encontrado.")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo IFC: {e}")
else:
    st.info("Por favor, envie um arquivo IFC para análise.")
