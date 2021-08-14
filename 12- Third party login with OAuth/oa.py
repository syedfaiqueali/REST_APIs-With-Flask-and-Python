"""
THE FILE WILL HOST ALL CLIENT SETTINGS.
"""

import flask_oauthlib.client import OAuth

oauth = OAuth()

github = oauth.remote_app(
    'github',
    consumer_key=os.getenv("GITHUB_CONSUMER_KEY"),
    consumer_secret=os.getenv("GITHUB_CONSUMER_SERCRET"),
    request_token_params={"scope": "user:email"}, # &scope=user:email -> Adds in req
    base_url="https://api.github.com/",
    request_token_url=None,  #OAuth2.0 mein None
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token", # What we send data to get access_token back
    authorized_url="https://github.com/login/oauth/authorize" # Where we send user in initial req
)
