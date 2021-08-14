import os

from db import db
from typing import List

# Defining table without Model, Table Id col would be default
# [id, item_id, order_id] => Columns
# [1, 3, 1]
# [2, 6, 1]
items_to_orders = db.Table(
    "items_to_orders",  # Table name
    db.Column("item_id", db.Integer, db.ForeignKey("items.id")),
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"))
)

class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    # Give a secondary table(items_to_orders) to go and find the items associated with the order
    # Many to many relationship
    items = db.relationship("ItemModel", secondary=items_to_orders, lazy="dynamic")

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "OrderModel":
        return cls.query.filter_by(id=_id).first()

    def set_status(self, new_status: str) -> None:
        self.status = new_status
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
