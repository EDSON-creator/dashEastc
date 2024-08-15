import streamlit as st
import sqlite3

st.set_page_config(layout="wide")


def check_login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return True
    else:
        return False
    


def login_page():
    st.title("Login Page")

    username = st.text_input("Usernae")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["page"] = "dashboard"
            #st.experimental_rerun()  # Ensure the page rerenders immediately
        else:
            st.error("Invalid username or password")
