from flask import Flask
from firebase_service import FirebaseService
import os

from routes.home_routes import home_routes


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(12).hex()

    app.config["FIREBASE_SERVICE"] = FirebaseService()

    app.register_blueprint(home_routes)

    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
