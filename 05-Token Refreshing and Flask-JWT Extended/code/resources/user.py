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


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        # If user not found in db
        if not user:
            return {'message': 'User not found'}, 404
        # Return the found user
        return user.json()


    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)

        # If user not found in db
        if not user:
            return {'message': 'User not found'}, 404
        # User founded, delete it
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200
