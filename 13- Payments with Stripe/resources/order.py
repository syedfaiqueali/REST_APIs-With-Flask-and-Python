from collections import Counter

from flask import request
from flask_restful import Resource
from stripe import error

from libs.strings import gettext
from models.item import ItemModel
from models.order import OrderModel, ItemsInOrder
from schemas.order import OrderSchema

order_schema = OrderSchema()

class Order(Resource):
    @classmethod
    def get(cls):
        return order_schema.dump(OrderModel.find_all(), many=True), 200

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
        for _id, count in item_id_quantities.most_common(): #most_common() -> [(5,3), (3,1), (2,1)]
            item = ItemModel.find_by_id(_id)
            if not item:
                return {"message": gettext("order_item_by_id_not_found").format(_id)}, 404

            # Item not found in list so append it in items list
            items.append(ItemsInOrder(item_id=_id, quantity=count))

        order = OrderModel(items=items, status="pending")
        order.save_to_db()  # This does not submit to stripe

        try:
            # Use Stripe's library to make requests...
            order.set_status("failed")
            #order.charge_with_stripe(data["token"])
            order.charge_with_stripe1()
            order.set_status("complete") # Only if above line passes

            return order_schema.dump(order), 200

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            print('Status is: %s' % e.http_status)
            print('Code is: %s' % e.code)
            # param is '' in this case
            print('Param is: %s' % e.param)
            print('Message is: %s' % e.user_message)
            return e.json_body, e.http_status
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return e.json_body, e.http_status
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            return e.json_body, e.http_status
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return e.json_body, e.http_status
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return e.json_body, e.http_status
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return e.json_body, e.http_status
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            print(e)
            return {"message": gettext("order_error")}, 500
