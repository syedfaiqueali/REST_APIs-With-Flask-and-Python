from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from blacklist import BLACKLIST

# Constants
BLANK_ERROR = "{} cannot be blank."
USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id} successfully logged out."

# Extract username and password from the request
# _user_parser => underscore in start to make its access 'private'
_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username", type=str, required=True, help=BLANK_ERROR.format("username")
)
_user_parser.add_argument(
    "password", type=str, required=True, help=BLANK_ERROR.format("password")
)


class UserRegister(Resource):
    # Endpoints
    @classmethod
    def post(cls):
        # Parse user's sent data from the req and return it as dict
        data = _user_parser.parse_args()

        # Check if user already exists
        if UserModel.find_by_username(data["username"]):
            return {"message": USER_ALREADY_EXISTS}, 400

        # Creating a UserModel obj and unpacking data dict containing username and password
        user = UserModel(**data)
        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)

        # If user not found in db
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        # Return the found user
        return user.json()

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)

        # If user not found in db
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        # User founded, delete it
        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # Parse user's sent data from the req and return it as dict
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data["username"])

        # check user and password => authenticate()
        if user and safe_str_cmp(user.password, data["password"]):
            # create access and refresh token and return it => identity()
            access_token = create_access_token(
                identity=user.id, fresh=True
            )  # fresh ;token refreshing
            refresh_token = create_refresh_token(user.id)

            return {
                "access_token": access_token,  # main jwt_token
                "refresh_token": refresh_token,
            }, 200

        # User doesn't exists
        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        # jti is JWT ID, a unique identifier for a JWT.
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
