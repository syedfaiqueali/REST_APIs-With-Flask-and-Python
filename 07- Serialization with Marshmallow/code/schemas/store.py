from ma import ma
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    # Tells ma that items property is nested inside store and contains many items
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel  # Go into StoreModel and look into column def & create marshmallow fields
        dump_only = ("id",)  # Will not be looked at when creating the model
        include_fk = True  # Include ForeignKey
