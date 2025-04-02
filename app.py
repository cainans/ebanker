from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

accounts = []

class accountBalance(Resource):
    def get(self):
        try:
            account_id = int(request.args.get('account_id'))
        except Exception:
            response = jsonify({"message": "Invalid or missing account_id"})
            response.status_code = 400
            return response

        account = next((acc for acc in accounts if acc["id"] == account_id), None)

        if account:
            response = jsonify(account["value"])
            response.status_code = 200
        else:
            response = jsonify(0)
            response.status_code = 404

        return response


class accountEvent(Resource):
    def get(self, user_id):
        user = next((u for u in users if u["id"] == user_id), None)
        if user:
            return jsonify(user)
        response = jsonify({"message": "User not found"})
        response.status_code = 404
        return response

    def delete(self, user_id):
        global users

        if not any(user["id"] == user_id for user in users):
            response = jsonify({"message": "User not found"})
            response.status_code = 404
        else:
            users[:] = [u for u in users if u["id"] != user_id]

            response = jsonify({"message": "User deleted"})
            response.status_code = 200
        return response

api.add_resource(accountEvent, '/event')
api.add_resource(accountBalance, '/balance')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
