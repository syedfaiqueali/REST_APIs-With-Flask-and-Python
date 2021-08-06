from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from marshmallow import ValidationError
from models.item import ItemModel
from schemas.item import ItemSchema

# Constants
BLANK_ERROR = "{} cannot be blank."
ERROR_INSERTING = "An error occured inserting the item."
ERROR_UPDATING = "An error occured while updating the item."
NAME_ALREDY_EXISTS = "An item with name {} already exists."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."

item_schema = ItemSchema()  # Single Item
item_list_schema = ItemSchema(many=True)  # Many items


class Item(Resource):
    # Endpoints
    @classmethod
    def get(cls, name: str):
        """
        To select item from database with specific 'name'
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):
        # If found an item so no need to add it just return message
        if ItemModel.find_by_name(name):
            return {
                "message": NAME_ALREDY_EXISTS.format(name)
            }, 400  # When req goes wrong

        item_json = request.get_json()  # get user's sent json payload
        item_json["name"] = name  # Populating json with items name

        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500  # Internal Server Error

        return item_schema.dump(item), 201

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
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        # updating
        if item:
            item.price = item_json["price"]
        # Inserting
        else:
            item_json["name"] = name  # Populating json with item's name
            item = item_schema.load(item_json)

        # Commit changes
        item.save_to_db()
        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200
