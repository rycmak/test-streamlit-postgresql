import streamlit as st
import streamlit.components.v1 as components
import app_graphs
import app_form

def make_pages():
  # Register pages
    pages = {
        "About": page_about,
        "Graphs": page_graphs,
        "Form": page_form
    }

    st.sidebar.title("Navigation")
    # Radio buttons for selecting page
    page = st.sidebar.radio("Go to", tuple(pages.keys()))
    # Display the selected page
    pages[page]()

# Intro page
def page_about():
    html_string = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap');
        html {{
            font-family: IBM Plex Sans, Arial, sans-serif;
            font-size: 100%;
        }}
        body {{
            font-size: 1em;
            font-family: inherit;
            line-height: 1.6;
        }}
        </style>

        <h1 style='font-size: 1.5em; text-align: center'>
            Welcome to my magnificent streamlit test app!
        </h1>
        <h3 style='text-align: center; margin-bottom: 2em'>👷‍♀️👩‍💻👩‍👧‍👧</h3>
        <p>
            This is a small test app with PostgreSQL for purposes of testing deployment 🪂.
        </p>
        """
    components.html(html_string, height=600, scrolling=True)

def page_graphs():
    st.title("Informative graphs")
    app_graphs.draw_map()

def page_form():
    st.header("Apply to become a magician! 🎈")
    applicant_info = app_form.signup()
    if st.button("Submit"):
        print("applicant info: ", applicant_info)
        app_form.save(applicant_info)