from s2sphere import CellId, Cell, LatLng, RegionCoverer, LatLngRect
import folium
from folium.plugins import MousePosition

import pandas as pd
df = pd.read_csv("kildare_poi.csv") 
pois = df.to_dict(orient="records")


# Kildare Town center
center_lat = 53.1586
center_lng = -6.9096

# Bounding box size (in degrees)
lat_delta = 0.03
lng_delta = 0.08

# Create bounding box around Kildare Town
p1 = LatLng.from_degrees(center_lat - lat_delta, center_lng - lng_delta)
p2 = LatLng.from_degrees(center_lat + lat_delta, center_lng + lng_delta)
rect = LatLngRect.from_point_pair(p1, p2)

# Function to get all S2 cell IDs for a given level over a region
def get_s2_cells_in_region(rect, level):
    coverer = RegionCoverer()
    coverer.min_level = level
    coverer.max_level = level
    coverer.max_cells = 300  # Reasonable limit
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

# Create base map centered on Kildare (OSM as default)
#m = folium.Map(location=[center_lat, center_lng], zoom_start=15, tiles="OpenStreetMap", name="OpenStreetMap")
m = folium.Map(location=[center_lat, center_lng], zoom_start=15, tiles=None)


# Cursor Lat & Long pos
MousePosition(
    position="bottomright",
    separator=" | ",
    prefix="Lat/Lng:",
    lat_formatter="function(num) {return L.Util.formatNum(num, 5);}",
    lng_formatter="function(num) {return L.Util.formatNum(num, 5);}",
).add_to(m)


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

# Tint L17 for number of stops/gyms/non-stops per cell

from collections import defaultdict

# Build POI counts per L17 S2 cell
# Add a tool tip at cursor showing count
poi_counts = defaultdict(int)
for poi in pois:
    latlng = LatLng.from_degrees(poi["lat"], poi["lng"])
    cell_id = CellId.from_lat_lng(latlng).parent(17)
    poi_counts[cell_id.id()] += 1


for cell_id in cells_L17:
    cid = cell_id.id()
    count = poi_counts[cid]

    color = (
        "#ff0000" if count >= 3 else
        "#ffa500" if count == 2 else
        "#00ff00" if count == 1 else
        "#cccccc"
    )

    polygon = get_cell_polygon(cell_id)
    folium.Polygon(
        locations=polygon,
        color=color,
        fill=True,
        fill_opacity=0.4,
        weight=1,
        tooltip=f"{count} Items in cell"
    ).add_to(m)
# end Tint & Tool Tip


# Removed this block of blue overlay on L17 for performance 
# Draw Level 17 cells (blue)
#for cell_id in cells_L17:
#    polygon = get_cell_polygon(cell_id)
#    folium.Polygon(
#        locations=polygon,
#        color='blue',
#        fill=False,
#        weight=1,
#        tooltip=f"L17: {cell_id.id()}"
#    ).add_to(m)



# Add PokéStops and Gyms as markers

# Create feature groups for each POI type
gyms = folium.FeatureGroup(name='Gyms')
pokestops = folium.FeatureGroup(name='PokéStops')
nominated = folium.FeatureGroup(name='Nominated')
potential = folium.FeatureGroup(name='Potential')
notpogo = folium.FeatureGroup(name='NotPogo/Unknown')

# show 80m spin radius, off by default
range_fg = folium.FeatureGroup(name="Interaction Ranges", show=False)

# Add markers to appropriate groups
for poi in pois:
    if poi["type"] == "PokéStop":
        color = "blue"
        icon = "🔵"
        group = pokestops
    elif poi["type"] == "Gym":
        color = "red"
        icon = "🔴"
        group = gyms
    elif poi["type"] == "Nominated":
        color = "purple"
        icon = "🟣"
        group = nominated
    elif poi["type"] == "Potential":
        color = "lightgray"
        icon = "💡"
        group = potential
    else:  # NotPogo or unknown
        color = "gray"
        icon = "❔"
        group = notpogo

    note = poi.get('notes')
    note_text = f"<br><br>💡<strong>Notes:</strong> {note}" if isinstance(note, str) and note.strip() else ""
    popup_text = f"{icon} {poi['name']} ({poi['type']}){note_text}"

    marker = folium.Marker(
        location=[poi["lat"], poi["lng"]],
        popup=popup_text,
        icon=folium.Icon(color=color, icon="info-sign")
    )
    group.add_child(marker)


    #Add interaction circle
    folium.Circle(
        location=[poi["lat"], poi["lng"]],
        radius=80,
        color=color,
        weight=0.5,
        fill=True,
        fill_color=color,
        fill_opacity=0.10
     ).add_to(range_fg)



# Add all groups to the map
gyms.add_to(m)
pokestops.add_to(m)
nominated.add_to(m)
potential.add_to(m)
notpogo.add_to(m)
range_fg.add_to(m) # 80m range per poi

# Add Esri sat
folium.TileLayer(
   	tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr='Esri',
   	name='Esri Satellite',
    overlay=False,
    control=True
).add_to(m)

# Add OpenStreetMap *last* to make it default
folium.TileLayer(
    tiles="OpenStreetMap",
    name="OpenStreetMap",
    overlay=False,
    control=True
).add_to(m)

# Add layer control to toggle groups
folium.LayerControl(collapsed=False).add_to(m)

# Now save the map as usual
m.save("index.html")


# go to current location
from folium.plugins import LocateControl
LocateControl(auto_start=False).add_to(m)


# Save the map
m.save("index.html")



### News panel:

# Inject News panel and toggle button into the generated HTML
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

injection = '''
<button onclick="toggleNews()" style="position: absolute; top: 140px; left: 10px; z-index: 1000;">📰 News/Info</button>
<div id="newsPanel" style="display: none; position: absolute; top: 40px; left: 120px; z-index: 1000; background: #bab6a0; padding: 10px; border: 1px solid #ccc; max-width: 300px;">
  <h3>News</h3>
  <ul>
    <li>PoI: 📍 Grey Abbey Boardwalk bench approved</li>
    <li>PoI: 📍 Firecastle appears on market square</li>
    <li>PoI: 📍 Kildare Derby Legends trail marker 11 of 12 approved</li>
  </ul>
  <h3>Marker Legend</h3>
  <ul>
  <li>🔴 Gym (Red)</li>
  <li>🔵 PokéStop (Blue)</li>
  <li>🟣 Nominated (Pink)</li>
  <li>⚫ Not in Pokémon Go (Black)</li>
  <li>⚫ Potential (Grey)</li>
  </ul>
  <hr noshade>
  Cells with green tint are occupied by one PoI. Orange for two PoI and Red for three plus.<br>
  Only one PoI can (usually!) occupy a L17 cell.
</div>
<script>
function toggleNews() {
  const panel = document.getElementById('newsPanel');
  panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}
</script>
'''

html = html.replace('</body>', injection + '</body>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

