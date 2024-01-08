FROM python:3.10.4-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential libmariadbclient-dev

# Set the working directory
WORKDIR /swiftbank

# Install dependencies
COPY requirements.txt . 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project code to the work directory.
COPY . .

# Expose the port
EXPOSE 8000