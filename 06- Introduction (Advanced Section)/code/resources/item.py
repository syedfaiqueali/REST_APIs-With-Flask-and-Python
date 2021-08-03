from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.item import ItemModel

# Constants
BLANK_ERROR = "{} cannot be blank."
ERROR_INSERTING = "An error occured inserting the item."
ERROR_UPDATING = "An error occured while updating the item."
NAME_ALREDY_EXISTS = "An item with name {} already exists."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."


class Item(Resource):
    # Parsing the request
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,  # Price only float
        required=True,  # No req without price
        help=BLANK_ERROR.format("price"),
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=BLANK_ERROR.format("store_id")
    )

    # Endpoints
    @classmethod
    def get(cls, name: str):
        """
        To select item from database with specific 'name'
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):
        # If found an item so no need to add it just return message
        if ItemModel.find_by_name(name):
            return {
                "message": NAME_ALREDY_EXISTS.format(name)
            }, 400  # When req goes wrong

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500  # Internal Server Error

        return item.json(), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        # Finding item
        item = ItemModel.find_by_name(name)
        # Checking if not null so delete
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, name: str):
        # Getting items data
        data = Item.parser.parse_args()  # Parsing args come thru json payload

        item = ItemModel.find_by_name(name)

        # If item not in the dB
        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {"message": ERROR_INSERTING}, 500
        # If item found in the dB
        else:
            try:
                item.price = data["price"]
            except:
                return {"message": ERROR_UPDATING}, 500
        # Commit changes
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": [item.json() for item in ItemModel.find_all()]}, 200
