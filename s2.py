from s2sphere import CellId, Cell, LatLng, RegionCoverer, LatLngRect
import folium

import pandas as pd
df = pd.read_csv("kildare_poi.csv") 
pois = df.to_dict(orient="records")

# Kildare Town center
center_lat = 53.1586
center_lng = -6.9096

# Bounding box size (in degrees)
lat_delta = 0.02
lng_delta = 0.03

# Create bounding box around Kildare Town
p1 = LatLng.from_degrees(center_lat - lat_delta, center_lng - lng_delta)
p2 = LatLng.from_degrees(center_lat + lat_delta, center_lng + lng_delta)
rect = LatLngRect.from_point_pair(p1, p2)

# Function to get all S2 cell IDs for a given level over a region
def get_s2_cells_in_region(rect, level):
    coverer = RegionCoverer()
    coverer.min_level = level
    coverer.max_level = level
    coverer.max_cells = 500  # Reasonable limit
    return coverer.get_covering(rect)

# Get S2 cells at levels 14 and 17
cells_L14 = get_s2_cells_in_region(rect, 14)
cells_L17 = get_s2_cells_in_region(rect, 17)

# Function to convert CellId to polygon corners
def get_cell_polygon(cell_id):
    cell = Cell(cell_id)
    corners = []
    for i in range(4):
        vertex = cell.get_vertex(i)
        latlng = LatLng.from_point(vertex)
        corners.append((latlng.lat().degrees, latlng.lng().degrees))
    corners.append(corners[0])  # close polygon
    return corners

# Create base map centered on Kildare
m = folium.Map(location=[center_lat, center_lng], zoom_start=15)

# Draw Level 14 cells (red)
for cell_id in cells_L14:
    polygon = get_cell_polygon(cell_id)
    folium.Polygon(
        locations=polygon,
        color='purple',
        fill=False,
        weight=4,
        opacity=0.9,
        tooltip=f"L14: {cell_id.id()}"
    ).add_to(m)

# Draw Level 17 cells (blue)
for cell_id in cells_L17:
    polygon = get_cell_polygon(cell_id)
    folium.Polygon(
        locations=polygon,
        color='blue',
        fill=False,
        weight=1,
        tooltip=f"L17: {cell_id.id()}"
    ).add_to(m)

# Add PokéStops and Gyms as markers
for poi in pois:
    color = "blue" if poi["type"] == "PokéStop" else "green"
    icon = "🔵" if poi["type"] == "PokéStop" else "🔴"
    
    folium.Marker(
        location=[poi["lat"], poi["lng"]],
        popup=f"{icon} {poi['name']} ({poi['type']})",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)


# Save the map
m.save("kildare_s2.html")

