from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.Schema):
    # Tell marshmallow that password field is only for loading data
    class Meta:
        model = ItemModel  # Go into ItemModel and look into column def & create marshmallow fields
        load_only = ("store",)  # Will not return(dump) store by doing this
        dump_only = ("id",)  # Will not be looked at when creating the model
        include_fk = True  # Include ForeignKey
