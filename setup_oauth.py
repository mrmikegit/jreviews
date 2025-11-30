import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes required for the application
SCOPES = [
    'https://www.googleapis.com/auth/business.manage'
]

def main():
    print("--- Google My Business OAuth Setup ---")
    print("This script will help you get your Refresh Token and Account/Location IDs.")
    print("You need a Client ID and Client Secret from the Google Cloud Console.")
    print("Ensure you have enabled the 'Google My Business Information API'.")
    print("--------------------------------------")

    client_id = input("Enter your Client ID: ").strip()
    client_secret = input("Enter your Client Secret: ").strip()

    if not client_id or not client_secret:
        print("Error: Client ID and Client Secret are required.")
        return

    # Create a client config dictionary
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://localhost"]
        }
    }

    try:
        # Run the OAuth flow
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)

        print("\n--- OAuth Successful! ---")
        print(f"GMB_REFRESH_TOKEN: {creds.refresh_token}")
        print("Save this token!\n")

        # List Accounts and Locations
        print("--- Fetching Accounts and Locations ---")
        service = build("mybusinessbusinessinformation", "v1", credentials=creds)

        # List Accounts
        accounts_request = service.accounts().list()
        accounts_response = accounts_request.execute()
        accounts = accounts_response.get("accounts", [])

        if not accounts:
            print("No accounts found.")
        else:
            for account in accounts:
                account_name = account.get("name") # e.g., accounts/123456789
                account_id = account_name.split("/")[1]
                print(f"\nAccount: {account.get('accountName')} ({account_name})")
                print(f"GMB_ACCOUNT_ID: {account_id}")

                # List Locations for this Account
                locations_request = service.accounts().locations().list(
                    parent=account_name,
                    readMask="name,title,storeCode"
                )
                locations_response = locations_request.execute()
                locations = locations_response.get("locations", [])

                if not locations:
                    print("  No locations found for this account.")
                else:
                    for location in locations:
                        location_name = location.get("name") # e.g., accounts/123456789/locations/987654321
                        location_id = location_name.split("/")[3]
                        print(f"  Location: {location.get('title')} ({location_name})")
                        print(f"  GMB_LOCATION_ID: {location_id}")

    except Exception as e:
        print(f"\nError during setup: {e}")

if __name__ == "__main__":
    main()
