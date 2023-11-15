# Useful Commands
- Start Docker Daemon
```bash
$ sudo service docker start
```
- Build the docker image based on Dockerfile
```bash
$ docker build .
```
- Build the docker image based on docker-compose.yml file
```bash
$ docker compose build
```
- Build the docker image based on specific docker compose file
```bash
$ docker compose -f docker-compose-deploy.yml build
```
- Rebuild the docker image
```bash
$ docker compose up --build
```
- Run the docker containers based on docker-compose.yml file
```bash
$ docker compose up
```
- Run the docker containers based on specific docker compose file
```bash
$ docker compose -f docker-compose-deploy.yml up
```
- Rebuild and run the docker containers based on specific docker compose file
```bash
$ docker compose -f docker-compose-deploy.yml up --build
```
- Check images
```bash
$ docker images
```
- Check files in the image
```bash
$ docker run -it <image_id> sh
```
- Remove containers
```bash
$ docker compose down
```
- Remove containers of specific docker-compose.yml file
```bash
$ docker compose -f docker-compose-deploy.yml down
```
- Remove all images without at least one container associated to them
```bash
$ docker image prune
```
- View all volumes
```bash
$ docker volume ls
```
- Remove volumes
```bash
$ docker volume rm <volume_name>
```
- Remove volumes of specific docker-compose.yml file
```bash
$ docker-compose -f docker-compose-deploy.yml down --volumes
```
- Check logs of the container on production
```bash
$ docker-compose -f docker-compose-deploy.yml logs
```

## Run commands inside the container
- Using `docker compose run` command
    ```bash
    $ docker compose run --rm app sh -c "<command>"

    # docker compose run - runs a one-off command
    # --rm - removes the container after finish running
    # app - name of the service in docker-compose.yml file
    # sh -c - shell command
    ```
- Using specific docker-compose.yml file
    ```bash
    $ docker compose -f docker-compose-deploy.yml run --rm app sh -c "<django-command>"
    ```

- Open a shell terminal inside the container. Allows to run commands directly inside the container.
    ```bash
    $ docker exec -it <running_container_name> sh
    ```
- Alias for `docker compose run` command:
    - Add the following alias to your `.bashrc` or `.bash_aliases` file:
        ```bash
        alias drun='docker compose run --rm app sh -c'
        # or
        drun() {
            docker compose run --rm app sh -c "$*"
        }
        # automatically wraps arguments in quotes
        ```
    - Apply changes
        ```bash
        $ source ~/.bashrc
        ```
    - Now you can run commands using `drun` alias:
        ```bash
        $ drun "<command>"

        $ drun "python manage.py test"  # e.g.
        ```

## Generate Django Secret Key
- Open a shell terminal inside the container
    ```bash
    $ docker compose run --rm app sh -c "python manage.py shell"
    ```
- Generate secret key
    ```python
    >>> from django.core.management.utils import get_random_secret_key
    >>> get_random_secret_key()
    ```

[Back to top ↑](#useful-commands)

[Back to README.md](README.md)