from collections import OrderedDict

class AccountService(object):
    def __init__(self, store):
        self.store = store

    def reset(self):
        self.store.reset()

    def get_balance(self, account_id):
        acc = self.store.get(account_id)

        return acc['balance'] if acc else None

    def deposit(self, destination, amount):
        acc = self.store.get(destination)

        if acc:
            acc['balance'] += amount
        else:
            acc = {'id': destination, 'balance': amount}
        self.store.save(acc)

        return {'destination': acc}

    def withdraw(self, origin, amount):
        acc = self.store.get(origin)

        if not acc:
            return None, 404
        if acc['balance'] < amount:
            return {'message': 'Insufficient funds'}, 400

        acc['balance'] -= amount
        self.store.save(acc)

        return {'origin': acc}, 201

    def transfer(self, origin_id, destination_id, amount):
        origin = self.store.get(origin_id)
        destination = self.store.get(destination_id)

        if not origin:
            return None, 404
        elif origin['balance'] < amount:
            return {'message': 'Insufficient funds'}, 400

        origin['balance'] -= amount

        if destination:
            destination['balance'] += amount
        else:
            destination = {'id': destination_id, 'balance': amount}

        self.store.save(origin)
        self.store.save(destination)

        return {'origin': origin, 'destination': destination}, 201