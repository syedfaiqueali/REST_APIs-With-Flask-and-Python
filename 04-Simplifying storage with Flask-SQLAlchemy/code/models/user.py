import sqlite3
from db import db

class UserModel(db.Model):
    # To Tell SQLAlchemy tablename and col_name
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) # Parameter should always be tuple
        # Fetch first row from results set
        row = result.fetchone()
        # If row not none
        if row:
            user = cls(*row) # row[0], row[1], row[3] => *row
        else:
            user = None
        # Close connection
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,)) # Parameter should always be tuple
        # Fetch first row from results set
        row = result.fetchone()
        # If row not none
        if row:
            user = cls(*row) # row[0], row[1], row[3] => *row
        else:
            user = None
        # Close connection
        connection.close()
        return user
