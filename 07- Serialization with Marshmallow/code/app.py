from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from ma import ma
from db import db
from blacklist import BLACKLIST
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh

# App config properties
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///data.db"  # From where to read db file
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # Disable db to track every modifications
app.config[
    "PROPAGATE_EXCEPTIONS"
] = True  # To allow Flask Extensions raise their own exceptions
# app.config['JWT_SECRET_KEY'] => If want to have app and jwt secret key diff
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # Enable blacklist for both 'access' and 'refresh'
app.secret_key = "jose"  # 'jose' is used to encrypt the JWT
api = Api(app)

# This decorator is going to affect method below it
#  and going to run first before first request into this app
@app.before_first_request
def create_tables():
    db.create_all()


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
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)  # Tell marshmallow obj what flask app is it talking to
    app.run(port=5000, debug=True)
