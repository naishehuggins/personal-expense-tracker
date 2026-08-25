import pandas as pd

from database import get_connection


def get_financial_summary():
    """Return total income, expenses, balance, and transaction count."""

    connection = get_connection()

    query = """
        SELECT
            transaction_type,
            SUM(amount) AS total
        FROM transactions
        GROUP BY transaction_type
    """

    dataframe = pd.read_sql_query(query, connection)

    total_income = 0
    total_expenses = 0

    for _, row in dataframe.iterrows():

        if row["transaction_type"] == "Income":
            total_income = row["total"]

        elif row["transaction_type"] == "Expense":
            total_expenses = row["total"]

    transaction_count = connection.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    connection.close()

    balance = total_income - total_expenses

    return {
        "income": total_income,
        "expenses": total_expenses,
        "balance": balance,
        "transaction_count": transaction_count
    }


def get_expenses_by_category():
    """Return total expenses grouped by category."""

    connection = get_connection()

    query = """
        SELECT
            category,
            SUM(amount) AS total
        FROM transactions
        WHERE transaction_type = 'Expense'
        GROUP BY category
        ORDER BY total DESC
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe


def get_recent_transactions(limit=5):
    """Return the most recent transactions."""

    connection = get_connection()

    query = """
        SELECT
            id,
            transaction_type,
            amount,
            category,
            date,
            description
        FROM transactions
        ORDER BY date DESC, id DESC
        LIMIT ?
    """

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=(limit,)
    )

    connection.close()

    return dataframe


def get_monthly_spending():
    """Return total expenses grouped by month."""

    connection = get_connection()

    query = """
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(amount) AS total
        FROM transactions
        WHERE transaction_type = 'Expense'
        GROUP BY month
        ORDER BY month
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe


def get_monthly_income_expenses():
    """Return monthly income and expenses."""

    connection = get_connection()

    query = """
        SELECT
            strftime('%Y-%m', date) AS month,
            transaction_type,
            SUM(amount) AS total
        FROM transactions
        GROUP BY month, transaction_type
        ORDER BY month
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    if dataframe.empty:
        return dataframe

    # Convert rows into columns for easier charting
    dataframe = dataframe.pivot(
        index="month",
        columns="transaction_type",
        values="total"
    ).fillna(0)

    # Make sure both columns exist
    if "Income" not in dataframe.columns:
        dataframe["Income"] = 0

    if "Expense" not in dataframe.columns:
        dataframe["Expense"] = 0

    return dataframe[["Income", "Expense"]]


def get_highest_spending_category():
    """Return the category with the highest total spending."""

    connection = get_connection()

    query = """
        SELECT
            category,
            SUM(amount) AS total
        FROM transactions
        WHERE transaction_type = 'Expense'
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """

    result = connection.execute(query).fetchone()

    connection.close()

    if result is None:
        return None

    return {
        "category": result[0],
        "amount": result[1]
    }