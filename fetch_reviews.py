import os
import json
import requests
import sys
from flask import Flask, render_template

app = Flask(__name__)
reviews_data = []

def fetch_reviews():
    global reviews_data
    print("Starting review fetch...")
    api_key = os.environ.get("GOOGLE_API_KEY")
    place_id = os.environ.get("PLACE_ID")

    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return
    
    if not place_id:
        print("Error: PLACE_ID environment variable not set.")
        return

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "OK":
            print(f"Error fetching reviews: {data.get('status')} - {data.get('error_message', '')}")
            return

        result = data.get("result", {})
        reviews_data = result.get("reviews", [])
        
        print(f"Successfully fetched {len(reviews_data)} reviews.")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@app.route('/')
def index():
    return render_template('index.html', reviews=reviews_data)

if __name__ == "__main__":
    # Fetch reviews once on startup
    fetch_reviews()
    # Start Flask server
    app.run(host='0.0.0.0', port=8080)
