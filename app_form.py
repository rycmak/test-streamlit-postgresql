import streamlit as st
import app_db_setup as dbs
import json

with open('config.json') as config_file:
  conf_data = json.load(config_file)

def signup():
  applicant_info = {
    "year": conf_data["year"],
    "name": st.text_input("Name", ""),
    "comment": st.text_area("Comments", "")
  }
  return applicant_info

def save(response):
    # Initialize sqlite database
    connection = dbs.init_db()
    #save inputs to db
    dbs.save(connection, response)