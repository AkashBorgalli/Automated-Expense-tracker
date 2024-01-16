from datetime import datetime
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import pandas as pd
import inflect

EXPENSES_FILE = "expenses.csv"

categorywise_expenses = {}

def main():
    """
    Description: Main function to run the Automated Expense Tracker.
    :raise Exception: Raised if an error occurs during the process.
    :return: None
    :rtype: None
    """
    print("Welcome to the Automated Expense Tracker!")
    while True:
        try:
            print("\nPlease select one of these options:")
            print("1. Add Expense")
            print("2. View Summary")
            print("3. Add Money")
            print("4. Check Balance")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                add_expense()
                print("Expense added successfully!")
            elif choice == "2":
                total_expenses, category_summary = view_summary()
                print("\nExpense Summary:")
                print(f"Total Expenses: €{total_expenses:.2f}")
                result = convert_euros_to_words(total_expenses)
                print(result)
                print("\nCategory-wise Expense Summary:")
                for k, v in category_summary.items():
                    print(k, '-->', v, "euros")
                    categorywise_expenses[k] = v
                generate_chart(categorywise_expenses)
            elif choice == "3":
                while True:
                    print("\nPlease select one of these options:")
                    print("1. Add Money to Forex Card")
                    print("2. Add Money to AIB Account")
                    print("3. Exit")
                    add_money_choice = input("Enter your choice: ")

                    if add_money_choice == "1":
                        result = update_balance_in_forex_card()
                        print(result)
                    elif add_money_choice == "2":
                        result = update_balance_in_aib_account()
                        print(result)
                    elif add_money_choice == "3":
                        print("Exiting from Add Money options")
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == "4":
                    forex_balance, aib_balance = check_balance()
                    if type(forex_balance) == str:
                        print('Error occured!')
                    elif type(forex_balance) == None:
                        print("No expenses recorded. Balances not available.")
                        print('Please use option 1 to add expense!')
                    else:
                        print("Current Balances:")
                        print(f'Balance in Forex Account is : €{forex_balance}')
                        print(f'Balance in Forex Account in words : {convert_euros_to_words(forex_balance)}')
                        print(f'Balance in AIB Account is : €{aib_balance}')
                        print(f'Balance in AIB Account in words : {convert_euros_to_words(aib_balance)}')

            elif choice == "5":
                print("Exiting the Expense Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred in main function: {e}")

def check_balance():
    """
    Description: Checks the current balance in the Forex Card and AIB Account based on the last recorded expense.

    :raise Exception: Raised if an error occurs during the process.
    :return: A tuple containing the current Forex Card balance and AIB Account balance.
             If the expenses file is empty, returns (None, None).
    :rtype: tuple
    """
    try:
        df = pd.read_csv(EXPENSES_FILE)
        if df.empty:
            # If expenses file is empty, return (None, None)
            return None, None
        else:
            # Retrieve the last recorded expense
            last_record = df.tail(1)
            forex_balance = last_record['Forex_Balance'].values[0]
            aib_balance = last_record['AIB_Balance'].values[0]
            return forex_balance, aib_balance
    except Exception as e:
        # Handle and print any exceptions that may occur
        error_message = f"An error occurred in check balance function: {e}"
        print(error_message)
        return error_message, None



