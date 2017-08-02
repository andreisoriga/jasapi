## General playground for flask and angularjs ##

Requires: Python >3.6

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
