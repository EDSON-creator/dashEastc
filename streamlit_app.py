import streamlit as st


st.set_page_config(layout="wide")
# Import page functions
from login import login_page
from dash import home_page

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"

    if st.session_state["logged_in"]:
        home_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
