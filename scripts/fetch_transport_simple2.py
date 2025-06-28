
import requests

# 🔑 1. Konfigurasi API & Koordinat
API_KEY = "5b3ce3597851110001cf6248e644fd9d109a413697b6963b173c72ef"
START = [106.8272, -6.1754]  # Monas
END = [106.7816, -6.2607]    # Blok M

# 🌐 2. Ambil Data Rute dari API
def fetch_route(api_key, start, end):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
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
        print("✅ API success.")
        return response.json()
    except Exception as e:
        print(f"❌ Error accessing ORS API: {e}")
        return None

# 🧾 3. Tampilkan & Simpan Hasil
def show_and_save(data):
    if not data or 'routes' not in data:
        print("❌ No route data found.")
        return

    route = data['routes'][0]
    summary = route['summary']
    steps = route['segments'][0]['steps']

    print(f"📍 Distance: {summary['distance']} meters")
    print(f"⏱️ Duration: {summary['duration']} seconds")

    print("\n🧭 Instructions:")
    for i, step in enumerate(steps, start=1):
        print(f"{i}. {step['instruction']} ({step['distance']} m)")

    with open("route_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Distance: {summary['distance']} meters\n")
        f.write(f"Duration: {summary['duration']} seconds\n\n")
        f.write("Instructions:\n")
        for i, step in enumerate(steps, start=1):
            f.write(f"{i}. {step['instruction']} ({step['distance']} m)\n")

    print("\n💾 Saved to route_summary.txt")

# 🚀 4. Jalankan
if __name__ == "__main__":
    data = fetch_route(API_KEY, START, END)
    if data:
        show_and_save(data)
