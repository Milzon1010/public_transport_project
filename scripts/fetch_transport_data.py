import requests  # Import library requests untuk kirim HTTP request

def test_ors_key_and_fetch(api_key, test_start, test_end):
    """
    Fungsi untuk mengetes:
    - Server ORS aktif atau tidak
    - API key valid atau tidak
    - Sekaligus fetch rute sederhana untuk memastikan semuanya bekerja
    """
    url = "https://api.openrouteservice.org/v2/directions/driving-car"  # Endpoint directions
    headers = {
        'Authorization': api_key,  # API key untuk otorisasi
        'Content-Type': 'application/json'  # Format body request
    }
    body = {
        "coordinates": [test_start, test_end]  # Titik awal dan akhir
    }

    try:
        # Kirim POST request ke ORS directions
        response = requests.post(url, json=body, headers=headers, timeout=5)
        response.raise_for_status()  # Kalau status code >=400 akan error
        data = response.json()  # Convert response ke dict
        print(f"✅ ORS server aktif dan API key valid!")
        return data  # Return data untuk diproses
    except Exception as e:
        # Kalau error, tampilkan pesan error dan isi response
        print(f"❌ Gagal akses ORS API / API key invalid: {e}")
        if response is not None:
            print(f"❌ Response content: {response.text}")
        return None  # Return None supaya tidak lanjut

def process_and_export(data):
    """
    Fungsi untuk:
    - Menampilkan ringkasan rute dan langkah ke console
    - Export hasil ke file TXT
    """
    if not data or 'routes' not in data:
        print("❌ Tidak ada rute di response.")
        return

    route = data['routes'][0]  # Ambil rute pertama
    summary = route['summary']  # Ambil ringkasan jarak + durasi

    # Tampilkan ringkasan ke console
    print(f"✅ Route summary:")
    print(f"  - Distance: {summary['distance']} meters")
    print(f"  - Duration: {summary['duration']} seconds")

    # Tampilkan langkah-langkah perjalanan
    print("\n✅ Instructions:")
    steps = route['segments'][0]['steps']  # Ambil langkah-langkah
    for step in steps:
        print(f"- {step['instruction']} ({step['distance']} m)")

    # Simpan ke file TXT
    with open("route_summary.txt", "w", encoding="utf-8") as f:
        # Tulis ringkasan
        f.write(f"Route summary (driving-car):\n")
        f.write(f"Distance: {summary['distance']} meters\n")
        f.write(f"Duration: {summary['duration']} seconds\n\n")
        f.write("Instructions:\n")
        # Tulis langkah-langkah
        for step in steps:
            f.write(f"- {step['instruction']} ({step['distance']} m)\n")

    print("\n✅ Data rute disimpan di route_summary.txt")

if __name__ == "__main__":
    # API key kamu
    API_KEY = "5b3ce3597851110001cf6248e644fd9d109a413697b6963b173c72ef"
    # Koordinat Monas (lon, lat)
    ORIGIN = [106.8272, -6.1754]
    # Koordinat Blok M (lon, lat)
    DEST = [106.7816, -6.2607]

    # Tes server + key, dan fetch rute
    data = test_ors_key_and_fetch(API_KEY, ORIGIN, DEST)

    # Kalau sukses, proses dan export
    if data:
        process_and_export(data)
    else:
        print("❌ Stop: API tidak siap / key bermasalah.")