def add_expense():
    """
    Description: Adds an expense to the expenses file.
    :raise Exception: Raised if an error occurs during the process.
    :return: The added expense.
    :rtype: dict
    """
    try:
        try:
            df = pd.read_csv(EXPENSES_FILE)
        except FileNotFoundError:
            # If the file is not found, create it
            df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description", "Forex_Account", "AIB_Account", "Forex_Balance", "AIB_Balance"])
            df.to_csv(EXPENSES_FILE, index=False)

            # Ask for initial balances
            while True:
                try:
                    forex_balance = float(input("Enter the initial Forex balance (greater than 0): "))
                    aib_balance = float(input("Enter the initial AIB balance (greater than 0): "))

                    if forex_balance > 0 and aib_balance > 0:
                        break
                    else:
                        print("Balances must be greater than 0. Please try again.")
                except ValueError:
                    print("Invalid input. Balances must be numeric. Please try again.")

            # Create the first record with initial balances
            first_expense = {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Category": "initial_balance",
                "Amount": 0.00,
                "Description": "Initial Balances",
                "Forex_Account": forex_balance,
                "AIB_Account": aib_balance,
                "Forex_Balance": forex_balance,
                "AIB_Balance": aib_balance
            }

            save_expense_to_file(EXPENSES_FILE, first_expense)
            print("Initial balances added successfully.")

            return first_expense

        # Continue with the rest of the logic if the file exists
        last_record = df.tail(1)
        date_str = input("Enter the date (YYYY-MM-DD): ")
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        amount = float(input("Enter the amount spent: "))
        # Define valid categories
        valid_categories = ["groceries", "pub", "restaurant", "movie-tickets", "purchased-beers", "travelling", "others"]

        # Ask for category until a valid one is provided
        while True:
            print('Please choose from this options', ", ".join(valid_categories))
            category = input("Enter the expense category: ").lower()
            if category in valid_categories:
                break
            else:
                print("Invalid category. Please choose from: ", valid_categories)

        description = input("Enter a brief description: ")

        while True:
            account_type = int(input("Press 1 if you used Forex \n Press 2 if you used AIB account\n"))
            if account_type == 1:
                forex_balance = last_record['Forex_Balance'].values[0]
                update_forex_balance = forex_balance - amount
                expense = {"Date": date, "Category": category, "Amount": amount, "Description": description,
                            "Forex_Account": update_forex_balance, "AIB_Account": last_record['AIB_Account'].values[0],
                            "Forex_Balance": update_forex_balance, "AIB_Balance": last_record['AIB_Balance'].values[0]}
                save_expense_to_file(EXPENSES_FILE,expense)
                break
            elif account_type == 2:
                aib_balance = last_record['AIB_Balance'].values[0]
                update_aib_balance = aib_balance - amount
                expense = {"Date": date, "Category": category, "Amount": amount, "Description": description,
                            "Forex_Account": last_record['Forex_Account'].values[0], "AIB_Account": update_aib_balance,
                            "Forex_Balance": last_record['Forex_Balance'].values[0], "AIB_Balance": update_aib_balance}
                save_expense_to_file(EXPENSES_FILE,expense)
                break
            else:
                print("Invalid Option!")

        return expense

    except Exception as e:
        print(f"An error occurred in add_expense_function: {e}")
        return None


def convert_euros_to_words(euros):
    """
    Description: Converts euros to words using inflect library.
    :raise Exception: Raised if an error occurs during the process.
    :param euros: The amount in euros.
    :type euros: float
    :return: The amount in words.
    :rtype: str
    """
    try:
        # Create an inflect engine
        p = inflect.engine()

        # Extract the whole and fractional parts
        whole_part, fractional_part = str(euros).split('.')

        # Convert the whole part to words
        whole_words = p.number_to_words(int(whole_part))

        # Convert the fractional part to words
        fractional_words = p.number_to_words(int(fractional_part))

        # Combine the words for the whole and fractional parts
        if fractional_part != '0':
            result = f"{whole_words} euros and {fractional_words} cents only"
        else:
            result = f"{whole_words} euros only"

        return result.capitalize()

    except Exception as e:
        print(f"An error occurred in convert euros to words function: {e}")
        return None

