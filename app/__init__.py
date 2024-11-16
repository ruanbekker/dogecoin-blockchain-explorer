import timeago
from flask import Flask
from datetime import datetime
from config import Config

def datetimeformat(value, format="%Y-%m-%d %H:%M:%S"):
    return datetime.fromtimestamp(value).strftime(format)

def timeago_filter(value):
    return timeago.format(datetime.fromtimestamp(value), datetime.now())


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    from .routes import routes
    app.register_blueprint(routes)

    # Add custom Jinja filters
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['timeago'] = timeago_filter

    return app

