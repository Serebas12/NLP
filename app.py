import streamlit as st
import pandas as pd
import pydeck as pdk

def generate_stars(rating):
    full_stars = int(rating)
    half_star = 1 if (rating - full_stars >= 0.5) else 0
    empty_stars = 5 - full_stars - half_star

    stars_html = '<span style="color: gold;">'
    stars_html += '<i class="fas fa-star"></i> ' * full_stars
    stars_html += '<i class="fas fa-star-half-alt"></i> ' * half_star
    stars_html += '<i class="far fa-star"></i> ' * empty_stars
    stars_html += '</span>'
    return stars_html


def main():
    # Título y descripción con algo de estilo
    st.title('TastyMap - Sabor en Palabras')
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    """, unsafe_allow_html=True)

    # Cargar la información desde el archivo CSV
    resumen = pd.read_csv("C:/Users/jssaa/OneDrive/Documentos/sebastian saavedra/Maestria/Semestre 2024 02/NLP/Proyecto/resumen_pruebas.csv", delimiter=";", encoding='latin1')
    resumen['latitude'] = resumen['latitude'].str.replace(',', '.').astype(float)
    resumen['longitude'] = resumen['longitude'].str.replace(',', '.').astype(float)


    # Selección de restaurante
    restaurantes = resumen["Restaurante"].tolist()
    Restaurante_favorito = st.selectbox('Descubre el mejor restaurante cerca a ti:', restaurantes)

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
        st.markdown(generate_stars(restaurante_info["Calificacion"]), unsafe_allow_html=True)

        # Review
        st.subheader("Más reviews:")
        st.markdown(f'<a href="{restaurante_info["Reviews"]}" class="link" target="_blank">Clic aquí para leer más reseñas</a>', unsafe_allow_html=True)

        # Mapa

        coord_persona=[4.628363, -74.064807]

        st.subheader("Mapa de referencia")
        restaurante_coords = [restaurante_info['latitude'], restaurante_info['longitude']]
        
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

        view_state = pdk.ViewState(latitude=restaurante_info['latitude'], longitude=restaurante_info['longitude'], zoom=14)

        st.pydeck_chart(pdk.Deck(layers=[icon_layer], initial_view_state=view_state))




if __name__ == "__main__":
    main()
