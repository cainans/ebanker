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
        elif event["type"] == "withdraw":
            response = self.accountWithdraw(event)
        elif event["type"] == "transfer":
            response = self.accountTransfer(event)
        else:
            response = jsonify({"message": "Invalid event type"})
            response.status_code = 404

        return response

    def accountDeposit(self, event):
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
        for i, acc in enumerate(accounts):
            if acc["id"] == event["origin"]:
                if acc["balance"] >= event["amount"]:
                    accounts[i]["balance"] -= event["amount"]

                    ordered_response = OrderedDict([
                        ("origin", OrderedDict([
                            ("id", accounts[i]["id"]),
                            ("balance", accounts[i]["balance"])
                        ]))
                    ])
                else:
                    response = jsonify({"message": "Insufficient funds"})
                    response.status_code = 400
                    return response

                break
        else:
            response = jsonify(0)
            response.status_code = 404
            return response

        json_response = json.dumps(ordered_response)
        return Response(json_response, status=201, mimetype='application/json')

    def accountTransfer(self, event):
        ordered_response, idx_origin, idx_destination = None, None, None

        if event["origin"] is None or event["destination"] is None or event["amount"] is None:
            response = jsonify(0)
            response.status_code = 404
            return response

        for i, acc in enumerate(accounts):
            if acc["id"] == event["origin"]:
                idx_origin = i
            elif acc["id"] == event["destination"]:
                idx_destination = i

        if idx_origin is not None:
            if accounts[idx_origin]["balance"] >= event["amount"]:
                accounts[idx_origin]["balance"] -= event["amount"]

            if idx_destination is not None:
                accounts[idx_destination]["balance"] += event["amount"]
            else:
                accounts.append({"id": event["destination"], "balance": event["amount"]})
                idx_destination = len(accounts) - 1

        else:
            response = jsonify(0)
            response.status_code = 404
            return response

        ordered_response = OrderedDict([
            ("origin", OrderedDict([
                ("id", accounts[idx_origin]["id"]),
                ("balance", accounts[idx_origin]["balance"])
            ])),
            ("destination", OrderedDict([
                ("id", accounts[idx_destination]["id"]),
                ("balance", accounts[idx_destination]["balance"])
            ]))
        ])

        json_response = json.dumps(ordered_response)
        return Response(json_response, status=201, mimetype='application/json')


class resetAccounts(Resource):
    def post(self):
        global accounts

        accounts[:] = []

        return Response(status=200)
        
api.add_resource(accountEvent, '/event')
api.add_resource(accountBalance, '/balance')
api.add_resource(resetAccounts, '/reset')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
