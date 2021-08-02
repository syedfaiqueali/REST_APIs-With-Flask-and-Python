from db import db

class ItemModel(db.Model):
    # To Tell SQLAlchemy tablename and col_name
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # It will see store_id and find items belonging to that store
    # No needs for joins in SQLAlchemy
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id
        }

    @classmethod
    def find_by_name(cls, name):
        # return an item obj from db
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # Using both for insert and update
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
