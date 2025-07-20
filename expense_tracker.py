import os
import json
from datetime import datetime

DATA_FILE = "expenses.json"

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses):
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format! Use YYYY-MM-DD.")
        return

    try:
        amount = float(input("Enter expense amount: "))
    except ValueError:
        print("Invalid amount!")
        return

    category = input("Enter expense category (e.g., Food, Transport): ").strip()
    description = input("Enter description (optional): ").strip()

    if date not in expenses:
        expenses[date] = []

    expenses[date].append({
        "amount": amount,
        "category": category,
        "description": description
    })

    save_expenses(expenses)
    print("Expense added successfully!")

def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    for date, items in sorted(expenses.items()):
        print(f"\nDate: {date}")
        for i, exp in enumerate(items, start=1):
            print(f"  {i}. Amount: {exp['amount']}, Category: {exp['category']}, Description: {exp['description']}")

def delete_expense(expenses):
    view_expenses(expenses)
    date = input("\nEnter the date of the expense you want to delete (YYYY-MM-DD): ").strip()

    if date not in expenses:
        print("No expenses found for this date.")
        return

    for i, exp in enumerate(expenses[date], start=1):
        print(f"{i}. Amount: {exp['amount']}, Category: {exp['category']}, Description: {exp['description']}")

    try:
        index = int(input("Enter the number of the expense to delete: "))
        if 1 <= index <= len(expenses[date]):
            expenses[date].pop(index - 1)
            if not expenses[date]:
                del expenses[date]
            save_expenses(expenses)
            print("Expense deleted successfully!")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

def view_monthly_summary(expenses):
    monthly_totals = {}

    for date_str, items in expenses.items():
        month = date_str[:7]  # YYYY-MM
        total = sum(exp['amount'] for exp in items)
        monthly_totals[month] = monthly_totals.get(month, 0) + total

    if not monthly_totals:
        print("No expenses to summarize.")
        return

    print("\nMonthly Expense Summary:")
    for month, total in sorted(monthly_totals.items()):
        print(f"{month}: {total:.2f}")

def main():
    expenses = load_expenses()

    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. View Monthly Summary")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            view_monthly_summary(expenses)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select from 1-5.")

if __name__ == "__main__":
    main()
