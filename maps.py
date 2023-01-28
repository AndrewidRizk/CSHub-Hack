import googlemaps
from datetime import datetime
import folium

# Create a map object centered on New York City
nyc_map = folium.Map(location=[40.693943, -73.985880], zoom_start=13)

# Save the map to an HTML file
nyc_map.save('nyc_map.html')

nyc_map = folium.Map(location=[40.693943, -73.985880], zoom_start=13, api_key='YOUR_API_KEY')

<iframe src="nyc_map.html" width="600" height="450"></iframe>