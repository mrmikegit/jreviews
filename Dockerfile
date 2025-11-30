FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fetch_reviews.py .

# Set default environment variables (can be overridden at runtime)
ENV OUTPUT_FILE=/data/reviews.json

# Create a directory for data persistence
RUN mkdir -p /data

CMD ["python", "fetch_reviews.py"]
