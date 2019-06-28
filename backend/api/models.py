import time
from flask_sqlalchemy import SQLAlchemy

# Init db
db = SQLAlchemy()


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.Text, nullable=True)
    ranking = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    item_metadata = db.Column(db.JSON)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, title, desc, ranking, category_id, meta):
        """initialize with params."""
        self.title = title
        self.desc = desc
        self.ranking = ranking
        self.category_id = category_id
        self.item_metadata = meta
        # print(meta)
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        self.created_date = now
        self.modified_date = now

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Item.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Category(db.Model):
    """
    Create an Category Table
    """
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Item.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
