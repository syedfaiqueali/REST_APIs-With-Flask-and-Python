from typing import Dict, Union
from db import db

UserJSON = Dict[str, Union[int, str]]


class UserModel(db.Model):
    # To Tell SQLAlchemy tablename and col_name
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(
            username=username
        ).first()  # SELECT * FROM users WHERE username=username LIMIT 1

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
