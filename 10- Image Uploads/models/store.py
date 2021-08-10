from typing import List  # For type hinting
from db import db


class StoreModel(db.Model):
    # To Tell SQLAlchemy tablename and col_name
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # Back reference of store to keep check of its items
    # lazy='dynamic' ;tells SQLAlchemy to not go into the items table
    # and creates an obj for each item and everytime we call json(self)
    # we have to look into table again and again
    # overlaps="store" ;to hide warning in debug
    items = db.relationship("ItemModel", lazy="dynamic", overlaps="store")

    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        # return an item obj from db
        return cls.query.filter_by(
            name=name
        ).first()  # SELECT * FROM stores WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        return cls.query.all()

    # Using both for insert and update
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
