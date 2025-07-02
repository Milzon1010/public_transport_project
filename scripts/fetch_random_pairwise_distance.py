import requests
import pandas as pd
from itertools import combinations

SAMPLE_DATA = [
    {"nama": "Monas", "longitude": 106.8272, "latitude": -6.1754},
    {"nama": "Gambir", "longitude": 106.8300, "latitude": -6.1778},
    {"nama": "Tanah Abang", "longitude": 106.8112, "latitude": -6.1865},
    {"nama": "Cikini", "longitude": 106.8384, "latitude": -6.1970},
    {"nama": "Senen", "longitude": 106.8500, "latitude": -6.1705},
    {"nama": "Menteng", "longitude": 106.8323, "latitude": -6.1900},
    {"nama": "Kemayoran", "longitude": 106.8651, "latitude": -6.1496}
]

API_KEY = "5b3ce3597851110001cf6248e644fd9d109a413697b6963b173c72ef"
df = pd.DataFrame(SAMPLE_DATA)

pairs = list(combinations(df.index, 2))
results = []
for i, j in pairs:
    row_a = df.loc[i]
    row_b = df.loc[j]
    coord_a = [row_a["longitude"], row_a["latitude"]]
    coord_b = [row_b["longitude"], row_b["latitude"]]
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {'Authorization': API_KEY, 'Content-Type': 'application/json'}
    body = {"coordinates": [coord_a, coord_b]}
    try:
        response = requests.post(url, json=body, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        jarak = data["routes"][0]["summary"]["distance"]
    except Exception as e:
        print(f"❌ Error: {e}")
        jarak = None
    results.append({
        "nama_A": row_a["nama"], "nama_B": row_b["nama"],
        "long_A": coord_a[0], "lat_A": coord_a[1],
        "long_B": coord_b[0], "lat_B": coord_b[1],
        "jarak_A_B (meter)": jarak
    })
df_result = pd.DataFrame(results)
df_result.to_csv("random_pairwise_distance.csv", index=False)
print("✅ Saved: random_pairwise_distance.csv")
