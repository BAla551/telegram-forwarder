# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system packages (optional but recommended for some Python wheels)
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy your app files into the container
COPY main.py .
COPY link_forwarder.session .

# Ensure we see live log output (important for Railway logs)
ENV PYTHONUNBUFFERED=1

# Run the main script
CMD ["python", "main.py"]
