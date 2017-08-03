from flask import g, request
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

    api.add_resource(ItemList, '/api/<table>')
    api.add_resource(Item, '/api/<table>/<idx>')

    return app


class Item(Resource):

    def get(self, table, idx):
        """ Grabs a row from table based on the id

        return status code: 200 (OK) | 404 (Not found)
        """

        db = get_db()
        data = db[table].find_one(id=idx)

        return data if data else '', 404

    def delete(self, table, idx):
        """ Delete rows from the table.

            return status code: 204 (No Content) | 404 (Not found)
        """

        db = get_db()

        status = db[table].delete(id=idx)

        if not status:
            return '', 404

        return '', 204

    def put(self, table, idx):
        """ Update a row in the table.

            return status code: 201 (Created) | 404 (Not found)
        """

        db = get_db()

        json_data = request.get_json(force=True)
        state = db[table].update(json_data, ['id'])

        if not state:
            return '', 404

        return '', 201


class ItemList(Resource):

    # def __init__(self):
    #     self.reqparse = reqparse.RequestParser()
    #     self.reqparse.add_argument('name', type=str, required=True, help='No task title provided', location='json')
    #     self.reqparse.add_argument('age', type=int, default="", location='json')

    #     super(ItemList, self).__init__()

    def get(self, table):
        """ Grabs all rows from table

        return status code: 200 (OK)
        """

        db = get_db()
        return list(db[table].all())

    def post(self, table):
        """ Create a new row

        return status code: 201 (Created)
        """

        # args = self.reqparse.parse_args()
        db = get_db()

        json_data = request.get_json(force=True)
        item_id = db[table].insert(json_data)

        return item_id, 201

    def delete(self, table):
        """ Drops the table

        return status code: 204 (No Content)
        """

        db = get_db()

        status = db[table].drop()

        if not status:
            return '', 500

        return '', 204
