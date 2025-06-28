
import requests
import time

def get_distance_with_retry(api_key, coord_a, coord_b, retries=2, wait=2):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": [coord_a, coord_b]
    }

    for attempt in range(retries + 1):
        try:
            response = requests.post(url, json=body, headers=headers, timeout=10)
            status_code = response.status_code
            print(f"🔄 HTTP Status ({coord_a} -> {coord_b}): {status_code}")

            response.raise_for_status()  # Raise error jika status code >= 400
            data = response.json()
            distance = data["routes"][0]["summary"]["distance"]
            print(f"✅ Distance: {distance} meters")
            return distance

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt+1} failed for {coord_a} -> {coord_b}: {e}")
            with open("error_log.txt", "a") as log:
                log.write(f"{coord_a} -> {coord_b} | Attempt {attempt+1} | Error: {e}\n")
            if attempt < retries:
                print(f"⏳ Retrying in {wait} seconds...")
                time.sleep(wait)
            else:
                print(f"❌ All {retries+1} attempts failed for {coord_a} -> {coord_b}.")
                return None

# Contoh penggunaan (bisa dipanggil di script utama kamu)
if __name__ == "__main__":
    API_KEY = "5b3ce3597851110001cf6248e644fd9d109a413697b6963b173c72ef"
    A = [106.8272, -6.1754]
    B = [106.7816, -6.2607]
    get_distance_with_retry(API_KEY, A, B)
