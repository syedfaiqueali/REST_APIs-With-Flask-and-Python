from flask import g, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from oa import github

from models.user import UserModel

class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(callback="http://localhost:5000/login/github/authorized")


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = github.authorized_response()

        # Edge case check
        if resp is None or resp.get("access_token") is None:
            error_response = {
                "error": request.args["error"],
                "error_description": request.args["error_description"]
            }
            return error_response

        g.access_token = resp['access_token']  #return access_token
        github_user = github.get('user')   #get user's github details
        github_username = github_user.data['login'] #get user's name

        # Find user if exits in our db
        user = UserModel.find_by_username(github_username)

        # If not exits so save it to db without password
        if not user:
            user = UserModel(username=github_username, password=None)
            user.save_to_db()

        #
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200
