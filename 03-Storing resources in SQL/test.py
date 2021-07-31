import sqlite3

# Initialize connection
connection = sqlite3.connect('data.db')

# Allows to start things(responsible for executing the queries)
cursor = connection.cursor()

# Creatng Queries
create_table = "CREATE TABLE users(id int, username text, password text)"

# Executing queries
cursor.execute(create_table)

# Storing data into dB
user = (1, 'faiq', 'asdf')
insert_query = "INSERT INTO users VALUES(?, ?, ?)"

# Run query
cursor.execute(insert_query, user)

# Inserting many users
users = [
    (2, 'ali', 'asdf'),
    (3, 'syed', 'asdf')
]
cursor.executemany(insert_query, users)

# Select query
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# To save values
connection.commit()
# To close connection
connection.close()
