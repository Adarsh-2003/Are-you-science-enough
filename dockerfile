# Use the official Python image
FROM python:3.10-slim

# Set work directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py", "--port", "5000"]