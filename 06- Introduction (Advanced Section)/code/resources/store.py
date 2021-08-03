from flask_restful import Resource
from models.store import StoreModel

# Constants
ERROR_INSERTING = "An error occured inserting the store."
NAME_ALREDY_EXISTS = "An store with name {} already exists."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted."


class Store(Resource):
    # Endpoints
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        # If store found
        if store:
            return store.json()  # Return items as well
        return {"message": STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": NAME_ALREDY_EXISTS.format(name)}, 400

        # Store doesn't exists, so creating a new store
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return store.json(), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": STORE_DELETED}


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {
            "stores": [store.json() for store in StoreModel.find_all()]
        }  # query.all() is not suitable to use in Resource
