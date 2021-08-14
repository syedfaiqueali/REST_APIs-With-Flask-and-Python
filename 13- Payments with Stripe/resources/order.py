from collections import Counter

from flask import request
from flask_restful import Resource

from libs.strings import gettext
from models.item import ItemModel
from models.order import OrderModel, ItemsInOrder


class Order(Resource):
    @classmethod
    def post(cls):
        """
        Expect a token and a list of item ids from the request body.
        Construct an order and talk to the Stripe API to make a charge.
        """
        data = request.get_json() # Token + list of item id's
        items = []

        # Count item ids quantities items[5,5,5] => (5,3) ;5 is 3times
        item_id_quantities = Counter(data["item_ids"])

        # Iterate over items and retrieve them from the database
        # (id, count) -> for loop
        for _id in count in item_id_quantities.most_common(): #most_common() -> [(5,3), (3,1), (2,1)]
            item = ItemModel.find_by_id(_id)
            if not item:
                return {"message": gettext("order_item_by_id_not_found").format(_id)}, 404

            # Item not found in list so append it in items list
            items.append(ItemsInOrder(item_id=_id, quantity=count))

        order = OrderModel(items=items, status="pending")
        order.save_to_db()  # This does not submit to stripe

        order.set_status("something")
