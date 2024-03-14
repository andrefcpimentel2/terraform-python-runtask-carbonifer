# Use a minimal Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# Copy requirements file
COPY carbonifer/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script
COPY carbonifer/carbonifer.py .

# Expose port 80
EXPOSE 80

# Run the Python script
CMD ["python", "carbonifer/carbonifer.py"]
