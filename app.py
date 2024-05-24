import streamlit as st
from PIL import Image
import imageio.v3 as iio
import os
import random
from home import show_home
from about import show_about
from demo import show_demo

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

    </style>
    """,
    unsafe_allow_html=True,
)



def main():
    st.sidebar.image("logo1.jpg", use_column_width=True)
    selected_page = None
    for page_name, page_func in PAGES.items():
        if st.sidebar.button(page_name):
            selected_page = page_name
            page_func()
    if selected_page is None:
        selected_page = 'Home'
        PAGES[selected_page]()  # Show the home page by default

        

if __name__ == "__main__":
    main()
