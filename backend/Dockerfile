FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY . .

# Start the FastAPI server using the PORT environment variable provided by Render
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
