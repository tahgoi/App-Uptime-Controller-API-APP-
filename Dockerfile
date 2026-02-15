# Use official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Start the Panel Dashboard natively from the container
CMD ["panel", "serve", "app.py", "--port", "8589", "--address", "0.0.0.0", "--allow-websocket-origin=*"]