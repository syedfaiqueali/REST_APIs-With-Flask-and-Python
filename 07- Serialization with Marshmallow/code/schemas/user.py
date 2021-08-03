from marshmallow import Schema, fields


class UserSchema(Schema):
    # Tell marshmallow that password field is only for loading data
    class Meta:
        load_only = ("password",)  # Will not return password by doing this
        dump_only = ("id",)

    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
