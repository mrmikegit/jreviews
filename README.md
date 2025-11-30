# Google Reviews Fetcher

A Dockerized Flask application that fetches customer reviews from Google and displays them on a web page. Supports both the Google Places API and the Google My Business (GMB) API via OAuth.

## Features

- **Dual API Support**: Switch between Google Places API and GMB API using a flag.
- **Web-Based OAuth Setup**: Easily obtain GMB credentials via a built-in setup page.
- **Cloud Run Ready**: Optimized for deployment on Google Cloud Run.

## Deployment (Google Cloud Run)

1.  **Prerequisites**:
    - Google Cloud Project.
    - `gcloud` CLI installed.

2.  **Deploy**:
    ```bash
    ./deploy_cloud_run.sh
    ```

3.  **Configuration**:
    Set the following environment variables in your Cloud Run service:

    | Variable | Description |
    | :--- | :--- |
    | `USE_GMB_OAUTH` | Set to `true` to use GMB API, `false` for Places API. |
    | `GOOGLE_API_KEY` | Required if `USE_GMB_OAUTH` is `false`. |
    | `PLACE_ID` | Required if `USE_GMB_OAUTH` is `false`. |
    | `GMB_CLIENT_ID` | Required if `USE_GMB_OAUTH` is `true`. |
    | `GMB_CLIENT_SECRET` | Required if `USE_GMB_OAUTH` is `true`. |
    | `GMB_REFRESH_TOKEN` | Required if `USE_GMB_OAUTH` is `true`. |
    | `GMB_ACCOUNT_ID` | Required if `USE_GMB_OAUTH` is `true`. |
    | `GMB_LOCATION_ID` | Required if `USE_GMB_OAUTH` is `true`. |

## Usage

- **View Reviews**: Visit the root URL (`/`).
- **Setup OAuth**: Visit `/setup` to generate your Refresh Token and find your Account/Location IDs.
