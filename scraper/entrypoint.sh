#!/bin/bash
set -e

# Start Xvfb in the background
Xvfb :99 -ac &

# Run the scraper script
python /app/main.py
