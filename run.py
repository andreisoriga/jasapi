import os

from flask_script import Manager, Server

from src.app import create_app
from src.utils import get_app_root_path

app = create_app(os.getenv('FLAKS_CONF_FILE', str(get_app_root_path() / 'config.yml')),
                 os.getenv('FLASK_CONF_ENV', 'DEVELOPMENT'))

# Flask-scripts specific
manager = Manager(app)
manager.add_command("runserver", Server())
server = Server(host=app.config['APP_IP'],
                port=app.config['APP_PORT'],
                debug=app.config['DEBUG'])


@manager.shell
def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()
