# API Server

## Prerequisites

Before deploying the server be sure to install the following packages:

### Ubuntu/Debian:

- unixodbc-dev
- python3-dev
- default-libmysqlclient-dev
- build-essential

If using a different distro, install the appropriate equivalent

### Python packages:

- pipenv

## Installation

### Prelogue

If you plan to use the OHCA API server with nginx, it is higly recommended that it be installed in `/var/www/...` with `www-data:www-data` as the owner. 

### Development

First clone the repo and cd into the API's directory (use `api-stable` for production o `api-dev` for development)

```bash
git clone --single-branch --branch api-stable https://github.com/SterArcher/OHCA-registry-Slovenia.git
cd OHCA-registry-Slovenia
```

Next we'll install a virtual environment for Python

```bash
mkdir .venv
pipenv install
```
This will download and install all the needed Python packages and install them in the virtual environment so as not to mess with your system Python installation

Next we need to set the appropriate environment variables in the `.env` file

```bash
echo "ALLOWED_HOSTS= 
DATABASE=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASS=
DATABASE_HOST=
DATABASE_PORT=" > .env
```

- **ALLOWED_HOSTS** should contain a comma separated list of hosts on which the API will be available. To allow any connection a wildcard (`*`) can be specified. Defaults to `*`.
- **DATABASE** specifies the type of database. Supported types are:
    - MySQL (`msql`)
    - MariaDB (`mariadb`)
    - Microsoft SQL Server (`mssql`)
    - PostgreSQL (`postresql`)
- **DATABASE_NAME** specifies the database name.
- **DATABASE_USER** specifies the database username.
- **DATABASE_PASS** specifies the password for DATABASE_USER
- **DATABASE_HOST** specifies the database address. Defaults to `localhost`.
- **DATABASE_PORT** specifies the port at which the database is reachable. Defaults to default of specified DATABASE.

Before running the server for the first time we have to add a SECRET_KEY for encryption

```bash
echo "SECRET_KEY=$(openssl rand -base64 48)" >> ohca/settings.py
```

Now we can finally run the server for the first time.

```bash
pipenv shell # Enter the virtual environment
./manage.py makemigrations
./manage.py migrate # Create the necessary db structures
./manage.py createsuperuser # Create a superuser for the admin console
./manage.py runserver # Actually run the server
```

The server should now be available at http://127.0.0.1:8000. The server should only be used for development purposes. 

### Production

To run the API in a production environment you should se Gunicorn or another WSGI in conjunction with Nginx (or similar). First stop the server instance started above, then let's start a Gunicorn instance.

```bash
gunicorn --workers 3 --bind unix:ohca.sock -m 007 ohca.wsgi
```

The server is now available at the unix socket `ohca.sock` (`http://unix:/path/to/ohca.sock`). To allow access to the server we need to set up Nginx as a reverse proxy to the socket. To do this we can use the provided helper script `generate.py`

```bash
./generate.py nginx > ohca.conf
```

The script will output an appropriate Nginx config file, which can then be installed to the sites-enabled directory, usually `/etc/nginx/sites-enabled`. After that restart nginx and you're ready to go.

### Systemd service

In a production setting it's advised to run the server as a daemon or service. The `generate.py` script provides an easy service generator.

To generate a service file with www-data as the service user and group (recommended) run.

```bash
./generate.py systemd www-data www-data > ohca-api.service
```

Before starting the service make sure to set the correct permissions of the current directory

```bash
chown www-data:www-data -R ./
```

All that's left is to install the service to the appropiate directory and start it.

```bash
sudo cp ohca-api.service /etc/systemd/system
sudo systemctl start ohca-api
```

To run the service at start up run

```bash
sudo systemctl enable ohca-api
```