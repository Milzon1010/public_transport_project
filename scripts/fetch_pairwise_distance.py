
import requests
import pandas as pd
from itertools import combinations

# 🔑 1. Konfigurasi API & Titik Lokasi Jakarta Pusat
API_KEY = "5b3ce3597851110001cf6248e644fd9d109a413697b6963b173c72ef"

locations = pd.DataFrame({
    "nama": ["Monas", "Gambir", "Tanah Abang", "Cikini", "Senen"],
    "longitude": [106.8272, 106.8300, 106.8112, 106.8384, 106.8500],
    "latitude": [-6.1754, -6.1778, -6.1865, -6.1970, -6.1705],
    "kota": ["Jakarta Pusat"] * 5
})

# 🔄 2. Buat kombinasi pasangan titik (tanpa duplikat, tidak bolak-balik)
pairs = list(combinations(locations.index, 2))

# 🔁 3. Fungsi untuk hitung jarak dari ORS API
def get_distance(api_key, coord_a, coord_b):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": [coord_a, coord_b]
    }
    try:
        response = requests.post(url, json=body, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["routes"][0]["summary"]["distance"]
    except Exception as e:
        print(f"❌ Error fetching route {coord_a} -> {coord_b}: {e}")
        return None

# 📊 4. Loop kombinasi dan simpan hasil jarak
results = []
for i, j in pairs:
    row_a = locations.loc[i]
    row_b = locations.loc[j]
    coord_a = [row_a["longitude"], row_a["latitude"]]
    coord_b = [row_b["longitude"], row_b["latitude"]]
    distance = get_distance(API_KEY, coord_a, coord_b)
    results.append({
        "nama_A": row_a["nama"],
        "nama_B": row_b["nama"],
        "long_A": coord_a[0],
        "lat_A": coord_a[1],
        "long_B": coord_b[0],
        "lat_B": coord_b[1],
        "jarak_A_B (meter)": distance
    })

# 💾 5. Tampilkan dan simpan ke CSV
df_pairs = pd.DataFrame(results)
print("\n📍 Pairwise Distance Table:")
print(df_pairs)

df_pairs.to_csv("pairwise_distance_jakpus.csv", index=False)
print("\n✅ Saved to pairwise_distance_jakpus.csv")
