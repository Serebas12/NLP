from geopy.distance import geodesic

class funciones_proyecto:

    def __init__(self):
        pass

    def generate_stars(self, rating):
        full_stars = int(rating)
        half_star = 1 if (rating - full_stars >= 0.5) else 0
        empty_stars = 5 - full_stars - half_star

        stars_html = '<span style="color: gold;">'
        stars_html += '<i class="fas fa-star"></i> ' * full_stars
        stars_html += '<i class="fas fa-star-half-alt"></i> ' * half_star
        stars_html += '<i class="far fa-star"></i> ' * empty_stars
        stars_html += '</span>'
        
        return stars_html

    def calculate_distance(self, row, person_coords):
        restaurant_coords = (row['latitude'], row['longitude'])
        distance = geodesic(restaurant_coords, person_coords).kilometers  # devuelve la distancia en kilómetros
        
        return distance
    
    def top_ordenado(self,df,top,coord_persona):
        df['distancia'] = df.apply(self.calculate_distance, args=(coord_persona,), axis=1)
        df= df.sort_values(by='distancia', ascending=True )
        df= df.head(top)
        df= df.sort_values(by='Calificacion', ascending=False )

        return df
