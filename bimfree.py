import ifcopenshell

def extract_quantities(ifc_file_path):
    # Abra o modelo IFC
    model = ifcopenshell.open(ifc_file_path)

    # Criar uma lista para armazenar os quantitativos
    quantities_list = []

    # Iterar sobre todos os elementos que tenham um tipo geométrico
    for element in model:
        # Verifica se o elemento é um IfcProduct (que tem geometria)
        if 'IfcProduct' in element.is_a():
            quantities = {}

            # Obter o nome e o tipo do elemento
            quantities['Name'] = element.Name
            quantities['Type'] = element.is_a()

            # Tentativa de obter a área ou volume
            if 'Volume' in element.get_info():
                quantities['Volume'] = element.get_info()['Volume']
            elif 'Area' in element.get_info():
                quantities['Area'] = element.get_info()['Area']

            # Adicionar quantitativos à lista
            quantities_list.append(quantities)

    return quantities_list

def main(ifc_file_path):
    quantities = extract_quantities(ifc_file_path)

    # Exibir os quantitativos extraídos
    for qty in quantities:
        print(qty)

if __name__ == "__main__":
    # Substitua 'seuarquivo.ifc' pelo caminho do seu arquivo IFC
    main('seuarquivo.ifc')
