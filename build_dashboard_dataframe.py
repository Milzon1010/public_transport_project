import pandas as pd
import random

df_pairwise = pd.read_csv("random_pairwise_distance.csv")
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
hours = list(range(6, 22))  # 6am to 21pm

traffic_data = []
for _, row in df_pairwise.iterrows():
    route_name = f"{row['nama_A']} – {row['nama_B']}"
    lat = (row['lat_A'] + row['lat_B']) / 2
    lon = (row['long_A'] + row['long_B']) / 2
    for day in days:
        for hour in hours:
            # Simulasi rush hour lebih ramai
            if hour in [7,8,9,17,18,19]:
                volume = random.randint(1400, 2200)
            else:
                volume = random.randint(200, 1200)
            # Jalur khusus super padat (misal: Monas – Tanah Abang)
            if route_name in ["Monas – Tanah Abang", "Tanah Abang – Monas"]:
                volume += random.randint(300, 500)
            traffic_data.append({
                "route": route_name,
                "hour": hour,
                "day": day,
                "traffic_volume": volume,
                "lat": lat,
                "lon": lon
            })
df_traffic = pd.DataFrame(traffic_data)
df_traffic.to_csv("jakarta_traffic_data.csv", index=False)
print("✅ Generated: jakarta_traffic_data.csv for dashboard")
