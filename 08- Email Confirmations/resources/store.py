from flask_restful import Resource
from models.store import StoreModel
from schemas.store import StoreSchema

# Constants
ERROR_INSERTING = "An error occured inserting the store."
NAME_ALREDY_EXISTS = "An store with name {} already exists."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted."

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    # Endpoints
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        # If store found
        if store:
            return store_schema.dump(store), 200  # Return items as well
        return {"message": STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": NAME_ALREDY_EXISTS.format(name)}, 400

        # Store doesn't exists, so creating a new store
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": STORE_DELETED}


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"stores": store_list_schema.dump(StoreModel.find_all())}, 200
