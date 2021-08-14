from flask_restful import Resource
from oa import github

class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(callback="http://localhost:5000/login/github/authorized")
