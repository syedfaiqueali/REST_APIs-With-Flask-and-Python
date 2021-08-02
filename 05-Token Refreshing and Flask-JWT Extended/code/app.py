from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import UserRegister, User, UserLogin       # Importing resources to let SQLAlchemy know them
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# App config properties
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # From where to read db file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False         # Disable db to track every modifications
app.config['PROPAGATE_EXCEPTION'] = True                     # To allow Flask Extensions raise their own exceptions
# app.config['JWT_SECRET_KEY'] => If want to have app and jwt secret key diff
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


# Adding resource and determine how its going to be access
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login') # can also call it /auth

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
