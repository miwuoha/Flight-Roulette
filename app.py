from collections import Counter
from flask import Flask, render_template
import random

app = Flask(__name__)

destinations = [
    {
        "city": "Tokyo",
        "country": "Japan",
        "airport": "HND",
        "trip_type": "International",
        "fact": "Tokyo's Shibuya Crossing sees up to 3,000 people cross at once.",
        "price_min": 850,
        "price_max": 1450
    },
    {
        "city": "Paris",
        "country": "France",
        "airport": "CDG",
        "trip_type": "International",
        "fact": "The Eiffel Tower grows about 6 inches taller in summer heat.",
        "price_min": 650,
        "price_max": 1100
    },
    {
        "city": "Honolulu",
        "country": "United States",
        "airport": "HNL",
        "trip_type": "Domestic",
        "fact": "Honolulu is the only U.S. city with a royal palace, Iolani Palace.",
        "price_min": 380,
        "price_max": 650
    },
    {
        "city": "Sydney",
        "country": "Australia",
        "airport": "SYD",
        "trip_type": "International",
        "fact": "The Sydney Opera House has over one million roof tiles.",
        "price_min": 1100,
        "price_max": 1800
    },
    {
        "city": "Los Angeles",
        "country": "United States",
        "airport": "LAX",
        "trip_type": "Domestic",
        "fact": "LA has more registered cars than people over the age of 16.",
        "price_min": 180,
        "price_max": 420
    },
    {
        "city": "London",
        "country": "England",
        "airport": "LHR",
        "trip_type": "International",
        "fact": "Big Ben is actually the name of the bell, not the clock tower.",
        "price_min": 600,
        "price_max": 1050
    },
    {
        "city": "Rio de Janeiro",
        "country": "Brazil",
        "airport": "GIG",
        "trip_type": "International",
        "fact": "Christ the Redeemer was struck by lightning and lost a finger in 2014.",
        "price_min": 750,
        "price_max": 1300
    },
    {
        "city": "New York",
        "country": "United States",
        "airport": "JFK",
        "trip_type": "Domestic",
        "fact": "New York City has over 6,400 miles of streets, more than the length of Route 66 twice over.",
        "price_min": 150,
        "price_max": 380
    },
    {
        "city": "Reykjavik",
        "country": "Iceland",
        "airport": "KEF",
        "trip_type": "International",
        "fact": "Reykjavik runs almost entirely on geothermal and hydroelectric power.",
        "price_min": 550,
        "price_max": 950
    },
    {
        "city": "Chicago",
        "country": "United States",
        "airport": "ORD",
        "trip_type": "Domestic",
        "fact": "The Chicago River is dyed green every year for St. Patrick's Day.",
        "price_min": 140,
        "price_max": 360
    },
    {
        "city": "San Francisco",
        "country": "United States",
        "airport": "SFO",
        "trip_type": "Domestic",
        "fact": "San Francisco's famous cable cars are the world's last manually operated cable car system.",
        "price_min": 200,
        "price_max": 450
    },
    {
        "city": "Las Vegas",
        "country": "United States",
        "airport": "LAS",
        "trip_type": "Domestic",
         "fact": "Las Vegas has more hotel rooms than almost any other city in the United States.",
        "price_min": 160,
        "price_max": 380
    },
    {
         "city": "Denver",
        "country": "United States",
        "airport": "DEN",
        "trip_type": "Domestic",
        "fact": "Denver is exactly one mile above sea level, giving it the nickname the 'Mile High City.'",
        "price_min": 150,
        "price_max": 350
    },
    {
        "city": "Miami",
        "country": "United States",
        "airport": "MIA",
        "trip_type": "Domestic",
        "fact": "Miami is the only major U.S. city founded by a woman.",
        "price_min": 180,
        "price_max": 400
    },
    {
        "city": "Amsterdam",
        "country": "Netherlands",
        "airport": "AMS",
        "trip_type": "International",
        "fact": "Amsterdam has more bicycles than residents, with hundreds of thousands of bikes throughout the city.",
        "price_min": 620,
        "price_max": 1050
    },
    {
        "city": "Barcelona",
        "country": "Spain",
        "airport": "BCN",
        "trip_type": "International",
        "fact": "Barcelona's Sagrada Família has been under construction for more than 140 years.",
        "price_min": 640,
        "price_max": 1080
    },
    {
        "city": "Singapore",
        "country": "Singapore",
        "airport": "SIN",
        "trip_type": "International",
        "fact": "Singapore is one of the world's smallest countries, covering only about 280 square miles of land.",
        "price_min": 950,
        "price_max": 1600
    },
    {
        "city": "Seoul",
        "country": "South Korea",
        "airport": "ICN",
        "trip_type": "International",
        "fact": "Seoul's subway system has some of the world's longest underground escalators.",
        "price_min": 900,
        "price_max": 1500
    },
    {
        "city": "Cape Town",
        "country": "South Africa",
        "airport": "CPT",
        "trip_type": "International",
        "fact": "Cape Town's Table Mountain is one of the oldest mountains in the world, estimated to be over 200 million years old.",
        "price_min": 900,
        "price_max": 1550
    },
    {
        "city": "Accra",
        "country": "Ghana",
        "airport": "ACC",
        "trip_type": "International",
        "fact": "Accra is one of the few major cities located almost directly on the Greenwich Meridian.",
        "price_min": 850,
        "price_max": 1400
    }
]

# lowest and highest fares across the whole network, used to scale the
# price-range meter in the UI so it's always relative to real bounds
NETWORK_PRICE_FLOOR = min(d["price_min"] for d in destinations)
NETWORK_PRICE_CEIL = max(d["price_max"] for d in destinations)

# these are some endpoints for my application
request_count = 0

# keeps the most recent picks, newest first
roll_history = []
MAX_HISTORY = 10

# tracks how many times each city has been picked
leaderboard = Counter()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/destination")
def destination():
    global request_count
    request_count += 1

    pick = random.choice(destinations)

    roll_history.insert(0, pick)
    del roll_history[MAX_HISTORY:]

    leaderboard[pick["city"]] += 1

    response = dict(pick)
    response["network_min"] = NETWORK_PRICE_FLOOR
    response["network_max"] = NETWORK_PRICE_CEIL
    return response


@app.route("/history")
def history():
    return {
        "history": roll_history
    }


@app.route("/leaderboard")
def get_leaderboard():
    top = leaderboard.most_common(5)
    return {
        "leaderboard": [{"city": city, "count": count} for city, count in top]
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


@app.route("/stats")
def stats():
    return {
        "requests": request_count
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
