from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
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
NOT_CONFIRMED_ERROR = (
    "You have not confirmed registeration, please check your email <{}>."
)
USER_CONFIRMED = "User confirmed."

# Creating Schema
user_schema = UserSchema()


class UserRegister(Resource):
    # Endpoints
    @classmethod
    def post(cls):
        # Creating a UserModel obj
        user_json = request.get_json()
        user = user_schema.load(user_json)  #return dict
        user_obj = UserModel(**user)   #convert dict to obj

        # Check if user already exists
        if UserModel.find_by_username(user_obj.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        user_obj.save_to_db()

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
        user_json = request.get_json()
        user_data = user_schema.load(user_json)  # Which we got from request

        user_obj = UserModel(**user_data)

        # find req data into the dB => returns obj
        user = UserModel.find_by_username(user_obj.username)

        # check user and password => authenticate()
        if user and safe_str_cmp(user_obj.password, user.password):
            #
            if user.activated:
                # create access and refresh token and return it => identity()
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)

                return {
                    "access_token": access_token,  # main jwt_token
                    "refresh_token": refresh_token,
                }, 200
            return {"message": NOT_CONFIRMED_ERROR.format(user.username)}, 400

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


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not User:
            return {"message": USER_NOT_FOUND}, 404

        # If user found in dB so activate him
        user.activated = True
        user.save_to_db()
        return {"message": USER_CONFIRMED}, 200
