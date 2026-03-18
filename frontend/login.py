import os

import streamlit as st


def _get_username() -> str:

    if "DASHBOARD_USERNAME" in st.secrets:
        return str(st.secrets["DASHBOARD_USERNAME"])

    return os.getenv("DASHBOARD_USERNAME", "admin")


def _get_password() -> str:

    if "DASHBOARD_PASSWORD" in st.secrets:
        return str(st.secrets["DASHBOARD_PASSWORD"])

    return os.getenv("DASHBOARD_PASSWORD", "admin123")


def login():

    st.title("AI Cloud Optimizer Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):

        if user == _get_username() and pwd == _get_password():
            st.session_state["login"] = True
        else:
            st.error("Wrong login")


def check_login():

    if "login" not in st.session_state:
        st.session_state["login"] = False

    if not st.session_state["login"]:
        login()
        return False

    return True