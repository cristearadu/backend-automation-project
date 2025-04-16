FROM python:3.10-slim

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
RUN pip install -r requirements.txt

# Set test type as build arg/env
ARG TEST_TYPE=regression
ENV TEST_TYPE=${TEST_TYPE}

# Start json-server in background, wait, then run tests
CMD ["/bin/bash", "-c", "pytest", "-n", "auto", "-m", "${TEST_TYPE}"]