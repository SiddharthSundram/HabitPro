from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_wtf.csrf import CSRFProtect 
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Extensions GLOBALLY
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # Redirects here if not logged in
login_manager.login_message_category = 'error'
csrf = CSRFProtect()
mail = Mail()

# Define Limiter here so it can be imported in routes.py
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init Extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    limiter.init_app(app) # Bind the limiter to the app
    
    # Register Blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Create DB Tables
    with app.app_context():
        # Import ALL models here so SQLAlchemy detects them
        from app.models import User, Habit, DailyLog, Achievement, UserAchievement, Feedback
        
        db.create_all()

        # SEED ACHIEVEMENTS (Only if empty)
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