import pandas as pd

from database import get_connection


def save_budget(category, month, year, amount):
    """Create or update a monthly budget for a category."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO budgets (
            category,
            month,
            year,
            amount
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(category, month, year)
        DO UPDATE SET amount = excluded.amount
        """,
        (category, month, year, amount)
    )

    connection.commit()
    connection.close()


def get_budgets(month, year):
    """Return budgets for a specific month."""

    connection = get_connection()

    query = """
        SELECT
            id,
            category,
            month,
            year,
            amount
        FROM budgets
        WHERE month = ?
        AND year = ?
        ORDER BY category
    """

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=(month, year)
    )

    connection.close()

    return dataframe


def get_category_spending(category, month, year):
    """Return total spending for a category in a specific month."""

    connection = get_connection()

    query = """
        SELECT
            COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE transaction_type = 'Expense'
        AND category = ?
        AND strftime('%m', date) = ?
        AND strftime('%Y', date) = ?
    """

    result = connection.execute(
        query,
        (
            category,
            f"{month:02d}",
            str(year)
        )
    ).fetchone()

    connection.close()

    return result[0]


def delete_budget(budget_id):
    """Delete a budget."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM budgets WHERE id = ?",
        (budget_id,)
    )

    connection.commit()
    connection.close()