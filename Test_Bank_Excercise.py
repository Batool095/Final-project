import pytest
import datetime
from bank_exercise import BankAccount



#fixtures
@pytest.fixture
def setup_account():
    account_holder = "Batool"
    initial_balance = 1000
    account = BankAccount(account_holder, initial_balance)
    return account, initial_balance


@pytest.fixture
def setup_2accounts():
    account1 = BankAccount("Alice", 1000) 
    account2 = BankAccount("Bob", 500)  
    return account1, account2


#Account Creation Tests
#1
def test_create_with_valid_balance(setup_account):
    account, initial_balance = setup_account
    
    assert account.check_balance() == initial_balance
    assert account.account_holder == "Batool"


#2
def test_create_with_negative_balance():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount("Noor", -1000)


#3
def test_account_holder_name(setup_account):
    account, initial_balance = setup_account
    assert account.account_holder == "Batool"


#Deposit Tests
#1
def test_deposit_valid_amount(setup_account):
    account, initial_balance = setup_account

    new_balance = account.deposit(500)

    assert new_balance == 1500



#2
def test_deposit_zero_balance(setup_account):
    account, initial_balance = setup_account

    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(0)

#3
def test_deposit_negative_balance(setup_account):
    account, initial_balance = setup_account

    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(-50)



# Withdrawal Tests
#1
def test_withdraw_valid_amount(setup_account):
    account, initial_balance = setup_account

    new_balance = account.withdraw(500)

    assert new_balance == 500
 

#2
def test_withdraw_more_than_balance(setup_account):
    account, initial_balance = setup_account

    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(1500)


#3
def test_withdraw_zero_balance(setup_account):
    account, initial_balance = setup_account

    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(0)


#3
def test_withdraw_negative_balance(setup_account):
    account, initial_balance = setup_account

    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(-50)


#Transfer Tests
#1
def test_transfer_valid_amount(setup_2accounts):
    account1, account2 = setup_2accounts

    new_balance_sender_Ac1 = account1.transfer(account2, 300)

    assert new_balance_sender_Ac1  == 700
    assert account2.check_balance() == 800
 

#2
def test_transfer_more_than_balance(setup_2accounts):
    account1, account2 = setup_2accounts

    with pytest.raises(ValueError, match="Insufficient funds"):
        account2.transfer(account1, 600)


#3
def test_transfer_to_non_bankaccount(setup_2accounts):
    account1, account2 = setup_2accounts
    non_bank_account = {"name": "Not a BankAccount", "balance": 0}

    with pytest.raises(TypeError, match="Recipient must be a BankAccount instance"):
        account1.transfer(non_bank_account, 600)


#Transaction History Tests
#1
def test_transactions_record(setup_account):
    account, initial_balance = setup_account

    account.deposit(500)
    account.withdraw(200)
    account2 = BankAccount("Test", 500)
    account.transfer(account2, 300)

    transactions = account.get_transaction_history()

    assert len(transactions) == 4
     
    assert transactions[0]["type"] == "Account Created"
    assert transactions[1]["type"] == "Deposit"
    assert transactions[2]["type"] == "Withdrawal"
    assert transactions[3]["type"] == "Withdrawal"

    assert transactions[1]["amount"] == 500
    assert transactions[2]["amount"] == -200
    assert transactions[3]["amount"] == -300

    assert transactions[1]["balance_after"] == 1500
    assert transactions[2]["balance_after"] == 1300
    assert transactions[3]["balance_after"] == 1000



#2
def test_transactions_history_details(setup_account):
    account, initial_balance = setup_account


    account.deposit(500)
    account.withdraw(200)

    transactions = account.get_transaction_history()


    assert transactions[1]["type"] == "Deposit"
    assert transactions[1]["amount"] == 500
    assert transactions[1]["balance_after"] == 1500


    assert transactions[2]["type"] == "Withdrawal"
    assert transactions[2]["amount"] == -200
    assert transactions[2]["balance_after"] == 1300

#3
def test_transaction_timestamps_are_present(setup_account):
    account, initial_balance = setup_account

    account.deposit(500)
    account.withdraw(200)

    transactions = account.get_transaction_history()

    for txn in transactions:
        assert isinstance(txn["timestamp"], datetime.datetime) 
