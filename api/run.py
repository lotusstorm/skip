from flask import Flask
from app import api_bp
from Structures import db
from flask_cors import CORS


def create_app(config_filename):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_filename)
    app.register_blueprint(api_bp, url_prefix='/api')
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
