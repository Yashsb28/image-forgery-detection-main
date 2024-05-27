import streamlit as st
from PIL import Image
import imageio.v3 as iio
import os
import random
from home import show_home
from about import show_about
from demo import show_demo
from database import init_db, add_user, get_user

st.set_page_config(page_title="AI-Forgery Guard", layout="wide")

PAGES = {
    "Home": show_home,
    "About": show_about,
    "Demo": show_demo
}

st.markdown(
    """
    <style>
    .st-emotion-cache-16txtl3 {
      padding: 3rem 1.5rem;
    }

    .st-emotion-cache-hc3laj {
      display: inline-flex;
      -webkit-box-align: center;
      align-items: center;
      -webkit-box-pack: center;
      justify-content: center;
      font-weight: 400;
      padding: 0.25rem 0.75rem;
      border-radius: 0.5rem;
      min-height: 38.4px;
      margin: 0px;
      line-height: 1.6;
      color: inherit;
      width: 100%;
      user-select: none;
      background-color: rgb(43, 44, 54);
      border: 1px solid rgba(250, 250, 250, 0.2);
    }

    .st-emotion-cache-z5fcl4 {
      width: 75%;
      padding: 3rem 1rem 10rem;
      min-width: auto;
      max-width: initial;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

def signup():
    st.title("Welcome to AI-FORGERY GUARD")
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    def password_valid(password):
        if len(password) < 5:
            return False
        if not any(char.isdigit() for char in password):
            return False
        return True

    if st.button("Sign Up"):
        if get_user(username):
            st.warning("Username already exists. Please choose another one.")
        elif password != confirm_password:
            st.warning("Passwords do not match.")
        elif not password_valid(password):
            st.warning("Password must be at least 5 characters long and contain at least one number.")
        else:
            add_user(username, password)
            st.success("You have successfully signed up!")
            st.info("Please log in with your new credentials.")
            st.session_state.page = "Login"
            st.experimental_rerun()

def login():
    st.title("Welcome to AI-FORGERY GUARD")
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = get_user(username)
        if user and user[1] == password:
            st.success("You have successfully logged in!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "Home"
            st.experimental_rerun()
        else:
            st.warning("Incorrect username or password.")

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "page" not in st.session_state:
        st.session_state.page = "Login"
    
    init_db()  # Initialize the database

    if st.session_state.logged_in:
        st.sidebar.image("logo1.jpg", use_column_width=True)
        selected_page = None
        for page_name, page_func in PAGES.items():
            if st.sidebar.button(page_name):
                st.session_state.page = page_name
                selected_page = page_name
                st.experimental_rerun()
        
        if selected_page is None:
            selected_page = st.session_state.page
        
        PAGES[selected_page]()
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "Login"
            st.experimental_rerun()
    else:
        if st.session_state.page == "Login":
            login()
        elif st.session_state.page == "Signup":
            signup()
        
        if st.session_state.page == "Login":
            if st.button("Go to Signup"):
                st.session_state.page = "Signup"
                st.experimental_rerun()
        elif st.session_state.page == "Signup":
            if st.button("Go to Login"):
                st.session_state.page = "Login"
                st.experimental_rerun()

if __name__ == "__main__":
    main()
