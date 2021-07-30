from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

# Defining the resource
class Item(Resource):
    # Defining methods
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404


    def post(self, name):
        # If the req doesn't have proper content type, this will trigger error
        # get_json(force,silent)
        # force=True ;dont need content-type header, nice but dangerous
        # silent=True ;dont give error but return none
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}



# Adding resource and determine how its going to be access
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
