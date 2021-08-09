from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage

# Custom Field
class FileStorageField(fields.Field):
    default_error_messages = {"invalid": "Not a valid image."}

    def _deserialize(self, value, attr, data) -> FileStorage:
        # If it exists
        if value is None:
            return None

        # If it is a file storage
        if not isinstance(value, FileStorage):
            self.fail("invalid")  # raises ValidationError

        return value


class ImageSchema(Schema):
    # Gets a required file storage field (img)
    image = FileStorageField(required=True)
