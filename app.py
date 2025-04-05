from flask import Flask, request
from flask_restful import Api, Resource
from service.account_service import AccountService
from store.account_store import AccountStore

app = Flask(__name__)
api = Api(app)

store = AccountStore()
service = AccountService(store)

class ResetAccounts(Resource):
    def post(self):
        service.reset()

        return 'OK', 200

class AccountBalance(Resource):
    def get(self):
        account_id = request.args.get('account_id')
        balance = service.get_balance(account_id)

        if balance is not None:
            return balance, 200
        else:
            return 0, 404

class AccountEvent(Resource):
    def post(self):
        event = request.get_json()
        event_type = event.get('type')

        if event_type == 'deposit':
            result = service.deposit(event['destination'], event['amount'])

            return result, 201
        elif event_type == 'withdraw':
            result, status = service.withdraw(event['origin'], event['amount'])

            if result:
                return result, status
            else:
                return 0, status
        elif event_type == 'transfer':
            result, status = service.transfer(event['origin'],event['destination'], event['amount'])

            if result:
                return result, status
            else:
                return 0, status

        return 'Invalid event type', 400

api.add_resource(ResetAccounts, '/reset')
api.add_resource(AccountBalance, '/balance')
api.add_resource(AccountEvent, '/event')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
