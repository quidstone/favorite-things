from flask import Flask
from flask_cors import CORS


def create_app(run_filename):
    app = Flask(run_filename)
    from api.models import db
    CORS(app, support_credentials=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = '''mysql://rahat:Nopass1234!@192.168.5.5/favourite_things'''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from api.routes import init_routes
    init_routes(app)
    return app
