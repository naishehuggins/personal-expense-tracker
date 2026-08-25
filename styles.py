import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styles to the application."""

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #f7f8fa;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
        }

        h1 {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
        }

        h2 {
            font-size: 1.5rem !important;
            font-weight: 650 !important;
        }

        h3 {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
        }

        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.85rem;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.6rem;
            font-weight: 700;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            min-height: 42px;
        }

        div[data-baseweb="input"] {
            border-radius: 10px;
        }

        div[data-baseweb="select"] {
            border-radius: 10px;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }

        div[data-testid="stAlert"] {
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )