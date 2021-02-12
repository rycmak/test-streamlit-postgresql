import streamlit as st
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import config

def init_db():
  """ Connect to PostgreSQL server """
  connection = None
  try:
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    db_name = params["database"]

    connection = psycopg2.connect(**params)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = connection.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS magicians (
                      year INTEGER NOT NULL,
                      name VARCHAR(255) NOT NULL PRIMARY KEY,
                      city TEXT NOT NULL,
                      country TEXT NOT NULL,
                      latitude REAL NOT NULL,
                      longitude REAL NOT NULL
                    );""")
    return connection

  except (Exception, psycopg2.DatabaseError) as error:
    print(error)


def save(connection, response):
    cur = connection.cursor()
    query = """INSERT INTO magicians (year, name, city, country, latitude, longitude) 
                VALUES (%s, %s, %s, %s, %s, %s);"""
    data = [r for r in response.values()]
    try:
      cur.execute(query, data)
      st.success("Success!  You are now a magician! 🎉")
      st.balloons()
    except (Exception, psycopg2.DatabaseError) as error:
      st.error(f"You application to become a magician has been unsuccessful 😱.")
      st.error(error)
   
    connection.close()
    print('Database connection closed.')
