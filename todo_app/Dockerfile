FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Declaring a volume for storing the database
VOLUME ["/app/data"]

# Expose the application port
EXPOSE 80

# Start FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
