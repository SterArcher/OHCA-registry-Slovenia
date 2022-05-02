# syntax=docker/dockerfile:1
FROM python:3.8-slim as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

###################
# DEPENDENCY STAGE
FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install unixodbc-dev default-libmysqlclient-dev build-essential -y --no-install-recommends

# Install python dependencies in /opt/app/.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv lock
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

################
# RUNTIME STAGE
FROM base AS runtime

RUN apt-get update && apt-get install unixodbc-dev default-libmysqlclient-dev -y --no-install-recommends

# Copy virtual env from python-deps stage
RUN mkdir -p /opt/app/.venv

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /opt/app
