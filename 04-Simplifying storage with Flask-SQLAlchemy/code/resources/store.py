from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    # Endpoints
    def get(self, name):
        store = StoreModel.find_by_name(name)
        # If store found
        if store:
            return store.json()  #Return items as well
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A store with name \'{}\' already exists.'.format(name)}, 400

        # Store doesn't exists, so creating a new store
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured while creating the store.'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
