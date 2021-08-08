import traceback

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

from libs.strings import gettext
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel

# Creating Schema
user_schema = UserSchema()


class UserRegister(Resource):
    # Endpoints
    @classmethod
    def post(cls):
        # Creating a UserModel obj
        user_json = request.get_json()
        user = user_schema.load(user_json)  # return dict
        user_obj = UserModel(**user)  # convert dict to obj

        # Check if user already exists
        if UserModel.find_by_username(user_obj.username):
            return {"message": gettext("user_username_exists")}, 400

        # Check if email is unique
        if UserModel.find_by_email(user_obj.email):
            return {"message": gettext("user_email_exists")}, 400

        try:
            user_obj.save_to_db()

            # Create a confirmation model with user id and save it to db before sending confirmation email
            confirmation = ConfirmationModel(user_obj.id)
            confirmation.save_to_db()

            user_obj.send_confirmation_email()
            return {"message": gettext("user_registered")}, 201

        except MailGunException as e:  # When send_confirmation_email() failed
            user_obj.delete_from_db()
            return {"message": str(e)}, 500
        except:
            traceback.print_exc()  # Failed to save user into db or other exceptions
            user_obj.delete_from_db()
            return {"message": gettext("user_error_creating")}, 500


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)

        # If user not found in db
        if not user:
            return {"message": gettext("user_not_found")}, 404
        # Return the found user
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)

        # If user not found in db
        if not user:
            return {"message": gettext("user_not_found")}, 404
        # User founded, delete it
        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # Passing dict from req to user_schema
        user_json = request.get_json()
        user_data = user_schema.load(
            user_json, partial=("email",)
        )  # Which we got from request, ignore email if not present

        user_obj = UserModel(**user_data)

        # find req data into the dB => returns obj
        user = UserModel.find_by_username(user_obj.username)

        # check user and password => authenticate()
        if user and safe_str_cmp(user_obj.password, user.password):
            # If confirmation exists and is confirmed
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                # create access and refresh token and return it => identity()
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)

                return {
                    "access_token": access_token,  # main jwt_token
                    "refresh_token": refresh_token,
                }, 200
            return {"message": gettext("user_not_confirmed").format(user.email)}, 400

        # User doesn't exists
        return {"message": gettext("user_invalid_credentials")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        # jti is JWT ID, a unique identifier for a JWT.
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
