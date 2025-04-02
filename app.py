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

    def post(self):
        new_user = request.get_json()
        users.append(new_user)
        return jsonify({"message": "New user added", "user": new_user})

class User(Resource):
    def get(self, user_id):
        user = next((u for u in users if u["id"] == user_id), None)
        if user:
            return jsonify(user)
        response = jsonify({"message": "User not found"})
        response.status_code = 404
        return response

    def delete(self, user_id):
        global users
        user = [u for u in users if u["id"] != user_id]
        return jsonify({"message": "User deleted"})

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
