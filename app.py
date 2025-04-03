import json
from collections import OrderedDict
from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

accounts = []

class accountBalance(Resource):
    def get(self):
        try:
            account_id = request.args.get('account_id')
        except Exception:
            response = jsonify({"message": "Invalid or missing account_id"})
            response.status_code = 400
            return response

        account = next((acc for acc in accounts if acc["id"] == account_id), None)

        if account:
            response = jsonify(account["balance"])
            response.status_code = 200
        else:
            response = jsonify(0)
            response.status_code = 404

        return response


class accountEvent(Resource):
    def post(self):
        event = request.get_json()

        if event["type"] == "deposit":
            response = self.accountDeposit(event)
       #elif event["type"] == "withdraw":
           #response = self.accountWithdraw(event)
       #elif event["type"] == "transfer":
           #response = self.accountTransfer(event)
        else:
            response = jsonify({"message": "Invalid event type"})
            response.status_code = 404

        return response

    def accountDeposit(self, event):
        global accounts

        for i, acc in enumerate(accounts):
            if acc["id"] == event["destination"]:
                accounts[i]["balance"] += event["amount"]
                break
        else:
            accounts.append({"id": event["destination"], "balance": event["amount"]})

        updated_account = next(acc for acc in accounts if acc["id"] == event["destination"])
        ordered_response = OrderedDict([
            ("destination", OrderedDict([
                ("id", updated_account["id"]),
                ("balance", updated_account["balance"])
            ]))
        ])

        json_response = json.dumps(ordered_response)
        return Response(json_response, status=201, mimetype='application/json')

    def accountWithdraw(self, event):
        return

    def accountTransfer(self, event):
        return


class resetAccounts(Resource):
    def post(self):
        global accounts

        accounts[:] = []

        return

api.add_resource(accountEvent, '/event')
api.add_resource(accountBalance, '/balance')
api.add_resource(resetAccounts, '/reset')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
