FROM python:3.10.4-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install core dependencies.
RUN apt-get update \ 
    && apt-get install -y gcc python3-dev libpq-dev build-essential libmariadbclient-dev

# Set the working directory
WORKDIR /mogdynamics

# Install dependencies
COPY ./requirements ./requirements
RUN pip install --upgrade pip
RUN pip install -r ./requirements/prod.txt

# Make the script executable
COPY ./docker/production/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy the project code to the work directory.
COPY . .

ENV DJANGO_SETTINGS_MODULE=core.settings.prod

ENTRYPOINT ["/entrypoint.sh"]