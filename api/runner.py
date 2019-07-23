# -*- coding: utf-8 -*-
from gevent.pywsgi import WSGIServer
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
    application = create_app("config")
    # application.run()
    http_server = WSGIServer(('0.0.0.0', 5000), application)
    http_server.serve_forever()
