# Useful Commands
- Start Docker Daemon
    ```bash
    $ sudo service docker start
    ```
- Build the docker image based on docker-compose.yml file
    ```bash
    $ docker compose build
    ```
- Build the docker image based on Dockerfile
    ```bash
    $ docker build .
    ```
- Rebuild the docker image
    ```bash
    $ docker compose up --build
    ```
- Run the docker containers based on docker-compose.yml file
    ```bash
    $ docker compose up
    ```
- Check images
    ```bash
    $ docker images
    ```
- Check files in the image
    ```bash
    $ docker run -it <image_id> sh
    ```
- Remove old containers
    ```bash
    $ docker compose down
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