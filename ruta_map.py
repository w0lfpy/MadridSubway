import folium
import pandas as pd

# Cargar datos de estaciones
stops_df = pd.read_csv("data/stops_clean.csv")
data_address = pd.read_csv("etiquetas_grafos_metro_PRO.csv")

# Crear diccionario de vértices (estaciones)
vertices_mapa = {
    row["stop_name"]: {"x": row["stop_lon"], "y": row["stop_lat"]}
    for _, row in stops_df.iterrows()
}

lineas_estaciones = {
    row["nombre"]: row["linea"] for _, row in data_address.iterrows()
}

colores_lineas = {
    "1": "#0072BC",
    "2": "#C60C30",
    "3": "#FFD200",
    "4": "#A05A2C",
    "5": "#009739",
    "6": "#A8A9AD",
    "7": "#F58220",
    "8": "#E30585",
    "9": "#92278F",
    "10": "#003DA5",
    "11": "#006D5D",
    "12": "#BFD730",
    "R": "#6E6E6E"
}

def crear_mapa(ruta=None):
    # Calcular el centro del mapa
    centro_lat = stops_df["stop_lat"].mean()
    centro_lon = stops_df["stop_lon"].mean()
    centro = [centro_lat, centro_lon]

    mapa = folium.Map(location=centro, zoom_start=12)
    
    if ruta:
        # Agregar marcadores solo para las estaciones en la ruta
        for idx, est in enumerate(ruta):
            info = vertices_mapa[est]
            folium.Marker(
                location=[info["y"], info["x"]],
                popup=est,
                tooltip=est,
                icon=folium.Icon(color="gray")
            ).add_to(mapa)

        # Dibujar líneas entre estaciones con color por línea
        for i in range(len(ruta) - 1):
            est_actual = ruta[i]
            est_siguiente = ruta[i + 1]
            coord_actual = [vertices_mapa[est_actual]["y"], vertices_mapa[est_actual]["x"]]
            coord_siguiente = [vertices_mapa[est_siguiente]["y"], vertices_mapa[est_siguiente]["x"]]

            # Suponemos que ambas estaciones están en la misma línea
            linea = lineas_estaciones.get(est_actual)
            color = colores_lineas.get(linea)

            folium.PolyLine(
                locations=[coord_actual, coord_siguiente],
                color=color,
                weight=6,
                opacity=0.9
            ).add_to(mapa)

    return mapa

def agregar_ruta_al_mapa(mapa, ruta):
    coordenadas = [[vertices_mapa[est]["y"], vertices_mapa[est]["x"]] for est in ruta]
    folium.PolyLine(locations=coordenadas, color='red', weight=5, opacity=0.7).add_to(mapa)
