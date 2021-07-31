import sqlite3

# Creating Database
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Creating tables
create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items(name text, price real)"
cursor.execute(create_table)

# Item entry for testing purpose
cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

# Saving and terminate connection
connection.commit()
connection.close()
