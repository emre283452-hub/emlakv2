from flask import Flask, request, jsonify
from flask_cors import CORS
from sahibinden_scraper import fetch_listings

app = Flask(__name__)
CORS(app)

# Basit değerleme algoritması (örnek amaçlı)
def simple_valuation(area, room_count, building_age, city):
    base_prices = {
        "istanbul": 40000,
        "ankara": 30000,
        "izmir": 35000,
    }
    base = base_prices.get(city.lower(), 25000)
    price = area * base
    price *= (1 + 0.1 * (room_count - 1))
    price *= (1 - min(building_age, 30) * 0.01)
    return int(price)

@app.route("/api/value", methods=["POST"])
def evaluate():
    data = request.json
    area = float(data.get("area", 100))
    room_count = int(data.get("room_count", 2))
    building_age = int(data.get("building_age", 5))
    city = data.get("city", "istanbul")
    estimated_value = simple_valuation(area, room_count, building_age, city)
    return jsonify({"estimated_value": estimated_value})

@app.route("/api/fetch-listings", methods=["GET"])
def get_listings():
    city = request.args.get("city", "istanbul")
    district = request.args.get("district", "kadikoy")
    page = int(request.args.get("page", 1))
    data = fetch_listings(city, district, page)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)