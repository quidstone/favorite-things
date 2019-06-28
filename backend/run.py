from api import create_app


# Run Server
if __name__ == '__main__':
    app = create_app(__name__)
    app.run(debug=True)
