# Proyecto_MetroMadrid

## Descripción General

Este proyecto modela y resuelve rutas óptimas en la red del Metro de Madrid utilizando grafos y algoritmos de búsqueda. Permite consultar estaciones, calcular rutas más cortas y visualizar resultados en un mapa interactivo mediante una interfaz web desarrollada con Streamlit.

---

## Fundamentos Matemáticos y Algorítmicos

### Representación del Grafo

- **Vértices:** Cada estación del metro es un nodo, identificado por su nombre y coordenadas (x, y).
- **Aristas:** Cada conexión directa entre estaciones es una arista, ponderada por la distancia euclidiana entre las estaciones conectadas.

#### Cálculo de Distancias

La distancia entre dos estaciones se calcula con la fórmula euclidiana:

```python
def distancia_euclidiana(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
```

#### Algoritmo de Búsqueda

Para encontrar la ruta más corta entre dos estaciones se emplea el **algoritmo de Dijkstra**:

- Se inicializan los costes mínimos desde el origen a cada nodo.
- Se exploran los vecinos de cada nodo, actualizando los costes acumulados.
- Se reconstruye la ruta óptima al finalizar la búsqueda.

#### Construcción del Grafo

El grafo se construye a partir del archivo `etiquetas_grafos_metro_PRO.csv`, donde cada fila representa una estación, sus vecinos y coordenadas. Las aristas se crean solo entre estaciones adyacentes en la misma línea.

---

## Funcionalidades

- **Visualización de estaciones:** Consulta de información detallada de cada estación, incluyendo coordenadas y vecinos.
- **Búsqueda de estaciones:** Por nombre, vecinos o coordenadas.
- **Cálculo de rutas óptimas:** Encuentra la ruta más corta entre dos estaciones, mostrando la secuencia de estaciones y la distancia total.
- **Visualización en mapa:** Muestra la ruta calculada sobre un mapa interactivo.

---

## Estructura del Proyecto

- `app.py`: Interfaz principal con Streamlit.
- `MetroMadrid_Grafo.py`: Lógica de grafos, búsqueda y utilidades matemáticas.
- `ruta_map.py`: Funciones para visualización en mapas.
- `etiquetas_grafos_metro_PRO.csv`: Datos de estaciones y conexiones.
- `data/`: Archivos auxiliares y datos GTFS.
- Documentos PDF y diagramas: Explicaciones teóricas y diagramas de flujo.

---

## Ejecución del Proyecto

### Requisitos

- Python 3.8 o superior
- Paquetes: `streamlit`, `pandas`, `streamlit_folium`

Instala las dependencias con:

```sh
pip install streamlit pandas streamlit_folium
```

### Ejecución

Desde la raíz del proyecto, ejecuta:

```sh
streamlit run app.py
```

Esto abrirá la interfaz web en tu navegador, donde podrás:

- Buscar estaciones por nombre, vecinos o coordenadas.
- Calcular y visualizar rutas óptimas.
- Explorar el grafo del Metro de Madrid.

---

## Documentación y Referencias

- **ENTREGA MENSUAL - GRAFO METRO DE MADRID.pdf:** Explicación teórica y matemática del modelado del grafo.
- **MetroMadrid_Grafo_BUSCAR_CAMINO_INFORME.pdf:** Detalles del algoritmo de búsqueda de caminos.
- **Grafo_metro_madrid - Diagrama Flujo.png:** Diagrama de flujo del sistema.

---

**Autor:**  
Jose Suárez & Miguel Ángel Mascaró

**Licencia:**  
Todos los derechos tanto personales como comerciales quedan reservados en exclusiva a los creadores del contenido mostrado.