import streamlit as st
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import config

def init_db():
  """
  Connect to PostgreSQL server
  and create relevant tables needed for user sign-up.

  Note: The table "rounds" containing info about year should exist even if there are no users.
  Before the app is opened for user sign-up, create this table:
  "CREATE TABLE IF NOT EXISTS rounds (
                      id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                      year INTEGER UNIQUE NOT NULL);"
  insert_rounds = "INSERT INTO rounds (year) VALUES (%s);"
  cursor.execute(insert_rounds, [config(section='data')['year']])
  """
  connection = None
  if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ["DATABASE_URL"]
  else:
    db = config()
    DATABASE_URL = f"postgresql://{db['user']}@{db['host']}/{db['database']}"
  try:
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = connection.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS magicians_all (
                      id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
                      name VARCHAR(255) UNIQUE NOT NULL);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS locations (
                      id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                      city TEXT NOT NULL,
                      country TEXT NOT NULL,
                      latitude REAL NOT NULL,
                      longitude REAL NOT NULL,
                      CONSTRAINT locations_city_country UNIQUE (city, country));""")
    cur.execute("""CREATE TABLE IF NOT EXISTS shows (
                      id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                      fk_round_id INTEGER NOT NULL REFERENCES rounds(id),
                      fk_magician_1_id INTEGER NOT NULL REFERENCES magicians_all(id),
                      fk_magician_2_id INTEGER NOT NULL REFERENCES magicians_all(id),
                      CONSTRAINT shows_rid_m1id UNIQUE (fk_round_id, fk_magician_1_id),
                      CONSTRAINT shows_rid_m2id UNIQUE (fk_round_id, fk_magician_2_id));""")
    cur.execute("""CREATE TABLE IF NOT EXISTS magicians_rounds (
                      id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                      fk_magician_id INTEGER NOT NULL REFERENCES magicians_all(id),
                      fk_location_id INTEGER NOT NULL REFERENCES locations(id),
                      comments TEXT NOT NULL,
                      fk_round_id INTEGER NOT NULL REFERENCES rounds(id),
                      fk_show_id INTEGER REFERENCES shows(id) ON DELETE SET NULL,
                      CONSTRAINT magicians_rounds_mid_rid UNIQUE (fk_magician_id, fk_round_id));""")
    return connection

  except (Exception, psycopg2.DatabaseError) as error:
    print(error)


def save(connection, response):
    cur = connection.cursor()
    insert_magicians_all = """INSERT INTO magicians_all (name) VALUES (%s)
                                ON CONFLICT (name) DO NOTHING;"""
    insert_locations = """INSERT INTO locations (city, country, latitude, longitude)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT ON CONSTRAINT locations_city_country DO NOTHING;"""
    insert_magicians_rounds = """INSERT INTO magicians_rounds 
                                  (fk_magician_id, fk_location_id, comments, fk_round_id) 
                                  VALUES (%s, %s, %s, %s);"""
    try:
      cur.execute(insert_magicians_all, [response["name"]])
      cur.execute(insert_locations, [response["city"], response["country"], 
                                      response["latitude"], response["longitude"]])
      cur.execute("SELECT id FROM magicians_all WHERE name = %s;", [response["name"]])
      magician_id = cur.fetchone()
      cur.execute("SELECT id FROM locations WHERE city = %s AND country = %s;", 
                    [response["city"], response["country"]])
      location_id = cur.fetchone()
      cur.execute("SELECT id FROM rounds WHERE year = %s", [config(section='data')['year']])
      round_id = cur.fetchone()
      cur.execute(insert_magicians_rounds, [magician_id, location_id, response["comments"], round_id])
      st.success("Success!  You are now a magician! 🎉")
      st.balloons()
    except (Exception, psycopg2.DatabaseError) as error:
      st.error(f"You application to become a magician has been unsuccessful 😱.")
      st.error(error)
   
    connection.close()
    print('Database connection closed.')
