from flask import Flask

from app.views.report_view import generate_report_data
from config import Config
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.add_url_rule('/report/<string:date>', 'report', generate_report_data, methods=['GET'])

    return app
