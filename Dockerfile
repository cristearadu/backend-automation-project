FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    openjdk-17-jre \
    && apt-get clean

# Install Allure CLI
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl -o allure-2.24.0.zip -L https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.zip && \
    unzip allure-2.24.0.zip -d /opt/ && \
    ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure

WORKDIR /app

# Copy dependencies and source code
COPY ./requirements.txt ./requirements.txt
COPY ./tests ./tests
COPY ./helpers ./helpers
COPY ./schemas ./schemas
COPY ./conftest.py ./conftest.py
COPY ./core ./core
COPY ./request_builders ./request_builders
COPY ./pytest.ini ./pytest.ini

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set test type as build arg/env
ARG TEST_TYPE=regression
ENV TEST_TYPE=${TEST_TYPE}
RUN mkdir -p /app/allure-report /app/allure-results /app/reports
RUN chmod -R 777 /app/allure-report /app/allure-results /app/reports

# Start json-server in background, wait, then run tests
CMD pytest -n auto -m ${TEST_TYPE} --alluredir=allure-results --junitxml=reports/junit.xml || true && allure generate allure-results --clean -o allure-report