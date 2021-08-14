import os
import stripe

from db import db
from typing import List
from flask import Flask, jsonify

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

    @property
    def description(self):
        """
        Generates a simple string represting this order,
        in the format of 5x chairs, 2x tables
        """
        item_counts = [f"{i.quantity}x {i.item.name}" for i in self.items]
        return ",".join(item_counts)

    @property
    def amount(self):
        # Price * Quantity Do this for all items in list
        # To convert into cents => * 100
        # sum is 29.95 -> *100 -> 2995 -> int(2995)
        # sum is 29.95 -> int(29.55) -> 29*100 -> 2900 => Loose value
        return int(sum([item_data.item.price * item_data.quantity for item_data in self.items]) * 100)

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

    def charge_with_stripe1(self):
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        
        intent = stripe.PaymentIntent.create(
            amount=self.amount,
            currency=CURRENCY,
            payment_method_types=['card'],
            description=self.description
        )

        return jsonify(client_secret=intent.client_secret)

    def set_status(self, new_status: str) -> None:
        self.status = new_status
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
