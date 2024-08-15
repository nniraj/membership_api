import sqlite3

with open('schema.sql', 'r') as sql_file:
    sql_script = sql_file.read()

db = sqlite3.connect('members.db')
cursor = db.cursor()
cursor.executescript(sql_script)
db.commit()
db.close()