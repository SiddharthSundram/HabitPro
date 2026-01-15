from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize Extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login' 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Create DB Tables
    with app.app_context():
        db.create_all()

        # SEED ACHIEVEMENTS
        from app.models import Achievement
        if not Achievement.query.first():
            badges = [
                Achievement(name="First Step", description="Log your first habit", icon="fas fa-shoe-prints", criteria_type="total_logs", threshold=1, color="text-blue-500"),
                Achievement(name="Consistency is Key", description="Reach a 7-day streak", icon="fas fa-fire", criteria_type="streak", threshold=7, color="text-orange-500"),
                Achievement(name="Habit Master", description="Reach a 30-day streak", icon="fas fa-crown", criteria_type="streak", threshold=30, color="text-purple-500"),
                Achievement(name="Century Club", description="Log 100 total activities", icon="fas fa-medal", criteria_type="total_logs", threshold=100, color="text-yellow-500"),
                Achievement(name="Gym Rat", description="Complete 10 Health habits", icon="fas fa-dumbbell", criteria_type="category_health", threshold=10, color="text-green-500")
            ]
            db.session.add_all(badges)
            db.session.commit()
            print("Achievements Seeded!")

    return app