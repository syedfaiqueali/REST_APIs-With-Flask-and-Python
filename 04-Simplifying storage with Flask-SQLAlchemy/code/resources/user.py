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

    # Endpoints
    def post(self):
        # Using UserRegister parser
        data = UserRegister.parser.parse_args()

        # Check if user already exists
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        # Creating a UserModel obj and unpacking data dict containing username and password
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201
