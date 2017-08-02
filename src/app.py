from flask import g
from flask_restful import Resource, Api
from flask_cors import CORS

from src.extensions import Flask

import dataset


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = dataset.connect('sqlite:///src/db/dba.db')
    return db


def create_app(config_file, config_env):
    app = Flask(__name__, static_url_path='')
    api = Api(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_yaml(config_file, config_env)
    app.url_map.strict_slashes = False

    api.add_resource(TodoList, '/api/todos')
    api.add_resource(Todo, '/api/todos/<idx>')

    return app


class Todo(Resource):

    def get(self, idx):
        db = get_db()
        table = db['user']

        # Insert a new record.
        # table.insert(dict(name='John Doe', age=46, country='China'))

        return table.find_one(id=idx)

    # def delete(self, todo_id):
    #     abort_if_todo_doesnt_exist(todo_id)
    #     del TODOS[todo_id]
    #     return '', 204

    # def put(self, todo_id):
    #     args = parser.parse_args()
    #     task = {'task': args['task']}
    #     TODOS[todo_id] = task
    #     return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        db = get_db()
        table = db['todos']
        return table.all()

    # def post(self):
    #     args = parser.parse_args()
    #     todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
    #     todo_id = 'todo%i' % todo_id
    #     TODOS[todo_id] = {'task': args['task']}
    #     return TODOS[todo_id], 201
