import streamlit as st
import streamlit.components.v1 as components
import app_info
import app_form
import app_matches
import SessionState
from config import config

session_state = SessionState.get(admin=False, admin_pw='')

def make_pages():
  # Register pages
    pages = {
        "About": page_about,
        "Where do magicians come from?": page_info,
        "Become a magician!": page_form
    }

    st.sidebar.title("Navigation")
    admin_btn = st.sidebar.empty()
    # Radio buttons for selecting page
    if not session_state.admin:
        page = st.sidebar.radio("Go to", tuple(pages.keys()))
        admin_btn = st.sidebar.button("Admin")
    if admin_btn:
        session_state.admin = True
        page_admin()
    else:
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


def page_admin():
    admin_pw = config(filename='secrets.toml', section='admin')['pw']
    if session_state.admin_pw == admin_pw:
        app_matches.match_buddies()
        session_state.admin = False
    else:
        pw = st.text_input("Admin password:", "")
        session_state.admin_pw = pw
        if session_state.admin_pw == admin_pw:
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
        elif st.button("Return to home page"):
            session_state.admin = False
            raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
