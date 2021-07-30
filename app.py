from flask import Flask, jsonify, request

app = Flask(__name__)

# Request it going to understand
'''
@app.route('/')  # 'http://www.google.com/'
def home():
    return 'Hello, world faiq!'
'''

stores = [
    {
        'name': 'Imtiaz',
        'items': [
            {
                'name': 'Item1',
                'price': 15.99
            }
        ]
    }
]

# POST - used to receive the data
# GET - used to send data back only

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over stores
    for store in stores:
        # If the store name matches, return it
        if store['name'] == name:
            return jsonify(store)
    # If none match, return an error message
    return jsonify({'message': 'Store not found !!'})


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name:, price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()

    # Iterate over stores
    for store in stores:
        # If the store name matches, return it
        if store['name'] == name:
            # Create new item
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            # Return new item
            return jsonify(new_item)
    # Return message if store not found
    return jsonify({'message': 'Store not found !!'})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    # Iterate over stores
    for store in stores:
        # If the store name matches, return it
        if store['name'] == name:
            return jsonify({'items': store['items']})
    # Return message if store not found
    return jsonify({'message': 'Store not found !!'})


app.run(port=5000)
