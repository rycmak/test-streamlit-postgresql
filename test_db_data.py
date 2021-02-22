import app_db_setup as dbs

connection = dbs.init_db()
cur = connection.cursor()
query = """INSERT INTO shows (year, month, fk_magician_1_id, fk_magician_2_id) VALUES
         (2025, 3, (SELECT id FROM magicians WHERE name = 'Harry Potter'), 
                    (SELECT id FROM magicians WHERE name = 'Jackie O'))"""
cur.execute(query)
query = """INSERT INTO shows (year, month, fk_magician_1_id, fk_magician_2_id) VALUES
        (2089, 10, (SELECT id FROM magicians WHERE name = 'Harry Potter'), 
                  (SELECT id FROM magicians WHERE name = 'Thor the Norse God'))"""
cur.execute(query)                  
query = """INSERT INTO shows (year, month, fk_magician_1_id, fk_magician_2_id) VALUES
         (2091, 12, (SELECT id FROM magicians WHERE name = 'Thor the Norse God'), 
                  (SELECT id FROM magicians WHERE name = 'Rumpelstilschen'))"""
cur.execute(query)
connection.close()