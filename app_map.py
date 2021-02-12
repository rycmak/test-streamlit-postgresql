import streamlit as st
import app_db_setup as dbs
import pandas as pd

def load_data():
    connection = dbs.init_db()
    cur = connection.cursor()
    query = "SELECT * FROM magicians;"
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

def draw_map(df):
    st.map(df[["latitude", "longitude"]], zoom = 0)
    if st.checkbox("Reveal all magicians"):
        st.write(df[["name", "city", "country"]])
