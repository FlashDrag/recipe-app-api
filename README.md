# Recipe API
REST API with Python, Django REST Framework and Docker using Test Driven Development (TDD)

## Project Requirements
### Programming Languages
- [Python](https://www.python.org/)

### Database

### Frameworks
- [Django](https://www.djangoproject.com/) - Python web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - Django toolkit for building web APIs

### Libraries


### Tools
- [VS Code](https://code.visualstudio.com/) - IDE
- [PIP](https://pypi.org/project/pip/) - Python package manager

- [Git](https://git-scm.com/) - Version control system
- [GitHub](https://github.com/) - Version control system hosting service

- [Docker](https://www.docker.com/) - Containerization platform
- [Docker Compose](https://docs.docker.com/compose/) - Tool for defining and running multi-container Docker applications
- [Docker Hub](https://hub.docker.com/) - Container image registry

- [flake8](https://flake8.pycqa.org/en/latest/) - Python linting tool


## Project Preparation
## Local Development Environment Setup (Ubuntu 22.04)
##### Prerequisites
- Install Docker Engine

    https://docs.docker.com/engine/install/ubuntu/
- Install Docker Compose V2

    https://docs.docker.com/compose/install/linux/#install-using-the-repository
- Manage Docker as a non-root user(grand the user access to the docker command without needing to use sudo)

    https://docs.docker.com/engine/install/linux-postinstall/
- Clone the GitHub repository
    ```bash
    $ git clone git@github.com:FlashDrag/recipe-app-api.git <path_to_local_dir>
    ```

### Project Setup
- Create requirements.txt file and add the following:
    ```
    Django>=3.2.4,<3.3
    djangorestframework>=3.12.4,<3.13
    ```
- Create an empty `app` folder
- Configure linting with flake8
    - Create `requirements.dev.txt`. Dev requirements are only needed for development and testing in the local environment.
        ```
        flake8>=3.9.2,<3.10
        ```
    - Create `.flake8` file inside `app` folder and add the following:
        ```bash
        [flake8]
        exclude =
        migrations,
        __pycache__,
        manage.py,
        settings.py
        ```
- Create Dockerfile file and add the following:

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

    - Lighter Dockerfile configuration
```bash
# python image from docker hub
# alpine is an efficient and lightweight linux distro for docker
FROM python:3.11.6-alpine3.18

# maintainer of the image
LABEL maintainer="linkedin.com/in/pavlo-myskov"

# tells python to run in unbuffered mode.
# The output will be printed directly to the terminal
ENV PYTHONUNBUFFERED 1

# copy requirements.txt from local machine into docker image
COPY ./requirements.txt /tmp/requirements.txt
# copy the dev requirements file from local machine into docker image
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# copy the app folder from local machine into docker image
COPY ./app /app
# set the working directory.
# All subsequent commands will be run from this directory
WORKDIR /app
# Expose port 8000 from the container to outside world(our localhost)
# It allows us to access the port from our web browser
EXPOSE 8000

# set default environment variable
ARG DEV=false
# RUN - is a command to execute when building the image
# python -m venv /py - creates a virtual environment in the /py directory
# ... --upgrade pip - upgrades pip
# .. /tmp/requirements.txt - installs all the requirements
# rm -rf /tmp - removes the temporary directory
# adduser - creates a user inside the docker image(best practice to not run as root)
# --disabled-password - disables the password for the user
# --no-create-home - does not create a home directory for the user
# --django-user - name of the user
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ] ; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# update PATH environment variable to include the /py/bin directory
# so that we can run python commands without specifying the full path
ENV PATH="/py/bin:$PATH"

# specify the user that we're switching to
USER django-user

```
- Create `.dockerignore` file and add the following:
```bash
# Git
.git
.gitignore

# Docker
.docker

# Python
app/__pycache__/
app/*/__pycache__/
app/*/*/__pycache__/
app/*/*/*/__pycache__/
.env/
.venv/
venv/
```
- Build the docker image (optionally, as we're going to use docker-compose)
    ```bash
    $ sudo service docker start
    $ docker build .
    ```
- Create docker-compose.yml file and add the following:
```bash
# version of docker-compose syntax
version: '3.9'

# define services
services:
  # name of the service
  app:
    build:
      # path to the Dockerfile
      context: .
      # override the default environment variable
      args:
        - DEV=true
    # port mapping. Maps port 8000 on the host to port 8000 on the container
    ports:
      - '8000:8000'
    # volumes to mount. Mounts the app directory on the host to the /app directory on the container.
    # Allows to reflect changes made on the host in the container without having to rebuild the container.
    volumes:
      - ./app:/app
      # `- ./app:/home/django-user/app` - for dev container development
    # command to run when the container starts
    command: >
      sh -c 'python manage.py runserver 0.0.0.0:8000'
```
- Build the docker image
    ```bash
    $ docker compose build
    ```
- Create a Django project
    ```bash
    $ docker compose run --rm app sh -c "django-admin startproject app ."
    ```
- Start the Django development server
    ```bash
    $ docker compose up
    ```

### Local Development
Choose one of the following options:
#### 1. Dev Container
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
- Use Dockerfile config for dev containers
- Open the Command Palette (Ctrl+Shift+P) and run the **Remote-Containers: Reopen in Container** command.

#### 2. Local virtual environment
Since you've mounted your app codebase as a Docker volume you can develop your application directly on your local machine and see the changes reflected in the container without having to rebuild the container.
##### Setup Local Virtual Environment
- Create virtual environment using virtualwrapper
    ```bash
    $ mkvirtualenv recipe-app-api
    ```
- Install requirements
    ```bash
    $ pip install -r requirements.txt
    ```
- Install dev requirements
    ```bash
    $ pip install -r requirements.dev.txt
    ```
- All development dependencies you can add to `requirements.dev.txt` file.
- **Make sure the all dependencies including python version on your local machine match the dependencies in the container to avoid any issues.**


### Useful Commands
- Linting
    ```bash
    $ docker compose run --rm app sh -c "flake8"
    ```
- Test
    ```bash
    $ docker compose run --rm app sh -c "python manage.py test"
    ```
- Start Docker Daemon
    ```bash
    $ sudo service docker start
    ```
- Build the docker image from docker-compose.yml file
    ```bash
    $ docker compose build
    ```
- Build the docker image from Dockerfile
    ```bash
    $ docker build .
    ```
- Start the Django development server
    ```bash
    $ docker compose up
    ```
- Remove old containers
    ```bash
    $ docker compose down
    ```
- Rebuild the docker image
    ```bash
    $ docker compose up --build
    ```
- Check images
    ```bash
    $ docker images
    ```
- Check files in the image
    ```bash
    $ docker run -it <image_id> sh
    ```

## Production Environment Setup
### Docker Hub Configuration
DockerHub is a platform that allows us to pull Docker images down to our local machine and push Docker images up to the cloud.

- Docker Hub account
    https://hub.docker.com/
- Create New Access Token
    - Go to https://hub.docker.com/ > Account Settings > Security > New Access Token
    - Token Description: `recipe-app-api-github-actions`
    - Access permissions: `read-only`
    - Don't close token, until you've copied and pasted it into your GitHub repository

    - Warning: Use different tokens for different environments
    - To use access token from your Docker CLI client(at the password prompt use the access token as the password)
        ```bash
        $ docker login -u <username>
        ```

### GitHub Actions Configuration
- Create new repo if not exists
- Add Docker Hub secrets to GitHub repository for GitHub Actions jobs

    _Settings > Secrets > Actions > New repository secret_

    - `DOCKERHUB_USER`: `<username>`

    - `DOCKERHUB_TOKEN`: `<access_token>`
- Create a config file at `.github/workflows/checks.yml`
```bash
---
name: Checks

on: [push]

jobs:
  test-lint:
    name: Test and Lint
    runs-on: ubuntu-22.04
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USER }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: Checkout
        uses: actions/checkout@v4
      - name: Test
        run: docker compose run --rm app sh -c "python manage.py test"
      - name: Lint
        run: docker compose run --rm app sh -c "flake8"
```