import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


# Defining the resource
class Item(Resource):
    # Parsing the request
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,     # Price only float
        required = True,  # No req without price
        help = "This field cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        '''
        To select item from database with specific 'name'
        '''
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        # If item found
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        # If found an item so no need to add it just return message
        if self.find_by_name(name):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()
        
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        # Getting items data
        # data = request.get_json() # without payload
        data = Item.parser.parse_args()  # Parsing args come thru json payload

        # Filtering list for the searched item
        item = next(filter(lambda x: x['name'] == name, items), None)
        # If item not in the list
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        # If item found in the list
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}
