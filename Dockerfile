FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    openjdk-17-jre \
    && apt-get clean

# Install Allure CLI
RUN curl -o allure.zip -Ls https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip && \
    unzip allure.zip -d /opt/ && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    rm allure.zip

WORKDIR /app

# Copy dependencies and source code
COPY ./requirements.txt ./requirements.txt
COPY ./tests ./tests
COPY ./helpers ./helpers
COPY ./schemas ./schemas
COPY ./conftest.py ./conftest.py
COPY ./core ./core
COPY ./request_builders ./request_builders

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set test type as build arg/env
ARG TEST_TYPE=regression
ENV TEST_TYPE=${TEST_TYPE}

# Start json-server in background, wait, then run tests
CMD pytest -n auto -m ${TEST_TYPE} --alluredir=allure-results --junitxml=reports/junit.xml && allure generate allure-results --clean -o allure-report