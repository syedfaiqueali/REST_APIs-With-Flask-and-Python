import os

from flask import Flask, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager

from flask_uploads import configure_uploads, patch_request_class
from marshmallow import ValidationError
from dotenv import load_dotenv

from ma import ma
from db import db
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.image import ImageUpload, Image, AvatarUpload
from libs.image_helper import IMAGE_SET

app = Flask(__name__)
load_dotenv(".env", verbose=True)  # load .env
app.config.from_object("default_config")  # load config using 'default_config'
app.config.from_envvar("APPLICATION_SETTINGS")  # Now load 'app config'
# app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
patch_request_class(app, 10 * 1024 * 1024)  # to limit max size of images =10MB
configure_uploads(app, IMAGE_SET)
api = Api(app)

# This decorator is going to affect method below it
#  and going to run first before first request into this app
@app.before_first_request
def create_tables():
    db.create_all()


# By defining this now no need to try except ValidationError anywhere
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


# not creating /auth, have to create them self explicitly
jwt = JWTManager(app)

# Return true if token being sent isn't the blacklisted
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(
    decrypted_token,
):  # Can access any detail from decrypted_token
    return (
        decrypted_token["jti"] in BLACKLIST
    )  # return => Bool ;if false then goes to revoked_token_callback()


# Registering resource and determine how its going to be access
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")  # can also call it /auth
api.add_resource(UserLogout, "/logout")
api.add_resource(
    Confirmation, "/user_confirmation/<string:confirmation_id>"
)  # For HTML page
api.add_resource(
    ConfirmationByUser, "/confirmation/user/<int:user_id>"
)  # For retrieving or resending confirmation
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(AvatarUpload, "/upload/avatar")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)  # Tell marshmallow obj what flask app is it talking to
    app.run(port=5000, debug=True)
