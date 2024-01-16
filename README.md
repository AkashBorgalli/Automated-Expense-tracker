# Automated Expense Tracker

#### Video Demo: [Demo Video](https://youtu.be/pOulFxgl3TA)

#### Description:
The Automated Expense Tracker is a Python program designed to simplify the process of tracking and managing expenses. The program allows users to input their daily expenses, categorize them, and generate a summary report. It also features graphical visualizations for expense distribution, the ability to add money to Forex or AIB accounts, and checking balances in both accounts.

## Features:
1. **Expense Input:**
    - Users can input their daily expenses, including the amount spent and a brief description.
    - The program prompts the user for the date and category of the expense.

2. **Expense Categorization:**
    - Expenses can be categorized into predefined categories (e.g., groceries, utilities, entertainment).
    - Users can customize categories and add new ones as needed.

3. **Expense Summary:**
    - The program provides a summary of total expenses for each category.
    - Users can view the total expenses for a specific day, week, or month.

4. **Graphical Visualization:**
    - Generate graphical visualizations (bar charts, pie charts) to represent expense distribution.
    - Provide visual insights into spending patterns over time.

5. **Add Money in Forex or AIB Account:**
    - It can also load money in Forex or AIB account (in a csv file)

6. **Check Balances in both Accounts:**
   -  It can also display the balances of both accounts.

## Project Structure:
```bash
project
├── expense_chart.png       # A visual representation of project expenses
├── expenses.csv            # CSV file containing project expenses data
├── test_expenses.csv       # CSV file for testing purposes with sample expenses data
├── requirements.txt        # List of Python packages required for the project
├── project.py              # Main Python script for the project
├── test_project.py         # Test script for testing the functionality of project.py
└── README.md               # Project documentation and information
```

## Installation

1. Install the required libraries by running:

```bash
pip install -r requirements.txt
```


2. Run the script

```bash
python project.py
```

3. Usage
Follow the on-screen instructions to navigate through the options:

- **Add Expense (Option 1)**: Add your expenses with details.
- **View Summary (Option 2)**: View your expense summary and category-wise distribution.
- **Add Money (Option 3)**: Add money to either the Forex Card or AIB Account.
- **Check Balance (Option 4)**: Check the current balances in both the Forex Card and AIB Account.
- **Exit (Option 5)**: Exit the Expense Tracker.


Notes
- The script uses a CSV file (expenses.csv) to store expense records.
- Initial balances are required if no expenses are recorded yet.
- Make sure to input valid data as per the prompts.


Enjoy tracking your expenses!