# imports
from werkzeug.security import safe_str_cmp
from models.user import UserModel

# Function to authenticate the user
def authenticate(username, password):
    # Looking user into dB
    user = UserModel.find_by_username(username)

    # Checking user not none and user's password matches
    if user and safe_str_cmp(user.password, password):
        return user


# Function Unique to flask JWT, payload(contents of jwt tokens)
def identity(payload):
    # Extract user's if from the payload
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
