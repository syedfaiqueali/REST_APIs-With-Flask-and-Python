from marshmallow import pre_dump

from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    # Tell marshmallow that password field is only for loading data
    class Meta:
        model = UserModel  # Go into UserModel and look into column def & create marshmallow fields
        load_only = ("password",)  # Will not return(dump) password by doing this
        dump_only = (
            "id",
            "confirmation",
        )  # Will not be looked at when creating the model

        @pre_dump
        def _pre_dump(self, user: UserModel):
            """Whenever we resent the confirmation, the schema will not include old expired confirmations."""
            user.confirmation = [user.most_recent_confirmation]
            return user
