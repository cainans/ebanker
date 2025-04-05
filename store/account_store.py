class AccountStore:
    def __init__(self):
        self.accounts = {}

    def reset(self):
        self.accounts.clear()

    def get(self, account_id):
        return self.accounts.get(account_id)

    def save(self, account):
        self.accounts[account['id']] = account