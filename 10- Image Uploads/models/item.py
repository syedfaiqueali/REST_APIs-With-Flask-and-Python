from typing import List  # For type hinting
from db import db


class ItemModel(db.Model):
    # To Tell SQLAlchemy tablename and col_name
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(80), unique=True, nullable=False
    )  # unique =True => No 2 rows can have same value
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    # It will see store_id and find items belonging to that store
    # No needs for joins in SQLAlchemy
    store = db.relationship("StoreModel")

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        # return an item obj from db
        return cls.query.filter_by(
            name=name
        ).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    # Using both for insert and update
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
