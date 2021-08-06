from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    # Tell marshmallow that password field is only for loading data
    class Meta:
        model = UserModel  # Go into UserModel and look into column def & create marshmallow fields
        load_only = ("password",)  # Will not return(dump) password by doing this
        dump_only = ("id", "activated")  # Will not be looked at when creating the model
