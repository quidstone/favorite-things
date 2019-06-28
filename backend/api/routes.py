from flask import request, jsonify, abort
from api.models import db, Item, Category
from sqlalchemy.exc import SQLAlchemyError
from api.schemas import ItemSchema, CategorySchema
from flask_cors import cross_origin
import time

# app global variables
SERVER_ERROR_MSG = '''there is a problem with our server right now, please be 
sure to try after some time'''


def init_routes(app):

    # Init Item schema
    item_schema = ItemSchema(strict=True)
    items_schema = ItemSchema(many=True, strict=True)

    # Init Category schema
    category_schema = CategorySchema(strict=True)
    categories_schema = CategorySchema(many=True, strict=True)

    # Create an Item
    @app.route('/item', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def add_item():
        ranking = request.json['ranking']
        category_id = request.json['category_id']
        db_item = Item.query.filter_by(
            ranking=ranking, category_id=category_id).first()
        print(type(db_item))
        if db_item is not None:
            return jsonify(error="ranking taken,please use another ranking"), 406
        title = request.json['title']
        des = request.json['description']

        item_meta = request.json['item_meta']

        new_item = Item(title, des, ranking, category_id, item_meta)
        try:
            new_item.save()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e.args[0])
            errorMsg = SERVER_ERROR_MSG
            return jsonify(error=errorMsg), 500, {'Content-Type': 'application/json; charset=utf-8'}
        return (item_schema.jsonify(new_item), 201, {'Content-Type': 'application/json; charset=utf-8'})

    # Get All Items
    @app.route('/item', methods=['GET'])
    def get_items():
        all_items = Item.query.all()
        if len(all_items) == 0:
            return('', 204)
        result = items_schema.dump(all_items)
        return jsonify(result.data)

    # Get All Items per category
    @app.route('/category/<id>/items', methods=['GET', 'OPTIONS'])
    def get_items_per_category(id):
        db_category = Category.query.get(id)
        print(db_category)
        if db_category is None:
            abort(404)
        all_items = Item.query.filter_by(category_id=id)
        print(type(all_items))
        if all_items.count() == 0:
            return('', 204)
        result = items_schema.dump(all_items)
        return jsonify(result.data)

    # Get a single Item
    @app.route('/item/<id>', methods=['GET'])
    def get_item(id):
        item = Item.query.get(id)
        if item is None:
            abort(404)
        return item_schema.jsonify(item)

    # get available item rank
    @app.route('/item/check/availability/<rank>', methods=['GET'])
    def get_item_rank(rank):
        db_item = Item.query.filter_by(ranking=rank).first()
        print(type(db_item))
        if db_item is None:
            return "Okay"
        else:
            return "Taken", 406

    # Update an Item
    @app.route('/item/<id>', methods=['PUT'])
    def update_item(id):
        db_item = Item.query.get(id)
        if db_item is None:
            abort(404)
        title = request.json['title']
        desc = request.json['description']
        ranking = request.json['ranking']
        category_id = request.json['category_id']
        item_meta = request.json['item_meta']

        db_item.title = title
        db_item.desc = desc
        db_item.category_id = category_id
        db_item.item_meta = item_meta
        db_item.ranking = ranking

        now = time.strftime('%Y-%m-%d %H:%M:%S')
        db_item.modified_date = now
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            # errorMsg = e.args[0]
            errorMsg = SERVER_ERROR_MSG
            return jsonify(error=errorMsg), 500

        return item_schema.jsonify(db_item)

    # Delete an item
    @app.route('/item/<id>', methods=['DELETE'])
    def delete_product(id):
        db_item = Item.query.get(id)
        if db_item is None:
            abort(404)
        db.session.delete(db_item)
        db.session.commit()

        return item_schema.jsonify(db_item)

    '''now writing for category apis'''

    # create a category
    @app.route('/category', methods=['POST'])
    def add_category():
        name = request.json['name']
        category = Category(name)
        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError:
            # print(e)
            db.session.rollback()
            errorMsg = SERVER_ERROR_MSG
            return jsonify(error=errorMsg), 500

        return category_schema.jsonify(category)

    # get all categories
    @app.route('/category', methods=['GET', 'OPTIONS'])
    def get_categories():
        all_categories = Category.query.all()
        if len(all_categories) == 0:
            return('', 204)
        result = categories_schema.dump(all_categories)
        return jsonify(result.data)

    # get a category
    @app.route('/category/<id>', methods=['GET'])
    def get_category(id):
        db_category = Category.query.get(id)
        if db_category is None:
            abort(404)
        return category_schema.jsonify(db_category)

    # Delete a category
    @app.route('/category/<id>', methods=['DELETE'])
    def delete_category(id):
        db_category = Category.query.get(id)
        if db_category is None:
            abort(404)
        db.session.delete(db_category)
        db.session.commit()

        return category_schema.jsonify(db_category)