def view_summary():
    """
    Description: Displays the expense summary based on user-defined filters.
    :raise Exception: Raised if an error occurs during the process.
    :return: Total expenses and category-wise expense summary.
    :rtype: tuple
    """
    try:
        df = pd.read_csv(EXPENSES_FILE)

        filter_choice = input("How would you like to filter the data? (date/category): ").lower()

        if filter_choice == 'date':
            start_date = input("Enter the start date (DD-MM-YYYY): ")
            end_date = input("Enter the end date (DD-MM-YYYY, leave blank for the last record): ")

            if start_date and end_date:
                filtered_df = df.loc[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
            elif start_date:
                filtered_df = df.loc[df['Date'] >= start_date]
            elif end_date:
                filtered_df = df.loc[df['Date'] <= end_date]
            else:
                filtered_df = df.copy()

        elif filter_choice == 'category':
            category_filter = input("Enter the category to filter: ")
            filtered_df = df.loc[(df['Category'] == category_filter) & (df['Category'] != 'add_money') & (df['Category'] != 'initial_balance')]

        else:
            print("Invalid filter choice. Please choose 'date' or 'category'.")
            return None, None

        if filtered_df.empty:
            return f"No matching expenses found."

        total_expenses = filtered_df.loc[filtered_df['Category'] != 'add_money', 'Amount'].sum()
        filtered_df = df.loc[(df['Category'] != 'add_money')& (df['Category'] != 'initial_balance')]
        category_summary = filtered_df.groupby('Category')['Amount'].sum()

        return total_expenses, category_summary

    except Exception as e:
        print(f"An error occurred in view sumary_function: {e}")
        return None, None

def generate_chart(category_expenses, save_path='expense_chart.png'):
    """
    Description: Generates a pie chart based on category-wise expenses.
    :param category_expenses: A dictionary containing category-wise expenses.
    :type category_expenses: dict
    :param save_path: The path to save the chart image.
    :type save_path: str
    :return: None
    :rtype: None
    """
    try:
        labels = list(category_expenses.keys())
        values = list(category_expenses.values())
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Expense Distribution by Category')
        plt.savefig(save_path)
        plt.close()
        print(f"Chart saved as {save_path}")
    except Exception as e:
        print(f"An error occurred in generate_chart_function: {e}")


def update_balance_in_forex_card():
    """
    Description: Updates the balance in the Forex Card account.
    :raise Exception: Raised if an error occurs during the process.
    :return: A success message or None in case of an error.
    :rtype: str or None
    """
    try:
        df = pd.read_csv(EXPENSES_FILE)

        # Get user input for date and amount
        date_str = input("Enter the date for adding money to Forex Card (YYYY-MM-DD): ")
        amount = float(input("Enter the amount to add to Forex Card: "))

        # Convert date string to datetime format
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")

        # Get the last record to calculate updated balance
        last_record = df.tail(1)
        forex_balance = last_record['Forex_Balance'].values[0]
        update_forex_balance = forex_balance + amount

        new_record = {
            "Date": date,
            "Category": "add_money",
            "Amount": amount,
            "Description": "Added money to Forex Card",
            "Forex_Account": update_forex_balance,
            "AIB_Account": last_record['AIB_Account'].values[0],
            "Forex_Balance": update_forex_balance,
            "AIB_Balance": last_record['AIB_Balance'].values[0]
        }

        save_expense_to_file(EXPENSES_FILE,new_record)
        return f"Money added of amount: {amount} to Forex Card successfully!"

    except Exception as e:
        print(f"An error occurred in update_balance_in_forex_card: {e}")
        return None

def update_balance_in_aib_account():
    """
    Description: Updates the balance in the AIB Account.
    :raise Exception: Raised if an error occurs during the process.
    :return: A success message or None in case of an error.
    :rtype: str or None
    """
    try:
        df = pd.read_csv(EXPENSES_FILE)

        # Get user input for date and amount
        date_str = input("Enter the date for adding money to AIB Account (YYYY-MM-DD): ")
        amount = float(input("Enter the amount to add to AIB Account: "))

        # Convert date string to datetime format
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")

        # Get the last record to calculate updated balance
        last_record = df.tail(1)
        aib_balance = last_record['AIB_Balance'].values[0]
        update_aib_balance = aib_balance + amount

        new_record = {
            "Date": date,
            "Category": "add_money",
            "Amount": amount,
            "Description": "Added money to AIB Account",
            "Forex_Account": last_record['Forex_Account'].values[0],
            "AIB_Account": update_aib_balance,
            "Forex_Balance": last_record['Forex_Balance'].values[0],
            "AIB_Balance": update_aib_balance
        }

        save_expense_to_file(EXPENSES_FILE,new_record)
        return f"Money added of amount: {amount} to AIB Account successfully!"

    except Exception as e:
        print(f"An error occurred in update_balance_in_aib_account: {e}")
        return None

def save_expense_to_file(filename,expense):
    """
    Description: Saves an expense to the expenses file.
    :param filename: name of the csv to save the expense.
    :type filename: str
    :param expense: The expense to be saved.
    :type expense: dict
    :raise Exception: Raised if an error occurs during the process.
    :return: A success message or None in case of an error.
    :rtype: str or None
    """
    try:
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['Date', 'Category', 'Amount', 'Description','Forex_Account','AIB_Account','Forex_Balance','AIB_Balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow(expense)
        return "saved expense successfully!"
    except Exception as e:
        print(f"An error occurred in save_expense_function: {e}")
        return None

if __name__ == "__main__":
    main()
