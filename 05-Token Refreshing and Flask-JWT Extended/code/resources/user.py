from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp
from models.user import UserModel

# Extract username and password from the request
# _user_parser => underscore in start to make its access 'private'
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type = str,
                          required = True,
                          help = "This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type = str,
                          required = True,
                          help = "This field cannot be blank."
                          )

class UserRegister(Resource):
    # Endpoints
    def post(self):
        # Parse user's sent data from the req and return it as dict
        data = _user_parser.parse_args()

        # Check if user already exists
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        # Creating a UserModel obj and unpacking data dict containing username and password
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
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


class UserLogin(Resource):
    def post(self):
        # Parse user's sent data from the req and return it as dict
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data['username'])

        # check user and password => authenticate()
        if user and safe_str_cmp(user.password, data['password']):
            # create access and refresh token and return it => identity()
            access_token = create_access_token(identity=user.id, fresh=True) # fresh ;token refreshing
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        # User doesn't exists
        return {'message': 'Invalid credentials!'}, 401
