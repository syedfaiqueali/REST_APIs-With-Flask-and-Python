from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.user import UserRegister, User       # Importing resources to let SQLAlchemy know them
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

# App config properties
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # From where to read db file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False         # Disable db to track every modifications
app.config['PROPAGATE_EXCEPTION'] = True                     # To allow Flask Extensions raise their own exceptions
app.secret_key = 'jose'
api = Api(app)

# This decorator is going to affect method below it
#  and going to run first before first request into this app
@app.before_first_request
def create_tables():
    db.create_all()

# /auth
jwt = JWT(app, authenticate, identity)

# Adding resource and determine how its going to be access
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
