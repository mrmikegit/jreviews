import os
import json
import requests
import sys

def fetch_reviews():
    api_key = os.environ.get("GOOGLE_API_KEY")
    place_id = os.environ.get("PLACE_ID")
    output_file = os.environ.get("OUTPUT_FILE", "reviews.json")

    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        sys.exit(1)
    
    if not place_id:
        print("Error: PLACE_ID environment variable not set.")
        sys.exit(1)

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "OK":
            print(f"Error fetching reviews: {data.get('status')} - {data.get('error_message', '')}")
            sys.exit(1)

        result = data.get("result", {})
        reviews = result.get("reviews", [])

        with open(output_file, "w") as f:
            json.dump(reviews, f, indent=2)
        
        print(f"Successfully saved {len(reviews)} reviews to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_reviews()
