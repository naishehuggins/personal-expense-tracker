import pandas as pd
import streamlit as st
from datetime import date

from database import initialize_database

from transactions import (
    add_transaction,
    get_transactions,
    delete_transaction
)

from analytics import (
    get_financial_summary,
    get_expenses_by_category,
    get_recent_transactions,
    get_monthly_spending,
    get_monthly_income_expenses,
    get_highest_spending_category
)

from budgets import (
    save_budget,
    get_budgets,
    get_category_spending,
    delete_budget
)

from styles import apply_custom_styles


# -----------------------------------------
# Initialize application
# -----------------------------------------

initialize_database()
apply_custom_styles()


# -----------------------------------------
# Page configuration
# -----------------------------------------

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# -----------------------------------------
# Sidebar
# -----------------------------------------

st.sidebar.markdown(
    """
    # 💰 Expense Tracker

    *Manage your money with clarity.*
    """
)

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Add Transaction",
        "Transactions",
        "Analytics",
        "Budgets"
    ]
)


# =========================================
# DASHBOARD
# =========================================

if page == "Dashboard":

    st.title("Good morning 👋")

    st.write(
        "Here's a quick overview of your financial activity."
    )

    # -----------------------------------------
    # Financial summary
    # -----------------------------------------

    summary = get_financial_summary()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Income",
            f"${summary['income']:,.2f}"
        )

    with col2:
        st.metric(
            "Total Expenses",
            f"${summary['expenses']:,.2f}"
        )

    with col3:

        balance_status = (
            "Positive"
            if summary["balance"] >= 0
            else "Negative"
        )

        st.metric(
            "Current Balance",
            f"${summary['balance']:,.2f}",
            delta=balance_status
        )

    with col4:
        st.metric(
            "Transactions",
            summary["transaction_count"]
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------
    # Spending insight
    # -----------------------------------------

    highest_category = get_highest_spending_category()

    if highest_category:

        st.subheader("💡 Spending Insight")

        st.info(
            f"Your highest spending category is "
            f"**{highest_category['category']}** "
            f"at **${highest_category['amount']:,.2f}**."
        )

    st.divider()

    # -----------------------------------------
    # Charts
    # -----------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.subheader("Spending by Category")

        expenses = get_expenses_by_category()

        if expenses.empty:

            st.info(
                "📊 You don't have any expenses recorded yet. "
                "Add your first expense to start seeing spending insights."
            )

        else:

            category_chart = expenses.set_index(
                "category"
            )

            st.bar_chart(
                category_chart["total"]
            )

    with chart_col2:

        st.subheader("Monthly Spending")

        monthly_spending = get_monthly_spending()

        if monthly_spending.empty:

            st.info(
                "No monthly spending data available yet."
            )

        else:

            monthly_chart = monthly_spending.set_index(
                "month"
            )

            st.line_chart(
                monthly_chart["total"]
            )

    # -----------------------------------------
    # Income vs Expenses
    # -----------------------------------------

    st.subheader("Income vs Expenses Over Time")

    monthly_finances = get_monthly_income_expenses()

    if monthly_finances.empty:

        st.info(
            "Not enough data to display this chart yet."
        )

    else:

        st.line_chart(
            monthly_finances
        )

    st.divider()

    # -----------------------------------------
    # Recent transactions
    # -----------------------------------------

    st.subheader("Recent Transactions")

    recent = get_recent_transactions()

    if recent.empty:

        st.info(
            "📝 No transactions yet. "
            "Add your first transaction to get started."
        )

    else:

        recent_display = recent.copy()

        recent_display["amount"] = recent_display[
            "amount"
        ].apply(
            lambda value: f"${value:,.2f}"
        )

        recent_display.columns = [
            "ID",
            "Type",
            "Amount",
            "Category",
            "Date",
            "Description"
        ]

        st.dataframe(
            recent_display,
            use_container_width=True,
            hide_index=True
        )


# =========================================
# ADD TRANSACTION
# =========================================

elif page == "Add Transaction":

    st.title("Add Transaction")

    st.write(
        "Record your income or expense and keep your finances up to date."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------
    # Transaction form
    # -----------------------------------------

    with st.form("transaction_form"):

        st.subheader("Transaction Details")

        col1, col2 = st.columns(2)

        with col1:

            transaction_type = st.selectbox(
                "Transaction Type",
                ["Expense", "Income"]
            )

        with col2:

            transaction_date = st.date_input(
                "Date",
                value=date.today()
            )

        col3, col4 = st.columns(2)

        with col3:

            amount = st.number_input(
                "Amount",
                min_value=0.01,
                step=0.01,
                format="%.2f"
            )

        with col4:

            if transaction_type == "Expense":

                categories = [
                    "Food",
                    "Transport",
                    "Rent",
                    "Utilities",
                    "Shopping",
                    "Entertainment",
                    "Health",
                    "Education",
                    "Other"
                ]

            else:

                categories = [
                    "Salary",
                    "Freelance",
                    "Business",
                    "Gift",
                    "Other"
                ]

            category = st.selectbox(
                "Category",
                categories
            )

        description = st.text_input(
            "Description",
            placeholder="e.g. Grocery shopping, August salary, taxi ride"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "Save Transaction",
            use_container_width=True
        )

        if submitted:

            if amount <= 0:

                st.error(
                    "Amount must be greater than zero."
                )

            elif not description.strip():

                st.error(
                    "Please enter a description."
                )

            elif not category:

                st.error(
                    "Please select a category."
                )

            else:

                add_transaction(
                    transaction_type=transaction_type,
                    amount=amount,
                    category=category,
                    date=transaction_date.isoformat(),
                    description=description.strip()
                )

                st.success(
                    "✅ Transaction saved successfully!"
                )

                st.write(
                    f"**{transaction_type}:** "
                    f"${amount:,.2f} · "
                    f"**{category}** · "
                    f"{description.strip()}"
                )
# =========================================
# TRANSACTIONS
# =========================================

elif page == "Transactions":

    st.title("Transaction History")

    st.write(
        "View, search, filter, and manage your transactions."
    )

    transactions_df = get_transactions()

    if transactions_df.empty:

        st.info(
            "No transactions found. "
            "Add your first transaction to get started."
        )

    else:

        # Convert date column
        transactions_df["date"] = pd.to_datetime(
            transactions_df["date"]
        ).dt.date

        # -----------------------------------------
        # Filters
        # -----------------------------------------

        st.subheader("Filters")

        col1, col2, col3 = st.columns(3)

        with col1:

            type_filter = st.selectbox(
                "Transaction Type",
                ["All", "Income", "Expense"]
            )

        with col2:

            category_options = sorted(
                transactions_df["category"]
                .unique()
                .tolist()
            )

            category_filter = st.selectbox(
                "Category",
                ["All"] + category_options
            )

        with col3:

            search_term = st.text_input(
                "Search Description",
                placeholder="e.g. groceries"
            )

        # Date filters
        date_col1, date_col2 = st.columns(2)

        with date_col1:

            start_date = st.date_input(
                "Start Date",
                value=transactions_df["date"].min()
            )

        with date_col2:

            end_date = st.date_input(
                "End Date",
                value=transactions_df["date"].max()
            )

        # -----------------------------------------
        # Apply filters
        # -----------------------------------------

        filtered_df = transactions_df.copy()

        if type_filter != "All":

            filtered_df = filtered_df[
                filtered_df["transaction_type"] == type_filter
            ]

        if category_filter != "All":

            filtered_df = filtered_df[
                filtered_df["category"] == category_filter
            ]

        if search_term.strip():

            filtered_df = filtered_df[
                filtered_df["description"].str.contains(
                    search_term.strip(),
                    case=False,
                    na=False
                )
            ]

        filtered_df = filtered_df[
            (filtered_df["date"] >= start_date) &
            (filtered_df["date"] <= end_date)
        ]

        # -----------------------------------------
        # Transaction count
        # -----------------------------------------

        st.write(
            f"Showing **{len(filtered_df)}** transaction(s)"
        )

        # -----------------------------------------
        # Transaction table
        # -----------------------------------------

        display_df = filtered_df[
            [
                "id",
                "transaction_type",
                "amount",
                "category",
                "date",
                "description"
            ]
        ].copy()

        display_df["amount"] = display_df["amount"].apply(
            lambda value: f"${value:,.2f}"
        )

        display_df.columns = [
            "ID",
            "Type",
            "Amount",
            "Category",
            "Date",
            "Description"
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------------------
        # Delete transaction
        # -----------------------------------------

        st.subheader("Delete Transaction")

        transaction_ids = filtered_df["id"].tolist()

        selected_id = st.selectbox(
            "Select a transaction to delete",
            transaction_ids
        )

        delete_button = st.button(
            "🗑️ Delete Selected Transaction",
            type="secondary"
        )

        if delete_button:

            delete_transaction(selected_id)

            st.success(
                f"Transaction #{selected_id} deleted successfully."
            )

            st.rerun()


# =========================================
# ANALYTICS
# =========================================

elif page == "Analytics":

    st.title("📊 Expense Analytics")

    st.write(
        "Understand where your money is going and "
        "how your spending changes over time."
    )

    # -----------------------------------------
    # Highest spending category
    # -----------------------------------------

    highest_category = get_highest_spending_category()

    if highest_category:

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Highest Spending Category",
                highest_category["category"]
            )

        with col2:

            st.metric(
                "Amount Spent",
                f"${highest_category['amount']:,.2f}"
            )

    st.divider()

    # -----------------------------------------
    # Spending by category
    # -----------------------------------------

    st.subheader("Spending by Category")

    expenses = get_expenses_by_category()

    if expenses.empty:

        st.info(
            "No expense data available yet. "
            "Add some expenses first."
        )

    else:

        chart_data = expenses.set_index(
            "category"
        )

        st.bar_chart(
            chart_data["total"]
        )

        st.subheader("Category Breakdown")

        display_expenses = expenses.copy()

        display_expenses["total"] = display_expenses[
            "total"
        ].apply(
            lambda value: f"${value:,.2f}"
        )

        display_expenses.columns = [
            "Category",
            "Total Spent"
        ]

        st.dataframe(
            display_expenses,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # -----------------------------------------
    # Monthly spending
    # -----------------------------------------

    st.subheader("Monthly Spending")

    monthly_spending = get_monthly_spending()

    if monthly_spending.empty:

        st.info(
            "No monthly spending data available yet."
        )

    else:

        monthly_chart = monthly_spending.set_index(
            "month"
        )

        st.line_chart(
            monthly_chart["total"]
        )

        display_monthly = monthly_spending.copy()

        display_monthly["total"] = display_monthly[
            "total"
        ].apply(
            lambda value: f"${value:,.2f}"
        )

        display_monthly.columns = [
            "Month",
            "Total Spent"
        ]

        st.dataframe(
            display_monthly,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # -----------------------------------------
    # Income vs Expenses
    # -----------------------------------------

    st.subheader("Income vs Expenses Over Time")

    monthly_finances = get_monthly_income_expenses()

    if monthly_finances.empty:

        st.info(
            "Not enough data to display income and expenses over time."
        )

    else:

        st.line_chart(
            monthly_finances
        )


# =========================================
# BUDGETS
# =========================================

elif page == "Budgets":

    st.title("Monthly Budgets")

    st.write(
        "Set spending limits and monitor your progress throughout the month."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------
    # Select month
    # -----------------------------------------

    st.subheader("Budget Period")

    selected_month = st.date_input(
        "Select a month",
        value=date.today(),
        format="YYYY-MM-DD"
    )

    month = selected_month.month
    year = selected_month.year

    st.divider()

    # -----------------------------------------
    # Set budget
    # -----------------------------------------

    st.subheader("Set a Budget")

    expense_categories = [
        "Food",
        "Transport",
        "Rent",
        "Utilities",
        "Shopping",
        "Entertainment",
        "Health",
        "Education",
        "Other"
    ]

    with st.form("budget_form"):

        col1, col2 = st.columns(2)

        with col1:

            category = st.selectbox(
                "Expense Category",
                expense_categories
            )

        with col2:

            budget_amount = st.number_input(
                "Monthly Budget",
                min_value=0.01,
                step=10.00,
                format="%.2f"
            )

        submitted = st.form_submit_button(
            "Save Budget",
            use_container_width=True
        )

        if submitted:

            if budget_amount <= 0:

                st.error(
                    "Budget amount must be greater than zero."
                )

            else:

                save_budget(
                    category=category,
                    month=month,
                    year=year,
                    amount=budget_amount
                )

                st.success(
                    f"✅ {category} budget saved successfully."
                )

                st.rerun()

    st.divider()

    # -----------------------------------------
    # Existing budgets
    # -----------------------------------------

    st.subheader(
        f"Your Budgets — {selected_month.strftime('%B %Y')}"
    )

    budgets_df = get_budgets(
        month=month,
        year=year
    )

    if budgets_df.empty:

        st.info(
            "💰 No budgets have been set for this month yet."
        )

    else:

        for _, budget in budgets_df.iterrows():

            category = budget["category"]
            budget_amount = budget["amount"]

            spent = get_category_spending(
                category=category,
                month=month,
                year=year
            )

            remaining = budget_amount - spent

            percentage_used = (
                spent / budget_amount
                if budget_amount > 0
                else 0
            )

            progress = min(
                max(percentage_used, 0),
                1
            )

            st.subheader(category)

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Budget",
                    f"${budget_amount:,.2f}"
                )

            with col2:

                st.metric(
                    "Spent",
                    f"${spent:,.2f}"
                )

            with col3:

                if remaining >= 0:

                    st.metric(
                        "Remaining",
                        f"${remaining:,.2f}"
                    )

                else:

                    st.metric(
                        "Over Budget",
                        f"${abs(remaining):,.2f}"
                    )

            st.progress(progress)

            st.write(
                f"**{percentage_used * 100:.1f}% of budget used**"
            )

            if percentage_used >= 1:

                st.error(
                    f"🔴 You have exceeded your {category} budget."
                )

            elif percentage_used >= 0.8:

                st.warning(
                    f"🟡 You are approaching your {category} budget."
                )

            else:

                st.success(
                    f"🟢 You are within your {category} budget."
                )

            if st.button(
                f"Delete {category} Budget",
                key=f"delete_budget_{budget['id']}"
            ):

                delete_budget(
                    int(budget["id"])
                )

                st.success(
                    f"{category} budget deleted."
                )

                st.rerun()

            st.divider()