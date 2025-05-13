import pandas as pd
# el directorio donde se guarda el archivo que contiene los datos
data_address = "etiquetas_grafos_metro_PRO.csv"
data = pd.read_csv(data_address)

# Diccionario de vertices y aristas
vertices = {}
aristas = {}

# La distancia entre origen y destino, utilizada como funcion heuristica en la busqueda de caminos
def distancia_euclidiana(origen_x, origen_y, destino_x, destino_y):
    return ((destino_x - origen_x)**2 + (destino_y - origen_y)**2)**(1/2)

# Funcion que crea los vertices del grafo con nombre de la estacion
# Los atributos son las cordenadas de la estacion y sus vecinosº
def crear_vertice(nombre, vecinos, coordenadas_origen):
    x = coordenadas_origen[0]
    y = coordenadas_origen[1]
    if nombre not in vertices:
        vertices[nombre] = {"vecinos": vecinos, "x": x, "y": y}
    else:
        for vecino in vecinos:
            vertices[nombre]["vecinos"].append(vecino)
# Funcion que crea las aristas del grafo
# Tiene como atributos los nombres del origen y destino asi como sus coordenadas respectivas
def crear_arista(origen_nombre, destino_nombre, coordenadas_origen, coordenadas_destino):
    origen_x = coordenadas_origen[0]
    origen_y = coordenadas_origen[1]
    
    destino_x = coordenadas_destino[0]
    destino_y = coordenadas_destino[1]
    
    distancia = distancia_euclidiana(origen_x, origen_y, destino_x, destino_y)
    
    aristas[(origen_nombre, destino_nombre)] = {"distancia": distancia}

# Funcion que elimina un vertice
def eliminar_vertice(vertice):
    try:
        for key, value in vertices[vertice].items():
            if key == "vecinos":
                estacion_anterior = value[0]
                #print(estacion_anterior)
                estacion_siguiente = value[1]
                #print(estacion_siguiente)
                estaciones_vecinos = value
                #print(estaciones_vecinos)
        
        # Elimino las aristas que tienen el vértice como origen
        for arista, info in aristas.copy().items():
            if arista[0] == vertice or arista[1] == vertice:
                del aristas[arista]
        
        # Elimino de los vecinos la estación eliminada
        for estacion in estaciones_vecinos:
            for x, y in vertices[estacion].items():
                if x == "vecinos":
                    y.remove(vertice)
        
        # Añado los nuevos vecinos
        for k, v in vertices[vertice].items():
            if k == "vecinos":
                for i in range(len(v)-1):
                    estacion_anterior = v[i]
                    estacion_siguiente = v[i+1]
                    vertices[estacion_anterior]["vecinos"].append(estacion_siguiente)
                    vertices[estacion_siguiente]["vecinos"].append(estacion_anterior)
                    
        #Elimino la estación deseada
        if vertice in vertices: 
            del vertices[vertice]
        
        print(f"La estación {vertice} ha sido eliminada con éxito")
    except:
        print("La estación introducida no existe!!")

# Funcion que busca un vertice basandose en uno de sus atributos 
def buscar_vertice(nombre, vecinos, coordenadas):
    #Buscar estación por su nombre
    if nombre:
        return nombre, vertices.get(nombre, None)
    #Buscar estación por sus vecinos
    if vecinos:
        for vertice in vertices:
            if vertices[vertice]["vecinos"] == vecinos:
                return vertice, vertices[vertice]
    #Buscar estación por sus coordenadas
    if coordenadas:
        for vertice in vertices:
            if vertices[vertice]["x"] == coordenadas[0] and vertices[vertice]["y"] == coordenadas[1]:
                return vertice, vertices[vertice]
    
# Funcion que calcula el tamaño del grafo teniendo en cuenta el numero de nodos
def calcular_size():
    return len(vertices)

# Funcion f del algoritmo A*
def f(vecino, h):
    return vecino + h

