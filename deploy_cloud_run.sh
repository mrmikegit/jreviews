#!/bin/bash

# Configuration
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="google-reviews-fetcher"
REGION="us-central1" # Change if needed
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

if [ -z "$PROJECT_ID" ]; then
  echo "Error: No Google Cloud Project ID found. Please run 'gcloud config set project <YOUR_PROJECT_ID>'."
  exit 1
fi

echo "Deploying to Project: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"

# 1. Build the Docker image
echo "Building Docker image..."
gcloud builds submit --tag $IMAGE_NAME .

# 2. Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars USE_GMB_OAUTH=false

echo "Deployment complete!"
echo "To set secrets, use the Google Cloud Console or:"
echo "gcloud run services update $SERVICE_NAME --set-env-vars GMB_CLIENT_ID=...,GMB_CLIENT_SECRET=..."
