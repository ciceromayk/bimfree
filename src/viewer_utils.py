# src/viewer_utils.py
import ifcopenshell

def process_ifc_file(ifc_file_path):
    model = ifcopenshell.open(ifc_file_path)
    # Lógica para iterar sobre as entidades do modelo (ex: IfcBuildingElementProxy, IfcWall)
    # e extrair informações como geometria, cor e propriedades.
    # Utilize a biblioteca ifcopenshell para essa tarefa.
    # A complexidade aqui dependerá do nível de detalhe necessário.
    # O retorno pode ser uma estrutura de dados (ex: dicionário ou DataFrame)
    # que contenha as informações para visualização.
    return model # ou uma estrutura de dados mais simples
