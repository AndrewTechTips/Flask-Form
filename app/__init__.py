from flask import Flask
from app.config import Config
from app.extensions import db, mail


def create_app():
    # Point to root directories, for template and static assets
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    # Create tables inside the app context
    with app.app_context():
        db.create_all()

    return app
