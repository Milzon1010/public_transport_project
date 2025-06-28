
import requests
import pandas as pd
import folium

def fetch_route_geometry(api_key, start, end):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": [start, end]
    }

    try:
        response = requests.post(url, json=body, headers=headers, timeout=5)
        print(f"📡 HTTP Status: {response.status_code}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching route geometry: {e}")
        return None


def create_route_map(geojson_data, output_path="route_map.html"):
    try:
        # Ambil koordinat tengah rute untuk posisi tengah peta
        coords = geojson_data["features"][0]["geometry"]["coordinates"]
        mid_index = len(coords) // 2
        mid_point = coords[mid_index][::-1]  # reverse to (lat, lon)

        route_map = folium.Map(location=mid_point, zoom_start=13)
        folium.GeoJson(geojson_data, name="route").add_to(route_map)
        folium.LayerControl().add_to(route_map)
        route_map.save(output_path)

        print(f"🗺️ Route map saved to {output_path}")

    except Exception as e:
        print(f"❌ Error generating map: {e}")


if __name__ == "__main__":
    API_KEY = "5b3ce3597851110001cf6248e644fd9d109a413697b6963b173c72ef"

    print("=== Visual Route Map Generator ===")
    start_input = input("Enter start coordinates (lon,lat): ").strip()
    end_input = input("Enter end coordinates (lon,lat): ").strip()

    try:
        start_coords = [float(x) for x in start_input.split(",")]
        end_coords = [float(x) for x in end_input.split(",")]
    except:
        print("❌ Invalid coordinate format.")
        exit()

    geo_data = fetch_route_geometry(API_KEY, start_coords, end_coords)
    if geo_data:
        create_route_map(geo_data)
