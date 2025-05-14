import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from streamlit.components.v1 import html
from MetroMadrid_Grafo import inicializar_grafo, buscar_vertice, buscar_camino, vertices
from ruta_map import crear_mapa

# Interfaz Streamlit
def main():
    st.set_page_config("Metro de Madrid", layout="wide")
    st.title("🚇 Metro de Madrid")
    st.subheader("Visualiza estaciones, busca rutas y administra el grafo")

    inicializar_grafo()

    tab1, tab2 = st.tabs(["📍 Buscar Estación", "🗺️ Buscar Ruta"])

    with tab1:
        st.header("Buscar estación")
        metodo = st.selectbox("Buscar por:", ["Nombre", "Vecinos", "Coordenadas"])
        if metodo == "Nombre":
            nombre = st.text_input("Introduce el nombre de la estación").upper()
            if nombre and nombre in vertices:
                col1, col2 = st.columns(2)
                with col1:
                    stops_df = pd.read_csv("data/stops_clean.csv")
                    vertices_mapa = {
                        row["stop_name"]: {"x": row["stop_lon"], "y": row["stop_lat"]}
                        for _, row in stops_df.iterrows()
                    }
                    if nombre in vertices_mapa:
                        st.write("Ubicación en el mapa:")
                        st.map(pd.DataFrame({
                            "lat": [vertices_mapa[nombre]["y"]],
                            "lon": [vertices_mapa[nombre]["x"]]
                        }))
                with col2:
                    if nombre in vertices_mapa:
                        st.write(f"Coordenadas de {nombre}:")
                        with st.container():
                            st.markdown(
                                f"""
                                <div style="border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9; color: black; width: fit-content;">
                                    <strong>Latitud: {vertices_mapa[nombre]['y']}</strong><br>
                                </div>
                                """, unsafe_allow_html=True
                            )
                        with st.container():
                            st.markdown(
                                f"""
                                <div style="border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9; color: black; width: fit-content;">
                                    <strong>Longitud: {vertices_mapa[nombre]['x']}</strong><br>
                                </div>
                                """, unsafe_allow_html=True
                            )
                    st.divider()
                    st.write("Estaciones cercanas:")
                    vecinos = vertices[nombre]["vecinos"]
                    vecinos_unicos = list(set(vecinos)) 
                    for vecino in vecinos_unicos:
                        with st.container():
                            st.markdown(
                                f"""
                                <div style="border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9; color: black; width: fit-content;">
                                    <strong>Nombre: {vecino}</strong><br>
                                </div>
                                """, unsafe_allow_html=True
                            )
        elif metodo == "Vecinos":
            vecinos_input = st.text_input("Introduce vecinos separados por coma").upper()
            vecinos = [v.strip() for v in vecinos_input.split(",")]
            nombre, resultado = buscar_vertice(None, vecinos, None)
            if resultado:
                st.write(f"Estación encontrada: {nombre}")
                st.json(resultado)
            else:
                st.error("No se encontró ninguna estación con esos vecinos.")
        elif metodo == "Coordenadas":
            x = st.number_input("Coordenada X", value=0)
            y = st.number_input("Coordenada Y", value=0)
            nombre, resultado = buscar_vertice(None, None, [x, y])
            if resultado:
                st.write(f"Estación encontrada: {nombre}")
                st.json(resultado)
            else:
                st.error("No se encontró ninguna estación con esas coordenadas.")

    with tab2:
        st.header("Buscar la ruta más corta")
        origen = st.selectbox("Estación de origen", list(vertices.keys()))
        destino = st.selectbox("Estación de destino", list(vertices.keys()))
        if st.button("Calcular ruta"):
            ruta, distancia = buscar_camino(origen, destino)
            st.success(f"Ruta encontrada: {' ➡️ '.join(ruta)}")
            st.info(f"Distancia total: {distancia:.2f} unidades")
            
            try:
                mapa = crear_mapa(ruta)  
                html(mapa._repr_html_(), height=500, scrolling=False)
            except Exception as e:
                st.error("❌ Error al generar el mapa.")
                st.code(str(e), language="python")

if __name__ == "__main__":
    main()
