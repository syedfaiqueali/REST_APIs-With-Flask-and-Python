import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


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
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created successfully.'}, 201
