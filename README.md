# Personal Expense Tracker

A simple personal finance web application built with Python, Streamlit, SQLite, and Pandas.

The application allows users to record income and expenses, monitor their spending, analyze financial activity, and set monthly budgets.

##  Features

### Dashboard
- Total income
- Total expenses
- Current balance
- Transaction count
- Spending by category
- Monthly spending
- Income vs expenses
- Recent transactions

### Transactions
- Add income and expenses
- Search transactions
- Filter by transaction type
- Filter by category
- Filter by date
- Delete transactions

### Analytics
- Highest spending category
- Spending breakdown by category
- Monthly spending trends
- Income vs expenses over time

### Budgets
- Create monthly budgets
- Track spending against budgets
- Calculate remaining budget
- Show budget usage percentage
- Warn users when they are approaching or exceeding a budget

## Technologies Used

- Python
- Streamlit
- SQLite
- Pandas

## Project Structure

```text
expense_tracker/
│
├── app.py
├── database.py
├── transactions.py
├── analytics.py
├── budgets.py
├── styles.py
├── requirements.txt
├── README.md
└── expenses.db

### 1. Clone the repository

```bash
git clone git@github.com:naishehuggins/personal-expense-tracker.git

cd personal-expense-tracker

python -m pip install -r requirements.txt

python -m streamlit run app.py


### 2. In your VS Code terminal

You run **only the command itself**, without `bash`.

For example:

```powershell
python -m pip install -r requirements.txt
or
python -m streamlit run app.py
