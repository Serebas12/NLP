import streamlit as st
import pandas as pd
import pydeck as pdk
from Functions import funciones_proyecto

# Configuración inicial
n_top = 30

def main():
    # Coordenadas por defecto
    coord_persona_default = [4.628363, -74.064807]  

    # Activación de funciones
    funcion = funciones_proyecto()

    # Título y descripción con algo de estilo
    st.title('TastyMap - Sabor en Palabras')
    st.markdown("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">""", unsafe_allow_html=True)

    # Cargar la información desde el archivo CSV
    resumen = pd.read_csv("C:/Users/jssaa/OneDrive/Documentos/sebastian saavedra/Maestria/Semestre 2024 02/NLP/Proyecto/resumen_streamlit_final.csv", 
                          delimiter=";", encoding='utf8')

    # Campos de entrada para las coordenadas del usuario
    st.subheader("Ajusta tu ubicación")
    col1, col2 = st.columns(2)

    with col1:
        user_lat = st.number_input('Latitud', value=coord_persona_default[0], format="%.3f", step=0.001)

    with col2:
        user_lon = st.number_input('Longitud', value=coord_persona_default[1], format="%.3f", step=0.001)

    # Validación de las coordenadas ingresadas
    if not (-90 <= user_lat <= 90 and -180 <= user_lon <= 180):
        st.error("Por favor, ingresa coordenadas válidas (Latitud entre -90 y 90, Longitud entre -180 y 180).")
        return

    # Actualizar coord_persona con los valores ingresados
    coord_persona = [user_lat, user_lon]

    # Ordenar información y obtener el top según las coordenadas ingresadas
    resumen = funcion.top_ordenado(resumen, n_top, coord_persona=(coord_persona[0], coord_persona[1]))

    # Selección de restaurante
    restaurantes = resumen["Restaurante"].tolist()
    st.subheader("Descubre el mejor restaurante cerca a ti:")
    Restaurante_favorito = st.selectbox('', restaurantes)

    if Restaurante_favorito:
        restaurante_info = resumen[resumen['Restaurante'] == Restaurante_favorito].iloc[0]

        # Usar columnas para organizar la información mejor
        col1, col2 = st.columns(2)

        # Puntos fuertes
        with col1:
            st.subheader("Puntos fuertes:")
            st.markdown(f'<p class="info-text">{restaurante_info["Bueno"]}</p>', unsafe_allow_html=True)

        # Puntos a mejorar
        with col2:
            st.subheader("Puntos a mejorar:")
            st.markdown(f'<p class="info-text">{restaurante_info["Malo"]}</p>', unsafe_allow_html=True)

        # Calificación
        st.subheader("Calificación:")      
        st.markdown(funcion.generate_stars(restaurante_info["Calificacion"]), unsafe_allow_html=True)

        # Review
        st.subheader("Más reviews:")
        st.markdown(f'<a href="{restaurante_info["Reviews"]}" class="link" target="_blank">Clic aquí para leer más reseñas</a>', unsafe_allow_html=True)

        # Mapa
        st.subheader("Mapa de referencia")
        
        # Crear un DataFrame para el mapa
        data = pd.DataFrame({
            'latitude': [restaurante_info['latitude'], coord_persona[0]],
            'longitude': [restaurante_info['longitude'], coord_persona[1]],
            'icon_data': [
                {"url": "https://cdn-icons-png.flaticon.com/512/1046/1046771.png", "width": 128, "height": 128, "anchorY": 128},
                {"url": "https://cdn-icons-png.flaticon.com/512/2353/2353678.png", "width": 128, "height": 128, "anchorY": 128}
            ]
        })

        # Configuración del mapa en Pydeck
        icon_layer = pdk.Layer(
            'IconLayer',
            data,
            get_icon='icon_data',
            get_position=['longitude', 'latitude'],
            get_size=4,
            size_scale=15,
            pickable=True
        )

        # Vista inicial del mapa centrada en las coordenadas ingresadas
        view_state = pdk.ViewState(latitude=coord_persona[0], longitude=coord_persona[1], zoom=14)

        st.pydeck_chart(pdk.Deck(layers=[icon_layer], initial_view_state=view_state))

        # Encuesta
        st.subheader("Encuesta sobre uso de la herramienta")
        st.markdown(f'<a href="https://forms.gle/Cxdu8cKqpN9xsXGt9" class="link" target="_blank">Clic aquí para dejar tu reseña</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
