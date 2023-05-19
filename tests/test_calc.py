# A demo test for practice
# Not part of the api testing.

import pytest
from app.calculations import add, BankAccount, InsufficientBalance


def test_add():
    assert add(2, 3) == 5


def test_insufficient_balance():
    bank_balance = BankAccount(10)
    with pytest.raises(InsufficientBalance):
        bank_balance.withdraw(50)
