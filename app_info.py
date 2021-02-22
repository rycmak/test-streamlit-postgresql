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
        st.write(df[["id", "name", "city", "country"]])

def list_shows():
    st.header("Find magic shows:")
    magician = st.text_input("Magician name:", "")
    if magician == "":
        return
    connection = dbs.init_db()
    cur = connection.cursor()
    cur.execute("SELECT * FROM magicians WHERE name = '%s'" % magician)
    magician_id = cur.fetchone()[0]
    query = """SELECT * FROM shows WHERE fk_magician_1_id = %s
                    OR fk_magician_2_id = %s;""" % (str(magician_id), str(magician_id))
    df = pd.read_sql_query(query, connection)
    if len(df) > 0:
        st.write(df)
    else:
        st.info("Sorry, no shows found 😥.")