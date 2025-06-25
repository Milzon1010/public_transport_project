from flask import Flask, render_template, request  # Import Flask & tools untuk form + template
import requests  # Untuk request ke API

# Inisialisasi Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    travel_time = None  # Default: belum ada hasil

    if request.method == "POST":
        # Ambil input form
        start = request.form.get("start")
        end = request.form.get("end")

        # Saat ini pakai dummy dulu koordinat (Monas ke Blok M)
        origin = [106.8272, -6.1754]  # Koordinat Monas (dummy)
        dest = [106.7816, -6.2607]    # Koordinat Blok M (dummy)

        # Siapkan ORS API call
        api_key = "5b3ce3597851110001cf6248e644fd9d109a413697b6963b173c72ef"
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json'
        }
        body = {
            "coordinates": [origin, dest]
        }

        try:
            # Panggil API
            res = requests.post(url, json=body, headers=headers)
            res.raise_for_status()  # Error kalau status code >=400
            data = res.json()

            # Ambil duration dari API response
            travel_time = data["routes"][0]["summary"]["duration"]

        except Exception as e:
            # Kalau error, tampilkan pesan
            travel_time = f"❌ Error: {e}"

    # Render template dengan hasil (kalau ada)
    return render_template("index.html", travel_time=travel_time)
