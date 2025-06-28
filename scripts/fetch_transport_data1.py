
import requests
import pandas as pd
import time


def fetch_and_process(api_key, start_coords, end_coords, max_retries=3):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "coordinates": [start_coords, end_coords]
    }

    attempt = 0
    while attempt < max_retries:
        try:
            print(f"🔄 Attempt {attempt + 1} of {max_retries} to fetch route...")

            response = requests.post(url, json=payload, headers=headers, timeout=10)

            status = response.status_code
            print(f"📡 HTTP Status Code: {status}")

            if status == 200:
                print("✅ Success: Route data retrieved.")
            elif status == 401:
                print("🔐 Error 401: Unauthorized - Invalid API key.")
                break
            elif status == 429:
                print("⏳ Error 429: Too many requests - Rate limit exceeded.")
                time.sleep(5)
            elif status >= 400:
                print(f"❌ HTTP Error {status}: {response.reason}")
                time.sleep(2)
            else:
                print(f"⚠️ Unexpected status: {status}")

            response.raise_for_status()
            data = response.json()

            segment = data["features"][0]["properties"]["segments"][0]
            distance = segment["distance"]
            duration = segment["duration"]
            steps = segment["steps"]

            print(f"\n📍 Distance: {distance:.2f} meters")
            print(f"⏱️ Duration: {duration:.2f} seconds")
            print("\n🧭 Instructions:")
            for i, step in enumerate(steps):
                print(f"{i+1}. {step['instruction']} ({step['distance']:.1f} m)")

            df = pd.DataFrame(steps)
            df.to_csv("data/route.csv", index=False)
            print("\n💾 Saved route steps to 'data/route.csv'")

            return

        except requests.exceptions.RequestException as e:
            print(f"❌ Network or API error: {e}")
            attempt += 1
            time.sleep(2)

    print("🚫 Failed to fetch route after maximum retries.")


if __name__ == "__main__":
    api_key = "YOUR_API_KEY_HERE"

    start = [106.827153, -6.175110]  # Monas
    end = [106.865036, -6.121435]    # Ancol

    fetch_and_process(api_key, start, end)
