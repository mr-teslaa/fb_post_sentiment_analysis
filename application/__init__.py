from flask import Flask
from application.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from application.public.views import public
    app.register_blueprint(public)

    return app