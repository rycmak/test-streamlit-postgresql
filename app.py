import streamlit as st
from app_pages import make_pages

st.set_page_config(page_title="Test App")

def main():
    make_pages()

if __name__ == "__main__":
    main()