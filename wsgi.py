import os

from werkzeug.contrib.fixers import ProxyFix

from src.app import create_app
from src.utils import get_app_root_path

app = create_app(os.getenv('FLASK_CONF_FILE', str(get_app_root_path() / 'config.yml')),
                 os.getenv('FLASK_CONF_ENV', 'DEVELOPMENT'))

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run()
