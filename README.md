## General playground for flask and angularjs ##

Requires: Python >3.6

### Usage ###

**Update campaign version**

```bash
curl -X PUT -d '{"version": "2.3.0.4"}' http://localhost:5000/api/campaign/2.3.0.5 --header "Content-Type:application/json"
```

**Get all campaign versions**

```bash
curl http://localhost:5000/api/campaign
```

**Delete campaign version**

```bash
curl -X DELETE http://localhost:5000/api/campaign/2.3.0.5
```

**Get tests**

```bash
curl -i http://localhost:5000/api/tests\?version\=2.3.0.4

curl -i http://localhost:5000/api/tests

curl -i http://localhost:5000/api/tests\?version\=2.3.0.4\&filter\=project\;doors_id
```

**Update test**

```bash
curl -X PUT -d '{"result": [{"project": "MAV", "result": "OK"}],"comment": "updated"}' http://localhost:5000/api/tests/1 --header "Content-Type:application/json"
```

**Update multiple tests based on filter**

```bash
curl -X PATCH -d '{"project": "PKP","result": "OK"}' http://localhost:5000/api/tests\?version\=2.4.0.3\&automated\=1 --header "Content-Type:application/json"
```

**Delete test**

```bash
curl -X DELETE http://localhost:5000/api/tests/3
```

**Create a new campaign**

```bash
curl -F "file=@doors.zip" -F "version=2.4.0.1" http://localhost:5000/api/campaign
```

### Installation: ###

First create the venv:

```bash
cd <project_home>
python -m venv venv
```

Install all modules from requirements.txt:

```bash
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Create database:

```bash
python run.py shell
    db.create_all()
```

**Start application**

Execute command `python run.py runserver`

**Gunicorn setup**

Create file `/lib/systemd/system/myproject-gunicorn.service` with contents:

```
# Gunicorn Site systemd service file

[Unit]
Description=Gunicorn server for myproject
After=network.target
After=syslog.target

[Service]
User=asoriga
Group=www-data
WorkingDirectory=/home/asoriga/application/python3-mqtt-app
Environment=PATH=/home/asoriga/application/python3-mqtt-app/venv/bin
ExecStart=/home/asoriga/application/python3-mqtt-app/venv/bin/gunicorn --worker-class eventlet --workers 1 --bind unix:myproject.sock wsgi:app --env FLASK_CONF_FILE="/home/asoriga/application/config.yml" --env FLASK_CONF_ENV="PRODUCTION"

Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Gunicorn process can now be managed using commands:

```bash
systemctl daemon-reload
sudo systemctl stop myproject-gunicorn.service
sudo systemctl start myproject-gunicorn.service
sudo systemctl status myproject-gunicorn.service
```

**Nginx setup**

WARNING: remove the default connection from `/etc/nginx/sites-enabled/default`

Nginx configuration file (`/etc/nginx/sites-available/myproject`) shall look like:

```
server {
    listen 80;
    server_name "";

    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx.key;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/myproject/myproject.sock;
    }
}
```

**Debug**

NGINX wrror file: `/var/log/nginx/error.log`

If permission errors use this hack (find a better alternative for this):

    chmod g+x /home/<user>/
    chmod g+r /home/<user>/

And also set all permissions to the `myproject` folder...

**Misc**

To update python packages run:

```
pip install -U $(pip list --outdated|awk '{printf $1" "}')
```
