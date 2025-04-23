# Use a slim and secure Python image
FROM python:3.11-slim-bullseye

# Install OS-level dependencies
RUN apt-get update && apt-get install -y \
 build-essential \
 gcc \
 netcat \
 curl \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app


# Pre-copy only requirements to cache dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script (for caching)
COPY entrypoint.sh /app/entrypoint.sh

# Copy the rest of the project files
COPY . .

# run entry point
RUN chmod +x /app/entrypoint.sh

# Set environment variables: helpful for logging in Docker containers
ENV PYTHONUNBUFFERED=1

# Run custom startup script
CMD ["/app/entrypoint.sh"]