# # Funcion que busca el camino más corto entre dos estaciones utilizando el algoritmo de busqueda A*
def buscar_camino(origen_nombre, destino_nombre):
    origen = vertices[origen_nombre]        
    destino = vertices[destino_nombre]
    
    print("ORIGEN: ", origen)
    print("DESTINO: ", destino)
    
    # La pila utilizada, open_set contiene nodos inexplorados y closed_set contiene nodos explorados
    open_set = {origen_nombre: 0}
    closed_set = set()
    
    # g_values contiene todos los nodos junto con el coste desde el origen
    g_values = {origen_nombre: 0}
    
    # anterior_nodo contiene todos los nodos explorados para después retroceder y crear la ruta
    anterior_nodo = {}
    
    while open_set:
        
        # utilizando una función anónima para extraer de open_set el nodo con la menor coste hasta el destino
        current_node = min(open_set, key=lambda n: f(g_values[n], distancia_euclidiana(vertices[n]["x"], vertices[n]["y"], destino["x"], destino["y"])))
        
        # finalizar el bucle
        if current_node == destino_nombre:
            print("llegao")
            break
        
        # descolar el nodo de la lista y añadirlo a la lista de nodos explorados
        del open_set[current_node]
        closed_set.add(current_node)
        
        
        for vecino in vertices[current_node]["vecinos"]:
            
            # si el vecino ya se ha explorado pasar al próximo vecino
            if vecino in closed_set:
                continue 
            
            # asegurémonos de que la arista exista antes de intentar acceder a ella
            if (current_node, vecino) not in aristas:
                continue
            
            # el valor potencial de g(vecino ), la suma entre el valor g(n) + la distancia euclidiana hasta el vecino
            g_potencial = g_values[current_node] + aristas[(current_node, vecino)]["distancia"]
            
            # Si el vecino no está en la pila añadir para ser explorado y añadir su coste desde el origen
            # Si el vecino sí está en open_set pero el camino encontrado es menor que el que ya está guardado, actualizar g_values
            if vecino not in open_set or g_potencial < g_values[vecino]:
                open_set[vecino] = g_potencial
                g_values[vecino] = g_potencial
                anterior_nodo[vecino] = current_node
    
    ruta = [destino_nombre]
    ruta_distancias = []

    return construir_ruta_recursive(anterior_nodo, origen_nombre, destino_nombre, ruta_distancias, ruta)

# Funcion que retrocede el camino y construye la ruta más corta RECURSIVA
def construir_ruta_recursive(anterior_nodo, origen, destino, ruta_distancias, ruta):
    estacion_anterior = anterior_nodo[destino]    
    if estacion_anterior != origen:
        ruta.append(estacion_anterior)
        ruta_distancias.append(aristas[destino, estacion_anterior]["distancia"])
        
        
        construir_ruta_recursive(anterior_nodo, origen, estacion_anterior, ruta_distancias, ruta)
    else:
        ruta.append(origen)
        ruta_distancias.append(aristas[destino, estacion_anterior]["distancia"])

    
    ruta_distancias_suma = sum(ruta_distancias)
    ruta_revesed = list(reversed(ruta))
    
    return ruta_revesed, ruta_distancias_suma

# Funcion que retrocede el camino y construye la ruta más corta NO RECURSIVA
def construir_ruta(anterior_nodo, origen, destino):
    ruta = [destino]
    ruta_distancia = 0
    
    # Empezando desde el destino se retrocede añadiendo los nodos a la lista de ruta y luego se le da la vuelta
    while destino != origen:
        # estacion final es la ultima estacion en la pila, se iguala a la anterior
        estacion_final = destino
        destino = anterior_nodo[destino]
        estacion_anterior = destino
        
        # estacion final y la anterior se usan para buscar la arista entre ellos y asi sumar su distancia a la distancia de la ruta
        ruta_distancia += aristas[(estacion_final, estacion_anterior)]["distancia"]
        
        ruta.append(destino)
    ruta.reverse()
    
    return ruta, ruta_distancia

# Inicializar grafo
def inicializar_grafo():
    vertices = {}
    for idx in data.index:
        nombre = data.loc[idx, "nombre"]
        coord = (data.loc[idx, "x"], data.loc[idx, "y"])
        vecinos = []

        if idx + 1 < len(data) and data.loc[idx, "linea"] == data.loc[idx + 1, "linea"]:
            vecinos.append(data.loc[idx + 1, "nombre"])
            crear_arista(nombre, data.loc[idx + 1, "nombre"], coord, (data.loc[idx + 1, "x"], data.loc[idx + 1, "y"]))

        if idx - 1 >= 0 and data.loc[idx, "linea"] == data.loc[idx - 1, "linea"]:
            vecinos.append(data.loc[idx - 1, "nombre"])
            crear_arista(nombre, data.loc[idx - 1, "nombre"], coord, (data.loc[idx - 1, "x"], data.loc[idx - 1, "y"]))

        crear_vertice(nombre, vecinos, coord)
