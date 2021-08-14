from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

convention = {
    "ix": "ix_%(column_0_label)s", #index names
    "uq": "uq_%(table_name)s_%(column_0_name)s",  #unique constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s", #check constraint
    "fk": "fk_%(table_name)s_%(column_0_name)_%(referred_table_name)s", #foreign key constraint
    "pk": "pk_%(table_name)s", # primary key constraint
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
