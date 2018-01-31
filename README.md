## hdtapps-prototype: 
A prototypical implementation of a framework for handling data transformation applications in the context of TraDE Middleware 

Requirements:
Python 3.6, MongoDB, Docker, Celery+Redis as a broker

## Installation

1. Create virtual environment: <br>
  a) navigate to project's folder <br>
  b) create virtual environment: <b>python -m venv venv</b>  <br>

2. Activate virtual environment: <br>
   Linux: source venv/bin/activate <br>
   Windows: venv\Scripts\activate.bat <br>

3. Install using pip: pip install -r requirements.txt (or pip3 install -r requirements.txt) <br>
4. Change MongoDB and Redis configurations in config.py if not default ports are used

## Running

1. In one terminal instance activate the virtual environment and run a Celery worker
 using the following command: <b>celery worker -A celery_worker.celery --loglevel=info</b><br>
2. In another terminal instance activate the virtual environment and run the application using the following command: <b>python -m run </b><br>
3. Connect using localhost:8080 <br>
4. Test API calls at http://localhost:8080/ui using <a href="https://github.com/swagger-api/swagger-ui">Swagger UI</a>

## Project's structure

- app/ - application <br>
--- mod_repo/ - repository module <br>
--- mod_tm/ - task manager module <br>
--- mod_swagger_ui/ - <a href="https://github.com/swagger-api/swagger-ui">Swagger UI</a> to simplify working with prototype's API <br>
--- static/ - static files <br>
--- templates/ - Jinja2 templates <br>
- config.py - configuration settings <br>
- run.py - launcher

## Dockerized version

Configure the Docker daemon so that it exposes the API as described here: [Docker Daemon Configuration](https://docs.docker.com/engine/admin/#configure-the-docker-daemon)

For example, set/extend `/etc/docker/daemon.json` on Linux as follows:
```
{
  "hosts": ["tcp://0.0.0.0:2376", "unix:///var/run/docker.sock", ...]
}
```

Since this opens the Docker API to remote systems it is recommended to set corresponding firewall rules that only allow clients running in local Docker containers or on the host itself to access the API endpoint. Please check therefore the documentation of your underlying OS how to configure such firewall rules. To get the IP range of the containers your can execute the following command `docker network inspect bridge` that returns the subnet (e.g., 172.17.0.0) used for the containers. With this information you can create a corresponding rule that only allows connections to the Docker API from localhost and the IP range of the containers (or any other remote host you want to explicitly give access to it).

Adapt the `docker-compose.yml` file to your local setup, e.g., change potentially conflicting port mappings of the services and update the `DOCKER_HOST` environment variable values using your local IP address and the port specified in `/etc/docker/daemon.json`. For example, this will result in `DOCKER_HOST=http://192.168.109.132:2376`. This is required so that the hdtapps-framework container can send commands to the Docker engine running on the host.

Use `docker-compose build` within the root folder of the project to pull or build all required images.

With `docker-compose up -d` the required framework containers can be created and started (four containers: hdtapps-framework, mongodb, celery-worker, redis) in the background.
Without setting `-d`the log outputs of all containers are forwarded to the current terminal which can be helpful for debugging.
To stop and destroy all running containers execute `docker-compose down` which removes also all related resources such as volumes, networks, etc.

A complete list of docker-compose commands and their parameters can be found here: [Docker Docs](https://docs.docker.com/compose/reference/overview/)
