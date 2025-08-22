# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script
COPY app.py .

# Set timezone (optional, adjust if needed)
ENV TZ=Asia/Kolkata

# Run script when container starts
CMD ["python", "app.py"]