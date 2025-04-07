from .flask_routes import setup_flask_app
from flask import Flask


def main():
    app = setup_flask_app(Flask('app'))
    app.run(debug=True)
