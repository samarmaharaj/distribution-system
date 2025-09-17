# Use Python from Google's Docker Hub mirror to avoid pull DNS issues
FROM mirror.gcr.io/library/python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY node.py .

# This is the base command to run.
# The node name (e.g., "node1") will be appended by docker-compose.
ENTRYPOINT ["python", "node.py"]