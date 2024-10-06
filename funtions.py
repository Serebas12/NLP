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

