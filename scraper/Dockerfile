FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    libgconf-2-4 \
    libxi6 \
    libxss1 \
    libxtst6 \
    libnss3 \
    libcups2 \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome from the official repository
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN echo "Fetching ChromeDriver..." \
    && CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/linux64/chromedriver-linux64.zip" \
    \
    && echo "Downloading ChromeDriver from $CHROMEDRIVER_URL..." \
    && wget -q "$CHROMEDRIVER_URL" -O chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mkdir -p /usr/local/bin/chromedriver \
    && mv chromedriver-linux64 /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip

# Set up Python environment
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scraper code
COPY . .

# Set up Xvfb for headless browsing
ENV DISPLAY=:99

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
