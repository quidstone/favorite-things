from api import create_app


# Run Server
if __name__ == '__main__':
    app = create_app(__name__)
    app.run('0.0.0.0', port=5000, debug=True)
