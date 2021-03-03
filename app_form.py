import streamlit as st
from config import config
import app_db_setup as dbs
import requests

params = config(section="data")

def signup():
  
  applicant_info_1 = {
    # "year": params["year"],
    "name": st.text_input("Name", "")
  }

  city, country = st.beta_columns(2)
  applicant_info_2 = {
    "city": city.text_input("City", ""),
    "country": country.text_input("Country", "")
  }

  applicant_info_3 = {
    "comments": st.text_area("Comments", "")
  }

  applicant_info = {**applicant_info_1, **applicant_info_2, **applicant_info_3}
  return applicant_info


def get_lat_long(info):
  city = info["city"]
  country = info["country"]
  location_query = "city=%s&country=%s" % (city, country)
  url = "https://nominatim.openstreetmap.org/search/?" + location_query + "&format=json"
  response = requests.get(url).json()
  latitude = float(response[0]["lat"])
  longitude = float(response[0]["lon"])
  return latitude, longitude


def save(response):
  # First, add latitude and longitude info
  latitude, longitude = get_lat_long(response)
  response["latitude"] = latitude
  response["longitude"] = longitude
  # Initialize sqlite database
  connection = dbs.init_db()
  #save inputs to db
  dbs.save(connection, response)