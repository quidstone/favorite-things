from flask import g, request, jsonify, abort
from api.models import db, Item, Category
from sqlalchemy.exc import SQLAlchemyError
from api.schemas import ItemSchema, CategorySchema
from flask_cors import cross_origin
import time

# app global variables
SERVER_ERROR_MSG = '''there is a problem with our server right now, please be
sure to try after some time'''


def end_of_loop():
    raise StopIteration


def readjust_ranking(new_rank, previous_rank, category_id, is_firsttime):
    """updating existing item by ranking in table"""
    is_descending = False
    start_at = new_rank
    stop_at = previous_rank - 1  # not affecting previous rank as it should get updated
    if(not is_firsttime
       and previous_rank is not None and previous_rank < new_rank):
        """item rank is descending"""
        start_at = previous_rank + 1
        stop_at = new_rank
        is_descending = True

    if not is_firsttime:
        query_str = "select ranking from items where ranking >= {}\
                    and ranking <= {} and category_id={}\
                    order by ranking asc"\
        .format(start_at, stop_at, category_id)
    else:
        query_str = "select ranking from items where ranking >= {}\
                    and category_id={}\
                    order by ranking asc"\
        .format(start_at, category_id)

    db_items = list(db.engine.execute(query_str))
    print(query_str)
    db_item_length = len(db_items)
    no_diffs_greater_than_one_length = db_item_length - 1
    list_range = db_item_length-1
    diffs = list(end_of_loop() if db_items[i]._row[0]-db_items[i]._row[0] > 1
                 else db_items[i+1]._row[0]-db_items[i]._row[0]
                 for i in range(list_range))

    """checking if theres a 2 diff in the range"""
    if(len(diffs) < no_diffs_greater_than_one_length):
        update_rank_up_to = db_items[len(diffs)]._row[0]
    else:
        update_rank_up_to = str(db_items[db_item_length-1]._row[0])
    stop_update_at = db_items[0]._row[0]

    if not is_descending:
        update_query = "UPDATE items SET ranking = ranking + 1 WHERE \
            ranking <={} and ranking >= {} and category_id = {}"\
            .format(update_rank_up_to, stop_update_at, category_id)
    else:
        update_query = "UPDATE items SET ranking = ranking - 1 WHERE \
            ranking <={} and ranking >= {} and category_id = {}"\
            .format(update_rank_up_to, stop_update_at, category_id)
    print(update_query)
    result = db.engine.execute(update_query)

    # if(result.rowcount):
    #     return ()
    return result


def init_routes(app):

    # Init Item schema
    item_schema = ItemSchema(strict=True)
    items_schema = ItemSchema(many=True, strict=True)

    # Init Category schema
    category_schema = CategorySchema(strict=True)
    categories_schema = CategorySchema(many=True, strict=True)

    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.before_request
    def log_request():
        # if request.path == '/favicon.ico':
        #     return response
        # elif request.path.startswith('/static'):
        #     return response

        now = time.time()
        duration = round(now - g.start, 2)
        #dt = datetime.datetime.fromtimestamp(now)
        #timestamp = rfc3339(dt, utc=True)

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        host = request.host.split(':', 1)[0]
        print("ip {} host {}".format(ip, host))
        if request.args:
            args = dict(request.args)
            print("args {}", args)

    # Create an Item
    @app.route('/item', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def add_item():
        ranking = request.json['ranking']
        category_id = request.json['category_id']
        same_rank_item = Item.query.filter_by(
            ranking=ranking, category_id=category_id).first()
        if same_rank_item is not None:
            readjust_ranking(int(ranking), None, int(
                category_id), is_firsttime=True)
        title = request.json['title']
        des = request.json['description']

        item_meta = request.json['item_meta']

        new_item = Item(title, des, ranking, category_id, item_meta)
        try:
            new_item.save()
        except SQLAlchemyError as e:
            print(e.args[0])
            errorMsg = SERVER_ERROR_MSG
            return jsonify(error=errorMsg),\
                500, {'Content-Type': 'application/json; charset=utf-8'}
        return (item_schema.jsonify(new_item),
                201, {'Content-Type': 'application/json; charset=utf-8'})

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
        if db_category is None:
            abort(404)
        all_items = Item.query.filter_by(category_id=id)
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
        same_rank_item = Item.query.filter_by(ranking=ranking,
                                              category_id=category_id).first()
        if same_rank_item is not None:
            readjust_ranking(int(ranking), int(db_item.ranking),
                             int(category_id), is_firsttime=False)

        item_meta = request.json['item_meta']

        db_item.title = title
        db_item.desc = desc
        db_item.category_id = category_id
        db_item.item_meta = item_meta
        db_item.ranking = ranking

        now = time.strftime('%Y-%m-%d %H:%M:%S')
        db_item.modified_date = now
        try:
            db_item.update()
        except SQLAlchemyError:
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
        db_item.delete(db_item)

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
