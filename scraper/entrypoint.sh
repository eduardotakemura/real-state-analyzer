#!/bin/bash
set -e

# Start Xvfb in the background
Xvfb :99 -ac &

# Run the scraper script
python -u /app/main.py
