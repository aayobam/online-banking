FROM python-3.10.4-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODES 1
ENV PYTHONUNBUFFERED 1

# Install core dependencies.
RUN apt-get update \ 
    && apt-get install -y gcc python3-dev libpq-dev build-essential libmariadbclient-dev

# Sets working directory
WORKDIR /swiftbank-app

# Install dependencies
COPY ./requirements.txt ./requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make the script executable
COPY /docker/dev/entrypoint.ss /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy the project code to the work directory.
COPY . /swiftbank-app

ENTRYPOINT [ "/entrypoint.sh" ]
