
import requests
import pandas as pd
import time

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

        if response.status_code == 200:
            print("✅ API success.")
        elif response.status_code == 401:
            print("🔐 Invalid API key.")
        elif response.status_code == 429:
            print("⏳ Rate limit exceeded.")
        else:
            print(f"❌ Unexpected error: {response.reason}")

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"❌ Error: {e}")
        if 'response' in locals():
            print(response.text)
        return None


def show_save_route(data, txt_path="route_summary.txt", csv_path="data/route.csv"):
    try:
        route = data['routes'][0]
        summary = route['summary']
        steps = route['segments'][0]['steps']

        print(f"\n📍 Distance: {summary['distance']} meters")
        print(f"⏱️ Duration: {summary['duration']} seconds")
        print("\n🧭 Instructions:")
        for i, step in enumerate(steps):
            print(f"{i+1}. {step['instruction']} ({step['distance']:.1f} m)")

        # Save to TXT
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"Distance: {summary['distance']} meters\n")
            f.write(f"Duration: {summary['duration']} seconds\n\n")
            f.write("Instructions:\n")
            for step in steps:
                f.write(f"- {step['instruction']} ({step['distance']:.1f} m)\n")
        print(f"💾 Saved text summary to {txt_path}")

        # Save to CSV
        df = pd.DataFrame(steps)
        df.to_csv(csv_path, index=False)
        print(f"💾 Saved full steps to {csv_path}")

    except Exception as e:
        print(f"❌ Failed to process and save data: {e}")


if __name__ == "__main__":
    API_KEY = "5b3ce3597851110001cf6248e644fd9d109a413697b6963b173c72ef"

    print("=== Route Estimator CLI ===")
    start_input = input("Enter start coordinates (lon,lat): ").strip()
    end_input = input("Enter end coordinates (lon,lat): ").strip()

    try:
        start_coords = [float(x) for x in start_input.split(",")]
        end_coords = [float(x) for x in end_input.split(",")]
    except:
        print("❌ Invalid input format. Use: 106.8272,-6.1754")
        exit()

    data = fetch_route(API_KEY, start_coords, end_coords)
    if data:
        show_save_route(data)
