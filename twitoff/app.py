"""Main application and routing logic for Twitoff."""
from flask import Flask
from .models import DB 

def create_app():
    """Create and configure an instance of the flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/') 
    def root():
        return "Welcome to TwitOff!"
        
    return app 