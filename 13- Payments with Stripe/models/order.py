import os
import stripe

from db import db
from typing import List

# Constants
CURRENCY = "usd"

# Defining table without Model, Table Id col would be default
# [id, item_id, order_id] => Columns
# [1, 3, 1]
# [2, 6, 1]
'''
items_to_orders = db.Table(
    "items_to_orders",  # Table name
    db.Column("item_id", db.Integer, db.ForeignKey("items.id")),
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"))
)
'''

class ItemsInOrder(db.Model):
    __tablename__ = "items_in_orders"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)

    item = db.relationship("ItemModel")
    order = db.relationship("OrderModel", back_populates="items")


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    # back_populates="order" (when we want reflective changes to occur in both tables)
    items = db.relationship("ItemsInOrder", back_populates="order")

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "OrderModel":
        return cls.query.filter_by(id=_id).first()

    def charge_with_stripe(self, token:str) -> stripe.Charge:
        stripe.api_key = os.getenv("STRIPE_API_KEY")

        return stripe.Charge.create(
            amount=self.amount,  # amount of cents (100 means USD$1.00)
            currency=CURRENCY,
            description=self.description,
            source=token
        )

    def set_status(self, new_status: str) -> None:
        self.status = new_status
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
