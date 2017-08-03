## Just Another Stupid Api used for fast storing of json data ##

Requires: Python >3.6

## Usage ##

Create a new resource:

    curl -X POST -i http://127.0.0.1:5000/api/<TABLE> -d '<JSON_DATA>' --header "Content-Type:application/json"

    Example:
    curl -X POST -i http://127.0.0.1:5000/api/user -d '{"name": "John Doe", "age": 20}' --header "Content-Type:application/json"


GET all rows from specified table:

    curl -i http://127.0.0.1:5000/api/<TABLE>

    Example:
    curl -i http://127.0.0.1:5000/api/user


DELETE one item from specified table and id:

    curl -X DELETE -i http://127.0.0.1:5000/api/<TABLE>/<ID> --header "Content-Type:application/json"

    Example:
    curl -X DELETE -i http://127.0.0.1:5000/api/user/2 --header "Content-Type:application/json"

PUT (update) a row from specified table and id:

    curl -X PUT -i http://127.0.0.1:5000/api/<TABLE>/<ID> -d '<JSON_DATA_WITH_ID>' --header "Content-Type:application/json"

    Example:
    curl -X PUT -i http://127.0.0.1:5000/api/user/3 -d '{"id": 3, "name": "John Michael", "age": 40}' --header "Content-Type:application/json"

DELETE all data (drops the table):

    curl -X DELETE -i http://127.0.0.1:5000/api/<TABLE>

    Example:
    curl -X DELETE -i http://127.0.0.1:5000/api/user

### Installation: ###

**Install Python 3.6+**

    sudo apt-get install build-essential libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl

Grab the latest Python version from https://www.python.org/downloads/

Unpack it, cd into the new directory and execute:

    ./configure

    make

    sudo make install

Test if the version is correct:

    python3.6 --version
    pip3.6 --version

If pip was not updated to Python 3.6, install this one also from sources:

    wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate
    sudo python3.6 get-pip.py

    pip3.6 --version

**create the venv**

    cd <project_home>
    python3.6 -m venv venv


Install all modules from requirements.txt:

    source venv/bin/activate
    pip install -r requirements.txt
    deactivate

**Nginx setup**

Install nginx:

    sudo apt install nginx

Nginx configuration file (`/etc/nginx/sites-available/myproject`) shall look like:

    server {
        listen 5000;
        listen [::]:5000;

        server_name _;

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/webuser/myproject/myproject.sock;
        }
    }

Check config:

    sudo nginx -t

Enable server:

Go to `/etc/nginx/sites-enabled/` and:

    sudo rm default
    sudo ln -s /etc/nginx/sites-available/myproject myproject

Restart nginx:

    sudo service nginx restart

**Nginx Debug**

NGINX error file: `/var/log/nginx/error.log`

**Gunicorn setup**

Create file `/lib/systemd/system/myproject-gunicorn.service` with contents:

    # Gunicorn Site systemd service file

    [Unit]
    Description=Gunicorn server for myproject
    Wants=network-online.target
    After=network.target network-online.target

    [Service]
    User=webuser
    Group=www-data
    WorkingDirectory=/home/user/myproject
    Environment=PATH=/home/user/myproject/venv/bin
    ExecStart=/home/user/myproject/venv/bin/gunicorn --worker-class eventlet --workers 4 --bind unix:myproject.sock wsgi:app --env FLASK_CONF_FILE="/home/user/myproject/config.yml" --env FLASK_CONF_ENV="PRODUCTION"

    Restart=on-failure

    [Install]
    WantedBy=multi-user.target

Gunicorn process can now be managed using commands:

    sudo systemctl daemon-reload
    sudo systemctl stop myproject-gunicorn.service
    sudo systemctl start myproject-gunicorn.service
    sudo systemctl status myproject-gunicorn.service

**Misc**

To update python packages run:

```
pip install -U $(pip list --outdated|awk '{printf $1" "}')
```
