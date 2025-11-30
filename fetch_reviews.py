import os
import json
import requests
import sys
from flask import Flask, render_template, request, redirect, url_for, session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = os.urandom(24) # Needed for session
reviews_data = []

# Scopes required for the application
SCOPES = [
    'https://www.googleapis.com/auth/business.manage'
]

def fetch_reviews():
    global reviews_data
    print("Starting review fetch...")
    
    use_gmb_oauth = os.environ.get("USE_GMB_OAUTH", "false").lower() == "true"
    
    if use_gmb_oauth:
        fetch_gmb_reviews()
    else:
        fetch_places_reviews()

def fetch_gmb_reviews():
    global reviews_data
    print("Fetching reviews using GMB API (OAuth)...")
    
    client_id = os.environ.get("GMB_CLIENT_ID")
    client_secret = os.environ.get("GMB_CLIENT_SECRET")
    refresh_token = os.environ.get("GMB_REFRESH_TOKEN")
    account_id = os.environ.get("GMB_ACCOUNT_ID")
    location_id = os.environ.get("GMB_LOCATION_ID")
    
    if not all([client_id, client_secret, refresh_token, account_id, location_id]):
        print("Error: Missing GMB OAuth environment variables.")
        return

    try:
        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )
        
        service = build("mybusinessbusinessinformation", "v1", credentials=creds)
        parent = f"accounts/{account_id}/locations/{location_id}"
        
        reviews = []
        next_page_token = None
        
        while True:
            request = service.accounts().locations().reviews().list(
                parent=parent,
                pageSize=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            fetched_reviews = response.get("reviews", [])
            reviews.extend(fetched_reviews)
            
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        
        # Normalize reviews to match existing format
        normalized_reviews = []
        for r in reviews:
            normalized_reviews.append({
                "author_name": r.get("reviewer", {}).get("displayName", "Anonymous"),
                "profile_photo_url": r.get("reviewer", {}).get("profilePhotoUrl", ""),
                "rating": ["STAR_RATING_UNSPECIFIED", "ONE", "TWO", "THREE", "FOUR", "FIVE"].index(r.get("starRating", "STAR_RATING_UNSPECIFIED")),
                "relative_time_description": r.get("createTime", ""), # GMB returns ISO timestamp, might need formatting
                "text": r.get("comment", "")
            })
            
        reviews_data = normalized_reviews
        print(f"Successfully fetched {len(reviews_data)} reviews via GMB API.")

    except Exception as e:
        print(f"Error fetching GMB reviews: {e}")

def fetch_places_reviews():
    global reviews_data
    print("Fetching reviews using Google Places API...")
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
        
        print(f"Successfully fetched {len(reviews_data)} reviews via Places API.")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@app.route('/')
def index():
    return render_template('index.html', reviews=reviews_data)

@app.route('/setup')
def setup():
    client_id = os.environ.get("GMB_CLIENT_ID", "")
    client_secret = os.environ.get("GMB_CLIENT_SECRET", "")
    # Determine redirect URI based on request host
    redirect_uri = url_for('oauth2callback', _external=True, _scheme='https')
    return render_template('setup.html', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

@app.route('/authorize', methods=['POST'])
def authorize():
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    
    if not client_id or not client_secret:
        return "Client ID and Client Secret are required.", 400
    
    # Store in session for callback
    session['client_id'] = client_id
    session['client_secret'] = client_secret
    
    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    
    redirect_uri = url_for('oauth2callback', _external=True, _scheme='https')
    
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session.get('state')
    client_id = session.get('client_id')
    client_secret = session.get('client_secret')
    
    if not state or not client_id or not client_secret:
        return "Session expired or invalid. Please start setup again.", 400

    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    
    # Force HTTPS for redirect_uri if behind proxy/worker
    redirect_uri = url_for('oauth2callback', _external=True, _scheme='https')

    try:
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            state=state,
            redirect_uri=redirect_uri
        )
        
        # Use the full URL from the request, ensuring HTTPS
        authorization_response = request.url.replace('http://', 'https://')
        flow.fetch_token(authorization_response=authorization_response)
        
        creds = flow.credentials
        refresh_token = creds.refresh_token
        
        # Fetch Accounts using Account Management API
        account_service = build("mybusinessaccountmanagement", "v1", credentials=creds)
        business_service = build("mybusinessbusinessinformation", "v1", credentials=creds)
        
        accounts_data = []
        accounts_response = account_service.accounts().list().execute()
        accounts = accounts_response.get("accounts", [])
        
        for account in accounts:
            account_name = account.get("name")
            account_id = account_name.split("/")[1]
            
            locations_data = []
            # Fetch Locations using Business Information API
            locations_response = business_service.accounts().locations().list(
                parent=account_name,
                readMask="name,title,storeCode"
            ).execute()
            locations = locations_response.get("locations", [])
            
            for location in locations:
                location_name = location.get("name")
                location_id = location_name.split("/")[3]
                locations_data.append({
                    "title": location.get("title"),
                    "id": location_id,
                    "name": location_name
                })
            
            accounts_data.append({
                "name": account.get("accountName"),
                "id": account_id,
                "full_name": account_name,
                "locations": locations_data
            })
            
        return render_template('setup_result.html', 
                             refresh_token=refresh_token, 
                             accounts=accounts_data,
                             client_id=client_id,
                             client_secret=client_secret)
                             
    except Exception as e:
        return f"Error during OAuth callback: {e}", 500

if __name__ == "__main__":
    # Fetch reviews once on startup
    fetch_reviews()
    # Start Flask server
    app.run(host='0.0.0.0', port=8080)
