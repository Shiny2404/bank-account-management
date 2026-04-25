#FEATURES
# bank acount,deposit money,withdraw money,details,update details,delete account

import json
import random
import string
from pathlib import Path


class Bank:
    database = "data.json"
    data = []

    # Load data safely
    try:
        if Path(database).exists():
            with open(database, "r") as fs:
                data = json.load(fs)
        else:
            data = []
    except Exception as err:
        print("Error loading database:", err)
        data = []

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def __accountgenerate(cls):
        chars = (
            random.choices(string.ascii_letters, k=3)
            + random.choices(string.digits, k=3)
            + random.choices("!@#$%^&*", k=1)
        )
        random.shuffle(chars)
        return "".join(chars)

    @staticmethod
    def get_account_no(user):
        return user.get("accountNo") or user.get("accountNo.")

    # ---------------- ACCOUNT CREATION ----------------

    def Createaccount(self):
        try:
            info = {
                "name": input("Enter name: "),
                "age": int(input("Enter age: ")),
                "email": input("Enter email: "),
                "pin": int(input("Enter 4-digit PIN: ")),
                "accountNo": Bank.__accountgenerate(),
                "balance": 0
            }

            if info["age"] < 18 or len(str(info["pin"])) != 4:
                print("Age must be 18+ and PIN must be 4 digits")
                return

            Bank.data.append(info)
            Bank.__update()

            print("\nAccount created successfully")
            for k, v in info.items():
                print(f"{k} : {v}")

        except ValueError:
            print("Invalid input")

    # ---------------- DEPOSIT ----------------

    def depositmoney(self):
        accnumber = input("Enter account number: ")
        pin = int(input("Enter PIN: "))

        userdata = [
            i for i in Bank.data
            if Bank.get_account_no(i) == accnumber and i["pin"] == pin
        ]

        if not userdata:
            print("Account not found")
            return

        amount = int(input("Enter amount to deposit: "))
        if amount <= 0 or amount > 10000:
            print("Deposit must be between 1 and 10000")
            return

        userdata[0]["balance"] += amount
        Bank.__update()
        print("Money deposited successfully")

    # ---------------- WITHDRAW ----------------

    def withdrawmoney(self):
        accnumber = input("Enter account number: ")
        pin = int(input("Enter PIN: "))

        userdata = [
            i for i in Bank.data
            if Bank.get_account_no(i) == accnumber and i["pin"] == pin
        ]

        if not userdata:
            print("Account not found")
            return

        amount = int(input("Enter amount to withdraw: "))
        if amount > userdata[0]["balance"]:
            print("Insufficient balance")
            return

        userdata[0]["balance"] -= amount
        Bank.__update()
        print("Money withdrawn successfully")

    # ---------------- SHOW DETAILS ----------------

    def showdetails(self):
        accnumber = input("Enter account number: ")
        pin = int(input("Enter PIN: "))

        userdata = [
            i for i in Bank.data
            if Bank.get_account_no(i) == accnumber and i["pin"] == pin
        ]

        if not userdata:
            print("Account not found")
            return

        print("\n📄 Account Details")
        for k, v in userdata[0].items():
            print(f"{k} : {v}")

    # ---------------- UPDATE DETAILS ----------------

    def updatedetails(self):
        accnumber = input("Enter account number: ")
        pin = int(input("Enter PIN: "))

        userdata = [
            i for i in Bank.data
            if Bank.get_account_no(i) == accnumber and i["pin"] == pin
        ]

        if not userdata:
            print("Account not found")
            return

        print("Cannot change age, account number or balance")

        name = input("New name (enter to skip): ")
        email = input("New email (enter to skip): ")
        new_pin = input("New PIN (enter to skip): ")

        if name:
            userdata[0]["name"] = name
        if email:
            userdata[0]["email"] = email
        if new_pin:
            if new_pin.isdigit() and len(new_pin) == 4:
                userdata[0]["pin"] = int(new_pin)
            else:
                print("Invalid PIN")
                return

        Bank.__update()
        print("Details updated")

    # ---------------- DELETE ----------------

    def Delete(self):
        accnumber = input("Enter account number: ")
        pin = int(input("Enter PIN: "))

        userdata = [
            i for i in Bank.data
            if Bank.get_account_no(i) == accnumber and i["pin"] == pin
        ]

        if not userdata:
            print("Account not found")
            return

        confirm = input("Press Y to delete account: ")
        if confirm.lower() == "y":
            Bank.data.remove(userdata[0])
            Bank.__update()
            print("Account deleted")
        else:
            print("Deletion cancelled")


# ---------------- MENU ----------------

user = Bank()

print("\n--- BANK MENU ---")
print("1. Create Account")
print("2. Deposit")
print("3. Withdraw")
print("4. Show Details")
print("5. Update Details")
print("6. Delete Account")

choice = int(input("Enter choice: "))

if choice == 1:
    user.Createaccount()
elif choice == 2:
    user.depositmoney()
elif choice == 3:
    user.withdrawmoney()
elif choice == 4:
    user.showdetails()
elif choice == 5:
    user.updatedetails()
elif choice == 6:
    user.Delete()
else:
    print("Invalid choice")


