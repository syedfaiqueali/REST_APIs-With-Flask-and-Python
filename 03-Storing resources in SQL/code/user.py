import sqlite3
from flask_restful import Resource, reqparse

class User:
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


class UserRegister(Resource):

    # Parse through json req and make sure username and password are not blank
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = "This field cannot be blank."
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field cannot be blank."
    )

    def post(self):
        # Using UserRegister parser
        data = UserRegister.parser.parse_args()

        # Check if user already exists
        if User.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created successfully.'}, 201
