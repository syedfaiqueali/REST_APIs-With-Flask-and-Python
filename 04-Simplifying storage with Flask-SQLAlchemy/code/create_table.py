import sqlite3

# Creating Database
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Creating tables
create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

# Saving and terminate connection
connection.commit()
connection.close()
