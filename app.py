from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

users = [
    {"id": 1, "name": "Cainan"},
    {"id": 2, "name": "Rob"}
]

class UserList(Resource):
    def get(self):
        return jsonify(users)
