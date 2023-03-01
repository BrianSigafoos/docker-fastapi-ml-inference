# Versions with defaults. Override with env var to build a different version.
ARG PYTHON_VERSION=3.11

# More args
# For security, set a non-root user. Name is arbitrary.
ARG USER=nonroot
ARG USER_ID=1001
ARG PYTHON_ENV=production

# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:${PYTHON_VERSION}-slim-buster

# Args needed for this container
ARG USER
ARG USER_ID
ARG PYTHON_ENV

ENV PYTHON_ENV=${PYTHON_ENV}

# Recommended by hadolint
# https://github.com/hadolint/hadolint/wiki/DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Add non-root user
RUN groupadd --gid $USER_ID $USER \
  && useradd --uid $USER_ID --gid $USER --shell /bin/bash --create-home $USER

# Create a directory for the app code
RUN mkdir /app \
  && chown -R $USER:$USER /app

WORKDIR /app

# Copy dependency definitions for production-only requirements
COPY --chown=$USER:$USER pyproject.toml ./pyproject.toml

# Install poetry
RUN pip install poetry
# Don't create a virtualenv, we'll use the container's python so everything else just works
RUN poetry config virtualenvs.create false
# Install production-only dependencies
RUN poetry install --without dev,test

# COPY the app code that is needed to start the server and run the app
# This will be at `app/app` in the container.
# Note: .dockerignore only works for local builds, and not via Github Actions.
COPY --chown=$USER:$USER app app
COPY --chown=$USER:$USER .env.production .env.production

# Set user to non-root $USER
# This needs to be the numeric uid, not the username, for the k8s
# securityContext: runAsNonRoot check to work.
USER $USER_ID

# Default port is 8000, still specifying here to match the Kubernetes ml-pod-port
# https://www.uvicorn.org/deployment/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
