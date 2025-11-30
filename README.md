# Google Reviews Fetcher

This Docker container fetches Google Reviews for a specific place using the Google Places API and saves them to a JSON file.

## Prerequisites

- Docker installed
- Google Places API Key
- Place ID of the business

## Build the Image

```bash
sudo docker build -t google-reviews-fetcher .
```

## Run the Container

To run the container and save the reviews to a local directory (e.g., `./data`), use the following command:

```bash
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
