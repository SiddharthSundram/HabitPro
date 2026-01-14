from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize Extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # Redirect here if user isn't logged in

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints (Routes)
    from app.routes import main
    app.register_blueprint(main)

    # Create DB Tables if they don't exist
    with app.app_context():
        db.create_all()

    return app