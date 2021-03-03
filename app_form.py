import streamlit as st
from config import config
import app_db_setup as dbs
import requests
import pandas as pd
from datetime import datetime
from pytz import timezone, utc
from timezonefinder import TimezoneFinder
import geopandas
import matplotlib.pyplot as plt

params = config(section="data")

def signup():
  
  applicant_info_name = {
    # "year": params["year"],
    "name": st.text_input("Name", "")
  }

  city, country = st.beta_columns(2)
  applicant_info_loc = {
    "city": city.text_input("City", ""),
    "country": country.text_input("Country", "")
  }

  # Get latitude and longitude of participant's location
  location_valid, latitude, longitude = get_lat_long(applicant_info_loc)
  offset = utc_offset(location_valid, latitude, longitude)
  if location_valid:
      applicant_info_loc["latitude"] = latitude
      applicant_info_loc["longitude"] = longitude
      print_timezone(offset)

  draw_map(location_valid, latitude, longitude)  # will draw default map if location not valid

  applicant_info_comments = {
    "comments": st.text_area("Comments", "")
  }

  applicant_info = {**applicant_info_name, **applicant_info_loc, **applicant_info_comments}
  return applicant_info


def get_lat_long(info):
  city, country = [info["city"], info["country"]]
  location_query = "city=%s&country=%s" % (city, country)
  url = "https://nominatim.openstreetmap.org/search/?" + location_query + "&format=json"
  response = requests.get(url).json()
  if response:
        location_valid = True
        latitude = float(response[0]["lat"])
        longitude = float(response[0]["lon"])
  else:
      if city or country:
          st.error(f"""📌 Your location should be marked below; if not, 
                        please check that the details entered above are correct.""")
      location_valid = False
      latitude = 0.0
      longitude = 0.0
  return location_valid, latitude, longitude


def utc_offset(location_valid, lat, lng):
    """
    Returns a location's UTC offset in hours.
    Arguments:
    location_valid -- whether lat and lng have been determined by get_lat_long
    lat -- location's latitude
    lng -- location's longitude
    """
    if not location_valid:
        return 0
    today = datetime.now()
    tf = TimezoneFinder(in_memory=True)
    tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
    if tz_target is None:
        return 0
    today_target = tz_target.localize(today)
    today_utc = utc.localize(today)
    return (today_utc - today_target).total_seconds() / 3600


def draw_map(location_valid, latitude, longitude):
    fig, ax = plt.subplots()
    ax.axis('off')
    fig.patch.set_facecolor('None')
    fig.patch.set_edgecolor('#A8B3CC')
    fig.patch.set_linewidth('2')

    world_df = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world_plot = world_df.plot(figsize=(10, 10), ax=ax, alpha=0.3, color='#01852a', edgecolor='#0b5e24')
    
    point_df = pd.DataFrame({'Latitude': [latitude], 'Longitude': [longitude]})
    geo_point_df = geopandas.GeoDataFrame(
        point_df, geometry=geopandas.points_from_xy(point_df['Longitude'], point_df['Latitude']))

    # Plot point given by (latitude, longitude) on world map
    if location_valid:
        geo_point_df.plot(ax=world_plot, marker='*', markersize=300, color='#db0909')
    else:
        pass  # no location point to plot

    st.pyplot(fig)


def print_timezone(offset):
    if offset < 0:
        st.info(f"It looks like you are in time zone UTC{offset} 🤠.")
    else:
        st.info(f"It looks like you are in time zone UTC+{offset} 🤠.")


def save(response):
  # Initialize sqlite database
  connection = dbs.init_db()
  #save inputs to db
  dbs.save(connection, response)