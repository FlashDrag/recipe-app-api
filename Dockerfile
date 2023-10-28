# Use the specified Python image
FROM python:3.9-slim

# Set maintainer label
LABEL maintainer="linkedin.com/in/pavlo-myskov"

# Set environment variable to ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED 1

# Copy requirements files
COPY ./requirements.txt /home/django-user/tmp/requirements.txt
COPY ./requirements.dev.txt /home/django-user/tmp/requirements.dev.txt

# Create a django-user with specified home directory and no password
RUN adduser --home /home/django-user --disabled-password django-user

# Set the user's home directory as the working directory
WORKDIR /home/django-user/app

# Copy the app to the user's directory
COPY ./app /home/django-user/app

# Set permissions for django-user
RUN chown -R django-user:django-user /home/django-user

# Expose port 8000
EXPOSE 8000

# Argument for development dependencies installation
ARG DEV=false

# Set up Python virtual environment and install requirements
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /home/django-user/tmp/requirements.txt && \
    if [ "$DEV" = "true" ] ; then \
        /py/bin/pip install -r /home/django-user/tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /home/django-user/tmp

# Update PATH to include the Python virtual environment binaries
ENV PATH="/py/bin:$PATH"

# Switch to django-user for subsequent commands
USER django-user