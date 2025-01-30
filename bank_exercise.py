import datetime

class BankAccount:
    def __init__(self, account_holder, initial_balance=0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions = []
        self._record_transaction("Account Created", initial_balance)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        self._record_transaction("Deposit", amount)
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        self._record_transaction("Withdrawal", -amount)
        return self.balance

    def check_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transactions

    def transfer(self, recipient_account, amount):
        if not isinstance(recipient_account, BankAccount):
            raise TypeError("Recipient must be a BankAccount instance")
        
        self.withdraw(amount)  # Deduct from sender
        recipient_account.deposit(amount)  # Add to recipient
        return self.balance

    def _record_transaction(self, transaction_type, amount):
        self.transactions.append({
            "type": transaction_type,
            "amount": amount,
            "balance_after": self.balance,
            "timestamp": datetime.datetime.now()
        })


if __name__ == "__main__":
    account1 = BankAccount("Alice", 1000)
    account2 = BankAccount("Bob", 500)

    account1.deposit(500)
    account1.withdraw(200)
    account1.transfer(account2, 300)

    print("Alice's Balance:", account1.check_balance())
    print("Bob's Balance:", account2.check_balance())

    print("\nAlice's Transaction History:")
    for txn in account1.get_transaction_history():
        print(txn)

    print("\nBob's Transaction History:")
    for txn in account2.get_transaction_history():
        print(txn)
