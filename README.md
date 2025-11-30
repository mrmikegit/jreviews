# Google Reviews Fetcher

This project runs a Docker container on Cloudflare Workers (using Cloudflare Containers beta) to fetch Google Reviews for a specific place and save them to a JSON file.

## Prerequisites

- Node.js and npm installed
- Cloudflare account with access to Containers beta
- Google Places API Key
- Place ID of the business

## Setup

1.  Install dependencies:
    ```bash
    npm install
    ```

2.  Login to Cloudflare:
    ```bash
    npx wrangler login
    ```

## Deployment

To deploy the container to Cloudflare:

1.  Set your secrets (API Key and Place ID):
    ```bash
    npx wrangler secret put GOOGLE_API_KEY
    npx wrangler secret put PLACE_ID
    ```

2.  Deploy the worker:
    ```bash
    npx wrangler deploy
    ```

## Usage

Once deployed, you can trigger the review fetch by visiting the Worker URL with the `/fetch` endpoint:

```
https://google-reviews-fetcher.<your-subdomain>.workers.dev/fetch
```

The container will start, fetch the reviews, save them to `/data/reviews.json`, and keep running (serving a simple status page).

## Local Development (Optional)

You can still build and run the Docker container locally if needed:

```bash
docker build -t google-reviews-fetcher .
docker run --rm \
  -e GOOGLE_API_KEY="YOUR_API_KEY" \
  -e PLACE_ID="YOUR_PLACE_ID" \
  -v $(pwd)/data:/data \
  google-reviews-fetcher
```

### Environment Variables

- `GOOGLE_API_KEY`: Your Google Places API Key (Required).
- `PLACE_ID`: The Place ID of the business (Required).
- `OUTPUT_FILE`: Path to save the JSON file inside the container (Default: `/data/reviews.json`).

## Output

The reviews will be saved to `reviews.json` in the mounted volume.
