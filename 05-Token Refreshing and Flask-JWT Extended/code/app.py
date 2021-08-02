from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh   # Importing resources to let SQLAlchemy know them
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

# App config properties
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # From where to read db file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False         # Disable db to track every modifications
app.config['PROPAGATE_EXCEPTION'] = True                     # To allow Flask Extensions raise their own exceptions
# app.config['JWT_SECRET_KEY'] => If want to have app and jwt secret key diff
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] #Enable blacklist for both 'access' and 'refresh'
app.secret_key = 'jose'                                      # 'jose' is used to encrypt the JWT
api = Api(app)

# This decorator is going to affect method below it
#  and going to run first before first request into this app
@app.before_first_request
def create_tables():
    db.create_all()

# not creating /auth, have to create them self explicitly
jwt = JWTManager(app)

# This decorator will link our func to the above JWTManager
# This func will check that if we may want to add some extra data to our JWT
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Instead of hard coding, read it from a config file or a dB
        return {'is_admin': True}
    return {'is_admin': False}

# Return true if token being sent isn't the blacklisted
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):   # Can access any detail from decrypted_token
    return decrypted_token['jti'] in BLACKLIST      # return => Bool ;if false then goes to revoked_token_callback()


# To what to tell user when their token is expired, i.e after 5mins
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

# When token sent us is not an actual JWT
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

# When user logged out so put that token in revoked tokens list
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


# Adding resource and determine how its going to be access
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login') # can also call it /auth
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
