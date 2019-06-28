from flask_marshmallow import Marshmallow

# Init marshmallow
ma = Marshmallow()


class ItemSchema(ma.Schema):
    # Fields to expose
    class Meta:
        fields = ('id', 'title', 'desc', 'ranking',
                  'category_id', 'item_metadata', 'created_date',
                  'modified_date')


class CategorySchema(ma.Schema):
    # Fields to expose
    class Meta:
        fields = ('id', 'name', 'created_date', 'modified_date')
