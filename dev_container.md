#### Dev Container
The Remote - Containers extension lets you use a Docker container as a full-featured development environment. It allows you to use development environments inside containers, and develop the application directly inside the container.
##### Setup Dev Containers
- Install the *Dev Containers* extension in VS Code
- Create `.devcontainer` folder and `devcontainer.json` file in the root of the project.
```bash
$ mkdir .devcontainer
$ touch .devcontainer/devcontainer.json
```
*This file configures how VS Code should interact with your development container.*
- Add the following configuration to `devcontainer.json` file:
```
{
    // Name of the development container
    "name": "Django Dev Container",

    // Path to the docker-compose file relative to this devcontainer.json
    "dockerComposeFile": [
		"../docker-compose.yml"
	],
    // The service in docker-compose.yml that we want vs code to use as a dev containers
    "service": "app",
    "shutdownAction": "stopCompose",
    // Sets the main working directory inside the container
    "workspaceFolder": "/home/django-user/app",

    // VS Settings to apply inside the container
    "customizations": {
        "vscode": {
            "settings": {},  // settings.json
            "extensions": []  // list of vscode extensions to install inside the container
        }
    },

    // Ports to forward from the container to the host machine
    "forwardPorts": [8000, 3000],
    // Specifies the username that should be used for the VS Code remote session
    "remoteUser": "django-user"
}
```
- Dockerfile configuration for dev container development. It allows you to use VSCode extensions inside the container.
```bash
# Debian-based python image
FROM python:3.11.6-slim

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
```

- Open the Command Palette (Ctrl+Shift+P) and run the **Remote-Containers: Reopen in Container** command.