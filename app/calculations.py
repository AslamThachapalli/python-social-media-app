# This is a demo file for practicing testing with python.
# Not a part of the api.

def add(num1: int, num2: int):
    return num1 + num2


def subtract(num1: int, num2: int):
    return num1-num2


class InsufficientBalance(Exception):
    pass


class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientBalance("You have insufficient balance")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
