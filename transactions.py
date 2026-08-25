import pandas as pd

from database import get_connection


def add_transaction(
    transaction_type,
    amount,
    category,
    date,
    description
):
    """Save a new transaction to the database."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            transaction_type,
            amount,
            category,
            date,
            description
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            transaction_type,
            amount,
            category,
            date,
            description
        )
    )

    connection.commit()
    connection.close()


def get_transactions():
    """Return all transactions as a Pandas DataFrame."""

    connection = get_connection()

    query = """
        SELECT
            id,
            transaction_type,
            amount,
            category,
            date,
            description,
            created_at
        FROM transactions
        ORDER BY date DESC, id DESC
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe


def delete_transaction(transaction_id):
    """Delete a transaction using its ID."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    connection.commit()
    connection.close()