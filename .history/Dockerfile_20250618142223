FROM python:3.10-slim

# Install Chrome & drivers
RUN apt-get update && apt-get install -y wget gnupg unzip curl chromium chromium-driver

# Set display port to avoid crash
ENV DISPLAY=:99

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot script
COPY submission_notifier.py /app/submission_notifier.py
WORKDIR /app

CMD ["python", "submission_notifier.py"]