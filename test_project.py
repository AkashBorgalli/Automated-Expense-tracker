import pytest
from datetime import datetime
from unittest.mock import patch
from project import add_expense, view_summary, generate_chart, update_balance_in_forex_card, update_balance_in_aib_account, save_expense_to_file,convert_euros_to_words,check_balance
import csv
from pathlib import Path


@pytest.fixture
def sample_expense():
    return {
        "Date": "2024-01-01",
        "Category": "groceries",
        "Amount": 50.0,
        "Description": "Grocery shopping",
        "Forex_Account": 100.0,
        "AIB_Account": 200.0,
        "Forex_Balance": 50.0,
        "AIB_Balance": 150.0
    }

@pytest.fixture
def expenses_file(tmp_path):
    return tmp_path / "test_expenses.csv"

def test_save_expense_to_file(expenses_file, sample_expense):
    # Call the function with the sample expense
    result = save_expense_to_file(filename=expenses_file, expense=sample_expense)

    # Check if the result is as expected
    assert result == "saved expense successfully!"

    # Verify the content of the CSV file
    with open(expenses_file, 'r') as file:
        content = file.read()
        assert "Date,Category,Amount,Description,Forex_Account,AIB_Account,Forex_Balance,AIB_Balance" in content
        assert "2024-01-01,groceries,50.0,Grocery shopping,100.0,200.0,50.0,150.0" in content

def test_add_expense(sample_expense, monkeypatch, expenses_file):
    # Monkeypatch the input function to provide predefined inputs
    monkeypatch.setattr('builtins.input', lambda _: "1\n2024-01-01\n50\n" + sample_expense["Category"] + "\n2\n" + sample_expense["Description"])

    # Test whether add_expense adds an expense to the expenses file
    add_expense()

    # Construct the correct file path using the temporary directory
    file_path = "test_expenses.csv"

    # Read the content from the file using csv library
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        content = list(reader)

    # Assert against the content
    assert ["2024-01-01", "groceries", "50.0", "Grocery shopping", "100.0", "200.0", "50.0", "150.0"] == content[1]




@pytest.mark.parametrize("euros, expected_result", [
    (123.45, "One hundred and twenty-three euros and forty-five cents only"),
    (50.0, "Fifty euros only"),
    (0.75, "Zero euros and seventy-five cents only"),
    (1000.0, "One thousand euros only"),
    (999.99, "Nine hundred and ninety-nine euros and ninety-nine cents only"),
    (12.34, "Twelve euros and thirty-four cents only"),
])

def test_convert_euros_to_words(euros, expected_result):
    result = convert_euros_to_words(euros)
    assert result == expected_result



