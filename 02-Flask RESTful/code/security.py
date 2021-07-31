# imports
from werkzeug.security import safe_str_cmp
from user import User


# Table for registered users
users = [
    User(1, 'bob', 'asdf')
]

'''
username_mapping = { 'bob': {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
}

userid_mapping = { 1: {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
}
'''
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


# Function to authenticate the user
def authenticate(username, password):
    # Accessing dict using get(key, None(for not found key))
    user = username_mapping.get(username, None)

    # Checking user not none and user's password matches
    if user and safe_str_cmp(user.password, password):
        return user


# Function Unique to flask JWT, payload(contents of jwt tokens)
def identity(payload):
    # Extract user's if from the payload
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
