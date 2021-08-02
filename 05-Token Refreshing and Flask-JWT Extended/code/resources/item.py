from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
from models.item import ItemModel


class Item(Resource):
    # Parsing the request
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,     # Price only float
        required = True,  # No req without price
        help = "This field cannot be left blank"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a store it"
    )

    # Endpoints
    @jwt_required   # Without @jwt_required() at end because of 'flask_jwt_extended'
    def get(self, name):
        '''
        To select item from database with specific 'name'
        '''
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        # If found an item so no need to add it just return message
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400  # When req goes wrong

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item.'}, 500  # Internal Server Error

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        # get_jwt_claims is link up to our flask app and get data from the req coming and
        # interpret jwt comming thru req and extract the claim coming from the jwt
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        # Finding item
        item = ItemModel.find_by_name(name)
        # Checking if not null so delete
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}, 404

    def put(self, name):
        # Getting items data
        data = Item.parser.parse_args()  # Parsing args come thru json payload

        item = ItemModel.find_by_name(name)

        # If item not in the dB
        if item is None:
            try:
                item = ItemModel(name, **data) # or (name, data['price'], data['store_id'])
            except:
                return {'message': 'An error occured while inserting the item'}, 500
        # If item found in the dB
        else:
            try:
                item.price = data['price']
            except:
                return {'message': 'An error occured while updating the item'}, 500
        # Commit changes
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity() #give whatever we save in access token as identity
        items = [item.json() for item in ItemModel.find_all()]

        # Means user is still logged in
        if user_id:
            return {'items': items}, 200

        # User not logged in
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200
