# Recipe API
REST API with Python, Django REST Framework and Docker using Test Driven Development (TDD)


## Features
- Django UI admin panel
- Token-based authentication
- User management
    * Create user
    * Update user *(auth required)*
    * Get user detail *(auth required)*

- Recipe management *(auth required)*
    - Recipe API
        * View list of recipes
        * View detail of specific recipe
        * Create recipe
        * Update recipe
        * Delete recipe
    - Tags API
        * View list of tags
        * Create tag (accepts multiple tags when creating a recipe)
        * Update tag
        * Delete tag

## Documentation
The API documentation is created using [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/).
- Swagger UI: `<host>/api/docs/`
- ReDoc: `<host>/api/redoc/`
- OpenAPI schema: `<host>/api/schema/`
#### Django UI admin panel
`<host>/admin/`

#### User authentication with Token
- Create new user or use existing one
- To get a token, send a `POST` request to `<host>/api/user/token/` with the following payload:
    ```json
    {
        "email": "<user_email>",
        "password": "<user_password>"
    }
    ```
##### Swagger UI
- Copy the token from the response
- Click on the *Authorize* button in the top right corner
- Enter the `Token <token>` in the *Value* field of the *tokenAuth (apiKey)* section
##### Frontend App
- Save the token in the local storage
- Add the `Authorization: Token <token>` header to the request every time you make a request to the API

## Entity-Relationship Diagram
![ERD](docs/erd.png)

## Technologies Used
### Programming Languages
- [Python](https://www.python.org/)

### Frameworks
- [Django](https://www.djangoproject.com/) - Python web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - Django toolkit for building web APIs

### Libraries
- [flake8](https://flake8.pycqa.org/en/latest/) - Python linting tool
- [psycopg2](https://www.psycopg.org/) - PostgreSQL database adapter for Python
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) - OpenAPI schema generation for Django REST framework

### Tools
- [VS Code](https://code.visualstudio.com/) - IDE
- [PIP](https://pypi.org/project/pip/) - Python package manager

- [Git](https://git-scm.com/) - Version control system
- [GitHub](https://github.com/) - Version control system hosting service

- [Docker](https://www.docker.com/) - Containerization platform
- [Docker Compose](https://docs.docker.com/compose/) - Tool for defining and running multi-container Docker applications
- [Docker Hub](https://hub.docker.com/) - Container image registry


## Local Usage
- Clone the GitHub repository
    ```bash
    $ git clone
    ```
- Build the docker image
    ```bash
    $ docker compose build
    ```
- Run the containers
    ```bash
    $ docker compose up
    ```

## Project Development
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

### Project(Django) Setup
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
    # Maps directory in the container to the directory on the local machine
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

### Project(Database) Setup
#### Configure Docker for PostgreSQL
- Add PostgreSQL database to docker-compose.yml file
```bash
# ...
services:
    app:
        # specifies that the app service depends on the db service
        # also, it ensures that the db service is started before the app service
        depends_on:
            - db
        # ...
        # allows to connect to the database from the app service,
        # must match the credentials in the db service
        environment:
            # hostname of the database - the name of the service in docker-compose.yml file
            - DB_HOST=db
            - DB_NAME=devdb
            - DB_USER=devuser
            - DB_PASS=postgres

    # add db service,
    # `app` service will use `db` as a hostname to connect to the database
    db:
        # docker hub image to use
        image: postgres:13-alpine
        volumes:
            - dev-db-data:/var/lib/postgresql/data/
        environment:
            - POSTGRES_DB=devdb
            - POSTGRES_USER=devuser
            - POSTGRES_PASSWORD=postgres
        ports:
        - '5432:5432'

# named volumes
volumes:
    dev-db-data:
    dev-static-data:
```
- Run the containers to create the database
```bash
    $ docker compose up
```
- Add `psycopg2` dependencies to Dockerfile
```bash
# ...
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # install psycopg2 dependencies
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    # ...
    rm -rf /tmp && \
    # delete the .tmp-build-deps
    apk del .tmp-build-deps && \
    # ...
```
- Add `psycopg2` package to requirements.txt file
```
psycopg2>=2.8.6,>2.9
```
#### Configure Django to use PostgreSQL
- Add database configuration to settings.py file
```
# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
```
- Add database credentials to *.env* file. See the *.env.example* file for reference.
- Rebuild the docker image
```bash
$ docker compose up --build
```
##### Setup `wait_for_db` custom management command
Allows to wait for the database to be available before running the Django app.
- Create a new *core* app
```bash
$ docker compose run --rm app sh -c "python manage.py startapp core"
```
- Create a new *management* module with *commands* subdirectory inside *core* app
```bash
$ mkdir -p app/core/management/commands && touch app/core/management/__init__.py && touch app/core/management/commands/__init__.py
```
- Create a new *wait_for_db.py* file inside *commands* subdirectory
```bash
$ touch app/core/management/commands/wait_for_db.py
```
- Configure *wait_for_db.py* file. See the [file](app/core/management/commands/wait_for_db.py) for reference.
- Add *wait_for_db* command to *docker-compose.yml* file
```
# ...
services:
    app:
        # ...
        # command to run when the container starts
        command: >
            sh -c "python manage.py wait_for_db &&
                    python manage.py migrate &&
                    python manage.py runserver 0.0.0.0:8000"
```
- Clean up the containers
```bash
$ docker compose down
```
- Run the containers (optionally, for testing)
It is better first time to migrate the database after the *CustomUser* model has been created.
```bash
$ docker compose up
```
#### Create a Custom User Model
- Create a Custom User Model and a Custom User Manager. See the [file](app/core/models.py) for reference.
- Add `AUTH_USER_MODEL = 'core.User'` to *settings.py* file
- Make and apply migrations
```bash
$ docker compose run --rm app sh -c "python manage.py makemigrations core"
$ docker compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"
```
- Remove the db volume
In case, if you applied initial migrations before creating the Custom User Model. It will clean up the database.
```bash
$ docker volume rm recipe-app-api_dev-db-data
```
#### Configure DRF to use drf_spectacular
It allows to generate OpenAPI schema for the API.
- Add `drf_spectacular` package to requirements.txt file
- Add `rest_framework` and `drf_spectacular` to *INSTALLED_APPS* in *settings.py* file
- Add `REST_FRAMEWORK = {'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',}` to *settings.py* file
- Add url patterns to *urls.py* file
```python
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)
# ...

urlpatterns = [
    # ...
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    )
]
```
- Rebuild the docker image

### Local Development
Choose one of the following options:
#### 1. [VSCode dev container](dev_container.md)
Allows to develop the application inside a container using VSCode.

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
        run: docker compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"
      - name: Lint
        run: docker compose run --rm app sh -c "flake8"
```