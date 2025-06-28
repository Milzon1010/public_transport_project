
import requests
import pandas as pd
from itertools import combinations
import random

# 🔑 1. Contoh URL API publik yang menyediakan data titik (diganti jika ada API asli)
# Untuk simulasi kita gunakan data dummy dari JSON placeholder
# Ganti URL ini ke API kamu kalau sudah ada data titik real
SAMPLE_DATA = [
    {"nama": "Monas", "longitude": 106.8272, "latitude": -6.1754},
    {"nama": "Gambir", "longitude": 106.8300, "latitude": -6.1778},
    {"nama": "Tanah Abang", "longitude": 106.8112, "latitude": -6.1865},
    {"nama": "Cikini", "longitude": 106.8384, "latitude": -6.1970},
    {"nama": "Senen", "longitude": 106.8500, "latitude": -6.1705},
    {"nama": "Menteng", "longitude": 106.8323, "latitude": -6.1900},
    {"nama": "Kemayoran", "longitude": 106.8651, "latitude": -6.1496}
]

df = pd.DataFrame(SAMPLE_DATA)

# 🎲 2. Ambil 5 titik secara acak
sampled = df.sample(n=5, random_state=42).reset_index(drop=True)

# 🔁 3. Hitung jarak pairwise antar titik
API_KEY = "5b3ce3597851110001cf6248e644fd9d109a413697b6963b173c72ef"

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
        print(f"❌ Error: {e}")
        return None

results = []
pairs = list(combinations(sampled.index, 2))

for i, j in pairs:
    row_a = sampled.loc[i]
    row_b = sampled.loc[j]
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

df_result = pd.DataFrame(results)
print("\n📍 Pairwise Distance Table (Random 5 Points):")
print(df_result)
df_result.to_csv("random_pairwise_distance.csv", index=False)
print("\n✅ Saved to random_pairwise_distance.csv")
