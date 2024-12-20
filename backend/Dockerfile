# Use Python 3.9 as the base image
FROM python:3.9

# Update package index and upgrade pip
RUN apt-get update && apt-get install -y \
    && pip install --upgrade pip

# Set the working directory for the application
WORKDIR /backend

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 8000

# Start the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]