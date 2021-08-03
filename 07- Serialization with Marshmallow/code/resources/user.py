from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from marshmallow import ValidationError
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST

# Constants
BLANK_ERROR = "{} cannot be blank."
USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={}> successfully logged out."

# Creating Schema
user_schema = UserSchema()


class UserRegister(Resource):
    # Endpoints
    @classmethod
    def post(cls):
        # Passing dict from req to user_schema
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        # Check if user already exists
        if UserModel.find_by_username(user_data["username"]):
            return {"message": USER_ALREADY_EXISTS}, 400

        # Creating a UserModel obj and unpacking user_data dict containing username and password
        user = UserModel(**user_data)
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
        return user_schema.dump(user), 200

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
        # Passing dict from req to user_schema
        try:
            user_json = request.get_json()
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            return err.messages, 400

        # find user in database
        user = UserModel.find_by_username(user_data["username"])

        # check user and password => authenticate()
        if user and safe_str_cmp(user.password, user_data["password"]):
            # create access and refresh token and return it => identity()
            access_token = create_access_token(identity=user.id, fresh=True)
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
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
