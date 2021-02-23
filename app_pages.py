import streamlit as st
import streamlit.components.v1 as components
import app_info
import app_form

def make_pages():
  # Register pages
    pages = {
        "About": page_about,
        "Where do magicians come from?": page_info,
        "Become a magician!": page_form
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
            Welcome to the Magical World of <code>streamlit</code>!
        </h1>
        <h3 style='text-align: center; margin-bottom: 2em'>👷‍♀️👩‍💻👩‍👧‍👧</h3>
        <p>
            This is the place where you can sign up to become a magnificent maestro magician! 🎩
        </p>
        <p>
            (It is <s>actually</s> also a small test app with PostgreSQL for purposes of testing deployment 🪂.)
        </p>
        """
    components.html(html_string, height=600, scrolling=True)

def page_info():
    st.title("Locations of magicians around the world")
    magicians_df, shows_df = app_info.load_data()
    app_info.draw_map(magicians_df)
    app_info.list_shows_from_db()
    app_info.list_shows_from_df(magicians_df, shows_df)


def page_form():
    st.image("assets/images/magician.jpg", width=200)
    st.header("Apply to become a magician! 🎈")
    applicant_info = app_form.signup()
    if st.button("Submit"):
        app_form.save(applicant_info)