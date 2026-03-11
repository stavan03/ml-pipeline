# Start with a base Python environment
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy everything else into the container
COPY . .

# Tell Docker which port the app runs on
EXPOSE 8000

# The command to start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]