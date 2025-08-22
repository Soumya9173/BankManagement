import json
import random
import string
from pathlib import Path


class Bank:
    database = Path("data.json")

    def __init__(self):
        self.data = self._load_data()

    def _load_data(self):
        """Load database from file, return empty list if not exists."""
        if self.database.exists():
            try:
                with open(self.database, "r") as fs:
                    return json.load(fs)
            except Exception as e:
                print(f"Error reading DB: {e}")
                return []
        else:
            return []

    def _update(self):
        """Update the database file."""
        with open(self.database, "w") as fs:
            json.dump(self.data, fs, indent=4)

    def _generate_account(self):
        """Generate random account number (letters + digits only)."""
        chars = random.choices(string.ascii_letters + string.digits, k=8)
        return "".join(chars)

    def _find_user(self, acc, pin):
        """Find user record by acc number and pin."""
        acc = acc.strip()
        try:
            pin = int(pin)
        except ValueError:
            return None
        for user in self.data:
            if user.get("accountNo").strip() == acc and int(user.get("pin")) == pin:
                return user
        return None

    def create_account(self, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return False, "You must be 18+ and PIN must be 4 digits."

        info = {
            "name": name,
            "age": int(age),
            "email": email,
            "pin": int(pin),
            "accountNo": self._generate_account(),
            "balance": 0,
        }
        self.data.append(info)
        self._update()
        return True, info

    def deposit(self, acc, pin, amount):
        user = self._find_user(acc, pin)
        if not user:
            return False, "Invalid account or PIN"
        if amount <= 0 or amount > 10000:
            return False, "Amount must be between 1 and 10000"

        user["balance"] = int(user.get("balance", 0)) + int(amount)
        self._update()
        return True, f"Deposited {amount}. New balance: {user['balance']}"

    def withdraw(self, acc, pin, amount):
        user = self._find_user(acc, pin)
        if not user:
            return False, "Invalid account or PIN"
        if amount <= 0 or user["balance"] < amount:
            return False, "Insufficient balance"
        user["balance"] -= int(amount)
        self._update()
        return True, f"Withdrew {amount}. New balance: {user['balance']}"

    def show_details(self, acc, pin):
        user = self._find_user(acc, pin)
        if not user:
            return False, "Invalid account or PIN"
        return True, user

    def update_details(self, acc, pin, name=None, email=None, new_pin=None):
        user = self._find_user(acc, pin)
        if not user:
            return False, "Invalid account or PIN"

        if name:
            user["name"] = name
        if email:
            user["email"] = email
        if new_pin:
            if len(str(new_pin)) != 4:
                return False, "PIN must be 4 digits"
            user["pin"] = int(new_pin)

        self._update()
        return True, user

    def delete_account(self, acc, pin):
        user = self._find_user(acc, pin)
        if not user:
            return False, "Invalid account or PIN"
        self.data.remove(user)
        self._update()
        return True, "Account deleted"
