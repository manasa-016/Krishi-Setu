from sqlalchemy import func

EARTH_RADIUS = 6371  # kilometers

def haversine_distance(lat: float, lng: float, lat_column, lng_column):
    return EARTH_RADIUS * func.acos(
        func.cos(func.radians(lat)) *
        func.cos(func.radians(lat_column)) *
        func.cos(func.radians(lng_column) - func.radians(lng)) +
        func.sin(func.radians(lat)) *
        func.sin(func.radians(lat_column))
    )
