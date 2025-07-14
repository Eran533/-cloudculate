FROM --platform=$TARGETPLATFORM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 fonts-liberation libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    xdg-utils libu2f-udev libvulkan1 libxss1 libglib2.0-0 libgtk-3-0 \
    libssl-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set env vars for Chrome version
ENV CHROME_VERSION=138.0.7204.100

# Download Chrome & ChromeDriver based on architecture
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "amd64" ]; then \
        CHROME_ARCH="linux64"; \
    elif [ "$ARCH" = "arm64" ]; then \
        CHROME_ARCH="linux-arm64"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    echo "Downloading Chrome for $CHROME_ARCH..." && \
    wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/${CHROME_ARCH}/chrome-${CHROME_ARCH}.zip && \
    unzip chrome-${CHROME_ARCH}.zip && \
    mv chrome-${CHROME_ARCH} /opt/chrome && \
    ln -s /opt/chrome/chrome /usr/bin/google-chrome && \
    rm chrome-${CHROME_ARCH}.zip && \
    \
    echo "Downloading ChromeDriver for $CHROME_ARCH..." && \
    wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/${CHROME_ARCH}/chromedriver-${CHROME_ARCH}.zip && \
    unzip chromedriver-${CHROME_ARCH}.zip && \
    mv chromedriver-${CHROME_ARCH}/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-${CHROME_ARCH} chromedriver-${CHROME_ARCH}.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app ./app

# Set env vars for Selenium
ENV CHROME_BIN=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]  