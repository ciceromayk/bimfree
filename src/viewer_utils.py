# src/viewer_utils.py
import ifcopenshell
import ifcopenshell.geom
import numpy as np

def process_ifc_file(ifc_file_path):
    # Configurações para a geração da geometria
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True) # Use o motor OpenCASCADE
    
    # Abrir o arquivo IFC
    ifc_file = ifcopenshell.open(ifc_file_path)
    
    # Dicionários para armazenar os dados da geometria
    vertices = []
    faces = []
    
    # Iterar sobre todos os elementos de produto (ex: paredes, lajes, colunas)
    products = ifc_file.by_type('IfcProduct')
    
    # Contador para os índices das faces
    start_face_index = 0
    
    # Processar cada elemento
    for product in products:
        try:
            shape = ifcopenshell.geom.create_shape(settings, product)
            geometry = shape.geometry
            
            # Converter a geometria para arrays do numpy
            verts = np.array(geometry.verts).reshape((-1, 3))
            tris = np.array(geometry.faces).reshape((-1, 3))
            
            # Adicionar a geometria ao conjunto de dados global
            vertices.extend(verts.tolist())
            
            # Reajustar os índices das faces para o novo conjunto de vértices
            new_faces = tris + start_face_index
            faces.extend(new_faces.tolist())
            
            # Atualizar o índice inicial para o próximo elemento
            start_face_index += len(verts)
            
        except Exception as e:
            # Pula elementos que não possuem geometria ou que geram erro
            print(f"Erro ao processar o elemento {product.GlobalId}: {e}")
            continue

    if not vertices:
        return None, None
        
    return vertices, faces
