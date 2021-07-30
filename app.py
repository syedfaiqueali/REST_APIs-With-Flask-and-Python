from flask import Flask

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
    pass

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    pass

# GET /store
@app.route('/store')
def get_stores(name):
    pass

# POST /store/<string:name>/item {name:, price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    pass



app.run(port=5000)
